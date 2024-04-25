from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class ScenarioCaseLink(SQLModel, table=True):
    scenario_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="scenario.id"
    )
    case_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="case.id"
    )
    file_path: str
    md5_hash: str
    case: "Case" = Relationship(back_populates="scenario_links")
    scenario: "Scenario" = Relationship(back_populates="case_links")


class Scenario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = None
    bus_values: List["ScenarioBusValues"] = Relationship(back_populates="scenario")
    branch_values: List["ScenarioBranchValues"] = Relationship(
        back_populates="scenario"
    )
    case_links: List["ScenarioCaseLink"] = Relationship(back_populates="scenario")


class Case(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    file_path: str
    md5_hash: str
    description: Optional[str] = None
    rel_path: Optional[str] = None
    dynamic_files: List["CaseDynamicFile"] = Relationship(back_populates="case")
    generating_systems: List["GeneratingSystem"] = Relationship(back_populates="case")
    inf_generator: "InfGenerator" = Relationship(back_populates="case")
    bus_data: List["CaseBusData"] = Relationship(back_populates="case")
    branch_data: List["CaseBranchData"] = Relationship(back_populates="case")
    bus_values: List["ScenarioBusValues"] = Relationship(back_populates="case")
    branch_values: List["ScenarioBranchValues"] = Relationship(back_populates="case")
    scenario_links: List["ScenarioCaseLink"] = Relationship(back_populates="case")


class CaseDynamicFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_path: str
    rel_path: Optional[str] = None
    case_id: Optional[int] = Field(default=None, foreign_key="case.id")
    case: "Case" = Relationship(back_populates="dynamic_files")


class GeneratingSystem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    from_bus: int
    to_bus: int
    reversed: bool = Field(default=False)
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


class BusDefinition(SQLModel, table=True):
    case_id: Optional[int] = Field(foreign_key="case.id")
    bus_number: int = Field(primary_key=True)
    bus_name: str
    bus_base_voltage: float
    bus_type: int
    case: "Case" = Relationship(back_populates="bus_data")


class BranchDefinition(SQLModel, table=True):
    case_id: Optional[int] = Field(foreign_key="case.id")
    from_bus_number: int = Field(primary_key=True)
    to_bus_number: int = Field(primary_key=True)
    branch_id: str = Field(primary_key=True)
    from_bus_name: str
    to_bus_name: str
    pos_seq_impedance_pu: float
    zero_seq_impedance_pu: float
    pos_seq_charging_capacitance_pu: float
    zero_seq_charging_capacitance_pu: float
    case: "Case" = Relationship(back_populates="branch_data")


class MachineDefinition(SQLModel, table=True):
    case_id: Optional[int] = Field(foreign_key="case.id")
    bus_number: int = Field(primary_key=True)
    machine_id: str = Field(primary_key=True)
    machine_name: str
    case: "Case" = Relationship(back_populates="branch_data")


class MachineValues(SQLModel, table=True):
    case_id: Optional[int] = Field(primary_key=True, foreign_key="case.id")
    scenario_id: Optional[int] = Field(primary_key=True, foreign_key="scenario.id")
    bus_number: int = Field(primary_key=True)
    machine_id: str = Field(primary_key=True)
    mbase_mva: float
    active_power_mw: float
    reactive_power_mvar: float
    pmax: float
    pmin: float
    qmax: float
    qmin: float


class BusValues(SQLModel, table=True):
    case_id: Optional[int] = Field(primary_key=True, foreign_key="case.id")
    scenario_id: Optional[int] = Field(primary_key=True, foreign_key="scenario.id")
    bus_number: int = Field(primary_key=True, foreign_key="casebusdata.bus_number")
    bus_voltage_pu: float
    bus_voltage_kv: float
    bus_voltage_angle_deg: float
    case: "Case" = Relationship(back_populates="bus_values")
    scenario: "Scenario" = Relationship(back_populates="bus_values")


class BranchValues(SQLModel, table=True):
    case_id: Optional[int] = Field(primary_key=True, foreign_key="case.id")
    scenario_id: Optional[int] = Field(primary_key=True, foreign_key="scenario.id")
    from_bus_number: int = Field(
        primary_key=True, foreign_key="casebranchdata.from_bus_number"
    )
    to_bus_number: int = Field(
        primary_key=True, foreign_key="casebranchdata.to_bus_number"
    )
    branch_id: str = Field(primary_key=True, foreign_key="casebranchdata.branch_id")
    active_power_mw: float
    reactive_power_mvar: float
    case: "Case" = Relationship(back_populates="branch_values")
    scenario: "Scenario" = Relationship(back_populates="branch_values")
