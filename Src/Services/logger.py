import os
from datetime import datetime
from typing import Dict, Any
from Src.Core.validator import argument_exception

"""
Собственный логгер 
Поддерживает: консоль, файл, both. 
Настраиваемые уровни INFO/WARNING/ERROR.
"""


class logger:

    # Инициализация с проверкой настроек
    def __init__(self, settings: Dict[str, Any] = None):
        if settings is not None and not isinstance(settings, dict):
            raise argument_exception("settings must be dict or None")
        self.settings = settings or {}
        self._ensure_log_directory()

    # Ключи настроек (статические методы)
    @staticmethod
    def log_type_setting_key():  # "log_type"
        return "log_type"

    @staticmethod
    def show_info_logs_setting_key():  # "show_info_logs"
        return "show_info_logs"

    @staticmethod
    def show_warning_logs_setting_key():  # "show_warning_logs"
        return "show_warning_logs"

    @staticmethod
    def show_errors_logs_setting_key():  # "show_errors_logs"
        return "show_errors_logs"

    @staticmethod
    def log_path_setting_key():  # "log_path"
        return "log_path"


    # Функции установки параметров
    def set_log_type(self, log_type: str):
        # Устанавливает куда выводить: console/file/both
        if not isinstance(log_type, str):
            raise argument_exception("log_type must be str")
        if log_type not in ["console", "file", "both"]:
            raise argument_exception("wrong log_type, try one of this console/file/both")
        self.settings[self.log_type_setting_key()] = log_type


    # Вкл/выкл INFO логи
    def set_show_info_logs(self, show: bool):
        if not isinstance(show, bool):
            raise argument_exception("show must be bool")
        self.settings[self.show_info_logs_setting_key()] = show


    # Вкл/выкл WARNING логи
    def set_show_warning_logs(self, show: bool):
        if not isinstance(show, bool):
            raise argument_exception("show must be bool")
        self.settings[self.show_warning_logs_setting_key()] = show


    # Вкл/выкл ERROR логи
    def set_show_errors_logs(self, show: bool):
        if not isinstance(show, bool):
            raise argument_exception("show must be bool")
        self.settings[self.show_errors_logs_setting_key()] = show


    # Устанавливает путь к файлу логов
    def set_log_path(self, path: str):
        if not isinstance(path, str):
            raise argument_exception("path must be str")
        if not path.strip():
            raise argument_exception("path cannot be empty")
        self.settings[self.log_path_setting_key()] = path
        self._ensure_log_directory()


    # Основная функция логирования
    def log(self, message: str, log_type: str = "INFO"):
        if not isinstance(message, str):
            raise argument_exception("message must be str")
        if not isinstance(log_type, str):
            raise argument_exception("log_type must be str")

        log_type = log_type.upper()
        if log_type not in ["INFO", "WARNING", "ERROR"]:
            raise argument_exception("log_type must be INFO/WARNING/ERROR")

        # Проверяем разрешен ли этот тип лога
        show_key = {
            "INFO": self.show_info_logs_setting_key(),
            "WARNING": self.show_warning_logs_setting_key(),
            "ERROR": self.show_errors_logs_setting_key()
        }.get(log_type)

        if not self.settings.get(show_key, True):
            return  # Тип лога отключен

        # Формируем строку лога: "2025-12-08 12:44:00 - INFO - сообщение"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{timestamp} - {log_type} - {message}\n"

        # Выводим по настройкам
        output_type = self.settings.get(self.log_type_setting_key(), "console")
        if output_type not in ["console", "file", "both"]:
            output_type = "console"  # fallback

        if output_type in ["console", "both"]:
            print(log_line.rstrip())  # Консоль без \n

        if output_type in ["file", "both"]:
            self._write_to_file(log_line)


    # Внутренняя запись в файл (режим append)
    def _write_to_file(self, log_line: str):
        log_path = self.settings.get(self.log_path_setting_key(), "app.log")
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(log_line)
        except Exception as e:
            print(f"Error: cant write to file {log_path}")


    #Создает папку для логов если нет
    def _ensure_log_directory(self):
        log_path = self.settings.get(self.log_path_setting_key(), "")
        directory = os.path.dirname(log_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
