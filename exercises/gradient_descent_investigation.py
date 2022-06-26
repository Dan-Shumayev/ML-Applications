from typing import Callable, List, Tuple, Type

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from IMLearn import BaseModule
from IMLearn.desent_methods import ExponentialLR, FixedLR, GradientDescent
from IMLearn.desent_methods.modules import L1, L2
from IMLearn.learners.classifiers.logistic_regression import LogisticRegression
from IMLearn.utils import split_train_test


def plot_descent_path(module: Type[BaseModule],
                      descent_path: np.ndarray,
                      title: str = "",
                      xrange=(-1.5, 1.5),
                      yrange=(-1.5, 1.5)) -> go.Figure:
    """
    Plot the descent path of the gradient descent algorithm

    Parameters:
    -----------
    module: Type[BaseModule]
        Module type for which descent path is plotted

    descent_path: np.ndarray of shape (n_iterations, 2)
        Set of locations if 2D parameter space being the regularization path

    title: str, default=""
        Setting details to add to plot title

    xrange: Tuple[float, float], default=(-1.5, 1.5)
        Plot's x-axis range

    yrange: Tuple[float, float], default=(-1.5, 1.5)
        Plot's x-axis range

    Return:
    -------
    fig: go.Figure
        Plotly figure showing module's value in a grid of [xrange]x[yrange] 
        over which regularization path is shown

    Example:
    --------
    fig = plot_descent_path(IMLearn.desent_methods.modules.L1, np.ndarray([[1,1],[0,0]]))
    fig.show()
    """
    def predict_(w):
        return np.array([module(weights=wi).compute_output() for wi in w])

    from utils import decision_surface
    return go.Figure([decision_surface(predict_, xrange=xrange, yrange=yrange, \
                    density=70, showscale=False), \
                      go.Scatter(x=descent_path[:, 0], y=descent_path[:, 1], \
                        mode="markers+lines", marker_color="black")], \
                     layout=go.Layout(xaxis=dict(range=xrange), yaxis=dict(range=yrange),
                                      title=f"GD Descent Path {title}"))


def get_gd_state_recorder_callback() -> Tuple[Callable[[], None], List[np.ndarray], \
                        List[np.ndarray]]:
    """
    Callback generator for the GradientDescent class, 
    recording the objective's value and parameters at each iteration

    Return:
    -------
    callback: Callable[[], None]
        Callback function to be passed to the GradientDescent class, 
        recording the objective's value and parameters at each iteration of the algorithm

    values: List[np.ndarray]
        Recorded objective values

    weights: List[np.ndarray]
        Recorded parameters
    """
    weights, losses = [], []

    def callback(solver=None, weights=None, val=None, grad=None, t=None, eta=None, delta=None):
        weights.append(weights)
        losses.append(val)

    return callback, weights, losses

def compare_fixed_learning_rates(init: np.ndarray = np.array([np.sqrt(2), np.e / 3]),
                                 etas: Tuple[float] = (1, .1, .01, .001)):
    out_type = "best"

    for eta in etas:
        curr_eta = FixedLR(eta)
        l1_callback, l1_weights, l1_losses = get_gd_state_recorder_callback()
        l2_callback, l2_weights, l2_losses = get_gd_state_recorder_callback()

        # Initialize L1-2 norms
        l1_model = L1(init)
        l2_model = L2(init)

        # Set gradient descent algorithms for both norms with `curr_eta` learning-rate
        l1_solver, l2_solver = GradientDescent(learning_rate=curr_eta, out_type=out_type, \
            callback=l1_callback), GradientDescent(learning_rate=curr_eta, \
                                                out_type=out_type, callback=l2_callback)
        # Fit these norms by gradient descent iterations (done by `fit`)
        lowest_loss_l1, lowest_loss_l2 = l1_solver.fit(f=l1_model, X=np.nan, y=np.nan), \
            l2_solver.fit(f=l2_model, X=np.nan, y=np.nan)
        
        print(f"The Lowest Loss Obtained for the L1-norm for eta={eta} is {lowest_loss_l1}.\n")
        print(f"The Lowest Loss Obtained for the L2-norm for eta={eta} is {lowest_loss_l2}.\n")

        plt.plot(l1_losses, label=f"L1-Norm recording with eta={eta}")
        plt.plot(l2_losses, label=f"L2-Squared Norm recording with eta={eta}")
        
        if eta == .01:
            plot_descent_path(module=L1,
                              descent_path=np.array(l1_weights),
                              title="L1-norm Gradient Descent Path").show()
            plot_descent_path(module=L2,
                              descent_path=np.array(l2_weights),
                              title="L2-norm Gradient Descent Path").show()

    plt.legend()
    plt.show()


def compare_exponential_decay_rates(init: np.ndarray = np.array([np.sqrt(2), np.e / 3]),
                                    eta: float = .1,
                                    gammas: Tuple[float] = (.9, .95, .99, 1)):
    # Optimize the L1 objective using different decay-rate values of 
    # the exponentially decaying learning rate
    raise NotImplementedError()

    # Plot algorithm's convergence for the different values of gamma
    raise NotImplementedError()

    # Plot descent path for gamma=0.95
    raise NotImplementedError()


def load_data(path: str = "../datasets/SAheart.data", train_portion: float = .8) -> \
        Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Load South-Africa Heart Disease dataset and randomly split into a train- and test portion

    Parameters:
    -----------
    path: str, default= "../datasets/SAheart.data"
        Path to dataset

    train_portion: float, default=0.8
        Portion of dataset to use as a training set

    Return:
    -------
    train_X : DataFrame of shape (ceil(train_proportion * n_samples), n_features)
        Design matrix of train set

    train_y : Series of shape (ceil(train_proportion * n_samples), )
        Responses of training samples

    test_X : DataFrame of shape (floor((1-train_proportion) * n_samples), n_features)
        Design matrix of test set

    test_y : Series of shape (floor((1-train_proportion) * n_samples), )
        Responses of test samples
    """
    df = pd.read_csv(path)
    df.famhist = (df.famhist == 'Present').astype(int)
    return split_train_test(df.drop(['chd', 'row.names'], axis=1), df.chd, train_portion)


def fit_logistic_regression():
    # Load and split SA Heard Disease dataset
    X_train, y_train, X_test, y_test = load_data()

    # Plotting convergence rate of logistic regression over SA heart disease data
    raise NotImplementedError()

    # Fitting l1- and l2-regularized logistic regression models, 
    # using cross-validation to specify values of regularization parameter
    raise NotImplementedError()


if __name__ == '__main__':
    np.random.seed(0)
    compare_fixed_learning_rates()
    compare_exponential_decay_rates()
    fit_logistic_regression()
