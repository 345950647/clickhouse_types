# ClickHouse-Types

Converting ClickHouse types into other schemas' types

---

## PyArrow

```python
from clickhouse_types.pyarrow import dtype_from_string

dtype_from_string('Array(DateTime64(9, Asia/Shanghai))')
```

```
>>> list<item: timestamp[ns, tz=Asia/Shanghai]>
```

```python
from clickhouse_types.pyarrow import field_from_string

field_from_string('HelloWorld Map(UInt128, DateTime64(9, Asia/Shanghai))')
```

```
>>> pyarrow.Field<HelloWorld: map<fixed_size_binary[16], timestamp[ns, tz=Asia/Shanghai]>>
```

```python
from clickhouse_types.pyarrow import schema_from_string

schema_from_string('Hello FixedString(6), World Tuple(Int8, Int8)')
```

```
>>> Hello: fixed_size_binary[6]
>>> World: struct<f1: int8, f2: int8>
>>>   child 0, f1: int8
>>>   child 1, f2: int8
```

## SQLAlchemy & ClickHouse-SQLAlchemy

```python
from clickhouse_types.sqlalchemy import type_from_string

type_from_string('DateTime64(9,Asia/Shanghai)')
```

```
>>> DateTime64(9, 'Asia/Shanghai')
```