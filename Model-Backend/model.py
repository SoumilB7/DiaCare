import joblib
import torch
import torch.nn as nn
import numpy as np
from llama_parse import LlamaParse
from dotenv import load_dotenv
import os

load_dotenv()

llama_api_key = os.getenv("LLAMA_API_KEY")

parser = LlamaParse(
    result_type="markdown",
    premium_mode=True,
    num_workers=9,
    parsing_instruction="",
    verbose=True,
    skip_diagonal_text=False,
    page_separator="\n\n============================================\n\n",
    api_key=llama_api_key,
)

async def aloder(textual_content,info):
    print("hh",textual_content[:10])
    textual_output = await parser.aload_data(textual_content,extra_info=info)
    print("heree",textual_output)
    return textual_output


loaded_model = nn.Sequential(
    nn.Linear(8, 16),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(16, 8),
    nn.ReLU(),
    nn.Linear(8, 3),  
    nn.Softmax(dim=1)  
)

loaded_model.load_state_dict(torch.load("diabetes_ann_model1.pth"))
loaded_model.eval() 

scaler = joblib.load("scaler1.pkl")

def detect_diabetes(vals):
    vals = np.array([vals]) 
    vals_scaled = scaler.transform(vals) 
    vals_tensor = torch.tensor(vals_scaled, dtype=torch.float32)
    with torch.no_grad():
        prediction_prob = loaded_model(vals_tensor)  
        predicted_class = torch.argmax(prediction_prob, dim=1).item()
    labels = {0: "No Diabetes", 1: "Type 1 Diabetes", 2: "Type 2 Diabetes"}
    return labels[predicted_class]