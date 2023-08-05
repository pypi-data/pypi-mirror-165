"""The |pydwf.core.api.digital_io| module implements a single class: |DigitalIO|."""

from pydwf.core.dwf_device_subapi import AbstractDwfDeviceSubApi

from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.constants import RESULT_SUCCESS


class DigitalIO(AbstractDwfDeviceSubApi):
    """The |DigitalIO| class provides access to the static digital I/O functionality of a |DwfDevice:link|.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfDevice| and subsequently assigned to its
        public |digitalIO:link| attribute for access by the user.

    The class implements 3 generic methods: :py:meth:`reset`, :py:meth:`configure`, and :py:meth:`status`,
    and 8 methods that come in both 32- and 64-bits variants, where 32 and 64 refer to the maximum number
    of digital pins that the methods can handle.
    """

    def reset(self) -> None:
        """Reset all |DigitalIO| settings to default values.

        It sets the digital pins to tri-state (high impedance, not enabled) and output value to zero.

        If auto-configure is enabled, the values are immediately applied.

        Raises:
            DwfLibraryError: An error occurred while executing the *reset* operation.
        """
        result = self.lib.FDwfDigitalIOReset(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def configure(self) -> None:
        """Configure the |DigitalIO| functionality.

        This method transfers the settings to the Digilent Waveforms device. It is not needed
        if auto-configure is enabled.

        Raises:
            DwfLibraryError: An error occurred while executing the *configure* operation.
        """
        result = self.lib.FDwfDigitalIOConfigure(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def status(self) -> None:
        """Read the |DigitalIO| status and input values from the device to the PC.

        The status inquiry methods that follow will return the information that was read from the device
        when this method was last called.

        Note that the |DigitalIO| functionality is not managed by a state machine,
        so this method does not return a value.

        Raises:
            DwfLibraryError: An error occurred while executing the *status* operation.
        """
        result = self.lib.FDwfDigitalIOStatus(self.hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def outputEnableInfo(self) -> int:
        """Get the digital pins that can be enabled for output as a bitmask.

        The *output enable state* of a pin determines if it is driven as an output.
        If not, it is in high impedance (also known as high Z) mode.

        Only digital pins that are used as outputs should be enabled; digital pins that are used as inputs
        should remain disabled (the default state after reset).

        This is the 32-bits version of this method. For the 64-bits version, see :py:meth:`outputEnableInfo64`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Returns:
            int: A bitmask of pins that can be used as outputs.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_output_enable_mask = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalIOOutputEnableInfo(self.hdwf, c_output_enable_mask)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_enable_mask = c_output_enable_mask.value
        return output_enable_mask

    def outputEnableSet(self, output_enable: int) -> None:
        """Set the digital pins that are enabled for output as a bitmask.

        The *output enable* state of a pin determines if it is driven as an output.
        If not, it is in high impedance (also known as high Z) mode.

        Only digital pins that are used as outputs should be enabled; digital pins that are used as inputs
        should remain disabled (the default state after reset).

        This is the 32-bits version of this method. For the 64-bits version, see :py:meth:`outputEnableSet64`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Parameters:
            output_enable (int): A bitmask of pins that will be used as outputs.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfDigitalIOOutputEnableSet(self.hdwf, output_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def outputEnableGet(self) -> int:
        """Get the digital pins that are enabled for output as a bitmask.

        The *output enable* state of a pin determines if it is driven as an output.
        If not, it is in high impedance (also known as high Z) mode.

        Only digital pins that are used as outputs should be enabled; digital pins that are used as inputs
        should remain disabled (the default state after reset).

        This is the 32-bits version of this method. For the 64-bits version, see :py:meth:`outputEnableGet64`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Returns:
            int: A bitmask of pins that are currently configured as outputs.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_output_enable = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalIOOutputEnableGet(self.hdwf, c_output_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_enable = c_output_enable.value
        return output_enable

    def outputInfo(self) -> int:
        """Get the digital pins that can be used as outputs, i.e., driven high or low, as a bitmask.

        This is the 32-bits version of this method. For the 64-bits version, see :py:meth:`outputInfo64`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Returns:
            int: A bitmask of pins that can be used as outputs.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_output_mask = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalIOOutputInfo(self.hdwf, c_output_mask)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_mask = c_output_mask.value
        return output_mask

    def outputSet(self, output: int) -> None:
        """Set the digital pins that are currently driven high as a bitmask.

        This is the 32-bits version of this method. For the 64-bits version, see :py:meth:`outputSet64`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Parameters:
            output (int): A bitmask of pins that will be driven high.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfDigitalIOOutputSet(self.hdwf, output)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def outputGet(self) -> int:
        """Get the digital pins that are currently driven high as a bitmask.

        This is the 32-bits version of this method. For the 64-bits version, see :py:meth:`outputGet64`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Returns:
            int: A bitmask of pins that are currently set to high.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_output = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalIOOutputGet(self.hdwf, c_output)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output = c_output.value
        return output

    def inputInfo(self) -> int:
        """Return the digital pins that can be used for input on the device as a bitmask.

        This is the 32-bits version of this method. For the 64-bits version, see :py:meth:`inputInfo64`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Returns:
            int: A bitmask of pins that can be used as inputs.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_input_mask = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalIOInputInfo(self.hdwf, c_input_mask)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        input_mask = c_input_mask.value
        return input_mask

    def inputStatus(self) -> int:
        """Return the current state of the digital input pins on the device as a bitmask.

        Before calling this method, call the :py:meth:`status` method to read the current digital input
        status from the device.

        This is the 32-bits version of this method. For the 64-bits version, see :py:meth:`inputStatus64`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Returns:
            int: A bitmask of pins that are currently read as high.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_input = typespec_ctypes.c_unsigned_int()
        result = self.lib.FDwfDigitalIOInputStatus(self.hdwf, c_input)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        input_ = c_input.value
        return input_

    def outputEnableInfo64(self) -> int:
        """Get the digital pins that can be enabled for output as a bitmask.

        The *output enable state* of a pin determines if it is driven as an output.
        If not, it is in high impedance (also known as high Z) mode.

        Only digital pins that are used as outputs should be enabled; digital pins that are used as inputs
        should remain disabled (the default state after reset).

        This is the 64-bits version of this method. For the 32-bits version, see :py:meth:`outputEnableInfo`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Returns:
            int: A bitmask of pins that can be used as outputs.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_output_enable_mask = typespec_ctypes.c_unsigned_long_long()
        result = self.lib.FDwfDigitalIOOutputEnableInfo64(self.hdwf, c_output_enable_mask)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_enable_mask = c_output_enable_mask.value
        return output_enable_mask

    def outputEnableSet64(self, output_enable: int) -> None:
        """Set the digital pins that are enabled for output as a bitmask.

        The *output enable* state of a pin determines if it is driven as an output.
        If not, it is in high impedance (also known as high Z) mode.

        Only digital pins that are used as outputs should be enabled; digital pins that are used as inputs
        should remain disabled (the default state after reset).

        This is the 64-bits version of this method. For the 32-bits version, see :py:meth:`outputEnableSet`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Parameters:
            output_enable (int): A bitmask of pins that will be used as outputs.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfDigitalIOOutputEnableSet64(self.hdwf, output_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def outputEnableGet64(self) -> int:
        """Get the digital pins that are enabled for output as a bitmask.

        The *output enable* state of a pin determines if it is driven as an output.
        If not, it is in high impedance (also known as high Z) mode.

        Only digital pins that are used as outputs should be enabled; digital pins that are used as inputs
        should remain disabled (the default state after reset).

        This is the 64-bits version of this method. For the 32-bits version, see :py:meth:`outputEnableGet`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Returns:
            int: A bitmask of pins that are currently configured as outputs.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_output_enable = typespec_ctypes.c_unsigned_long_long()
        result = self.lib.FDwfDigitalIOOutputEnableGet64(self.hdwf, c_output_enable)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_enable = c_output_enable.value
        return output_enable

    def outputInfo64(self) -> int:
        """Get the digital pins that can be used as outputs, i.e., driven high or low, as a bitmask.

        This is the 64-bits version of this method. For the 32-bits version, see :py:meth:`outputInfo`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Returns:
            int: A bitmask of pins that can be used as outputs.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_output_mask = typespec_ctypes.c_unsigned_long_long()
        result = self.lib.FDwfDigitalIOOutputInfo64(self.hdwf, c_output_mask)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output_mask = c_output_mask.value
        return output_mask

    def outputSet64(self, output: int) -> None:
        """Set the digital pins that are currently driven high as a bitmask.

        This is the 64-bits version of this method. For the 32-bits version, see :py:meth:`outputSet`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Parameters:
            output (int): A bitmask of pins that will be driven high.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        result = self.lib.FDwfDigitalIOOutputSet64(self.hdwf, output)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()

    def outputGet64(self) -> int:
        """Get the digital pins that are currently driven high as a bitmask.

        This is the 64-bits version of this method. For the 32-bits version, see :py:meth:`outputGet`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Returns:
            int: A bitmask of pins that are currently set to high.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_output = typespec_ctypes.c_unsigned_long_long()
        result = self.lib.FDwfDigitalIOOutputGet64(self.hdwf, c_output)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        output = c_output.value
        return output

    def inputInfo64(self) -> int:
        """Return the digital pins that can be used for input on the device as a bitmask.

        This is the 64-bits version of this method. For the 32-bits version, see :py:meth:`inputInfo`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Returns:
            int: A bitmask of pins that can be used as inputs.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_input_mask = typespec_ctypes.c_unsigned_long_long()
        result = self.lib.FDwfDigitalIOInputInfo64(self.hdwf, c_input_mask)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        input_mask = c_input_mask.value
        return input_mask

    def inputStatus64(self) -> int:
        """Return the current state of the digital input pins on the device as a bitmask.

        Before calling this method, call the :py:meth:`status` method to read the current digital input
        status from the device.

        This is the 64-bits version of this method. For the 32-bits version, see :py:meth:`inputStatus`.
        The 32 and 64 bits refer here to the maximum number of digital pins that the methods can handle.

        Returns:
            int: A bitmask of pins that are currently read as high.

        Raises:
            DwfLibraryError: An error occurred while executing the operation.
        """
        c_input = typespec_ctypes.c_unsigned_long_long()
        result = self.lib.FDwfDigitalIOInputStatus64(self.hdwf, c_input)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        input_ = c_input.value
        return input_
