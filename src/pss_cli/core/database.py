from typing import List
from sqlmodel import SQLModel, Session, select, create_engine


class Database:
    def __init__(self, sqlite_filename: str):
        sqlite_url = f"sqlite:///{sqlite_filename}"
        self.engine = create_engine(sqlite_url)

    @classmethod
    def get_all_table_names(self) -> List[str]:
        """Return a list of all table names"""
        return SQLModel.metadata.tables.keys()

    @classmethod
    def get_table_object(self, table_name: str):
        """Return a SQLModel of the table from the table name"""

        tables_dict = {
            table.__tablename__: table for table in SQLModel.__subclasses__()
        }
        return tables_dict.get(table_name)

    def create_db_and_tables(self):
        print("Creating database and tables")
        SQLModel.metadata.create_all(bind=self.engine)

    def select_table(self, table_name: str):
        """Return objects from the database table"""

        table_obj = self.get_table_object(table_name)
        with Session(self.engine) as session:
            results = session.exec(select(table_obj)).all()

        print(results)

        if None in results:
            return None

        return results

    def session(self):
        """Return a session object"""
        return Session(self.engine)

    def add(self, obj: SQLModel, session: Session):
        """Add an object to the database"""

        session.add(obj)
        session.commit()
        session.refresh(obj)
        print(f"Added {obj.__tablename__} object to the database:")
        return obj


db = Database(sqlite_filename="sqlite.db")
