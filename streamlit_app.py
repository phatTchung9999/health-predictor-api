import streamlit as st
import requests

st.set_page_config(page_title="Health Predictor", page_icon="🩺")

st.title("🩺 Health Predictor")
st.write("Enter your information below to get a health prediction from your FastAPI backend.")

# Change this later if you deploy your API
API_URL = "http://3.134.78.96:8000/predict"

with st.form("health_form"):
    age = st.number_input("Age", min_value=1, max_value=119, value=25)
    weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0, step=0.1)
    height = st.number_input("Height (m)", min_value=0.5, value=1.75, step=0.01)
    smoker = st.selectbox("Do you smoke?", options=[False, True], format_func=lambda x: "Yes" if x else "No")

    submitted = st.form_submit_button("Predict")

if submitted:
    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "smoker": smoker
    }

    bmi = round(weight / (height ** 2), 2)
    st.info(f"Your BMI: **{bmi}**")

    try:
        response = requests.post(API_URL, json=payload, timeout=10)

        if response.status_code == 200:
            data = response.json()
            result = data.get("result", "No result returned")

            if result == "healthy":
                st.success(f"Prediction: {result}")
            else:
                st.error(f"Prediction: {result}")

            st.json(data)
        else:
            st.error(f"Request failed: {response.status_code}")
            st.text(response.text)

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server. Make sure it is running on port 8000.")
    except requests.exceptions.Timeout:
        st.error("Request timed out.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")