# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Gitlab_stats:

Generate a report from gitlab's pipeline metrics

for help:    gitlab_stats -h
"""
import argparse
import os
import sys

from gitlab_stats import utils
from gitlab_stats.wrapper import API


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="gitlab-stats: Generate a report from gitlab's pipeline metrics"
    )
    parser.add_argument(
        "id",
        help="Put the id of the gitlab project",
        default=get_env('PROJECT_ID'),
        nargs="?"
    )
    parser.add_argument(
        "-r", "--report",
        action="store_true",
        dest="report",
        default=get_env('CREATE_REPORT', default=False),
        help="Generate a report in csv"
    )
    parser.add_argument(
        "-u", "--url",
        default=get_env('GITLAB_URL', default="https://gitlab.com"),
        nargs="?",
        help="Put the url of your gitlab instance if different from https://gitlab.com"
    )
    parser.add_argument(
        "-p", "--proxy",
        default=get_env('HTTP_PROXY'),
        nargs="?",
        help="Add the url of your proxy like 'http://my.proxy.url:8083'"
    )
    return parser.parse_args(args)


def get_env(key, default=''):
    if key in os.environ:
        value = os.environ[key]
        return [value]
    else:
        return [default]


def main():
    args = parse_args(sys.argv[1:])
    proxy = utils.format_proxy(args.proxy[0])
    gitlab = API(base_url=args.url[0], proxies=proxy)
    print("Fetching your project information ...")
    project_id = args.id[0]
    pipelines = gitlab.get_all_pipelines_info(
        project_id, pages=int(os.environ['PIPELINE_PAGES']))
    utils.dumping(pipelines, project_id)


if __name__ == '__main__':
    main()
