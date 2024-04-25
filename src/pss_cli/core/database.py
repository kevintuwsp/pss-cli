from typing import List, Optional, Sequence, Union
from sqlmodel import SQLModel, Session, select, create_engine
from sqlalchemy import ColumnElement

from pss_cli.core.logging import log


class Database:
    def __init__(self, sqlite_filename: str):
        sqlite_url = f"sqlite:///{sqlite_filename}"
        self.engine = create_engine(sqlite_url)

    def get_all_table_names(self) -> List[str]:
        """Return a list of all table names"""
        return list(map(str, SQLModel.metadata.tables.keys()))

    def get_table_object(self, table_name: str):
        """Return a SQLModel of the table from the table name"""

        tables_dict = {
            str(table.__tablename__): table for table in SQLModel.__subclasses__()
        }
        return tables_dict.get(table_name)

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(bind=self.engine)

    def select_table(
        self,
        table_name: str,
        where: Optional[ColumnElement[bool]] = None,
        session: Optional[Session] = None,
    ) -> Union[Sequence[SQLModel], Sequence[None], None]:
        """Return objects from the database table"""

        table_obj = self.get_table_object(table_name)
        statement = select(table_obj)
        if where is not None:
            statement = statement.where(where)

        if not session:
            with Session(self.engine) as session:
                results = session.exec(statement).all()
        else:
            results = session.exec(statement).all()

        if None in results:
            return None

        log.info(results)

        return results

    def session(self):
        """Return a session object"""
        return Session(self.engine)

    def add(self, obj: SQLModel, session: Session, commit: bool = True):
        """Add an object to the database"""

        session.add(obj)

        if commit:
            session.commit()
            session.refresh(obj)
        # print(f"Added {obj.__tablename__} object to the database:")
        # print_model(obj)
        return obj

    def commit(self, session: Session):
        """Commit the session"""
        session.commit()


db = Database(sqlite_filename="sqlite.db")
