#! /usr/bin/env python3

import sys
import os
import json
from datetime import date
from jinja2 import Environment, PackageLoader, select_autoescape
import colander
from jsonresume.schema.resume import Resume as ResumeSchema


def date_formatter(_date: str) -> str:
    if _date:
        return date.fromisoformat(_date).strftime("%b %Y")


def is_valid_resume(file_path: str) -> bool:
    status = False

    try:
        with open(file_path, 'r') as fp:
            resume_json = json.load(fp)
    except (IOError, ValueError):
        print("Invalid json file".format(file_path), file=sys.stderr)
    else:
        try:
            resume = ResumeSchema().deserialize(resume_json)
        except colander.Invalid:
            print("Invalid JSON, doesn't confirm to schema", file=sys.stderr)
        else:
            status = True

    return status


def main(json_file):
    env = Environment(
        loader=PackageLoader("jinja", package_path='templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    env.filters['date_formatter'] = date_formatter

    template = env.get_template("index.j2")

    with open(json_file) as fp:
        resume = json.load(fp)

    with open("index.html", "w") as fp:
        fp.write(template.render(**resume))


if __name__ == "__main__":
    main(sys.argv[1])
