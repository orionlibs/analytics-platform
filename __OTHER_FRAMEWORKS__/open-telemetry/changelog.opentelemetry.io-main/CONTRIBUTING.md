# Contributing to OpenTelemetry Changelog

Thank you for your interest in contributing to OpenTelemetry Changelog! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

This project follows the [OpenTelemetry Community Code of Conduct](https://github.com/open-telemetry/community/blob/main/code-of-conduct.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v18 or later)
- npm (comes with Node.js)

### Setting Up Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/changelog.opentelemetry.io.git
   cd changelog.opentelemetry.io
   ```
3. Add the upstream repository as a remote:
   ```bash
   git remote add upstream https://github.com/open-telemetry/changelog.opentelemetry.io.git
   ```
4. Install dependencies:
   ```bash
   npm install
   ```
5. Install Playwright browsers and dependencies for testing:
   ```bash
   npx playwright install --with-deps
   ```

### Development Workflow

1. Create a new branch for your changes:
   ```bash
   git checkout -b your-branch-name
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
3. Make your changes

4. Run linting to ensure code style consistency:
   ```bash
   npm run lint
   ```
5. Run tests:
   ```bash
   npm test
   ```
6. Commit your changes:
   ```bash
   git commit -m "Your descriptive commit message"
   ```
7. Push to your fork:
   ```bash
   git push origin your-branch-name
   ```
8. Create a pull request

## Development Approach

### Test-Driven Development (TDD)

This project uses Test-Driven Development for implementing new features:

1. **Write Tests First**: Begin by writing tests that define the expected behavior
2. **Verify Test Failure**: Run tests to confirm they fail (since the feature isn't implemented yet)
3. **Implement Feature**: Write the code to make the tests pass
4. **Refactor**: Clean up the code while ensuring tests still pass

### Visual Testing

Visual regression testing is critical for this project:

1. **Visual Tests**: Always create visual tests for UI components and layout changes
2. **Multiple Viewports**: Test across different viewport sizes (mobile, tablet, desktop)
3. **Dark Mode**: Test both light and dark modes where applicable

### Testing Tools

- **Playwright**: Used for end-to-end and visual regression testing
- **Test Endpoint**: Use the `/api/test` endpoint in development mode for creating test entries (accessible via the Test Controls button)
- **Test Data Attributes**: Add `data-testid` attributes to elements for reliable test selection

## Project Structure

- `/src/app`: Next.js app router pages and API routes
- `/src/app/api`: API routes for webhook handling and testing
- `/src/components`: React components
- `/src/lib`: Utility functions and shared code
- `/src/types`: TypeScript type definitions
- `/tests`: Playwright tests

## Code Style Guidelines

### TypeScript

- Use strict mode with `strictNullChecks` enabled
- Define proper types for all variables, parameters, and return values
- Avoid using `any` type; use proper TypeScript types instead

### Imports

- Use absolute imports with `@/` prefix for src directory
  ```typescript
  // Good
  import { Component } from "@/components/component";
  
  // Avoid
  import { Component } from "../../components/component";
  ```

### React Components

- Use functional React components with TypeScript types
- Props should be properly typed with interfaces
- Use destructuring for props

### Error Handling

- Use try/catch with specific error types when possible
- Log errors with appropriate context
- Provide user-friendly error messages

### Styling

- Use Tailwind CSS with custom theme extensions
- Follow the existing design system and color schemes
- Ensure components are responsive and accessible

## Special Files and Configurations

### CLAUDE.md

The `CLAUDE.md` file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. It contains:

- Build commands
- Development approach guidelines
- Code style standards
- Project structure information
- Copyright header requirements

This file helps ensure consistent development practices whether using AI assistance or not.

### Copyright Headers

All source files must include the following copyright header:

```
/*
 * Copyright The OpenTelemetry Authors
 * SPDX-License-Identifier: Apache-2.0
 */
```

## Pull Request Guidelines

1. Each PR should address a single issue
2. Reference the issue number in the PR description with "Closes #X"
3. Ensure all linting passes (`npm run lint`)
4. Make sure all copyright headers are present
5. Keep changes focused and minimal
6. Include test coverage for new features or bug fixes
7. Update documentation if necessary
8. All tests must pass including visual regression tests

## Release Process

The OpenTelemetry Changelog website is automatically deployed through Netlify. When changes are merged to the main branch, they will be deployed to production after passing CI checks.

## Getting Help

If you have questions or need help with the contribution process:

- [Open an issue](https://github.com/open-telemetry/changelog.opentelemetry.io/issues/new) with your question
- Ask in the [OpenTelemetry Slack workspace](https://cloud-native.slack.com/archives/C01NFPCV44V) (#otel-ui-ux channel)

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [Apache 2.0 License](./LICENSE).