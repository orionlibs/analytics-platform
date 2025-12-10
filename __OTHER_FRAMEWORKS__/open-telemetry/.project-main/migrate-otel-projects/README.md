# migrate-otel-projects

A tool to migrate OpenTelemetry project markdown files to GitHub issues in the .project repository.

## Features

- Parses project markdown files from the OpenTelemetry community repository
- Extracts project metadata (sponsors, timeline, labels, etc.)
- Creates GitHub issues with proper formatting
- Updates GitHub project board fields
- Supports both regex-based and LLM-enhanced extraction

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. (Optional) Configure OpenAI API for enhanced extraction:
   
   **Option A: Using .env file (recommended)**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```
   
   **Option B: Environment variable**
   ```bash
   export OPENAI_API_KEY=sk-your-api-key-here
   ```
   
   **Option C: Using llm CLI**
   ```bash
   uv run llm keys set openai
   # Enter your OpenAI API key when prompted
   ```

   The tool works without LLM but extraction quality may be reduced for complex fields like sponsor parsing and timeline interpretation.

## Usage

### Basic Commands

```bash
# Show help
uv run python -m src --help

# Dry run for a specific project (default mode)
uv run python -m src --project browser-phase-1.md

# Dry run for all projects
uv run python -m src --all

# Save results to JSON
uv run python -m src --all --output-json results.json

# Run without LLM enhancement
uv run python -m src --all --no-llm
```

### Creating Issues (Production Mode)

⚠️ **Warning**: The following commands will create real GitHub issues!

```bash
# Create issue for a single project
uv run python -m src --project browser-phase-1.md --no-dry-run

# Create issues for all projects
uv run python -m src --all --no-dry-run

# Use a specific GitHub token
uv run python -m src --all --no-dry-run --github-token ghp_your_token
```

### Advanced Options

```bash
# Use a different community repo path
uv run python -m src --all --community-path /path/to/community

# Use a different project board ID
uv run python -m src --all --project-id 123
```

## How It Works

1. **Markdown Parsing**: Extracts sections hierarchically from project files
2. **Field Extraction**: Uses regex patterns with optional LLM fallback
3. **Data Validation**: Validates extracted data using Pydantic models
4. **GitHub Integration**: Creates issues and updates project board fields

## Field Mappings

### Issue Fields
- **Title**: Project name from H1 header
- **Body**: 
  - Link to original markdown file
  - Project metadata (status, sponsors, dates)
  - Deliverables summary (if LLM enabled)
  - Extraction warnings (if any)
- **Labels**: From the Labels section in markdown

### Project Board Fields
- **Status**: Based on directory (Active/Inactive/Completed)
- **Start Date**: Extracted from Timeline section
- **Estimate Target Date**: Extracted from Timeline section
- **GC Sponsor**: From Staffing section
- **TC Sponsors**: From Staffing section
- **Sponsorship Level**: Determined from sponsor presence

## Output Example

The tool creates issues with the following format:

```markdown
Project Markdown: https://github.com/open-telemetry/community/blob/main/projects/example.md

## Project Information
- **Status**: Active
- **Project Lead**: @username (Company)
- **GC Sponsors**: @sponsor1 (Company)
- **TC Sponsors**: @sponsor2 (Company), @sponsor3 (Company)
- **Sponsorship Level**: Full
- **Start Date**: 2024-01-01
- **Target Date**: 2024-12-31

## Deliverables Summary
Brief summary of project deliverables...

## Meeting Schedule
Weekly on Thursdays at 10am PST

## Project Board
https://github.com/orgs/open-telemetry/projects/123
```