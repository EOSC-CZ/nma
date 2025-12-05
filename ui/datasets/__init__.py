import traceback
from functools import wraps

from flask import abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_menu import current_menu
from invenio_i18n import lazy_gettext as _
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
from oarepo_ui.resources.decorators import allow_method
from oarepo_ui.resources.records.config import RecordsUIResourceConfig
from oarepo_ui.resources.records.resource import RecordsUIResource
from oarepo_ui.utils import can_view_deposit_page
from werkzeug.exceptions import HTTPException

from riv.records.create_record import create_record
from riv.resolvers.base import resolve_metadata
from riv.views import RegisterForm


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

    routes = {
        **RecordsUIResourceConfig.routes,
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
    ]

    try:
        from oarepo_vocabularies.ui.resources.components import (
            DepositVocabularyOptionsComponent,
        )

        components.append(DepositVocabularyOptionsComponent)
    except ImportError:
        pass

    application_id = "datasets"

    templates = {
        "record_detail": "datasets.RecordDetail",
        "search": "datasets.Search",
        "deposit_edit": "datasets.Deposit",
        "deposit_create": "datasets.Deposit",
    }


# call internal function and catch any errors
def handle_riv_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except HTTPException as http_exc:
            current_app.logger.error(f"HTTP error: {http_exc}")
            return abort(http_exc.code)

        except PermissionError as exc:
            current_app.logger.error(
                f"PermissionError while calling {func.__name__}: {exc}"
            )
            return abort(403)

        except Exception as exc:
            current_app.logger.exception(f"Unexpected error in {func.__name__}: {exc}")

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
                metadata, _ = resolve_metadata(pid)
                record_data = {"metadata": metadata}
                create_record(record_data)

                flash(f"Successfully registered dataset with PID: {pid}", "success")
                return redirect(
                    url_for("datasets_ui.deposit_edit", pid_value=record_data['id'])
                )
            except Exception as e:
                flash(f"Error registering dataset: {str(e)}", "error")
                return redirect(url_for("datasets_ui.deposit_create"))

        return current_oarepo_ui.catalog.render(
            self.get_jinjax_macro(
                "deposit_create",
            ),
            **{"form": form},
        )


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
            _("New Datasets"),
            order=1,
            visible_when=can_view_deposit_page,
        )


def finalize_app(app):
    """Finalize app"""
    init_menu(app)
    ui_overrides(app)


def create_blueprint(app):
    """Register blueprint for this resource."""
    blueprint = DatasetsUIResource(DatasetsUIResourceConfig()).as_blueprint()
    return blueprint


# TODO: register init_menu to finalize_app similarly blueprints & webpack is registered
