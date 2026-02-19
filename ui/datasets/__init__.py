import logging
import traceback
from collections.abc import Mapping
from functools import wraps

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_menu import current_menu
from invenio_app_rdm.records_ui.views.decorators import no_cache_response
from invenio_i18n import lazy_gettext as _
from invenio_pidstore.errors import PIDAlreadyExists, PIDDoesNotExistError
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
    pass_query_args,
    pass_record_or_draft,
    pass_route_args,
)
from oarepo_ui.resources.records.config import RecordsUIResourceConfig
from oarepo_ui.resources.records.resource import RecordsUIResource
from oarepo_ui.utils import can_view_deposit_page
from werkzeug.exceptions import HTTPException

from riv.proxies import current_resolver_registry, current_riv_extension
from riv.records.api import generate_id
from riv.records.create_record import create_record
from riv.records.utils import create_user_edit_grant, user_edit_grant_and_notification
from riv.resolvers.base import PIDProcessingError, UnsupportedPIDError
from riv.views import RegisterForm
from ui.resources.components.oai_record import OAIRecordComponent
from ui.resources.components.placeholder_remover import PlaceholderRemoverComponent
from ui.resources.components.rdm_vocabularies import RDMVocabularyOptionsComponent
from ui.resources.components.support_contact import RDMSupportContactComponent

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
        OAIRecordComponent,
        PlaceholderRemoverComponent,
        RDMSupportContactComponent,
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
        **RecordsUIResourceConfig.templates,
        "deposit_create": "datasets.DepositCreate"
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
            if current_app.debug:
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

    @pass_query_args("search")
    def search(
        self,
        page: int = 1,
        size: int = 10,
        **kwargs,
    ):
        """Return search page.

        If the query string contains a URL (starts with https://),
        this method will:
        1. Check if the URL is resolvable (supported by our resolvers)
        2. Convert it to our internal ID format
        3. Check if a record with that ID exists
        4. Redirect to the record detail page if it exists
        5. Redirect to the registration page if it doesn't exist
        """
        query = request.args.get("q", "").strip()
        if query.startswith("https://") or query.startswith("http://"):
            try:
                possible_id = current_resolver_registry.generate_id(query)
                self.api_service.read(identity=g.identity, id_=possible_id)

                return redirect(
                    url_for("datasets_ui.record_detail", pid_value=possible_id)
                )
            except UnsupportedPIDError:
                pass
            except PIDDoesNotExistError:
                flash(
                    _(
                        "This dataset is not yet registered in the repository. "
                        "You can register it using the 'Obtain the link for RIV' button below."
                    ),
                    "info",
                )
                return redirect(url_for("datasets_ui.deposit_create", identifier=query))

        return self._search(page, size, **kwargs)

    @login_required
    @allow_method(["GET", "POST"])
    @handle_riv_errors
    def deposit_create(self):
        """Create and publish record by persistent identifier. Generate secret link and send email to user. Grant access to support."""

        identifier = request.args.get("identifier", "")

        if request.method == "GET" and identifier:
            form = RegisterForm(data={"pid": identifier})
        else:
            form = RegisterForm()

        if form.validate_on_submit():
            pid = form.pid.data

            try:
                # Normal flow: resolve metadata from the identifier
                record_data, problems = current_resolver_registry.resolve(pid)

                published_record = create_record(record_data, pid, problems)
                edit_link = url_for(
                    "datasets_ui.deposit_edit",
                    pid_value=published_record["id"],
                    _external=True,
                )

                if not problems:
                    flash(
                        _(
                            "Thank you for submitting the record to the National Metadata Directory. If you need to add a link to you RIV submission, please use the link below."
                        ),
                        "success",
                    )
                    return redirect(
                        url_for(
                            "datasets_ui.record_detail", pid_value=record_data["id"]
                        )
                    )
                else:
                    user_edit_grant_and_notification(record_data, problems)
                    # Sanitize problem messages to prevent XSS
                    issues_list = "".join(
                        [f"<li>{escape(problem.message)}</li>" for problem in problems]
                    )
                    warning_message = Markup(
                        f'<div class="header">'
                        f'<i class="exclamation triangle icon"></i>'
                        f'{_("Thank you for submitting the record to the National Metadata Directory. We detected some metadata issues within the record. To obtain a URL for RIV reporting, please check and correct the metadata below.")}'
                        f"</div>"
                        f'<ul class="list">{issues_list}</ul>'
                    )
                    flash(warning_message, "warning")
                    return redirect(edit_link)
            except PIDAlreadyExists as e:
                return redirect(
                    url_for("datasets_ui.record_detail", pid_value=e.pid_value)
                )
            except UnsupportedPIDError:
                flash(
                    _(
                        "The provided identifier is a URL that can not be registered at the moment. "
                        "If your dataset does not have a DOI or a handle in URL format, "
                        'please contact support at <a href="mailto:info@eosc.cz">info@eosc.cz</a>.'
                    ),
                    "error",
                )

            except PIDDoesNotExistError:
                flash(
                    _(
                        "The provided identifier does not exist. "
                        "Please check it for typos and try again. "
                        'If the problem persists, please contact support at <a href="mailto:info@eosc.cz">info@eosc.cz</a>.'
                    ),
                    "error",
                )
            except PIDProcessingError:
                flash(
                    _(
                        "We were unable to resolve metadata at the moment, please try it again later."
                        'If the problem persists, please contact support at <a href="mailto:info@eosc.cz">info@eosc.cz</a>.'
                    ),
                    "error",
                )
            except Exception as e:
                logger.exception("Error registering dataset with PID %s", pid)
                flash(_("Error registering dataset: %(error)s", error=str(e)), "error")

        render_kwargs = {
            "form": form,
        }

        return current_oarepo_ui.catalog.render(
            self.get_jinjax_macro(
                "deposit_create",
            ),
            **render_kwargs,
        )

    @pass_route_args("view")
    @login_required
    # Read latest has different serialization that makes some items behave differently later in the UI
    @pass_record_or_draft()
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
            _("Obtain the link for RIV"),
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


def create_registered_blueprint(app):
    """Blueprint containing registration success page."""
    bp = Blueprint("registered", __name__)

    @bp.route("/registered")
    def registered():
        if current_user is not None and current_user.is_authenticated:
            return redirect("/")
        return render_template("registered.html")

    return bp


# TODO: register init_menu to finalize_app similarly blueprints & webpack is registered
