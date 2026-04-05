from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from schema.user_input import UserInput, QuestionInput
from openai import OpenAI
from dotenv import load_dotenv

import os
import pickle
import pandas as pd



with open('model/health_model.pkl', 'rb') as f:
    model = pickle.load(f)

MODEL_VERSION = '1.0.0'

load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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


@app.post('/ask')
def ask(data: QuestionInput):
    try:
        response = client.responses.create(
            model="gpt-5.4",
            instructions=(
                "You are a helpful health assistant. "
                "Answer the user's question based on the health information provided in their message. "
                "Be clear, simple, and practical. "
                "Do not claim to be a doctor, and do not give a medical diagnosis."),            
            input=data.question,
        )

        return {
            "answer": response.output_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))