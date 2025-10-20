from Src.Core.abstract_response import abstract_response
from Src.Core.common import common


class response_csv(abstract_response):

    # Сформировать CSV
    def create(self, format:str, data: list):
        text = super().create(format, data)

        # Шапка
        if data is None:
            return text
        item = data [ 0 ]

        fields = common.get_fields(item)
        text += "\t".join(fields) + "\n"

        # Формируем строки данных csv
        for row in data:
            values = [str(getattr(row, f, "")) for f in fields]
            text += "\t".join(values) + "\n"

        return text


