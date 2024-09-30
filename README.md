# Project Setup Documentation

## Environment Setup

### Create a `.env` File
First, set up a `.env` file with the path to your database. If you're using SQLite, you can define the `DATABASE_URL` as follows:

```bash
DATABASE_URL=sqlite:///path_to_your_database.db
SECRET_KEY=your_secret_key
```

Then generate a secret key using the python secrets module

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

This generates a secret key that you will need to replace your_secret_key in the .env file with. So your .env file will look as follows:

```bash
DATABASE_URL=sqlite:///path_to_your_database.db
SECRET_KEY=generated_key
```

## Deployment 

### Local Deployment

#### 1. Start the Backend Server 
1. First, install the necessary backend dependencies in terminal:
```
WORKDIR /backend
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
```
To start the backend server locally, use unvicorn with the following command:

```bash
 uvicorn backend.app.main:app --reload 
```

#### 2. Start the Frontend

1. First, install the necessary frontend packages:
```
npm install
```

2. Then, build or start the frontend:
    - To build:
    ```
    npm run build 
    ```
    - To start in development mode:
    ``` 
    npm start 
    ```

### Container Deployment 

#### 1. Build Docker Images

To deploy in a container, first configure the necessary parameters for your environment. Then, build the Docker images using the following command:

```
docker compose build 
```

This command will package both the frontend and backend folders into a container.

#### 2. Run the Docker Containers
After building, you can easily run the containers to deploy both the frontend and backend services.

