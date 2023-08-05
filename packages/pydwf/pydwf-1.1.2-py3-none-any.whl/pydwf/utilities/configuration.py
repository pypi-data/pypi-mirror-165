"""This module provides convenience functions for configuration of instruments, channels, and nodes.

Note:
    This is a preview of the configuration API. It is not complete, has not fully stabilized yet, and it may change
    in future releases of |pydwf|. Currently, only the |AnalogOut| and |AnalogIn| instruments are supported.

    Future releases of |pydwf| will add support for more instruments.
"""

from typing import Optional

import numpy as np

from pydwf.core.api.analog_in import AnalogIn
from pydwf.core.api.analog_out import AnalogOut

from pydwf.core.auxiliary.enum_types import (DwfAnalogInFilter, DwfTriggerSource, DwfTriggerSlope,
                                             DwfAnalogInTriggerType, DwfAnalogInTriggerLengthCondition,
                                             DwfAcquisitionMode, DwfAnalogOutMode, DwfAnalogOutIdle, DwfAnalogOutNode,
                                             DwfAnalogOutFunction)

########################################################################################################################
##                                                                                                                    ##
##                          Configuration support for the AnalogIn instrument and its channels                        ##
##                                                                                                                    ##
########################################################################################################################

def configure_analog_in_instrument(
        analog_in                         : AnalogIn,
        acquisition_mode                  : Optional[DwfAcquisitionMode],
        sample_frequency                  : Optional[float]=None,
        buffer_size                       : Optional[int]=None,
        noise_buffer_size                 : Optional[int]=None,
        record_duration                   : Optional[float]=None,
        trigger_source                    : Optional[DwfTriggerSource]=None,
        trigger_position                  : Optional[float]=None,
        trigger_auto_timeout              : Optional[float]=None,
        trigger_detector_holdoff          : Optional[float]=None,
        trigger_detector_type             : Optional[DwfAnalogInTriggerType]=None,
        trigger_detector_channel          : Optional[int]=None,
        trigger_detector_filter           : Optional[DwfAnalogInFilter]=None,
        trigger_detector_level            : Optional[float]=None,
        trigger_detector_hysteresis       : Optional[float]=None,
        trigger_detector_condition        : Optional[DwfTriggerSlope]=None,
        trigger_detector_length           : Optional[float]=None,
        trigger_detector_length_condition : Optional[DwfAnalogInTriggerLengthCondition]=None,
        sampling_source                   : Optional[DwfTriggerSource]=None,
        sampling_slope                    : Optional[DwfTriggerSlope]=None,
        sampling_delay                    : Optional[float]=None) -> None:

    """Configure analog-input instrument acquisition, triggering, and sampling settings."""

    # pylint: disable=too-many-locals, too-many-branches

    if acquisition_mode is not None:
        analog_in.acquisitionModeSet(acquisition_mode)

    if sample_frequency is not None:
        analog_in.frequencySet(sample_frequency)

    if buffer_size is not None:
        analog_in.bufferSizeSet(buffer_size)

    if noise_buffer_size is not None:
        analog_in.noiseSizeSet(noise_buffer_size)

    if record_duration is not None:
        analog_in.recordLengthSet(record_duration)

    if trigger_source is not None:
        analog_in.triggerSourceSet(trigger_source)

    if trigger_position is not None:
        analog_in.triggerPositionSet(trigger_position)

    if trigger_auto_timeout is not None:
        analog_in.triggerAutoTimeoutSet(trigger_auto_timeout)

    if trigger_detector_holdoff is not None:
        analog_in.triggerHoldOffSet(trigger_detector_holdoff)

    if trigger_detector_type is not None:
        analog_in.triggerTypeSet(trigger_detector_type)

    if trigger_detector_channel is not None:
        analog_in.triggerChannelSet(trigger_detector_channel)

    if trigger_detector_filter is not None:
        analog_in.triggerFilterSet(trigger_detector_filter)

    if trigger_detector_level is not None:
        analog_in.triggerLevelSet(trigger_detector_level)

    if trigger_detector_hysteresis is not None:
        analog_in.triggerHysteresisSet(trigger_detector_hysteresis)

    if trigger_detector_condition is not None:
        analog_in.triggerConditionSet(trigger_detector_condition)

    if trigger_detector_length is not None:
        analog_in.triggerLengthSet(trigger_detector_length)

    if trigger_detector_length_condition is not None:
        analog_in.triggerLengthConditionSet(trigger_detector_length_condition)

    if sampling_source is not None:
        analog_in.samplingSourceSet(sampling_source)

    if sampling_slope is not None:
        analog_in.samplingSlopeSet(sampling_slope)

    if sampling_delay is not None:
        analog_in.samplingDelaySet(sampling_delay)


def configure_analog_in_channel(analog_in           : AnalogIn,
                                channel             : int,
                                channel_enable      : Optional[bool]=None,
                                channel_filter      : Optional[DwfAnalogInFilter]=None,
                                channel_range       : Optional[float]=None,
                                channel_offset      : Optional[float]=None,
                                channel_attenuation : Optional[float]=None,
                                channel_bandwidth   : Optional[float]=None
                               ) -> None:
    """Configure an |AnalogIn| instrument channel.

    Parameters:
        analog_in (AnalogIn): The |AnalogIn| instrument to be configured.
        channel (int): The analog input channel to be configured.
        channel_enable(Optional[bool]): If given, enable or disable the specified channel.
        channel_filter(Optional[DwfAnalogInFilter]): If given, configure channel's filter setting.
        channel_range(Optional[float]): If given, set the channel's range setting.
        channel_offset(Optional[float]): If given, set the channel's offset setting.
        channel_attenuation(Optional[float]): If given, set the channel's attenuation setting.
        channel_bandwidth(Optional[float]): If given, set the channel's bandwidth setting.

        Raises:
            DwfLibraryError: One of the settings could not be applied.
    """

    if channel_enable is not None:
        analog_in.channelEnableSet(channel, channel_enable)

    if channel_filter is not None:
        analog_in.channelFilterSet(channel, channel_filter)

    if channel_range is not None:
        analog_in.channelRangeSet(channel, channel_range)

    if channel_offset is not None:
        analog_in.channelOffsetSet(channel, channel_offset)

    if channel_attenuation is not None:
        analog_in.channelAttenuationSet(channel, channel_attenuation)

    if channel_bandwidth is not None:
        analog_in.channelBandwidthSet(channel, channel_bandwidth)

########################################################################################################################
##                                                                                                                    ##
##                      Configuration support for the AnalogOut instrument and its channel nodes                      ##
##                                                                                                                    ##
########################################################################################################################

def configure_analog_out_channel(analog_out           : AnalogOut,
                                 channel              : int,
                                 wait_duration        : Optional[float]=None,
                                 run_duration         : Optional[float]=None,
                                 repeat_trigger_flag  : Optional[bool]=None,
                                 repeat               : Optional[int]=None,
                                 master_channel_index : Optional[int]=None,
                                 trigger_source       : Optional[DwfTriggerSource]=None,
                                 trigger_slope        : Optional[DwfTriggerSlope]=None,
                                 mode                 : Optional[DwfAnalogOutMode]=None,
                                 idle                 : Optional[DwfAnalogOutIdle]=None,
                                 limitation           : Optional[float]=None,
                                 custom_am_fm_enable  : Optional[bool]=None
                                ) -> None:
    """Configure an analog output channel.

    Parameters:
        analog_out (AnalogOut)                     : The |AnalogOut| instrument to be configured.
        channel (int)                              : The analog output channel to be configured.
        wait_duration(Optional[float])             : If given, enable or disable the specified channel.
        run_duration(Optional[float])              : If given, configure channel's filter setting.
        repeat_trigger_flag(Optional[bool])        : If given, set the channel's repeat trigger flag.
        repeat(Optional[int])                      : If given, set the channel's repeat setting.
        master_channel_index(Optional[int])        : If given, set the channel's master channel setting.
        trigger_source(Optional[DwfTriggerSource]) : If given, set the channel's trigger source.
        trigger_slope(Optional[DwfTriggerSlope])   : If given, set the channel's trigger slope.
        mode(Optional[DwfAnalogOutMode])           : If given, set the channel's mode.
        idle(Optional[DwfAnalogOutIdle])           : If given, set the channel's idle behavior.
        limitation(Optional[float])                : If given, set the channel's limitation setting.
        custom_am_fm_enable(Optional[bool])        : If given, set the channel's custom AM/FM enable setting.

        Raises:
            DwfLibraryError: One of the settings could not be applied.
    """

    if wait_duration is not None:
        analog_out.waitSet(channel, wait_duration)

    if run_duration is not None:
        analog_out.runSet(channel, run_duration)

    if repeat_trigger_flag is not None:
        analog_out.repeatTriggerSet(channel, repeat_trigger_flag)

    if repeat is not None:
        analog_out.repeatSet(channel, repeat)

    if master_channel_index is not None:
        analog_out.masterSet(channel, master_channel_index)

    if trigger_source is not None:
        analog_out.triggerSourceSet(channel, trigger_source)

    if trigger_slope is not None:
        analog_out.triggerSlopeSet(channel, trigger_slope)

    if mode is not None:
        analog_out.modeSet(channel, mode)

    if idle is not None:
        analog_out.idleSet(channel, idle)

    if limitation is not None:
        analog_out.limitationSet(channel, limitation)

    if custom_am_fm_enable is not None:
        analog_out.customAMFMEnableSet(channel, custom_am_fm_enable)


def configure_analog_out_channel_node(
        analog_out     : AnalogOut,
        channel        : int,
        node           : DwfAnalogOutNode,
        node_enable    : Optional[bool]=None,
        node_function  : Optional[DwfAnalogOutFunction]=None,
        node_frequency : Optional[float]=None,
        node_amplitude : Optional[float]=None,
        node_offset    : Optional[float]=None,
        node_symmetry  : Optional[float]=None,
        node_phase     : Optional[float]=None,
        node_data      : Optional[np.ndarray]=None) -> None:
    """Configure an analog output channel node.

    Parameters:
        analog_out (AnalogOut)                        : The |AnalogOut| instrument to be configured.
        channel (int)                                 : The analog output channel to be configured.
        node (DwfAnalogOutNode)                       : The analog output node to be configured.
        node_enable(Optional[float])                  : If given, set the channel node's enable state.
        node_function(Optional[DwfAnalogOutFunction]) : If given, set the channel node's function.
        node_frequency(Optional[float])               : If given, set the channel node's frequency.
        node_amplitude(Optional[float])               : If given, set the channel node's amplitude.
        node_offset(Optional[float])                  : If given, set the channel node's offset.
        node_symmetry(Optional[float])                : If given, set the channel node's symmetry.
        node_phase(Optional[float])                   : If given, set the channel node's phase.
        node_data(Optional[float])                    : If given, set the channel node's data.

        Raises:
            DwfLibraryError: One of the settings could not be applied.
    """

    if node_enable is not None:
        analog_out.nodeEnableSet(channel, node, node_enable)

    if node_function is not None:
        analog_out.nodeFunctionSet(channel, node, node_function)

    if node_frequency is not None:
        analog_out.nodeFrequencySet(channel, node, node_frequency)

    if node_amplitude is not None:
        analog_out.nodeAmplitudeSet(channel, node, node_amplitude)

    if node_offset is not None:
        analog_out.nodeOffsetSet(channel, node, node_offset)

    if node_symmetry is not None:
        analog_out.nodeSymmetrySet(channel, node, node_symmetry)

    if node_phase is not None:
        analog_out.nodePhaseSet(channel, node, node_phase)

    if node_data is not None:
        analog_out.nodeDataSet(channel, node, node_data)
