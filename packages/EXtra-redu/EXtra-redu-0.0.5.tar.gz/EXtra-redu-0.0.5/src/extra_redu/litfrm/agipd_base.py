import numpy as np

from collections import namedtuple
from euxfel_bunch_pattern import (
    DESTINATION_MASK, PHOTON_LINE_DEFLECTION, DESTINATION_T4D, DESTINATION_T5D
)

XgmIntensity = namedtuple('XgmIntensity', ['mu', 'sig'])
ReferenceDelay = namedtuple('ReferenceDelay', [
    'delay', 'pulse', 'frame', 'repetitionRate', 'position'])


class FramesAnnotation:
    """Frames annotatons (metadata)"""

    def __init__(self, npulse, energy, energy_std, master_ids,
                 xgm_ids, hasdata=None):
        self.npulse = npulse
        self.energy = energy
        self.energy_std = energy_std
        self.master_ids = master_ids
        self.xgm_ids = xgm_ids
        hasxray = npulse > 0
        self.hasdata = hasxray if hasdata is None else hasdata
        self.nlit = hasxray.sum()
        self.ndata = self.hasdata.sum()

    @classmethod
    def non_xray(cls, ncell, hasdata=None):
        return cls(
            np.zeros(ncell, np.uint16),
            np.zeros(ncell, float),
            np.zeros(ncell, float),
            np.zeros(0, np.uint16),
            np.zeros(0, np.uint16),
            np.ones(ncell, bool) if hasdata is None else hasdata
        )

    @classmethod
    def dark(cls, ncell):
        return cls.non_xray(ncell, np.zeros(ncell, bool))


class ParamDecoder:
    """Decodes Bunch Pattern"""

    @classmethod
    def get_instrument_pulse_mask(cls, bunch):
        return (bunch & cls.mask) == cls.code

    @classmethod
    def get_xgm_pulse_mask(cls, bunch):
        xgm_pulses = (bunch & cls.mask_xgm) == cls.code_xgm
        inst_pulses = (bunch & cls.mask) == cls.code
        return inst_pulses[xgm_pulses]

    @classmethod
    def get_xgm_pulse_mask_in_file(cls, bunch, xgm_maxlen=1000):
        xgm_pulses = (bunch & cls.mask_xgm) == cls.code_xgm
        inst_pulses = (bunch & cls.mask) == cls.code
        return inst_pulses[xgm_pulses]


class SA1(ParamDecoder):
    """SASE 1 Bunch Pattern Decoder"""
    mask = PHOTON_LINE_DEFLECTION | DESTINATION_MASK
    code = DESTINATION_T4D
    mask_xgm = DESTINATION_MASK
    code_xgm = DESTINATION_T4D


class SA2(ParamDecoder):
    """SASE 2 Bunch Pattern Decoder"""
    mask = DESTINATION_MASK
    code = DESTINATION_T5D
    mask_xgm = DESTINATION_MASK
    code_xgm = DESTINATION_T5D


class SA3(ParamDecoder):
    """SASE 3 Bunch Pattern Decoder"""
    mask = PHOTON_LINE_DEFLECTION | DESTINATION_MASK
    code = PHOTON_LINE_DEFLECTION | DESTINATION_T4D
    mask_xgm = DESTINATION_MASK
    code_xgm = DESTINATION_T4D


DESTINATION = {
    'SPB': SA1, 'FXE': SA1,
    'MID': SA2, 'HED': SA2,
    'SQS': SA3, 'SCS': SA3,
}

AGIPD_MAX_CELL = 352
CLOCKS_PER_PULSE = 22  # AGIPD timing: 1 clock = 10 ns
RATE_TO_STRIDE = {'4.5': 1, '2.2': 2, '1.1': 4, '0.5': 8}
RATE_OPTIONS = [float(k) for k in RATE_TO_STRIDE]
SPEED_OF_LIGHT = 2.76708438734  # m/tick (1 tick = 9.23 ns)
TICS_PER_PULSE = 24  # TIMESERVER timing: 1 tic = 9.23 ns
EVENT_CODE = {"dynamic": 181, "static": 16}
EVENT_PULSE = {
    16: lambda pulses: 0,
    181: lambda pulses: np.argmax(pulses),
}


class Agipd1g:
    def __init__(self, detector_control_id, litfrm):
        self.detector_control_id = detector_control_id
        self.litfrm = litfrm

    @property
    def state(self):
        return self.det.masterState

    @property
    def exp_type(self):
        return self.det.patternType

    def get_bunch_structure(self):
        """Reads AGIPD frame settings."""
        ncell = self.det.bunchStructure.nPulses.value
        rate = self.det.bunchStructure.repetitionRate.value
        first_pulse_id = self.det.bunchStructure.firstPulse.value
        if ncell > AGIPD_MAX_CELL:
            ncell = AGIPD_MAX_CELL

        return ncell, first_pulse_id, RATE_TO_STRIDE[f"{rate:.1f}"]


class Agipd2g:
    def __init__(self, detector_control_id, litfrm):
        self.detector_control_id = detector_control_id
        self.litfrm = litfrm
        if litfrm.alignMethod.value == 'by reference delay':
            raise ValueError(
                "Alignment method 'by reference delay' "
                "is not implemented for AGIPD 2nd gen.")

    @property
    def state(self):
        return self.det.ctrlDevsState

    @property
    def exp_type(self):
        return self.det.expType

    def get_bunch_structure(self):
        """Reads AGIPD frame settings."""
        ncell = self.det.bunchStructure.nPulses.value
        rate = self.det.bunchStructure.repetitionRate.value
        if ncell > AGIPD_MAX_CELL:
            ncell = AGIPD_MAX_CELL

        return ncell, 0, RATE_TO_STRIDE[f"{rate:.1f}"]


AGIPDGEN = {
    "AgipdComposite": Agipd1g,
    "Agipd2Composite": Agipd2g,
}


class AgipdLitFrameFinderBase:
    """Base class containing core LitFrameFinder algorithm"""

    def make_dark_run(self):
        """Make LitFrameFinder response for dark or pc mode."""
        ncell, first_pulse_id, stride = self._agipd.get_bunch_structure()
        agipd_pulse_ids = np.arange(ncell) * stride + first_pulse_id

        frames = FramesAnnotation.non_xray(ncell)
        return 0, ncell, agipd_pulse_ids, frames

    def process_train(self, bp, xgm):
        """Process train data and make LitFrameFinder response."""

        ncell, first_pulse_id, stride = self._agipd.get_bunch_structure()
        agipd_pulse_ids = np.arange(ncell) * stride + first_pulse_id

        bunch_pattern = bp.data.data.bunchPatternTable.value
        # ts = meta.timestamp.timestamp
        # tid = meta.timestamp.tid

        pulses = self.dst.get_instrument_pulse_mask(bunch_pattern)
        npulse = pulses.sum()

        xgm_pulses = self.dst.get_xgm_pulse_mask(bunch_pattern)
        nxgm = xgm_pulses.size
        if xgm is None:
            intensity = XgmIntensity(
                np.full(nxgm, self.missedIntensityTD, np.float32),
                np.full(nxgm, self.missedIntensitySigmaTD, np.float32),
            )
        else:
            intensity = XgmIntensity(
                xgm.data.data.intensityTD.value[:nxgm][xgm_pulses],
                xgm.data.data.intensitySigmaTD.value[:nxgm][xgm_pulses]
            )

        xgm_indices = np.flatnonzero(xgm_pulses)
        frames = self.get_agipd_frames_annotation(
            npulse, pulses, intensity, xgm_indices, ncell, stride
        )
        # or self.DetectorCtrl.patternTypeIndex != 0
        if self._agipd.exp_type.value != 'XRay':
            frames.hasdata[:] = True
            frames.ndata = frames.hasdata.size

        return npulse, ncell, agipd_pulse_ids, frames

    def get_pulse_to_frame_alignment(self, pulses, stride):
        """Returns the reference pulse and the shift in pulses
           to the first exposed pulse slot.
        """
        if self.alignMethod.value == 'by first pulse':
            shift = self.referenceFrame.value * stride
            ref_pulse = np.argmax(pulses)
        elif self.alignMethod.value == 'by reference delay':
            frame_timestep = RATE_TO_STRIDE[
                f"{self.ref.repetitionRate:.1f}"] * TICS_PER_PULSE
            shift = (self.ref.delay + self.ref.frame * frame_timestep
                     - self.trigger_delay)
            if self.motor_position is not None:
                unit_coef = self.motor.unitConversionCoef.value
                shift -= (unit_coef * (self.ref.position
                                       - self.motor_position) / SPEED_OF_LIGHT)

            shift = round(shift / TICS_PER_PULSE)
            ref_pulse = EVENT_PULSE[
                self.trigger_event](pulses) + self.ref.pulse
        else:
            raise ValueError("Unexpected value of attribute "
                             f"alignMethod: {self.alignMethod.value}")

        return ref_pulse, shift

    def get_agipd_frames_annotation(
        self, npulse, pulses, intensity, xgm_indices, ncell, stride
    ):
        """Matches X-ray pulses, their energy, etc to the AGIPD frames."""
        # if no beam
        if npulse == 0 or not self.shutters_are_open:
            return FramesAnnotation.dark(ncell)

        # read exposure time
        exposure_in_tics = self.DetectorCtrl.integrationTime.value
        exposure = min(int(np.ceil(exposure_in_tics
                                   / CLOCKS_PER_PULSE)), stride)

        pulse_no = np.full(pulses.size, 65535, dtype=np.uint16)
        pulse_no[pulses] = np.arange(npulse, dtype=np.uint16)

        # compute pulse per frame pattern
        nfrm_in_pulses = ncell * stride
        pulse_to_frame = np.zeros(nfrm_in_pulses, dtype=bool)
        energy_to_frame = np.zeros(nfrm_in_pulses, dtype=float)
        energy_std_to_frame = np.zeros(nfrm_in_pulses, dtype=float)
        local_pulse_ids = np.full(nfrm_in_pulses, 65535, dtype=np.uint16)

        ref_pulse, shift = self.get_pulse_to_frame_alignment(pulses, stride)

        # compute slices of frame and pulse arrays
        first_pulse = np.argmax(pulses)
        p0 = max(first_pulse - shift, 0)
        f0 = (shift - first_pulse) * (shift > first_pulse)

        npulse_exposed = min(2700 - p0, nfrm_in_pulses - f0)
        pN = p0 + npulse_exposed
        fN = f0 + npulse_exposed

        pulse_to_frame[f0:fN] = pulses[p0:pN]
        pulse_no_to_frame = np.extract(pulses[p0:pN], pulse_no[p0:pN])

        local_pulse_ids[pulse_to_frame] = pulse_no_to_frame
        local_pulse_ids = local_pulse_ids.reshape(ncell, stride)[:, :exposure]
        local_pulse_ids = local_pulse_ids[local_pulse_ids != 65535]

        master_pulse_ids = np.flatnonzero(pulses)[local_pulse_ids]
        xgm_pulse_ids = xgm_indices[local_pulse_ids]

        energy_to_frame[pulse_to_frame] = intensity.mu[pulse_no_to_frame]
        energy_to_frame = energy_to_frame.reshape(ncell, stride)[:, :exposure]

        energy_std_to_frame[pulse_to_frame] = intensity.sig[pulse_no_to_frame]
        energy_std_to_frame = energy_std_to_frame.reshape(
            ncell, stride)[:, :exposure]

        pulse_to_frame = pulse_to_frame.reshape(ncell, stride)[:, :exposure]

        frames = FramesAnnotation(
            pulse_to_frame.astype(np.uint16).sum(1),
            energy_to_frame.sum(1),
            np.sqrt(np.square(energy_std_to_frame).sum(1)),
            master_pulse_ids,
            xgm_pulse_ids,
        )
        return frames
