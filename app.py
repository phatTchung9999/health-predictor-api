from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

import pickle
import pandas as pd

with open('model/health_model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120)]
    weight: Annotated[float, Field(..., gt=0)]
    height: Annotated[float, Field(..., gt=0)]
    isSmoker: Annotated[bool, Field(..., description='True or False')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
@app.post('/predict')
def predict(user_input: UserInput):
    input_df = pd.DataFrame(
        [
            {
                'age': user_input.age,
                'weight': user_input.weight,
                'height': user_input.height,
                'bmi': user_input.bmi,
                'isSmoker': int(user_input.isSmoker)
            }
        ]
    )

    prediction = model.predict(input_df)[0]

    if prediction == 0:
        result = 'unhealthy'
    elif prediction == 1:
        result = 'healthy'

    return JSONResponse(status_code=200, content=
        {
            'result': result
        }
    )
