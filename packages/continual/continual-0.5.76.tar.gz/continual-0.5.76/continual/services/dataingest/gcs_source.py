import logging
import os
import traceback
import logging


from continual.python.sdk.exceptions import InternalError, InvalidArgumentError
from continual.python.blob.store import BlobStore
from continual.python.utils.utils import read_csv
from tableschema import Table


def is_column_categorical(series):
    unique_count = series.nunique(dropna=False)
    total_count = len(series)
    return total_count > unique_count


class FeatureSourceCloudStore:
    def __init__(self, id, filename):

        self.filename = filename
        self._id = id
        if filename is not None and len(filename) > 0:
            if not filename.startswith("gs://"):
                raise InvalidArgumentError(
                    "only google cloud store source supported", None
                )
            self.blob_store = BlobStore(filename)
        else:
            raise InvalidArgumentError("source is not file type", None)

    def _build_object_list(self):
        objects = []
        if self.filename is not None and len(self.filename) > 0:
            objects.append(self.filename)
        return objects

    def fetch_all(self):
        output = "/tmp/" + self._id
        self.file_path = self.blob_store.download_file(self.filename, outpath=output)
        return read_csv(self.file_path)

    def fetch_data(self, page_size=10000):
        objects = self._build_object_list()

        class BlobIterator:
            def __init__(self, id, blob_store, objects):
                self._blob_store = blob_store
                self._id = id
                self._objects = objects
                self._current_index = 0
                self.chunker = None
                self.file_path = None

            def __iter__(self):
                self._current_pointer = 0
                self.chunker = None
                return self

            def __next__(self):
                if self.chunker is not None:
                    return next(self.chunker)

                if (
                    self._current_index >= len(self._objects)
                    and self.file_path is not None
                ):
                    os.remove(self.file_path)
                    raise StopIteration

                output = "/tmp/" + self._id
                self.file_path = self._blob_store.download_file(
                    self._objects[self._current_index], outpath=output
                )
                logging.info("Downloaded " + self.file_path)
                self.chunker = read_csv(self.file_path, chunksize=page_size)

                self._current_index = self._current_index + 1
                return next(self.chunker)

        return BlobIterator(self._id, self.blob_store, objects)

    def infer_schema(self, filename, sample_row_count=100):

        # Download the file from the blob store.
        self.blob_store = BlobStore(filename)
        file_path = self.blob_store.download_file(filename, outpath="/tmp")
        logging.info("Downloaded " + file_path)

        inferred_schema = {"metadata": {}, "features": {}, "entities": {}, "models": {}}
        try:
            table = Table(file_path)
            table.infer()
            for f in table.schema.descriptor["fields"]:
                col = f["name"].strip()
                if col == "":
                    continue
                elif col.lower() == "id":
                    inferred_schema["metadata"][col] = "TEXT"
                    continue

                if len(col) > 63:
                    print("SKIPPING ", col)
                    continue

                if f["type"] == "boolean":
                    inferred_schema["features"][col] = "BOOLEAN"
                elif f["type"] == "number" or f["type"] == "integer":
                    inferred_schema["features"][col] = "NUMBER"
                elif f["type"] == "string":
                    inferred_schema["features"][col] = "TEXT"

            self.chunker = read_csv(file_path, chunksize=sample_row_count or 1)
            df = next(self.chunker)

            # Determine categorical columns.
            for k in inferred_schema["features"]:
                if inferred_schema["features"][k] != "TEXT":
                    continue
                if k in df.columns and is_column_categorical(df[k]):
                    inferred_schema["features"][k] = "CATEGORICAL"

            return inferred_schema, df

        except Exception:
            traceback.print_exc()
            raise InternalError("could not read source")

    def close(self):
        self._blob_store = None
