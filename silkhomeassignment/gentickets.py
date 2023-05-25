"""
gentickets.py

Create TICKET_COUNT number of random jira tickets over the course of RUN_TIME seconds

a) The creation time of the ticket is randomized.
b) Tickets priority is randomized. See priorities list.

"""
from atlassian import Jira
import argparse
import logging
import lorem
import random
import time
import toml

logging.basicConfig(level=logging.INFO)

issuetypes = ["Task", "Bug", "Improvement"]
priorities = ["Highest", "High", "Medium", "Low", "Lowest"]

TICKET_COUNT = 100
RUN_TIME = 60 * 60  # 1 hour


def generate_tickets(jira: Jira, project: str) -> None:
    logging.info(f"Run start time: {time.ctime()}")
    start_time = time.time()
    random_times = [random.uniform(0, RUN_TIME) for i in range(TICKET_COUNT)]
    random_times.sort()
    first_sleep_time = random_times[0]
    time.sleep(first_sleep_time)
    count = 1
    for i in range(1, len(random_times)):
        ta = time.time()
        issuetype = random.choice(issuetypes)
        priority = random.choice(priorities)

        issue_dict = {
            "project": {"key": project},
            "summary": lorem.sentence(),
            "description": lorem.paragraph(),
            "issuetype": {"name": issuetype},
            "priority": {"name": priority},
        }
        try:
            new_issue = jira.issue_create(fields=issue_dict)
            logging.debug(f"Created issue {count}: {new_issue}")
        except Exception as e:
            logging.error(f"Failed to create issue {count}: {e}")
        # set up the next sleep time
        tb = time.time()
        # we will take into account the time taken to run each ticket creation
        time.sleep(random_times[i] - (first_sleep_time + (tb - ta)))
        first_sleep_time = random_times[i]
    logging.info(f"Run end time: {time.ctime()}")


def main():
    parser = argparse.ArgumentParser(description="Create Jira tickets.")
    parser.add_argument(
        "--config",
        default="config.toml",
        help="Path to the config file (default: config.toml)",
    )
    args = parser.parse_args()
    config = toml.load(args.config)
    jira = Jira(
        url=config["jira"]["url"],
        username=config["jira"]["username"],
        password=config["jira"]["password"],
    )
    project = config["jira"]["project"]
    generate_tickets(jira, project)


if __name__ == "__main__":
    main()
