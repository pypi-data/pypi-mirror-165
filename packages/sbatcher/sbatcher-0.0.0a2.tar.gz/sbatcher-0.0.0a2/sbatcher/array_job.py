import argparse
import fileinput
import itertools
import json
import sys
from logging import DEBUG
import os
import shlex
import shutil
import socket
import subprocess
from typing import Iterable

import sbatcher
from sbatcher.logs import logger


def get_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--config", "-c", dest="config_file", required=True, help="Config file for the command (- for stdin)")
    parser.add_argument("--dry-run", action="store_true", help="Don't actually execute any commands")
    parser.add_argument("--log-level", default="INFO", help="Print debugging info")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose mode (same as --log-level DEBUG)")
    return parser.parse_args()


def main(config_file: str, dry_run: bool, log_level: str, verbose: bool):
    log_level = DEBUG if verbose else log_level.upper()
    logger.setLevel(log_level)
    logger.info(f"Hostname {socket.gethostname()}.")
    logger.debug("Verbose logging enabled.")

    config = load_config(config_file)


    logger.debug(f"Building command combinations from config at {os.path.abspath(config_file)}:")
    commands = list(command_combinations(config))
    logger.debug(f"Generated {len(commands)} command combinations:")
    for i, command in enumerate(commands):
        logger.debug(f"    commands[{i}] = `{pretty_print_command(command)}`")

    run_task_ids = []
    if "SLURM_ARRAY_TASK_ID" in os.environ:
        run_task_ids.append(int(os.environ["SLURM_ARRAY_TASK_ID"]))
    elif dry_run:
        run_task_ids.extend(range(len(commands)))

    array_command = build_array_command(config=config, n_commands=len(commands))

    if not len(run_task_ids) and shutil.which(array_command[0]) or dry_run:
        logger.info(f"Launching array job")
        run_process(array_command, input=json.dumps(config), dry_run=dry_run)
        logger.info(f"")
    elif not shutil.which("sbatch"):
        logger.warning(f"Command `{array_command[0]}` not found.")
        logger.warning(f"Running {len(commands)} commands locally.")
        run_task_ids.extend(range(len(commands)))

    for n, array_task_id in enumerate(run_task_ids):
        logger.info(f"Running array task #{array_task_id}")
        command = commands[array_task_id]
        run_process(command, dry_run=dry_run)
        if n < len(run_task_ids):
            logger.info(f"")


def load_config(config_file):
    config_file = config_file.strip()
    if config_file == "-":
        # Argument is coming from STDIN
        std_input = "\n".join(sys.stdin.readlines())
        print(std_input)
        config = json.loads(std_input)
    else:
        # Argument is a filename
        with open(config_file) as f:
            config = json.load(f)
    logger.debug(f"Loading config at {os.path.abspath(config_file)}.")
    logger.debug(f"Config as parsed:")
    for line in json.dumps(config, indent=4).split("\n"):
        logger.debug(f"    {line}")
    return config


def build_array_command(*, config, n_commands):
    script_path = get_script_path()

    sbatch_options = config.get("sbatch_args", {})

    array_config = config.get("array_config", {})
    concurrent_max = array_config.get("concurrent_max", None)

    sbatch_options["--array"] = f"0-{n_commands}" if concurrent_max is None else f"0-{n_commands}%{concurrent_max}"

    sbatch_args = []
    for arg, value in sbatch_options.items():
        sbatch_args.extend(x for x in (arg, value) if x is not None)

    command = ["sbatch", *sbatch_args, script_path]
    return command


def get_script_path():
    return os.path.join(os.path.dirname(sbatcher.__file__), "bin/sbatcher-array-job")


def run_process(command: Iterable[str], *, input: str = None, dry_run: bool):
    if dry_run:
        logger.info(f"Pretending to run command (--dry-run):")
    else:
        logger.info(f"Running command:")

    logger.info(f"    {pretty_print_command(command)}")
    if input is not None:
        logger.debug(f"Sending STDIN to command:")
        logger.debug(input)
    if dry_run:
        return None
    return subprocess.run(list(command), input=input, text=True, check=True)


def command_combinations(config):
    cmd = shlex.split(config["command"])
    for command_combination in itertools.product(*(
        arg_combinations(arg)
        for arg in config["args"]
    )):
        yield [*cmd, *itertools.chain(*command_combination)]
    #
    # CMD_ARGS=$(python p2g/grid_search_args.py --nth-combination ${SLURM_ARRAY_TASK_ID})
    # CMD="p2g/train.py $LANG_DIR $OUT_DIR $CMD_ARGS"
    # echo Running on $(hostname)
    # echo python $CMD
    # PYTHONPATH=. python $CMD


def arg_combinations(arg):
    combinations = [[str(arg["arg"])]]
    if "values" in arg:
        values = (str(v) for v in arg["values"])
        combinations = itertools.product(*combinations, values)
    if "present" in arg:
        combinations = *combinations, []
    return combinations


def pretty_print_command(command):
    return " ".join(shlex.quote(part) for part in command)


if __name__ == '__main__':
    main(**vars(get_args()))

'''
#SBATCH --time 23:59:59
#SBATCH --exclude exanode-8-18,exanode-8-13,exanode-7-23,exanode-7-18
#SBATCH --mem 16GB
#SBATCH -c 8

LANG_DIR=output/english_cmudict/data-bin
OUT_DIR=output/checkpoints/lstm/english_cmudict
LIMIT=16

if [[ -z $SLURM_ARRAY_TASK_ID ]]; then
    LOG_DIR=slurm-logs/$(date --iso-8601=seconds)
    mkdir -p $LOG_DIR
    N_JOBS=$((0 + $(python p2g/grid_search_args.py|wc -l)))
    CMD="--partition gpu --gres gpu:1 -o $LOG_DIR/slurm-%A_%a.out --array=0-$N_JOBS%$LIMIT $0"
    echo sbatch $CMD
    sbatch $CMD
else
    CMD_ARGS=$(python p2g/grid_search_args.py --nth-combination ${SLURM_ARRAY_TASK_ID})
    CMD="p2g/train.py $LANG_DIR $OUT_DIR $CMD_ARGS"
    echo Running on $(hostname)
    echo python $CMD
    PYTHONPATH=. python $CMD
fi
'''