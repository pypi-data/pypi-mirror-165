# Running TuxTrigger

## Create Configuration File

To make TuxTrigger work you have to provide configuration .yaml file with declared SQUAD details and repositories data
(url to tracked repository, selected branches and plan.yaml file for TuxSuite Plan).

Example of basic config.yaml

```yaml
squad:
  url: https://qa-reports.linaro.org
  group: group_name
  project: project_name
repositories:
- url: https://gitlab.com/Linaro/lkft/mirrors/stable/linux-stable
  branches:
    - name: master
      plan: stable.yaml
    - name: linux-5.18.y
      plan: stable_next.yaml
- url: https://gitlab.com/Linaro/lkft/mirrors/stable/linux-stable-rc
  branches:
    - name: master
      plan: stable.yaml
    - name: queue/5.4
      plan: stable_next.yaml
```

## Create Plan for TuxSuite

!!! note
    TuxTrigger requires valid TuxSuite account with TUXSUITE_TOKEN declared as env var

For sending plan to TuxSuite you must provide relevant plan (and include that in the configuration file)

Example of a plan file
```yaml
version: 1
name: stable_plan
description: stable_plan
jobs:
- tests:
    - {device: qemu-x86_64, tests: [ltp-smoke]}
```
For further information about plans and TuxSuite configuration please Visit: [TuxSuite Home](https://docs.tuxsuite.com/)

## Running TuxTrigger

To run tuxtrigger with the default configuration file:
```shell
tuxtrigger /path/to/config.yaml
```


