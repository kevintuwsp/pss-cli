from pydantic import BaseModel
from pss_cli.psse.api.case_data import PsseCaseDataMixin
import pssepath

pssepath.add_pssepath()

import psse34  # noqa: F401, E402  # type: ignore
import psspy  # noqa: E402  # type: ignore


class PsseAPI(PsseCaseDataMixin, BaseModel):
    def __init__(self):
        pass

    def initialise(self, num_busses: int = 200000) -> None:
        """Initialise PSSE"""
        psspy.psseinit(num_busses)

    def load_case(self, fpath: str) -> None:
        """Load a PSSE case from disk"""
        psspy.case(fpath)

    def save_case(self, fpath: str) -> None:
        """Save the loaded PSSE case to disk"""
        psspy.save(fpath)
