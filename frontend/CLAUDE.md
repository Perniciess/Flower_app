# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
bun dev          # Development server
bun run build    # Production build
bun start        # Production server
bun run lint     # Lint
bun run lint:fix # Lint with auto-fix
```

## Architecture

Next.js 16 app with React 19, TypeScript, and Tailwind CSS v4. Uses **Feature-Sliced Design (FSD)** architecture enforced by `eslint-plugin-boundaries`.

### FSD Layer Hierarchy (imports only allowed downward)

```
app → pages → widgets → features → entities → shared
```

- `src/app/` — providers, global styles, theme configuration
- `src/pages/` — page-level components composed from widgets
- `src/widgets/` — self-contained UI sections (header, footer, hero)
- `src/features/` — user interactions and business features
- `src/entities/` — domain models and their UI representations
- `src/shared/` — utilities (`cn` via clsx + tailwind-merge), reusable UI components (shadcn/ui pattern with CVA)

Next.js app router lives in `/app/` (root), FSD layers live in `/src/`.

### Component Conventions

- Each FSD slice uses barrel exports (`index.ts`)
- Widget structure: `src/widgets/{name}/ui/{Name}.tsx` + `src/widgets/{name}/config/index.ts`
- shadcn/ui components go to `src/shared/ui/components/`
- Path alias: `@/*` → `./src/*`

## Code Style

- 4-space indent, double quotes, semicolons (antfu ESLint config)
- Type imports use `import { type Foo }` (inline style)
- Unused variables prefixed with `_`
- Montserrat font with cyrillic subset
- Russian is allowed in content strings
