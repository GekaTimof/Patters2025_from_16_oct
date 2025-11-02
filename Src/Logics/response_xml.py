from Src.Core.abstract_response import abstract_response
from Src.Core.common import common


class response_xml(abstract_response):
    # Сформировать XML
    def create(self, format: str, data: list):
        text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<items>\n"

        for row in data:
            text += "  <item>\n"
            fields = common.get_fields(row)
            for f in fields:
                value = str(getattr(row, f, ""))
                text += f"    <{f}>{value}</{f}>\n"
            text += "  </item>\n"

        text += "</items>\n"
        return text

