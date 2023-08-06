# TuxTrigger Subcommands

## Output File

TuxTrigger is storing the state of each repositories in yaml file.
To declare a custom output file path type:

```shell
tuxtrigger path/to/config.yaml --output path/to/output.yaml
```

## Log File

To declare custom path for log file type:

```shell
tuxtrigger path/to/config.yaml --log-file path/to/log-file.txt
```

## Change Log Level

By default TuxTrigger log level is set to: info
You can adjust log level by choosing one of the levels (debug, info, warn, error)

```shell
tuxtrigger path/to/config.yaml --log-level=warn
```

## TuxSuite Plan Folder

All the plans should be in one directory:

```shell
tuxtrigger path/to/config.yaml --plan path/to/plan-folder
```

## Current version

```shell
tuxtrigger -v
```

## Help

```shell
tuxtrigger --help
```

