from pss_cli.core.controllers import Controller
from pss_cli.core.models import Case, Scenario, ScenarioCaseLink
from pss_cli.core.extractors import (
    BusDefinitionObjExtractor,
    BranchDefinitionObjExtractor,
    MachineDefinitionObjExtractor,
    TwoWindingTransformerDefinitionObjExtractor,
)


class CaseController(Controller):
    """Manages the cases in the project"""

    def __init__(self):
        super().__init__()

    def add(self, *args, **kwargs):
        pass

    def delete(self, name: str) -> None:
        pass

    # def add(
    #     self, name: str, description: str, file_path: str, scenarios: List[Scenario]
    # ):
    #     """Add a case to the database"""
    #
    #     md5_hash = get_hash(file_path)
    #     with db.session() as session:
    #         case = Case(
    #             name=name,
    #             description=description,
    #             file_path=file_path,
    #             md5_hash=md5_hash,
    #         )
    #
    #         for scenario in scenarios:
    #             scenario_file_path = self.create_scenario_file(scenario, case)
    #             scenario_case_link = ScenarioCaseLink(
    #                 scenario=scenario,
    #                 case=case,
    #                 file_path=str(scenario_file_path),
    #                 md5_hash=get_hash(str(scenario_file_path)),
    #             )
    #             session.add(scenario_case_link)
    #         session.add(case)
    #         session.commit()
    #         session.refresh(case)
    #
    #         bus_definitions = BusDefinitionObjExtractor().extract(case)
    #         branch_definitions = BranchDefinitionObjExtractor().extract(case)
    #         machine_definitions = MachineDefinitionObjExtractor().extract(case)
    #         two_winding_transformer_definitions = (
    #             TwoWindingTransformerDefinitionObjExtractor().extract(case)
    #         )
    #         session.add_all(bus_definitions)
    #         session.add_all(branch_definitions)
    #         session.add_all(machine_definitions)
    #         session.add_all(two_winding_transformer_definitions)
    #         session.commit()
    #
    #         logger.info(f"Added case to the database: {case.name}")
    #
    # def delete(self, name: str):
    #     """Delete a case from the database"""
    #
    #     with db.session() as session:
    #         statement = select(Case).where(Case.name == name)
    #         case = session.exec(statement).first()
    #         if not case:
    #             logger.error(f"Case {name} not found in the database")
    #             return
    #
    #         statement = select(ScenarioCaseLink).where(
    #             ScenarioCaseLink.case_id == case.id
    #         )
    #         scenario_case_links = session.exec(statement).all()
    #
    #         for scenario_case_link in scenario_case_links:
    #             if os.path.exists(scenario_case_link.file_path):
    #                 os.remove(scenario_case_link.file_path)
    #
    #         db.delete(case, session=session)
    #         logger.info(f"Deleted case from the database: {case}")
