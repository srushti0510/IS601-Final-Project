# Final Project – FastAPI User Management System

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [Features Implemented](#features-implemented)
- [New Feature](#new-feature)
- [Closed Issues (Bug Fixes)](#closed-issues-bug-fixes)
- [Docker Image](#docker-image)
- [Test Coverage Report](#test-coverage-report)
- [Reflection](#reflection)


## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/srushti0510/IS601-Final-Project.git
cd IS601-Final-Project
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Install required packages

```bash
pip install -r requirements.txt
```
### 4. Run Alembic migrations

```bash
alembic upgrade head
```
### 5. Start services using Docker Compose

```bash
docker compose up --build
```

### 6. Run tests with coverage

```bash
docker compose exec fastapi pytest --cov=app --cov-report=term-missing
```

## Features Implemented

-  **User registration and login** with secure password hashing using `bcrypt`
-  **JWT-based authentication** and role-based authorization (admin, user, manager)
-  **Email verification system** via SMTP, with mocked email testing support
-  **Profile picture uploads** stored in MinIO using secure pre-signed URLs
-  **Complete CRUD operations** for managing users
-  **Pagination and HATEOAS links** for user listings with consistent schema responses
-  **Added 10 new test cases** covering critical logic and edge scenarios  **
-  **85+ test coverage** with `pytest`, `pytest-asyncio`, and `pytest-cov`
-  **Alembic migrations** for managing schema versions cleanly
-  **Dockerized architecture** for FastAPI + PostgreSQL + MinIO
-  **CI/CD vulnerability scanning** using Trivy in GitHub Actions pipeline

## New Feature

## Profile Picture Upload with MinIO

This feature allows users to upload and store their profile pictures securely, enhancing the personalization of user accounts. The implementation leverages **MinIO**, an open-source object storage system compatible with AWS S3 APIs.

### Key Features:
- **API Endpoint for Profile Picture Upload**: Users can upload their profile pictures via a dedicated API endpoint.
- **Storage in MinIO**: Uploaded images are securely stored in MinIO, ensuring reliable, scalable storage.
- **User Profile Update**: The user profile is updated to include a URL linking to the uploaded profile picture stored in MinIO.

### Enhancements:
- **Image Resizing & Optimization**: Images can be resized and optimized to improve loading times and maintain consistent image sizes across user profiles.
- **Image Format Validation**: Restrict file uploads to specific image formats (e.g., JPEG, PNG) and limit image size to ensure performance.


### Setup Instructions:

1. **MinIO Setup**: Ensure that MinIO is properly configured and running in your environment for image storage. You can follow this guide for setup: [Setting up Object Storage with Minio with Docker](https://kodekloud.com/community/t/setting-up-object-storage-with-minio-with-docker/336624).
2. **Database Update**: Update the user profile model and database schema to include a field for storing the profile picture URL.
3. **API Endpoint Implementation**: Create a new API route to handle file uploads, store the files in MinIO, and update the user profile with the image URL.
4. **Testing**: Write tests to validate the functionality, including uploading an image and retrieving it from the user profile.

This feature improves user experience by allowing account customization through profile pictures and also ensures secure, scalable storage with MinIO.

## Closed Issues (Bug Fixes)

Here are the 5 issues I identified, fixed, tested, and merged:

1. **Bug #1:** [Duplicate login route](<https://github.com/srushti0510/IS601-Final-Project/issues/1>)  
   Fixed duplicate `/login/` route to resolve Swagger confusion and unexpected behavior.

2. **Bug #2:** [Duplicate fields in UserListResponse example](<https://github.com/srushti0510/IS601-Final-Project/issues/2>) <br>
   Removed duplicate fields in `UserListResponse` example to ensure correct schema rendering. 

3. **Bug #3:** [Role Field Type Inconsistency](<https://github.com/srushti0510/IS601-Final-Project/issues/3>) <br>
    Fixed inconsistency in `role` field type in `UserUpdate` and `UserBase` schemas.  

4. **Bug #4:** [UserResponse is missing fields present in route returns](<https://github.com/srushti0510/IS601-Final-Project/issues/4>) <br>
   Added missing fields (`created_at`, `updated_at`, etc.) to `UserResponse` schema.  

5. **Bug #5:** [Password Validation is Missing During User Creation](<https://github.com/srushti0510/IS601-Final-Project/issues/5>) <br>
   Added password validation to ensure strength requirements during user creation. 

## Docker Image

You can find the deployed Docker image here:

 **DockerHub**: [srushti5/final-project](https://hub.docker.com/repository/docker/srushti5/final-project/general)

To pull the image, run:

```bash
docker pull srushti5/final-project
```

## Test Coverage Report
To check test coverage, run:

```bash

docker compose exec fastapi pytest --cov=app --cov-report=term-missing
```
As of the final commit, test coverage is: 89%

## Reflection

This project provided valuable hands-on experience in building a production-level backend system using FastAPI. I was tasked with implementing several key features, such as user registration, authentication, file uploads, and secure token handling, all backed by a robust testing strategy. One of the most important lessons I learned was the significance of schema validation, test coverage, and proper API documentation.

A standout feature I worked on was integrating **Profile Picture Upload with MinIO**, which added a practical and highly relevant component to the user profile management system. It allowed me to explore object storage, file handling, and image management using MinIO — a new area for me that extended my understanding of cloud-native solutions.

The bug-fixing process taught me about the intricacies of backend development, especially around handling edge cases, such as password validation and inconsistent schema definitions. It also highlighted the importance of consistent and reliable API responses.

On the DevOps side, I gained exposure to CI/CD pipelines, Dockerization, and vulnerability scanning with Trivy, making the application more secure and deployable. Building out a strong CI/CD pipeline with automated builds, tests, and vulnerability scans was a crucial part of this project.

Through the integration of **MinIO**, Docker, and GitHub Actions, I further refined my skills in creating maintainable, secure, and efficient backend systems. The project also emphasized the importance of writing meaningful tests and the value of collaboration, especially when addressing production-level issues. The 91% test coverage we achieved reflects the thorough testing and attention to detail applied throughout the project.

In conclusion, this project wasn’t just about delivering features but also about ensuring the software is robust, secure, and scalable. I feel more confident in handling real-world challenges in backend development, particularly in integrating various technologies to create efficient and reliable systems.



