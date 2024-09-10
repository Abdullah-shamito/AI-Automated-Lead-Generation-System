from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import torch.nn as nn
import numpy as np

# Define the SimpleNN model class (ensure it's defined the same way as during training)
class SimpleNN(nn.Module):
    def __init__(self, input_size, num_classes):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, num_classes)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Define your FastAPI app
app = FastAPI()

# Initialize your model
model = SimpleNN(input_size=128, num_classes=10)  # Adjust input size and num_classes as per your trained model

# Define input data model
class LeadData(BaseModel):
    employees: int
    revenue: float
    founded_year: int
    keywords: str  # Assuming keywords are passed as a string

@app.on_event("startup")
async def load_model_weights():
    # Load model weights during startup
    model.load_state_dict(torch.load('lead_scoring_model.pth'))
    model.eval()  # Set the model to evaluation mode
    print("Model weights loaded successfully on startup.")

@app.get("/")
async def root():
    return {"message": "Lead Scoring Model is ready"}

@app.post("/predict")
async def predict_lead(data: LeadData):
    # Preprocess input data
    # Example: Numerical data preprocessing
    numerical_features = np.array([data.employees, data.revenue, data.founded_year], dtype=np.float32)
    numerical_features = torch.tensor(numerical_features).unsqueeze(0)  # Add batch dimension

    # Example: Keyword processing (simple encoding, assuming SentenceTransformer or other methods were used)
    # This part should match how your model was trained to handle keywords
    keywords_embedding = torch.rand(1, 125)  # Dummy embedding; replace with actual encoding logic

    # Combine numerical and keyword features
    all_features = torch.cat((numerical_features, keywords_embedding), dim=1)

    # Ensure the input size matches the model's expected input size
    if all_features.shape[1] != 128:
        raise HTTPException(status_code=400, detail="Input feature size mismatch with model's expected input size.")

    # Perform prediction
    with torch.no_grad():
        outputs = model(all_features)
        _, predicted = torch.max(outputs, 1)  # Get the index of the highest score

    return {"predicted_cluster": int(predicted.item())}
