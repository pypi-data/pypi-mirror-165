"""This module defines Python equivalents of the enumerations found in the C library header file *dwf.h*.

Note:
    The obsolete enumerations *TRIGCOND* and *STS* that are defined in the C header file have not been defined here.
    *TRIGCOND* has been replaced by |DwfTriggerSlope:link|; *STS* has been replaced by |DwfState:link|.
"""

import enum


class _FixReprMethod:
    """Mixin class that overrides the __repr__ methods for Enum classes.

    Enums in Python have a strange default '__repr__' implementation. This mixin class fixes that.
    """

    # pylint: disable=no-member, too-few-public-methods

    def __repr__(self):
        return "{}.{}".format(self.__class__.__name__, self.name)


@enum.unique
class DwfErrorCode(_FixReprMethod, enum.Enum):
    """Enumeration type for error reporting constants of the DWF API.

    This type is used by the |DwfLibrary.getLastError:link| method to report the error condition of the most
    recent C API call.

    In |pydwf|, it is only used as the type of the :py:attr:`~pydwf.core.auxiliary.exceptions.DwfLibraryError.code`
    field of |DwfLibraryError:link| instances.

    In the C API, this type is called 'DWFERC', and it is represented as an *int*.
    """

    NoErc = 0
    """No error occurred."""

    UnknownError = 1
    """Unknown error."""

    ApiLockTimeout = 2
    """API waiting on pending operation timed out."""

    AlreadyOpened = 3
    """Device already opened."""

    NotSupported = 4
    """Device not supported."""

    InvalidParameter0 = 0x10
    """Invalid parameter sent in API call."""

    InvalidParameter1 = 0x11
    """Invalid parameter sent in API call."""

    InvalidParameter2 = 0x12
    """Invalid parameter sent in API call."""

    InvalidParameter3 = 0x13
    """Invalid parameter sent in API call."""

    InvalidParameter4 = 0x14
    """Invalid parameter sent in API call."""


class DwfEnumFilter(_FixReprMethod, enum.Flag):
    """Enumeration type for device class constants, used during device enumeration.

    This type is used by the |DeviceEnum.enumerateDevices:link| method to constrain
    the type of devices that will be considered during device enumeration.

    In the C API, this type is called 'ENUMFILTER', and it is represented as an *int*.
    """

    All = 0
    """Enumerate all available devices."""

    Type = 0x80000000
    """Enumerate by type (0x80000000)."""

    USB = 0x00000001
    """Enumerate USB devices."""

    Network = 0x00000002
    """Enumerate Network devices."""

    AXI = 0x00000004
    """Enumerate AXI devices (used when running on an ADP 3x50 device)."""

    Remote   = 0x10000000
    """Enumerate remote devices (0x10000000)."""

    Audio = 0x20000000
    """Enumerate audio devices (0x20000000)."""

    Demo = 0x40000000
    """Enumerate demo devices (0x40000000)."""

    EExplorer = 1
    """Enumerate only Electronics Explorer devices. Deprecated since DWF version 3.17."""

    Discovery = 2
    """Enumerate only Analog Discovery devices. Deprecated since DWF version 3.17."""

    Discovery2 = 3
    """Enumerate only Analog Discovery 2 devices. Deprecated since DWF version 3.17."""

    DDiscovery = 4
    """Enumerate only Digital Discovery devices. Deprecated since DWF version 3.17."""


@enum.unique
class DwfEnumConfigInfo(_FixReprMethod, enum.Enum):
    """Enumeration type for device configuration parameter type constants.

    This type lists the device parameters that can vary between different |device configurations:link|
    of the same device.

    In the C API, this type is represented as an *int*.
    """

    #pylint: disable=line-too-long

    TooltipText = -1
    """Tooltip text.

    Maximum length: 2048 characters.

    Note:
        This value is not officially documented. Its existence was revealed in a
        `message on the Digilent forum <https://forum.digilentinc.com/topic/21720-small-issue-and-questions-about-device-configurations/#comment-62717>`_.
    """

    OtherInfoText = -2
    """Other info text.

    Maximum length: 256 characters.

    Note:
        This value is not officially documented. Its existence was revealed in a
        `message on the Digilent forum <https://forum.digilentinc.com/topic/21720-small-issue-and-questions-about-device-configurations/#comment-62717>`_.
    """

    AnalogInChannelCount = 1
    """Number of analog input channels."""

    AnalogOutChannelCount = 2
    """Number of analog output channels."""

    AnalogIOChannelCount = 3
    """Number of analog power supply channels.

    Note:
        This is a different number than the number of channels reported by the |AnalogIO.channelCount:link|
        method.
    """

    DigitalInChannelCount = 4
    """Number of digital input channels."""

    DigitalOutChannelCount = 5
    """Number of digital output channels."""

    DigitalIOChannelCount = 6
    """Number of digital I/O channels."""

    AnalogInBufferSize = 7
    """Analog in buffer size, in samples."""

    AnalogOutBufferSize = 8
    """Analog out buffer size, in samples."""

    DigitalInBufferSize = 9
    """Digital in buffer size, in samples."""

    DigitalOutBufferSize = 10
    """Digital out buffer size, in samples."""


@enum.unique
class DwfDeviceID(_FixReprMethod, enum.Enum):
    """Enumeration type for device ID constants.

    This type is used by the |DeviceEnum.deviceType:link| method to report on a selected device.

    In the C API, this type is called 'DEVID', and it is represented as an *int*.
    """

    EExplorer = 1
    """Electronics Explorer devices."""

    Discovery = 2
    """Analog Discovery devices."""

    Discovery2 = 3
    """Analog Discovery 2 devices."""

    DDiscovery = 4
    """Digital Discovery devices."""

    ADP3X50 = 6
    """Analog Discovery Pro devices."""


class DwfDeviceVersion(_FixReprMethod, enum.Enum):
    """Enumeration type for device version (i.e., hardware revision) constants.

    This type is used by the |DeviceEnum.deviceType:link| method to report the
    hardware revision of a selected device.

    Note:
        The device revision list given here is not complete; it does not cover all devices.

        Additionally, the enumeration values :py:attr:`EExplorerC` and :py:attr:`DiscoveryB`
        have identical integer values (2).

    In the C API, this type is called 'DEVVER', and it is represented as an *int*.
    """

    EExplorerC = 2
    """Electronics Explorer devices, revision C."""
    EExplorerE = 4
    """Electronics Explorer devices, revision E."""
    EExplorerF = 5
    """Electronics Explorer devices, revision F."""
    DiscoveryA = 1
    """Discovery devices, revision A."""
    DiscoveryB = 2
    """Discovery devices, revision B."""
    DiscoveryC = 3
    """Discovery devices, revision C."""


@enum.unique
class DwfDeviceParameter(_FixReprMethod, enum.Enum):
    """Enumeration type for device parameter constants.

    Device parameters are miscellaneous integer settings that influence the behavior of a device.

    The different device parameters are selected by one of the constant values defined here.

    This type is used to select device parameters, either to set/get global defaults using the |DwfLibrary|, or to
    to set/get parameter values on a specific, previously opened device |DwfDevice|.

    In the C API, this type is called 'DwfParam', and it is represented as an *int*.
    """

    KeepOnClose = 1
    """Keep the device running after close.

    Warning:

        This value is *obsolete*. Use *OnClose* instead.
    """

    UsbPower = 2
    """USB power behavior if AUX power is connected.

    Possible values:

    * 0 — Disable USB power.
    * 1 — Keep USB power enabled.

    This setting is implemented on the Analog Discovery 2.
    """

    LedBrightness = 3
    """Set multicolor LED brightness.

    The Digital Discovery features a multi-color LED. It is normally blue in case the device is not
    currently controlled by software, or green if it is.

    Setting this parameter from 0 to 100 changes the LED's relative brightness, in percents. This can be
    useful, for example, in a lab with sensitive optics that would preferably be completely dark.

    On the Analog Discovery 2, this setting has no effect.
    """

    OnClose = 4
    """Define behavior on close.

    Possible values:

    * 0 — On close, continue.
    * 1 — On close, stop the device.
    * 2 — On close, shut down the device.
    """

    AudioOut = 5
    """Enable or disable audio output.

    Possible values:

    * 0 — Disable audio output.
    * 1 — Enable audio output.

    This setting is implemented on the Analog Discovery and the Analog Discovery 2.
    """

    UsbLimit = 6
    """USB power limit.

    The value ranges from 0 to 1000, in mA. The value -1 denotes no limit.

    This setting is implemented on the Analog Discovery and the Analog Discovery 2.
    """

    AnalogOut = 7
    """Enable or disable analog output.

    Possible values:

    * 0 — Disable analog output.
    * 1 — Enable analog output.
    """

    Frequency = 8
    """This parameter is undocumented.

    Todo:
        The meaning of this parameter needs to be understood.

        It is some frequency; comments say unit is Hz.
    """

    ExtFreq = 9
    """This parameter is undocumented.

    Todo:
        The meaning of this parameter needs to be understood.

        It is some frequency; comments say unit is Hz.
    """

    ClockMode = 10
    """This parameter is undocumented.

    Todo:
        The meaning of this parameter needs to be understood.

    Possible values:

    * 0 — internal.
    * 1 — output.
    * 2 — input.
    * 3 — IO.
    """


class DwfState(_FixReprMethod, enum.Enum):
    """Enumeration type for instrument state constants, for instruments that are controlled by an internal
    state-machine.

    The following instrument APIs are controlled by a state machine:

    * |AnalogIn|
    * |AnalogOut| — *independent state machine for each channel*
    * |DigitalIn|
    * |DigitalOut|
    * |AnalogImpedance|

    This type is used to return the current state from their *status()* methods.

    Note:
        The enumeration values :py:attr:`Triggered` and :py:attr:`Running` have identical integer values (3).

        The state name :py:attr:`Triggered` is used for capture instruments (|AnalogIn|, |DigitalIn|),
        while :py:attr:`Running` is used for signal generation instruments (|AnalogOut|, |DigitalOut|).

    In the C API, this type is represented as an *unsigned char*.
    """

    Ready = 0
    """The instrument is idle, waiting to be configured or started."""

    Config = 4
    """The instrument is being configured."""

    Prefill = 5
    """The instrument is collecting data prior to arming itself, so it can deliver pre-trigger samples."""

    Armed = 1
    """The instrument is collecting samples and waiting for the trigger."""

    Wait = 7
    """The signal generation instrument is waiting before its next run."""

    Triggered = 3
    """The capture instrument is triggered and collecting data."""

    Running = 3
    """The signal generation instrument is running (generating signals)."""

    Done = 2
    """The instrument has completed a measurement or signal-generating sequence."""


@enum.unique
class DwfTriggerSource(_FixReprMethod, enum.Enum):
    """Enumeration type for trigger source constants.

    This type is used by the |DeviceControl| functionality and by the |AnalogIn|, |AnalogOut|, |DigitalIn|,
    and |DigitalOut| instruments.

    In the C API, this type is called 'TRIGSRC', and it is represented as an *unsigned char*.
    """

    None_ = 0
    """No trigger configured (device starts immediately)."""

    PC = 1
    """PC (software) trigger."""

    DetectorAnalogIn  = 2
    """AnalogIn trigger detector."""

    DetectorDigitalIn = 3
    """DigitalIn trigger detector."""

    AnalogIn = 4
    """AnalogIn instrument start."""

    DigitalIn = 5
    """DigitalIn instrument start."""

    DigitalOut = 6
    """DigitalOut instrument start."""

    AnalogOut1 = 7
    """|AnalogOut| instrument channel 1 start."""

    AnalogOut2 = 8
    """|AnalogOut| instrument channel 2 start."""

    AnalogOut3 = 9
    """|AnalogOut| instrument channel 3 start."""

    AnalogOut4 = 10
    """|AnalogOut| instrument channel 4 start."""

    External1 = 11
    """External trigger #1."""

    External2 = 12
    """External trigger #2."""

    External3 = 13
    """External trigger #3."""

    External4 = 14
    """External trigger #4."""

    High = 15
    """High (undocumented)."""

    Low = 16
    """Low (undocumented)."""

    Clock = 17
    """Clock (undocumented)."""

@enum.unique
class DwfTriggerSlope(_FixReprMethod, enum.Enum):
    """Enumeration type for trigger slope constants.

    This type is used by the |AnalogIn|, |AnalogOut|, |DigitalIn|, and |DigitalOut| instruments to select
    the trigger slope.

    In addition, the |AnalogIn| instrument uses it to select the slope of the sampling clock.

    In the C API, this type is represented as an *int*.
    """

    Rise = 0
    """Rising trigger slope."""

    Fall = 1
    """Falling trigger slope."""

    Either = 2
    """Either rising or falling trigger slope."""


@enum.unique
class DwfAcquisitionMode(_FixReprMethod, enum.Enum):
    """Enumeration type for acquisition mode constants.

    This type is used by the |AnalogIn| and |DigitalIn| instruments. These instruments
    support multiple acquisition modes that are appropriate for different data
    acquisition tasks.

    In the C API, this type is called 'ACQMODE', and it is represented as an *int*.
    """

    Single = 0
    """Perform a single buffer acquisition.

    Re-arm the instrument for the next capture after the data is fetched to the host
    using the instrument-specific *Status()* method.

    Note:
        The difference with the :py:attr:`Single1` mode is unclear.
    """

    ScanShift = 1
    """Perform a continuous acquisition in FIFO style.

    The trigger setting is ignored.

    The last sample is at the end of the buffer.
    The instrument's *statusSamplesValid()* method gives the number of the acquired samples,
    which will increase until reaching the buffer size.
    After that, the waveform image is shifted for every new sample.
    """

    ScanScreen = 2
    """Perform continuous acquisition circularly writing samples into the buffer.

    This is similar to a heart-monitor display.

    The trigger setting is ignored.

    The instrument's *statusIndexWrite()* method gives the buffer write position.
    """

    Record = 3
    """Perform acquisition for the length of time set by the instrument's *recordLengthSet()* method."""

    Overs = 4
    """Overscan mode (undocumented)."""

    Single1 = 5
    """Perform a single buffer acquisition.

    Note:
        The difference with the :py:attr:`Single` mode is unclear.
    """


@enum.unique
class DwfAnalogInFilter(_FixReprMethod, enum.Enum):
    """Enumeration type for analog input filter constants.

    This type is used by the |AnalogIn| instrument to select a filtering algorithm for the input and trigger channels.

    The |AnalogIn| instrument's ADC always captures samples at the maximum possible rate. If data acquisition at
    a lower sampling rate is requested, the resampling can be handled it several different ways.

    The most obvious choice is *averaging*. This will suppress high-frequency noise, which is often a good thing,
    but often it is also desirable to know that high-frequency noise is present in the signal, and the averaging
    may hide that fact.

    For that reason, the *decimation* filter is available, which simply selects a single sample captured at high
    frequency when resampling to a lower frequency. The signal-to-noise ratio (SNR) will suffer, but the presence
    of high-frequency noise (outliers) will be more easily seen in the resampled data.

    Todo:
        Examine the MinMax filter choice; it is not currently understood.

    In the C API, this type is called 'FILTER', and it is represented as an *int*.
    """

    Decimate = 0
    """Decimation filter."""

    Average = 1
    """Averaging filter."""

    MinMax = 2
    """Min/max filter."""


@enum.unique
class DwfAnalogInTriggerType(_FixReprMethod, enum.Enum):
    """Enumeration type for analog input trigger mode constants.

    This type is used by the |AnalogIn| instrument to specify the trigger type.

    In the C API, this type is called 'TRIGTYPE', and it is represented as an *int*.
    """

    Edge = 0
    """Edge trigger type."""

    Pulse = 1
    """Pulse trigger type."""

    Transition = 2
    """Transition trigger type."""

    Window = 3
    """Window trigger type."""


@enum.unique
class DwfAnalogInTriggerLengthCondition(_FixReprMethod, enum.Enum):
    """Enumeration type for analog input trigger length condition constants.

    This type is used by the |AnalogIn| instrument to specify the trigger length condition.

    In the C API, this type is called 'TRIGLEN', and it is represented as an *int*.
    """

    Less = 0
    """Trigger length condition 'less'."""

    Timeout = 1
    """Trigger length condition 'timeout'."""

    More = 2
    """Trigger length condition 'more'."""


@enum.unique
class DwfAnalogOutFunction(_FixReprMethod, enum.Enum):
    """Enumeration type for analog output waveform-shape function constants.

    This type is used by the |AnalogOut| instrument to represent the wave-shape produced on an
    analog output channel node. The nine fixed waveform shape options are shown below.

    .. only:: html

        .. image:: /images/waveforms.gif

    .. only:: latex

        .. image:: /images/waveforms.pdf

    In the C API, this type is called 'FUNC', and it is represented as an *unsigned char*.
    """

    DC = 0
    """DC (constant signal) waveform shape. The signal level varies between -1 and 1."""

    Sine = 1
    """Sinusoid waveform shape. The signal level varies between -1 and 1."""

    Square = 2
    """Square waveform shape. The signal level varies between -1 and 1."""

    Triangle = 3
    """Triangle waveform shape. The signal level varies between -1 and 1."""

    RampUp = 4
    """Ramp Up waveform shape. The signal level varies between -1 and 1."""

    RampDown = 5
    """Ramp Down waveform shape. The signal level varies between -1 and 1."""

    Noise = 6
    """Noise waveform shape. The signal level is uniformly distributed between -1 and 1."""

    Pulse = 7
    """Pulse waveform shape. The signal level varies between 0 and 1."""

    Trapezium = 8
    """Trapezium waveform shape. The signal level varies between -1 and 1."""

    SinePower = 9
    """Sinusoid Power waveform shape. The signal level varies between -1 and 1."""

    Custom = 30
    """Custom (user-defined) waveform shape. The signal level varies between -1 and 1."""

    Play = 31
    """Continuous playback mode. The signal level varies between -1 and 1."""


@enum.unique
class DwfAnalogOutNode(_FixReprMethod, enum.Enum):
    """Enumeration type for analog output node type constants.

    This type is used by the |AnalogOut| instrument to represent the node types associated with each output channel.

    In the C API, this type is called 'AnalogOutNode' (without the *Dwf* prefix), and it is represented as an *int*.
    """

    Carrier = 0
    """Carrier signal node. This node represents the base signal without modulation applied."""

    FM = 1
    """Frequency Modulation node."""

    AM = 2
    """Amplitude Modulation node."""


@enum.unique
class DwfAnalogOutMode(_FixReprMethod, enum.Enum):
    """Enumeration type for analog out mode constants (voltage or current).

    This type is used by the |AnalogOut| instrument to set or retrieve the mode of a channel.

    In the C API, this type is represented as an *int*.
    """

    Voltage = 0
    """Voltage mode."""

    Current = 1
    """Current mode."""


@enum.unique
class DwfAnalogOutIdle(_FixReprMethod, enum.Enum):
    """Enumeration type for analog output idle state constants.

    This type is used by the |AnalogOut| instrument to set the idle behavior of an output channel.

    In the C API, this type is represented as an *int*.
    """

    Disable = 0
    """When idle, disable the output."""

    Offset = 1
    """When idle, drive the analog output offset."""

    Initial = 2
    """When idle, drive the initial value of the selected waveform shape."""


@enum.unique
class DwfDigitalInClockSource(_FixReprMethod, enum.Enum):
    """Enumeration type for digital input clock source constants.

    This type is used by the |DigitalIn| instrument to specify a clock source.

    In the C API, this type is represented as an *int*.
    """

    Internal = 0
    """Use internal clock source."""

    External = 1
    """Use external clock source."""

    External2 = 2
    """Use alternate external clock source."""


@enum.unique
class DwfDigitalInSampleMode(_FixReprMethod, enum.Enum):
    """Enumeration type for digital input sample mode constants.

    This type is used by the |DigitalIn| instrument to specify a sample mode.

    In the C API, this type is represented as an *int*.
    """

    Simple = 0
    """Only digital samples (no noise)."""

    Noise = 1
    """Alternate samples (noise, sample, noise, sample, …) where noise is more than one transition between two samples.

    This setting is available when the sample rate is less than the maximum clock frequency (i.e., the divider is
    greater than one). Digital noise can indicate glitches or ringing.
    """


@enum.unique
class DwfDigitalOutOutput(_FixReprMethod, enum.Enum):
    """Enumeration type for digital output mode constants.

    This type is used by the |DigitalOut| instrument to specify the electronic behavior of a digital output channel.

    In the C API, this type is represented as an *int*.
    """

    PushPull = 0
    """Push/Pull."""

    OpenDrain = 1
    """Open Drain."""

    OpenSource = 2
    """Open Source."""

    ThreeState = 3
    """Tristate (for custom and random)."""


@enum.unique
class DwfDigitalOutType(_FixReprMethod, enum.Enum):
    """Enumeration type for digital output type constants.

    This type is used by the |DigitalOut| instrument to specify the behavior mode of a digital output channel.

    In the C API, this type is represented as an *int*.
    """

    Pulse = 0
    """Pulse output."""

    Custom = 1
    """Custom output."""

    Random = 2
    """Random output."""

    ROM = 3
    """ROM (lookup table) output."""

    State = 4
    """State machine output."""

    Play = 5
    """Continuous playback output."""


@enum.unique
class DwfDigitalOutIdle(_FixReprMethod, enum.Enum):
    """Enumeration type for digital output idle mode constants.

    This type is used primarily by the |DigitalOut| instrument to specify the idle behavior mode of a digital
    output channel.

    In addition to that, it is used by the |DigitalSpi| protocol functionality to specify the idle behavior
    of the pins it controls.

    In the C API, this type is represented as an *int*.
    """

    Init = 0
    """Same as initial value of selected output pattern."""

    Low  = 1
    """Low signal level."""

    High = 2
    """High signal level."""

    Zet  = 3
    """High impedance."""


@enum.unique
class DwfAnalogIO(_FixReprMethod, enum.Enum):
    """Enumeration type for Analog I/O channel node type constants.

    This type is used by the |AnalogIO| functionality to report the node type.

    In the C API, this type is called 'ANALOGIO', and it is represented as an *unsigned char*.
    """

    Undocumented = 0
    """This value is returned in Analog Pro devices when using 3.16.3 of the DWF library. That is probably a bug."""

    Enable = 1
    """The node represent an on/off switch."""

    Voltage = 2
    """The node represents a voltage."""

    Current = 3
    """The node represents a current."""

    Power = 4
    """The node represents a power."""

    Temperature = 5
    """The node represents a temperature."""

    Dmm = 6
    """The node represents a DMM (digital multimeter) value."""

    Range = 7
    """The node represents a range."""

    Measure = 8
    """(unknown)"""

    Time = 9
    """The node represents a time."""

    Frequency = 10
    """The node represents a frequency."""

    Resistance = 11
    """The node represents a resistance."""


@enum.unique
class DwfAnalogImpedance(_FixReprMethod, enum.Enum):
    """Enumeration type for analog impedance measurement types.

    This type is used by the |AnalogImpedance| measurement functionality to specify a measurement quantity type.

    In the C API, this type is represented as an *int*.
    """

    Impedance = 0
    """Measure impedance, in Ohms."""

    ImpedancePhase = 1
    """Measure impedance phase, in radians."""

    Resistance = 2
    """Measure resistance, in Ohms."""

    Reactance = 3
    """Measure reactance, in Ohms."""

    Admittance = 4
    """Measure admittance, in Siemens."""

    AdmittancePhase = 5
    """Measure admittance phase, in radians."""

    Conductance = 6
    """Measure conductance, in Siemens."""

    Susceptance = 7
    """Measure susceptance, in Siemens."""

    SeriesCapacitance = 8
    """Measure series capacitance, in Farad."""

    ParallelCapacitance = 9
    """Measure parallel capacitance, in Farad."""

    SeriesInductance = 10
    """Measure series inductance, in Henry."""

    ParallelInductance = 11
    """Measure parallel inductance, in Henry."""

    Dissipation = 12
    """Measure dissipation, as a factor."""

    Quality = 13
    """Measure quality, as a factor."""

    Vrms = 14
    """Measure Vrms, in Volts."""

    Vreal = 15
    """Measure Vreal (real part of complex voltage), in Volts."""

    Vimag = 16
    """Measure Vimag (imaginary part of complex voltage), in Volts."""

    Irms = 17
    """Measure Irms, in Amps."""

    Ireal = 18
    """Measure Ireal (real part of complex current), in Amps."""

    Iimag = 19
    """Measure Iimag (imaginary part of complex current), in Amps."""


@enum.unique
class DwfDmm(_FixReprMethod, enum.Enum):
    """Enumeration type for DMM (digital multimeter) measurements.

    Note:

        This type is currently unused in the API. It is intended for functionality in the new ADP5250 device.

    In the C API, this type is called 'DwfDmm', and it is represented as an *int*.
    """

    Resistance = 1
    """Resistance measurement."""

    Continuity = 2
    """Continuity measurement."""

    Diode = 3
    """Diode measurement."""

    DCVoltage = 4
    """DC voltage measurement."""

    ACVoltage = 5
    """AC voltage measurement."""

    DCCurrent = 6
    """DC current measurement."""

    ACCurrent = 7
    """AC current measurement."""

    DCLowCurrent = 8
    """DC low current measurement."""

    ACLowCurrent = 9
    """AC low current measurement."""

    Temperature = 10
    """Temperature measurement."""
