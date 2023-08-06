from urllib.parse import ParseResult
import yaml
import logging
import subprocess

from pathlib import Path
from tuxtrigger.inputvalidation import YamlValidator


LOG = logging.getLogger("tuxtrigger")


def yaml_load(data):
    return yaml.load(data, Loader=yaml.FullLoader)


def yaml_file_read(file_path: Path):
    with file_path.open("r") as file:
        loaded_yaml = yaml_load(file)
    return loaded_yaml


def yaml_file_write(data_input, file_path: Path):
    with file_path.open("w") as writer:
        yaml.dump(data_input, writer)


def create_repo_list(data_input):
    if data_input is None:
        return 0
    for item in data_input["repositories"]:
        yield YamlValidator(**item)


# def find_in_yaml(value, data_yaml):
#     if data_yaml is None:
#         return None
#     if value in data_yaml:
#         return data_yaml[value]
#     for k, v in data_yaml.items():
#         if isinstance(v, dict):
#             for i in find_in_yaml(value, v):
#                 return i


def compare_sha(url_key, branch_name, input_dict, data_yaml_file) -> bool:
    if data_yaml_file is None:
        LOG.warning("\t*** Data Input is none, not able to compare sha")
        LOG.debug(f'\t-> sha: {input_dict[branch_name]["sha"]}')
        return False
    if branch_name not in data_yaml_file[url_key]:
        LOG.warning("\t*** Branch not found in yaml file")
        LOG.debug(f"\t*** branch name: {branch_name}")
        return False
    if (
        not input_dict[branch_name]["sha"]
        == data_yaml_file[url_key][branch_name]["sha"]
    ):
        LOG.info(
            f'\t-> sha: {input_dict[branch_name]["sha"]} vs \
        previous sha {data_yaml_file[url_key][branch_name]["sha"]}'
        )
        return True
    LOG.info(f'\t-> sha: {input_dict[branch_name]["sha"]}')
    LOG.info("\t-> no changes")
    return False


def create_squad_project(url: ParseResult, branch_name: str) -> str:
    url_fragment = (url.path).split("/")
    url_fragment = list(filter(None, url_fragment))
    return f'{(url_fragment[-1]).replace(".git","")}-{branch_name.replace("/","-")}'


def run_lsremote(repository: str, branch: str) -> dict:
    value_dict = dict()
    git_result = subprocess.run(
        ["git", "ls-remote", repository, branch],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    splited_value = git_result.stdout.split()
    value_dict[branch] = {"sha": "", "ref": ""}
    if git_result.returncode != 0:
        return value_dict

    if splited_value:
        value_dict[branch] = {"sha": splited_value[0], "ref": splited_value[1]}

    return value_dict
