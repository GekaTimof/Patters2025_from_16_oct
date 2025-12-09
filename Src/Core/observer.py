from Src.Core.abstract_service import abstract_scrvice
from Src.Core.common import common
from Src.repository import reposity
from Src.Services.logger import logger
import Src.Services.nomenclature_service
import Src.Services.group_service
import Src.Services.storage_service
import Src.Services.range_service

class observer:
    def __init__(self):
        # Словарь {имя_класса: класс-наследник abstract_scrvice}
        self.services = common.get_all_subclasses_dict(abstract_scrvice)
        # Кэш экземпляров сервисов
        self.instances = {}

    def event(self, repository: reposity, event: str, dto, service_logger: logger) -> list:
        service_logger.log(f"Observer get and start handel event - {event}", "WARNING")
        responses = []
        for service_name, service_class in self.services.items():
            try:
                # Создаём экземпляр сервиса (если нет в кэше)
                if service_name not in self.instances:
                    self.instances[service_name] = service_class()

                service: abstract_scrvice = self.instances[service_name]

                response = service.handle(repository, event, dto, service_logger)
                if response is not None:
                    responses.append(response)
            except Exception as e:
                # LOG Ошибка при обработке события
                service_logger.log(f"Error in service execution - {service_name}", "ERROR")
                continue

        # Ни один сервис не обработал событие
        if len(responses) == 0:
            # LOG Предупреждение, ни один event не смог обработать событие
            service_logger.log(f"No one service can handle event - {event}", "WARNING")
            empty_response = [{
                "message": f"No one service can handle event - {event}"
            }]
            return empty_response

        else:
            service_logger.log(f"Observer finish handel event - {event}", "INFO")
            return responses