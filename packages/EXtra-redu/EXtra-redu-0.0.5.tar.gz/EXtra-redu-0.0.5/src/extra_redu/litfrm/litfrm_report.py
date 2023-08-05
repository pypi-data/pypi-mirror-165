import os
import csv
import argparse

from extra_data import RunDirectory
from extra_data.read_machinery import find_proposal
from extra_redu import (
    make_litframe_finder, BunchPatternNotFound, DetectorNotFound
)
from extra_redu.litfrm.utils import litfrm_run_report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate litframe report for a proposal.')
    parser.add_argument('proposal', metavar='propno', type=int, nargs=1,
                        help='proposal Id')
    parser.add_argument('-o', '--csv', metavar='csv', type=str, nargs=1,
                        help='the name of output CSV-file')

    args = parser.parse_args()

    propno = args.proposal[0]
    csvname = f"litfrm_p{propno:06}.csv" if args.csv is None else args.csv[0]

    propdir = find_proposal(f"p{propno:06d}")
    inst = propdir.split('/')[4]
    print(f"Proposal No: {propno}")
    print(f"Proposal directory: {propdir}")
    print(f"Instrument: {inst}")

    runs = sorted([
        int(fn[1:]) for fn in os.listdir(os.path.join(propdir, "raw"))
        if fn[0] == 'r' and fn[1:].isdigit()
    ])

    f = open(csvname, 'w', newline='')
    fieldnames = ['runno', 'source', 'runtype', 'pattern_no', 'trains',
                  'npulse', 'ndataframe', 'nframe', 'frames', 'exception']
    writer = csv.DictWriter(
        f, fieldnames=fieldnames, delimiter=';', quotechar='"',
        quoting=csv.QUOTE_NONNUMERIC
    )
    writer.writeheader()

    for runno in runs:
        rundir = os.path.join(propdir, "raw", f"r{runno:04}")
        dc = RunDirectory(rundir)

        try:
            litfrm = make_litframe_finder(inst, dc)
            r = litfrm.process()
            runtype = litfrm.DetectorCtrl.patternType.value
            rep = litfrm_run_report(r)
            for r in rep:
                frmintf = ', '.join(
                    [':'.join([str(n) for n in slc]) for slc in r['frames']]
                )
                trsintf = ':'.join([str(n) for n in r['trains']])
                recfrm = r.copy()
                recfrm['frames'] = frmintf
                recfrm['runno'] = runno
                recfrm['runtype'] = runtype
                writer.writerow(recfrm)
                if r['pattern_no'] == 0:
                    print("{runno:4d} {source:30s} {runtype:6s}".format(
                        **recfrm), end='')
                else:
                    print(" "*42, end='')
                print(
                    ("{pattern_no:2d} {trsintf:25s} {npulse:4d} "
                     "{ndataframe:3d} {nframe:3d} [{frames}]"
                     ).format(trsintf=trsintf, **recfrm))
        except BunchPatternNotFound:
            runtype = litfrm.DetectorCtrl.patternType.value
            errmsg = f"BunchPattern not found ({runtype})"
            writer.writerow(dict(runno=runno, exception=errmsg))
            print(f"{runno:4d} - skip: {errmsg}")
        except DetectorNotFound:
            errmsg = "Detector not found"
            writer.writerow(dict(runno=runno, exception=errmsg))
            print(f"{runno:4d} - skip: {errmsg}")

    f.close()
