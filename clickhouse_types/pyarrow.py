import pyarrow as pa

_dtypes = {
    'Bool': pa.bool_(),
    'UInt8': pa.uint8(),
    'Int8': pa.int8(),
    'Enum8': pa.int8(),
    'UInt16': pa.uint16(),
    'Int16': pa.int16(),
    'Enum16': pa.int16(),
    'UInt32': pa.uint32(),
    'Int32': pa.int32(),
    'UInt64': pa.uint64(),
    'Int64': pa.int64(),
    'Float32': pa.float32(),
    'Float64': pa.float64(),
    'Date32': pa.date32(),
    'DateTime': pa.date64(),
    'String': pa.binary(),
    'IPv4': pa.uint32(),
    'IPv6': pa.binary(16),
    'Int128': pa.binary(16),
    'UInt128': pa.binary(16),
    'Int256': pa.binary(32),
    'UInt256': pa.binary(32),
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


# https://clickhouse.com/docs/en/sql-reference/data-types/datetime64
_units = {
    '0': 's',
    '1': 'ms',
    '2': 'ms',
    '3': 'ms',
    '4': 'us',
    '5': 'us',
    '6': 'us',
    '7': 'ns',
    '8': 'ns',
    '9': 'ns',
}


def timestamp(
        seq: str,
) -> pa.DataType:
    unit, tz = _split_with_padding(seq, 2)
    dtype = pa.timestamp(_units[unit], tz)
    return dtype


def time32(
        seq: str,
) -> pa.DataType:
    return pa.time32(_units[seq])


def time64(
        seq: str,
) -> pa.DataType:
    return pa.time64(_units[seq])


def fixed_size_binary(
        seq: str,
) -> pa.DataType:
    return pa.binary(int(seq))


def decimal(
        seq: str,
) -> pa.DataType:
    precision, scale = seq.split(',', 1)
    dtype = pa.decimal128(int(precision), int(scale))
    return dtype


def decimal256(
        seq: str,
) -> pa.DataType:
    precision, scale = seq.split(',', 1)
    dtype = pa.decimal256(int(precision), int(scale))
    return dtype


def list_(
        seq: str,
) -> pa.DataType:
    return pa.list_(_dtype_from_string(seq))


def struct(
        seq: str,
) -> pa.DataType:
    return pa.struct(
        [(f'f{y}', _dtype_from_string(z)) for y, z in enumerate(_split_skipping_parenthesis(seq), start=1)]
    )


def map_(
        seq: str,
) -> pa.DataType:
    k, v = _split_skipping_parenthesis(seq)
    dtype = pa.map_(_dtype_from_string(k), _dtype_from_string(v))
    return dtype


def nullable(
        seq: str,
) -> pa.DataType:
    return _dtype_from_string(seq)


_dtype_funcs = {
    'DateTime64(': (11, timestamp),
    'Decimal(': (8, decimal),
    'Decimal256(': (11, decimal256),
    'FixedString(': (12, fixed_size_binary),
    'Array(': (6, list_),
    'Tuple(': (6, struct),
    'Map(': (4, map_),
    'Nullable(': (9, nullable),
}


def _dtype_from_string(
        seq: str,
) -> pa.DataType:
    if seq in _dtypes:
        dtype = _dtypes[seq]
    else:
        for name, (i, func) in _dtype_funcs.items():
            if seq.startswith(name):
                dtype = func(seq[i:-1])
                break
        else:
            raise ValueError(seq)
    return dtype


def dtype_from_string(
        seq: str,
) -> pa.DataType:
    return _dtype_from_string(seq.replace(' ', ''))


def field_from_string(
        seq: str,
) -> pa.Field:
    i = None
    for j, s in enumerate(seq):
        if i is None:
            if s != ' ':
                i = j
        else:
            if s == ' ':
                break
    else:
        raise ValueError(seq)
    field = pa.field(seq[i:j], dtype_from_string(seq[j + 1:]))
    return field


def schema_from_string(
        seq: str,
) -> pa.Schema:
    return pa.schema([field_from_string(x) for x in _split_skipping_parenthesis(seq)])


__all__ = [
    'dtype_from_string',
    'field_from_string',
    'schema_from_string',
]
