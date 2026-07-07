---
name: understand
description: A comprehensive guide for analyzing, mapping, and deeply understanding an unfamiliar codebase or specific piece of code.
when_to_use: Use this skill when the user asks to explain code, map a project's architecture, understand what a file does, or invokes the `/understand` command.
---

# Codebase Understanding & Analysis Skill

## Objective
Your goal is to provide a precise, exhaustive, and structured explanation of how a codebase or specific piece of code works. You must not rely on vague guesses or superficial reading. You are required to act as a senior architect performing a deep-dive code review. 

## General Rules & Constraints
1. **Never Guess:** If a dependency, import, or function call is not defined in the current file, use search tools (like `grep` or `glob`) to find its definition before explaining it.
2. **Be Exhaustive:** Do not stop at the surface level. Trace the execution flow from the entry point down to the core logic.
3. **Cite Your Sources:** Always mention the exact file paths and function names you are analyzing.
4. **Identify the Unknowns:** If a piece of code relies on external APIs, missing environment variables, or unavailable microservices, explicitly state what is missing and how it affects the system.

---

## Execution Methodology

When tasked with understanding a codebase, follow these distinct phases in order:

### Phase 1: High-Level Architectural Mapping
Before reading individual functions, understand the system's shape.
1. **Identify the Tech Stack:** Look at package managers (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`). Identify the language, framework, and key dependencies.
2. **Locate Entry Points:** Find where the execution begins.
   - *Node/JS:* `index.js`, `main.ts`, `app.js`
   - *Python:* `main.py`, `app.py`, `__main__.py`
   - *Go/Rust:* `main.go`, `src/main.rs`
   - *Java/C#:* Files containing `public static void main`
3. **Map the Directory Structure:** Identify patterns (e.g., MVC, Clean Architecture, Feature-sliced design). What does `src/`, `lib/`, `components/`, or `controllers/` contain?

### Phase 2: Contextual Deep-Dive (By Codebase Type)
Apply specific analysis strategies based on the type of project you are looking at:

#### A. Backend / API Servers
- **Routing & Controllers:** Find where HTTP endpoints or gRPC methods are defined. Trace a request from the router to the controller.
- **Business Logic (Services):** Identify the core service layer where the actual work happens, separate from the transport layer.
- **Data Access Layer (Models/Repositories):** Look for ORM definitions (Prisma, SQLAlchemy, Hibernate) or raw SQL queries. Understand the database schema and relationships.
- **Middleware/Interceptors:** Check for authentication, logging, or error handling that wraps requests.

#### B. Frontend / UI Applications (React, Vue, Angular, etc.)
- **Routing:** Identify the navigation structure (e.g., `react-router`, Next.js `pages/` or `app/` router).
- **State Management:** Find how global state is handled (Redux, Zustand, Vuex, Context API).
- **Component Hierarchy:** Pick a core page and map its component tree. Distinguish between "Smart" (container) components and "Dumb" (presentational) components.
- **Data Fetching:** Look for API calls (`fetch`, `axios`, React Query, Apollo GraphQL) and understand how data enters the UI.

#### C. CLI Tools & Scripts
- **Argument Parsing:** Find how user input is captured (e.g., `argparse`, `Commander.js`, `clap`).
- **Execution Flow:** Trace the linear steps from input parsing -> validation -> core execution -> output formatting.
- **Side Effects:** Identify what the script modifies (File system operations, network calls, environment variables).

#### D. Libraries & SDKs
- **Public API Surface:** Identify what is exported for users to consume (e.g., `index.ts` exports, `__init__.py`).
- **Internal Core:** Understand the hidden abstractions that the user doesn't see.
- **Configuration:** How does a user instantiate or configure the library?

### Phase 3: Control & Data Flow Tracing
When analyzing a specific feature or bug:
1. **Input:** What data enters the function/system? (Types, schemas, payloads).
2. **Transformations:** How is the data mutated or validated? Trace the exact sequence of function calls.
3. **External Calls:** Does it talk to a database, third-party API, or message queue?
4. **Output/Side Effects:** What is returned to the user, and what state was changed in the system?

---

## Output Formatting Requirements

When presenting your final explanation to the user, use the following structure:

### 1. Executive Summary
A 2-3 sentence high-level overview of what the code does and its primary purpose.

### 2. Architecture & Tech Stack (If applicable)
A brief list of the languages, frameworks, and architectural patterns in use.

### 3. Step-by-Step Execution Flow
A numbered list explaining how data moves through the code. 
*Example:*
1. Request hits `/api/users` in `routes/user.ts`.
2. Middleware `auth.ts` validates the JWT.
3. Controller `UserController.get` calls `UserService.find`.
4. `UserService` queries the PostgreSQL DB via Prisma.

### 4. Key Components / File Breakdown
A bulleted list of the most critical files or functions and their specific responsibilities.

### 5. Edge Cases & Potential Risks
Highlight any areas where the code might fail, lack validation, or have performance bottlenecks (e.g., N+1 query problems, missing try/catch blocks, unhandled promise rejections).

---

## Example Scenarios

**Scenario 1: User says "/understand src/auth/login.ts"**
*Your Action:* 
1. Read `src/auth/login.ts`. 
2. If it calls `verifyPassword(hash)` from `utils/crypto.ts`, you MUST read `utils/crypto.ts` before answering.
3. Provide the Executive Summary, trace the flow from the HTTP request to the DB query, and highlight if rate-limiting is missing (Potential Risk).

**Scenario 2: User says "/understand how the payment processing works"**
*Your Action:*
1. Search the codebase for `payment`, `stripe`, or `checkout` using grep/glob.
2. Find the entry point (e.g., `PaymentController`).
3. Trace the flow to `StripeService` and the `WebhookHandler`.
4. Explain the full lifecycle: User clicks pay -> Intent created -> Webhook received -> DB updated.
