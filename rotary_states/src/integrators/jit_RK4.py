from numba import njit

@njit
def __jit_stepRK4(RS, X, t_i, h, args):
    k1 = RS(X, t_i, *args)
    k2 = RS(X + h * k1 / 2, t_i + h / 2, *args)
    k3 = RS(X + h * k2 / 2, t_i + h / 2, *args)
    k4 = RS(X + h * k3, t_i + h, *args)
    return h * (k1 + 2 * k2 + 2 * k3 + k4) / 6

@njit
def jit_last_state(RS, q0, t0, t_end, args, h):
    '''
    Return last state at the t_end time moment.
    Take Right hand side, initial state, step by time,
    last time moment and args of system.
    '''
    X, t = q0.copy(), t0
    while t + h < t_end:
        X += __jit_stepRK4(RS, X, t, h, args)
        t += h

    X += __jit_stepRK4(RS, X, t, t_end - t, args)
    return X
