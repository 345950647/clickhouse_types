# ClickHouse-Types

Converting ClickHouse types into other schema types

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

schema_from_string('HelloWorld Map(UInt128, DateTime64(9, Asia/Shanghai))')
```

```
>>> HelloWorld: map<fixed_size_binary[16], timestamp[ns, tz=Asia/Shanghai]>
>>>   child 0, entries: struct<key: fixed_size_binary[16] not null, value: timestamp[ns, tz=Asia/Shanghai]> not null
>>>       child 0, key: fixed_size_binary[16] not null
>>>       child 1, value: timestamp[ns, tz=Asia/Shanghai]
```

## SQLAlchemy & ClickHouse-SQLAlchemy

```python
from clickhouse_types.sqlalchemy import type_from_string

type_from_string('DateTime64(9,Asia/Shanghai)')
```

```
>>> DateTime64(9, 'Asia/Shanghai')
```