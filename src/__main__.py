import argparse
import os
import sys
import yaml
from .concrete_design_flow1 import ConcreteDesignFlow1


def check_file_path(args: argparse.Namespace):
    circuit_absolute_path = os.path.abspath(args.file_path)
    if os.path.exists(circuit_absolute_path) == False:
        print("Circuit file does not exist. Exiting...")
        return None, 1
    return circuit_absolute_path, 0


def check_config_file_path(args: argparse.Namespace):
    config_absolute_path = os.path.abspath(args.config_file_path)
    if os.path.exists(config_absolute_path) == False:
        print("Config file does not exist. Exiting...")
        return None, 1
    return config_absolute_path, 0


def load_yaml(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def flow(args):
    circuit_absolute_path, exit_code = check_file_path(args)
    if exit_code == 1:
        return

    config_absolute_path, exit_code = check_config_file_path(args)
    if exit_code == 1:
        return

    config = load_yaml(config_absolute_path)
    display_gui = True

    design_flow = ConcreteDesignFlow1(
        circuit_path=circuit_absolute_path, config=config, display_gui=display_gui
    )
    design_flow.run()


def main(args=None):
    parser = argparse.ArgumentParser(description="mqt-dasqa cli")
    parser.add_argument(
        "--file-path",
        type=str,
        help="QASM 2.0 absolute or relative file path",
        required=True,
    )
    parser.add_argument(
        "--config-file-path",
        type=str,
        help="Config absolute or relative file path",
        required=True,
    )
    args = parser.parse_args()
    flow(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
