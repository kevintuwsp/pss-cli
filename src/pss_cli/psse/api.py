from pydantic import BaseModel, validate_arguments
import pssepath

pssepath.add_pssepath()

import psse34  # noqa: F401, E402
import psspy  # noqa: E402


class PsseAPI(BaseModel):
    def __init__(self):
        pass

    @validate_arguments
    def initialise(self, num_busses: int = 200000) -> None:
        """Initialise PSSE"""
        psspy.psseinit(num_busses)

    @validate_arguments
    def load_case(self, fpath: str) -> None:
        """Load a PSSE case from disk"""
        psspy.load(fpath)

    @validate_arguments
    def save_case(self, fpath: str) -> None:
        """Save the loaded PSSE case to disk"""
        psspy.save(fpath)
