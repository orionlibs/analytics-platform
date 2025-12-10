# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linting with ESLint
- `npm test` - Run Playwright tests
- `npm run test:ui` - Run tests with Playwright UI
- `npm run test:debug` - Run tests in debug mode
- `npm run test:visual` - Run visual regression tests
- Testing: Use `/api/test` endpoint in development mode only (accessible via Test Controls button)

## Development Approach
- Use Test-Driven Development (TDD) when implementing new features
- Write tests first, ensure they fail, then implement the feature
- Use Playwright for visual regression and integration testing
- Add data-testid attributes to elements for reliable test selection
- For API changes, use the test endpoint or create simple test scripts
- Verify changes work in both development and production builds

## Code Style Guidelines
- TypeScript: Strict mode with strictNullChecks enabled
- ESLint: Extends Next.js core-web-vitals and TypeScript configs
- Imports: Use absolute imports with `@/` prefix for src directory
- Components: Use functional React components with TypeScript types
- Error handling: Use try/catch with specific error types when possible
- Naming: PascalCase for components, camelCase for functions/variables
- Styling: Use Tailwind CSS with custom theme extensions
- State management: Use React hooks (useState, useEffect)

## Copyright Headers
All source files must include the following copyright header:
```
/*
 * Copyright The OpenTelemetry Authors
 * SPDX-License-Identifier: Apache-2.0
 */
```

## Project Structure
- `/src/app` - Next.js app router pages and API routes
- `/src/components` - React components
- `/src/lib` - Utility functions and shared code
- `/src/types` - TypeScript type definitions

## PR Guidelines
- Each PR should address a single issue
- Reference the issue number in the PR description with "Closes #X"
- All linting must pass (`npm run lint`)
- Make sure all copyright headers are present
- Keep changes focused and minimal
