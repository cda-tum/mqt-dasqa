import argparse
import os
import sys
import yaml
from mqhad.architecture_generator.generator import Generator
from mqhad.designer.design import Design
from qiskit import QuantumCircuit


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

    print("#### Start generating architecture ####")
    qc = QuantumCircuit.from_qasm_file(circuit_absolute_path)
    generator = Generator(qc=qc)
    qubit_grid, qubit_frequencies = generator.generate()
    print("#### Architecture generated ####")
    print("Qubit grid:", qubit_grid)
    print("Qubit frequencies:", qubit_frequencies)
    print("#### Start generating physical design ####")
    design = Design(
        design_backend="metal",
        qubit_grid=qubit_grid,
        qubit_frequencies=qubit_frequencies,
        display_gui=True,
        config=config,
    )
    design.design()
    print("#### Physical design generated ####")


def main(args=None):
    parser = argparse.ArgumentParser(description="mqhad cli")
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
