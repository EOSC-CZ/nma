from datasets.files.api import DatasetsFile
from datasets.records.api import DatasetsRecord
from datasets.resources.files.config import DatasetsFileResourceConfig
from datasets.resources.files.resource import DatasetsFileResource
from datasets.resources.records.config import DatasetsResourceConfig
from datasets.resources.records.resource import DatasetsResource
from datasets.services.files.config import DatasetsFileServiceConfig
from datasets.services.files.service import DatasetsFileService
from datasets.services.records.config import DatasetsServiceConfig
from datasets.services.records.service import DatasetsService

DATASETS_RECORD_RESOURCE_CONFIG = DatasetsResourceConfig


DATASETS_RECORD_RESOURCE_CLASS = DatasetsResource


DATASETS_RECORD_SERVICE_CONFIG = DatasetsServiceConfig


DATASETS_RECORD_SERVICE_CLASS = DatasetsService


OAREPO_PRIMARY_RECORD_SERVICE = {
    DatasetsRecord: "datasets",
    DatasetsFile: "datasets_file",
}


DATASETS_FILES_RESOURCE_CONFIG = DatasetsFileResourceConfig


DATASETS_FILES_RESOURCE_CLASS = DatasetsFileResource


DATASETS_FILES_SERVICE_CONFIG = DatasetsFileServiceConfig


DATASETS_FILES_SERVICE_CLASS = DatasetsFileService
