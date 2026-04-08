# Python + FastAPI + JWT Auth + RAG + LLM + Groq

A REST API that serves:

- FastAPI

- JWT Auth

- a RAG Application using a LLP by Groq

- Swagger / OpenAPI

Last updated:

- 08-04-2026

Python Version:

- 3.12

# Get startet

- Clone the repository from my GitHub 

- Create a virtual environment by Powershell or VS Code:

"python -m venv <name_of_venv>"

- Go to the virtual environment's directory and activate it:

"Scripts/activate"

- Install the requirements:

"pip3 install -r requirements.txt"

# Swagger documentation / Testing the API

FastAPI provides the Swagger documentation of the API where you can perform CRUD operations

To access the documentation, we must run uvicorn:

"uvicorn main:app --reload"

If everything works fine, the FastAPI and Swagger documentation is now available at: 

`http://127.0.0.1:8000/docs`

- Use the Swagger for Login by the Credentials to get the JWT Access Token for Auth

# JWT Authentication

- The token will expire after 60 minutes for testing and demo. Then a 401 status will happen

# Deployment to Vercel

- Take a look at the file "vercel.json"

- Create a Project at Vercel from your repository at GitHub with the code of this FastAPI

- Create the envirement variables from .env at Vercel with Groq API Key and the Credentials for Auth

- Make a commit to your GitHub

- Go to Vercel and check that the build and deployment happened and your site is in Production

Happy use of FastAPI :-)

