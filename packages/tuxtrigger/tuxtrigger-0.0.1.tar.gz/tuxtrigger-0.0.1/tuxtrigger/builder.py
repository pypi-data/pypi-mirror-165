#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import os
import subprocess
import json
import logging
import tempfile
import requests


LOG = logging.getLogger("tuxtrigger")


def tux_console_build(git_repo, git_ref, target_arch, kconfig, toolchain):
    with tempfile.NamedTemporaryFile(suffix=".json") as json_temp:
        build = subprocess.run(
            [
                "tuxsuite",
                "build",
                "--git-repo",
                git_repo,
                "--git-ref",
                git_ref,
                "--target-arch",
                target_arch,
                "--kconfig",
                kconfig,
                "--toolchain",
                toolchain,
                "--json-out",
                json_temp.name,
                "--no-wait",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if build.returncode != 0:
            LOG.warning(f"*build stdout {build.stdout}")
            LOG.warning(f"*build stderr {build.stderr}")
            raise Exception(f"*** Tuxsuite not build repo {build.stderr}")

        LOG.debug(build.stdout)

        json_output = json.load(json_temp)
        LOG.debug(f'\t*** Build UID: {json_output["uid"]}')
        return json_output["uid"]


def tux_console_plan(json_data, plan_file, squad_group, squad_project) -> int:
    if json_data is None:
        LOG.warning("\t** Not able to submit plan -> json output is None")
        return 1
    with tempfile.NamedTemporaryFile(suffix=".json") as json_temp:
        plan = subprocess.run(
            [
                "tuxsuite",
                "plan",
                "--git-repo",
                json_data["git_repo"],
                "--git-ref",
                json_data["git_ref"],
                "--name",
                json_data["git_describe"],
                "--no-wait",
                plan_file,
                "--json-out",
                json_temp.name,
            ]
        )
        if plan.returncode != 0:
            LOG.warning(f'\t** Submiting Plan for {json_data["git_describe"]} failed')
            return 1
        LOG.info(f'\t-> Submiting Plan for {json_data["git_describe"]}')
        squad_submit(json_data, squad_group, squad_project, json_temp.name)
        return 0


def build_result(uid):
    if uid is None:
        return None
    build = subprocess.run(
        ["tuxsuite", "build", "get", uid, "--json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    json_output = json.loads(build.stdout)
    LOG.debug(f"\t ** JSON OUTPUT: {json_output}")
    LOG.info(
        f'\t-> Build {json_output["uid"]} state: {json_output["state"]}, result: {json_output["result"]}, git describe: {json_output["git_describe"]}'
    )
    return json_output


def build_result_list() -> int:
    build = subprocess.run(
        ["tuxsuite", "build", "list", "--json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    json_output_list = json.loads(build.stdout)
    for item in json_output_list:
        LOG.info(
            f'\t-> Build {item["uid"]} state: {item["state"]}, result: {item["result"]}, git describe: {item["git_describe"]}'
        )
    return 0


def squad_submit(json_data, squad_group, squad_project, plan_json):
    if squad_group is None or squad_project is None:
        LOG.warn("** SQUAD config is not available! Unable to process **")
        return 1

    squad = subprocess.run(
        [
            "squad-client",
            "submit-tuxsuite",
            "--group",
            squad_group,
            "--project",
            squad_project,
            "--build",
            json_data["git_describe"],
            "--backend",
            "tuxsuite.com",
            "--json",
            plan_json,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if squad.returncode != 0:
        LOG.warning(f"*build stdout {squad.stdout}")
        LOG.warning(f"*build stderr {squad.stderr}")
        raise Exception(f"*** squad-client not able to pass data {squad.stderr}")

    LOG.debug(squad.stdout)
    LOG.info(f'\t-> Plan submitted to SQUAD git describe: {json_data["git_describe"]}')
    return 0


def squad_sha_request(squad_project):
    url = f'{os.getenv("SQUAD_HOST")}/api/projects/?slug={squad_project}'
    resp = requests.get(url)
    json_output = json.loads(resp.content)
    id = json_output["results"][0]["id"]
    build_url = (
        f'{os.getenv("SQUAD_HOST")}/api/projects/{id}/builds/?ordering=-datetime'
    )
    build_resp = requests.get(build_url)
    build_json = json.loads(build_resp.content)
    lastest_version_url = build_json["results"][0]["metadata"]
    metadata_resp = requests.get(lastest_version_url)
    metadata_json = json.loads(metadata_resp.content)
    git_sha = metadata_json["git_sha"]
    return git_sha
