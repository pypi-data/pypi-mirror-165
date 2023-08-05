import math
import numpy as np
import teneva


def _inter_build(d, D):
    Rx = np.zeros((d + 1, D), dtype=np.object)
    Rx[0, :] = np.ones(D, dtype=float)
    Rx[d, :] = np.ones(D, dtype=float)

    Ry = np.zeros((d + 1,), dtype=np.object)
    Ry[0] = np.ones((1, 1), dtype=float)
    Ry[d] = np.ones((1, 1), dtype=float)

    Ryz = np.zeros((d + 1,), dtype=np.object)
    Ryz[0] = np.ones((1, 1), dtype=float)
    Ryz[d] = np.ones((1, 1), dtype=float)

    Rz = np.zeros((d + 1,), dtype=np.object)
    Rz[0] = np.ones((1, 1), dtype=float)
    Rz[d] = np.ones((1, 1), dtype=float)

    Rxz = np.zeros((d + 1, D), dtype=np.object)
    Rxz[0, :] = np.ones(D, dtype=float)
    Rxz[d, :] = np.ones(D, dtype=float)

    return Rx, Ry, Rz, Rxz, Ryz


def _inter_update(Gx, Gy, Gz, Rx, Ry, Rz, Rxz, Ryz, z_rand=False, l2r=True):
    Ry, ind = _dot_maxvol(Gy, Ry, None, l2r)
    Rx = [_dot_maxvol(G, R, ind, l2r)[0] for (G, R) in zip(Gx, Rx)]
    if Gz is not None:
        r1, n, r2 = Gz.shape
        ind = np.random.permutation(n * r1)[:r2] if z_rand else None
        Rz, ind = _dot_maxvol(Gz, Rz, ind, l2r)
        Ryz, _ = _dot_maxvol(Gy, Ryz, ind, l2r)
        Rxz = [_dot_maxvol(G, R, ind, l2r)[0] for (G, R) in zip(Gx, Rxz)]
    return Rx, Ry, Rz, Rxz, Ryz


def xxx(G, R, l2r=True):
    r1, n, r2, d2 = G.shape

    if l2r:
        G = teneva._reshape(G, (r1 * n * r2, d2))
        G = teneva._reshape(G.T, (d2 * r1 * n, r2))
        G = G @ R
        G = teneva._reshape(G, (d2, r1 * n * G.shape[-1]))
        G = G.T
    else:
        G = teneva._reshape(G, (r1, n * r2 * d2))
        G = R @ G
        G = teneva._reshape(G, (G.shape[0] * n * r2, d2))

    return G


def my_chop2(sv, eps):
    if eps <= 0.0:
        r = len(sv)
        return r
    sv0 = np.cumsum(abs(sv[::-1]) ** 2)[::-1]
    ff = [i for i in range(len(sv0)) if sv0[i] < eps ** 2]
    if len(ff) == 0:
        return len(sv)
    else:
        return np.amin(ff)


def _core_update(G, u, r_new, d2, l2r=True):
    r1, n, r2 = G.shape
    if l2r:
        G = teneva._reshape(G, (r1, n * r2))
        u = teneva._reshape(u, (r_new * r1, d2))
        u = teneva._reshape(u.T, (d2 * r_new, r1))
        Q = u @ G
        Q = teneva._reshape(Q, (d2, r_new, n, r2))
    else:
        G = teneva._reshape(G, (r1 * n, r2))
        u = teneva._reshape(u, (d2, r2 * r_new))
        u = teneva._reshape(u.T, (r2, r_new * d2))
        Q = G @ u
        Q = teneva._reshape(Q, (r1 * n * r_new, d2))
        Q = teneva._reshape(Q.T, (d2, r1, n, r_new))
    return Q


def _dot_maxvol(G, R, ind=None, l2r=True):
    r1, n, r2 = G.shape

    Q = teneva._reshape(G, (r1, n*r2) if l2r else (r1*n, r2))
    R = R * Q if isinstance(R, (int, float)) else (R @ Q if l2r else Q @ R)
    R = teneva._reshape(R, (R.shape[0]*n, r2) if l2r else (r1, n*R.shape[1]))

    if ind is None:
        ind = teneva._maxvol(R if l2r else R.T)[0]

    R = R[ind, :] if l2r else R[:, ind]

    return R, ind


def _svd_solve(G, R, kickrank=None):
    r1, n, r2, d2 = G.shape

    G = teneva._reshape(G, (r1 * n * r2, d2))
    G = teneva._reshape(G.T, (d2 * r1 * n, r2))
    G = np.linalg.solve(R.T, G.T).T
    G = teneva._reshape(G, (d2, r1 * n * r2)).T

    if kickrank is not None:
        G = teneva._reshape(G, (r1 * n, r2 * d2))
        G, sz, vz = np.linalg.svd(G, full_matrices=False)
        G = G[:, :min(kickrank, G.shape[1])]

    return G


def _svd(Y_new, dirn, kickrank, eps, d, rmax, l2r=True):
    if kickrank is None or kickrank < 0:
        if dirn > 0:
            u, v = np.linalg.qr(Y_new)
            v = np.conj(np.transpose(v))
            r = u.shape[1]
            s = np.ones((r, ))
        else:
            v, u = np.linalg.qr(np.transpose(Y_new))
            v = np.conj(v)
            u = np.transpose(u)
            r = u.shape[1]
            s = np.ones((r, ))

    else:
        try:
            u, s, v = np.linalg.svd(Y_new, full_matrices=False)
        except:
            m = Y_new
            tmp = np.array(np.random.randn(m, m), dtype=float)
            tmp, ru_tmp = np.linalg.qr(tmp)
            u, s, v = np.linalg.svd(np.dot(Y_new, tmp))
            v = np.dot(v, np.conj(tmp).T)

        v = np.conj(np.transpose(v))
        r = my_chop2(s, eps / math.sqrt(d) * np.linalg.norm(s))
        r = min(r, rmax, len(s))

    u = u[:, :r]
    v = v[:, :r]
    s = np.diag(s[:r])

    if l2r:
        v = v @ s
    else:
        u = u @ s

    return u, v


def _svd_solve_tr(G, R, d2, kickrank=None, R2=None):
    r1, n, r2, d = G.shape

    G = teneva._reshape(G, (r1, n * r2 * d2))
    G = np.linalg.solve(R, G) # multiply with inverted R
    G = teneva._reshape(G, (r1 * n * r2, d2))

    if R2 is not None:
        G = teneva._reshape(G.T, (d2 * r1 * n, r2))
        G = np.linalg.solve(R2.T, G.T).T

    if kickrank is not None:
        G = teneva._reshape(G.T, (d2 * r1, n * r2))
        G = np.linalg.svd(G, full_matrices=False)[-1]
        G = G[:min(kickrank, G.shape[0]), :].T


    # G = teneva._reshape(G, (r1, n, r2, d2))

    return G


def _func_y(funs, crx, Rx, Rxz, i, n, nx, rx, ry, rz, is2=False, is3=False):
    if is2:
        curbl = np.zeros((rz[i] * n[i] * ry[i + 1], nx), dtype=float)
    elif is3:
        curbl = np.zeros((ry[i] * n[i] * ry[i + 1], nx), dtype=float)
    else:
        curbl = np.zeros((ry[i] * n[i] * rz[i + 1], nx), dtype=float)

    for j in range(nx):
        # For kick
        cr = teneva._reshape(crx[i, j], (rx[i, j], n[i] * rx[i + 1, j]))
        cr = np.dot(Rxz[i, j] if is2 else Rx[i, j], cr)
        cr = teneva._reshape(cr, ((rz[i] if is2 else ry[i]) * n[i], rx[i + 1, j]))
        cr = np.dot(cr, Rx[i + 1, j] if (is2 or is3) else Rxz[i + 1, j])
        curbl[:, j] = cr.flatten('F')

    res = funs(curbl)

    return res


def _func_z(funs, crx, Rxz, i, n, nx, rx, rz):
    curbl = np.zeros((rz[i] * n[i] * rz[i + 1], nx), dtype=float)

    for j in range(nx):
        cr = teneva._reshape(crx[i, j], (rx[i, j], n[i] * rx[i + 1, j]))
        cr = np.dot(Rxz[i, j], cr)
        cr = teneva._reshape(cr, (rz[i] * n[i], rx[i + 1, j]))
        cr = np.dot(cr, Rxz[i + 1, j])
        curbl[:, j] = cr.flatten('F')

    res = funs(curbl)

    return res
