from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal


class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120)]
    weight: Annotated[float, Field(..., gt=0)]
    height: Annotated[float, Field(..., gt=0)]
    smoker: Annotated[bool, Field(..., description='True or False')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
class QuestionInput(BaseModel):
    question : Annotated[str, Field(..., description='Question that you want to ask gpt')]