from pydantic import BaseModel
import pssepath

from pss_cli.utils.silence import SilenceStdout

pssepath.add_pssepath()

import psse34  # noqa: F401, E402  # type: ignore
import psspy  # noqa: E402  # type: ignore

from pss_cli.psse.api.case_data import PsseCaseDataMixin  # noqa: E402


class PsseAPI(PsseCaseDataMixin, BaseModel):
    initialised: bool = False

    def __post_init__(self):
        self.initialised = False

    def initialise(self, num_busses: int = 200000) -> None:
        """Initialise PSSE"""

        if not self.initialised:
            with SilenceStdout():
                psspy.psseinit(num_busses)
            self.initialised = True

    def load_case(self, fpath: str) -> None:
        """Load a PSSE case from disk"""
        psspy.case(fpath)

    def save_case(self, fpath: str) -> None:
        """Save the loaded PSSE case to disk"""
        psspy.save(fpath)


api = PsseAPI()
