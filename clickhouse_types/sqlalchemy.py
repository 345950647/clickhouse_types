import sqlalchemy as sa
from clickhouse_sqlalchemy import types

_dtypes = {
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


def _split_skipping_parenthesis(
        seq: str,
        sep: str = ',',
):
    seqs = []
    n = 0
    i = 0
    for j, s in enumerate(seq):
        if s == '(':
            n += 1
        elif s == ')':
            n -= 1
        elif s == sep and not n:
            seqs.append(seq[i:j])
            i = j + 1
    else:
        seqs.append(seq[i:])
    return seqs


def _split_with_padding(
        seq: str,
        length: int,
        sep: str = ',',
):
    seqs = seq.split(sep)
    length -= len(seqs)
    if length:
        seqs += [None] * length
    return seqs


def datetime64(
        seq: str,
) -> sa.types.TypeEngine:
    unit, timezone = _split_with_padding(seq, 2)
    instance = types.DateTime64(int(unit), timezone)
    return instance


def fixed_string(
        seq: str,
) -> sa.types.TypeEngine:
    return types.String(int(seq))


def decimal(
        seq: str,
) -> sa.types.TypeEngine:
    precision, scale = seq.split(',', 1)
    instance = types.Decimal(int(precision), int(scale))
    return instance


def decimal256(
        seq: str,
) -> sa.types.TypeEngine:
    precision, scale = seq.split(',', 1)
    instance = types.Decimal(int(precision), int(scale))
    return instance


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
    k, v = _split_skipping_parenthesis(seq)
    instance = types.Map(_type_from_string(k), _type_from_string(v))
    return instance


def nullable(
        seq: str,
) -> sa.types.TypeEngine:
    return types.Nullable(_type_from_string(seq))


_dtype_funcs = {
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
    if seq in _dtypes:
        instance = _dtypes[seq]
    else:
        for name, (i, func) in _dtype_funcs.items():
            if seq.startswith(name):
                instance = func(seq[i:-1])
                break
        else:
            raise ValueError(seq)
    return instance


def type_from_string(
        seq: str,
) -> sa.types.TypeEngine:
    return _type_from_string(seq.replace(' ', ''))


__all__ = [
    'type_from_string',
]
