# Allstar Security Policy Enforcement

## Overview

This repository outlines the security policy enforcement for the OpenTelemetry organization, using the [Allstar GitHub App](https://github.com/ossf/allstar). Allstar helps enforce security best practices by automatically checking and ensuring our repositories comply with our established policies.

## Configured Allstar Actions

Allstar is configured to take the following action upon detecting a policy violation within any repository in the OpenTelemetry organization:
- **issue**: For each violation, Allstar will create a GitHub issue within the affected repository. If the issue remains open and unchanged for more than 36 hours, it will be pinged with a comment every 36 hours. The issue will be automatically closed by Allstar once the violation is resolved.

## Enforced Policies

The following Allstar security policies are actively enforced across the OpenTelemetry organization's repositories:

### Repository Administrators Policy
- Ensures that each repository has assigned administrators.
- Maintains that teams are designated as administrators.

### GitHub Actions Policy
- Monitors GitHub Actions workflows to ensure they adhere to our security rules.
- Checks for the use of static security scans within the workflows.

### Binary Artifacts Policy
- Prevents binary artifacts from being committed to the repositories.
- Ensures that source code is human-readable and free from hidden vulnerabilities.

### Branch Protection Policy
- Verifies that the main branches (e.g., `main`) have branch protection rules enforced, such as required reviews, status checks, and more.

### SECURITY.md Policy
- Checks that a security policy file named `SECURITY.md` is present and properly filled out in each repository or at the organisation. This file should detail how to report security vulnerabilities.
