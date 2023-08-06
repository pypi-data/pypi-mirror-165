import math
import numpy as np
import teneva


from .act_cross_utils import _core_update

from .act_cross_utils import _dot_maxvol
from .act_cross_utils import _svd_solve
from .act_cross_utils import _svd_solve_tr
from .act_cross_utils import _func_y
from .act_cross_utils import _func_z
from .act_cross_utils import _svd
from .act_cross_utils import xxx

from .act_cross_utils import _inter_build
from .act_cross_utils import _inter_update


def act_cross(f, X_list, Y0, eps=1.E-6, eps_exit=1.E-6, nswp=10, rmax=9999999, log=False, kickrank=5, kickrank2=0, d2=1):
    D = len(X_list)               # Number of function inputs
    d = len(X_list[0])            # Dimension of the (any) input tensor
    n = teneva.shape(X_list[0])   # Shape of the (any) input tensor

    # TT-cores of all input tensors (array of shape [d, D] of 3D arrays):
    X = np.array([[G.copy() for G in X] for X in X_list], dtype=np.object).T

    # TT-ranks of all input tensors (array of shape [d+1, D] of int):
    R_all = np.array([teneva.ranks(X) for X in X_list]).T

    # TT-tensor for solution:
    Y = teneva.copy(Y0)
    ry = teneva.ranks(Y0)

    # TT-tensor for error:
    if kickrank > 0:
        z = teneva.tensor_rand(n, kickrank)
        rz = teneva.ranks(z)
    else:
        # TODO !!!!
        z = [None for _ in range(d)]
        rz = np.zeros(d+1, dtype=int)

    # Interface matrices:
    Rx, Ry, Rz, Rxz, Ryz = _inter_build(d, D)

    for i in range(0, d-1):
        teneva.orthogonalize_left(Y, i, inplace=True)
        ry[i+1] = Y[i].shape[-1]

        if kickrank > 0:
            teneva.orthogonalize_left(z, i, inplace=True)
            rz[i+1] = z[i].shape[-1]

        Rx[i+1, :], Ry[i+1], Rz[i+1], Rxz[i+1, :], Ryz[i+1] = _inter_update(
            X[i, :], Y[i], z[i],
            Rx[i, :], Ry[i], Rz[i], Rxz[i, :], Ryz[i],
            z_rand=True)

    d2 = ry[d]
    ry[d] = 1
    Y[d-1] = np.transpose(Y[d-1], [2, 0, 1])  # permute

    dy_max = 0.
    block_order = [+d, -d]
    order_index = 1
    i = d - 1
    swp = 1
    dirn = int(math.copysign(1, block_order[order_index]))

    while swp <= nswp or dirn > 0:
        Y_old = teneva._reshape(Y[i].copy(), -1)

        Y_new = _func_y(f, X, Rx, Rxz, i, n, D, R_all, ry, rz, is3=True)
        Y_new = teneva._reshape(Y_new, (ry[i], n[i], ry[i+1], d2))
        Y_new = _svd_solve_tr(Y_new, Ry[i], d2)
        Y_new = teneva._reshape(Y_new, (ry[i], n[i], ry[i+1], d2))
        Y_new = _svd_solve(Y_new, Ry[i+1])
        Y_new = teneva._reshape(Y_new, -1)

        dy = teneva.accuracy(Y_old, Y_new)
        dy_max = max(dy_max, dy)

        if dirn > 0:
            Y_new = teneva._reshape(Y_new, (d2, ry[i] * n[i] * ry[i+1]))
            Y_new = teneva._reshape(Y_new.T, (ry[i] * n[i], ry[i+1] * d2))
        else:
            Y_new = teneva._reshape(Y_new, (d2 * ry[i], n[i] * ry[i + 1]))

        u, v = _svd(Y_new, dirn, kickrank, eps, d, rmax, l2r=dirn>0)

        if dirn > 0 and i < d-1:
            if kickrank > 0:
                # Compute the function at residual indices
                zy = _func_y(f, X, Rx, Rxz, i, n, D, R_all, ry, rz)
                zy = teneva._reshape(zy, (-1, d2))

                zz = _func_z(f, X, Rxz, i, n, D, R_all, rz)
                zz = teneva._reshape(zz, (-1, d2))

                # Assemble y at z indices (sic!) and subtract
                dzy = teneva._reshape(u @ v.T, (ry[i], n[i], ry[i+1], d2))
                dzy = xxx(dzy, Ryz[i+1], l2r=True)

                # zy still requires casting from samples to core entities
                zy = teneva._reshape(zy, (ry[i], n[i], rz[i+1], d2))
                zy = _svd_solve_tr(zy, Ry[i], d2)
                zy = zy - dzy

                dzy = teneva._reshape(dzy, (ry[i], n[i], rz[i+1], d2))
                dzy = xxx(dzy, Ryz[i], l2r=False)

                zz = zz - dzy
                # Interpolate all remaining samples into core elements
                zy = teneva._reshape(zy, (ry[i], n[i], rz[i+1], d2))
                zy = _svd_solve(zy, Rz[i+1], kickrank)

                # For z update
                zz = teneva._reshape(zz, (rz[i], n[i] * rz[i + 1] * d2))
                zz = np.linalg.solve(Rz[i], zz)

                zz = teneva._reshape(zz, (rz[i], n[i], rz[i + 1], d2))
                zz = _svd_solve(zz, Rz[i+1], kickrank)

                # Second random kick rank
                zz = np.hstack((zz, np.random.randn(rz[i] * n[i], kickrank2)))
                u, rv = np.linalg.qr(np.hstack((u, zy)))
                radd = zy.shape[1]

                zz, _ = np.linalg.qr(zz)
                rz[i+1] = zz.shape[1]
                z[i] = teneva._reshape(zz, (rz[i], n[i], rz[i+1]))
            else:
                rv = 1
                radd = 0

            v = np.hstack((v, np.zeros((ry[i+1] * d2, radd), dtype=float)))
            v = rv @ v.T

            Y[i] = teneva._reshape(u, (ry[i], n[i], u.shape[1]))
            Y[i+1] = _core_update(Y[i+1], v, Y[i].shape[-1], d2)
            ry[i+1] = Y[i].shape[-1]

            Q = teneva._reshape(zz, (rz[i], n[i], rz[i+1])) # if kickrank > 0 !
            Rx[i+1, :], Ry[i+1], Rz[i+1], Rxz[i+1, :], Ryz[i+1] = _inter_update(
                X[i, :], Y[i], Q,
                Rx[i, :], Ry[i], Rz[i], Rxz[i, :], Ryz[i])

        if dirn < 0 and i > 0:
            if kickrank > 0:
                # AMEN kick. Compute the function at residual indices
                zy = _func_y(f, X, Rx, Rxz, i, n, D, R_all, ry, rz, is2=True)
                zy = teneva._reshape(zy, (-1, d2))

                zz = _func_z(f, X, Rxz, i, n, D, R_all, rz)
                zz = teneva._reshape(zz, (-1, d2))

                # Assemble y at z indices (sic!) and subtract
                dzy = teneva._reshape(u @ v.T, (ry[i], n[i], ry[i+1], d2))
                dzy = xxx(dzy, Ryz[i], l2r=False)

                # zy still requires casting from samples to core entries
                zy = teneva._reshape(zy, (rz[i], n[i], ry[i+1], d2))
                zy = _svd_solve(zy, Ry[i+1])
                zy = zy - dzy

                dzy = teneva._reshape(dzy, (rz[i], n[i], ry[i+1], d2))
                dzy = xxx(dzy, Ryz[i+1], l2r=True)

                zz = zz - dzy

                # Cast sample indices to core elements
                zy = teneva._reshape(zy, (rz[i], n[i], ry[i+1], d2))
                zy = _svd_solve_tr(zy, Rz[i], d2, kickrank)

                zz = teneva._reshape(zz, (rz[i], n[i], rz[i+1], d2))
                zz = _svd_solve_tr(zz, Rz[i], d2, kickrank, R2=Rz[i+1])

                rnd = np.random.randn(n[i] * rz[i + 1], kickrank2)
                zz = np.hstack((zz, rnd))

                v, rv = np.linalg.qr(np.hstack((v, zy)))
                radd = zy.shape[1]
                u = np.hstack((u, np.zeros((d2 * ry[i], radd), dtype=float)))
                u = np.dot(u, rv.T)

                zz, _ = np.linalg.qr(zz)
                rz[i] = zz.shape[1]
                zz = teneva._reshape(zz.T, (rz[i], n[i], rz[i + 1]))
                z[i] = zz

            else:
                rv = 0
                radd = 0

            Y[i] = teneva._reshape(v.T, (v.shape[1], n[i], ry[i+1]))
            Y[i-1] = _core_update(Y[i-1], u, Y[i].shape[0], d2, l2r=False)
            ry[i] = Y[i].shape[0]

            Q = teneva._reshape(zz, (rz[i], n[i], rz[i+1])) # if kickrank > 0 !
            Rx[i, :], Ry[i], Rz[i], Rxz[i, :], Ryz[i] = _inter_update(
                X[i, :], Y[i], Q,
                Rx[i+1, :], Ry[i+1], Rz[i+1], Rxz[i+1, :], Ryz[i+1],
                l2r=False)

        if dirn > 0 and i == d - 1:
            Y[i] = teneva._reshape(u @ v.T, (ry[i] * n[i] * ry[i + 1], d2))
            Y[i] = teneva._reshape(Y[i].T, (d2, ry[i], n[i], ry[i + 1]))

        if dirn < 0 and i == 0:
            Y[i] = teneva._reshape(u @ v.T, (d2, ry[i], n[i], ry[i + 1]))

        i += dirn
        block_order[order_index] = block_order[order_index] - dirn

        if block_order[order_index] == 0:
            order_index += 1

            if log:
                erank = np.sqrt(np.dot(ry[:d], n * ry[1:]) / np.sum(n))
                text = '== '
                text += f'# {swp:-4d} | '
                text += f'delta: {dy_max:-8.1e} | '
                text += f'rank: {erank:-5.1f}'
                print(text)

            if dy_max < eps_exit and dirn > 0:
                break

            if order_index >= len(block_order):
                block_order = [+d, -d]
                order_index = 0
                dy_max = 0
                swp += 1

            dirn = int(math.copysign(1, block_order[order_index]))
            i = i + dirn

    Y[d-1] = np.transpose(Y[d-1][:, :, :, 0], [1, 2, 0])

    return Y
