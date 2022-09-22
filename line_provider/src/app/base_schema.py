import pydantic


class BaseSchema(pydantic.BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
