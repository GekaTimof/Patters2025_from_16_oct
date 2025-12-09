from Src.Core.abstract_service import abstract_scrvice
from Src.repository import reposity
from Src.Dtos.service_dto import service_dto
from Src.Core.validator import operation_exception
from Src.Core.prototype import prototype
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.group_dto import group_dto
from Src.Models.group_model import group_model
from Src.Services.logger import logger

class group_service(abstract_scrvice):

    # Метод для обработки события
    # Принимает на вход тип события (название метода) и dto (параметры)
    def handle(self, repository: reposity, event, dto: service_dto, service_logger: logger):
        return super().handle(repository, event, dto, service_logger)

    # Метод для получения группы (по id)
    def get(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_id:
            return None
        if dto.target_model != "group":
            return None

        # LOG Предупреждение о попытке получения
        service_logger.log("Trying to get group", "WARNING")

        try:
            id = dto.target_id
            groups = repository.data[repository.groups_key()]
            for group in groups:
                if group.id == id:
                    # LOG Информация что объект удачно получен
                    service_logger.log("Finish of group getting", "INFO")
                    return group
            # выйти в except
            raise operation_exception("")
        except:
            # LOG Ошибка получения
            service_logger.log("Error of group getting", "ERROR")
            raise operation_exception("Cant get group")

    # Метод для добавления объекта
    def put(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_group_dto:
            return None

        # LOG Предупреждение о попытке добавления
        service_logger.log("Trying to put group", "WARNING")

        try:
            target_dto: group_dto = dto.target_group_dto
            name: str = target_dto.name

            # Проверяем, есть ли группа с такими параметрами
            data = [i.to_dto() for i in repository.data[repository.groups_key()]]
            filter_prototype = prototype(data)

            # Фильтр по name
            filter_obj = filter_dto(
                field_name="name",
                value=name,
                filter_type="EQUAL"
            )
            filtered_data = prototype.filter(filter_prototype, filter_obj)

            if len(filtered_data.data) == 0:
                model = group_model().from_dto(target_dto, repository.cache)
                model_id = model.id
                # LOG Информация что объект удачно добавлен
                service_logger.log("Finish of group putting", "INFO")
                repository.add_item(repository.groups_key(), model)
                response = {
                    "message": "Group successfully putted",
                    "id": model_id
                }
                return response
            else:
                raise operation_exception("")
        except:
            # LOG Ошибка добавления
            service_logger.log("Error of group putting", "ERROR")
            raise operation_exception("Cant put group (it already exist)")

    # Метод для обновления объекта
    def patch(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_group_dto:
            return None
        if not dto.target_id:
            return None

        # LOG Предупреждение о попытке обновления
        service_logger.log("Trying to patch group", "WARNING")

        try:
            target_dto = dto.target_group_dto
            target_id = dto.target_id

            # Ищем подходящую группу
            groups = repository.data[repository.groups_key()]
            for i, group in enumerate(groups):
                if group.id == target_id:
                    # Проверяем, нет ли зависимые объекты
                    data = []
                    data += repository.data[repository.nomenclatures_key()]
                    filter_prototype = prototype(data)
                    filter_obj = filter_dto(
                        field_name="group_id",
                        value=target_id,
                        filter_type="EQUAL"
                    )
                    filtered_data = prototype.filter(filter_prototype, filter_obj)

                    if len(filtered_data.data) == 0:
                        model = group_model().from_dto(target_dto, repository.cache)
                        model.id = target_id
                        groups[i] = model
                        # LOG Информация что объект удачно обновлен
                        service_logger.log("Finish of group patching", "INFO")
                        response = {
                            "message": "Group successfully patched",
                            "id": target_id
                        }
                        return response
                    else:
                        raise operation_exception("")
            raise operation_exception("")
        except:
            # LOG Ошибка обновления
            service_logger.log("Error of group patching", "ERROR")
            raise operation_exception("Cant patch group (it have dependent objects)")

    # Метод для удаления объекта
    def delete(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_id:
            return None
        if dto.target_model != "group":
            return None

        # LOG Предупреждение о попытке удаления
        service_logger.log("Trying to delete group", "WARNING")

        try:
            id = dto.target_id

            # Проверяем, нет ли зависимые объекты
            data = []
            data += repository.data[repository.nomenclatures_key()]
            filter_prototype = prototype(data)
            filter_obj = filter_dto(
                field_name="group_id",
                value=id,
                filter_type="EQUAL"
            )
            filtered_data = prototype.filter(filter_prototype, filter_obj)

            if len(filtered_data.data) == 0:
                groups = repository.data[repository.groups_key()]
                for i, group in enumerate(groups):
                    if group.id == id:
                        # LOG Информация что объект удачно удалён
                        service_logger.log("Finish of group deleting", "INFO")
                        groups.pop(i)
                        response = {
                            "message": "Group successfully deleting"
                        }
                        return response
            raise operation_exception("")
        except:
            # LOG Ошибка удаления
            service_logger.log("Error of group deleting", "ERROR")
            raise operation_exception("Cant delete group (it have dependent objects)")
