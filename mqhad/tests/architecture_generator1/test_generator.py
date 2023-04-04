import itertools
from unittest import mock
import pytest
import numpy as np
from qiskit import QuantumRegister, QuantumCircuit
from mqhad.architecture_generator1.profile import Profile
from mqhad.architecture_generator1.layout import Layout
from mqhad.architecture_generator1.bus import Bus
from mqhad.architecture_generator1.chip import Chip


class TestGenerator:
    @classmethod
    def setup_class(cls):
        """setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        qr = QuantumRegister(5)
        qc = QuantumCircuit(qr)
        qc.h([0, 1, 2, 3])
        qc.x(4)
        qc.cx(0, 1)
        qc.h(4)
        qc.cx(0, 4)
        qc.h(0)
        qc.cx(1, 4)
        qc.cx(2, 4)
        qc.cx(3, 4)
        qc.cx(0, 4)
        cls.qc = qc

    def test_generate(self):
        with mock.patch(
            "mqhad.architecture_generator1.yieldsimulator.YieldSimulator"
        ) as mock_class:
            from mqhad.architecture_generator1.generator import Generator

            def infinite_generator():
                for i in itertools.count():
                    yield (i, 1.0 + 0.1 * i)

            instance = mock_class.return_value
            instance.simulate = mock.MagicMock(side_effect=infinite_generator())
            generator = Generator(qc=self.qc)
            qubit_grid, qubit_frequencies = generator.generate()
            np.testing.assert_equal(qubit_grid, [[-1, 2, -1], [3, 4, 0], [-1, 1, -1]])
            np.testing.assert_allclose(
                qubit_frequencies,
                [
                    5.339999999999993,
                    5.339999999999993,
                    5.339999999999993,
                    5.339999999999993,
                    5.17,
                ],
                rtol=1e-2,
            )

    # This test need to below tests that is mocking the YieldSimulator
    # so that the mocked YieldSimulator in previous tests is mocked properly.
    # Once the Frequency class is imported in this method, it is added to the namespace
    # and the mocked YieldSimulator is not mocked anymore.
    def test_init(self):
        from mqhad.architecture_generator1.frequency import Frequency
        from mqhad.architecture_generator1.generator import Generator

        with pytest.raises(TypeError):
            Generator()
        with pytest.raises(TypeError):
            Generator(qc=1)
        Generator(qc=self.qc)
        with pytest.raises(TypeError):
            Generator(qc=self.qc, profile=1)
        Generator(qc=self.qc, profile=Profile())
        with pytest.raises(TypeError):
            Generator(qc=self.qc, layout=1)
        Generator(qc=self.qc, layout=Layout())
        with pytest.raises(TypeError):
            Generator(qc=self.qc, bus=1)
        Generator(qc=self.qc, bus=Bus())
        with pytest.raises(TypeError):
            Generator(qc=self.qc, chip=1)
        Generator(qc=self.qc, chip=Chip())
        with pytest.raises(TypeError):
            Generator(qc=self.qc, frequency=1)
        Generator(qc=self.qc, frequency=Frequency())
