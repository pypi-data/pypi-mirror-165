import os
from os.path import join
from pathlib import Path
from typing import Iterable, Literal, Optional, Sequence, Set, Tuple, Type, get_args

from dlt.common import json, pendulum
from dlt.common.file_storage import FileStorage
from dlt.common.dataset_writers import TLoaderFileFormat, write_jsonl, write_insert_values
from dlt.common.configuration import LoadVolumeConfiguration
from dlt.common.exceptions import TerminalValueError
from dlt.common.schema import Schema, TSchemaUpdate, TTableSchemaColumns
from dlt.common.storages.versioned_storage import VersionedStorage
from dlt.common.typing import DictStrAny, StrAny

from dlt.common.storages.exceptions import JobWithUnsupportedWriterException


# folders to manage load jobs in a single load package
TWorkingFolder = Literal["new_jobs", "failed_jobs", "started_jobs", "completed_jobs"]

class LoadStorage(VersionedStorage):

    STORAGE_VERSION = "1.0.0"
    NORMALIZED_FOLDER = "normalized"  # folder within the volume where load packages are stored
    LOADED_FOLDER = "loaded"  # folder to keep the loads that were completely processed

    NEW_JOBS_FOLDER: TWorkingFolder = "new_jobs"
    FAILED_JOBS_FOLDER: TWorkingFolder = "failed_jobs"
    STARTED_JOBS_FOLDER: TWorkingFolder = "started_jobs"
    COMPLETED_JOBS_FOLDER: TWorkingFolder = "completed_jobs"

    LOAD_SCHEMA_UPDATE_FILE_NAME = "schema_updates.json"
    SCHEMA_FILE_NAME = "schema.json"

    ALL_SUPPORTED_FILE_FORMATS: Set[TLoaderFileFormat] = set(get_args(TLoaderFileFormat))

    def __init__(
        self,
        is_owner: bool,
        C: Type[LoadVolumeConfiguration],
        preferred_file_format: TLoaderFileFormat,
        supported_file_formats: Iterable[TLoaderFileFormat]
    ) -> None:
        if not LoadStorage.ALL_SUPPORTED_FILE_FORMATS.issuperset(supported_file_formats):
            raise TerminalValueError(supported_file_formats)
        if preferred_file_format not in supported_file_formats:
            raise TerminalValueError(preferred_file_format)
        self.preferred_file_format = preferred_file_format
        self.supported_file_formats = supported_file_formats
        self.delete_completed_jobs = C.DELETE_COMPLETED_JOBS
        super().__init__(LoadStorage.STORAGE_VERSION, is_owner, FileStorage(C.LOAD_VOLUME_PATH, "t", makedirs=is_owner))

    def initialize_storage(self) -> None:
        self.storage.create_folder(LoadStorage.LOADED_FOLDER, exists_ok=True)
        self.storage.create_folder(LoadStorage.NORMALIZED_FOLDER, exists_ok=True)

    def create_temp_load_folder(self, load_id: str) -> None:
        # delete previous version
        if self.storage.has_folder(load_id):
            self.storage.delete_folder(load_id, recursively=True)
        self.storage.create_folder(load_id)
        # create processing directories
        self.storage.create_folder(join(load_id, LoadStorage.NEW_JOBS_FOLDER))
        self.storage.create_folder(join(load_id, LoadStorage.COMPLETED_JOBS_FOLDER))
        self.storage.create_folder(join(load_id, LoadStorage.FAILED_JOBS_FOLDER))
        self.storage.create_folder(join(load_id, LoadStorage.STARTED_JOBS_FOLDER))

    def write_temp_loading_file(self, load_id: str, table_name: str, table: TTableSchemaColumns, file_id: str, rows: Sequence[StrAny]) -> str:
        file_name = self.build_loading_file_name(load_id, table_name, file_id)
        with self.storage.open_file(file_name, mode="w") as f:
            if self.preferred_file_format == "jsonl":
                write_jsonl(f, rows)
            elif self.preferred_file_format == "insert_values":
                write_insert_values(f, rows, table.keys())
        return Path(file_name).name

    def load_schema(self, load_id: str) -> Schema:
        # load schema from a load package to be processed
        schema_path = join(self.get_load_path(load_id), LoadStorage.SCHEMA_FILE_NAME)
        return self._load_schema(schema_path)

    def load_temp_schema(self, load_id: str) -> Schema:
        # load schema from a temporary load package
        schema_path = join(load_id, LoadStorage.SCHEMA_FILE_NAME)
        return self._load_schema(schema_path)

    def save_temp_schema(self, schema: Schema, load_id: str) -> str:
        # save a schema to a temporary load package
        dump = json.dumps(schema.to_dict())
        return self.storage.save(join(load_id, LoadStorage.SCHEMA_FILE_NAME), dump)

    def save_temp_schema_updates(self, load_id: str, schema_updates: Sequence[TSchemaUpdate]) -> None:
        with self.storage.open_file(join(load_id, LoadStorage.LOAD_SCHEMA_UPDATE_FILE_NAME), mode="w") as f:
            json.dump(schema_updates, f)

    def commit_temp_load_folder(self, load_id: str) -> None:
        self.storage.atomic_rename(load_id, self.get_load_path(load_id))

    def list_loads(self) -> Sequence[str]:
        loads = self.storage.list_folder_dirs(LoadStorage.NORMALIZED_FOLDER, to_root=False)
        # start from the oldest packages
        return sorted(loads)

    def list_completed_loads(self) -> Sequence[str]:
        loads = self.storage.list_folder_dirs(LoadStorage.LOADED_FOLDER, to_root=False)
        # start from the oldest packages
        return sorted(loads)

    def list_new_jobs(self, load_id: str) -> Sequence[str]:
        new_jobs = self.storage.list_folder_files(join(self.get_load_path(load_id), LoadStorage.NEW_JOBS_FOLDER))
        # make sure all jobs have supported writers
        wrong_job = next((j for j in new_jobs if LoadStorage.parse_load_file_name(j)[1] not in self.supported_file_formats), None)
        if wrong_job is not None:
            raise JobWithUnsupportedWriterException(load_id, self.supported_file_formats, wrong_job)
        return new_jobs

    def list_started_jobs(self, load_id: str) -> Sequence[str]:
        return self.storage.list_folder_files(join(self.get_load_path(load_id), LoadStorage.STARTED_JOBS_FOLDER))

    def list_failed_jobs(self, load_id: str) -> Sequence[str]:
        return self.storage.list_folder_files(join(self.get_load_path(load_id), LoadStorage.FAILED_JOBS_FOLDER))

    def list_archived_failed_jobs(self, load_id: str) -> Sequence[str]:
        return self.storage.list_folder_files(join(self.get_archived_path(load_id), LoadStorage.FAILED_JOBS_FOLDER))

    def begin_schema_update(self, load_id: str) -> Optional[TSchemaUpdate]:
        schema_update_file = join(self.get_load_path(load_id), LoadStorage.LOAD_SCHEMA_UPDATE_FILE_NAME)
        if self.storage.has_file(schema_update_file):
            schema_update: TSchemaUpdate = json.loads(self.storage.load(schema_update_file))
            return schema_update
        else:
            return None

    def commit_schema_update(self, load_id: str) -> None:
        load_path = self.get_load_path(load_id)
        schema_update_file = join(load_path, LoadStorage.LOAD_SCHEMA_UPDATE_FILE_NAME)
        self.storage.atomic_rename(
            schema_update_file, join(load_path, LoadStorage.COMPLETED_JOBS_FOLDER, LoadStorage.LOAD_SCHEMA_UPDATE_FILE_NAME)
        )

    def start_job(self, load_id: str, file_name: str) -> str:
        return self._move_file(load_id, LoadStorage.NEW_JOBS_FOLDER, LoadStorage.STARTED_JOBS_FOLDER, file_name)

    def fail_job(self, load_id: str, file_name: str, failed_message: Optional[str]) -> str:
        load_path = self.get_load_path(load_id)
        if failed_message:
            self.storage.save(join(load_path, LoadStorage.FAILED_JOBS_FOLDER, file_name) + ".exception", failed_message)
        # move to failed jobs
        return self._move_file(load_id, LoadStorage.STARTED_JOBS_FOLDER, LoadStorage.FAILED_JOBS_FOLDER, file_name)

    def retry_job(self, load_id: str, file_name: str) -> str:
        return self._move_file(load_id, LoadStorage.STARTED_JOBS_FOLDER, LoadStorage.NEW_JOBS_FOLDER, file_name)

    def complete_job(self, load_id: str, file_name: str) -> str:
        return self._move_file(load_id, LoadStorage.STARTED_JOBS_FOLDER, LoadStorage.COMPLETED_JOBS_FOLDER, file_name)

    def archive_load(self, load_id: str) -> None:
        load_path = self.get_load_path(load_id)
        has_failed_jobs = len(self.list_failed_jobs(load_id)) > 0
        # delete load that does not contain failed jobs
        if self.delete_completed_jobs and not has_failed_jobs:
            self.storage.delete_folder(load_path, recursively=True)
        else:
            archive_path = self.get_archived_path(load_id)
            self.storage.atomic_rename(load_path, archive_path)

    def get_load_path(self, load_id: str) -> str:
        return join(LoadStorage.NORMALIZED_FOLDER, load_id)

    def get_archived_path(self, load_id: str) -> str:
        return join(LoadStorage.LOADED_FOLDER, load_id)

    def build_loading_file_name(self, load_id: str, table_name: str, file_id: str) -> str:
        file_name = f"{table_name}.{file_id}.{self.preferred_file_format}"
        return join(load_id, LoadStorage.NEW_JOBS_FOLDER, file_name)

    def _save_schema(self, schema: Schema, load_id: str) -> str:
        dump = json.dumps(schema.to_dict())
        schema_path = join(self.get_load_path(load_id), LoadStorage.SCHEMA_FILE_NAME)
        return self.storage.save(schema_path, dump)

    def _load_schema(self, schema_path: str) -> Schema:
        stored_schema: DictStrAny = json.loads(self.storage.load(schema_path))
        return Schema.from_dict(stored_schema)

    def _move_file(self, load_id: str, source_folder: TWorkingFolder, dest_folder: TWorkingFolder, file_name: str) -> str:
        load_path = self.get_load_path(load_id)
        dest_path = join(load_path, dest_folder, file_name)
        self.storage.atomic_rename(join(load_path, source_folder, file_name), dest_path)
        return self.storage._make_path(dest_path)

    def job_elapsed_time_seconds(self, file_path: str) -> float:
        return pendulum.now().timestamp() - os.path.getmtime(file_path)  # type: ignore

    def _get_file_path(self, load_id: str, folder: TWorkingFolder, file_name: str) -> str:
        load_path = self.get_load_path(load_id)
        return join(load_path, folder, file_name)

    @staticmethod
    def parse_load_file_name(file_name: str) -> Tuple[str, TLoaderFileFormat]:
        p = Path(file_name)
        ext: TLoaderFileFormat = p.suffix[1:]  # type: ignore
        if ext not in LoadStorage.ALL_SUPPORTED_FILE_FORMATS:
            raise TerminalValueError(ext)

        parts = p.stem.split(".")
        return (parts[0], ext)
