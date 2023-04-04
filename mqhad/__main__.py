import argparse
import os
import sys
import yaml
from mqhad.architecture_generator1.generator import Generator
from mqhad.designer.design import Design
from mqhad.optimizer.optimizer import Optimizer
from qiskit import QuantumCircuit
from qiskit_metal import MetalGUI


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
    )
    result = design.design()
    print("#### Physical design generated ####")
    print("Optimizing design...")
    canvas = result["canvas"]
    Optimizer(
        canvas=canvas, qubit_frequencies=qubit_frequencies, config=config
    ).optimize()
    print("Design optimized")

    if display_gui == True:
        # We define a exit_no_operation() function that simply does nothing, and then use
        # the monkeypatch.setattr() method to replace the sys.exit() function with exit_noop() during the test.
        # This way, if the program calls sys.exit(), it will be replaced with the
        # no-op function and the test will continue to run instead of exiting.
        def exit_no_operation(status):
            pass

        gui = MetalGUI(canvas.get_canvas())
        q_app = gui.qApp
        print("Design completed. Building GUI...")
        gui.rebuild()
        gui.autoscale()
        print("GUI built.")
        sys.exit = exit_no_operation
        sys.exit(q_app.exec_())
    else:
        print("Design completed.")


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
