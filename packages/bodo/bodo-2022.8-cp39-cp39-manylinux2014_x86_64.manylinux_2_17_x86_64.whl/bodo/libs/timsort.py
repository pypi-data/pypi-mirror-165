import numba
import numpy as np
import pandas as pd
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    lxzkv__igw = hi - lo
    if lxzkv__igw < 2:
        return
    if lxzkv__igw < MIN_MERGE:
        tcr__omiry = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + tcr__omiry, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    vzb__yatvn = minRunLength(lxzkv__igw)
    while True:
        khtz__ubslu = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if khtz__ubslu < vzb__yatvn:
            qvsb__kapu = lxzkv__igw if lxzkv__igw <= vzb__yatvn else vzb__yatvn
            binarySort(key_arrs, lo, lo + qvsb__kapu, lo + khtz__ubslu, data)
            khtz__ubslu = qvsb__kapu
        stackSize = pushRun(stackSize, runBase, runLen, lo, khtz__ubslu)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += khtz__ubslu
        lxzkv__igw -= khtz__ubslu
        if lxzkv__igw == 0:
            break
    assert lo == hi
    stackSize, tmpLength, tmp, tmp_data, minGallop = mergeForceCollapse(
        stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
        tmp_data, minGallop)
    assert stackSize == 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def binarySort(key_arrs, lo, hi, start, data):
    assert lo <= start and start <= hi
    if start == lo:
        start += 1
    while start < hi:
        tatmu__gtihe = getitem_arr_tup(key_arrs, start)
        ovc__fldi = getitem_arr_tup(data, start)
        fbi__rnyj = lo
        gdc__sef = start
        assert fbi__rnyj <= gdc__sef
        while fbi__rnyj < gdc__sef:
            oqrno__uln = fbi__rnyj + gdc__sef >> 1
            if tatmu__gtihe < getitem_arr_tup(key_arrs, oqrno__uln):
                gdc__sef = oqrno__uln
            else:
                fbi__rnyj = oqrno__uln + 1
        assert fbi__rnyj == gdc__sef
        n = start - fbi__rnyj
        copyRange_tup(key_arrs, fbi__rnyj, key_arrs, fbi__rnyj + 1, n)
        copyRange_tup(data, fbi__rnyj, data, fbi__rnyj + 1, n)
        setitem_arr_tup(key_arrs, fbi__rnyj, tatmu__gtihe)
        setitem_arr_tup(data, fbi__rnyj, ovc__fldi)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    wvr__euoq = lo + 1
    if wvr__euoq == hi:
        return 1
    if getitem_arr_tup(key_arrs, wvr__euoq) < getitem_arr_tup(key_arrs, lo):
        wvr__euoq += 1
        while wvr__euoq < hi and getitem_arr_tup(key_arrs, wvr__euoq
            ) < getitem_arr_tup(key_arrs, wvr__euoq - 1):
            wvr__euoq += 1
        reverseRange(key_arrs, lo, wvr__euoq, data)
    else:
        wvr__euoq += 1
        while wvr__euoq < hi and getitem_arr_tup(key_arrs, wvr__euoq
            ) >= getitem_arr_tup(key_arrs, wvr__euoq - 1):
            wvr__euoq += 1
    return wvr__euoq - lo


@numba.njit(no_cpython_wrapper=True, cache=True)
def reverseRange(key_arrs, lo, hi, data):
    hi -= 1
    while lo < hi:
        swap_arrs(key_arrs, lo, hi)
        swap_arrs(data, lo, hi)
        lo += 1
        hi -= 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def minRunLength(n):
    assert n >= 0
    jto__emnes = 0
    while n >= MIN_MERGE:
        jto__emnes |= n & 1
        n >>= 1
    return n + jto__emnes


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    kgia__pjyoh = len(key_arrs[0])
    tmpLength = (kgia__pjyoh >> 1 if kgia__pjyoh < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    lct__jghd = (5 if kgia__pjyoh < 120 else 10 if kgia__pjyoh < 1542 else 
        19 if kgia__pjyoh < 119151 else 40)
    runBase = np.empty(lct__jghd, np.int64)
    runLen = np.empty(lct__jghd, np.int64)
    return stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def pushRun(stackSize, runBase, runLen, runBase_val, runLen_val):
    runBase[stackSize] = runBase_val
    runLen[stackSize] = runLen_val
    stackSize += 1
    return stackSize


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeCollapse(stackSize, runBase, runLen, key_arrs, data, tmpLength,
    tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n >= 1 and runLen[n - 1] <= runLen[n] + runLen[n + 1
            ] or n >= 2 and runLen[n - 2] <= runLen[n] + runLen[n - 1]:
            if runLen[n - 1] < runLen[n + 1]:
                n -= 1
        elif runLen[n] > runLen[n + 1]:
            break
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeForceCollapse(stackSize, runBase, runLen, key_arrs, data,
    tmpLength, tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n > 0 and runLen[n - 1] < runLen[n + 1]:
            n -= 1
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeAt(stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
    tmp_data, minGallop, i):
    assert stackSize >= 2
    assert i >= 0
    assert i == stackSize - 2 or i == stackSize - 3
    base1 = runBase[i]
    len1 = runLen[i]
    base2 = runBase[i + 1]
    len2 = runLen[i + 1]
    assert len1 > 0 and len2 > 0
    assert base1 + len1 == base2
    runLen[i] = len1 + len2
    if i == stackSize - 3:
        runBase[i + 1] = runBase[i + 2]
        runLen[i + 1] = runLen[i + 2]
    stackSize -= 1
    hzs__jnf = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert hzs__jnf >= 0
    base1 += hzs__jnf
    len1 -= hzs__jnf
    if len1 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    len2 = gallopLeft(getitem_arr_tup(key_arrs, base1 + len1 - 1), key_arrs,
        base2, len2, len2 - 1)
    assert len2 >= 0
    if len2 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    if len1 <= len2:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len1)
        minGallop = mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    else:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len2)
        minGallop = mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopLeft(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    tar__cwvc = 0
    pren__umg = 1
    if key > getitem_arr_tup(arr, base + hint):
        vet__ksr = _len - hint
        while pren__umg < vet__ksr and key > getitem_arr_tup(arr, base +
            hint + pren__umg):
            tar__cwvc = pren__umg
            pren__umg = (pren__umg << 1) + 1
            if pren__umg <= 0:
                pren__umg = vet__ksr
        if pren__umg > vet__ksr:
            pren__umg = vet__ksr
        tar__cwvc += hint
        pren__umg += hint
    else:
        vet__ksr = hint + 1
        while pren__umg < vet__ksr and key <= getitem_arr_tup(arr, base +
            hint - pren__umg):
            tar__cwvc = pren__umg
            pren__umg = (pren__umg << 1) + 1
            if pren__umg <= 0:
                pren__umg = vet__ksr
        if pren__umg > vet__ksr:
            pren__umg = vet__ksr
        tmp = tar__cwvc
        tar__cwvc = hint - pren__umg
        pren__umg = hint - tmp
    assert -1 <= tar__cwvc and tar__cwvc < pren__umg and pren__umg <= _len
    tar__cwvc += 1
    while tar__cwvc < pren__umg:
        zhf__zty = tar__cwvc + (pren__umg - tar__cwvc >> 1)
        if key > getitem_arr_tup(arr, base + zhf__zty):
            tar__cwvc = zhf__zty + 1
        else:
            pren__umg = zhf__zty
    assert tar__cwvc == pren__umg
    return pren__umg


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    pren__umg = 1
    tar__cwvc = 0
    if key < getitem_arr_tup(arr, base + hint):
        vet__ksr = hint + 1
        while pren__umg < vet__ksr and key < getitem_arr_tup(arr, base +
            hint - pren__umg):
            tar__cwvc = pren__umg
            pren__umg = (pren__umg << 1) + 1
            if pren__umg <= 0:
                pren__umg = vet__ksr
        if pren__umg > vet__ksr:
            pren__umg = vet__ksr
        tmp = tar__cwvc
        tar__cwvc = hint - pren__umg
        pren__umg = hint - tmp
    else:
        vet__ksr = _len - hint
        while pren__umg < vet__ksr and key >= getitem_arr_tup(arr, base +
            hint + pren__umg):
            tar__cwvc = pren__umg
            pren__umg = (pren__umg << 1) + 1
            if pren__umg <= 0:
                pren__umg = vet__ksr
        if pren__umg > vet__ksr:
            pren__umg = vet__ksr
        tar__cwvc += hint
        pren__umg += hint
    assert -1 <= tar__cwvc and tar__cwvc < pren__umg and pren__umg <= _len
    tar__cwvc += 1
    while tar__cwvc < pren__umg:
        zhf__zty = tar__cwvc + (pren__umg - tar__cwvc >> 1)
        if key < getitem_arr_tup(arr, base + zhf__zty):
            pren__umg = zhf__zty
        else:
            tar__cwvc = zhf__zty + 1
    assert tar__cwvc == pren__umg
    return pren__umg


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base1, tmp, 0, len1)
    copyRange_tup(arr_data, base1, tmp_data, 0, len1)
    cursor1 = 0
    cursor2 = base2
    dest = base1
    setitem_arr_tup(arr, dest, getitem_arr_tup(arr, cursor2))
    copyElement_tup(arr_data, cursor2, arr_data, dest)
    cursor2 += 1
    dest += 1
    len2 -= 1
    if len2 == 0:
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
        return minGallop
    if len1 == 1:
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
        return minGallop
    len1, len2, cursor1, cursor2, dest, minGallop = mergeLo_inner(key_arrs,
        data, tmp_data, len1, len2, tmp, cursor1, cursor2, dest, minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len1 == 1:
        assert len2 > 0
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
    elif len1 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len2 == 0
        assert len1 > 1
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo_inner(arr, arr_data, tmp_data, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        mfxn__kek = 0
        hax__dot = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                hax__dot += 1
                mfxn__kek = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                mfxn__kek += 1
                hax__dot = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not mfxn__kek | hax__dot < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            mfxn__kek = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if mfxn__kek != 0:
                copyRange_tup(tmp, cursor1, arr, dest, mfxn__kek)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, mfxn__kek)
                dest += mfxn__kek
                cursor1 += mfxn__kek
                len1 -= mfxn__kek
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            hax__dot = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if hax__dot != 0:
                copyRange_tup(arr, cursor2, arr, dest, hax__dot)
                copyRange_tup(arr_data, cursor2, arr_data, dest, hax__dot)
                dest += hax__dot
                cursor2 += hax__dot
                len2 -= hax__dot
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor1, arr, dest)
            copyElement_tup(tmp_data, cursor1, arr_data, dest)
            cursor1 += 1
            dest += 1
            len1 -= 1
            if len1 == 1:
                return len1, len2, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not mfxn__kek >= MIN_GALLOP | hax__dot >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base2, tmp, 0, len2)
    copyRange_tup(arr_data, base2, tmp_data, 0, len2)
    cursor1 = base1 + len1 - 1
    cursor2 = len2 - 1
    dest = base2 + len2 - 1
    copyElement_tup(arr, cursor1, arr, dest)
    copyElement_tup(arr_data, cursor1, arr_data, dest)
    cursor1 -= 1
    dest -= 1
    len1 -= 1
    if len1 == 0:
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
        return minGallop
    if len2 == 1:
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
        return minGallop
    len1, len2, tmp, cursor1, cursor2, dest, minGallop = mergeHi_inner(key_arrs
        , data, tmp_data, base1, len1, len2, tmp, cursor1, cursor2, dest,
        minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len2 == 1:
        assert len1 > 0
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
    elif len2 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len1 == 0
        assert len2 > 0
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi_inner(arr, arr_data, tmp_data, base1, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        mfxn__kek = 0
        hax__dot = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                mfxn__kek += 1
                hax__dot = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                hax__dot += 1
                mfxn__kek = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not mfxn__kek | hax__dot < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            mfxn__kek = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if mfxn__kek != 0:
                dest -= mfxn__kek
                cursor1 -= mfxn__kek
                len1 -= mfxn__kek
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, mfxn__kek)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    mfxn__kek)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            hax__dot = len2 - gallopLeft(getitem_arr_tup(arr, cursor1), tmp,
                0, len2, len2 - 1)
            if hax__dot != 0:
                dest -= hax__dot
                cursor2 -= hax__dot
                len2 -= hax__dot
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, hax__dot)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    hax__dot)
                if len2 <= 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor1, arr, dest)
            copyElement_tup(arr_data, cursor1, arr_data, dest)
            cursor1 -= 1
            dest -= 1
            len1 -= 1
            if len1 == 0:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not mfxn__kek >= MIN_GALLOP | hax__dot >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    oulfn__vzaoq = len(key_arrs[0])
    if tmpLength < minCapacity:
        emoe__qvenq = minCapacity
        emoe__qvenq |= emoe__qvenq >> 1
        emoe__qvenq |= emoe__qvenq >> 2
        emoe__qvenq |= emoe__qvenq >> 4
        emoe__qvenq |= emoe__qvenq >> 8
        emoe__qvenq |= emoe__qvenq >> 16
        emoe__qvenq += 1
        if emoe__qvenq < 0:
            emoe__qvenq = minCapacity
        else:
            emoe__qvenq = min(emoe__qvenq, oulfn__vzaoq >> 1)
        tmp = alloc_arr_tup(emoe__qvenq, key_arrs)
        tmp_data = alloc_arr_tup(emoe__qvenq, data)
        tmpLength = emoe__qvenq
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        mzyrj__geh = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = mzyrj__geh


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    gtqt__sswck = arr_tup.count
    tkm__diy = 'def f(arr_tup, lo, hi):\n'
    for i in range(gtqt__sswck):
        tkm__diy += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        tkm__diy += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        tkm__diy += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    tkm__diy += '  return\n'
    mpig__vudsl = {}
    exec(tkm__diy, {}, mpig__vudsl)
    ieqjd__yhwc = mpig__vudsl['f']
    return ieqjd__yhwc


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    gtqt__sswck = src_arr_tup.count
    assert gtqt__sswck == dst_arr_tup.count
    tkm__diy = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(gtqt__sswck):
        tkm__diy += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    tkm__diy += '  return\n'
    mpig__vudsl = {}
    exec(tkm__diy, {'copyRange': copyRange}, mpig__vudsl)
    vxbk__xvz = mpig__vudsl['f']
    return vxbk__xvz


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    gtqt__sswck = src_arr_tup.count
    assert gtqt__sswck == dst_arr_tup.count
    tkm__diy = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(gtqt__sswck):
        tkm__diy += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    tkm__diy += '  return\n'
    mpig__vudsl = {}
    exec(tkm__diy, {'copyElement': copyElement}, mpig__vudsl)
    vxbk__xvz = mpig__vudsl['f']
    return vxbk__xvz


def getitem_arr_tup(arr_tup, ind):
    kcjv__qlqfx = [arr[ind] for arr in arr_tup]
    return tuple(kcjv__qlqfx)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    gtqt__sswck = arr_tup.count
    tkm__diy = 'def f(arr_tup, ind):\n'
    tkm__diy += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(gtqt__sswck)]), ',' if gtqt__sswck == 1 else
        '')
    mpig__vudsl = {}
    exec(tkm__diy, {}, mpig__vudsl)
    flfw__wuow = mpig__vudsl['f']
    return flfw__wuow


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, dkxp__zzb in zip(arr_tup, val_tup):
        arr[ind] = dkxp__zzb


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    gtqt__sswck = arr_tup.count
    tkm__diy = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(gtqt__sswck):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            tkm__diy += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            tkm__diy += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    tkm__diy += '  return\n'
    mpig__vudsl = {}
    exec(tkm__diy, {}, mpig__vudsl)
    flfw__wuow = mpig__vudsl['f']
    return flfw__wuow


def test():
    import time
    xwgbi__icnx = time.time()
    umc__yqc = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((umc__yqc,), 0, 3, data)
    print('compile time', time.time() - xwgbi__icnx)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    znu__bftp = np.random.ranf(n)
    zsbt__ezg = pd.DataFrame({'A': znu__bftp, 'B': data[0], 'C': data[1]})
    xwgbi__icnx = time.time()
    wyfb__fmy = zsbt__ezg.sort_values('A', inplace=False)
    wvq__wbi = time.time()
    sort((znu__bftp,), 0, n, data)
    print('Bodo', time.time() - wvq__wbi, 'Numpy', wvq__wbi - xwgbi__icnx)
    np.testing.assert_almost_equal(data[0], wyfb__fmy.B.values)
    np.testing.assert_almost_equal(data[1], wyfb__fmy.C.values)


if __name__ == '__main__':
    test()
