<!--
Sync Impact Report:
- This is a NEW file (not a version update)
- Version: 2.0.0 (initial creation for Phase 2)
- Relationship: Supersedes constitution.md (v1.0.0) for Phase 2 development
- Phase 1 constitution preserved at: .specify/memory/constitution.md (v1.0.0)
- Templates requiring updates: ✅ plan-template.md (no changes needed), ✅ spec-template.md (no changes needed), ✅ tasks-template.md (no changes needed), ✅ phr-template.prompt.md (no changes needed)
- Follow-up TODOs: None
-->

# The Evolution of Todo Constitution (Phase 2)

## 1. Core Mandates

### Architecture
The project MUST be a monorepo with a `frontend/` (Next.js) and `backend/` (FastAPI) structure.

### Workflow
All development MUST follow Spec-Driven Development (SDD). No code is to be written without a corresponding Spec, Plan, and Task list.

### Agent Role
The AI agent is the implementer; the human is the architect. The agent MUST update Prompt History Records (PHR) after every significant interaction.

## 2. Technology Stack (Non-Negotiable)

- **Frontend**: Next.js 15+ (App Router), Tailwind CSS, Lucide React (icons), and Shadcn UI.
- **Backend**: Python 3.13, FastAPI, and SQLModel (ORM).
- **Database**: Neon Serverless PostgreSQL.
- **Authentication**: Better Auth with JWT-based communication between frontend and backend.

## 3. Development Principles

### Type Safety
Strict TypeScript for frontend; Type hints and Pydantic models for backend.

### State Management
Use modern React hooks (useState/useContext) or Server Actions where appropriate.

### Database Integrity
No task IDs SHALL be reused after deletion. All database schema changes MUST be documented in an ADR.

### Security
API endpoints MUST be protected. The backend MUST validate the Better Auth session/token before performing any CRUD operations.

## 4. UI/UX Standards

### Responsiveness
The web application MUST be mobile-friendly.

### Feedback
Every user action (Add, Delete, Toggle) MUST provide immediate UI feedback (e.g., loading states or optimistic updates).

### Theme
Support for Light and Dark modes using `next-themes`.

## 5. Definition of Done

- Feature is specified in `specs/`.
- Technical plan is approved in `plan.md`.
- Implementation matches the Task list exactly.
- PHR and ADR entries are updated.

## Governance

All PRs and reviews MUST verify compliance with these principles. Complex deviations MUST be documented and approved before implementation. Use the templates in `.specify/templates/` for all new artifacts.

**Version**: 2.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01

---

## Historical Reference: Phase 1 Constitution

The original Phase 1 constitution is preserved at `.specify/memory/constitution.md` for reference. Key differences between Phase 1 and Phase 2:

| Aspect | Phase 1 (v1.0.0) | Phase 2 (v2.0.0) |
|--------|------------------|------------------|
| Architecture | Python CLI | Next.js/FastAPI Monorepo |
| Storage | In-memory | Neon PostgreSQL |
| Authentication | None | Better Auth + JWT |
| UI | Terminal | Web (Tailwind + Shadcn) |
