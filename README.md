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

## SQLAlchemy & ClickHouse-SQLAlchemy

```python
from clickhouse_types.sqlalchemy import type_from_string

type_from_string('DateTime64(9,Asia/Shanghai)')
```

```
>>> DateTime64(9, 'Asia/Shanghai')
```