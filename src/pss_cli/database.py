from sqlmodel import SQLModel, create_engine


sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

engine = create_engine(sqlite_url)


def create_db_and_tables():
    print("Creating database and tables")
    SQLModel.metadata.create_all(bind=engine)
