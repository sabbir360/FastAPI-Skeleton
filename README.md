
# FastAPI Swagger/OpenAPI Skeleton
A minimal FastAPI project template with built-in Swagger (OpenAPI) documentation. It includes a sample endpoint adhering to OpenAPI standards and supports Docker deployment. The template also provides PostgreSQL integration with ORM support, allowing easy database switching between MySQL, Oracle, and SQL Server.

## Previews
### Swagger
![Swagger](./preview_images/swagger.png?raw=true)
### Redoc
![Redoc](./preview_images/redoc.png?raw=true)  
### OpenAPI
![OpenAPI](./preview_images/open_api.png?raw=true)

## Deployment Instructions
### Configuration
Create a `config.yaml` from `config.yaml.sample` and fill the required fields.
Create a Postgresql database and fill the database details in config.yaml. (It can be changed to any other database by defining in `yaml` and `db.py` file)
Create a JWT secret key and fill it in config.yaml.
Create APP Specific Access key and provide. (It can be replaced by database based access key management. Contact for more details.)

**Important: Make sure to keep your config.yaml file secure and do not share it. And Give access to _test_ before giving production app and keys**

### Local Development
#### Running the Server
```bash
uvicorn main:app --reload
```
- Follow instruction to browser server endpoint.
- For Swagger `http://127.0.0.1:8000/docs`
- For Redoc `http://127.0.0.1:8000/redoc`
- For OpenAPI `http://127.0.0.1:8000/openapi.json`
- For Using with other service `http://127.0.0.1:8000/`

---

### Docker Deployment

#### Build Docker Image
To package the application as a Docker container:
```bash
docker build -t api-service .
```

#### Run the Container
To start the service using Docker:
```bash
docker run -d -p 8000:8000 --name api-service  api-service 
```

#### Stop the Container
To stop the running container:
```bash
docker stop api-service 
```

#### Remove the Container
To remove the container:
```bash
docker rm api-service 
```

#### Docker Compose (Optional)
If you want to manage the deployment with Docker Compose, create a `docker-compose.yml` file like this:
```yaml
services:
  app:
    image: api-service 
    build:
      context: .
    ports:
      - "8000:8000"
```

Run the application using Docker Compose:
```bash
docker-compose up -d
```

Stop the application:
```bash
docker-compose down
```

---

### Notes
- Ensure Docker is installed and running on your system.
- The application will be accessible at `http://localhost:8000` when using the default configurations.


### 🚀 Need Further Assistance?

I bring 10+ years of experience in AWS, Cloud Architecture, and backend development with Python, Golang or Frameworks like FastAPI, Django, and Flask.

📌 Expertise in: RAG, LLM, and AI Agents

If you need help, consulting, or want to collaborate, feel free to reach out!

📩 [Github](https://github.com/sabbir360)

