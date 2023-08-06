import pandas as pd

from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.utils import register_ops


class Index(DataSpecWrapper[pd.Index]):
    ...


class RangeIndex(DataSpecWrapper[pd.RangeIndex]):
    ...


class Int64Index(DataSpecWrapper[pd.Int64Index]):
    ...


class UInt64Index(DataSpecWrapper[pd.UInt64Index]):
    ...


class Float64Index(DataSpecWrapper[pd.Float64Index]):
    ...


class DataFrameGroupBy(DataSpecWrapper[pd.core.groupby.DataFrameGroupBy]):
    ...


class SeriesGroupBy(DataSpecWrapper[pd.core.groupby.SeriesGroupBy]):
    ...


class RollingGroupby(DataSpecWrapper[pd.core.window.rolling.RollingGroupby]):
    ...


register_ops()
