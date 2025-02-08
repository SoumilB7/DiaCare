from fastapi import FastAPI, Request
import json
import base64
from model import detect_diabetes, aloder
from gemini import parse_data, diagnosiser, fallback_diagnosis


app = FastAPI()

@app.get("/")
async def read_root():
    return {"Master": "The python backend"}



@app.post("/predict-diabetes/")
async def predict_diabetes(
        request: Request
    ):
    raw_body = await request.body()
    decoded_body = raw_body.decode("utf-8", errors="replace")
    data = json.loads(decoded_body)
    Pregnancies = int(data.get("Pregnancies"))
    Glucose = int(data.get("Glucose"))
    BloodPressure = int(data.get("BloodPressure"))
    SkinThickness = int(data.get("SkinThickness"))
    Insulin = int(data.get("Insulin"))
    BMI = int(data.get("BMI"))
    DiabetesPedigreeFunction = int(data.get("DiabetesPedigreeFunction"))
    Age = int(data.get("Age"))

    prediction = detect_diabetes([Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age])

    return {"Prediction" : prediction}
    

@app.post("/predict-multimodal/")
async def predict_multimodal(
        request: Request
    ):
    raw_body = await request.body()
    decoded_body = raw_body.decode("utf-8", errors="replace")
    print("issue after this : ",decoded_body[:10])
    data = json.loads(decoded_body)
    print("loading done")
    textual_content = data.get("textual_data") # bytes
    textual_content = base64.b64decode(textual_content)
    textual_output = await aloder(textual_content)
    data = parse_data(textual_output)
    print("data parsing done : ",data)
    try:
        Pregnancies = int(data.get("Pregnancies"))
        Glucose = int(data.get("Glucose"))
        BloodPressure = int(data.get("BloodPressure"))
        SkinThickness = int(data.get("SkinThickness"))
        Insulin = int(data.get("Insulin"))
        BMI = int(data.get("BMI"))
        DiabetesPedigreeFunction = int(data.get("DiabetesPedigreeFunction"))
        Age = int(data.get("Age"))

        prediction = detect_diabetes([Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age])
        if prediction == "No Diabetes" and Glucose >115:
            prediction = "Pre Diabetic"
    except:
        data = fallback_diagnosis(textual_output)
        prediction = (data.get("Diabetes-type"))

    return {"Prediction" : prediction}



@app.post("/diagnosis/")
async def diagnosis(
        request: Request
    ):
    raw_body = await request.body()
    decoded_body = raw_body.decode("utf-8", errors="replace")
    print("issue after this : ",decoded_body)
    data = json.loads(decoded_body)
    print("loading done")
    type = (data.get("DiabetesType"))
    additional = (data.get("AdditionalInfo"))
    diagnostic  = diagnosiser(type,additional)
    response = json.dumps(diagnostic)
    return response

