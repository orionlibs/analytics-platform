# Code coverage report for Go and TypeScript

## Prerequisites

### TypeScript

- yarn
- package.json must contain a script `yarn test:coverage` which generates a report in `"jest --coverage"` style
- runs in node 16.x environment

## Description

**Code coverage comment not posted on PRs from forks.** That information can still be gleaned from the output of the previous step in the run.

This workflow does the following for caller pull requests:

- Checks out caller's PR's code
- Checks out caller's code on main
- Calculates test coverage for each
- Leaves a comment on the PR with a test coverage report with the difference between PR coverage vs main coverage
- When commits are added to the PR, the existing comment should be updated with an up-to-date coverage report

## Releasing

When updates are made to the workflow it needs to be re-released and any parent flows referencing this one will need to be updated.

In order to release:

- Navigate to the [releases](https://github.com/grafana/code-coverage/releases) page of the repo.
- Select `Draft a new release`.
- Create a new tag (increasing the version from the previous value).
- Set the title to the new version.
- Add a description for any changes that have been made since the previous release, ensure the target is `main` and then select `Publish release`.

The following workflows will then need to be updated, create a PR for each repository ensuring that the parent workflow targets the latest code coverage workflow.

### Grafana repo

- [Cloud Data Sources code coverage](https://github.com/grafana/grafana/blob/main/.github/workflows/cloud-data-sources-code-coverage.yml)
- [Observability code coverage](https://github.com/grafana/grafana/blob/main/.github/workflows/ox-code-coverage.yml)

### Datasources

- [ADX code coverage](https://github.com/grafana/azure-data-explorer-datasource/blob/main/.github/workflows/code-coverage.yml)
- [Athena code coverage](https://github.com/grafana/athena-datasource/blob/main/.github/workflows/code_coverage.yml)
- [Redshift code coverage](https://github.com/grafana/redshift-datasource/blob/main/.github/workflows/code-coverage.yml)
- [Timestream code coverage](https://github.com/grafana/timestream-datasource/blob/main/.github/workflows/code_coverage.yml)
- [X-Ray code coverage](https://github.com/grafana/x-ray-datasource/blob/main/../../../../../../.github/workflows/code-coverage.yml)
