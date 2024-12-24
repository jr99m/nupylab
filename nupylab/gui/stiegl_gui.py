"""
GUI for Stiegl reactor setup.

This GUI connects to and displays data from
    * Bronkhorst MFC Controller
    * Eurotherm 2416 Furnace Controller

Run the program by changing to the directory containing this file and calling:

python s4_gui.py
"""

import sys
from typing import Dict, List

# Instrument Imports #
from nupylab.instruments.heater.eurotherm2400 import Eurotherm2400 as Heater
from nupylab.instruments.mfc.bronkhorst_mfc import BronkhorstMFC as MFC
######################
from nupylab.utilities import list_resources, nupylab_procedure, nupylab_window
from pymeasure.display.Qt import QtWidgets
from pymeasure.experiment import (
    BooleanParameter,
    FloatParameter,
    IntegerParameter,
    ListParameter,
    Parameter,
)


class StieglProcedure(nupylab_procedure.NupylabProcedure):
    """Procedure for running experiments on flow reactor setups Stiegl and Ottakring.

    Running this procedure calls startup, execute, and shutdown methods sequentially.
    In addition to the parameters listed below, this procedure inherits `record_time`,
    `num_steps`, and `current_steps` from parent class.
    """

    # Units in parentheses must be valid pint units
    # First two entries must be "System Time" and "Time (s)"
    DATA_COLUMNS: List[str] = [
        "System Time",
        "Time (s)",
        "Furnace Temperature (degC)",
        "MFC H2 Flow (cc/min)",
        "MFC O2 Flow (cc/min)",
        "MFC CO2 Flow (cc/min)",
        "MFC CO Flow (cc/min)",
        "MFC N2 Flow (cc/min)",
        "MFC CH4 Flow (cc/min)",
        "MFC Ar Flow (cc/min)",
    ]

    resources = list_resources()

    furnace_port = ListParameter("Eurotherm Port", choices=resources)
    furnace_address = IntegerParameter(
        "Eurotherm Address", minimum=1, maximum=254, step=1, default=1
    )
    mfc_port = ListParameter("Bronkhorst Port", choices=resources)

    target_temperature = FloatParameter("Target Temperature", units="C")
    ramp_rate = FloatParameter("Ramp Rate", units="C/min")
    dwell_time = FloatParameter("Dwell Time", units="min")
    mfc_H2_setpoint = FloatParameter("MFC H2 Setpoint", units="sccm")
    mfc_O2_setpoint = FloatParameter("MFC O2 Setpoint", units="sccm")
    mfc_CO2_setpoint = FloatParameter("MFC CO2 Setpoint", units="sccm")
    mfc_CO_setpoint = FloatParameter("MFC CO Setpoint", units="sccm")
    mfc_N2_setpoint = FloatParameter("MFC N2 Setpoint", units="sccm")
    mfc_CH4_setpoint = FloatParameter("MFC CH4 Setpoint", units="sccm")
    mfc_Ar_setpoint = FloatParameter("MFC Ar Setpoint", units="sccm")

    TABLE_PARAMETERS: Dict[str, str] = {
        "Target Temperature [C]": "target_temperature",
        "Ramp Rate [C/min]": "ramp_rate",
        "Dwell Time [min]": "dwell_time",
        "MFC H2 [sccm]": "mfc_H2_setpoint",
        "MFC O2 [sccm]": "mfc_O2_setpoint",
        "MFC CO2 [sccm]": "mfc_CO2_setpoint",
        "MFC CO [sccm]": "mfc_CO_setpoint",
        "MFC N2 [sccm]": "mfc_N2_setpoint",
        "MFC CH4 [sccm]": "mfc_CH4_setpoint",
        "MFC Ar [sccm]": "mfc_Ar_setpoint",

    }

    # Entries in axes must have matches in procedure DATA_COLUMNS.
    # Number of plots is determined by the longer of X_AXIS or Y_AXIS
    X_AXIS: List[str] = ["Time (s)"]
    Y_AXIS: List[str] = [
        "Furnace Temperature (degC)",
        "MFC H2 Flow (cc/min)",
        "MFC O2 Flow (cc/min)",
        "MFC CO2 Flow (cc/min)",
        "MFC CO Flow (cc/min)",
        "MFC N2 Flow (cc/min)",
        "MFC CH4 Flow (cc/min)",
        "MFC Ar Flow (cc/min)",
    ]


    # Inputs must match name of selected procedure parameters
    INPUTS: List[str] = [
        "record_time",
        "furnace_port",
        "furnace_address",
        "mfc_port",
    ]

    def set_instruments(self) -> None:
        """Set and configure instruments list.

        Pass in connections from previous step, if applicable, otherwise create new
        instances. Send current step parameters to appropriate instruments.

        It is required for this method to create non-empty `instruments` and
        `active_instruments` attributes.
        """
        if self.previous_procedure is not None:
            furnace, mfc, = self.previous_procedure.instruments
        else:
            furnace = Heater(
                self.furnace_port, self.furnace_address, "Furnace Temperature (degC)"
            )
            mfc = MFC(
                self.mfc_port,
                (
                    "H2",
                    "O2",
                    "CO2",
                    "CO",
                    "N2",
                    "CH4",
                    "Ar",
                ),
                (
                    "MFC H2 Flow (cc/min)",
                    "MFC O2 Flow (cc/min)",
                    "MFC CO2 Flow (cc/min)",
                    "MFC CO Flow (cc/min)",
                    "MFC N2 Flow (cc/min)",
                    "MFC CH4 Flow (cc/min)",
                    "MFC Ar Flow (cc/min)",
                ),
            )

        self.instruments = (furnace, mfc)
        self.active_instruments = [furnace, mfc]
        furnace.set_parameters(self.target_temperature, self.ramp_rate, self.dwell_time)
        mfc.set_parameters(
            (
                self.mfc_H2_setpoint,
                self.mfc_O2_setpoint,
                self.mfc_CO2_setpoint,
                self.mfc_CO_setpoint,
                self.mfc_N2_setpoint,
                self.mfc_CH4_setpoint,
                self.mfc_Ar_setpoint,
            )
        )


def main(*args):
    """Run S4 procedure."""
    app = QtWidgets.QApplication(*args)
    window = nupylab_window.NupylabWindow(StieglProcedure)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main(sys.argv)
