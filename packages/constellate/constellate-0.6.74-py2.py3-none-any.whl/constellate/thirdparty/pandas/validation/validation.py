from functools import lru_cache
from typing import Union, Any, Dict, Callable

import pandas
import pandera
from decorator import decorator
from typing_extensions import TypeAlias

PanderaSchema: TypeAlias = Union[pandera.DataFrameSchema, pandera.SeriesSchema]
PandasType: TypeAlias = Union[pandas.DataFrame, pandas.Series]

LibrarySchema: TypeAlias = Union[PanderaSchema]


class DataValidationError(Exception):
    pass


@lru_cache(maxsize=25, typed=True)
def _from_pydantic_schema_to_pandera_schema(schema: LibrarySchema):
    if isinstance(schema, (pandera.DataFrameSchema, pandera.SeriesSchema)):
        return schema
    return schema.to_schema()


def _pandera_checks(
    data: PandasType = None,
    schema: LibrarySchema = None,
    schema_validation_options: Dict[str, Any] = None,
):
    row_total = len(data)
    sample_row_total = round(row_total * 0.25)
    head_row_total = round(row_total * 0.15)
    schema_validation_options = schema_validation_options or {
        # Head / Tail: 15 % of the rows
        "head": max(0, min(head_row_total if row_total > 100 else row_total, row_total)),
        "tail": max(0, min(head_row_total if row_total > 100 else row_total, row_total)),
        # Sample 25% of the rows
        "sample": max(0, min(sample_row_total if row_total > 100 else row_total, row_total)),
        "lazy": True,
        "inplace": True,
    }
    try:

        pandera_schema = schema
        if not isinstance(schema, (pandera.DataFrameSchema, pandera.SeriesSchema)):
            pandera_schema = _from_pydantic_schema_to_pandera_schema(schema=schema)

        # For list of checks carried out:
        # https://pandera.readthedocs.io/en/stable/lazy_validation.html
        return pandera_schema.validate(data, **schema_validation_options)
    except pandera.errors.SchemaErrors as e:
        msg = (
            f"Schema errors and failure cases:\n{e.failure_cases}"
            f"\nDataFrame object that failed validation:\n{e.data}"
        )
        raise DataValidationError(msg) from e


@decorator
def pandas_data_checks(
    fn: Callable,
    schema: LibrarySchema = None,
    schema_validation_options: Dict[str, Any] = None,
    *fn_args,
    **fn_kwargs,
):
    """
    @param: schema: Should be declared as is
        # using Pandera

        from pandera.typing import Series

        class MySchema(pa.SchemaModel):
            column1: Series[int] = pa.Field(le=10)
            column2: Series[float] = pa.Field(lt=-1.2)
            column3: Series[str] = pa.Field(str_startswith="value_")

            @pa.check("column3")
            def column_3_check(cls, series: Series[str]) -> Series[bool]:
                return series.str.split("_", expand=True).shape[1] == 2

    Usage:
        @pandas_data_checks(schema=MySchema)
        def generate_some_dataframe():
            return pandas.DataFrame(...)
    """

    data = fn(*fn_args, **fn_kwargs)
    if isinstance(
        schema, (pandera.DataFrameSchema, pandera.SeriesSchema, pandera.model._MetaSchema)
    ):
        return _pandera_checks(
            data=data, schema=schema, schema_validation_options=schema_validation_options
        )

    raise NotImplemented()
