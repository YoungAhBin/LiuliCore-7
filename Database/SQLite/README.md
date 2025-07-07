SQLite是轻量型结构化数据库。以下为借助ORM框架 SQLAlchemy 实现对SQLite数据库的增删改查，SQLite可以不事先建立，直接声明，在写入内容的时候，会自动建立，其它SQL数据库需提前建立好，才可以取得联系。

# SQLAlchemy框架解释说明
sqlalchemy就是把数据库变成一个对象操作的框架，stmt = select(User).where(User.name == "patrick")这一行代码返回的值就是sql查询语句，patrick = session.scalars(stmt).one()这一行代码就是执行了sql查询语句，所以这个框架就是通过python语言写sql查询语言来操作数据库，为什么可以适应多种数据库，因为在建立引擎的时候进行了声明，所以会产生对应的sql语句。增删改查为什么必须commit，因为前面语句都是标记，只有commit会提交任务执行。
# 以下为完整示例代码
```python

# 建立连接——引擎

from sqlalchemy import create_engine
engine = create_engine(r"sqlite+pysqlite:///C:\Users\传防科电脑\Desktop\memory_registry.db", echo=True)


# 定义表结构

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# 只要定义了继承自 DeclarativeBase（或 declarative_base()）的 ORM 类，所有这些表结构的信息就会自动被收集到 Base.metadata 中。

print(Base.metadata.tables.keys())


# 在数据库中创建表

Base.metadata.create_all(engine)


# 建立会话对象

from sqlalchemy.orm import Session
session = Session(engine)


# 增加数据

spongebob = User(
    name="spongebob",
    fullname="Spongebob Squarepants",
    addresses=[Address(email_address="spongebob@sqlalchemy.org")],
)
sandy = User(
    name="sandy",
    fullname="Sandy Cheeks",
    addresses=[
        Address(email_address="sandy@sqlalchemy.org"),
        Address(email_address="sandy@squirrelpower.org"),
    ],
)
patrick = User(name="patrick", fullname="Patrick Star")
session.add_all([spongebob, sandy, patrick])  # 单条数据用这个session.add(new_user)
session.commit()


# 选择数据

from sqlalchemy import select

session = Session(engine)

stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

for user in session.scalars(stmt):
    print(user)


# 更改数据

stmt = select(User).where(User.name == "patrick")
patrick = session.scalars(stmt).one()
patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))

stmt = select(User).where(User.name == "sandy")
sandy = session.scalars(stmt).one()
sandy.name = "libin"  

sandy.name = "libin"  #如果增加数据增加过这个对象，这个实例化对象已经存在在这个进程中，不用查询，直接修改这个对象的属性就可以

session.commit()
sandy.name


# 删除数据

stmt = select(User).where(User.name == "sandy")
sandy = session.scalars(stmt).one()
# user = session.get(User, 2) # 这种方式也可以取出来sandy这个对象
session.delete(sandy)       # 标记为删除
session.commit()           # 实际发出 DELETE SQL
```
