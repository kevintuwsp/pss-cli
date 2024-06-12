from collections import namedtuple
from typing import Dict, List, NamedTuple, Optional, Sequence, Union
from sqlmodel import SQLModel, Session, select, create_engine
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy.sql.expression import ColumnExpressionArgument
from sqlalchemy import and_, or_


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

    def add_object(self, object: SQLModel, commit: bool = True) -> SQLModel:
        """Add an object to the database"""

        with db.session() as session:
            session.add(object)
            if not commit:
                return object
            session.commit()
            session.refresh(object)

        return object

    def add_objects(
        self, objects: List[SQLModel], commit: bool = True
    ) -> List[SQLModel]:
        """Add a list of objects to the database"""

        with db.session() as session:
            session.add_all(objects)
            if not commit:
                return objects
            session.commit()
            for object in objects:
                session.refresh(object)

        return objects

    def delete_object(self, object: SQLModel, commit: bool = True) -> None:
        """Delete an object from the database"""

        with db.session() as session:
            session.delete(object)
            if not commit:
                return
            session.commit()

    def delete_objects(self, objects: List[SQLModel], commit: bool = True) -> None:
        """Delete a list of objects from the database"""

        with db.session() as session:
            for object in objects:
                session.delete(object)
            if not commit:
                return
            session.commit()

    def get_objects(
        self,
        table_name: str,
        conditions: Optional[List[ColumnExpressionArgument[bool]]] = None,
        condition_type: Optional[str] = "and",
    ):
        """Return a list of objects from the database that meet the conditions"""

        table = db.get_table_object(table_name)
        with db.session() as session:
            statement = select(table)
            if conditions:
                if condition_type == "and":
                    condition_expression = and_(*conditions)
                elif condition_type == "or":
                    condition_expression = or_(*conditions)
                else:
                    raise ValueError("condition_type must be 'and' or 'or'")
                statement = statement.where(condition_expression)
            objects = session.exec(statement).all()

        return objects

    def get_object(
        self,
        table_name: str,
        conditions: Optional[List[ColumnExpressionArgument[bool]]] = None,
        condition_type: Optional[str] = "and",
    ):
        """Return a single object from the database that meets the conditions"""

        table = db.get_table_object(table_name)
        with db.session() as session:
            statement = select(table)
            if conditions:
                if condition_type == "and":
                    condition_expression = and_(*conditions)
                elif condition_type == "or":
                    condition_expression = or_(*conditions)
                else:
                    raise ValueError("condition_type must be 'and' or 'or'")
                statement = statement.where(condition_expression)
            object = session.exec(statement).first()

        return object

    def get_objects_as_tuple(
        self,
        table_name: str,
        conditions: Optional[Dict[str, str]] = None,
    ) -> List[Optional[NamedTuple]]:
        """Return a list of objects from the database"""

        table_obj = db.get_table_object(table_name)
        if table_obj is None:
            raise ValueError(f"Table {table_name} not found in the database")

        with db.session() as session:
            statement = select(table_obj)
            if conditions is not None:
                for column, value in conditions.items():
                    statement = statement.where(getattr(table_obj.c, column) == value)
            objects = session.exec(statement).all()

        if objects:
            ObjectTuple = namedtuple("ObjectTuple", objects[0].__table__.columns.keys())
            return [ObjectTuple(*obj) for obj in objects]

        return []

    def get_object_as_tuple(
        self, table_name: str, conditions: Dict[str, str]
    ) -> Optional[NamedTuple]:
        """Return a single object from the database"""

        table_obj = db.get_table_object(table_name)
        if table_obj is None:
            raise ValueError(f"Table {table_name} not found in the database")

        with db.session() as session:
            statement = select(table_obj)
            for column, value in conditions.items():
                statement = statement.where(getattr(table_obj.c, column) == value)
            object = session.exec(statement).first()

        if object:
            ObjectTuple = namedtuple("ObjectTuple", object.__table__.columns.keys())
            return ObjectTuple(*object)

        return None


db = Database(sqlite_filename="sqlite.db")
