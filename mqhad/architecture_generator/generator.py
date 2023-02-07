from collections import OrderedDict
from mqhad.architecture_generator.generator_base import GeneratorBase
import rustworkx as rx
import numpy as np
from qiskit.circuit import QuantumCircuit
from typing import List, Tuple


class Generator(GeneratorBase):
    def __init__(self, qc: QuantumCircuit = None) -> None:
        self.qc = qc

    def generate(self):
        pass
