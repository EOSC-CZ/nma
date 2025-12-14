import logging
import traceback
from collections.abc import Mapping
from functools import wraps

from flask import (
    Blueprint,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required
from flask_menu import current_menu
from invenio_app_rdm.records_ui.views.decorators import no_cache_response
from invenio_i18n import lazy_gettext as _
from invenio_pidstore.errors import PIDAlreadyExists
from invenio_records_resources.services.errors import (
    PermissionDeniedError,
)
from markupsafe import Markup, escape
from oarepo_runtime.typing import record_from_result
from oarepo_ui.overrides import UIComponent
from oarepo_ui.overrides.components import UIComponentImportMode
from oarepo_ui.proxies import current_oarepo_ui
from oarepo_ui.resources import BabelComponent
from oarepo_ui.resources.components import (
    AllowedHtmlTagsComponent,
    EmptyRecordAccessComponent,
    FilesComponent,
    FilesLockedComponent,
    FilesQuotaAndTransferComponent,
    PermissionsComponent,
    RecordRestrictionComponent,
)
from oarepo_ui.resources.components.custom_fields import CustomFieldsComponent
from oarepo_ui.resources.decorators import (
    allow_method,
    pass_record_latest,
    pass_route_args,
    secret_link_or_login_required,
)
from oarepo_ui.resources.records.config import RecordsUIResourceConfig
from oarepo_ui.resources.records.resource import RecordsUIResource
from oarepo_ui.utils import can_view_deposit_page
from werkzeug.exceptions import HTTPException

from riv.records.create_record import create_record
from riv.resolvers.base import resolve_metadata
from riv.views import RegisterForm

from ui.resources.components.rdm_vocabularies import RDMVocabularyOptionsComponent

logger = logging.getLogger("DatasetsUI")


class DatasetsUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "templates"
    url_prefix = "/datasets"
    blueprint_name = "datasets_ui"
    model_name = "datasets"

    search_component = UIComponent(
        "DatasetsResultsListItem",
        "@js/datasets/search/ResultsListItem",
        UIComponentImportMode.DEFAULT,
    )

    routes: Mapping[str, str] = {
        "search": "",
        "deposit_create": "/uploads/new",
        "deposit_edit": "/uploads/<path:pid_value>",
        "record_detail": "/records/<path:pid_value>",
        "record_latest": "/records/<path:pid_value>/latest",
        "record_export": "/records/<path:pid_value>/export/<export_format>",
    }

    components = [
        AllowedHtmlTagsComponent,
        BabelComponent,
        PermissionsComponent,
        FilesComponent,
        # AllowedCommunitiesComponent,
        CustomFieldsComponent,
        RecordRestrictionComponent,
        EmptyRecordAccessComponent,
        FilesLockedComponent,
        FilesQuotaAndTransferComponent,
        RDMVocabularyOptionsComponent,
    ]

    record_detail_permissions = [
        "update",
        "manage",
        "read_files",
        "view",
    ]

    deposit_edit_permissions = [
        "manage",
        "update",
    ]

    deposit_create_permissions = [
        "manage",
        "create",
    ]

    application_id = "datasets"

    templates = {
        "record_detail": "datasets.RecordDetail",
        "search": "datasets.Search",
        "deposit_edit": "datasets.DepositEdit",
        "deposit_create": "datasets.Deposit",
    }


# call internal function and catch any errors
def handle_riv_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except HTTPException as http_exc:
            logger.exception("HTTP error")
            return abort(http_exc.code)

        except PermissionError:
            logger.exception("PermissionError while calling %s", func.__name__)
            return abort(403)

        except Exception as exc:
            logger.exception("Unexpected error in %s", func.__name__)
            raise
            return (
                render_template(
                    "datasets/errors/riv_error_page.jinja",
                    error=str(exc),
                    stack=traceback.format_exc(),
                ),
                500,
            )

    return wrapper


class DatasetsUIResource(RecordsUIResource):
    @login_required
    @allow_method(["GET", "POST"])
    @handle_riv_errors
    def deposit_create(self):
        """Create and publish record by persistent identifier. Generate secret link and send email to user. Grant access to support."""
        form = RegisterForm()
        if form.validate_on_submit():
            pid = form.pid.data

            try:
                metadata, problems = resolve_metadata(pid)
                record_data = {"metadata": metadata}
                secret_link = create_record(record_data, problems)
                if not problems:
                    flash(f"Successfully registered dataset with PID: {pid}", "success")
                    return redirect(
                        url_for(
                            "datasets_ui.record_detail", pid_value=record_data["id"]
                        )
                    )
                else:
                    # Sanitize problem messages to prevent XSS
                    issues_list = "".join(
                        [f"<li>{escape(problem.message)}</li>" for problem in problems]
                    )
                    warning_message = Markup(
                        f'<div class="header">'
                        f'<i class="exclamation triangle icon"></i>'
                        f'{_("Dataset was registered with issues. Please check/correct the metadata below:")}'
                        f"</div>"
                        f'<ul class="list">{issues_list}</ul>'
                    )
                    flash(warning_message, "warning")
                    return redirect(secret_link)
            except PIDAlreadyExists:
                flash(_("This dataset is already registered."), "info")
                return redirect(
                    url_for("datasets_ui.record_detail", pid_value=record_data["id"])
                )
            except Exception as e:
                logger.exception("Error registering dataset with PID %s", pid)
                flash(f"Error registering dataset: {str(e)}", "error")
                return redirect(url_for("datasets_ui.deposit_create"))

        return current_oarepo_ui.catalog.render(
            self.get_jinjax_macro(
                "deposit_create",
            ),
            **{"form": form},
        )

    @pass_route_args("view")
    @secret_link_or_login_required()
    @pass_record_latest
    @no_cache_response
    def deposit_edit(self, record, draft_files=None, files_locked=True, **kwargs):
        """Edit draft record."""
        if not self.api_service.check_permission(
            g.identity, "update", record=record_from_result(record)
        ):
            raise PermissionDeniedError(
                _("User does not have permission to edit record.")
            )

        return self._edit(record, draft_files, files_locked, **kwargs)


def ui_overrides(app):
    """Register UI overrides."""
    ui_resource_config = DatasetsUIResourceConfig()

    if (
        current_oarepo_ui is not None
        and ui_resource_config.model
        and ui_resource_config.model.record_json_schema
        and ui_resource_config.search_component
    ):
        current_oarepo_ui.register_result_list_item(
            ui_resource_config.model.record_json_schema,
            ui_resource_config.search_component,
        )


def init_menu(app):
    """Initialize menu before first request."""
    ui_resource_config = DatasetsUIResourceConfig()
    with app.app_context():
        current_menu.submenu("plus.create_datasets").register(
            f"{ui_resource_config.blueprint_name}.deposit_create",
            _("Register a Dataset"),
            order=1,
            visible_when=can_view_deposit_page,
        )


def search_redirect():
    """Redirect from /search to /datasets while persisting query args."""
    return redirect(url_for("datasets_ui.search", **request.args))


def finalize_app(app):
    """Finalize app"""
    init_menu(app)
    ui_overrides(app)


def create_blueprint(app):
    """Register blueprint for this resource."""

    blueprint = DatasetsUIResource(DatasetsUIResourceConfig()).as_blueprint()
    return blueprint


def create_record_detail_redirect_blueprint(app):
    """Blueprint containing route redirecting to ui record detail."""
    from flask import redirect as flask_redirect

    bp = Blueprint("pidresolver", __name__)

    @bp.route("/s/<path:pid_value>")
    def redirect(pid_value):
        return flask_redirect(url_for("datasets_ui.record_detail", pid_value=pid_value))

    return bp


# TODO: register init_menu to finalize_app similarly blueprints & webpack is registered
