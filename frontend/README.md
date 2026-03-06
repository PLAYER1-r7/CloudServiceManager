# Frontend (Phase 3)

Frontend application for Cloud Service Manager Phase 3 issues:

- `#22` Frontend foundation setup
- `#23` Service list UI (paging/filter/sort)

## Stack

- React + TypeScript + Vite
- React Router

## Setup

```bash
cd frontend
npm install
cp .env.example .env
```

## Environment Variables

`VITE_API_BASE_URL` is used for API access.

Example:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Run

```bash
cd frontend
npm run dev
```

Open: `http://localhost:5173`

## Quality Checks

```bash
cd frontend
npm run build
npm run lint
```

## Testing

```bash
cd frontend
npm run test
npm run test:e2e:install
npm run test:e2e
```

- Unit/UI tests: Vitest + Testing Library + MSW
- E2E tests: Playwright (Chromium)

## Current Pages

- `/` Home
- `/services` Service table with loading/error/empty states, pagination, filters, and sorting
- `/monitoring` Dashboard cards (running/stopped/region/provider) with manual and auto refresh
