import os
import sqlite3
from User_data_managing.constants import *


def write_content_to_file(path, content):
    # if file doesn't exist yet it will be created
    with open(path, 'w+', encoding='utf8') as file:
        file.write(content)


def get_file_content(path, start=0, number_of_bytes=-1):
    # start and number_of_bytes are used ro read particular diapason of bytes
    with open(path, encoding='utf8') as file:
        # if bytes range is wrong and exception is raised
        # then function returns full file content
        # that can occur when user enter book text not in language being studied
        try:
            file.seek(start)
            return file.read(number_of_bytes)
        except Exception:
            file.seek(0)
            return file.read()


def dec_convert_result_to_list_of_values(func):
    def new_func(*args, **kwargs):
        res = func(*args, **kwargs)
        try:
            return list(map(lambda x: x[0], res))
        except (IndexError, TypeError):
            return res

    return new_func


def dec_convert_result_to_single_value(func):
    def new_func(*args, **kwargs):
        res = func(*args, **kwargs)
        try:
            return res[0][0]
        except (IndexError, TypeError):
            return res

    return new_func


class DataManagingHelper:
    def __init__(self):
        self.con = sqlite3.connect(PATH_TO_DATA_DIRECTORY + '\\database.sqlite')
        self.cur = self.con.cursor()

    def execute(self, query, *query_args):
        if 'UPDATE' in query or 'INSERT' in query or 'DELETE' in query:
            self.cur.execute(query, query_args)
            self.con.commit()
        else:
            res = self.cur.execute(query, query_args).fetchall()
            return res


# base class for all data managers
class DataManager(DataManagingHelper):
    def __init__(self, language_abbreviation=None):
        super(DataManager, self).__init__()
        self.language = language_abbreviation


# settings are stored withing sqlite file
# settings manager can access them by id
class SettingsManager(DataManagingHelper):
    def __init__(self, kind=None):
        super(SettingsManager, self).__init__()
        self.type = kind

    @dec_convert_result_to_single_value
    def get_value(self, setting_id):
        query = 'SELECT value FROM Settings WHERE id = ?'
        return self.execute(query, setting_id)

    def change_value(self, setting_id, new_value):
        query = 'UPDATE Settings SET value = ? WHERE id = ?'
        self.execute(query, new_value, setting_id)

    def get_all(self):
        query = 'SELECT Settings.title, Settings.value FROM Settings'
        if self.type:
            query += f'JOIN SettingsTypes ON Settings.setting_type_id = SettingsTypes.id ' \
                     f'WHERE SettingsTypes.title = "{self.type}"'
        return self.execute(query)
