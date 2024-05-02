# MQT DASQA - Designer for Alternative Superconducting Quantum Architectures<!-- omit from toc -->

DASQA (pronounced "dah-skuh") is a framework to encapsulate application-driven quantum hardware architecture. In this repository, a reference implementation of the framework is provided. This implementation was done with modularality and easy extensibility in mind to allow for future extensions and improvement.

## Table of contents<!-- omit from toc -->

- [Steps in framework](#steps-in-framework)
- [Repository structure](#repository-structure)
- [Extending reference implementation](#extending-reference-implementation)
  - [Using the framework](#using-the-framework)
  - [Extending the framework](#extending-the-framework)
- [Trying reference implementation](#trying-reference-implementation)
  - [Installation](#installation)
    - [Installing Package](#installing-package)
    - [Installing Qiskit Metal](#installing-qiskit-metal)
  - [Usage](#usage)
    - [Command-line interface (CLI)](#command-line-interface-cli)
    - [Testing the Package](#testing-the-package)
  - [Development](#development)
  - [FAQs](#faqs)

## Steps in framework

In this section, we will describe the steps in the framework as follows:

1. `Architecture generator` - generates an optimized high-level architecture based on a quantum application(i.e, quantum circuit). The input of the architecture generator is a quantum application and it outputs a high-level architecture containing the layout of the qubits and qubit frequencies
2. `Physical layout mapper` - maps the high-level architecture to physical layout using tools such as Qiskit Metal
3. `Optimizer` - optimizes the geometries of the components to hit target parameters

## Repository structure

In this section, we will describe the structure of the repository as follows to help you navigate through the repository:

1. `src` - contains the reference implementation of the framework
   1. `architecture_generator1` is based on [G. Li, Y. Ding and Y. Xie](https://arxiv.org/abs/1911.12879)
      1. `bus` generates connection between qubits
      2. `chip` creates temporary chip for simulation. The temporary chip is a subgraph of the layout graph and it is used in the frequency generation module
      3. `frequency` generates frequency of qubits using Monte Carlo simulation. It chooses frequency configuration based on maximum yield rate as computed by the `yieldsimulator` module
      4. `layout` generates matrix of qubit layout
      5. `profile` generates profiles of quantum application. The profile of are as follows:
         1. Two qubit gate map which contains control and target gates of the two qubit gate
         2. Connectivity degree of qubits
         3. Adjacency matrix of qubit
      6. `yieldsimulator` calculates the yield rate that is used by the `frequency` module. Yield rate is the number of sub-graphs with no frequency collision divided by the number of trials
   2. `mapper` maps architecture generator layout to [Qiskit Metal](https://qiskit.org/documentation/metal/) physical layout
      1. `canvas` is a module that creates the design space for the physical layout
      2. `capacitor` creates the capacitors
      3. `capacitor_launchpad_connector` generates capacitor to launchpad connectors
      4. `launchpad` creates launchpads(i.e, readout/control)
      5. `qubit` creates qubits
      6. `qubit_capacitor_connector` creates qubit to capacitor connections
      7. `qubit_connector` creates qubit-to-qubit connections
   3. `optimal_geometry_finder` contains the algorithm to find the optimal geometry of a component given a target parameter
   4. `optimizer` optimizes the geometries of layout to hit target parameters
   5. `__main__.py` is the entry point for the Command-Line Interface (CLI) application
2. `notebooks` trains statistical model to stand-in for simulation software such as Ansys HFSS and used by the optimizer

## Extending reference implementation

### Using the framework

A reference implementation of the framework is provided in the `src` directory. The reference implementation is modular and extensible.

To this end, a concrete implementation which is a subclass of `DesignFlowBase` class is available at [src/concrete_design_flow1.py](src/concrete_design_flow1.py). In the concrete implementation, an example of how the `generate_architecture` and `optimize_layout` abstract methods are overriden is given.

Then, the `run` method defined in the `DesignFlowBase` class invokes the `generate_architecture` and `optimize_layout` methods to execute the design flow.

### Extending the framework

Each module in [src](src/) has abstract classes which allows for easy extensibility.

As an example, the qubit layout subclass [TransmonPocket6Qubit](src/mapper/qubit/metal/transmon_pocket_6_qubit.py) in the physical layout mapper inherits from the `QubitBase` abstract class defined in [QubitBase](src/mapper/qubit/qubit_base.py) as:

```python
class QubitBase(ABC):
@abstractmethod
def generate_qubit_layout(self):
  pass
```

The [TransmonPocket6Qubit](src/mapper/qubit/metal/transmon_pocket_6_qubit.py) subclass then defines how the qubits are positioned on the physical layout. For a complete list of possible abstract classes that can be overriden in each module, please refer to the individual modules in [src](src/) directory.

## Trying reference implementation

### Installation

#### Installing Package

1. Clone the repository - `git clone {URL}`

2. Change to cloned directory - `cd dasqa`

3. The easiest way to install the toolkit without affecting other packages is to create a virtual environment, i.e: using conda, as following. Else, you can just run `python -m pip install -e .`. Do note that DASQA is tested on Python 3.10.

```text
conda env create -n mqt-dasqa -f environment.yml
conda activate mqt-dasqa
python -m pip install -e .
```

#### Installing Qiskit Metal

1. Install Qiskit Metal following installation instructions at [Qiskit Metal](https://qiskit.org/documentation/metal/installation.html). Refer to the [Pre-existing environment](https://qiskit.org/documentation/metal/installation.html#option-2-a-pre-existing-environment) section. Note that to run the pip install command **without** the `--no-deps` flag so that all dependencies are installed for Qiskit Metal.

### Usage

#### Command-line interface (CLI)

```text
Usage:
    dasqa --file-path [PATH_TO_QASM_2.0_FILE] --config-file-path [PATH_TO_CONFIG_FILE]
```

The CLI will generate the high-level architecture of the placement of qubits in a 2D square-lattice and the corresponding qubit frequencies. The Metal GUI is invoked at the end as following where there is an option to save the design as a Python script.

![4_qubit_2D_square_lattice](docs/images/4_qubit_2D_square_lattice.png)

#### Testing the Package

1. There is a test circuit that could be used to test the package. Navigate to `dasqa` directory and execute `dasqa --file-path ./src/tests/test_circuit/circuit1.qasm --config-file-path ./src/tests/test_config/config.yml`

### Development

1. On top of normal installation, install development dependencies using `pip install -r requirements-dev.txt`

### FAQs

- QT Warnings

>From [Qiskit Metal FAQ](https://qiskit.org/documentation/metal/faq.html):
>
>Q: Why am I seeing a critical error from qt about not controlling layer-backing?
>
>A: If you are seeing: CRITICAL [_qt_message_handler]: …. WARNING: Layer-backing can not be explicitly controlled on 10.14 when built against the 10.14 SDK … you are likely running a MAC OS version that has trouble with the libraries. Based on information that is available online, this problem does not appear to have a solution. However, it does not seem like this error affects Qiskit Metal’s functionality. If you find problem with this, you might want to try using an older version of the dependency packages, beginning with lowering your python version to 3.7.x.
