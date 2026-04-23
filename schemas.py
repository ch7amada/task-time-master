from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Annotated
from fastapi import Query

"""
General validation schemas for fastapi data:
- BaseModel shared
- Model to create a new object -> nothing
- for update everything is optional
- Response
"""

class TimesheetBase(BaseModel):
    date: datetime
    type: int
    task: str
    costbearer: int
    duration: float

class TimesheetCreate(TimesheetBase):
    pass

class TimesheetUpdate(BaseModel):
    date: Optional[datetime] = None
    type: Optional[int] = None
    task: Optional[str] = None
    costbearer: Optional[int] = None
    duration: Optional[float] = None

def timesheet_update_params(
    date: Annotated[Optional[str], Query()] = None,
    type: Annotated[Optional[int], Query()] = None,
    task: Annotated[Optional[str], Query()] = None,
    costbearer: Annotated[Optional[int], Query()] = None,
    duration: Annotated[Optional[float], Query()] = None,
) -> TimesheetUpdate:
    parsed_date = None
    if date:
        try:
            parsed_date = datetime.strptime(date, "%d.%m.%Y %H:%M")
        except ValueError:
            from fastapi import HTTPException
            raise HTTPException(status_code=422, detail="Invalid date format. Expected DD.MM.YYYY HH:MM")
    return TimesheetUpdate(
        date=parsed_date,
        type=type,
        task=task,
        costbearer=costbearer,
        duration=duration,
    )

class TimesheetResponse(TimesheetBase):
    id: int

    # This tells Pydantic to read data even if it's not a dict, but an ORM model
    model_config = ConfigDict(from_attributes=True)