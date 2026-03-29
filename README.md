cat README_SKILLS.md 
# 🛠️ Claude Engineering Suite

A collection of high-precision, specialized **Claude Skills** designed to automate the entire software development lifecycle—from architectural planning to production-grade deployment.

These skills are designed for use with **Claude Code** and live in the `~/.claude/skills/` directory. They transform Claude into a multi-role engineering team, ranging from a Principal Architect to a Ruthless Auditor.

---

## 🏗️ 1. Planning & Execution
| Command | Role | Description |
| :--- | :--- | :--- |
| `/blueprint` | **Principal Architect** | Generates a zero-speculation `BLUEPRINT_*.md` with exact library versions, schemas, and file structures. |
| `/build` | **Lead Engineer** | Systematically implements blueprints in manageable, validated batches. Always asks for permission before moving to the next phase. |

## 🔍 2. Analysis & Understanding
| Command | Role | Description |
| :--- | :--- | :--- |
| `/understand` | **System Mapper** | Performs high-level architectural mapping and deep-dives into unfamiliar codebases without guessing or "hallucinating." |
| `/explain-code` | **Code Tutor** | Provides detailed, step-by-step walkthroughs of specific logic, algorithms, and their business purpose. |

## 🛠️ 3. Troubleshooting & Quality
| Command | Role | Description |
| :--- | :--- | :--- |
| `/debug` | **Aggressive Debugger** | Pinpoints root causes with 95%+ accuracy. Interrogates state, asks for logs, and validates hypotheses before proposing fixes. |
| `/critique` | **Ruthless Auditor** | Performs a brutal architectural audit, logging unvarnished feedback on security, tech debt, and "smells" into a dedicated file. |
| `/feedback-loop` | **Senior Developer** | Reviews the `/critique` output and presents the user with 2-3 actionable architectural options with pros/cons. |

## 🚀 4. Performance Optimization
| Command | Role | Description |
| :--- | :--- | :--- |
| `/check-optimize` | **Perf Auditor** | Audits the app for bottlenecks, writes benchmark tests, and logs tasks into a dedicated `optimization_tasks/` directory. |
| `/optimize_performance` | **Backend Specialist** | Executes backend optimizations (N+1 queries, indexing, Big-O reduction) to push the server to its absolute limit. |
| `/optimize_frontend` | **UI/UX Specialist** | Applies scientific aesthetic principles (8pt grid, Golden Ratio) and optimizes perceived performance and "feel." |

## 📦 5. DevOps & Deployment
| Command | Role | Description |
| :--- | :--- | :--- |
| `/dockerise` | **DevOps Engineer** | Generates highly optimized, multi-stage `Dockerfile`s and cohesive `docker-compose.yml` orchestrations for any stack. |

---

## ⚙️ Installation

To use these skills in your local environment:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-skills-repo.git
    ```

2.  **Symlink or Copy to your Claude directory:**
    ```bash
    mkdir -p ~/.claude/skills
    cp -r ./skills/* ~/.claude/skills/
    ```

3.  **Reload Claude Code:**
    Once the files are in `~/.claude/skills/[skill_name]/SKILL.md`, Claude will automatically recognize the new slash commands.

---

## 🧠 Philosophy: The Zero-Speculation Mandate

Unlike general AI prompts, these skills are built on the **Zero-Speculation Mandate**:
- **Prove it:** Skills like `/debug` and `/check-optimize` are forbidden from guessing. They must write tests or use logs to prove a state.
- **Batching:** Implementation skills like `/build` work in manageable chunks to ensure the context remains clean and the code remains high-quality.
- **Scientific Aesthetics:** UI optimizations use mathematical design rules rather than "subjective opinions."

---

*“Build fast, optimize deep, and deploy with precision.”*
