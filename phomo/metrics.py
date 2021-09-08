from typing import Protocol
import functools

import numpy as np


METRICS = {}


class MetricCallable(Protocol):
    def __call__(self, a: np.ndarray, b: np.ndarray) -> float:
        ...


def register_metric(func):
    METRICS[func.__name__] = func

    @functools.wraps(func)
    def metric(*args, **kwargs):
        return func(*args, **kwargs)

    return metric


@register_metric
def greyscale(img_a: np.ndarray, img_b: np.ndarray, *args, **kwargs) -> float:
    """Compute the greyscale distance.

    Args:
        img_a: array containing the RGB pixels with values between 0 and 255.
        img_b: array containing the RGB pixels with values between 0 and 255.
        *args, **kwargs: passed to `np.linalg.norm`.

    Returns:
        Colour distance approximation.
    """
    return np.linalg.norm(
        np.subtract(img_a.mean(axis=-1), img_b.mean(axis=-1), dtype=float),
        *args,
        **kwargs,
    )


@register_metric
def norm(img_a: np.ndarray, img_b: np.ndarray, *args, **kwargs) -> float:
    """`np.linalg.norm` distance metric.

    Args:
        img_a: array containing the RGB pixels with values between 0 and 255.
        img_b: array containing the RGB pixels with values between 0 and 255.
        *args, **kwargs: passed to `np.linalg.norm`.

    Returns:
        Colour distance approximation.
    """
    return np.linalg.norm(np.subtract(img_a, img_b, dtype=float), *args, **kwargs)


# def norm(img_a: np.ndarray, img_b: np.ndarray, *args, **kwargs) -> float:
#     """`np.linalg.norm` distance metric.

#     Args:
#         img_a: array containing the RGB pixels with values between 0
#             and 255.
#         img_b: array containing the RGB pixels with values between 0
#             and 255.

#     Returns:
#         Colour distance approximation.
#     """
#     return np.linalg.norm(
#         np.linalg.norm(
#             np.subtract(img_a, img_b, dtype=float),
#             axis=-1,
#             *args,
#             **kwargs,
#         )
#     )


@register_metric
def luv_approx(img_a: np.ndarray, img_b: np.ndarray, *args, **kwargs) -> float:
    """Distance metric, a L*U*V approximation.

    Reference:
        https://www.compuphase.com/cmetric.htm

    Args:
        img_a: array containing the RGB pixels with values between and 255.
        img_b: array containing the RGB pixels with values between and 255.
        *args, **kwargs: passed to `np.linalg.norm`.

    Returns:
        Colour distance approximation.
    """
    r = (img_a[:, :, 0] + img_b[:, :, 0]) // 2
    d = np.subtract(img_a, img_b, dtype=float)
    return np.linalg.norm(
        ((512 + r) * d[:, :, 0] ** 2)
        + 1024 * d[:, :, 1] ** 2
        + ((767 - r) * d[:, :, 2] ** 2),
        *args,
        **kwargs,
    )
