
# Audit Log Microservice

## Overview

The Audit Log Microservice is a pivotal component designed to chronicle the diverse array of activities within a microservices ecosystem. Its primary function is to capture and retain an immutable record of critical system events that detail the lifecycle of customer interactions and system processes. This includes, but is not limited to, the creation of new customer accounts, associations of customer records with external identities, billing transactions, and the deactivation of accounts.

In the dynamic landscape of microservices, where new services can be deployed and retired rapidly, the Audit Log Microservice stands as a central repository, offering a temporal snapshot of system states at any given point. Its open-ended architecture ensures adaptability, allowing for the seamless introduction of new event types as the system evolves.

By serving as an authoritative source of historical data, the service empowers stakeholders to trace sequences of events, debug system anomalies, maintain regulatory compliance, and derive analytical insights. Its robust API endpoints enable other services within the architecture to report events, ensuring that every significant action is captured and available for future query and analysis.

The Audit Log Microservice is not just a passive observer but an active participant in the governance of a microservices architecture, providing a foundational layer for accountability, transparency, and system intelligence.

## How to interact with the Public Service

The Audit Log Microservice is actively running and accessible for public interaction. The service is hosted on a robust AWS EC2 instance and is reachable at the URL: http://3.145.12.117/events .

To interact with the microservice, I recommend using Postman, a versatile platform for API development and testing. Postman facilitates both the sending of requests to the microservice and the interpretation of responses. It provides an intuitive, user-friendly interface that simplifies the construction of requests, setting of headers, and viewing of response data, headers, and status codes.



## API EndPoints

- GET '/events' : Fetch the list of events.

- POST '/events' : Create a new event.

#### Command to GET entire Event List : 

```http
  curl -X GET http://3.145.12.117/events
```

#### Command to POST an Event :

```http
  curl -X POST http://3.145.12.117/events \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "1",
    "event_type": "account_deleted",
    "timestamp": "2024-01-01T00:00:00Z",
    "src_service": "user_service",
    "invariant_data": {
      "message": "User deleted account",
      "priority": 2,
      "trace": "trace_id_789"
    },
    "app_data": {
      "username": "jondoe",
      "email": "jondoe@example.com"
    }
  }'

```

| Key | Value     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Content-Type`      | `application/json` | **Required** Header Key Value |



## File Structure

Below is the file structure of the Audit Log Microservice repository:

- `Dockerfile` - Contains the instructions to build the Docker image for the service.
- `Procfile` - Used to declare what commands are run by the application’s dynos on the Heroku platform. (Required if hosting on Heroku)
- `app.py` - The main Flask application script that defines API endpoints and logic.
- `app_database.py` - Handles the database operations like inserting and retrieving log events.
- `docker-compose.yml` - Defines services, networks, and volumes for a Docker application.
- `flask-app-ec2-key.pem` - The private key file for SSH access to the AWS EC2 instance. (Not uploaded actual key files for security reasons.)
- `requirements.txt` - Specifies the Python dependencies that need to be installed.


## Methodology

- #### [app.py]()

    #### Objective 
    This file serves as the main entry point for the Flask application. It defines the API endpoints for creating and retrieving audit log events and interacts with the MongoDB database through the app_database module.

    - POST /events
        
        Purpose: Records a new event in the audit log.
        
        Request Body: Expects a JSON payload containing the event details, including user_id, event_type, timestamp, src_service, invariant_data, and app_data.

        Response: Returns a JSON object with a message indicating the success or failure of the operation and, in case of success, the ID of the recorded event.

    - GET /events

        Purpose: Retrieves a paginated list of events from the audit log.

        Query Parameters: Optional parameters include user_id (to filter events by user ID), page (for pagination), and per_page (number of events per page).

        Response: Returns a JSON object containing the list of events, along with pagination details such as the total number of events, the current page, the number of events per page, and the total number of pages.

    #### Error Handling
        
    Both endpoints are equipped with try-except blocks to handle exceptions gracefully. In case of an error, the API responds with a JSON object containing an error message and a corresponding HTTP status code (e.g., 500 for internal server errors).
    
- #### [app_database.py]()

    #### Objective 
    This file contains functions for interacting with the MongoDB database. It handles the creation and retrieval of audit log events stored in the logger collection of the activity_db database.

    #### Functions :
    - create_log

        Purpose: Inserts a new event document into the logger collection.
        
        Parameters: Receives event details such as user_id, event_type, timestamp, src_service, invariant_data, app_data, and any additional keyword arguments (**kwargs).
       
        Implementation: Constructs an event document with the provided parameters and any additional fields from **kwargs. Attempts to insert the document into the collection and returns the inserted document's ID and a success flag.

        Base Arguments: The function defines a set of base arguments which are expected in every API request. These are user_id, event_type, timestamp, src_service, invariant_data, and app_data. These fields are considered compulsory for the function to execute correctly.

        Handling Additional Data with **kwargs: The **kwargs (keyword arguments) parameter in the function allows it to accept an arbitrary number of additional keyword arguments. This means that any extra JSON fields sent in the request that are not explicitly listed as parameters in the function will be captured in kwargs.

        Updating Event Dictionary: The event.update(kwargs) call takes all the additional key-value pairs provided in kwargs and adds them to the event dictionary. This means that any additional data passed in the API request will be stored alongside the compulsory fields in the MongoDB document.

        Flexibility and Extendibility: This design allows the API to be flexible and extendible. Clients can send additional data that may be required for future features or logging purposes without modifying the existing API contract.

    - read_logs

        Purpose: Retrieves a paginated list of all events from the logger collection.

        Parameters: limit (number of events to return) and skip (number of events to skip for pagination).

        Implementation: Performs a find operation on the collection with optional sorting by timestamp in descending order. Also calculates the total number of documents for pagination purposes. Returns a list of event documents and the total document count.

    - read_logs_by_user_id

        Purpose: Retrieves a paginated list of events filtered by a specific user ID.

        Parameters: user_id (ID of the user to filter by), limit, and skip.

        Implementation: Similar to read_logs, but adds a filter to only include documents with the matching user_id. Returns a list of filtered event documents and the total count of matching documents.

    #### Error Handling
    
    Each function is wrapped in a try-except block to catch and handle any exceptions that may occur during database operations. In case of an error, an appropriate message is printed, and a failure indication is returned.
## Dockerization 

Dockerization provides a convenient and consistent way to deploy the Audit Log Microservice application. By packaging the application and its dependencies into a Docker container, it can be easily run across different environments, ensuring consistent behavior. The process involves creating a Dockerfile, building the Docker image, running the container, and accessing the application. 

Process :

- Creating the Dockerfile

The first step in dockerizing the application is creating a Dockerfile. This file contains a set of instructions for building the Docker image, which includes the application and its dependencies. The Dockerfile for the Audit Log Microservice is as follows:

    - Start with a base image of Python 3.9 Slim, which provides a lightweight environment with Python pre-installed.
    - Set the working directory to /app inside the container.
    - Copy all files from the current directory (including the application code and requirements.txt) into the container.
    - Use the requirements.txt file to install the necessary Python dependencies using pip.
    - Expose port 5001, which is the port the Flask application will run on.
    - Set the entry point to python, and the default command to run app.py, which starts the Flask application.

- Building the Docker Image

With the Dockerfile in place, the next step is to build the Docker image. This is done using the docker build command, which reads the Dockerfile and creates an image based on the instructions. The image is tagged with the name audit-log-app for easy reference.

- Running the Docker Container
Once the image is built, a Docker container can be run from this image. The container is run in detached mode, meaning it runs in the background. Port 5001 of the container is mapped to port 5001 on the host machine, allowing access to the Flask application. The container is named audit-log-container for easy identification.

[Reference Link : Dockerize](https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/)


## Hosting on AWS EC2 

For the purpose of making my Audit Log Microservice accessible via a public URL, I chose to host the service as a Docker image on AWS EC2 and run it as a container. I opted for AWS EC2 for this basic proof-of-concept task due to its ease of use, scalability, and the ability to integrate seamlessly with other AWS services if needed in the future. Additionally, AWS provides a reliable and secure platform, which is essential for hosting a service that may handle sensitive data.

#### Setting Up the EC2 Instance :

- Launch an EC2 instance: Choose an Amazon Linux 2 AMI and an instance type that suits your needs.
- Connect to the EC2 instance: Use SSH to connect to your instance. For example:

        ssh -i path/to/your-key.pem ec2-user@your-instance-public-ip


#### Installing Docker on EC2 :

- Update the package repository

        sudo yum update -y
    
- Install Docker

        sudo amazon-linux-extras install docker
    
- Start the Docker service

        sudo service docker start

- Add the ec2-user to the Docker group (to run Docker commands without sudo)

        sudo usermod -a -G docker ec2-user

#### Deploying the Application :

- Create a directory for the application:

        mkdir auditlog
        cd auditlog

- Transfer the application files to the EC2 instance using scp (replace your-key.pem and your-instance-public-ip with your actual key and instance IP)

        scp -i path/to/your-key.pem Dockerfile docker-compose.yml app.py app_database.py requirements.txt ec2-user@your-instance-public-ip:/home/ec2-user/auditlog

- Build the Docker image

        sudo docker build -t ec2-flask:v2.0 -f Dockerfile .

- Run the Docker container (mapping port 80 of the instance to port 5001 of the container)

        sudo docker run -d -p 80:5001 ec2-flask:v2.0


[Reference Link : Host Docker on AWS EC2](https://www.youtube.com/watch?v=qNIniDftAcU)

