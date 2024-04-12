from typing import List
from sqlmodel import SQLModel, Session, select, create_engine


sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

engine = create_engine(sqlite_url)


def get_all_table_names() -> List[str]:
    """Return a list of all table names"""

    return SQLModel.metadata.tables.keys()


def get_table_object(table_name: str):
    tables_dict = {table.__tablename__: table for table in SQLModel.__subclasses__()}
    return tables_dict.get(table_name)


def create_db_and_tables():
    print("Creating database and tables")
    SQLModel.metadata.create_all(bind=engine)


def select_table(table_name: str):
    """Return objects from the database table"""

    table_obj = get_table_object(table_name)
    with Session(engine) as session:
        results = session.exec(select(table_obj)).all()

    return results
