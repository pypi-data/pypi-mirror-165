from computegraph import jaxify


def _set_np(arr, idx, value):
    arr[idx] = value
    return arr


def _set_jax(arr, idx, value):
    return arr.at[idx].set(value)


def _add_np(arr, idx, value):
    arr[idx] += value
    return arr


def _add_jax(arr, idx, value):
    return arr.at[idx].add(value)


def _mul_np(arr, idx, value):
    arr[idx] *= value
    return arr


def _mul_jax(arr, idx, value):
    return arr.at[idx].mul(value)


if jaxify.get_using_jax():
    arr_set = _set_jax
    arr_add = _add_jax
    arr_mul = _mul_jax

else:
    arr_set = _set_np
    arr_add = _add_np
    arr_mul = _mul_np
