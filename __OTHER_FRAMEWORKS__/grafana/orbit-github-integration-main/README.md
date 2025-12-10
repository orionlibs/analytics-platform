# orbit-github-integration
Integration between Orbit and GitHub.

Orbit offers a GitHub integration, but that integration only supports sending data from one (GitHub) _organisation_ to one (Orbit) _workspace_. If your repository, or repositories, fall under an organisation that already uses Orbit's integration, you won't be able to also send data to your workspace. 

If you manage multiple communities under one organisation you run into the same issue.

This integration uses the GitHub API to search GitHub for public repos with whatever attributes you specify, and fetches all the recent events for each one of them.

## Quickstart

Requirements:
- Python >= 3.8
- An Orbit account/workspace
- A GitHub account

To run **orbit-github** locally, you need to create a `.env` file like this one:

```sh
$ cat .env
# Required
ORBIT_WORKSPACE=your-orbit-workspace-id-goes-here
ORBIT_TOKEN=your-orbit-token-goes-here
GITHUB_TOKEN=your-github-token-goes-here
GITHUB_ORG_NAME=the-name-of-your-organization-goes-here
GITHUB_TOKEN=your-github-token-goes-here

# Optional
GITHUB_REPO_NAME_CONTAINS=string-to-match-repositories-with # Default: ""
MAX_EVENT_AGE=10 # Default: 1 (hour)
```

Install the requirements with:
```sh
$ pip install -r requirements.txt
```

Run the script with:
```
$ python orbit-github.py
time=2021-11-22T13:43:55.060610 level=INFO location=orbit-github.py:221:<module> msg="Starting github_orbit" 
time=2021-11-22T13:43:56.278318 level=INFO location=orbit-github.py:233:<module> msg="Processing repo" repository="k6"
time=2021-11-22T13:43:56.774092 level=INFO location=orbit-github.py:114:parse_github_event msg="Parsing event" repository="k6" type="IssueCommentEvent" user="na--"
...
```
Profit!

