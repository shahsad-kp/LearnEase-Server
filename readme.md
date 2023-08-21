![Logo](https://i.ibb.co/ngwjLL5/Unsastitled-2.png)


# LearnEase - Backend

### 🚀 About LearnEase
_LearnEase is an innovative virtual classroom application that takes video conferencing to the next level! With a focus on creating an engaging and interactive learning environment, LearnEase offers a plethora of exciting features designed to enrich the teaching and learning experience._

## Features

- Group Video: Engage in real-time video chats.
- Live Whiteboard: Foster creativity and dynamic lessons.
- Screenshare: Seamless sharing of multimedia content.
- Live Chat: Encourage interactive discussions.
- Document Sharing: Access study materials effortlessly.
- Teaching Activities: Make learning enjoyable and impactful.
- Grades: Track student progress efficiently.
- JWT Auth: Secure and protected virtual environment.


## Installation and Setup

#### 1 Prerequisites:
- Make sure you have Python installed on your system. You can download and install Python from the official website: https://www.python.org/
- Install Postgres on your system. You can download and install Postgres from the official website: https://www.postgresql.org/

#### 2 Clone the Repository:

- Open your terminal or command prompt.
- Change the current working directory to where you want to store the LearnEase backend project.
- Run the following command to clone the repository:
```bash
git clone https://github.com/shahsad-kp/LearnEase-Server.git
```

#### 3 Create a Virtual Environment:
- Change the current working directory to the project folder (e.g., LearnEase-Server).
- Create a virtual environment using Python's venv or virtualenv:
```bash
python -m venv venv
```
- Activate the virtual environment:
    - On Windows:
    ```bash
    venv\Scripts\activate
    ```
    - On macOS and Linux:
    ```bash
    source venv/bin/activate
    ```
#### 4 Install Backend Dependencies:
- With the virtual environment activated, run the following command to install the backend dependencies:
```bash
pip install -r requirements.txt
```

#### 5 Environment Variables:
d- Refer [environment variables](https://github.com/shahsad-kp/LearnEase-Server#environment-variables) for setting up the required environment variables for the LearnEase backend.


#### 6 Apply Database Migrations:
- Run the following command to apply the database migrations:
```bash
python manage.py migrate
```

#### 7 Start the Daphne Server:
- Run the following command to start the Daphne server with Channels:
```bash
daphne learn_ease_backend.asgi:application
```
- The backend application will be accessible at http://localhost:8000 (or another available port if 8000 is already in use).

That's it! You're all set to run the backend of LearnEase with Django, Daphne, Channels, and Postgres. Integrate this backend with the frontend to create a complete virtual classroom experience. Happy teaching and learning! 🚀📚

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file and store it settings folder:

`SECRET_KEY`

`DATABASE_NAME`

`DATABASE_USERNAME`

`DATABASE_PASSWORD`

`DATABASE_HOST`

`DATABASE_PORT`

`CORS_WHITELIST`

`ALLOWED_HOSTS`

`DEBUG`


## Feedback

If you have any feedback, please reach me at shahsadkpklr@gmail.com or connect me at [LinkedIn](https://www.linkedin.com/in/shahsad-kp/)


## Support
Show your support by 🌟 the project!!
