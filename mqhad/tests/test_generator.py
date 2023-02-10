import pytest
from qiskit import QuantumRegister, QuantumCircuit
from mqhad.architecture_generator.generator import Generator
from mqhad.architecture_generator.profile import Profile
from mqhad.architecture_generator.layout import Layout


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

    def test_init(self):
        with pytest.raises(TypeError):
            Generator(qc=1)
        with pytest.raises(TypeError):
            Generator(profile=1)
        Generator(profile=Profile())
        with pytest.raises(TypeError):
            Generator(layout=1)
        Generator(layout=Layout())

    def test_generate(self):
        generator = Generator(qc=self.qc)
        generator.generate()
