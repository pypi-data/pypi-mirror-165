from ._color import getHexColorList
from ._encoding import (
    check_file_by_line,
    check_non_ascii_char,
    check_non_ascii_index,
    ensure_no_zh_punctuation,
    is_ascii,
    is_ascii_only_file,
    replace_punc_for_file,
)
from ._file import MassCopier, alternative_file_path
from ._logging import get_logger, init_logger
from ._string import title_cap, title_capitalize
from ._time import (
    timeit,
    timeitprint,
    timestamp_microseconds,
    timestamp_milliseconds,
    timestamp_seconds,
)
from ._utils import (
    convert_date_to_datetime,
    convert_datetime_to_date,
    json_serial,
    print_bold,
    print_cyan,
    print_green,
    print_red,
    print_with_color,
    print_yellow,
    printc,
)
