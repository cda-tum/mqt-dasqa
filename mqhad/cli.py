import argparse
import os
from mqhad.architecture_generator.generator import Generator
from qiskit import QuantumCircuit


def main(args):
    print("#### Start generating architecture ###")
    absolute_path = os.path.abspath(args.file_path)
    qc = QuantumCircuit.from_qasm_file(absolute_path)
    generator = Generator(qc=qc)
    qubit_grid, qubit_frequencies = generator.generate()
    print("#### Architecture generated ###")
    print("Qubit grid:", qubit_grid)
    print("Qubit frequencies:", qubit_frequencies)
    print("#### Generation ended ###")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="mqhad cli")
    parser.add_argument(
        "--file-path",
        type=str,
        help="QASM 2.0 absolute or relative file path",
        required=True,
    )
    args = parser.parse_args()
    main(args)
