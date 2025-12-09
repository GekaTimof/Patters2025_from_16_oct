from Src.Core.abstract_service import abstract_scrvice
from Src.repository import reposity
from Src.Dtos.service_dto import service_dto
from Src.Core.validator import operation_exception
from Src.Core.prototype import prototype
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.range_dto import range_dto
from Src.Models.range_model import range_model
from Src.Services.logger import logger

class range_service(abstract_scrvice):

    # Метод для обработки события
    # Принимает на вход тип события (название метода) и dto (параметры)
    def handle(self, repository: reposity, event, dto: service_dto, service_logger: logger):
        return super().handle(repository, event, dto, service_logger)

    # Метод для получения диапазона (по id)
    def get(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_id:
            return None
        if dto.target_model != "range":
            return None

        # LOG Предупреждение о попытке получения
        service_logger.log("Trying to get range", "WARNING")

        try:
            id = dto.target_id
            ranges = repository.data[repository.ranges_key()]
            for range_ in ranges:
                if range_.id == id:
                    # LOG Информация что объект удачно получен
                    service_logger.log("Finish of range getting", "INFO")
                    return range_
            # выйти в except
            raise operation_exception("")
        except:
            # LOG Ошибка получения
            service_logger.log("Error of range getting", "ERROR")
            raise operation_exception("Cant get range")

    # Метод для добавления объекта
    def put(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_range_dto:
            return None

        # LOG Предупреждение о попытке добавления
        service_logger.log("Trying to put range", "WARNING")

        try:
            target_dto: range_dto = dto.target_range_dto
            name: str = target_dto.name

            # Проверяем, есть ли диапазон с такими параметрами
            data = [i.to_dto() for i in repository.data[repository.ranges_key()]]
            filter_prototype = prototype(data)

            # Фильтр по name
            filter_obj = filter_dto(
                field_name="name",
                value=name,
                filter_type="EQUAL"
            )
            filtered_data = prototype.filter(filter_prototype, filter_obj)

            if len(filtered_data.data) == 0:
                model = range_model().from_dto(target_dto, repository.cache)
                model_id = model.id
                # LOG Информация что объект удачно добавлен
                service_logger.log("Finish of range putting", "INFO")
                repository.add_item(repository.ranges_key(), model)
                response = {
                    "message": "Range successfully putted",
                    "id": model_id
                }
                return response
            else:
                raise operation_exception("")
        except:
            # LOG Ошибка добавления
            service_logger.log("Error of range putting", "ERROR")
            raise operation_exception("Cant put range (it already exist)")

    # Метод для обновления объекта
    def patch(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_range_dto:
            return None
        if not dto.target_id:
            return None

        # LOG Предупреждение о попытке обновления
        service_logger.log("Trying to patch range", "WARNING")

        try:
            target_dto = dto.target_range_dto
            target_id = dto.target_id

            # Ищем подходящий диапазон
            ranges = repository.data[repository.ranges_key()]
            for i, range_ in enumerate(ranges):
                if range_.id == target_id:
                    # Проверяем, нет ли зависимые объекты
                    data = []
                    data += repository.data[repository.nomenclatures_key()]
                    filter_prototype = prototype(data)
                    filter_obj = filter_dto(
                        field_name="range_id",
                        value=target_id,
                        filter_type="EQUAL"
                    )
                    filtered_data = prototype.filter(filter_prototype, filter_obj)

                    if len(filtered_data.data) == 0:
                        model = range_model().from_dto(target_dto, repository.cache)
                        model.id = target_id
                        ranges[i] = model
                        # LOG Информация что объект удачно обновлен
                        service_logger.log("Finish of range patching", "INFO")
                        response = {
                            "message": "Range successfully patched",
                            "id": target_id
                        }
                        return response
                    else:
                        raise operation_exception("")
            raise operation_exception("")
        except:
            # LOG Ошибка обновления
            service_logger.log("Error of range patching", "ERROR")
            raise operation_exception("Cant patch range (it have dependent objects)")

    # Метод для удаления объекта
    def delete(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_id:
            return None
        if dto.target_model != "range":
            return None

        # LOG Предупреждение о попытке удаления
        service_logger.log("Trying to delete range", "WARNING")

        try:
            id = dto.target_id

            # Проверяем, нет ли зависимые объекты
            data = []
            data += repository.data[repository.nomenclatures_key()]
            filter_prototype = prototype(data)
            filter_obj = filter_dto(
                field_name="range_id",
                value=id,
                filter_type="EQUAL"
            )
            filtered_data = prototype.filter(filter_prototype, filter_obj)

            if len(filtered_data.data) == 0:
                ranges = repository.data[repository.ranges_key()]
                for i, range_ in enumerate(ranges):
                    if range_.id == id:
                        # LOG Информация что объект удачно удалён
                        service_logger.log("Finish of range deleting", "INFO")
                        ranges.pop(i)
                        response = {
                            "message": "Range successfully deleting"
                        }
                        return response
            raise operation_exception("")
        except:
            # LOG Ошибка удаления
            service_logger.log("Error of range deleting", "ERROR")
            raise operation_exception("Cant delete range (it have dependent objects)")
