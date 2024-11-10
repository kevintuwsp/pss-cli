from collections import namedtuple
from typing import Dict, List, NamedTuple, Optional, Sequence, Union
from sqlmodel import SQLModel, Session, select, create_engine
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy.sql.expression import ColumnExpressionArgument
from sqlalchemy import and_, or_

from pss_cli.core.logging import logger


class Database:
    def __init__(self, sqlite_filename: str):
        sqlite_url = f"sqlite:///{sqlite_filename}"
        self.engine = create_engine(sqlite_url)
        self._current_session = None

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

    def get_session(self):
        """Return the current session"""
        if not self._current_session:
            self._current_session = Session(self.engine)
        return self._current_session

    def close_session(self):
        """Close the current session"""
        if self._current_session:
            self._current_session.close()
            self._current_session = None

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

    def commit(self, persist: bool = False):
        """Commit the session"""

        session = self.get_session()
        session.commit()

        if not persist:
            self.close_session()

    def add_object(
        self, object: SQLModel, commit: bool = True, persist: bool = False
    ) -> SQLModel:
        """Add an object to the database"""

        session = self.get_session()
        session.add(object)

        if commit:
            session.commit()
            session.refresh(object)

        if not persist:
            self.close_session()

        return object

    def add_objects(
        self, objects: List[SQLModel], commit: bool = True, persist: bool = False
    ) -> List[SQLModel]:
        """Add a list of objects to the database"""

        session = self.get_session()
        session.add_all(objects)
        if commit:
            session.commit()
            for object in objects:
                session.refresh(object)

        if not persist:
            self.close_session()

        return objects

    def delete_object(
        self, object: SQLModel, commit: bool = True, persist: bool = False
    ) -> None:
        """Delete an object from the database"""

        session = self.get_session()
        session.delete(object)
        if commit:
            session.commit()

        if not persist:
            self.close_session()

    def delete_objects(self, objects: List[SQLModel], commit: bool = True) -> None:
        """Delete a list of objects from the database"""

        with self.session() as session:
            for object in objects:
                session.delete(object)
            if not commit:
                return
            session.commit()

    def get_objects(
        self,
        table: SQLModel,
        conditions: Optional[List[Union[ColumnExpressionArgument[bool], bool]]] = None,
        condition_type: Optional[str] = "and",
    ) -> Sequence[Optional[SQLModel]]:
        """Return a list of objects from the database that meet the conditions"""

        session = self.get_session()
        statement = select(table)  # type: ignore
        if conditions:
            if condition_type == "and":
                condition_expression = and_(*conditions)  # type: ignore
            elif condition_type == "or":
                condition_expression = or_(*conditions)  # type: ignore
            else:
                raise ValueError("condition_type must be 'and' or 'or'")
            statement = statement.where(condition_expression)
        objects = session.exec(statement).all()

        if not objects:
            logger.error(f"Objects not found in table {table.__tablename__}")
            return []

        self.close_session()
        return objects

    def get_object(
        self,
        table: SQLModel,
        conditions: Optional[List[Union[ColumnExpressionArgument[bool], bool]]] = None,
        condition_type: Optional[str] = "and",
    ) -> Optional[SQLModel]:
        """Return a single object from the database that meets the conditions"""

        session = self.get_session()
        statement = select(table)  # type: ignore
        if conditions:
            if condition_type == "and":
                condition_expression = and_(*conditions)  # type: ignore
            elif condition_type == "or":
                condition_expression = or_(*conditions)  # type: ignore
            else:
                raise ValueError("condition_type must be 'and' or 'or'")
            statement = statement.where(condition_expression)
        object = session.exec(statement).first()

        if not object:
            logger.error(f"Object not found in table {table.__tablename__}")
            return None

        self.close_session()
        return object

    def refresh(self, obj: SQLModel):
        """Refresh the object from the database"""

        session = self.get_session()
        session.refresh(obj)
        self.close_session()

    def add_all_objects(
        self, objects: Sequence[SQLModel], commit: bool = True, persist: bool = False
    ):
        """Add a list of objects to the database"""

        session = self.get_session()
        session.add_all(objects)

        if commit:
            session.commit()

        if not persist:
            self.close_session()
            return


db = Database("sqlite.db")
