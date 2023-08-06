import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_state_diagram(probabilities, max_states=15, file_name=None, save_path=None):
    """Plots the state diagram

    Args:
        probabilities ([type]): array of time series
        max_states    (int): maximum number of hidden states
        filename      (str): filename of the parent dynophore trajectory
    """
    plt.clf()
    plt.cla()
    plt.xlabel("Number of hidden states $M$")
    plt.ylabel("Probability of observation $P\mathbf{o}$")
    plt.title(file_name)
    plt.plot(np.arange(1, max_states + 1, 1), probabilities)
    plt.savefig(save_path + "/" + file_name + "obs_prob.png", dpi=300)
    print("Successfully saved" + file_name + "_obs_prob.png")


def plot_transmat_map(trans_mat, file_name=None, save_path=None):
    """State transition matrix visualised as a heatmap

    Args:
        trans_mat ([type]): [description]
        file_name ([type], optional): [description]. Defaults to None.
        save_path ([type], optional): [description]. Defaults to None.
    """
    ax = sns.heatmap(trans_mat)
    ax.set(xlabel="State", ylabel="State", cmap="crest")
    plt.title(file_name)
    fig = ax.get_figure()
    fig.savefig(save_path + "/" + file_name + "trans_mat.png", dpi=300)
    print("Successfully saved" + file_name + "trans_mat.png")


def plot_transmat_graph(trans_mat, file_name=None, save_path=None):
    """transition state matrix visualized as a directed graph

    Args:
        trans_mat ([type]): [description]
        file_name ([type], optional): [description]. Defaults to None.
        save_path ([type], optional): [description]. Defaults to None.
    """
    raise NotImplementedError


def plot_score(scores, file_name=None, save_path=None):
    """Plots the score for the HMM analysis, as well as AIC and BIC scores

    Args:
        scores ([type]): [description]
        file_name ([type], optional): [description]. Defaults to None.
        save_path ([type], optional): [description]. Defaults to None.
    """

    return None
