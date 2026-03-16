##Midterm Project Backend

#Overview

This backend application was developed using Python Flask for the midterm project. It provides a simple web service and a /hello endpoint that attempts to connect to a PostgreSQL database.

#Tech Stack
	•	Python
	•	Flask
	•	PostgreSQL

#Endpoints

GET /

Returns the backend status.

Example response:
{
“success”: true,
“endpoint”: “/”,
“message”: “Backend is running”
}

GET /hello

Returns a JSON response showing whether the backend is running and whether the PostgreSQL connection was successful.

Example response:
{
“success”: false,
“endpoint”: “/hello”,
“message”: “Hello from Flask!”,
“database_status”: “connection failed”,
“error”: “Unable to connect to PostgreSQL with the current configuration.”
}

#Configuration

The application reads database configuration from environment variables:
	•	DB_HOST
	•	DB_PORT
	•	DB_NAME
	•	DB_USER
	•	DB_PASSWORD

Temporary placeholder values were used during local development. The actual PostgreSQL values will be updated after the Azure infrastructure setup is completed.

Running the Application

Install the required packages with pip install -r requirements.txt, create a .env file, and run the project with python app.py.
