"""Package teneva, module collection.matrices: various useful QTT-matrices.

This module contains the collection of functions for explicit construction of
various useful QTT-matrices (delta function and others).

"""
import numpy as np


from .vectors import _index_expand
from .vectors import _index_prepare
import teneva


def matrix_delta(q, i, j, v=1.):
    """Build QTT-matrix that is zero everywhere except for a given 2D index.

    Args:
        q (int): quantization level. The resulting matrix will have the shape
            2^q x 2^q (> 0).
        i (int): the col index for nonzero element (< 2^q). Note that "negative
            index notation" is supported.
        j (int): the row index for nonzero element (< 2^q). Note that "negative
            index notation" is supported.
        v (float): the value of the matrix at index "i, j".

    Returns:
        list: TT-tensor with 4D TT-cores representing the QTT-matrix.

    """
    i = _index_prepare(q, i)
    j = _index_prepare(q, j)
    ind_col = _index_expand(q, i)
    ind_row = _index_expand(q, j)
    Y = []
    for k in range(q):
        G = np.zeros((1, 2, 2, 1))
        G[0, ind_col[k], ind_row[k], 0] = 1.
        Y.append(G)
    Y[-1][0, ind_col[-1], ind_row[-1], 0] = v
    return Y


def matrix_toeplitz(x, d=None, D=None, kind='F'):
    """ Creates multilevel Toeplitz TT-matrix with ``D`` levels.

        # Arbitrary multilevel Toeplitz _matrix

        Possible _matrix types:

        * 'F' - full Toeplitz _matrix,             size(x) = 2^{d+1}
        * 'C' - circulant _matrix,                 size(x) = 2^d
        * 'L' - lower triangular Toeplitz _matrix, size(x) = 2^d
        * 'U' - upper triangular Toeplitz _matrix, size(x) = 2^d

        Sample calls:

        >>> # one-level Toeplitz _matrix:
        >>> T = tt.Toeplitz(x)
        >>> # one-level circulant _matrix:
        >>> T = tt.Toeplitz(x, kind='C')
        >>> # three-level upper-triangular Toeplitz _matrix:
        >>> T = tt.Toeplitz(x, D=3, kind='U')
        >>> # two-level mixed-type Toeplitz _matrix:
        >>> T = tt.Toeplitz(x, kind=['L', 'U'])
        >>> # two-level mixed-size Toeplitz _matrix:
        >>> T = tt.Toeplitz(x, [3, 4], kind='C')

    """

    # checking for arguments consistency
    def check_kinds(D, kind):
        if D % len(kind) == 0:
            kind.extend(kind * (D // len(kind) - 1))
        if len(kind) != D:
            raise ValueError(
                "Must give proper amount of _matrix kinds (one or D, for example)")

    dim = len(x)

    kind = list(kind)
    if not set(kind).issubset(['F', 'C', 'L', 'U']):
        raise ValueError("Toeplitz _matrix kind must be one of F, C, L, U.")
    if d is None:
        if D is None:
            D = len(kind)
        if dim % D:
            raise ValueError(
                "dim must be divisible by D when d is not specified!")
        if len(kind) == 1:
            d = np.array([dim // D - (1 if kind[0] == 'F' else 0)]
                          * D, dtype=np.int32)
            kind = kind * D
        else:
            check_kinds(D, kind)
            if set(kind).issubset(['F']):
                d = np.array([dim // D - 1] * D, dtype=np.int32)
            elif set(kind).issubset(['C', 'L', 'U']):
                d = np.array([dim // D] * D, dtype=np.int32)
            else:
                raise ValueError(
                    "Only similar _matrix kinds (only F or only C, L and U) are accepted when d is not specified!")
    elif d is not None:
        d = np.asarray(d, dtype=np.int32).flatten()
        if D is None:
            D = d.size
        elif d.size == 1:
            d = np.array([d[0]] * D, dtype=np.int32)
        if D != d.size:
            raise ValueError("D must be equal to len(d)")
        check_kinds(D, kind)
        if np.sum(d) + np.sum([(1 if knd == 'F' else 0)
                                 for knd in kind]) != dim:
            raise ValueError(
                "Dimensions inconsistency: dim != d_1 + d_2 + ... + d_D")

    I = [[1, 0], [0, 1]]

    J = [[0, 1], [0, 0]]

    JT = [[0, 0], [1, 0]]

    H = [[0, 1], [1, 0]]

    S = np.array([[[0], [1]], [[1], [0]]]).transpose()  # 2 x 2 x 1

    P = np.zeros((2, 2, 2, 2))
    P[:, :, 0, 0] = I
    P[:, :, 1, 0] = H
    P[:, :, 0, 1] = H
    P[:, :, 1, 1] = I
    P = np.transpose(P)  # 2 x 2! x 2 x 2 x '1'

    Q = np.zeros((2, 2, 2, 2))
    Q[:, :, 0, 0] = I
    Q[:, :, 1, 0] = JT
    Q[:, :, 0, 1] = JT
    Q = np.transpose(Q)  # 2 x 2! x 2 x 2 x '1'

    R = np.zeros((2, 2, 2, 2))
    R[:, :, 1, 0] = J
    R[:, :, 0, 1] = J
    R[:, :, 1, 1] = I
    R = np.transpose(R)  # 2 x 2! x 2 x 2 x '1'

    W = np.zeros([2] * 5)  # 2 x 2! x 2 x 2 x 2
    W[0, :, :, 0, 0] = W[1, :, :, 1, 1] = I
    W[0, :, :, 1, 0] = W[0, :, :, 0, 1] = JT
    W[1, :, :, 1, 0] = W[1, :, :, 0, 1] = J
    W = np.transpose(W)  # 2 x 2! x 2 x 2 x 2

    V = np.zeros((2, 2, 2, 2))
    V[0, :, :, 0] = I
    V[0, :, :, 1] = JT
    V[1, :, :, 1] = J
    V = np.transpose(V)  # '1' x 2! x 2 x 2 x 2

    crs = []
    xcrs = x # _vector.vector.to_list(x)
    ranks = teneva.ranks(x)
    dp = 0  # dimensions passed
    for j in range(D):
        currd = d[j]
        xcr = xcrs[dp]
        cr = np.tensordot(V, xcr, (0, 1))
        cr = cr.transpose(3, 0, 1, 2, 4)  # <r_dp| x 2 x 2 x |2> x |r_{dp+1}>
        cr = cr.reshape((ranks[dp], 2, 2, 2 * ranks[dp + 1]),
                        order='F')  # <r_dp| x 2 x 2 x |2r_{dp+1}>
        dp += 1
        crs.append(cr)
        for i in range(1, currd - 1):
            xcr = xcrs[dp]
            # (<2| x 2 x 2 x |2>) x <r_dp| x |r_{dp+1}>
            cr = np.tensordot(W, xcr, (1, 1))
            # <2| x <r_dp| x 2 x 2 x |2> x |r_{dp+1}>
            cr = cr.transpose([0, 4, 1, 2, 3, 5])
            # <2r_dp| x 2 x 2 x |2r_{dp+1}>
            cr = cr.reshape((2 * ranks[dp], 2, 2, 2 * ranks[dp + 1]), order='F')
            dp += 1
            crs.append(cr)

        if kind[j] == 'F':
            xcr = xcrs[dp]  # r_dp x 2 x r_{dp+1}
            cr = np.tensordot(W, xcr, (1, 1)).transpose([0, 4, 1, 2, 3, 5])
            # <2r_dp| x 2 x 2 x |2r_{dp+1}>
            cr = cr.reshape((2 * ranks[dp], 2, 2, 2 * ranks[dp + 1]), order='F')
            dp += 1
            xcr = xcrs[dp]  # r_dp x 2 x r_{dp+1}
            # <2| x |1> x <r_dp| x |r_{dp+1}>
            tmp = np.tensordot(S, xcr, (1, 1))
            # tmp = tmp.transpose([0, 2, 1, 3]) # TODO: figure out WHY THE HELL
            # this spoils everything
            # <2r_dp| x |r_{dp+1}>
            tmp = tmp.reshape((2 * ranks[dp], ranks[dp + 1]), order='F')
            # <2r_{dp-1}| x 2 x 2 x |r_{dp+1}>
            cr = np.tensordot(cr, tmp, (3, 0))
            dp += 1
            crs.append(cr)

        else:
            dotcore = None
            if kind[j] == 'C':
                dotcore = P
            elif kind[j] == 'L':
                dotcore = Q
            elif kind[j] == 'U':
                dotcore = R
            xcr = xcrs[dp]  # r_dp x 2 x r_{dp+1}
            # <2| x 2 x 2 x |'1'> x <r_dp| x |r_{dp+1}>
            cr = np.tensordot(dotcore, xcr, (1, 1))
            # <2| x <r_dp| x 2 x 2 x |r_{dp+1}>
            cr = cr.transpose([0, 3, 1, 2, 4])
            cr = cr.reshape((2 * ranks[dp], 2, 2, ranks[dp + 1]), order='F')
            dp += 1
            crs.append(cr)

    return crs
