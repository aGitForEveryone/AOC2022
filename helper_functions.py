from typing import Union, Sequence, Callable

import numpy as np


def digits_to_int(
    data: Union[Sequence[str], str],
    individual_character: bool = True,
    return_type: Callable = list,
) -> Union[Sequence[Sequence[int]], Sequence[int]]:
    """Converts character digits to ints. Can take both a Sequence of strings
    and a single string as input. It is possible to specify if string should be
    converted as a whole, or if digits should be treated individually.
    For example,
        1. the string "123" is converted to [1, 2, 3] or 123 (individual_character is True or False respectively)
        2. ["123", "456"] is converted to [[1, 2, 3], [4, 5, 6]] or [123, 456]

    Args:
        data:                   The string data to be converted
        individual_character:   If True, each digit in the string is converted
                                as a separate int. Otherwise, the string is
                                taken as a whole.
        return_type:            Specifies what data type the output should be.
                                By default, the function will return lists.
                                This should be a value Sequence type.

    Returns:
        The output will be the same level of nesting as the input, unless
        the digits should be treated individually. In that case, the output is
        nested 1 level more. The data type of the sequence can is user-defined.
    """

    def convert_line(line):
        return return_type(map(int, line)) if individual_character else int(line)

    if isinstance(data, str):
        return convert_line(data)

    return return_type(convert_line(line) for line in data)


def pad_numpy_array(
    np_array: np.ndarray,
    padding_symbol: int,
    pad_width: Union[int, tuple[int, ...], tuple[tuple[int, ...], ...]] = (1,),
) -> np.ndarray:
    """Pad a numpy array with a constant value

    Args:
        np_array:           Array to pad
        padding_symbol:     Value to set the padded values
        pad_width:          Number of values padded to the edges of each axis.
                            ((before_1, after_1), … (before_N, after_N)) unique
                            pad widths for each axis. ((before, after),) yields
                            same before and after pad for each axis. (pad,) or
                            int is a shortcut for before = after = pad width for
                            all axes.
    """
    return np.pad(np_array, pad_width, mode="constant", constant_values=padding_symbol)
