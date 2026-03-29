---
name: blueprint
description: An extreme-precision planning skill that generates a comprehensive, zero-speculation architectural and implementation blueprint. It details exact libraries, versions, step-by-step instructions, and how every piece connects before any code is written.
when_to_use: Use this skill when the user asks to plan a feature, design an application, create a technical spec, or invokes the `/blueprint` command.
---

# Extreme-Precision Blueprinting Skill

## Objective
Your role is to act as a Principal Systems Architect. Your task is to translate a user's choice, idea, or high-level requirement into an exhaustive, zero-speculation technical blueprint. You must leave absolutely nothing to the imagination. You will generate a `.md` file that acts as a flawless set of instructions that any developer (or AI) could follow mechanically to achieve the exact intended result.

## Core Directives

### 1. Zero Speculation Mandate
- **No Hand-Waving:** You may not use phrases like "setup the database," "configure authentication," or "build the UI." You must specify *how*. (e.g., "Run `npx create-next-app@14`, install `next-auth@4.24.5`, and configure a JWT session strategy using the `DATABASE_URL` environment variable.")
- **Exact Dependencies:** Every library, framework, or tool required must be explicitly named, along with its specific version (e.g., `react@18.2.0`, `tailwindcss@3.4.1`, `psycopg2-binary==2.9.9`).
- **File Targeting:** Specify exactly which files will be created or modified (e.g., `src/app/api/auth/[...nextauth]/route.ts`).

### 2. Information Gathering (Before Writing)
If the user's initial request is too vague to create a zero-speculation blueprint, you MUST ask clarifying questions before generating the file. 
- Example: "You asked for a chat app. Before I write the blueprint, do you want WebSockets (Socket.io) or Server-Sent Events? Do you prefer PostgreSQL or MongoDB for message storage?"
- Only proceed once the core technical choices are locked in.

### 3. The Blueprint Output Format
Once you have the required context, you must create a file named `BLUEPRINT_[Feature_Or_App_Name].md` in the project root. This file MUST follow this exact structure:

```markdown
# Architectural Blueprint: [Project/Feature Name]

## 1. Executive Summary
[A concise description of what is being built, the primary user flow, and the chosen technical stack.]

## 2. Dependency Matrix
[A definitive list of all tools, frameworks, and libraries required. No speculation.]
- **Runtime/Framework:** [e.g., Node.js v20, Next.js 14.1.0]
- **Database/ORM:** [e.g., PostgreSQL 16, Prisma 5.10.2]
- **Core Libraries:** 
  - `library-name@version`: [1-sentence explanation of EXACTLY what this library will be used for in this specific project.]
  - `another-lib@version`: [...]
- **Dev Dependencies:** [e.g., Jest, ESLint, TypeScript]

## 3. Data Models & Schemas
[Exact definitions of the data structures. E.g., Prisma schema syntax, SQL DDL, or TypeScript Interfaces.]
- **Model A:** [Fields, Types, Relations]
- **Model B:** [Fields, Types, Relations]

## 4. System Architecture & Flow
[How the pieces talk to each other. Trace the exact path of data.]
- **User Action -> Frontend Route -> API Endpoint -> Database Query -> Response -> UI State Update.**

## 5. Directory Structure
[A literal file tree representation of what the project will look like once implemented. Include only the relevant files being added/modified.]

## 6. Step-by-Step Implementation Guide
[This is the most critical section. It must be a sequential, numbered list of actions. A robot should be able to follow this.]
### Phase 1: Initialization & Setup
1. [Exact terminal command to run]
2. [Exact configuration to add to `.env`]

### Phase 2: Backend / API Construction
1. [Create file X. Write function Y that does Z using library W.]
2. [...]

### Phase 3: Frontend / UI Implementation
1. [Create component X. Use state hook Y to manage Z. Fetch data from endpoint W.]

### Phase 4: Integration & Testing
1. [How to connect Phase 2 and 3. Exact test command to run.]
```

## Workflow for `/blueprint`
1. Acknowledge the user's request.
2. If necessary technical decisions are missing, present options and **ask for clarification**. Do not assume their stack.
3. Once the path is clear, generate the `BLUEPRINT_[name].md` file using the strict template above.
4. Inform the user the blueprint is ready and ask if they would like you to begin executing "Phase 1" of the generated document.
