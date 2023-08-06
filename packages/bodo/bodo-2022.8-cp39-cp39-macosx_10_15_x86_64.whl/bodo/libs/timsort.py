import numba
import numpy as np
import pandas as pd
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    uqlk__sazz = hi - lo
    if uqlk__sazz < 2:
        return
    if uqlk__sazz < MIN_MERGE:
        ccs__sifsb = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + ccs__sifsb, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    skah__zer = minRunLength(uqlk__sazz)
    while True:
        toj__hycy = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if toj__hycy < skah__zer:
            exwt__wcxl = uqlk__sazz if uqlk__sazz <= skah__zer else skah__zer
            binarySort(key_arrs, lo, lo + exwt__wcxl, lo + toj__hycy, data)
            toj__hycy = exwt__wcxl
        stackSize = pushRun(stackSize, runBase, runLen, lo, toj__hycy)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += toj__hycy
        uqlk__sazz -= toj__hycy
        if uqlk__sazz == 0:
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
        tmls__herge = getitem_arr_tup(key_arrs, start)
        xodl__ealp = getitem_arr_tup(data, start)
        rhkjb__apsr = lo
        kkfsa__cmk = start
        assert rhkjb__apsr <= kkfsa__cmk
        while rhkjb__apsr < kkfsa__cmk:
            idvxy__sja = rhkjb__apsr + kkfsa__cmk >> 1
            if tmls__herge < getitem_arr_tup(key_arrs, idvxy__sja):
                kkfsa__cmk = idvxy__sja
            else:
                rhkjb__apsr = idvxy__sja + 1
        assert rhkjb__apsr == kkfsa__cmk
        n = start - rhkjb__apsr
        copyRange_tup(key_arrs, rhkjb__apsr, key_arrs, rhkjb__apsr + 1, n)
        copyRange_tup(data, rhkjb__apsr, data, rhkjb__apsr + 1, n)
        setitem_arr_tup(key_arrs, rhkjb__apsr, tmls__herge)
        setitem_arr_tup(data, rhkjb__apsr, xodl__ealp)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    xdac__dtps = lo + 1
    if xdac__dtps == hi:
        return 1
    if getitem_arr_tup(key_arrs, xdac__dtps) < getitem_arr_tup(key_arrs, lo):
        xdac__dtps += 1
        while xdac__dtps < hi and getitem_arr_tup(key_arrs, xdac__dtps
            ) < getitem_arr_tup(key_arrs, xdac__dtps - 1):
            xdac__dtps += 1
        reverseRange(key_arrs, lo, xdac__dtps, data)
    else:
        xdac__dtps += 1
        while xdac__dtps < hi and getitem_arr_tup(key_arrs, xdac__dtps
            ) >= getitem_arr_tup(key_arrs, xdac__dtps - 1):
            xdac__dtps += 1
    return xdac__dtps - lo


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
    bqj__vsq = 0
    while n >= MIN_MERGE:
        bqj__vsq |= n & 1
        n >>= 1
    return n + bqj__vsq


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    cje__togm = len(key_arrs[0])
    tmpLength = (cje__togm >> 1 if cje__togm < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    batyn__xipnd = (5 if cje__togm < 120 else 10 if cje__togm < 1542 else 
        19 if cje__togm < 119151 else 40)
    runBase = np.empty(batyn__xipnd, np.int64)
    runLen = np.empty(batyn__xipnd, np.int64)
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
    kdg__ufcd = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert kdg__ufcd >= 0
    base1 += kdg__ufcd
    len1 -= kdg__ufcd
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
    jyoqo__qze = 0
    emq__dhgkw = 1
    if key > getitem_arr_tup(arr, base + hint):
        brpmy__yml = _len - hint
        while emq__dhgkw < brpmy__yml and key > getitem_arr_tup(arr, base +
            hint + emq__dhgkw):
            jyoqo__qze = emq__dhgkw
            emq__dhgkw = (emq__dhgkw << 1) + 1
            if emq__dhgkw <= 0:
                emq__dhgkw = brpmy__yml
        if emq__dhgkw > brpmy__yml:
            emq__dhgkw = brpmy__yml
        jyoqo__qze += hint
        emq__dhgkw += hint
    else:
        brpmy__yml = hint + 1
        while emq__dhgkw < brpmy__yml and key <= getitem_arr_tup(arr, base +
            hint - emq__dhgkw):
            jyoqo__qze = emq__dhgkw
            emq__dhgkw = (emq__dhgkw << 1) + 1
            if emq__dhgkw <= 0:
                emq__dhgkw = brpmy__yml
        if emq__dhgkw > brpmy__yml:
            emq__dhgkw = brpmy__yml
        tmp = jyoqo__qze
        jyoqo__qze = hint - emq__dhgkw
        emq__dhgkw = hint - tmp
    assert -1 <= jyoqo__qze and jyoqo__qze < emq__dhgkw and emq__dhgkw <= _len
    jyoqo__qze += 1
    while jyoqo__qze < emq__dhgkw:
        cvdsj__xnx = jyoqo__qze + (emq__dhgkw - jyoqo__qze >> 1)
        if key > getitem_arr_tup(arr, base + cvdsj__xnx):
            jyoqo__qze = cvdsj__xnx + 1
        else:
            emq__dhgkw = cvdsj__xnx
    assert jyoqo__qze == emq__dhgkw
    return emq__dhgkw


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    emq__dhgkw = 1
    jyoqo__qze = 0
    if key < getitem_arr_tup(arr, base + hint):
        brpmy__yml = hint + 1
        while emq__dhgkw < brpmy__yml and key < getitem_arr_tup(arr, base +
            hint - emq__dhgkw):
            jyoqo__qze = emq__dhgkw
            emq__dhgkw = (emq__dhgkw << 1) + 1
            if emq__dhgkw <= 0:
                emq__dhgkw = brpmy__yml
        if emq__dhgkw > brpmy__yml:
            emq__dhgkw = brpmy__yml
        tmp = jyoqo__qze
        jyoqo__qze = hint - emq__dhgkw
        emq__dhgkw = hint - tmp
    else:
        brpmy__yml = _len - hint
        while emq__dhgkw < brpmy__yml and key >= getitem_arr_tup(arr, base +
            hint + emq__dhgkw):
            jyoqo__qze = emq__dhgkw
            emq__dhgkw = (emq__dhgkw << 1) + 1
            if emq__dhgkw <= 0:
                emq__dhgkw = brpmy__yml
        if emq__dhgkw > brpmy__yml:
            emq__dhgkw = brpmy__yml
        jyoqo__qze += hint
        emq__dhgkw += hint
    assert -1 <= jyoqo__qze and jyoqo__qze < emq__dhgkw and emq__dhgkw <= _len
    jyoqo__qze += 1
    while jyoqo__qze < emq__dhgkw:
        cvdsj__xnx = jyoqo__qze + (emq__dhgkw - jyoqo__qze >> 1)
        if key < getitem_arr_tup(arr, base + cvdsj__xnx):
            emq__dhgkw = cvdsj__xnx
        else:
            jyoqo__qze = cvdsj__xnx + 1
    assert jyoqo__qze == emq__dhgkw
    return emq__dhgkw


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
        ahe__aydl = 0
        bqln__gyo = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                bqln__gyo += 1
                ahe__aydl = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                ahe__aydl += 1
                bqln__gyo = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not ahe__aydl | bqln__gyo < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            ahe__aydl = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if ahe__aydl != 0:
                copyRange_tup(tmp, cursor1, arr, dest, ahe__aydl)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, ahe__aydl)
                dest += ahe__aydl
                cursor1 += ahe__aydl
                len1 -= ahe__aydl
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            bqln__gyo = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if bqln__gyo != 0:
                copyRange_tup(arr, cursor2, arr, dest, bqln__gyo)
                copyRange_tup(arr_data, cursor2, arr_data, dest, bqln__gyo)
                dest += bqln__gyo
                cursor2 += bqln__gyo
                len2 -= bqln__gyo
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
            if not ahe__aydl >= MIN_GALLOP | bqln__gyo >= MIN_GALLOP:
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
        ahe__aydl = 0
        bqln__gyo = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                ahe__aydl += 1
                bqln__gyo = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                bqln__gyo += 1
                ahe__aydl = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not ahe__aydl | bqln__gyo < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            ahe__aydl = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if ahe__aydl != 0:
                dest -= ahe__aydl
                cursor1 -= ahe__aydl
                len1 -= ahe__aydl
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, ahe__aydl)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    ahe__aydl)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            bqln__gyo = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if bqln__gyo != 0:
                dest -= bqln__gyo
                cursor2 -= bqln__gyo
                len2 -= bqln__gyo
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, bqln__gyo)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    bqln__gyo)
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
            if not ahe__aydl >= MIN_GALLOP | bqln__gyo >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    bbi__nqk = len(key_arrs[0])
    if tmpLength < minCapacity:
        qvf__yfxo = minCapacity
        qvf__yfxo |= qvf__yfxo >> 1
        qvf__yfxo |= qvf__yfxo >> 2
        qvf__yfxo |= qvf__yfxo >> 4
        qvf__yfxo |= qvf__yfxo >> 8
        qvf__yfxo |= qvf__yfxo >> 16
        qvf__yfxo += 1
        if qvf__yfxo < 0:
            qvf__yfxo = minCapacity
        else:
            qvf__yfxo = min(qvf__yfxo, bbi__nqk >> 1)
        tmp = alloc_arr_tup(qvf__yfxo, key_arrs)
        tmp_data = alloc_arr_tup(qvf__yfxo, data)
        tmpLength = qvf__yfxo
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        thwt__adw = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = thwt__adw


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    ngjqu__ckd = arr_tup.count
    jcxh__bcim = 'def f(arr_tup, lo, hi):\n'
    for i in range(ngjqu__ckd):
        jcxh__bcim += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        jcxh__bcim += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        jcxh__bcim += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    jcxh__bcim += '  return\n'
    csesw__lkm = {}
    exec(jcxh__bcim, {}, csesw__lkm)
    qwyxs__mkm = csesw__lkm['f']
    return qwyxs__mkm


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    ngjqu__ckd = src_arr_tup.count
    assert ngjqu__ckd == dst_arr_tup.count
    jcxh__bcim = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(ngjqu__ckd):
        jcxh__bcim += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    jcxh__bcim += '  return\n'
    csesw__lkm = {}
    exec(jcxh__bcim, {'copyRange': copyRange}, csesw__lkm)
    tup__ykm = csesw__lkm['f']
    return tup__ykm


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    ngjqu__ckd = src_arr_tup.count
    assert ngjqu__ckd == dst_arr_tup.count
    jcxh__bcim = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(ngjqu__ckd):
        jcxh__bcim += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    jcxh__bcim += '  return\n'
    csesw__lkm = {}
    exec(jcxh__bcim, {'copyElement': copyElement}, csesw__lkm)
    tup__ykm = csesw__lkm['f']
    return tup__ykm


def getitem_arr_tup(arr_tup, ind):
    rzfz__aqpbv = [arr[ind] for arr in arr_tup]
    return tuple(rzfz__aqpbv)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    ngjqu__ckd = arr_tup.count
    jcxh__bcim = 'def f(arr_tup, ind):\n'
    jcxh__bcim += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(ngjqu__ckd)]), ',' if ngjqu__ckd == 1 else '')
    csesw__lkm = {}
    exec(jcxh__bcim, {}, csesw__lkm)
    mgnia__vrwr = csesw__lkm['f']
    return mgnia__vrwr


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, lwd__zdjqw in zip(arr_tup, val_tup):
        arr[ind] = lwd__zdjqw


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    ngjqu__ckd = arr_tup.count
    jcxh__bcim = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(ngjqu__ckd):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            jcxh__bcim += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            jcxh__bcim += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    jcxh__bcim += '  return\n'
    csesw__lkm = {}
    exec(jcxh__bcim, {}, csesw__lkm)
    mgnia__vrwr = csesw__lkm['f']
    return mgnia__vrwr


def test():
    import time
    wmcte__nktj = time.time()
    rxdpb__ijc = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((rxdpb__ijc,), 0, 3, data)
    print('compile time', time.time() - wmcte__nktj)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    cyjnu__jligj = np.random.ranf(n)
    vhuk__uzuvr = pd.DataFrame({'A': cyjnu__jligj, 'B': data[0], 'C': data[1]})
    wmcte__nktj = time.time()
    cegs__gzv = vhuk__uzuvr.sort_values('A', inplace=False)
    vof__yluw = time.time()
    sort((cyjnu__jligj,), 0, n, data)
    print('Bodo', time.time() - vof__yluw, 'Numpy', vof__yluw - wmcte__nktj)
    np.testing.assert_almost_equal(data[0], cegs__gzv.B.values)
    np.testing.assert_almost_equal(data[1], cegs__gzv.C.values)


if __name__ == '__main__':
    test()
