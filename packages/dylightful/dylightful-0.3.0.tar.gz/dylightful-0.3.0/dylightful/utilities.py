import json
import os
from pathlib import Path
import pandas as pd

dirname = os.path.dirname(__file__)


def load_parsed_dyno(traj_path):
    """Loads the parsed trajectory from the parser

    Args:
        traj_path ([type]): Path to the parsed traj

    Returns:
        [type]: trajectory as pd.DataFrame, number of observations as int
    """
    with open(traj_path) as f:
        data = json.load(f)

    time_ser = pd.DataFrame(data)
    time_ser = time_ser.drop(columns="num_frames")
    obs = time_ser.drop_duplicates()
    num_obs = len(obs)
    print("There are actually ", num_obs, " present.")
    obs = obs.to_numpy()
    time_ser = time_ser.to_numpy()
    print("The length of the observation sequence is ", len(time_ser))
    return [time_ser, obs]


def save_dict(d, save_path, name=None):
    if name is None:
        name = "_time_series.json"
    else:
        name = "_" + name
        name += "_time_series.json"

    with open(save_path + name, "w") as fp:
        json.dump(d, fp)
    print("Saved file to", save_path)


def make_name(prefix, name, dir=dirname):
    """Merge a prefix and a name

    Args:
        prefix ([type]): [description]
        name ([type]): [description]

    Returns:
        [type]: [description]
    """
    if dir is None:
        dir = os.getcwd()
    if prefix is None:
        return os.path.join(dir, name)
    else:
        prefix = "_" + prefix
        name = prefix + name
    return os.path.join(dir, name)


def parse_file_path(path):
    """Automatically generates an output path for the time trajectory

    Args:
        path ([type]): Dynophore input path
    """
    return get_dir(path) + "/" + get_name(path)


def get_dir(path):
    """Automatically extracts the path to the dynophore trajectory

    Args:
        path (str): File path to the dynophore trajectory

    Returns:
        str: /some/file/path
    """
    dir_path = os.path.dirname(os.path.realpath(path))
    return dir_path


def get_name(path):
    """Gets the name of the dynophore trajectory without the .pml extension

    Args:
        path (str): File path to the dynophore trajectory

    Returns:
        str: dynophore_pml
    """
    file = Path(path).stem
    return file
