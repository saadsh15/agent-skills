---
name: dockerise
description: A precision engineering skill for containerizing any project. It deeply analyzes the tech stack, dependencies, and architecture to generate production-ready Dockerfiles for every component and a cohesive `docker-compose.yml` file.
when_to_use: Use this skill when the user asks to containerize a project, write Dockerfiles, set up Docker Compose, or invokes the `/dockerise` command.
---

# Precision Containerization & Orchestration Skill

## Objective
Your goal is to act as an elite DevOps Engineer. Your task is to analyze an entire project or specific components with absolute precision—understanding exactly what each part does, how it builds, what dependencies it requires, and how it communicates. You will then generate highly optimized, production-ready `Dockerfile`s for each service and a comprehensive `docker-compose.yml` to orchestrate them perfectly.

## Core Directives

### 1. Pinpoint Precision & Architectural Discovery
Before writing a single line of Docker code, you MUST deeply analyze the workspace:
- **Identify Services:** Find all distinct applications (e.g., frontend in `web/`, backend in `api/`, worker processes in `workers/`).
- **Analyze Stacks:** Read package managers (`package.json`, `requirements.txt`, `go.mod`, `pom.xml`) to determine the exact language versions, build commands, and runtime requirements.
- **Discover Dependencies:** Identify required external services (e.g., PostgreSQL, Redis, MongoDB, RabbitMQ) by looking at environment variables, configuration files, or connection strings.
- **Determine Ports & Volumes:** Map out exactly which ports need to be exposed and which directories need persistent volumes (e.g., database storage, uploaded media).

### 2. Crafting the Perfect Dockerfile
Every `Dockerfile` you generate must adhere to production-grade best practices:
- **Multi-Stage Builds:** Always use multi-stage builds for compiled languages (Go, Rust, Java, C++) and Node.js applications (building the frontend/backend, then copying only the built artifacts to a lean runner image).
- **Minimal Base Images:** Default to `alpine`, `distroless`, or slim variants of official images to minimize attack surface and image size.
- **Caching Optimization:** Order your commands strategically. Copy dependency files (e.g., `package.json`, `requirements.txt`) and install dependencies *before* copying the rest of the source code to maximize Docker layer caching.
- **Non-Root Execution:** NEVER run applications as the `root` user in the final container. Always create a dedicated user and switch to it (`USER appuser`).
- **Environment Parity:** Define essential environment variables (`ENV`) and expose the correct ports (`EXPOSE`).

### 3. Comprehensive Orchestration (Docker Compose)
The `docker-compose.yml` file is the heart of the project. It must be robust and cohesive:
- **Service Definitions:** Define every custom application and required third-party dependency (e.g., databases, caches).
- **Network Isolation:** Create custom Docker networks if services need logical separation (e.g., a `frontend-net` and a `backend-net`).
- **Healthchecks:** Implement robust `healthcheck` blocks for databases and critical APIs to ensure dependent services wait for them to be truly ready (using `depends_on` with `condition: service_healthy`).
- **Persistent Volumes:** Define named volumes for databases to ensure data survives container restarts.
- **Environment Variables:** Use an `.env` file structure or explicit `environment` blocks for configuration. Pass sensitive data securely.

### 4. Execution Workflow for `/dockerise`
1. **Analyze:** Scan the project structure and read relevant configuration files to build a mental map of the architecture.
2. **Confirm (If Ambiguous):** If it's unclear what a specific service does or what database version is required, ASK the user before proceeding. Do not guess.
3. **Generate Dockerfiles:** Write a highly optimized `Dockerfile` in the root of each respective service directory.
4. **Generate Compose:** Write the `docker-compose.yml` file in the project root.
5. **Create Supporting Files:** Generate a `.dockerignore` file for each service (ignoring `node_modules`, `.git`, `.env`, etc.) to keep build contexts small.
6. **Documentation:** Create a brief `DOCKER_README.md` explaining how to build, run (`docker-compose up -d`), and stop the environment, including any prerequisites (like filling out an `.env` file).

## Example Scenario

**User Request:** "/dockerise my project"
*Your Action:*
1. You notice a Node.js API (`backend/`), a React app (`frontend/`), and a `.env.example` referencing PostgreSQL and Redis.
2. You create a multi-stage `Dockerfile` in `frontend/` that builds the React app and serves it via Nginx.
3. You create a multi-stage `Dockerfile` in `backend/` that installs Node modules, switches to a non-root user, and runs the server.
4. You write `.dockerignore` files for both.
5. You create `docker-compose.yml` at the root, defining `api`, `web`, `postgres` (with a persistent volume and healthcheck), and `redis`.
6. You set the `api` service to `depends_on` the `postgres` healthcheck.
7. You provide the user with the exact commands to start the cluster.
