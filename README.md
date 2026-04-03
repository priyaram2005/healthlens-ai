# HealthLens AI

AI-powered system that converts complex medical reports into simple, understandable health insights.

## Problem Statement

Medical reports are often complex and difficult for non-medical individuals to understand. Patients struggle to interpret values, assess health risks, and take appropriate actions without professional guidance.

## Solution

HealthLens AI is an intelligent system that transforms medical reports into simple, actionable insights.

It allows users to upload reports (PDF/text), automatically extracts key health parameters, analyzes them using AI, and presents:
- Easy-to-understand visualizations
- Risk level (Low / Moderate / High)
- AI-generated health score
- Personalized recommendations in plain language

This bridges the gap between medical data and user understanding, enabling smarter and faster health decisions.

## Features

- Upload PDF medical reports
- Extract health parameters automatically
- Risk prediction (Low / Moderate / High)
- Visual dashboard with charts & gauge meter
- Smart health recommendations


## Tech Stack

- Frontend: Streamlit
- Backend: Flask
- ML Model: Random Forest Classifier
- Visualization: Plotly


## Project Structure

Codecure AI 2026/
│
├── backend/
│   ├── app.py
│   ├── train_model.py
│   ├── model.pkl
│
├── frontend/
│   ├── dashboard.py
│
├── Reports/
│   ├── Report1.pdf
│   ├── Report2.pdf
│   ├── Report3.pdf
│
├── requirements.txt
├── README.md

## How to Run

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run backend
cd backend
python app.py

### 3. Run frontend
cd frontend
streamlit run dashboard.py

## How it Works

1. User uploads report
2. Text is extracted from PDF
3. Parameters are detected
4. ML model predicts risk
5. Dashboard displays insights


## ⚠️ Note

This is an AI prototype and not a medical diagnosis tool.
