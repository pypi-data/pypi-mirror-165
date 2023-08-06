import xml.etree.ElementTree as ET
import numpy as np
import json

from dylightful.utilities import save_dict, parse_file_path


def get_time_series(pml_path):
    """gets the time_series of the dynophore from the pml file

    Args:
        pml_path (str): path to the pml file containing the Dynophore trajectory

    Returns:
        [dictionary, JSON]: returns the time series for each superfeature as a JSON file
    """

    save_path = parse_file_path(pml_path)

    tree = ET.parse(pml_path)
    root = tree.getroot()
    time_series = {}
    cartesian_traj = {}
    centroids = {}
    for child in root:
        i = 0
        frames = []
        coordinates = []

        for attributes in child:
            if i == 0:
                x = float(attributes.get("x3"))
                y = float(attributes.get("y3"))
                z = float(attributes.get("z3"))
                centre = [x, y, z]
            else:  # first entry does not provide frameIndex information
                frame_idx = int(attributes.get("frameIndex"))
                x = float(attributes.get("x3"))
                y = float(attributes.get("y3"))
                z = float(attributes.get("z3"))
                coordinates.append([x, y, z])

                frames.append(frame_idx)
                if i == 1:  # get the value of the last frameIndex
                    max_index = frame_idx + 1  # counting in python starts at 0
                elif max_index < frame_idx + 1:
                    max_index = frame_idx + 1
            i += 1
        time_series[child.get("id")] = frames
        cartesian_traj[child.get("id")] = coordinates
        centroids[child.get("id")] = centre
    cartesian_full_traj = {}
    cartesian_full_traj["centroids"] = centroids
    cartesian_full_traj["cartesian"] = cartesian_traj
    save_dict(cartesian_full_traj, save_path=save_path, name="cartesian")
    time_series["num_frames"] = max_index
    time_series = rewrites_time_series(time_series)

    save_dict(time_series, save_path=save_path)
    return time_series


def rewrites_time_series(feature_series):
    """Convertes to a sparse time series to be ready for the HMM processing

    Args:
        feature_series (np.array):

    Returns:
        dictionionary, JSON: JSON with the time series per superfeature
    """

    max_frames = feature_series["num_frames"]
    keys = list(feature_series.keys())
    for i in range(len(keys) - 1):
        time_ser_feat = feature_series[keys[i]]
        new_time_ser = np.zeros(int(max_frames))
        try:
            for frame_index in time_ser_feat:
                try:
                    if frame_index < len(new_time_ser):
                        new_time_ser[int(frame_index)] = 1
                        if max_frames < frame_index:
                            max_frames = int(
                                frame_index
                            )  # if something with the frame_index is wrong set it here
                            print("superfeature:", keys[i])
                            print("Set max frames to", frame_index)
                            if i > 0:
                                for j in range(i):
                                    print("resetting", keys[j])
                                    tmp = list(feature_series[keys[j]])
                                    tmp += [0]
                                    feature_series[keys[j]] = tmp
                    else:
                        tmp = np.zeros(int(frame_index + 50))  # free new memory
                        tmp[: len(new_time_ser)] = new_time_ser
                        tmp[int(frame_index)] = 1
                        new_time_ser = tmp
                except:
                    print(
                        "Error parsing into new time series in superfeature, ",
                        keys[i],
                        "in frame",
                        frame_index,
                        "but the memory was only",
                        len(new_time_ser),
                        "time points",
                    )
                    continue
        except:
            raise RuntimeError("Fatal error while parsing superfeature", keys[i])
        new_time_ser = new_time_ser[:max_frames]
        assert len(new_time_ser) == max_frames, (
            "Lengths of parsed time series does not match the maximum number of frames. Length was"
            + str(len(new_time_ser))
        )
        feature_series[keys[i]] = new_time_ser.astype(np.int32).tolist()
    for i in range(len(keys) - 1):
        print(len(feature_series[keys[i]]))
    return feature_series


def get_atom_serials(pml_path):

    save_path = parse_file_path(pml_path)

    tree = ET.parse(pml_path)
    root = tree.getroot()
    for child in root:
        print(child)


def load_env_partners_mixed(json_path):
    """Generates the env_partners with occurences from the corresponding json

    Args:
        json_path ([type]): [description]
    """

    with open(json_path) as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    num_features = len(jsonObject["superfeatures"])
    storage_env_partners = {}
    for i in range(num_features):
        env_partners = jsonObject["superfeatures"][i]["envpartners"]

        for env_partner in env_partners:
            name = env_partner["name"]
            storage_env_partners[name + ":superFeature" + str(i)] = env_partner[
                "occurrences"
            ]
    return storage_env_partners


def load_env_partners(json_path):
    """Generates the env_partners with occurences from the corresponding json

    Args:
        json_path ([type]): [description]
    """

    with open(json_path) as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    num_features = len(jsonObject["superfeatures"])
    storage_env_partners = {}
    for i in range(num_features):
        env_partners = jsonObject["superfeatures"][i]["envpartners"]

        for env_partner in env_partners:
            name = env_partner["name"]
            storage_env_partners[name] = []
        for env_partner in env_partners:
            name = env_partner["name"]
            storage_env_partners[name].append(env_partner["occurrences"])
    return storage_env_partners


if __name__ == "__main__":
    # get_time_series("../Trajectories/Dominique/1KE7_dynophore.json")
    # get_time_series("../tests/Trajectories/1KE7_dynophore.pml")
    # get_atom_serials(pml_path="../tests/Trajectories/1KE7_dynophore.pml")
    res = load_env_partners(
        json_path="../tests/Trajectories/ZIKV/ZIKV-Pro-427-1_dynophore.json"
    )
    print(res)
