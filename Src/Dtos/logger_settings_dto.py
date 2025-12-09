from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import validator
from Src.Core.validator import argument_exception
from Src.repository import reposity

class logger_settings_dto(abstract_dto):

    # Тип лога: console/file/both
    __log_types: list = ["console", "file", "both"]
    __log_type: str = "console"

    # Путь к файлу логов
    __log_path: str = "logs/service.log"

    # Показ INFO логов
    __show_info_logs: bool = True

    # Показ WARNING логов
    __show_warning_logs: bool = True

    # Показ ERROR логов
    __show_errors_logs: bool = True

    # Тип лога
    @property
    def log_type(self) -> str:
        return self.__log_type

    @log_type.setter
    def log_type(self, value: str):
        validator.validate(value, str)
        if value not in self.__log_types:
            raise argument_exception(f"log type not one of {self.__log_types}")
        self.__log_type = value.strip()


    # Путь к файлу логов
    @property
    def log_path(self) -> str:
        return self.__log_path

    @log_path.setter
    def log_path(self, value: str):
        validator.validate(value, str)
        self.__log_path = value.strip()


    # Показ INFO логов
    @property
    def show_info_logs(self) -> bool:
        return self.__show_info_logs

    @show_info_logs.setter
    def show_info_logs(self, value: bool):
        validator.validate(value, bool)
        self.__show_info_logs = value


    # Показ WARNING логов
    @property
    def show_warning_logs(self) -> bool:
        return self.__show_warning_logs

    @show_warning_logs.setter
    def show_warning_logs(self, value: bool):
        validator.validate(value, bool)
        self.__show_warning_logs = value


    # Показ ERROR логов
    @property
    def show_errors_logs(self) -> bool:
        return self.__show_errors_logs

    @show_errors_logs.setter
    def show_errors_logs(self, value: bool):
        validator.validate(value, bool)
        self.__show_errors_logs = value


    # Инициализация из dict (по ключам репозитория), если ключ пуст, ставим дефолтное значение
    def init_from_repository(self, repository: reposity) -> None:
        # Тип лога
        if reposity.log_type_setting_key() in repository.data and repository.data[reposity.log_type_setting_key()]:
            self.log_type = repository.data[reposity.log_type_setting_key()]
        else:
            self.log_type = "console"

        # Путь к файлу логов
        if reposity.log_path_setting_key() in repository.data and repository.data[reposity.log_path_setting_key()]:
            self.log_path = repository.data[reposity.log_path_setting_key()]
        else:
            self.log_path = "logs/service.log"

        # Показ INFO логов
        if reposity.show_info_logs_setting_key() in repository.data:
            self.show_info_logs = bool(repository.data[reposity.show_info_logs_setting_key()])
        else:
            self.show_info_logs = True

        # Показ WARNING логов
        if reposity.show_warning_logs_setting_key() in repository.data:
            self.show_warning_logs = bool(repository.data[reposity.show_warning_logs_setting_key()])
        else:
            self.show_warning_logs = True

        # Показ ERROR логов
        if reposity.show_errors_logs_setting_key() in repository.data:
            self.show_errors_logs = bool(repository.data[reposity.show_errors_logs_setting_key()])
        else:
            self.show_errors_logs = True
