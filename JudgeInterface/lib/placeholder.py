from typing import Dict, List
import re

class Placeholder:
    @staticmethod
    def for_create_query(fields_len: int) -> str:
        placeholder = ''
        for i in range(fields_len):
            placeholder += '?, '
        placeholder = re.sub(', $', '', placeholder)
        return placeholder

    @staticmethod
    def for_select_query(requested_fields: List[str]) -> str:
        placeholder = ''
        for field in requested_fields:
            placeholder += f'{field}, '
        placeholder = re.sub(', $', '', placeholder)
        return placeholder

    @staticmethod
    def for_where_query(requested_fields: List[str]) -> str:
        placeholder = ''
        for key in requested_fields:
            placeholder += key + ' = ? AND '
        placeholder = re.sub(' AND $', '', placeholder)
        return placeholder

    @staticmethod
    def for_update_query(update_fields: List[str]) -> str:
        placeholder = ''
        for key in update_fields:
            placeholder += key + ' = ?, '
        placeholder = re.sub(', $', '', placeholder)
        return placeholder
