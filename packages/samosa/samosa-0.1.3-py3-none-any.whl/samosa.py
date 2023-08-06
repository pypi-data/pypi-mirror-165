#!/usr/bin/env python3
# Copyright 2022 David Seaward and contributors
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import stat
import sys
from importlib import resources
from time import sleep

from pygit2 import Repository, GitError
from pygit2._pygit2 import GIT_BRANCH_LOCAL, GIT_BRANCH_REMOTE


def get_config_key(config, key):
    try:
        return list(config.get_multivar(key))[-1]
    except IndexError:
        return None


def get_remote_address(repo, key):
    try:
        return repo.remotes[key].url
    except KeyError:
        return None


def print_samosa_message(line1, line2):
    samosa1 = "* *"
    samosa2 = " * "

    diff = abs(len(line1) - len(line2))
    spacer = " " * diff

    if len(line1) < len(line2):
        line1 += spacer
    else:
        line2 += spacer

    print(f"\n{line1}  {samosa1}\n{line2}  {samosa2}\n", file=sys.stdout)


def valid_suffix(address):
    for suffix in ["example.com", "example.edu", "example.net", "example.org", ".example", ".invalid"]:
        if address.endswith(suffix):
            return False

    return True


def debug_print_config(config):
    for entry in config:
        print(f"{entry.name}: {entry.value} ({entry.level})")


def debug_print_remotes(repo):
    for item in repo.remotes:
        print(item.name)


def validate_path(path):
    try:
        repo: Repository = Repository(path, flags=0)
        config = repo.config.snapshot()
    except GitError:
        print(f"No repository found in {path}", file=sys.stderr)
        return False

    if os.getenv("DEBUG", default=False):
        debug_print_config(config)
        debug_print_remotes(repo)

    errors = []

    # USERNAME IS VALID

    username = get_config_key(config, "user.name")
    if username is None or username in ["example", "invalid"]:
        errors.append("Fix invalid username with: git config --local user.name \"Your Name\"")

    # EMAIL ADDRESS IS VALID

    email_address = get_config_key(config, "user.email")
    if email_address is None or not valid_suffix(email_address):
        errors.append("Fix invalid email address with: git config --local user.email \"address@mail.example\"")

    # ANY REMOTE EXISTS

    if len(repo.remotes) == 0:
        errors.append("No remotes defined!")

    # ORIGIN REMOTE (test occurs later)

    origin_address = get_remote_address(repo, "origin")
    if origin_address is None:
        errors.append("Fix missing origin with: git remote add origin "
                      "git@example.example:origin/example.git")

    # UPSTREAM REMOTE EXISTS

    upstream_address = get_remote_address(repo, "upstream")
    if upstream_address is None:
        errors.append("Fix missing upstream with: git remote add upstream "
                      "git@example.example:upstream/example.git")

    remote_push_default = get_config_key(config, "remote.pushdefault")
    if remote_push_default is None or remote_push_default != "origin":
        errors.append(f"Fix default push remote with: git config remote.pushdefault origin")

    branch_push_default = get_config_key(config, "push.default")
    if branch_push_default is None or branch_push_default != "current":
        errors.append("Fix default push branch with: git config push.default current")

    # PRE-COMMIT HOOK EXISTS

    pre_commit_status = "Not set"
    pre_commit_path = os.path.join(path, ".git/hooks/pre-commit")
    if not os.path.isfile(pre_commit_path):
        try:
            with resources.open_text("samosa_resource", "pre-commit") as source, open(pre_commit_path, "w") as target:
                for line in source:
                    target.write(line)

        except IOError:
            errors.append(f"Pre-commit hook is missing and cannot be added. Please create .git/hooks/pre-commit")

    # PRE-COMMIT HOOK IS EXECUTABLE

    if os.path.isfile(pre_commit_path):

        # set owner execution
        mode = os.stat(pre_commit_path).st_mode
        os.chmod(pre_commit_path, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        # confirm owner execution
        if os.stat(pre_commit_path).st_mode & stat.S_IXUSR:
            pre_commit_status = "Set"
        else:
            errors.append(f"Fix missing executable bit with: chmod u+x .git/hooks/pre-commit")

    # LOCAL MAIN BRANCH EXISTS

    local_main_branch = repo.lookup_branch("main", GIT_BRANCH_LOCAL)
    if local_main_branch is None:
        local_main_name = "missing"
        errors.append("No local branch named main!")
    else:
        local_main_name = "main"

    # UPSTREAM MAIN BRANCH EXISTS

    upstream_main_branch = repo.lookup_branch("upstream/main", GIT_BRANCH_REMOTE)
    if upstream_main_branch is None:
        errors.append("No upstream branch named main!")

    # set upstream of `local/main` TO `upstream/main`
    if local_main_branch and upstream_main_branch:
        local_main_branch.upstream = upstream_main_branch

    # CONFIRM UPSTREAM OF `local/main` is `upstream/main`

    if local_main_branch:
        local_main_upstream = local_main_branch.upstream.raw_branch_name.decode()
        if local_main_upstream != "upstream/main":
            errors.append("Fix upstream target with: git branch main --set-upstream-to=upstream/main")
    else:
        local_main_upstream = "missing"  # No additional errors required

    # FINAL CHECK FOR PRE-COMMIT

    if pre_commit_status == "Not set":
        errors.append(f"Pre-commit hook still not set!")

    summary = [f"  Upstream: {upstream_address}",
               f"    Origin: {origin_address}",
               f" Pull from: {local_main_name} <- {local_main_upstream}",
               f"   Push to: current -> {remote_push_default}:{branch_push_default}",
               f"Pre-commit: {pre_commit_status}",
               f" Signature: {username} <{email_address}>"]

    print("\n".join(summary), file=sys.stdout)

    sleep(0.5)  # force result to appear after summary

    if any(errors):
        print("ERRORS:\n" + "\n".join(errors), file=sys.stderr)
        return False
    else:
        print_samosa_message("This repository", "is samosa standard")
        return True


def validate_cwd_and_exit():
    if validate_path(os.getcwd()):
        exit(0)
    else:
        exit(1)


if __name__ == '__main__':
    validate_cwd_and_exit()
