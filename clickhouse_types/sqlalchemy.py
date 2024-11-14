import sqlalchemy as sa
from clickhouse_sqlalchemy import types

from clickhouse_types._utils import _split_with_padding, _split_skipping_parenthesis

_types = {
    'Bool': types.Boolean,
    'UInt8': types.UInt8,
    'Int8': types.Int8,
    'Enum8': types.Enum8,
    'UInt16': types.UInt16,
    'Int16': types.Int16,
    'Enum16': types.Enum16,
    'UInt32': types.UInt32,
    'Int32': types.Int32,
    'UInt64': types.UInt64,
    'Int64': types.Int64,
    'Float32': types.Float32,
    'Float64': types.Float64,
    'Date32': types.Date32,
    'DateTime': types.DateTime,
    'String': types.String,
    'IPv4': types.IPv4,
    'IPv6': types.IPv6,
    'Int128': types.Int128,
    'UInt128': types.UInt128,
    'Int256': types.Int256,
    'UInt256': types.UInt256,
}


def datetime64(
        seq: str,
) -> sa.types.TypeEngine:
    unit, timezone = _split_with_padding(seq, 2)
    obj = types.DateTime64(int(unit), timezone)
    return obj


def fixed_string(
        seq: str,
) -> sa.types.TypeEngine:
    return types.String(int(seq))


def decimal(
        seq: str,
) -> sa.types.TypeEngine:
    precision, scale = seq.split(',', 1)
    obj = types.Decimal(int(precision), int(scale))
    return obj


def decimal256(
        seq: str,
) -> sa.types.TypeEngine:
    precision, scale = seq.split(',', 1)
    obj = types.Decimal(int(precision), int(scale))
    return obj


def array(
        seq: str,
) -> sa.types.TypeEngine:
    return types.Array(_type_from_string(seq))


def tuple_(
        seq: str,
) -> sa.types.TypeEngine:
    return types.Tuple([_type_from_string(s) for s in _split_skipping_parenthesis(seq)])


def map_(
        seq: str,
) -> sa.types.TypeEngine:
    key, value = _split_skipping_parenthesis(seq)
    obj = types.Map(_type_from_string(key), _type_from_string(value))
    return obj


def nullable(
        seq: str,
) -> sa.types.TypeEngine:
    return types.Nullable(_type_from_string(seq))


_type_funcs = {
    'DateTime64(': (11, datetime64),
    'Decimal(': (8, decimal),
    'Decimal256(': (11, decimal256),
    'FixedString(': (12, fixed_string),
    'Array(': (6, array),
    'Tuple(': (6, tuple_),
    'Map(': (4, map_),
    'Nullable(': (9, nullable),
}


def _type_from_string(
        seq: str,
) -> sa.types.TypeEngine:
    if seq in _types:
        obj = _types[seq]
    else:
        for name, (i, func) in _type_funcs.items():
            if seq.startswith(name):
                obj = func(seq[i:-1])
                break
        else:
            raise ValueError(seq)
    return obj


def type_from_string(
        seq: str,
) -> sa.types.TypeEngine:
    return _type_from_string(seq.replace(' ', ''))


__all__ = [
    'type_from_string',
]
