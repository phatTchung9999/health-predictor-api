from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput

import pickle
import pandas as pd

with open('model/health_model.pkl', 'rb') as f:
    model = pickle.load(f)

MODEL_VERSION = '1.0.0'

app = FastAPI()


@app.get('/')
def home():
    return {'message' : 'Health Prediction API'}

@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model': model is not None
    }


@app.post('/predict')
def predict(user_input: UserInput):
    input_df = pd.DataFrame(
        [
            {
                'age': user_input.age,
                'weight': user_input.weight,
                'height': user_input.height,
                'bmi': user_input.bmi,
                'smoker': int(user_input.smoker)
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
