#!/usr/bin/env python3
# Downloads images from a given subreddit


import json
import os
import pprint
import praw
import subprocess
import sys


subreddit = ""
destination = ""


def print_usage():
    print("Usage: {0} <subreddit> [destination]")


def handle_no_args():
    print_usage()
    exit(1)


def handle_only_sub():
    global subreddit
    subreddit = sys.argv[1]


def handle_dest():
    handle_only_sub()
    global destination
    destination = sys.argv[2]


def handle_invalid():
    print_usage()
    exit(1)


def handle_args():
    if len(sys.argv) == 2:
        handle_only_sub()
    elif len(sys.argv) == 3:
        handle_dest()
    else:
        handle_invalid()


def main():
    handle_args()

    # Retrieve secrets
    with open("secrets") as f:
        client_id = f.readline().strip("\n")
        client_secret = f.readline().strip("\n")
        username = f.readline().strip("\n")
        password = f.readline().strip("\n")
        user_agent = f.readline().strip("\n")

    # Create Reddit instance (read only for now)
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         #password=password,
                         user_agent=user_agent)
                         #username=username)

    # See if custom directory has been specified
    if destination != "":
        directory = os.path.abspath(destination)
    else:
        directory = os.getcwd()

    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        subprocess.run("mkdir -p {}".format(directory).split())

    print(directory)

    print("Fetching content from {}...".format("/r/" + subreddit))

    for submission in reddit.subreddit(subreddit).top(time_filter="all", limit=2):
        print("Downloading image: {}".format(submission.title))
        subprocess.run("youtube-dl {}".format(submission.url).split(),
                       cwd=directory)


if __name__ == "__main__":
    main()
