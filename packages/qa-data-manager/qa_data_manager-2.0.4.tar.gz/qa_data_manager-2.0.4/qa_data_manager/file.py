import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import Files


class File:
    def __init__(self, file_path, file_name, file_size, file_extension):
        self._created_at = datetime.datetime.now()
        self._deleted_at = None
        self._extension = file_extension  # jpg
        self._file = file_path  # /my_compucter/my_files/test.jpg
        self._name = file_name  # test.jpg
        self._preview_for = None
        self._size = file_size  # 210

    def with_deleted_at(self):
        self._deleted_at = datetime.datetime.now()
        return self

    def with_previously_uploaded_file(self, hour):
        self._created_at = datetime.datetime.now() - datetime.timedelta(hours=int(hour))
        return self

    def generate(self):
        file = Files(created_at=self._created_at,
                     deleted_at=self._deleted_at,
                     extension=self._extension,
                     file=self._file,
                     name=self._file,
                     preview_for=self._preview_for,
                     size=self._size,
                     updated_at=self._created_at)

        file.save()
        return model_to_dict(file)
