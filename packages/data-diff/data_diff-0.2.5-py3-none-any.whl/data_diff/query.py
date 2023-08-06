from runtype import dataclass

SKIP = object()


def _drop_skips(exprs):
    return [e for e in exprs if e is not SKIP]


class ITable:
    def __init__(self, *path):
        assert all(isinstance(str, i) for i in path)
        self.path = path

    def select(self, *exprs):
        exprs = _drop_skips(exprs)
        ...

    def where(self, *exprs):
        exprs = _drop_skips(exprs)
        if not exprs:
            return self

        ...

    def at(self, *exprs):
        exprs = _drop_skips(exprs)
        if not exprs:
            return self
        ...

    def join(self, target):
        return Join(self, target)

    def group_by(self, *, keys=None, values=None):
        assert keys or values
        pass

    def with_schema(self):
        pass

    def __getattr__(self, column):
        if column not in self.columns:
            raise KeyError()
        return Column(self, column)


class Table(ITable):
    def insert_values(self, rows):
        pass

    def insert_query(self, query):
        pass


class Q:
    def __getattr__(self, name):
        return _ResolveName(name)

    def __getitem__(self, name):
        return _ResolveName(name)


class Join(ITable):
    def on(self, *exprs):
        exprs = _drop_skips(exprs)
        if not exprs:
            return self


def join(*tables):
    "Joins each table into a 'struct'"
    ...


class Select(ITable):
    pass


class GroupBy(ITable):
    def having(self):
        pass


@dataclass
class Select(ITable):
    columns: Sequence[SqlOrStr]
    table: SqlOrStr = None
    where: Sequence[SqlOrStr] = None
    order_by: Sequence[SqlOrStr] = None
    group_by: Sequence[SqlOrStr] = None
    limit: int = None

    def compile(self, parent_c: Compiler):
        c = parent_c.replace(in_select=True)
        columns = ", ".join(map(c.compile, self.columns))
        select = f"SELECT {columns}"

        if self.table:
            select += " FROM " + c.compile(self.table)

        if self.where:
            select += " WHERE " + " AND ".join(map(c.compile, self.where))

        if self.group_by:
            select += " GROUP BY " + ", ".join(map(c.compile, self.group_by))

        if self.order_by:
            select += " ORDER BY " + ", ".join(map(c.compile, self.order_by))

        if self.limit is not None:
            select += " " + c.database.offset_limit(0, self.limit)

        if parent_c.in_select:
            select = "(%s)" % select
        return select


@dataclass
class Cte(ITable):
    expr: Expr
    name: str
    params: Tuple[str, ...]


def make_cte(t, *, name=None, params=None):
    return Cte()


def test1():
    src = Table("src_table")
    q = src.select(src.a, src.b).where(src.a > src.b + 1)
