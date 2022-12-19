#
# This is a helper file for extracting the raw data from the .emsa files.
#

from pathlib import Path
import numpy as np


def read_emsa_file(filepath):
    """
    Takes inn a filename and gives counts from .emsa pluss its filename.

    Parameters
    ----------
    filepath : string
        path to the file

    Returns
    -------
    array, string
        counts in the array, and the name of the file
    """
    start_string = "#SPECTRUM    : Spectral Data Starts Here"
    stop_string = "#ENDOFDATA   : "
    filepath = Path(filepath)
    # If the line  below fail, it is because the data-folder is moved or renamed.
    with open(filepath, "r") as f:
        name = filepath.stem
        lines = f.readlines()
        # remove the line endings, which are '\n' for emsa
        lines = [line.rstrip("\n") for line in lines]
    start_index = lines.index(start_string)
    stop_index = lines.index(stop_string)
    lines = lines[start_index + 1 : stop_index]
    lines = [line.split(", ") for line in lines]
    counts = np.array(lines).T[1]  # select only counts, drop keV
    counts = np.array([float(c) for c in counts])
    return counts, name


def get_counts_and_name(filter, normalize=True, path="data/2022-09-06_EDS-SEM-APREO/"):
    """
    Gets counts and name of an emsa-file from a string-filter.
    Will only return the first filtered match.
    Can normalize on the max value in the counts.
    Correct filter is "GaAs_30kV" etc.
    E.g. filter on "GaAs" will give GaAs_05kV data.

    Parameters
    ----------
    filter : string
        filter on the emsa filename
    normalize : bool, optional
        If the data are to be normalized to the highest peak, by default True
    path : str, optional
        Path to the emsa-files, by default 'data/2022-09-06_EDS-SEM-APREO/'

    Returns
    -------
    array, string
        array of (normalized) counts, and the filename stem
    """
    all_emsa = Path(path).glob("*.emsa")
    for emsa in all_emsa:
        if filter in emsa.stem:
            counts, name = read_emsa_file(emsa)
    if normalize:
        counts = counts / counts.max()
    return counts, name


def get_multiple_counts_and_names(
    filter, normalize=True, path="data/2022-09-06_EDS-SEM-APREO/"
):
    """
    Gets counts and name of multiple emsa-file from a string-filter.
    Can normalize on the max value in the counts.

    Parameters
    ----------
    filter : string
        filter on the emsa filename
    normalize : bool, optional
        If the data are to be normalized to the highest peak, by default True
    path : str, optional
        Path to the emsa-files, by default 'data/2022-09-06_EDS-SEM-APREO/'

    Returns
    -------
    list of array, list of string
        list of array of (normalized) counts, and the list of filename stem
    """
    all_emsa = Path(path).glob("*.emsa")
    counts = []
    names = []
    for emsa in all_emsa:
        if filter in emsa.stem:
            c, n = read_emsa_file(emsa)
            if normalize:
                c = c / c.max()
            counts.append(c)
            names.append(n)
    return counts, names
