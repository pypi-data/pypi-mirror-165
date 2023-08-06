from ehelply_bootstrapper.drivers.driver import Driver
from ehelply_bootstrapper.utils.connection_details import ConnectionDetails
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from pydantic import BaseModel


class MySQLCredentials(ConnectionDetails):
    database: str


class Mysql(Driver):
    def __init__(
            self,
            credentials: MySQLCredentials,
            verbosity: int = 0,
            use_async: bool = False,
            pool_size: int = 4,
            max_overflow: int = 4
    ):
        super().__init__(verbosity=verbosity)
        self.Base = None
        self.SessionLocal = None
        self.credentials: MySQLCredentials = credentials

        self.use_async: bool = use_async
        self.pool_size: int = pool_size
        self.max_overflow: int = max_overflow

    def setup(self):

        if self.use_async:
            engine = create_async_engine(
                self.make_connection_string(
                    "mysql",
                    self.credentials.host,
                    self.credentials.port,
                    self.credentials.database,
                    self.credentials.username,
                    self.credentials.password
                ),
                pool_pre_ping=True,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow
            )

            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine,
                expire_on_commit=False,
                class_=AsyncSession
            )
        else:
            engine = create_engine(
                self.make_connection_string(
                    "mysql",
                    self.credentials.host,
                    self.credentials.port,
                    self.credentials.database,
                    self.credentials.username,
                    self.credentials.password
                ),
                pool_pre_ping=True,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow
            )

            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        self.Base = declarative_base()

    def make_connection_string(self, driver: str, host: str, port: int, database_name: str, username: str,
                               password: str):
        driver_type: str = "pymysql"
        if self.use_async:
            driver_type = "aiomysql"

        return driver + f"+{driver_type}://" + username + ':' + password + '@' + host + ':' + str(port) + '/' + database_name

    # def inject_fastapi_middleware(self, app: FastAPI):
    #     @app.middleware("http")
    #     async def db_session_middleware(request: Request, call_next):
    #         response = Response("Internal server error", status_code=500)
    #         try:
    #             request.state.db = self.SessionLocal()
    #             response = await call_next(request)
    #         finally:
    #             request.state.db.close()
    #         return response
