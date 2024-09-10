# AI-Automated-Lead-Generation-System

Prototype of an AI-powered lead generation system designed to identify, qualify, and nurture potential leads for TAIPPA's services in the Dubai/UAE market.

## Project Overview

This project implements an AI-driven lead scoring and clustering system using a combination of data cleaning, natural language processing, and clustering algorithms. The system identifies and qualifies potential leads based on their likelihood to convert, leveraging advanced machine learning techniques.

### Key Components

- **Data Cleaning and Manipulation:**
  - The initial dataset is loaded and cleaned by removing irrelevant columns and handling missing values.
  - Key features such as 'Annual Revenue', 'Company Size', and textual descriptions are retained for further processing.

- **Natural Language Processing with LangChain and OpenAI:**
  - Text features like 'Short Description' and 'Keywords' are processed using LangChain and OpenAI models.
  - The system generates embeddings from textual data to represent the semantic content in a format suitable for machine learning models.

- **Clustering Model:**
  - A clustering model is developed using PyTorch and GaussianMixture.
  - The model categorizes leads into clusters based on their features, aiding in targeted marketing strategies.
  - PyTorch is utilized for feature extraction, possibly through a neural network, followed by clustering using GaussianMixture.

## Model Training and Evaluation

- The clustering model is trained using features derived from both numerical and embedded text data.
- Evaluation metrics and validation procedures are implemented to ensure the model segments leads accurately.

## How to Use

### Requirements

- Python 3.x
- PyTorch
- Scikit-learn
- Pandas
- LangChain
- OpenAI API Access

### Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Abdullah-shamito/AI-Automated-Lead-Generation-System
   cd AI-Automated-Lead-Generation-System
2. **Install Dependencies**:

  ```bash

    pip install -r requirements.txt

3. **Load the Data**:
        Ensure your data file is in the correct directory. The model expects a CSV file with the required columns as shown in the sample data.

4. **Run the Notebook**:
        Open the Jupyter notebook AI Model Development.ipynb and execute the cells sequentially to clean the data, generate embeddings, and build the clustering model.

5. **Model Deployment**
FastAPI Deployment

    Use FastAPI to create a web server for deploying the model.

Endpoints

    Root Endpoint:
        URL: /
        Method: GET
        Response: Basic health check message indicating the model is ready.

    Predict Endpoint:
        URL: /predict
        Method: POST
        Input: JSON containing lead data (e.g., employees, revenue, founded year, keywords).
        Output: Cluster prediction indicating the likelihood of a lead to convert.

**Docker Deployment**

Create a Dockerfile:

```dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME LeadScoringApp

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

Build and Run the Docker Container:

```bash

    # Build the Docker image
    docker build -t lead-scoring-app .

    # Run the Docker container
    docker run -p 80:80 lead-scoring-app

Kubernetes Deployment

    Create a Deployment Manifest (deployment.yaml):

    yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: lead-scoring-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: lead-scoring-app
  template:
    metadata:
      labels:
        app: lead-scoring-app
    spec:
      containers:
      - name: lead-scoring-app
        image: lead-scoring-app:latest
        ports:
        - containerPort: 80


**Deploy on Kubernetes**:

```bash

    # Apply the deployment and service
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml

    # Check the status of your deployment
    kubectl get deployments

    # Get the external IP of your service
    kubectl get services

