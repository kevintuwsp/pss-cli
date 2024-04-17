import typer

from sqlmodel import Session, select
from rich import print

from pss_cli.core.models import Scenario, Case, CaseDynamicFile


app = typer.Typer()


# @app.command()
# def query_data():
#     with Session(engine) as session:
#         results = session.exec(
#             select(Scenario, Case, CaseDynamicFile)
#             .join(Case, isouter=True, onclause=Scenario.cases)
#             .join(CaseDynamicFile, isouter=True, onclause=Case.dynamic_files)
#         ).all()
#         for result in results:
#             print(results)
