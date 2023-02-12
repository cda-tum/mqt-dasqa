from collections import OrderedDict
from mqhad.designer.qubit_connection.metal import RouteMeanderConnector
from qiskit_metal.designs import DesignPlanar
import numpy as np


class TestRouteMeanderConnector:
    # TODO: The design needs to have qubits in it. How to do in modular way?
    def test_generate_qubit_connection(self):
        pass

    def test_get_upward_connection_configuration(self):
        route_connector = RouteMeanderConnector()
        assert route_connector._get_upward_connection_configuration(4, 4) == (
            "B0",
            "B2",
            "700um",
        )
        assert route_connector._get_upward_connection_configuration(4, 3) == (
            "B1",
            "B3",
            "-700um",
        )
        assert route_connector._get_upward_connection_configuration(3, 4) == (
            "B1",
            "B3",
            "-700um",
        )
        assert route_connector._get_upward_connection_configuration(3, 3) == (
            "B0",
            "B2",
            "700um",
        )

    def test_sideway_connection_configuration(self):
        route_connector = RouteMeanderConnector()
        assert route_connector._get_sideway_connection_configuration(0, 2) == (
            "B1",
            "B0",
            OrderedDict({0: ["R", "150um"]}),
        )
        assert route_connector._get_sideway_connection_configuration(1, 2) == (
            "B3",
            "B2",
            OrderedDict(),
        )
        assert route_connector._get_sideway_connection_configuration(0, 3) == (
            "B3",
            "B2",
            OrderedDict(),
        )
        assert route_connector._get_sideway_connection_configuration(1, 3) == (
            "B1",
            "B0",
            OrderedDict({0: ["R", "150um"]}),
        )

    def test_find_resonator_length(self):
        pass
