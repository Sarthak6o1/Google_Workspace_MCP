import argparse
import os

from google_helper import get_credentials


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.force and os.path.exists("token.json"):
        os.remove("token.json")

    get_credentials()
