# Project 3: Containerization and Load Balancing

In this project, you will learn about containerization, container orchestration, and load balancing by creating a distributed system using Docker, Docker Compose, and Nginx. You will containerize a Python web service and set up a load-balanced environment with multiple service instances.

## Project Objectives
- Containerize a Python web application
- Set up a multi-container environment using Docker Compose
- Configure and implement load balancing using Nginx
- Work with persistent data using volumes
- Implement health checks for container orchestration
- Configure environment variables for container configuration

## Prerequisites
- Docker and Docker Compose installed on your system
- Basic understanding of Python and web services
- Basic understanding of SQL and Redis
- Git for version control

## Project Steps

### 1. Understanding the Codebase
- Review the provided `service.py` which contains a Python web service
- Understand the service dependencies (Redis and PostgreSQL)
- Review `init.sql` which contains the database initialization script

### 2. Containerize the Web Service (2 points)
1. Create a `Dockerfile` for the Python web service that:
   - Uses an appropriate Python base image
   - Sets up the working directory
   - Installs dependencies from requirements.txt
   - Copies the service code
   - Specifies the command to run the service

Note: The docker image will not work yet, unless you provide the database and redis configuration

### 3. Set Up Docker Compose (4 points)
1. Create a `docker-compose.yml` file that defines:
   - PostgreSQL service with:
     - Appropriate image and version
     - Environment variables for database credentials
     - Volume for data persistence
     - Volume mount for init.sql
     - Health check configuration
   - Redis service with:
     - Appropriate image and version
     - Volume for data persistence
     - Health check configuration
   - Web service with:
     - Build configuration using your Dockerfile
     - Environment variables for Redis and PostgreSQL connections
     - Dependency configuration on Redis and PostgreSQL
     - Port exposure on port 9999 for the web service

Test that web service is now working by opening http://localhost:9999 in a web browser.

### 4. Scale the Web Service (1.5 points)
1. Modify your Docker Compose configuration to create three instances of your web service (web1, web2, web3)
2. Ensure all instances:
   - Share the same configuration
   - Have appropriate environment variables
   - Depend on Redis and PostgreSQL services
   - Do not expose any ports to the host

### 5. Implement Load Balancing (2.5 points)
1. Create an `nginx.conf` file that:
   - Defines an upstream block for backend servers
   - Configures proper load balancing across web1, web2, and web3
   - Sets up proper proxy headers
2. Add Nginx service to Docker Compose:
   - Use the official Nginx image
   - Mount your nginx.conf
   - Configure proper port mapping
   - Set up dependencies on web services
   - Expose the Nginx port to the host on port 9999

Test that load balancing is now working by opening http://localhost:9999 in a web browser. (It should show three different instance Ids)

### 6. Testing and Validation
1. Build and start your services:
   ```bash
   docker-compose up --build
   ```
2. Test the load balancing:
   - Make multiple requests to your service
   - Verify requests are distributed across instances
   - Check logs to confirm load balancing
3. Test persistence:
   - Create data through your service
   - Restart containers
   - Verify data persists

### Environment Variables
Your web service should be configured with the following environment variables:
- `REDIS_HOST`: Redis server hostname
- `DB_HOST`: PostgreSQL server hostname
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASS`: Database password

### Success Criteria
- All containers start successfully and pass health checks
- Web service can connect to both Redis and PostgreSQL
- Load balancing works across all three web service instances
- Data persists across container restarts
- GitHub Actions workflow passes all tests

### Submission
- Push your code to the provided GitHub repository
- Ensure all configuration files are properly created
- Verify GitHub Actions workflow passes
- Include any additional documentation in this README if needed
