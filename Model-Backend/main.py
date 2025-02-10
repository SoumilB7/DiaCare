from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import base64
from model import detect_diabetes, aloder
from llama_parse import LlamaParse
from gemini import parse_data, diagnosiser, fallback_diagnosis
from dotenv import load_dotenv
import os

load_dotenv()

llama_api_key = os.getenv("LLAMA_API_KEY")

parser = LlamaParse(
    result_type="markdown",
    premium_mode=True,
    num_workers=8,
    parsing_instruction="This is a medical report",
    verbose=True,
    skip_diagonal_text=False,
    page_separator="\n\n============================================\n\n",
    api_key=llama_api_key,
)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5500",
    "http://localhost:8000",
    "https://yourdomain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)
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
    data = json.loads(decoded_body)
    textual_content = data.get("textual_data") 
    textual_content = base64.b64decode(textual_content)
    filename = data.get("file_name")
    extra_info = {"file_name":filename}
    textual_output = await parser.aload_data(textual_content,extra_info=extra_info)
    data = parse_data(textual_output)
    # print(textual_content)
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
        print("yahana")
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

