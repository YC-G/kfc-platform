# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT, TEXT, DATETIME, VARCHAR, SMALLINT
from sqlalchemy import Column
from werkzeug.security import check_password_hash


Base = declarative_base()
metadata = Base.metadata


class Msg(Base):
    __tablename__ = "msg"
    id = Column(BIGINT, primary_key=True)
    content = Column(TEXT)
    createdAt = Column(DATETIME, nullable=False)


class User(Base):
    __tablename__ = "user"
    id = Column(BIGINT, primary_key=True)
    name = Column(VARCHAR(20), nullable=False, unique=True)
    pwd = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(100), nullable=False, unique=True)
    phone = Column(VARCHAR(11), nullable=False, unique=True)
    createdAt = Column(DATETIME, nullable=False)

    def check_pwd(self, sub_pwd):
        return check_password_hash(self.pwd, sub_pwd)


class PoolServer(Base):
    __tablename__ = "pool_server"
    id = Column(BIGINT, primary_key=True)
    hostname = Column(VARCHAR(255), nullable=False, unique=False)
    port = Column(SMALLINT, nullable=False, unique=False)



if __name__ == "__main__":
    import mysql.connector
    from sqlalchemy import create_engine

    mysql_configs = dict(
        db_host="127.0.0.1",
        db_name="kfcplatform",
        db_port=3306,
        db_user="root",
        db_pwd="Gyc072503"
    )

    # Create link engine, link address, encoding, whether to output logs
    # link format: "db_system_name + connection_driver_name://user:password@host:port/db_name"
    engine = create_engine(
        "mysql+mysqlconnector://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}".format(**mysql_configs),
        encoding='utf-8'
    )

    metadata.create_all(engine)