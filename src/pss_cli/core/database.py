from typing import List, Optional, Sequence, Union
from sqlmodel import SQLModel, Session, select, create_engine
from sqlalchemy import ColumnElement


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
        where: Optional[
            Union[List[ColumnElement[bool]], List[ColumnElement[bool]]]
        ] = None,
        session: Optional[Session] = None,
    ) -> Union[Sequence[SQLModel], Sequence[None], None]:
        """Return objects from the database table"""

        table_obj = self.get_table_object(table_name)
        statement = select(table_obj)

        if where is not None:
            if isinstance(where, list):
                for where_clause in where:
                    statement = statement.where(where_clause)
            else:
                statement = statement.where(where)

        if not session:
            with self.session() as session:
                results = session.exec(statement).all()
        else:
            results = session.exec(statement).all()

        if None in results:
            return None

        return results

    def session(self):
        """Return a session object"""
        return Session(self.engine)

    def add_all(self, objs: Sequence[SQLModel], session: Session, commit: bool = True):
        """Add a list of objects to the database"""

        for obj in objs:
            session.add(obj)
        if commit:
            session.commit()

        return objs

    def add(self, obj: SQLModel, session: Session, commit: bool = True):
        """Add an object to the database"""

        session.add(obj)

        if commit:
            session.commit()
            session.refresh(obj)
        return obj

    def delete(self, obj: SQLModel, session: Session, commit: bool = True):
        """Delete an object from the database"""

        session.delete(obj)

        if commit:
            session.commit()

    def commit(self, session: Session):
        """Commit the session"""
        session.commit()


db = Database(sqlite_filename="sqlite.db")
