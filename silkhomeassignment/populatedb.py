"""
populatedb.py

Reads the tickets created by gentickets modules and stores the
High / Critical(Highest) ones into a DB
"""

from atlassian import Jira
from tinydb import TinyDB
import argparse
import logging
import time
import toml

logging.basicConfig(level=logging.INFO)

priorities = [
    "Highest",
    "High",
]


def populatedb(jira: Jira, project: str) -> None:
    logging.info(f"Run start time: {time.ctime()}")
    query = f"""project = "{project}" AND priority IN ({','.join(priorities)}) ORDER BY created DESC"""
    start_at = 0
    max_results = 10
    db = TinyDB("issues.json")
    count = 0
    while True:
        response = jira.jql(
            query,
            start=start_at,
            limit=max_results,
            fields=[
                "summary",
                "description",
                "issuetype",
                "priority",
                "created",
            ],
        )
        for issue in response["issues"]:
            db.insert(issue["fields"])
            count += 1
        if response["total"] <= start_at + max_results:
            break
        start_at += max_results
    logging.info(f"Populated {count} issues.")
    logging.info(f"Run end time: {time.ctime()}")


def main():
    parser = argparse.ArgumentParser(description="Create Jira tickets.")
    parser.add_argument(
        "--config",
        default="config.toml",
        help="Path to the config file (default: config.toml)",
    )
    parser.add_argument(
        "--output",
        default="issues.json",
        help="Path to the output file (default: issues.json)",
    )
    args = parser.parse_args()
    config = toml.load(args.config)
    jira = Jira(
        url=config["jira"]["url"],
        username=config["jira"]["username"],
        password=config["jira"]["password"],
    )
    project = config["jira"]["project"]
    populatedb(jira, project)


if __name__ == "__main__":
    main()
