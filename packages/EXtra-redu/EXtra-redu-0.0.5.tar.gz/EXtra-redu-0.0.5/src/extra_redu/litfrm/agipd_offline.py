import numpy as np

from collections import namedtuple
from extra_data.exceptions import PropertyNameError
from .agipd_base import (
    AgipdLitFrameFinderBase, Agipd1g, Agipd2g, ReferenceDelay,
    EVENT_CODE, DESTINATION, AGIPD_MAX_CELL, SA1, SA2, SA3,
)


# Exceptions
class LitFrameFinderError(RuntimeError):
    pass


class SourceNotFound(LitFrameFinderError):
    pass


class BunchPatternNotFound(SourceNotFound):
    pass


class DetectorNotFound(SourceNotFound):
    pass


class TriggerNotFound(SourceNotFound):
    pass


class NoReferenceDelay(LitFrameFinderError):
    pass


AttributeValue = namedtuple('AttributeValue', ['value'])
AVal = AttributeValue


class Agipd1gOffline(Agipd1g):
    def read_run_values(self, dc):
        srcname = self.detector_control_id

        AgipdBunchStructure = namedtuple('Agipd1BunchStructure', [
            'nPulses', 'firstPulse', 'repetitionRate'
        ])
        AgipdDetectorCtrl = namedtuple('Agipd1DetectorCtrl', [
            'bunchStructure', 'patternType', 'patternTypeIndex',
            'integrationTime', 't0Delay'
        ])
        self.det = AgipdDetectorCtrl(
            bunchStructure=AgipdBunchStructure(
                nPulses=AVal(dc.get_run_value(
                    srcname, 'bunchStructure.nPulses')),
                firstPulse=AVal(dc.get_run_value(
                    srcname, 'bunchStructure.firstPulse')),
                repetitionRate=AVal(dc.get_run_value(
                    srcname, 'bunchStructure.repetitionRate')),
            ),
            patternType=AVal(dc.get_run_value(
                srcname, 'patternType')),
            patternTypeIndex=AVal(dc.get_run_value(
                srcname, 'patternTypeIndex')),
            integrationTime=AVal(dc.get_run_value(
                srcname, 'integrationTime')),
            t0Delay=AVal(dc.get_run_value(
                srcname, 't0Delay')),
        )
        return self.det


class Agipd2gOffline(Agipd2g):
    def read_run_values(self, dc):
        srcname = self.detector_control_id

        AgipdBunchStructure = namedtuple('Agipd2BunchStructure', [
            'nPulses', 'repetitionRate'
        ])
        AgipdDetectorCtrl = namedtuple('Agipd2DetectorCtrl', [
            'bunchStructure', 'expType', 'expTypeIndex',
            'integrationTime',
        ])
        self.det = AgipdDetectorCtrl(
            bunchStructure=AgipdBunchStructure(
                nPulses=AVal(dc.get_run_value(
                    srcname, 'bunchStructure.nPulses')),
                repetitionRate=AVal(dc.get_run_value(
                    srcname, 'bunchStructure.repetitionRate')),
            ),
            expType=AVal(dc.get_run_value(
                srcname, 'expType')),
            expTypeIndex=AVal(dc.get_run_value(
                srcname, 'expTypeIndex')),
            integrationTime=AVal(dc.get_run_value(
                srcname, 'integrationTime')),
        )
        return self.det


AGIPDGEN_OFFLINE = {
    "AgipdComposite": Agipd1gOffline,
    "Agipd2Composite": Agipd2gOffline,
}

Trigger = namedtuple('Trigger', ['deviceId', 'name'])
Motor = namedtuple('Motor', ['deviceId', 'positionProperty',
                             'unitConversionCoef'])


class AgipdLitFrameFinderOffline(AgipdLitFrameFinderBase):

    def __init__(self, dev_id, dc, ref_delays={}, **kwargs):
        self.dev_id = dev_id
        self.dc = dc
        self._reference = ref_delays

        for a, v in kwargs.items():
            setattr(self, a, AVal(v))

        if dev_id in dc.control_sources:
            try:
                self._configure(dc, dev_id)
            except PropertyNameError:
                self._configure_v03(dc, dev_id)

        inst = self.instrumentName.value
        self.dst = DESTINATION[inst]

        agipd_class = AGIPDGEN_OFFLINE.get(self._get_agipd_classid(dc))
        if agipd_class is None:
            raise ValueError("Unknown class of AgipdComposite device")
        self._agipd = agipd_class(self.detector_control_id, self)

        self.shutters_are_open = True

    def _configure_v03(self, dc, dev_id):
        def get_property(key):
            return AVal(dc.get_run_value(dev_id, key))

        def get_value(key):
            return dc.get_run_value(dev_id, key)

        self.detector_control_id = get_value('DetectorCtrl')
        self.alignMethod = get_property('alignMethod')
        self.instrumentName = get_property('instrumentName')
        self.referenceFrame = get_property('referenceFrame')

        self.trigger = Trigger(
            deviceId=get_value('Timer'),
            name=get_property('trigger'),
        )
        self.motor = Motor(
            deviceId='',
            positionProperty='',
            unitConversionCoef=1,
        )

    def _configure(self, dc, dev_id):
        def get_property(key):
            return AVal(dc.get_run_value(dev_id, key))

        def get_value(key):
            return dc.get_run_value(dev_id, key)

        self.detector_control_id = get_value('detectorId')
        self.alignMethod = get_property('alignMethod')
        self.instrumentName = get_property('instrumentName')
        self.referenceFrame = get_property('referenceFrame')

        self.trigger = Trigger(
            deviceId=get_value('trigger.deviceId'),
            name=get_property('trigger.name'),
        )
        self.motor = Motor(
            deviceId=get_value('motor.deviceId'),
            positionProperty=get_property('motor.positionProperty'),
            unitConversionCoef=get_property('motor.unitConversionCoef'),
        )
        for event_name, event_code in EVENT_CODE.items():
            ref = ReferenceDelay(**dict([
                (key, get_value(f"referenceDelay.{event_name}.{key}"))
                for key in ReferenceDelay._fields
            ]))
            if ref.delay != -1:
                self._reference[event_code] = ref

    def _get_agipd_classid(self, dc):
        srcname = self.detector_control_id
        if srcname not in dc.control_sources:
            raise(DetectorNotFound(f"Source '{srcname}' is not found."))

        return dc.get_run_value(srcname, 'classId')

    def _read_run_values(self, dc):
        self.DetectorCtrl = self._agipd.read_run_values(dc)

        if self.alignMethod.value == "by reference delay":
            self._read_trigger_and_motor_values(dc)

    def _read_trigger_and_motor_values(self, dc):
        srcname = self.trigger.deviceId
        if srcname not in dc.control_sources:
            raise(TriggerNotFound(f"Source {srcname} is not found."))

        key = self.trigger.name.value
        self.trigger_event = dc.get_run_value(srcname, key + '.event')
        self.trigger_delay = dc.get_run_value(srcname, key + '.delay')

        self.ref = self._reference.get(self.trigger_event)
        if self.ref is None:
            raise(NoReferenceDelay("Reference delay for marco event "
                                   f"{self.trigger_event} is not set."))

        srcname = self.motor.deviceId
        if srcname in dc.control_sources:
            key = self.motor.positionProperty.value
            self.motor_position = dc.get_run_value(srcname, key)
        else:
            self.motor_position = None

    def _read_pp_decoder(self, dc):
        pp_src = dc[self.pp_decoder_id]
        trainId = pp_src['sase1/nPulses'].train_id_coordinates()
        bunch_pattern = np.zeros([trainId.size, 2700], dtype=np.uint32)
        n1 = pp_src['sase1/nPulses'].ndarray()
        p1 = pp_src['sase1/pulseIds'].ndarray()
        n2 = pp_src['sase2/nPulses'].ndarray()
        p2 = pp_src['sase2/pulseIds'].ndarray()
        n3 = pp_src['sase3/nPulses'].ndarray()
        p3 = pp_src['sase3/pulseIds'].ndarray()
        for i in range(trainId.size):
            bunch_pattern[i, p1[i, :n1[i]]] |= SA1.code
            bunch_pattern[i, p2[i, :n2[i]]] |= SA2.code
            bunch_pattern[i, p3[i, :n3[i]]] |= SA3.code
        return trainId, bunch_pattern

    def process(self, force=False):
        if not force and hasattr(self, 'r'):
            return self.r

        dc = self.dc
        self._read_run_values(dc)

        # bunch pattern
        if self.bunch_pattern_id in dc.instrument_sources:
            bp_keydata = dc[self.bunch_pattern_id, 'data.bunchPatternTable']
            bunch_pattern = bp_keydata.ndarray()
            trainId = bp_keydata.train_id_coordinates()
            bpsrc = "timeserver"
        elif self.pp_decoder_id in dc.control_sources:
            trainId, bunch_pattern = self._read_pp_decoder(dc)
            bpsrc = "pp_decoder"
        elif self._agipd.exp_type.value == 'XRay':
            raise(BunchPatternNotFound(
                f"Neither source '{self.bunch_pattern_id}' nor source "
                f"'{self.pp_decoder_id}' are found."))
        else:
            # only for dark runs
            bpsrc = "none"
            trainId = np.array(dc.train_ids, np.uint64)
            bunch_pattern = None

        # XGM
        if self.xgm_id not in dc.instrument_sources:
            xgm_flag = np.zeros(trainId.size, bool)
        else:
            xgm_en_keydata = dc[self.xgm_id, 'data.intensityTD']
            xgm_sig_keydata = dc[self.xgm_id, 'data.intensitySigmaTD']

            xgm_trainId = xgm_en_keydata.train_id_coordinates()
            xgm_sel = np.in1d(xgm_trainId, trainId)
            xgm_trainId = xgm_trainId[xgm_sel]

            xgm_intensityTD = xgm_en_keydata.ndarray()[xgm_sel]
            xgm_intensitySigmaTD = xgm_sig_keydata.ndarray()[xgm_sel]

            xgm_flag = np.in1d(trainId, xgm_trainId)
            xgm_map = np.roll(np.cumsum(xgm_flag), 1)
            xgm_map[0] = 0

        Output = namedtuple('Output', [
            'nFrame', 'detectorPulseId', 'nPulsePerFrame', 'energyPerFrame',
            'energySigma', 'dataFramePattern', 'masterPulseId', 'xgmPulseId'
        ])
        Result = namedtuple('Results', [
            'nPulse', 'nFrame', 'litFrames', 'nLitFrame', 'dataFrames',
            'nDataFrame', 'output', 'meta'
        ])
        Meta = namedtuple('Meta', ['litFrmDev', 'trainId'])
        n = trainId.shape[0]
        r = Result(
            nPulse=AVal(np.zeros(n, np.uint16)),
            nFrame=AVal(np.zeros(n, np.uint16)),
            nLitFrame=AVal(np.zeros(n, np.uint16)),
            litFrames=AVal(np.zeros([n, AGIPD_MAX_CELL], np.uint16)),
            nDataFrame=AVal(np.zeros(n, np.uint16)),
            dataFrames=AVal(np.zeros([n, AGIPD_MAX_CELL], np.uint16)),
            output=Output(
                nFrame=np.zeros(n, np.uint16),
                nPulsePerFrame=np.zeros([n, AGIPD_MAX_CELL], np.uint16),
                energyPerFrame=np.zeros([n, AGIPD_MAX_CELL], np.float32),
                energySigma=np.zeros([n, AGIPD_MAX_CELL], np.float32),
                dataFramePattern=np.zeros([n, AGIPD_MAX_CELL], bool),
                detectorPulseId=np.zeros([n, AGIPD_MAX_CELL], np.uint16),
                masterPulseId=np.zeros([n, 2700], np.uint16),
                xgmPulseId=np.zeros([n, 2700], np.uint16),
            ),
            meta=Meta(litFrmDev=f"offline/{bpsrc}", trainId=trainId),
        )

        Data = namedtuple('Data', ['data'])
        BunchPatternTable = namedtuple(
            'BunchPatternTable', ['bunchPatternTable'])
        XGM = namedtuple('XGM', ['intensityTD', 'intensitySigmaTD'])

        for no, tid in enumerate(trainId):
            if bunch_pattern is not None:
                bp = Data(Data(BunchPatternTable(AVal(bunch_pattern[no]))))

                if xgm_flag[no]:
                    xgm_no = xgm_map[no]
                    xgm = Data(Data(XGM(
                        intensityTD=AVal(xgm_intensityTD[xgm_no]),
                        intensitySigmaTD=AVal(xgm_intensitySigmaTD[xgm_no]),
                    )))
                else:
                    xgm = None

                (npulse, ncell,
                 agipd_pulse_ids, frames) = self.process_train(bp, xgm)
            else:
                (npulse, ncell,
                 agipd_pulse_ids, frames) = self.make_dark_run()

            # send pipeline (fast) data
            r.output.nFrame[no] = ncell
            r.output.detectorPulseId[no, :ncell] = agipd_pulse_ids
            r.output.nPulsePerFrame[no, :ncell] = frames.npulse
            r.output.energyPerFrame[no, :ncell] = frames.energy
            r.output.energySigma[no, :ncell] = frames.energy_std
            r.output.dataFramePattern[no, :ncell] = frames.hasdata
            nmaster = frames.master_ids.size
            r.output.masterPulseId[no, :nmaster] = frames.master_ids
            nxgm = frames.xgm_ids.size
            r.output.xgmPulseId[no, :nxgm] = frames.xgm_ids

            litframes = np.flatnonzero(frames.npulse)
            dataframes = np.flatnonzero(frames.hasdata)

            # update attributes (slow data)
            r.nPulse.value[no] = npulse
            r.nFrame.value[no] = ncell
            r.litFrames.value[no, :frames.nlit] = litframes
            r.nLitFrame.value[no] = frames.nlit
            r.dataFrames.value[no, :frames.ndata] = dataframes
            r.nDataFrame.value[no] = frames.ndata

        self.r = r
        return r

    def read(self):
        dc = self.dc
        inst_src = dc[self.dev_id + ':output']
        trainId = inst_src['data.nFrame'].train_id_coordinates()

        Output = namedtuple('Output', [
            'nFrame', 'detectorPulseId', 'nPulsePerFrame', 'energyPerFrame',
            'energySigma', 'dataFramePattern', 'masterPulseId', 'xgmPulseId'
        ])
        Result = namedtuple('Results', [
            'nPulse', 'nFrame', 'litFrames', 'nLitFrame', 'dataFrames',
            'nDataFrame', 'output', 'meta'
        ])
        Meta = namedtuple('Meta', ['litFrmDev', 'trainId'])
        out = Output(
            nFrame=inst_src['data.nFrame'].ndarray(),
            nPulsePerFrame=inst_src['data.nPulsePerFrame'].ndarray(),
            energyPerFrame=inst_src['data.energyPerFrame'].ndarray(),
            energySigma=inst_src['data.energySigma'].ndarray(),
            dataFramePattern=inst_src['data.dataFramePattern'].ndarray(),
            detectorPulseId=inst_src['data.detectorPulseId'].ndarray(),
            masterPulseId=inst_src['data.masterPulseId'].ndarray(),
            xgmPulseId=inst_src['data.xgmPulseId'].ndarray(),
        )

        n = trainId.size
        litframes = np.zeros([n, 352], dtype=np.uint16)
        dataframes = np.zeros([n, 352], dtype=np.uint16)
        for no, tid in enumerate(trainId):
            a = np.flatnonzero(out.nPulsePerFrame[no])
            litframes[no, :a.size] = a
            a = np.flatnonzero(out.dataFramePattern[no])
            dataframes[no, :a.size] = a

        r = Result(
            nPulse=AVal(out.nPulsePerFrame.sum(1)),
            nFrame=AVal(out.nFrame),
            nLitFrame=AVal((out.nPulsePerFrame != 0).sum(1)),
            litFrames=AVal(litframes),
            nDataFrame=AVal(out.dataFramePattern.sum(1)),
            dataFrames=AVal(dataframes),
            output=out,
            meta=Meta(litFrmDev=self.dev_id, trainId=trainId),
        )

        self.r = r
        return r

    def read_or_process(self):
        channel = self.dev_id + ':output'
        if channel in self.dc.instrument_sources:
            r = self.read()
            if len(r.meta.trainId):
                return r

        return self.process(force=True)


class AgipdLitFrameFinderConfigureMID:
    dev_id = "MID_EXP_AGIPD1M1/REDU/LITFRM"

    detector_control_id = "MID_EXP_AGIPD1M1/MDL/FPGA_COMP"
    bunch_pattern_id = "MID_RR_UTC/TSYS/TIMESERVER:outputBunchPattern"
    xgm_id = "SA2_XTD1_XGM/XGM/DOOCS:output"
    pp_decoder_id = "MID_RR_SYS/MDL/PULSE_PATTERN_DECODER"

    trigger = Trigger(
        deviceId="MID_EXP_SYS/TSYS/UTC-2-S4",
        name=AVal("backTrg3")
    )
    motor = Motor(
        deviceId="MID_AGIPD_MOTION/MDL/DOWNSAMPLER",
        positionProperty=AVal("t4EncoderPosition"),
        unitConversionCoef=AVal(1e-3),
    )
    alignMethod = AVal("by first pulse")
    referenceFrame = AVal(1)

    missedIntensityTD = AVal(10000)
    missedIntensitySigmaTD = AVal(0)

    instrumentName = AVal("MID")


class AgipdLitFrameFinderMID(AgipdLitFrameFinderConfigureMID,
                             AgipdLitFrameFinderOffline):
    def __init__(self, dc, dev_id=AgipdLitFrameFinderConfigureMID.dev_id,
                 ref_delays={}, **kwargs):
        super().__init__(self.dev_id, dc, ref_delays, **kwargs)


class AgipdLitFrameFinderConfigureSPB:
    dev_id = 'SPB_IRU_AGIPD1M1/REDU/LITFRM'

    detector_control_id = 'SPB_IRU_AGIPD1M1/MDL/FPGA_COMP'
    bunch_pattern_id = 'SPB_RR_SYS/TSYS/X2TIMER2:outputBunchPattern'
    xgm_id = 'SPB_XTD9_XGM/XGM/DOOCS:output'
    pp_decoder_id = 'SPB_RR_SYS/MDL/BUNCH_PATTERN'

    trigger = Trigger(
        deviceId="SPB_EXP_SYS/TSYS/UTC_1_S3",
        name=AVal("backTrg3")
    )
    motor = Motor(
        deviceId="",
        positionProperty=AVal(""),
        unitConversionCoef=AVal(1),
    )
    alignMethod = AVal('by first pulse')
    referenceFrame = AVal(1)

    missedIntensityTD = AVal(10000)
    missedIntensitySigmaTD = AVal(0)

    instrumentName = AVal('SPB')


class AgipdLitFrameFinderSPB(AgipdLitFrameFinderConfigureSPB,
                             AgipdLitFrameFinderOffline):
    def __init__(self, dc, dev_id=AgipdLitFrameFinderConfigureSPB.dev_id,
                 ref_delays={}, **kwargs):
        super().__init__(self.dev_id, dc, ref_delays, **kwargs)


class AgipdLitFrameFinderConfigureHED:
    dev_id = 'HED_EXP_AGIPD500K2G/REDU/LITFRM'

    detector_control_id = 'HED_EXP_AGIPD500K2G/MDL/FPGA_COMP'
    bunch_pattern_id = 'HED_RR_UTC/TSYS/TIMESERVER:outputBunchPattern'
    xgm_id = 'HED_XTD6_XGM/XGM/DOOCS:output'
    pp_decoder_id = 'SA2_BR_UTC/MDL/BUNCHPATTERN_DECODER'

    trigger = Trigger(
        deviceId="HED_EXP_SYS/TSYS/UTC-1-S2",
        name=AVal("backTrg3")
    )
    motor = Motor(
        deviceId="",
        positionProperty=AVal(""),
        unitConversionCoef=AVal(1),
    )
    alignMethod = AVal('by first pulse')
    referenceFrame = AVal(1)

    missedIntensityTD = AVal(10000)
    missedIntensitySigmaTD = AVal(0)

    instrumentName = AVal('HED')


class AgipdLitFrameFinderHED(AgipdLitFrameFinderConfigureHED,
                             AgipdLitFrameFinderOffline):
    def __init__(self, dc, dev_id=AgipdLitFrameFinderConfigureHED.dev_id,
                 ref_delays={}, **kwargs):
        super().__init__(self.dev_id, dc, ref_delays, **kwargs)


AgipdLitFrameFinderProfiles = {
    "MID": AgipdLitFrameFinderMID,
    "SPB": AgipdLitFrameFinderSPB,
    "HED": AgipdLitFrameFinderHED,
}


def find_litframe_finder_sources(dc):
    litfrm_finder_ids = [
        src for src, cls in (
            (src, dc.get_run_value(src, 'classId'))
            for src in dc.control_sources
        ) if cls == 'AgipdLitFrameFinder'
    ]
    return litfrm_finder_ids


def make_litframe_finder(inst, dc, dev_id=None, ref_delays={}):
    if inst not in AgipdLitFrameFinderProfiles:
        raise IndexError("Unexpected name of AgipdLitFrameFinder profile")

    litfrm_finder_cls = AgipdLitFrameFinderProfiles[inst]
    dev_ids = find_litframe_finder_sources(dc)

    if not dev_id:
        dev_id = litfrm_finder_cls.dev_id

    if dev_ids and dev_id not in dev_ids:
        dev_id = dev_ids[0]

    return litfrm_finder_cls(dc, dev_id, ref_delays=ref_delays)
