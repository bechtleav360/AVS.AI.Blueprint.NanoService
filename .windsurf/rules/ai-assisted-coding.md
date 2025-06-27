---
trigger: manual
---

# AI-Assisted Coding Guidelines – Python + FastAPI Microservice

This document defines how to use AI tools responsibly when coding microservices with FastAPI.

## 1. Role of AI

- AI tools are allowed for code generation, refactoring, and review support.
- AI output must be treated as a draft — final code must be verified by the developer.
- Developers are fully responsible for the correctness, clarity, and security of all code.

## 2. Using AI for Code Generation

- Write clear function signatures, docstrings, and comments before using AI completions.
- Break down tasks into focused prompts to improve relevance and quality.
- Avoid using AI for entire modules or files without manual review.

## 3. Acceptance Criteria for AI Code

- Must comply with all architecture, testing, and documentation rules.
- Must be readable, testable, and maintainable.
- Must avoid tight coupling, redundant abstractions, or hidden side effects.

## 4. Documentation and Comments

- Use AI to help generate docstrings, but ensure they are accurate and complete.
- Annotate complex or non-obvious logic for both human readers and future AI use.

## 5. Security and Confidentiality

- Do not use AI tools to process or expose credentials, tokens, production logs, or sensitive internal data.
- Prompts should be limited to general structure or logic, not proprietary implementations.

## 6. AI in Code Review

- AI may assist in review comments or suggestions, but human judgment remains primary.
- Do not auto-accept AI review suggestions without evaluation.

## 7. Developer Responsibility

- All AI-assisted code must meet the same standards as manually written code.
- Do not bypass reviews, testing, or architecture checks based on AI output.
