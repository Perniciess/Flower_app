# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Next.js 16 frontend for a flower shop ("KupiBuket74"), written in TypeScript with React 19. Uses Bun as the runtime/package manager. The UI is in Russian.

## Commands

```bash
bun install              # Install dependencies
bun run dev              # Dev server (localhost:3000)
bun run build            # Production build
bun run start            # Production server
bun run lint             # ESLint check
bun run lint:fix         # ESLint autofix
```

## Architecture: Feature Sliced Design (FSD)

The `src/` directory follows FSD with strict layer boundaries enforced by `eslint-plugin-boundaries`. Layers are imported top-down only — a lower layer cannot import from a higher one.

```
src/
├── app/         → Providers (React Query), layouts, global styles
├── pages/       → Page-level containers, re-exported via app/ route files
├── widgets/     → Large standalone UI blocks (Header, Footer, Hero)
├── features/    → User-facing functionality slices (auth forms, hooks)
├── entities/    → Business domain entities (session/user queries)
└── shared/      → API client, stores, types, config, UI primitives
```

**Import rules:** `app > pages > widgets > features > entities > shared`. Each layer's segments must be imported through `index.ts` barrel exports, except `shared/` which allows deep imports.

### How Next.js App Router connects to FSD

Route files in `/app` are thin re-exports that point to `src/pages/` components. Route groups `(client)`, `(admin)`, `auth` map to corresponding layout components in `src/app/layouts/`. Layouts in `src/app/layouts/` wrap children without adding extra UI (passthrough pattern) except for the root layout which applies font, metadata, and Providers.

### Path Aliases

`@/app/*`, `@/pages/*`, `@/widgets/*`, `@/features/*`, `@/entities/*`, `@/shared/*` — all resolve to `src/<layer>/*`.

## API Layer (`src/shared/api/`)

- **`base.ts`** — Fetch wrapper: auto-JSON, FormData support, injects `Authorization: Bearer` from Zustand store, credentials included
- **`client.ts`** — Two instances: `api` (basic) and `apiAuth` (auto-retries on 401 via `/auth/refresh`, logs out on refresh failure)
- **`interceptors.ts`** — CSRF token injection from cookies for non-GET requests
- **`query-client.ts`** — React Query client (5min staleTime, 1 retry)

Custom `ApiError` class carries `status`, `statusText`, and `data`.

## State Management

- **Zustand** (`src/shared/stores/auth.store.ts`) — Holds `accessToken` only. Used by the API layer for auth headers.
- **React Query** — Server state. Session user fetched via `useSessionQuery()` in `src/entities/session/`.

## Styling

- Tailwind CSS v4 with OKLCH custom properties in `globals.css`
- Brand color: `#326964` (teal)
- Component variants via `class-variance-authority` (CVA)
- `cn()` utility (`clsx` + `tailwind-merge`) in `shared/lib/utils.ts`
- Font: Montserrat (Google Fonts), weights 300–700, Latin + Cyrillic
- Shared UI components based on Radix UI primitives (Button, Input, Label, Field, Separator)

## Code Style

- ESLint flat config based on `@antfu/eslint-config`: 4-space indent, double quotes, semicolons required
- `import type` enforced for type-only imports (`verbatimModuleSyntax` in tsconfig)
- Strict TypeScript: `noUncheckedIndexedAccess`, `noImplicitOverride`, `isolatedModules`
- Husky for pre-commit hooks

## Environment

Required `.env` variable: `NEXT_PUBLIC_API_URL` (e.g., `http://127.0.0.1:8000/api/v1`)

Backend API runs on port 8000. See root `CLAUDE.md` for backend/bot setup and the full auth flow (registration → Telegram bot phone verification → JWT tokens).
