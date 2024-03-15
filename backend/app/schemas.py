from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator
from pydantic_geojson import FeatureModel


class DateRange(BaseModel):
    start: str
    end: str


    @validator('start', 'end')
    def check_isoformat(cls, v):
        try:
            datetime.fromisoformat(v)
        except ValueError:
            raise ValueError('Date is not in ISO format')
        return v


class ProjectBase(BaseModel):
    name: str = Field(max_length=32, description="Maximum 32 characters")
    description: Optional[str]

    date_range: DateRange
    area_of_interest: FeatureModel


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int

    class Config:
        # orm_mode = True
        from_attributes = True


class ProjectList(BaseModel):
    projects: List[Project]
