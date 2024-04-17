from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class ScenarioCaseLink(SQLModel, table=True):
    scenario_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="scenario.id"
    )
    case_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="case.id"
    )


class Scenario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = None
    cases: List["Case"] = Relationship(
        back_populates="scenarios", link_model=ScenarioCaseLink
    )


class Case(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    file_name: str
    md5_hash: str
    description: Optional[str] = None
    rel_path: Optional[str] = None
    scenarios: List["Scenario"] = Relationship(
        back_populates="cases", link_model=ScenarioCaseLink
    )
    dynamic_files: List["CaseDynamicFile"] = Relationship(back_populates="case")
    generating_systems: List["GeneratingSystem"] = Relationship(back_populates="case")
    inf_generator: "InfGenerator" = Relationship(back_populates="case")


class CaseDynamicFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_name: str
    rel_path: Optional[str] = None
    case_id: Optional[int] = Field(default=None, foreign_key="case.id")
    case: "Case" = Relationship(back_populates="dynamic_files")


class GeneratingSystem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    from_bus: int
    to_bus: int
    case_id: Optional[int] = Field(default=None, foreign_key="case.id")
    case: "Case" = Relationship(back_populates="generating_systems")
    generators: List["Generator"] = Relationship(back_populates="generating_systems")
    setpoints: "GeneratingSystemSetpoint" = Relationship(
        back_populates="generating_system"
    )


class Generator(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bus_number: int
    machine_id: str = "1"
    generating_system_id: Optional[int] = Field(
        default=None, foreign_key="generatingsystem.id"
    )
    generating_systems: "GeneratingSystem" = Relationship(back_populates="generators")


class InfGenerator(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bus_number: int
    remote_bus_number: int
    machine_id: str = "1"
    case_id: Optional[int] = Field(default=None, foreign_key="case.id")
    case: "Case" = Relationship(back_populates="inf_generator")
    setpoint: "InfGeneratorSetpoint" = Relationship(back_populates="generator")


class GeneratingSystemSetpoint(SQLModel, table=True):
    scenario_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="scenario.id"
    )
    generating_system_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="generatingsystem.id"
    )

    p_setpoint: Optional[float] = None
    q_setpoint: Optional[float] = None
    generating_system: "GeneratingSystem" = Relationship(back_populates="setpoints")


class InfGeneratorSetpoint(SQLModel, table=True):
    scenario_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="scenario.id"
    )
    inf_generator_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="infgenerator.id"
    )

    v_setpoint: Optional[float] = None
    generator: "InfGenerator" = Relationship(back_populates="setpoint")
