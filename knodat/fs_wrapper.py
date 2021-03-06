#!/usr/bin/env python27
# -*- coding: utf-8 -*-

import os
import re
import logging
import collections

module_logger = logging.getLogger("FS Wrapper")
formatting = logging.Formatter(
    fmt="%(relativeCreated)d -- %(name)s -- %(levelname)s -- %(message)s")

ch = logging.StreamHandler()
ch.setFormatter(formatting)
ch.setLevel(logging.WARNING)

module_logger.addHandler(ch)


def ls(what="", directory="."):
    """
    Return content of a directory.

    :param str what: regular expression restricting directory listing
    :param str directory: path that shall be searched

    Rough equivalent of ``ls`` command available on the linux command line
    """
    if not directory.endswith("/"):
        directory = directory + "/"
    module_logger.info("ls() -- directory: %s" % directory)

    tmp = os.listdir(directory)
    todelete = list()

    for i in range(len(tmp)):
        if not re.match(what, tmp[i]):
            todelete.append(i)

    todelete.reverse()
    for i in todelete:
        tmp.__delitem__(i)

    for i in range(len(tmp)):
        tmp[i] = directory + tmp[i]

    return tmp


def extractParametersFromFilename(filename):
    module_logger.warning(
        "using deprecated function extractParametersFromFilename!")
    return extract_parameters_from_filename(filename)


def extract_parameters_from_filename(filename, tail=2, orientation=True,
                                     return_tail=False):
    """
    Takes a given filename and returns an array with extracted parameters
    filename is the name given to numerical output according to some fixed
    scheme. Parts of the filename are separated by unsderscores "_", decimal
    points are replaced by "p", so Latex and gnuplot can also work with the
    files. The first element is some explanatory abbreviation, the physical
    parameters come next alternating name and value. The return value is a
    dict with the parameter names as keys and their values as items. The last
    item is also neglected, it usually should state only the type of the file.

    Example:
    Consider a file called:
    AC_W_190_L_3700_E_0p11_lambdaBR_0p01_DeltaSO_0p001_transmissionsx.out

    AC is just the explanation that a ribbon with armchair orientation is the
    calculation basis, transmissionsx tells us that the spintransmission with
    respect to the x-axis as spin-quantization axis is calculated. The real
    physical parameters are in between, so the return value is the dictionary:
    {'W' : 190, 'L' : 3700, 'E' : 0.11, 'lambdaBR' : 0.01, 'DeltaSO' : 0.001}
    """
    tmp = filename.split("/")[-1]

    information = tmp.split("_")
    results = collections.OrderedDict()
    if orientation is True:
        results["orientation"] = information[0][:]
    for i in range((len(information) - tail) / 2):
        key = information[2 * i + 1]
        value = float(information[2 * i + 2].replace("p", "."))
        results[key] = value

    if return_tail is True:
        results["__tail__"] = information[-1]

    return results


def filename_from_parameters(parameters, prefix="ZZ", suffix="bla.out"):
    """
    Return a string created from dict ``parameters``, ``prefix`` and ``suffix``.

    This method is basically the inverse of
    :func:`extract_parameters_from_filename`. Given the example there we can
    pass the returned dictionary as ``parameters``, "AC" as ``prefix`` and
    "transmissionsx.out" as ``suffix`` we would recover the original filename.
    Note that decimal points get replaced by "p". The intention of this
    behaviour was to avoid problems when using the created files in gnuplot
    or latex.
    """
    final_array = [prefix]
    final_array.extend(
        [("%s_%g" % (key, val)).replace(".", "p")
         for key, val in parameters.items()])
    final_array.append(suffix)

    result = "_".join(final_array)

    return result
