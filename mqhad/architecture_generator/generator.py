from mqhad.architecture_generator.generator_base import GeneratorBase
from mqhad.architecture_generator.profile import ProfileBase, Profile
from mqhad.architecture_generator.layout import LayoutBase, Layout
from mqhad.architecture_generator.bus import BusBase, Bus
from mqhad.architecture_generator.chip import ChipBase, Chip
from mqhad.architecture_generator.frequency import FrequencyBase, Frequency
from mqhad.utils import Utils
from qiskit.circuit import QuantumCircuit


class Generator(GeneratorBase):
    def __init__(
        self,
        qc: QuantumCircuit = None,
        profile: ProfileBase = None,
        layout: LayoutBase = None,
        bus: BusBase = None,
        chip: ChipBase = None,
        frequency: FrequencyBase = None,
    ) -> None:
        if qc is not None:
            Utils.check_type(qc, QuantumCircuit)
        self.qc = qc

        if profile is not None:
            Utils.check_type(profile, ProfileBase)
        self.profile = profile

        if layout is not None:
            Utils.check_type(layout, LayoutBase)
        self.layout = layout

        if bus is not None:
            Utils.check_type(bus, BusBase)
        self.bus = bus

        if chip is not None:
            Utils.check_type(chip, ChipBase)
        self.chip = chip

        if frequency is not None:
            Utils.check_type(frequency, FrequencyBase)
        self.frequency = frequency

    def generate(self):
        print("Generating profile...")
        if self.profile is None:
            self.profile = Profile(self.qc)
        self._ordered_degree, self._adjacency_matrix = self.profile.get_profile()

        print("Generating layout...")
        if self.layout is None:
            self.layout = Layout(self._ordered_degree, self._adjacency_matrix)
        self._dimX, self._dimY, self._qubit_grid = self.layout.get_layout()

        print("Generating buses...")
        if self.bus is None:
            self.bus = Bus(
                self._dimX,
                self._dimY,
                self._qubit_grid,
                self._adjacency_matrix,
                num_4Q_bus=10,
            )
        self._bus_grid, self._bus_locations_4Q = self.bus.bus_select()

        print("Generating chip...")
        if self.chip is None:
            self.chip = Chip(
                self.qc.num_qubits, self._qubit_grid, self._bus_locations_4Q
            )
        self.chip.generate_buses()

        print("Generating frequencies...")
        if self.frequency is None:
            self.frequency = Frequency(
                self.qc.num_qubits,
                self._dimX,
                self._dimY,
                self._qubit_grid,
                self._bus_locations_4Q,
            )
        self._qubit_frequencies = self.frequency.get_frequency_allocation()

        print("Completed architecture generation.")

        return self._qubit_grid, self._qubit_frequencies
