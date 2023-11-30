import shutil
import click
import requests
from datetime import datetime
import os


@click.group()
def cli():
    pass


main_template = """
def solve(input_lines: list[str]):
    pass

def main():
    with open("{0}/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    print(solve(test_input))


if __name__ == "__main__":
    main()
"""


@cli.command()
@click.option("--day", type=int, default=datetime.now().day)
@click.option("--session_cookie", type=str)
@click.option("--year", type=int, default=datetime.now().year)
def new_day(day: int, session_cookie: str, year: str):
    padded = str(day).zfill(2)
    print(f"Creating day {padded}")

    if os.path.isdir(padded):
        raise Exception(f"Folder {padded} already exists")

    os.mkdir(padded)
    os.mkdir(f"{padded}/1")
    os.mkdir(f"{padded}/2")

    with open(f"{padded}/1/main.py", "w") as f:
        f.writelines(main_template.format(padded))

    if not session_cookie:
        print("No session cookie specified. Skipping download")
        return
    
    url = f"https://adventofcode.com/{year}/day/{day}/input"

    print(f"Downloading: {url}")

    r = requests.get(url, headers={
        "Cookie": f"session={session_cookie}"
    })

    with open(f"{padded}/input.txt", "w") as f:
        f.writelines(r.text)


test_template = """
from main import solve

def test_main():
    assert solve([])
"""


@cli.command()
@click.option("--day", type=int, default=datetime.now().day)
def add_tests(day):
    padded = str(day).zfill(2)
    print(f"Creating tests for day {padded}")

    if not os.path.isdir(padded):
        raise Exception(f"Folder {padded} doesn't exist")

    if os.path.isfile(f"{padded}/1/test_main_{padded}_1.py"):
        raise Exception(f"Tests for {padded} already exists")

    with open(f"{padded}/1/test_main_{padded}_1.py", "w") as f:
        f.writelines(test_template)

    with open(f"{padded}/2/test_main_{padded}_2.py", "w") as f:
        f.writelines(test_template)


@cli.command()
@click.option("--day", type=int, default=datetime.now().day)
def part_two(day: int):
    padded = str(day).zfill(2)
    print(f"Creating part 2 of day {padded}")

    if not os.path.isdir(padded):
        raise Exception(f"Folder {padded} doesn't exist")

    if os.path.isfile(f"{padded}/2/main.py"):
        raise Exception(f"Part 2 file of {padded} already exists")

    shutil.copy2(f"{padded}/1/main.py", f"{padded}/2/main.py")


if __name__ == "__main__":
    cli()
