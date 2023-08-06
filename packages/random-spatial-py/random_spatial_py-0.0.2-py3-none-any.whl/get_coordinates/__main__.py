import os
import sys
import getopt

import geopandas as gpd
from .boundaries.get_world_countries import get_countries
from .utils.points import random_from_point
from .utils.show import show_points
from .utils.export import export_json, export_txt


def help_str():
    msg = "Function takes multiple parameters to prepare a set of random points. Available parameters are:\n" \
          "* -x: <longitude>\n" \
          "* -y <latitude>\n" \
          "* -n (optional) <number of points>\n" \
          "* -s (optional) <step size to define area with random points>\n" \
          "* --txt (optional) <path to export txt>\n" \
          "* --json (optional) <path to export JSON>\n" \
          "* -v or --view (optional) <show generated points - if country POSTAL given then show only within its " \
          "borders>\n" \
          "-h or --help (optional) <shows this message>"
    return msg


def run(x, y, n=None, step=None, txt=None, json=None, view=False, area_to_show=None):

    if n is None:
        n = 100

    if step is None:
        step = 0.1

    pts = random_from_point(x, y, no=n, step_size=step)

    if isinstance(txt, str):
        export_txt(txt, pts)

    if isinstance(json, str):
        export_json(json, pts)

    if view:
        GDF = get_countries()
        show_points(points=pts, boundaries=GDF, country_postal=area_to_show)

    print('Longitude, Latitude')
    for point in pts:
        print(point)


def myfunc(argv):
    arg_x = None
    arg_y = None
    arg_n = None
    arg_step = None
    arg_txt = None
    arg_json = None
    arg_view = False
    arg_postal = None

    arg_help = help_str()

    try:
        opts, args = getopt.getopt(argv[1:],
                                   'hx:y:n:s:f:vp:',
                                   ["help", "step-size=", "txt=", "json=",
                                    "view", "postal="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt == "-x":
            arg_x = float(arg)
        elif opt == "-y":
            arg_y = float(arg)
        elif opt == "-n":
            arg_n = int(arg)
        elif opt in ("-s", "--step-size"):
            arg_step = float(arg)
        elif opt == "--txt":
            arg_txt = arg
        elif opt == "--json":
            arg_json = arg
        elif opt in ("-v", "--view"):
            arg_view = True
        elif opt in ("-p", "--postal"):
            arg_postal = arg
            arg_view = True

    if arg_x is not None and arg_y is not None:
        run(x=arg_x, y=arg_y, n=arg_n, step=arg_step,
            txt=arg_txt, json=arg_json, view=arg_view, area_to_show=arg_postal)
    else:
        raise KeyError('You must provide -x <longitude> and -y <latitude> parameters')


if __name__ == '__main__':
    myfunc(sys.argv)
