from sqlalchemy.orm import Session
from typing import Annotated
from core.auth import get_current_user
from core.database_config import get_db
from fastapi import Depends

DBSessionDep = Annotated[Session, Depends(get_db)]
CurrentUserDep = Annotated[dict, Depends(get_current_user)]
