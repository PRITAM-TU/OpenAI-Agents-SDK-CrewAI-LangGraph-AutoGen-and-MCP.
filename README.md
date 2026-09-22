# Master AI Agents in 30 Days

A hands-on learning repository for building 8 real-world AI agent projects using:

- OpenAI Agents SDK
- CrewAI
- LangGraph
- AutoGen
- Model Context Protocol (MCP)

This project is designed to help you learn how to build autonomous, collaborative, and production-oriented AI agents step by step.

## Overview

This repository serves as a practical workspace for exploring modern AI agent frameworks and patterns. Each project focuses on a different use case and demonstrates how agentic systems can be used for automation, reasoning, tool-calling, and multi-agent collaboration.

The learning path is structured around:

- Understanding agent architecture
- Designing task-oriented workflows
- Connecting agents to tools and APIs
- Building multi-agent collaboration patterns
- Integrating memory, orchestration, and external context
- Shipping useful real-world AI-powered applications

## Learning Goals

By the end of this course/repository, you should be able to:

- Build AI agents with the OpenAI Agents SDK
- Orchestrate multi-agent workflows with CrewAI
- Design stateful agent graphs with LangGraph
- Create conversational and collaborative agents with AutoGen
- Connect agents to tools and data sources via MCP
- Deploy practical AI agent applications in real-world scenarios

## Repository Structure

This workspace is currently being used as a learning project directory and will evolve as each project is added.

```text
.
├── README.md
├── project-01/
├── project-02/
├── project-03/
├── project-04/
├── project-05/
├── project-06/
├── project-07/
├── project-08/
└── .git/
```

## Suggested 8 Project Roadmap

1. AI Research Assistant
2. Task Automation Agent
3. Customer Support Agent
4. Sales or Lead Qualification Agent
5. Coding Assistant / Dev Workflow Agent
6. Multi-Agent Team Coordinator
7. Workflow Orchestration with LangGraph
8. MCP-powered Tool-Integrated Agent System

## Prerequisites

Before starting, make sure you have:

- Python 3.10+
- A package manager such as pip or uv
- Access to an OpenAI API key (or another compatible model provider)
- Git installed
- A code editor such as VS Code

## Setup

Create a virtual environment and install the dependencies for each project as needed:

```bash
python -m venv .venv
source .venv/bin/activate   # On macOS/Linux
.venv\Scripts\activate      # On Windows
pip install -U pip
```

Then install project-specific dependencies inside each project folder:

```bash
pip install -r requirements.txt
```

## Environment Variables

Many projects will require API keys or configuration values. A common pattern is:

```bash
export OPENAI_API_KEY="your-api-key"
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-api-key"
```

## Recommended Workflow

- Start with one framework at a time
- Build small prototypes before scaling to complex agents
- Test tool calling and agent reasoning in isolation
- Add memory and orchestration only when the base behavior works
- Document each project clearly with usage instructions and examples

## Notes

This repository is intended for learning, experimentation, and practical implementation. You can use it as:

- A personal study repo
- A course project tracker
- A portfolio of AI agent projects
- A sandbox for prototyping agent-based applications

## License

This repository is for educational use. Add an explicit license file if you plan to share it publicly or distribute it commercially.

## Future Enhancements

- Add individual project READMEs
- Include architecture diagrams
- Add sample prompts and outputs
- Add deployment examples
- Add tests and evaluation scripts

## Contributing

If you are working through this repository, consider keeping each project in its own folder with a dedicated README, requirements file, and example usage notes.

---

Built for learning, experimentation, and practical AI agent development.
