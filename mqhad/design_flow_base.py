from abc import ABC, abstractmethod
from typing import Any
import sys
from mqhad.architecture_generator1.generator import Generator
from mqhad.mapper.mapper import Mapper
from mqhad.optimizer.optimizer import Optimizer
from qiskit import QuantumCircuit
from qiskit_metal import MetalGUI


class DesignFlowBase(ABC):
    def __init__(
        self, qc: Any = None, circuit_path: str = "", config: dict = {}, *args, **kwargs
    ):
        self.config = config
        self.qc = qc
        self.circuit_path = circuit_path

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config: dict):
        self._config = config

    @property
    def qc(self):
        return self._qc

    @qc.setter
    def qc(self, qc: Any):
        self._qc = qc

    @property
    def circuit_path(self):
        return self._circuit_path

    @circuit_path.setter
    def circuit_path(self, circuit_path: str):
        self._circuit_path = circuit_path

    @property
    def qubit_grid(self):
        return self._qubit_grid

    @qubit_grid.setter
    def qubit_grid(self, qubit_grid: dict):
        self._qubit_grid = qubit_grid

    @property
    def qubit_frequencies(self):
        return self._qubit_frequencies

    @qubit_frequencies.setter
    def qubit_frequencies(self, qubit_frequencies: dict):
        self._qubit_frequencies = qubit_frequencies

    @property
    def canvas(self):
        return self._canvas

    @canvas.setter
    def canvas(self, canvas: MetalGUI):
        self._canvas = canvas

    @abstractmethod
    def generate_architecture(self):
        pass

    @abstractmethod
    def map_to_physical_layout(self):
        pass

    @abstractmethod
    def optimize_design(self):
        pass

    @abstractmethod
    def display_gui(self):
        pass

    # Hooks
    def read_circuit(self):
        pass

    def run(self):
        if self._qc == None:
            self.read_circuit()

        print("#### Start generating architecture ####")
        self.generate_architecture()
        print("#### Architecture generated ####")
        print("Qubit grid:", self.qubit_grid)
        print("Qubit frequencies:", self.qubit_frequencies)

        print("#### Start mapping to physical layout ####")
        self.map_to_physical_layout()
        print("#### Physical layout generated ####")

        print("Optimizing design...")
        self.optimize_design()
        print("Design optimized")

        self.display_gui()


class ConcreteDesignFlow(DesignFlowBase):
    def __init__(
        self,
        circuit_path: str = "",
        config: dict = {},
        display_gui: bool = True,
        *args,
        **kwargs
    ):
        super().__init__(circuit_path=circuit_path, config=config)
        self._display_gui = display_gui

    def read_circuit(self):
        self.qc = QuantumCircuit.from_qasm_file(self.circuit_path)

    def generate_architecture(self):
        generator = Generator(qc=self.qc)
        self.qubit_grid, self.qubit_frequencies = generator.generate()

    def map_to_physical_layout(self):
        if self.qubit_grid is None:
            print(
                "Error: qubit grid not generated. Please run generate_architecture() first."
            )
            return
        mapper = Mapper(
            design_backend="metal",
            qubit_grid=self.qubit_grid,
            qubit_frequencies=self.qubit_frequencies,
        )
        result = mapper.map()
        self.canvas = result["canvas"]

    def optimize_design(self):
        if self.canvas is None:
            print(
                "Error: physical design not generated. Please run generate_physical_design() first."
            )
            return

        optimizer = Optimizer(
            canvas=self.canvas,
            qubit_frequencies=self.qubit_frequencies,
            config=self.config,
        )
        optimizer.optimize()

    def display_gui(self):
        if self._display_gui == True:
            # We define a exit_no_operation() function that simply does nothing, and then use
            # the monkeypatch.setattr() method to replace the sys.exit() function with exit_noop() during the test.
            # This way, if the program calls sys.exit(), it will be replaced with the
            # no-op function and the test will continue to run instead of exiting.
            def exit_no_operation(status):
                pass

            gui = MetalGUI(self.canvas.get_canvas())
            q_app = gui.qApp
            print("Building GUI...")
            gui.rebuild()
            gui.autoscale()
            print("GUI built.")
            sys.exit = exit_no_operation
            sys.exit(q_app.exec_())
