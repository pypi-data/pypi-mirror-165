from typing import List
import numpy as np


def _get_edges(cx: float, cy: float, rad: float):
    xmin = cx - rad
    xmax = cx + rad
    ymin = cy - rad
    ymax = cy + rad
    return xmin, xmax, ymin, ymax


def _create_points_set(edges, no):
    """

    :param edges: (List) xmin, xmax, ymin, ymax
    :param no: (int)
    :return: (List)
    """
    x = np.random.uniform(edges[0], edges[1], no)
    y = np.random.uniform(edges[2], edges[3], no)
    pts = list(zip(x, y))
    return pts


def random_from_point(cx: float,
                      cy: float,
                      no=100,
                      step_size=0.1) -> List:
    """

    :param cx: (float) Longitude.
    :param cy: (float) Latitude.
    :param no: (int) The number of returned points.
    :param step_size: (float) step from the coordinates to create a bounding box with random points,
    :return: (List) Set of points of size no.
    """
    # Create set of points within bounding box
    edges = _get_edges(cx, cy, step_size)
    points_set = _create_points_set(edges, no)
    return points_set
