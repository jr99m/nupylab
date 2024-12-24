"""Adapts Bronkhorst porpar driver (wrapper around propar python package) in FlowBus setup of Multiple MFCs to NUPylab instrument class for use with NUPyLab GUIs.

This is quick and dirty implementation for prototyping purposes and doesn't implement expose the full propar protocoll and its commands

"""

from __future__ import annotations

import propar
from typing import List, Optional, Sequence, TYPE_CHECKING, Union

from nupylab.utilities import DataTuple, NupylabError
from nupylab.utilities import nupylab_instrument
from nupylab.utilities.nupylab_instrument import NupylabInstrument 

from enum import IntEnum

class FlowBus(IntEnum):
    CAPACITY = 21
    CAPACITY_UNIT_INDEX = 23
    SETPOINT = 9
    FMEASURE = 205
    FSETPOINT = 206
    FLUIDNAME = 25

class BronkhorstMFC(NupylabInstrument):
    """Bronkhorst MFC instrument class. Abstracts Aera Bronkhorst driver for NUPyLab procedures.

    Attributes:
        data_label: labels for DataTuples.
        name: name of instrument.
        lock: thread lock for preventing simultaneous calls to instrument.
        propar: Propar driver class with channels for all connected MFCs.
    """
    def __init__(
        self,
        port: str,
        gas_label: Union[str, Sequence[str]],
        data_label: Union[str, Sequence[str]],
        name: str = "Bronkhorst MFC",
    ) -> None:
        """Initialize  data labels, name, and connection parameters.

        Args:
            port: string name of port, e.g. `ASRL1::INSTR`.
            gas_label: Names of Gases according to MFC.
            data_label: labels for DataTuples. :meth:`get_data` returns flow rate for
                each channel, and corresponding labels should match entries in
                DATA_COLUMNS of calling procedure class.
            name: name of instrument.

        Raises:
            ValueError if lengths of addresses, mfc_classes, and data_label
            do not match.
        """

        self.port = port
        self.name = name
        super().__init__(data_label, name)
        
        self.propar = None
        self.gas_label = gas_label


    def connect(self) ->None:
        """Connect to FlowBus."""
        with self.lock:
            self.propar

        mfcs = dict()
        for ch in range(255):
            mfc = propar.instrument(self.port, ch)
            fluid_name = mfc.readParameter(FlowBus.FLUIDNAME) # None if no device on channel
            if fluid_name is None: 
                continue

            fluid_name = fluid_name.strip()    
            mfcs[fluid_name] = mfc
            # log.info(f"Found '{fluid_name}' on channel '{ch}'")

        self.mfcs = [mfcs[gas] for gas in self.gas_label]
        self._connected = True
        self._ranges = [ins.readParameter(FlowBus.CAPACITY) for ins in mfcs]

    
    def set_parameters(self, setpoints: Sequence[float]) -> None:
        """Set Aera flow setpoints.

        Args:
            setpoints: MFC channel setpoints.

        Raises:
            ValueError if lengths of setpoints and data_label do not match.
        """
        err_msg = "Setpoints length must match length of data_label."
        if isinstance(setpoints, (float, int)) and not isinstance(
            self.data_label, str
        ):
            raise ValueError(err_msg)
        elif len(setpoints) != len(self.data_label):
            raise ValueError(err_msg)
        self._parameters = setpoints

    def start(self) -> None:
        """Convert setpoints from sccm to % and set flow.

        Raises:
            NupylabError if `start` method is called before `set_parameters`.
        """
        if self._parameters is None:
            raise NupylabError(
                f"`{self.__class__.__name__}` method `set_parameters` "
                "must be called before calling its `start` method."
            )

        setpoints = self._parameters
        with self.lock:
            for instrument, setpoint in zip(self.mfcs, setpoints):
                instrument.writeParameter(FlowBus.FSETPOINT, setpoint)
        

        self._parameters = None
    
    def get_data(self) -> List[DataTuple]:
        """Read flow for each MFC channel.

        Returns:
            DataTuples with flow for each channel.
        """
        flow_rates: List[float] = []
        with self.lock:
            for instrument, in self.mfcs:
                flow_rates.append(instrument.readParameter(FlowBus.FMEASURE))
        return list(
            DataTuple(label, flow_rate)
            for label, flow_rate in zip(self.data_label, flow_rates)
        )


    def stop_measurement(self) -> None:
        """Stop Bronkhorst MFC measurement. Not implemented."""
        pass
    
    def shutdown(self):
        for mfc in self.mfcs:
            mfc.writeParameter(FlowBus.FSETPOINT, 0)
    

