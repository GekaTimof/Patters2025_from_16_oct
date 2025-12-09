import abc
from Src.Core.common import common
from Src.repository import reposity
from Src.Dtos.service_dto import service_dto
from Src.Services.logger import logger


class abstract_scrvice(abc.ABC):
    # Абстраутный метод для обработки событий
    # Принимает на вход тип события (название метода) и dto (параметры)
    @abc.abstractmethod
    def handle(self, repository: reposity, event, dto: service_dto, service_logger: logger):
        # Прорверяем, есть ли событие event (если есть - вызываем)
        methods = common.get_method_names(self)
        if event in methods and event != "handle":
            method = getattr(self, event)
            return method(repository, dto, service_logger)