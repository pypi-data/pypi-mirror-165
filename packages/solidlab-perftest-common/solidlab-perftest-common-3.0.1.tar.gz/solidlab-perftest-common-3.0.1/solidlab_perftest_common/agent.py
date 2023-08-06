import enum
from datetime import timedelta, datetime
from typing import Optional, Union, List, Dict, Any

from pydantic import BaseModel


class AgentCommandType(enum.Enum):
    WRITE_FILE = "WRITE_FILE"
    EXEC_BASH = "EXEC_BASH"
    START_SERVICE = "START_SERVICE"
    STOP_SERVICE = "STOP_SERVICE"


class AgentCommandResultStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    TIMEOUT = "TIMEOUT"


class Agent(BaseModel):
    testenv_id: int
    machine_id: str
    last_active: datetime
    active: bool


class AgentCommandResult(BaseModel):
    command_id: int

    status: AgentCommandResultStatus
    started: datetime
    stopped: datetime

    # output of command, all optional
    return_value: Optional[int] = None
    error_msg: Optional[str] = None
    trace: Optional[str] = None
    debug_msg: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None


class AgentCommand(BaseModel):
    id: int
    testenv_id: int  # testenv_id + machine_id identifies agent the command belongs too
    machine_id: str  # testenv_id + machine_id identifies agent the command belongs too
    experiment_id: Optional[int]
    created: datetime
    name: str  # hrn of the command, ignored by agent, but useful to inform users
    type: AgentCommandType
    # data:
    #   CSS config filename, or bash commands array, or service name. Type depends on AgentCommandType.
    #   (Dict[str, Any] is not used yet, but might be in the future)
    #
    # data type by AgentCommandType:
    #   - WRITE_FILE -> List[str] with 2 elements ([filename, file_content])
    #   - EXEC_BASH -> List[str] of command parts
    #   - START_SERVICE -> str (service name)
    #   - STOP_SERVICE -> str (service name)
    #
    data: Union[str, List[str], Dict[str, Any]]
    timeout_s: float


class AgentCommandFull(AgentCommand):
    result: Optional[AgentCommandResult]
