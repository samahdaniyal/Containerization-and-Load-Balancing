# Containerization & High-Availability Load Balancing

This project demonstrates the transition from a standalone application to a distributed, containerized system. It focuses on container orchestration using **Docker Compose**, service scaling, and traffic management using **Nginx** as a load balancer.

## Project Overview

The goal of this architecture is to ensure a Python web service can handle increased traffic and maintain high availability. By decoupling the application from the host environment and implementing a load-balanced cluster, the system becomes more resilient and easier to scale.

---

## Technical Stack

* **Backend:** Python Web Service
* **Data Stores:** PostgreSQL (Relational) & Redis (Caching/Key-Value)
* **Orchestration:** Docker & Docker Compose
* **Load Balancing:** Nginx
* **Infrastructure:** Health Checks, Persistent Volumes, and Environment Configuration

---

## Implementation Phases

### 1. Application Containerization
The Python service was containerized using a custom `Dockerfile`, ensuring a consistent runtime environment. This phase included:
* Streamlining dependencies via `requirements.txt`.
* Configuring environment variables for dynamic database discovery.
* Implementing Docker health checks to monitor service readiness.

### 2. Multi-Container Orchestration
Using `docker-compose.yml`, a full-stack environment was defined to coordinate the interaction between the web service and its dependencies:
* **PostgreSQL:** Configured with persistent volumes and automated schema initialization via `init.sql`.
* **Redis:** Integrated for fast data access with dedicated persistence.
* **Networking:** Established a private internal network for secure inter-service communication.



### 3. Scaling & Load Balancing
To handle high request volumes, the web service was scaled horizontally to multiple instances.
* **Service Scaling:** Deployed three identical instances (`web1`, `web2`, `web3`) of the application.
* **Nginx Reverse Proxy:** Configured an Nginx upstream block to distribute incoming traffic across the service cluster.
* **Traffic Distribution:** Implemented Round-Robin load balancing, verified by tracking unique instance IDs per request.



---

## Key Features

| Feature | Implementation |
| :--- | :--- |
| **Persistence** | Docker Volumes ensure PostgreSQL and Redis data survives container restarts. |
| **High Availability** | Nginx automatically routes traffic away from unhealthy containers. |
| **Security** | Only the Nginx port (9999) is exposed to the host; databases remain on a private network. |
| **Automation** | GitHub Actions workflow integrated for automated testing and validation. |

---

## Deployment

To build and launch the entire distributed system:

```bash
# Build and start all services in detached mode
docker-compose up --build -d

# Verify the health of the cluster
docker-compose ps
```

---

Once running, the load-balanced application is accessible at http://localhost:9999
