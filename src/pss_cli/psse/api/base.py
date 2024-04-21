from pydantic import BaseModel
import pssepath

pssepath.add_pssepath()

import psse34  # noqa: F401, E402  # type: ignore
import psspy  # noqa: E402  # type: ignore

from pss_cli.psse.api.case_data import PsseCaseDataMixin  # noqa: E402
from pss_cli.utils.silence import SilenceStdout


class PsseAPI(PsseCaseDataMixin, BaseModel):
    def __init__(self):
        pass

    def initialise(self, num_busses: int = 200000) -> None:
        """Initialise PSSE"""
        with SilenceStdout():
            psspy.psseinit(num_busses)

    def load_case(self, fpath: str) -> None:
        """Load a PSSE case from disk"""
        psspy.case(fpath)

    def save_case(self, fpath: str) -> None:
        """Save the loaded PSSE case to disk"""
        psspy.save(fpath)


api = PsseAPI()
