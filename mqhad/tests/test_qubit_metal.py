from collections import OrderedDict
from unittest.mock import MagicMock
import numpy as np
from mqhad.designer.qubit import QubitMetal
from qiskit_metal.designs import DesignPlanar
from qiskit_metal.qlibrary.qubits.transmon_pocket_6 import TransmonPocket6


class TestQubitMetal:
    @classmethod
    def setup_class(cls):
        """setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.qubit_grid = np.array(
            [
                [-1, -1, -1, 0, -1, -1, -1, 1, -1, -1, -1],
                [-1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                [-1, 12, -1, -1, -1, 13, -1, -1, -1, 14, -1],
                [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, -1],
                [-1, -1, -1, 25, -1, -1, -1, 26, -1, -1, -1],
            ]
        )
        cls.pins_to_remove = OrderedDict(
            [
                (
                    15,
                    {
                        "surrounding_qubits": {
                            "left": -1,
                            "right": 16,
                            "top": -1,
                            "bottom": -1,
                        },
                        "remove": ["B0", "B2", "B1"],
                    },
                ),
                (
                    2,
                    {
                        "surrounding_qubits": {
                            "left": -1,
                            "right": 3,
                            "top": 12,
                            "bottom": -1,
                        },
                        "remove": ["B2", "B3"],
                    },
                ),
                (
                    12,
                    {
                        "surrounding_qubits": {
                            "left": -1,
                            "right": -1,
                            "top": 16,
                            "bottom": 2,
                        },
                        "remove": ["B0", "B3"],
                    },
                ),
                (
                    16,
                    {
                        "surrounding_qubits": {
                            "left": 15,
                            "right": 17,
                            "top": -1,
                            "bottom": 12,
                        },
                        "remove": ["B0"],
                    },
                ),
                (
                    3,
                    {
                        "surrounding_qubits": {
                            "left": 2,
                            "right": 4,
                            "top": -1,
                            "bottom": -1,
                        },
                        "remove": ["B2", "B1"],
                    },
                ),
                (
                    17,
                    {
                        "surrounding_qubits": {
                            "left": 16,
                            "right": 18,
                            "top": -1,
                            "bottom": -1,
                        },
                        "remove": ["B2", "B1"],
                    },
                ),
                (
                    0,
                    {
                        "surrounding_qubits": {
                            "left": -1,
                            "right": -1,
                            "top": 4,
                            "bottom": -1,
                        },
                        "remove": ["B0", "B3"],
                    },
                ),
                (
                    4,
                    {
                        "surrounding_qubits": {
                            "left": 3,
                            "right": 5,
                            "top": -1,
                            "bottom": 0,
                        },
                        "remove": ["B0"],
                    },
                ),
                (
                    18,
                    {
                        "surrounding_qubits": {
                            "left": 17,
                            "right": 19,
                            "top": 25,
                            "bottom": -1,
                        },
                        "remove": ["B3"],
                    },
                ),
                (
                    25,
                    {
                        "surrounding_qubits": {
                            "left": -1,
                            "right": -1,
                            "top": -1,
                            "bottom": 18,
                        },
                        "remove": ["B0", "B3"],
                    },
                ),
                (
                    5,
                    {
                        "surrounding_qubits": {
                            "left": 4,
                            "right": 6,
                            "top": -1,
                            "bottom": -1,
                        },
                        "remove": ["B2", "B1"],
                    },
                ),
                (
                    19,
                    {
                        "surrounding_qubits": {
                            "left": 18,
                            "right": 20,
                            "top": -1,
                            "bottom": -1,
                        },
                        "remove": ["B2", "B1"],
                    },
                ),
                (
                    6,
                    {
                        "surrounding_qubits": {
                            "left": 5,
                            "right": 7,
                            "top": 13,
                            "bottom": -1,
                        },
                        "remove": ["B3"],
                    },
                ),
                (
                    13,
                    {
                        "surrounding_qubits": {
                            "left": -1,
                            "right": -1,
                            "top": 20,
                            "bottom": 6,
                        },
                        "remove": ["B0", "B3"],
                    },
                ),
                (
                    20,
                    {
                        "surrounding_qubits": {
                            "left": 19,
                            "right": 21,
                            "top": -1,
                            "bottom": 13,
                        },
                        "remove": ["B0"],
                    },
                ),
                (
                    7,
                    {
                        "surrounding_qubits": {
                            "left": 6,
                            "right": 8,
                            "top": -1,
                            "bottom": -1,
                        },
                        "remove": ["B2", "B1"],
                    },
                ),
                (
                    21,
                    {
                        "surrounding_qubits": {
                            "left": 20,
                            "right": 22,
                            "top": -1,
                            "bottom": -1,
                        },
                        "remove": ["B2", "B1"],
                    },
                ),
                (
                    1,
                    {
                        "surrounding_qubits": {
                            "left": -1,
                            "right": -1,
                            "top": 8,
                            "bottom": -1,
                        },
                        "remove": ["B0", "B3"],
                    },
                ),
                (
                    8,
                    {
                        "surrounding_qubits": {
                            "left": 7,
                            "right": 9,
                            "top": -1,
                            "bottom": 1,
                        },
                        "remove": ["B0"],
                    },
                ),
                (
                    22,
                    {
                        "surrounding_qubits": {
                            "left": 21,
                            "right": 23,
                            "top": 26,
                            "bottom": -1,
                        },
                        "remove": ["B3"],
                    },
                ),
                (
                    26,
                    {
                        "surrounding_qubits": {
                            "left": -1,
                            "right": -1,
                            "top": -1,
                            "bottom": 22,
                        },
                        "remove": ["B0", "B3"],
                    },
                ),
                (
                    9,
                    {
                        "surrounding_qubits": {
                            "left": 8,
                            "right": 10,
                            "top": -1,
                            "bottom": -1,
                        },
                        "remove": ["B2", "B1"],
                    },
                ),
                (
                    23,
                    {
                        "surrounding_qubits": {
                            "left": 22,
                            "right": 24,
                            "top": -1,
                            "bottom": -1,
                        },
                        "remove": ["B2", "B1"],
                    },
                ),
                (
                    10,
                    {
                        "surrounding_qubits": {
                            "left": 9,
                            "right": 11,
                            "top": 14,
                            "bottom": -1,
                        },
                        "remove": ["B3"],
                    },
                ),
                (
                    14,
                    {
                        "surrounding_qubits": {
                            "left": -1,
                            "right": -1,
                            "top": 24,
                            "bottom": 10,
                        },
                        "remove": ["B0", "B3"],
                    },
                ),
                (
                    24,
                    {
                        "surrounding_qubits": {
                            "left": 23,
                            "right": -1,
                            "top": -1,
                            "bottom": 14,
                        },
                        "remove": ["B1", "B0"],
                    },
                ),
                (
                    11,
                    {
                        "surrounding_qubits": {
                            "left": 10,
                            "right": -1,
                            "top": -1,
                            "bottom": -1,
                        },
                        "remove": ["B3", "B2", "B1"],
                    },
                ),
            ]
        )

    def test_generate_qubit_layout(self):
        design = DesignPlanar()
        qubit = QubitMetal()
        qubit._get_open_qubit_pins = MagicMock(return_value=self.pins_to_remove)
        qubit._generate_qubits = MagicMock(
            return_value=[
                TransmonPocket6(design),
                TransmonPocket6(design),
            ]
        )
        qubits = qubit.generate_qubit_layout()
        assert len(qubits) == 2

    def test_generate_qubits(self):
        design = DesignPlanar()
        qubit = QubitMetal()
        qubits = qubit._generate_qubits(design, self.qubit_grid, self.pins_to_remove)
        assert len(qubits) == np.sum(self.qubit_grid != -1)

    def test_get_open_qubit_pins(self):
        qubit = QubitMetal()
        open_qubit_pins = qubit._get_open_qubit_pins(self.qubit_grid)
        assert open_qubit_pins == self.pins_to_remove

    def test_get_qubit(self):
        qubit = QubitMetal()
        assert 0 == qubit._get_qubit(self.qubit_grid, 0, 3)
        assert -1 == qubit._get_qubit(self.qubit_grid, 0, 0)
        assert -1 == qubit._get_qubit(self.qubit_grid, -1, 1)
        assert -1 == qubit._get_qubit(self.qubit_grid, 1, -1)
        assert -1 == qubit._get_qubit(self.qubit_grid, self.qubit_grid.shape[0] + 1, 5)
        assert -1 == qubit._get_qubit(self.qubit_grid, 5, self.qubit_grid.shape[1] + 1)
