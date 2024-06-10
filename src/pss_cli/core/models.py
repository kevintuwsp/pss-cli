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
    case: "Case" = Relationship(
        back_populates="scenario_links",
    )
    scenario: "Scenario" = Relationship(
        back_populates="case_links",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )


class Scenario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = None
    bus_values: List["BusValues"] = Relationship(
        back_populates="scenario",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    branch_values: List["BranchValues"] = Relationship(
        back_populates="scenario",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    machine_values: List["MachineValues"] = Relationship(
        back_populates="scenario",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    two_winding_transformer_values: List["TwoWindingTransformerValues"] = Relationship(
        back_populates="scenario",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    case_links: List["ScenarioCaseLink"] = Relationship(
        back_populates="scenario",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )


class Case(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    file_path: str
    md5_hash: str
    description: Optional[str] = None
    dynamic_files: List["CaseDynamicFile"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    generating_systems: List["GeneratingSystem"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    inf_generator: "InfGenerator" = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    bus_definitions: List["BusDefinition"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    branch_definitions: List["BranchDefinition"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    machine_definitions: List["MachineDefinition"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    two_winding_transformer_definitions: List["TwoWindingTransformerDefinition"] = (
        Relationship(
            back_populates="case",
            sa_relationship_kwargs={"cascade": "all, delete"},
        )
    )
    bus_values: List["BusValues"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    branch_values: List["BranchValues"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    machine_values: List["MachineValues"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    two_winding_transformer_values: List["TwoWindingTransformerValues"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    scenario_links: List["ScenarioCaseLink"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )


class CaseDynamicFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_path: str
    rel_path: Optional[str] = None
    case_id: Optional[int] = Field(default=None, foreign_key="case.id")
    case: "Case" = Relationship(back_populates="dynamic_files")


class GeneratingSystem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    from_bus_number: int
    to_bus_number: int
    branch_id: str
    reversed: bool = Field(default=False)
    case_id: Optional[int] = Field(default=None, foreign_key="case.id")
    case: "Case" = Relationship(back_populates="generating_systems")
    generators: List["Generator"] = Relationship(
        back_populates="generating_systems",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
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
    case_id: Optional[int] = Field(primary_key=True, foreign_key="case.id")
    bus_number: int = Field(primary_key=True)
    bus_name: str
    bus_base_voltage: float
    bus_type: int
    case: "Case" = Relationship(back_populates="bus_definitions")


class BranchDefinition(SQLModel, table=True):
    case_id: Optional[int] = Field(primary_key=True, foreign_key="case.id")
    from_bus_number: int = Field(primary_key=True)
    to_bus_number: int = Field(primary_key=True)
    branch_id: str = Field(primary_key=True)
    from_bus_name: str
    to_bus_name: str
    pos_seq_r_pu: float
    pos_seq_x_pu: float
    zero_seq_r_pu: float
    zero_seq_x_pu: float
    pos_seq_b_pu: float
    zero_seq_b_pu: float
    case: "Case" = Relationship(back_populates="branch_definitions")


class MachineDefinition(SQLModel, table=True):
    case_id: Optional[int] = Field(primary_key=True, foreign_key="case.id")
    bus_number: int = Field(primary_key=True)
    machine_id: str = Field(primary_key=True)
    machine_name: str
    case: "Case" = Relationship(back_populates="machine_definitions")


class TwoWindingTransformerDefinition(SQLModel, table=True):
    case_id: Optional[int] = Field(primary_key=True, foreign_key="case.id")
    from_bus_number: int = Field(primary_key=True)
    to_bus_number: int = Field(primary_key=True)
    branch_id: str = Field(primary_key=True)
    xfr_name: str
    pos_seq_r_pu: float
    pos_seq_x_pu: float
    zero_seq_r_pu: float
    zero_seq_x_pu: float
    vector_group: str
    controlled_bus_number: int
    sbase_mva: float
    rmax_pu: float
    rmin_pu: float
    vmax_pu: float
    vmin_pu: float
    case: "Case" = Relationship(back_populates="two_winding_transformer_definitions")


class BusValues(SQLModel, table=True):
    case_id: Optional[int] = Field(primary_key=True, foreign_key="case.id")
    scenario_id: Optional[int] = Field(primary_key=True, foreign_key="scenario.id")
    bus_number: int = Field(primary_key=True, foreign_key="busdefinition.bus_number")
    bus_voltage_pu: float
    bus_voltage_kv: float
    bus_voltage_angle_deg: float
    case: "Case" = Relationship(back_populates="bus_values")
    scenario: "Scenario" = Relationship(back_populates="bus_values")


class BranchValues(SQLModel, table=True):
    case_id: Optional[int] = Field(primary_key=True, foreign_key="case.id")
    scenario_id: Optional[int] = Field(primary_key=True, foreign_key="scenario.id")
    from_bus_number: int = Field(
        primary_key=True, foreign_key="branchdefinition.from_bus_number"
    )
    to_bus_number: int = Field(
        primary_key=True, foreign_key="branchdefinition.to_bus_number"
    )
    branch_id: str = Field(primary_key=True, foreign_key="branchdefinition.branch_id")
    active_power_mw: float
    reactive_power_mvar: float
    case: "Case" = Relationship(back_populates="branch_values")
    scenario: "Scenario" = Relationship(back_populates="branch_values")


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
    case: "Case" = Relationship(back_populates="machine_values")
    scenario: "Scenario" = Relationship(back_populates="machine_values")


class TwoWindingTransformerValues(SQLModel, table=True):
    case_id: Optional[int] = Field(primary_key=True, foreign_key="case.id")
    scenario_id: Optional[int] = Field(primary_key=True, foreign_key="scenario.id")
    from_bus_number: int = Field(
        primary_key=True, foreign_key="twowindingtransformerdefinition.from_bus_number"
    )
    to_bus_number: int = Field(
        primary_key=True, foreign_key="twowindingtransformerdefinition.to_bus_number"
    )
    branch_id: str = Field(
        primary_key=True, foreign_key="twowindingtransformerdefinition.branch_id"
    )
    ratio: float
    case: "Case" = Relationship(back_populates="two_winding_transformer_values")
    scenario: "Scenario" = Relationship(back_populates="two_winding_transformer_values")
