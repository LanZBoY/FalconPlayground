
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from utils import config
import falcon

class SessionContext:

    def __init__(self, url = config.DB_CONNECTION) -> None:
        self.DB_CONNECTION = url

    def __enter__(self) -> Session:
        self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={self.DB_CONNECTION}", echo = True)
        self.session = Session(self.engine)
        return self.session
    
    def __exit__(self, type, value, traceback):
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            raise falcon.HTTPBadRequest(title = "Acton exception.", code = "ACTION_EXCEPTION")
        self.session.close()
