from pydantic import BaseModel


class CompanyProfileCreate(BaseModel):
    company_name: str
    communication_style: str
    meeting_frequency: str
    work_pace: str
    environment_type: str
    remote_policy: str


class CompanyProfileOut(CompanyProfileCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
