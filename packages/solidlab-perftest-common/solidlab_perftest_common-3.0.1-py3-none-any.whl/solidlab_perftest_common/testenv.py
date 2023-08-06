import enum
from datetime import timedelta, datetime
from typing import Optional, Union, List, Dict, Any

from pydantic import BaseModel


class TestEnvStatus(enum.Enum):
    STARTING = "STARTING"
    # RUNNING says nothing about any active agent(s). Check agents for that.
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    # FAILED: Something went wrong. (So it is possible the TestEnv is partially running without agents, etc.)
    FAILED = "FAILED"


class TestEnvDef(BaseModel):
    # Describes the setup used to run tests in
    id: int
    name: str
    description: str
    # TODO especRepo: repo  # details about ESpec to use
    # fixed parameters for this environment. For example: clientCount, serverCpuCount,
    fixed_parameters: Dict[int, Union[str, int, bool]]  # parameterId to parameterValue


class TestEnv(BaseModel):
    # Describes a running test setup in which tests (= TestFragments) can be run
    id: int
    testenv_def_id: int
    slice_urn: str
    auth_token: str  # auth token needed by agent running to auth themselves to perftest-server
    status: TestEnvStatus

    # commit_id: the CSS commit currently installed. This can be changed by running tests.
    commit_id: Optional[int]
    # TODO in_use: Optional[int]  # ActiveSweepId  # locked because in use by a certain active TestFragment
