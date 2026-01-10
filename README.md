# Cloud-Based Student Management App

This project is a simple cloud-based web application built to understand
how real-world frontend and backend systems communicate over HTTP in a cloud
environment.

The focus of this project is on cloud architecture and deployment rather than
complex application logic.



## Architecture Overview

The application follows a basic cloud-native separation of concerns:

Browswer -> S3(Static Frontend) -> HTTP Requests -> EC2(Flask Backend) 

- **Frontend**: Static HTML and JavaScript hosted on Amazon S3 using Static Website Hosting
- **Backend**: REST API built using Flask and deployed on Amazon EC2
- **Communication**: Frontend communicates with backend APIs over HTTP




## Features

- Add student records using HTTP POST requests
- Retrieve student records using HTTP GET requests
- Simple frontend interface to interact with backend APIs



## Technologies Used

- Python
- Flask
- HTML & JavaScript
- Amazon S3 (Static Website Hosting)
- Amazon EC2
- AWS Security Groups
- HTTP / REST APIs



## Key Learnings

- Understanding frontend and backend separation in cloud architectures
- Hosting static content using Amazon S3
- Deploying backend services on EC2
- Handling cross-origin requests using CORS(Cross Origin Resource Sharing)
- Configuring ports and security groups for public access over the internet
- Debugging real-world cloud networking issues



## Running the Backend Locally

bash terminal-
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

## Project Status
- This project will be extended to include:
- Application Load Balancer
- Removal of hardcoded backend endpoints
- HTTPS support


