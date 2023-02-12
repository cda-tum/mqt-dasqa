# mqhad
Munich Quantum HArdware Designer

## Installation

1. Clone the repository - `git clone {URL}`

2. Change directory - `cd mqhad`

3. Install - `python -m pip install -e .`

4. Install Qiskit Metal following installation instructions at [Qiskit Metal](https://qiskit.org/documentation/metal/installation.html)

## Usage

1. For CLI - `mqhad --file-path {PATH_TO_QASM_2.0_FILE}`

## Development

1. Install required dependencies - `pip install -r requirements.txt`

2. Install dev dependencies - `pip install -r requirements-dev.txt`

## Experimental Feature

Explanation on YieldSimulator2 - Vectorized - Faster in large circuit - need tests to prove

## Future Improvements

1. Make random seed in YieldSimulator and YieldSimulator2 configurable for the user

2. Make it easy for user to configure which yield simulator they want to use

3. Experiment further speed up in YieldSimulator2. For instance, using JAX, jit, etc. The initial mask creation takes a bit time. Maybe the itertools.combinations can be improved; https://stackoverflow.com/a/16008578/1893470.

4. Currently Generator is expecting a Qiskit QuantumCircuit. This dependency can be removed to be more generic. Possibly, suppoting other libraries' circuits, i.e: Cirq, Q#, etc.

6. Add examples on how to use the package in another program

7. Increase test coverage, notably on edge cases. For instance, the designer module has a considerable amount of if-else statement which would be good to be tested.

8. Refactor Frequency class. Frequency class can be refactored to make the functions leaner and more testable.

9. Save output of Metal design as Python script using (DesignPlanar.to_python_script)[https://qiskit.org/documentation/metal/stubs/qiskit_metal.designs.DesignPlanar.to_python_script.html#qiskit_metal.designs.DesignPlanar.to_python_script]. Potentially, we don't need a GUI opened. If this is possible, then we can give an option to the user, to either open the GUI and/or generate a Python script containing their design.

10. The Design class is can be refactored to follow a creational pattern, i.e: Factory, AbstractFactory, Builder etc. The steps to construct a layout can be harmonized into a series of steps defined in an interface that can be implemented by different concrete implementation classes. The idea is to support various Metal designs and possibly other hardware designer backend seamlessly in the future.