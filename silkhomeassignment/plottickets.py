"""
plottickets.py

Create a bar chart that shows the number of tickets created per minute 
over the 1 hour period - the X axis will have 60 ticks - one per minute,
and the bar height will be the number of tickets created in that minute.
"""

from atlassian import Jira
from dateutil.parser import parse
from tinydb import TinyDB, Query
import argparse
import logging
import matplotlib.pyplot as plt
import pandas as pd
import time
from typing import List

logging.basicConfig(level=logging.INFO)


def plot_issues_per_minutes(timestamps: List[str], output_file: str) -> None:
    df = pd.DataFrame([parse(t) for t in timestamps], columns=["created"])
    df = df.set_index("created").sort_index()
    df_resampled = df.resample("1min").size()
    df_resampled = df_resampled.reset_index()
    df_resampled["created"] = df_resampled["created"].dt.strftime("%H-%M")
    df_resampled = df_resampled.set_index("created")
    df_resampled.plot(kind="bar")
    plt.title("Number of Issues per minute")
    plt.xlabel("Time")
    plt.ylabel("Number of Issues")
    plt.savefig(output_file, dpi=300, bbox_inches="tight")


def plot_tickets(dbfile: str, pngfile: str) -> None:
    logging.info(f"Run start time: {time.ctime()}")
    db = TinyDB(dbfile)
    db.all()
    data = [i["created"] for i in db.all()]
    plot_issues_per_minutes(data, pngfile)
    logging.info(f"Run end time: {time.ctime()}")


def main():
    parser = argparse.ArgumentParser(description="Create Jira tickets.")
    parser.add_argument(
        "--input",
        default="issues.json",
        help="Path to the input file (default: issues.json)",
    )
    parser.add_argument(
        "--output",
        default="records_per_minute.png",
        help="Path to the output file (default: records_per_minute.png)",
    )
    args = parser.parse_args()
    plot_tickets(args.input, args.output)


if __name__ == "__main__":
    main()
