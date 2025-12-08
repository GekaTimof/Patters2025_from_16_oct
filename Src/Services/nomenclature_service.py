from Src.Core.abstract_service import abstract_scrvice
from Src.repository import reposity
from Src.Dtos.service_dto import service_dto
from Src.Core.validator import operation_exception
from Src.Core.prototype import prototype
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Models.nomenclature_model import nomenclature_model
from Src.Services.logger import logger


class nomenclature_service(abstract_scrvice):
    # Метод для обработки события
    # Принимает на вход тип события (название метода) и dto (параметры)
    def handle(self, repository: reposity, event, dto: service_dto, service_logger: logger):
        return super().handle(repository, event, dto, service_logger)

    # Метод для получения номенклатуры (по id)
    def get(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_id:
            return None
        if dto.target_model != "nomenclature":
            return None

        # LOG Предупреждение о попытке получения
        service_logger.log("Trying to get nomenclature", "WARNING")
        try:
            id = dto.target_id
            nomenclatures = repository.data[repository.nomenclatures_key()]
            for nomenclature in nomenclatures:
                if nomenclature.id == id:
                    # LOG Информация что объект удачно получен
                    service_logger.log("Finish of nomenclature getting", "INFO")
                    return nomenclature

            # выйти в except
            raise operation_exception("")
        except:
            # LOG Ошибка получения
            service_logger.log("Error of nomenclature getting", "ERROR")
            raise operation_exception("Cant get nomenclature")


    # Метод для добавления объекта
    def put(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_nomenclature_dto:
            return None

        # LOG Предупреждение о попытке добавления
        service_logger.log("Trying to put nomenclature", "WARNING")
        try:
            target_dto: nomenclature_dto = dto.target_nomenclature_dto
            group_id = target_dto.group_id
            range_id = target_dto.range_id
            name: str = target_dto.name

            # Проверяем, есть ли номенклатура с такими параметрами
            data = [i.to_dto() for i in repository.data[repository.nomenclatures_key()]]
            filter_prototype = prototype(data)
            # Фильтр по group_id
            filter_obj = filter_dto(
                field_name="group_id",
                value=group_id,
                filter_type="EQUAL"
            )
            filtered_data = prototype.filter(filter_prototype, filter_obj)

            # Фильтр по range_id
            filter_obj = filter_dto(
                field_name="range_id",
                value=range_id,
                filter_type="EQUAL"
            )
            filtered_data = prototype.filter(filtered_data, filter_obj)

            # Фильтр по name
            filter_obj = filter_dto(
                field_name="name",
                value=name,
                filter_type="EQUAL"
            )
            filtered_data = prototype.filter(filtered_data, filter_obj)

            if len(filtered_data.data) == 0:
                model = nomenclature_model().from_dto(target_dto, repository.cache)
                model_id = model.id
                # LOG Информация что объект удачно добавлен
                service_logger.log("Finish of nomenclature putting", "INFO")
                repository.add_item(repository.nomenclatures_key(), model)

                response = {
                    "message": "Nomenclature successfully putted",
                    "id": model_id
                }

                return response
            else:
                raise operation_exception("")
        except:
            # LOG Ошибка добавления
            service_logger.log("Error of nomenclature putting", "ERROR")
            raise operation_exception("Cant put nomenclature (it already exist)")


    # Метод для обновления объекта
    def patch(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_nomenclature_dto:
            return None
        if not dto.target_id:
            return None

        # LOG Предупреждение о попытке обновления
        service_logger.log("Trying to patch nomenclature", "WARNING")
        try:
            target_dto = dto.target_nomenclature_dto
            target_id = dto.target_id

            # Ищем подходящую номенклатуру
            nomenclatures = repository.data[repository.nomenclatures_key()]
            for i, nomenclature in enumerate(nomenclatures):
                if nomenclature.id == target_id:
                    # Проверяем, нет ли зависимые объекты
                    data = []
                    data += repository.data[repository.transactions_key()]
                    data += repository.data[repository.receipt_items_key()]
                    filter_prototype = prototype(data)
                    filter_obj = filter_dto(
                        field_name="nomenclature_id",
                        value=target_id,
                        filter_type="EQUAL"
                    )
                    filtered_data = prototype.filter(filter_prototype, filter_obj)

                    if len(filtered_data.data) == 0:
                        model = nomenclature_model().from_dto(target_dto, repository.cache)
                        model.id = target_id
                        nomenclatures[i] = model
                        # LOG Информация что объект удачно обновлен
                        service_logger.log("Finish of nomenclature patching", "INFO")

                        response = {
                            "message": "Nomenclature successfully patched",
                            "id": target_id
                        }

                        return response
                    else:
                        raise operation_exception("")

            raise operation_exception("")
        except:
            # LOG Ошибка обновления
            service_logger.log("Error of nomenclature patching", "ERROR")
            raise operation_exception("Cant patch nomenclature (it have dependent objects)")


    # Метод для удаления объекта
    def delete(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_id:
            return None
        if dto.target_model != "nomenclature":
            return None

        # LOG Предупреждение о попытке удаления
        service_logger.log("Trying to delete nomenclature", "WARNING")
        try:
            id = dto.target_id

            # Проверяем, нет ли зависимые объекты
            data = []
            data += repository.data[repository.transactions_key()]
            data += repository.data[repository.receipt_items_key()]
            filter_prototype = prototype(data)
            filter_obj = filter_dto(
                field_name="nomenclature_id",
                value=id,
                filter_type="EQUAL"
            )
            filtered_data = prototype.filter(filter_prototype, filter_obj)

            if len(filtered_data.data) == 0:
                nomenclatures = repository.data[repository.nomenclatures_key()]
                for i, nomenclature in enumerate(nomenclatures):
                    if nomenclature.id == id:  # ✅ Исправлено: dto.id → id
                        # LOG Информация что объект удачно удалён
                        service_logger.log("Finish of nomenclature deleting", "INFO")
                        nomenclatures.pop(i)

                        response = {
                            "message": "Nomenclature successfully deleting",
                        }

                        return response
            raise operation_exception("")
        except:
            # LOG Ошибка удаления
            service_logger.log("Error of nomenclature deleting", "ERROR")
            raise operation_exception("Cant delete nomenclature (it have dependent objects)")
