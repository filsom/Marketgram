from sqlalchemy import Column, cast
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy.orm import column_property
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

Base = declarative_base()    

def ident(name: str, service: str) -> str:
    return f'{name}, {service}'


class AType(Base):
    __tablename__ = "atype"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}, name={self.name} {id(self)}>"


class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    data = Column(String)
    type_id = Column(ForeignKey("atype.id"))
    # type_name = column_property(
    #     select(AType.name).where(AType.id == type_id).correlate_except(AType).scalar_subquery()
    # )
    service = Column(String)
    # type = relationship(AType)

    __mapper_args__ = {
        "polymorphic_on": data + ', ' + service,
        "polymorphic_identity": ident('a1', 'Base'),
    }


class ASub(A):
    __mapper_args__ = {"polymorphic_identity": ident('asub1', 'Telegram')}


class ASub2(A):
    __mapper_args__ = {"polymorphic_identity": ident('asub2', 'VK')}


e = create_engine("sqlite://", echo=True)
Base.metadata.create_all(e)

sess = Session(e)

a_type, asub_type = AType(name="a"), AType(name="asub")

sess.add_all(
    [
        A(data="a1", service='Base'),
        A(data="asub1", service='Telegram'),
        A(data="asub2", service='VK'),
        # A(data="asub2", type=asub_type),
        # A(data="a2", type=a_type),
    ]
)
sess.commit()

sess = Session(e)
for a in sess.query(A):
    print(type(a), a.service)