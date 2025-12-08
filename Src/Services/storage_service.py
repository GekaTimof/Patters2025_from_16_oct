from Src.Core.abstract_service import abstract_scrvice
from Src.repository import reposity
from Src.Dtos.service_dto import service_dto
from Src.Core.validator import operation_exception
from Src.Core.prototype import prototype
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.storage_dto import storage_dto
from Src.Models.storage_model import storage_model
from Src.Services.logger import logger

class storage_service(abstract_scrvice):

    # Метод для обработки события
    # Принимает на вход тип события (название метода) и dto (параметры)
    def handle(self, repository: reposity, event, dto: service_dto, service_logger: logger):
        return super().handle(repository, event, dto, service_logger)

    # Метод для получения склада (по id)
    def get(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_id:
            return None
        if dto.target_model != "storage":
            return None

        # LOG Предупреждение о попытке получения
        service_logger.log("Trying to get storage", "WARNING")

        try:
            id = dto.target_id
            storages = repository.data[repository.storages_key()]
            for storage in storages:
                if storage.id == id:
                    # LOG Информация что объект удачно получен
                    service_logger.log("Finish of storage getting", "INFO")
                    return storage
            # выйти в except
            raise operation_exception("")
        except:
            # LOG Ошибка получения
            service_logger.log("Error of storage getting", "ERROR")
            raise operation_exception("Cant get storage")


    # Метод для добавления объекта
    def put(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_storage_dto:
            return None

        # LOG Предупреждение о попытке добавления
        service_logger.log("Trying to put storage", "WARNING")

        try:
            target_dto: storage_dto = dto.target_storage_dto
            name: str = target_dto.name
            address = target_dto.address

            # Проверяем, есть ли склад с такими параметрами
            data = [i.to_dto() for i in repository.data[repository.storages_key()]]
            filter_prototype = prototype(data)

            # Фильтр по name
            filter_obj = filter_dto(
                field_name="name",
                value=name,
                filter_type="EQUAL"
            )
            filtered_data = prototype.filter(filter_prototype, filter_obj)

            # Фильтр по address
            filter_obj = filter_dto(
                field_name="address",
                value=address,
                filter_type="EQUAL"
            )
            filtered_data = prototype.filter(filtered_data, filter_obj)

            if len(filtered_data.data) == 0:
                model = storage_model().from_dto(target_dto, repository.cache)
                model_id = model.id
                # LOG Информация что объект удачно добавлен
                service_logger.log("Finish of storage putting", "INFO")
                repository.add_item(repository.storages_key(), model)
                response = {
                    "message": "Storage successfully putted",
                    "id": model_id
                }
                return response
            else:
                raise operation_exception("")
        except:
            # LOG Ошибка добавления
            service_logger.log("Error of storage putting", "ERROR")
            raise operation_exception("Cant put storage (it already exist)")


    # Метод для обновления объекта
    def patch(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_storage_dto:
            return None
        if not dto.target_id:
            return None

        # LOG Предупреждение о попытке обновления
        service_logger.log("Trying to patch storage", "WARNING")

        try:
            target_dto = dto.target_storage_dto
            target_id = dto.target_id

            # Ищем подходящий склад
            storages = repository.data[repository.storages_key()]
            for i, storage in enumerate(storages):
                if storage.id == target_id:
                    # Проверяем, нет ли зависимые объекты
                    data = []
                    data += repository.data[repository.transactions_key()]
                    data += repository.data[repository.receipt_items_key()]
                    filter_prototype = prototype(data)
                    filter_obj = filter_dto(
                        field_name="storage_id",
                        value=target_id,
                        filter_type="EQUAL"
                    )
                    filtered_data = prototype.filter(filter_prototype, filter_obj)

                    if len(filtered_data.data) == 0:
                        model = storage_model().from_dto(target_dto, repository.cache)
                        model.id = target_id
                        storages[i] = model
                        # LOG Информация что объект удачно обновлен
                        service_logger.log("Finish of storage patching", "INFO")
                        response = {
                            "message": "Storage successfully patched",
                            "id": target_id
                        }
                        return response
                    else:
                        raise operation_exception("")
            raise operation_exception("")
        except:
            # LOG Ошибка обновления
            service_logger.log("Error of storage patching", "ERROR")
            raise operation_exception("Cant patch storage (it have dependent objects)")


    # Метод для удаления объекта
    def delete(self, repository: reposity, dto: service_dto, service_logger: logger):
        # Если аргументы в dto не подходят
        if not dto.target_id:
            return None
        if dto.target_model != "storage":
            return None

        # LOG Предупреждение о попытке удаления
        service_logger.log("Trying to delete storage", "WARNING")

        try:
            id = dto.target_id

            # Проверяем, нет ли зависимые объекты
            data = []
            data += repository.data[repository.transactions_key()]
            data += repository.data[repository.receipt_items_key()]
            filter_prototype = prototype(data)
            filter_obj = filter_dto(
                field_name="storage_id",
                value=id,
                filter_type="EQUAL"
            )
            filtered_data = prototype.filter(filter_prototype, filter_obj)

            if len(filtered_data.data) == 0:
                storages = repository.data[repository.storages_key()]
                for i, storage in enumerate(storages):
                    if storage.id == id:
                        # LOG Информация что объект удачно удалён
                        service_logger.log("Finish of storage deleting", "INFO")
                        storages.pop(i)
                        response = {
                            "message": "Storage successfully deleting"
                        }
                        return response
            raise operation_exception("")
        except:
            # LOG Ошибка удаления
            service_logger.log("Error of storage deleting", "ERROR")
            raise operation_exception("Cant delete storage (it have dependent objects)")
