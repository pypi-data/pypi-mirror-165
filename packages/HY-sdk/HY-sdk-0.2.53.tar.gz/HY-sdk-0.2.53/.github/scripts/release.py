#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time     : 2022/8/27 14:30
@Author   : cuny
@File     : release.py
@Software : PyCharm
@Introduce: 
本文件调用GitHub CLI来创建具有自动递增版本号和自动生成的发行说明的新版本。
如果项目尚无任何版本，它将用作第一个版本号。
如果要增加主要或次要版本号，则必须手动创建一个版本才能执行此操作。
本文件将开始在新的主要或次要版本号之上生成补丁编号。
"""
import json
import subprocess


def get_last_version() -> str:
    """Return the version number of the last release."""
    json_string = (
        subprocess.run(
            ["gh", "release", "view", "--json", "tagName"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        .stdout.decode("utf8")
        .strip()
    )

    return json.loads(json_string)["tagName"]


def bump_patch_number(version_number: str) -> str:
    """Return a copy of `version_number` with the patch number incremented."""
    print("[latest version]: ", version_number)
    major, minor, patch = version_number.split(".")
    return f"{major}.{minor}.{int(patch) + 1}"


def create_new_patch_release():
    """Create a new patch release on GitHub."""
    try:
        last_version_number = get_last_version()
    except subprocess.CalledProcessError as err:
        if err.stderr.decode("utf8").startswith("HTTP 404:"):
            # The project doesn't have any releases yet.
            new_version_number = "0.0.1"
        else:
            raise
    else:
        new_version_number = bump_patch_number(last_version_number)

    subprocess.run(
        ["gh", "release", "create", "--generate-notes", new_version_number],
        check=True,
    )


if __name__ == "__main__":
    create_new_patch_release()
