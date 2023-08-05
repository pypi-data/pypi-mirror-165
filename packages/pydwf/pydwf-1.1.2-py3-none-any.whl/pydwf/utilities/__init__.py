"""The |pydwf.utilities| package provides utility functions for managing Digilent Waveforms devices.

It provides high-level functions that reflect best-practice implementations for common use-cases of |pydwf|.

Currently, it only provides a single function, but several more are expected in the future.
"""

# Make the openDwfDevice function directly available from the pydwf.utilities package.
from pydwf.utilities.open_dwf_device import openDwfDevice
