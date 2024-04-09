import os

from tabulate import tabulate

from rich import print
from sqlmodel import Session, select

from .models import Scenario, Case, CaseDynamicFile
from .database import engine, create_db_and_tables, sqlite_filename


def create_test_data():
    with Session(engine) as session:
        case_1 = Case(name="Case 1", file_name="case_1.sav")
        case_2 = Case(name="Case 2", file_name="case_2.sav")

        scenario_1 = Scenario(name="Scenario 1", cases=[case_1, case_2])
        scenario_2 = Scenario(name="Scenario 2", cases=[case_2])
        scenario_3 = Scenario(name="Scenario 3", cases=[case_1, case_2])
        scenario_4 = Scenario(name="Scenario 4", cases=[case_1])

        session.add(case_1)
        session.add(case_2)
        session.add(scenario_1)
        session.add(scenario_2)
        session.add(scenario_3)
        session.add(scenario_4)

        # session.commit()

        dynamic_file_1 = CaseDynamicFile(file_name="case_1.dll", case=case_1)
        dynamic_file_2 = CaseDynamicFile(file_name="dsusr.dll", case=case_1)

        dynamic_file_3 = CaseDynamicFile(file_name="case_2.dll", case=case_2)
        dynamic_file_4 = CaseDynamicFile(file_name="dsusr.dll", case=case_2)

        session.add(dynamic_file_1)
        session.add(dynamic_file_2)
        session.add(dynamic_file_3)
        session.add(dynamic_file_4)

        session.commit()


def query_data():
    with Session(engine) as session:
        results = session.exec(
            select(Scenario, Case, CaseDynamicFile)
            .join(Case, isouter=True, onclause=Scenario.cases)
            .join(CaseDynamicFile, isouter=True, onclause=Case.dynamic_files)
        ).all()
        # for result in results:
        print_tabulate(results)


def print_tabulate(result):
    # print(tabulate(result, headers=result.keys(), tablefmt="psql"))
    print(tabulate(result, tablefmt="psql"))


def main():
    print("pss-cli entry point")
    if os.path.exists(sqlite_filename):
        os.remove(sqlite_filename)
    create_db_and_tables()
    create_test_data()
    query_data()
