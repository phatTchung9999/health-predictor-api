import streamlit as st
import requests


API_URL = "http://localhost:8000/predict"
OPENAI_URL = "http://localhost:8000/ask"


st.set_page_config(page_title="Health Predictor", page_icon="🩺")

if "health_data" not in st.session_state:
    st.session_state.health_data = None
if "result" not in st.session_state:
    st.session_state.result = None

st.title("🩺 Health Predictor")

st.divider()

col1, col2 = st.columns(2, gap='large')


with col1:
    st.write("Enter your information below to get a health prediction.")

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
                
                st.session_state.health_data = {
                    "age": age,
                    "weight": weight,
                    "height": height,
                    "smoker": smoker,
                    "bmi": bmi,
                    "label": result
                }

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

with col2:
    st.write('Body Mass Index (BMI)')
    st.image('images/bmi_chart.png', use_container_width=True)


st.divider()

with st.form('chat_box'):
    question = st.text_input(label= 'Ask our AI how to get back in shape and stay healthy:' ,
                placeholder='How can I imporve my health?') 
    
    sent = st.form_submit_button("Ask") 

    if sent:
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try: 
                if st.session_state.health_data:
                    health = st.session_state.health_data
                    full_question = (
                        f"Here is the user's health information: "
                        f"age={health['age']}, weight={health['weight']} kg, "
                        f"height={health['height']} m, smoker={health['smoker']}, "
                        f"bmi={health['bmi']}, prediction_label={health['label']}. "
                        f"Now answer this question: {question}"
                    )
                elif st.session_state.result:
                    last_result = st.session_state.result
                    full_question = (
                        f"Here is your last answer: {last_result}"
                        f"Now answer this question following up the last answer: {question}"
                    )
                else:
                    full_question = question
                with st.spinner("Thinking..."):
                    answer = requests.post(
                        OPENAI_URL,
                        json={"question": full_question},
                        timeout=20
                    ) 

                if answer.status_code == 200:
                    data = answer.json()
                    result = data.get('answer', 'No result returned')
                    st.success(f"Answer: {result}")
                    st.session_state.result = {
                        'last_result': result
                    }
                    st.session_state.health_data = None
                else:
                    st.error(f"Request failed: {answer.status_code}")
                    st.text(answer.text)
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI server. Make sure it is running on port 8000.")
            except requests.exceptions.Timeout:
                st.error("Request timed out.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")




    