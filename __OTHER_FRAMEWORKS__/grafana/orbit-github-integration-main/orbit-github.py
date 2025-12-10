from github import Github
import datetime
import requests
from requests.adapters import HTTPAdapter
from decouple import config
from requests.packages.urllib3.util.retry import Retry
from logfmt_logger import getLogger

ORBIT_WORKSPACE = config("ORBIT_WORKSPACE", default="")
ORBIT_TOKEN = config("ORBIT_TOKEN", default="")
GITHUB_ORG_NAME = config("GITHUB_ORG_NAME", default="")
GITHUB_REPO_NAME_CONTAINS = config("GITHUB_REPO_NAME_CONTAINS", default="")
GITHUB_TOKEN = config("GITHUB_TOKEN", default="")
MAX_EVENT_AGE = config("MAX_EVENT_AGE", default=1, cast=int)

logger = getLogger("orbit_github")


class Orbit:
    def __init__(self, workspace, token):
        self.workspace = workspace
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

    def create_or_update_member(self, member, tags):
        url = f"https://app.orbit.love/api/v1/{self.workspace}/members"

        payload = {
            "member": {
                "bio": member.bio,
                "name": member.name,
                "github": member.login,
                "tags_to_add": tags,
                "twitter": member.twitter_username,
                "email": member.email,
                "url": member.blog,
                "company": member.company,
                "avatar_url": member.avatar_url,
                "location": member.location,
            }
        }

        retry_strategy = Retry(
            total=10,
            status_forcelist=[429],
            method_whitelist=["POST"],
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        response = requests.request("POST", url, json=payload, headers=self.headers)

        if response.status_code == 201 or response.status_code == 200:
            logger.info(
                "Created/updated member", extra={"context": {"member": member.login}},
            )
            return response.json()["data"]["id"]
        else:
            logger.error(
                "Failed to create/update member",
                extra={
                    "context": {
                        "member": member.login,
                        "error": response.text,
                        "status_code": response.status_code,
                    }
                },
            )
            return None

    def create_activity(self, activity_type, user, description, link, occurred_at, key):
        url = (
            f"https://app.orbit.love/api/v1/{self.workspace}/members/{user}/activities"
        )

        payload = {
            "description": description,
            "link": link,
            "title": activity_type,
            "description": description,
            "activity_type": activity_type,
            "occurred_at": occurred_at,
            "key": key,
        }

        response = requests.request("POST", url, json=payload, headers=self.headers)

        if response.status_code == 201 or response.status_code == 200:
            logger.info(
                "Created activity",
                extra={"context": {"activity": activity_type, "user": user}},
            )
        else:
            logger.error(
                "Failed to create activity",
                extra={
                    "context": {
                        "activity": activity_type,
                        "user": user,
                        "error": response.text,
                        "status_code": response.status_code,
                    }
                },
            )


# Docs: https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types
def parse_github_event(e):
    logger.info(
        "Parsing event",
        extra={
            "context": {"repository": repo.name, "type": e.type, "user": e.actor.login,}
        },
    )
    if e.type == "CommitCommentEvent":
        return
    elif e.type == "CreateEvent":
        return
    elif e.type == "DeleteEvent":
        return
    elif e.type == "ForkEvent":
        user_id = o.create_or_update_member(e.actor, "")
        if not user_id:
            return
        o.create_activity(
            f"g/{repo.name}/forked", user_id, "", "", e.created_at.isoformat(), e.id
        )
        return
    elif e.type == "GollumEvent":
        return
    elif e.type == "IssueCommentEvent":
        msg = f"In: [{e.payload['issue']['title']}]({e.payload['comment']['html_url']})"
        user_id = o.create_or_update_member(e.actor, "")
        if not user_id:
            return
        o.create_activity(
            f"g/{repo.name}/{e.payload['action']}-a-comment",
            user_id,
            msg,
            e.payload["comment"]["html_url"],
            e.created_at.isoformat(),
            e.id,
        )
        return
    elif e.type == "IssuesEvent":
        msg = (
            f"Named: [{e.payload['issue']['title']}]({e.payload['issue']['html_url']})"
        )
        user_id = o.create_or_update_member(e.actor, "")
        if not user_id:
            return
        o.create_activity(
            f"g/{repo.name}/{e.payload['action']}-an-issue",
            user_id,
            msg,
            e.payload["issue"]["html_url"],
            e.created_at.isoformat(),
            e.id,
        )
        return
    elif e.type == "MemberEvent":
        return
    elif e.type == "PublicEvent":
        return
    elif e.type == "PullRequestEvent":
        msg = f"Named: [{e.payload['pull_request']['title']}]({e.payload['pull_request']['html_url']})"
        user_id = o.create_or_update_member(e.actor, "")
        if not user_id:
            return
        o.create_activity(
            f"g/{repo.name}/{e.payload['action']}-a-pr",
            user_id,
            msg,
            e.payload["pull_request"]["html_url"],
            e.created_at.isoformat(),
            e.id,
        )
        return
    elif e.type == "PullRequestReviewEvent":
        return
    elif e.type == "PullRequestReviewCommentEvent":
        return
    elif e.type == "PushEvent":
        return
    elif e.type == "ReleaseEvent":
        return
    elif e.type == "SponsorshipEvent":
        return
    elif e.type == "WatchEvent":
        user_id = o.create_or_update_member(e.actor, "")
        if not user_id:
            return
        o.create_activity(
            f"g/{repo.name}/{e.payload['action']}-watching",
            user_id,
            "",
            "",
            e.created_at.isoformat(),
            e.id,
        )
        return
    else:
        logger.error(
            f"Failed parsing event: Unknown event type: {e.type}",
            extra={
                "context": {
                    "repository": repo.name,
                    "type": e.type,
                    "user": e.actor.login,
                }
            },
        )


if __name__ == "__main__":
    logger.info("Starting github_orbit")

    o = Orbit(ORBIT_WORKSPACE, ORBIT_TOKEN)
    g = Github(GITHUB_TOKEN)

    org = g.get_organization(GITHUB_ORG_NAME)

    for repo in org.get_repos():

        if GITHUB_REPO_NAME_CONTAINS not in repo.name or repo.private:
            continue

        logger.info(f"Processing repo", extra={"context": {"repository": repo.name}})

        for e in repo.get_events():
            if e.created_at < datetime.datetime.now() - datetime.timedelta(
                hours=MAX_EVENT_AGE
            ):
                logger.info(
                    f"No more events", extra={"context": {"repository": e.repo.name}}
                )
                break
            parse_github_event(e)
