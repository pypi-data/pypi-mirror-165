# Different metric functions to evaluate the HMM
import numpy as np


def calculate_aic(scores):
    """Plot aic of the HMM analysis

    returns:
        None
    """
    raise NotImplementedError


def calculate_bic(scores):
    """Plot aic of the HMM analysis

    returns:
        None
    """
    raise NotImplementedError


def calculate_mean_probas(time_ser, model):
    """Calculate the metric to evaluate based on average probabilities

    Args:
        time_ser (np.ndarray): dynophore time series
        model (HMM): Fitted HMM

    Returns:
        np.float: Probability of prediting the given time series based on the fitted model
                  Model
    """

    probas = model.predict_proba(time_ser)
    states = model.predict(time_ser)
    prob_ser = np.zeros(probas.shape)
    for i in range(len(states)):
        prob_ser[i, states[i]] = probas[i, states[i]]
    return np.mean(np.mean(prob_ser, axis=0))


def calculate_min_probas(time_ser, model):
    """Calculate the metric to evaluate based on min probabilities

    Args:
        time_ser (np.ndarray): dynophore time series
        model (HMM): Fitted HMM

    Returns:
        np.float: Probability of prediting the given time series based on the fitted model
                  Model
    """

    probas = model.predict_proba(time_ser)
    states = model.predict(time_ser)
    prob_ser = np.zeros(probas.shape)
    for i in range(len(states)):
        prob_ser[i, states[i]] = probas[i, states[i]]
    return np.amin(np.amin(prob_ser, axis=0))


def calculate_max_probas(time_ser, model):
    """Calculate the metric to evaluate based on max probabilities

    Args:
        time_ser (np.ndarray): dynophore time series
        model (HMM): Fitted HMM

    Returns:
        np.float: Probability of prediting the given time series based on the fitted model
                  Model
    """

    probas = model.predict_proba(time_ser)
    states = model.predict(time_ser)
    prob_ser = np.zeros(probas.shape)
    for i in range(len(states)):
        prob_ser[i, states[i]] = probas[i, states[i]]
    return np.amax(np.max(prob_ser, axis=0))
