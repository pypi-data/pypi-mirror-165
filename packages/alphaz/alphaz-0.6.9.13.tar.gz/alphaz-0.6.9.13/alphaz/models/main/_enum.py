from enum import Enum


class EnumStr(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

