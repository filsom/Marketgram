from sqlalchemy.types import BigInteger
from sqlalchemy.ext.compiler import compiles


class BIGSERIAL(BigInteger):
    pass


@compiles(BIGSERIAL, "postgresql")
def compile_bigserial_pg(type_, compiler, **kw):
    return "BIGSERIAL"