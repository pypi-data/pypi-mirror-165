from enum import Enum

from .._content_type import ContentType
from ..._tools import make_enum_arg_parser, ArgsParser, validate_bool_value


class DataGridType(Enum):
    UDF = "udf"
    RDP = "rdp"


data_grid_types_arg_parser = make_enum_arg_parser(DataGridType)
use_field_names_in_headers_arg_parser = ArgsParser(validate_bool_value)

data_grid_type_value_by_content_type = {
    DataGridType.UDF.value: ContentType.DATA_GRID_UDF,
    DataGridType.RDP.value: ContentType.DATA_GRID_RDP,
}

content_type_by_data_grid_type = {
    ContentType.DATA_GRID_UDF: DataGridType.UDF,
    ContentType.DATA_GRID_RDP: DataGridType.RDP,
}


def get_data_grid_type(content_type: ContentType) -> DataGridType:
    data_grid_type = content_type_by_data_grid_type.get(content_type)

    if not data_grid_type:
        raise ValueError(f"There is no DataGridType for content_type:{content_type}")

    return data_grid_type
