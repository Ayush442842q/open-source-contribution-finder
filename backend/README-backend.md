# Open Source Contribution Finder Backend
## Project Description
The Open Source Contribution Finder Backend is a RESTful API designed to facilitate open source contributions by connecting contributors with projects that match their skills. The API provides endpoints for registering contributors, retrieving contributor profiles, and creating new projects.

## Tech Stack Used
* Node.js as the backend runtime environment
* Express.js as the web framework
* MongoDB as the database management system
* JSON Web Tokens (JWT) for authentication

## Setup Instructions
To set up the backend API, follow these steps:
1. **Clone the repository**: Run `git clone https://github.com/your-username/open-source-contribution-finder-backend.git` to clone the repository.
2. **Install dependencies**: Run `npm install` to install the required dependencies.
3. **Create a MongoDB database**: Create a new MongoDB database and add a `contributors` and `projects` collection.
4. **Set environment variables**: Set the following environment variables:
	* `MONGO_URI`: The MongoDB connection string.
	* `JWT_SECRET`: The secret key for generating JWT tokens.
	* `PORT`: The port number for the API to listen on.
5. **Start the API**: Run `npm start` to start the API.

## Environment Variables Needed
The following environment variables are required:
* `MONGO_URI`: The MongoDB connection string.
* `JWT_SECRET`: The secret key for generating JWT tokens.
* `PORT`: The port number for the API to listen on.

## API Endpoints Overview
The API provides the following endpoints:
* `POST /api/v1/contributors`: Registers a new contributor.
* `GET /api/v1/contributors/{id}`: Retrieves a contributor's profile.
* `POST /api/v1/projects`: Creates a new project.

## API Endpoints Details
### 1. Register Contributor
* **HTTP Method + Path**: `POST /api/v1/contributors`
* **Description**: Registers a new contributor.
* **Authentication**: Required, JWT Bearer token
* **Request Body**:
```json
{
  "name": "string",
  "email": "string",
  "skills": ["string"]
}
```
* **Success Response**:
	+ HTTP Status Code: 201
	+ JSON Response Schema:
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "skills": ["string"]
}
```
* **Error Responses**:
	+ 400: Invalid request body
	+ 401: Unauthorized
	+ 409: Contributor already exists

### 2. Get Contributor Profile
* **HTTP Method + Path**: `GET /api/v1/contributors/{id}`
* **Description**: Retrieves a contributor's profile.
* **Authentication**: Required, JWT Bearer token
* **Request Body**: None
* **Success Response**:
	+ HTTP Status Code: 200
	+ JSON Response Schema:
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "skills": ["string"]
}
```
* **Error Responses**:
	+ 401: Unauthorized
	+ 404: Contributor not found

### 3. Create Project
* **HTTP Method + Path**: `POST /api/v1/projects`
* **Description**: Creates a new project.
* **Authentication**: Required, JWT Bearer token
* **Request Body**:
```json
{
  "name": "string",
  "description": "string",
  "requiredSkills": ["string"]
}
```
* **Success Response**:
	+ HTTP Status Code: 201
	+ JSON Response Schema:
```json
{
  "id": "integer",
  "name": "string",
  "description": "string",
  "requiredSkills": ["string"]
}
```
* **Error Responses**:
	+ 400: Invalid request body
	+ 401: Unauthorized
	+ 409: Project already exists

## How to Run Locally
To run the API locally, follow these steps:
1. **Clone the repository**: Run `git clone https://github.com/your-username/open-source-contribution-finder-backend.git` to clone the repository.
2. **Install dependencies**: Run `npm install` to install the required dependencies.
3. **Create a MongoDB database**: Create a new MongoDB database and add a `contributors` and `projects` collection.
4. **Set environment variables**: Set the following environment variables:
	* `MONGO_URI`: The MongoDB connection string.
	* `JWT_SECRET`: The secret key for generating JWT tokens.
	* `PORT`: The port number for the API to listen on.
5. **Start the API**: Run `npm start` to start the API.

## How to Run Tests
To run tests, follow these steps:
1. **Install dependencies**: Run `npm install` to install the required dependencies.
2. **Create a test database**: Create a new MongoDB database for testing.
3. **Set environment variables**: Set the following environment variables:
	* `MONGO_URI`: The MongoDB connection string for the test database.
	* `JWT_SECRET`: The secret key for generating JWT tokens.
4. **Run tests**: Run `npm test` to run the tests.