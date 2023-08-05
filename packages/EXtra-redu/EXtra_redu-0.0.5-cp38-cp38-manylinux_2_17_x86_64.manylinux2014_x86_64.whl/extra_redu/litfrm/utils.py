import numpy as np


def steady_intervals(a):
    """Find intervals of consecutive identical values"""
    if len(a) > 0:
        i = np.flatnonzero(np.diff(a))
        i0 = 0
        intv = True
        for iN in i:
            if intv:
                yield (i0, iN)
                intv = False
            else:
                i0 = iN + 1
                intv = True

        if intv:
            yield (i0, len(a) - 1)


def find_intervals(ptrn, intrv):
    ix = np.flatnonzero(ptrn)
    if ix.size == 1:
        intrv.append((ix[0],))
    else:
        steps = np.diff(ix)
        for f0, fN in steady_intervals(steps):
            i0 = ix[f0]
            if f0 == fN:
                intrv.append((i0,))
            else:
                iN = ix[fN + 1] + 1
                s = steps[f0]
                intrv.append((i0, iN) if s == 1 else (i0, iN, s))
    return intrv


def litfrm_run_report(r):
    """Compute single run litframe report"""
    rep = []
    ptrnno = 0
    nfrm_uniq, nfrm_ix = np.unique(r.output.nFrame, return_inverse=True)
    for i in range(nfrm_uniq.size):
        nfrm = nfrm_uniq[i]
        npls_uniq, npls_ix = np.unique(
            r.output.nPulsePerFrame[nfrm_ix == i, :nfrm],
            return_inverse=True, axis=0
        )
        datafrm = r.output.dataFramePattern[nfrm_ix == i, :nfrm]
        tid = r.meta.trainId[nfrm_ix == i]
        one = tid.dtype.type(1)

        trsint = []
        for j in range(npls_uniq.shape[0]):
            trsint = find_intervals(npls_ix == j, trsint)

        for trs in sorted(trsint):
            t0 = trs[0]
            tN = trs[1] - 1 if len(trs) > 1 else t0
            trains = ((tid[t0], tid[tN] + one, trs[2]) if len(trs) == 3
                      else (tid[t0], tid[tN] + one))

            ptrn = datafrm[t0, :]
            ndata = ptrn.sum()
            npls = npls_uniq[npls_ix[t0], :].sum()

            frmint = find_intervals(ptrn, [])
            rep.append(dict(
                source=r.meta.litFrmDev, pattern_no=ptrnno, trains=trains,
                npulse=npls, ndataframe=ndata, nframe=nfrm, frames=frmint,
            ))
            ptrnno += 1

    return rep
