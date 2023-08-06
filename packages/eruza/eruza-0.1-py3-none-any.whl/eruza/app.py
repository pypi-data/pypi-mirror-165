#!/usr/bin/env python

import argparse
import configparser
import os
import shutil
import sys


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        help=(
            "profile to use if ARM_PROFILE not set. if ARM_PROFILE is set, this "
            "will override it."
        ),
    )
    parser.add_argument(
        "--ignore-missing",
        action="store_true",
        help=(
            "if no matching config section is found, continue processing anyway "
            "without setting environment variables."
        ),
    )

    subparsers = parser.add_subparsers(dest="command")

    exec_parser = subparsers.add_parser("exec")
    exec_parser.add_argument("command", nargs=argparse.REMAINDER)
    exec_parser.set_defaults(which="exec")

    env_parser = subparsers.add_parser("env")
    env_parser.set_defaults(which="env")

    eval_parser = subparsers.add_parser("eval")
    eval_parser.set_defaults(which="eval")

    args = parser.parse_args()

    credentials_dir = os.path.expanduser("~/.azure/")
    credentials_path = os.path.join(credentials_dir, "credentials")

    if not os.path.exists(credentials_dir):
        sys.stderr.write("no credentials dir\n")
        sys.stderr.flush()
        sys.exit(1)

    if not os.path.exists(credentials_path):
        sys.stderr.write("no credentials path\n")
        sys.stderr.flush()
        sys.exit(1)

    file_stat = os.stat(credentials_path)
    file_mask = oct(file_stat.st_mode)[-3:]
    if file_mask != "600":
        sys.stderr.write(
            "permissions {} on {} are too broad, must be exactly 600\n"
            .format(
                file_mask,
                credentials_path,
            )
        )
        sys.stderr.flush()
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(credentials_path)

    profile = os.environ.get("ARM_PROFILE")
    if args.profile:
        profile = args.profile

    if profile not in config:
        if not args.ignore_missing:
            sys.stderr.write("no config for env {}\n".format(profile))
            sys.stderr.flush()
            sys.exit(1)

    azure_vars = {}
    if profile in config:
        for key, value in config[profile].items():
            azure_vars[key.upper()] = value

    new_environ = os.environ.copy()
    new_environ.update(azure_vars)
    new_environ["ERUZA"] = "1"
    new_environ["ERUZA_PROFILE"] = profile

    if args.which == "env":
        for key, value in new_environ.items():
            print("{}={}".format(key, value))
    elif args.which == "eval":
        for key, value in new_environ.items():
            if key.startswith("ARM_") or key.startswith("ERUZA_"):
                print("export {}={}".format(key, value))

    elif args.which == "exec":
        if args.command:
            new_command = args.command
        else:
            new_command = [os.environ.get("SHELL", "/bin/sh")]

        exec_path = new_command[0]
        if not "/" in exec_path:
            maybe_exec_path = shutil.which(exec_path)
            if maybe_exec_path:
                exec_path = maybe_exec_path

        os.execve(exec_path, new_command, new_environ)
    else:
        raise Exception(
            "Implementation Error: unknown value for args.which {}"
            .format(args.which)
        )
