# Customer Support Ticket API

A lightweight FastAPI application for managing customer support tickets.

## Features
- Create, retrieve, and list support tickets.
- Input validation using Pydantic models.
- Interactive API documentation powered by Swagger UI.

---

## Setup & Local Installation

Follow these steps to set up and run the application locally on your machine:

1.Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate

2.Install Dependencies
pip install -r requirements.txt

3.Running the Application
"uvicorn main:app --reload" in terminal
The server will start running at http://127.0.0.1:8000.

Interactive API Documentation
Once the server is running, you can test all endpoints directly using Swagger UI:

Swagger UI: http://127.0.0.1:8000/docs
