from typing import List

import pandas
from pandas import DataFrame


def fillnone(df: DataFrame = None, column_names: List[str] = None) -> None:
    """
    Convert pandas.NA into None
    """

    def _to_none(x):
        return None if isinstance(x, type(pandas.NA)) else x

    for col_name in column_names:
        # Turn nan/NaN/NAType into None
        # pandas v1.3.4: Works
        # pandas v1.4.0: Not Works
        # chunk[col_name] = chunk[col_name].replace({pandas.NA, None})

        # pandas v1.3.4: Untested
        # pandas v1.4.0: Works
        df[col_name] = df[col_name].apply(_to_none)
