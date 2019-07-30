import numpy as np
import numpy.random
import scipy.stats as ss
import matplotlib.pyplot as plt
from scipy.special import logsumexp

from RandomGaussian import gen_gaussian_mixture

ax = np.newaxis


def exp_max_numpy(data_input, param_guess=None, num_iter=100):

    """
        Runs the Expectation-Maximization algorithm using NumPy.
        :param data_input: Data used in the EM algorithm
        :param param_guess: Initial guess for parameter values
        :param num_iter: Number of iterations (default 100)
        :return: Estimated parameters
    """

    if param_guess is None:
        init_mu = np.array([3.0, 3.0])
        init_sig = np.array([0.5, 0.6])
        init_weights = np.array([0.5, 0.5])
    else:
        init_mu = param_guess['mu']
        init_sig = param_guess['sig']
        init_weights = param_guess['weight']

    # Initialize the parameters to be estimated
    mu, sig, alpha = init_mu, init_sig, init_weights

    for ite in range(1, num_iter):

        dist_mix = np.vectorize(ss.norm)(mu, sig)

        # Step 1 - Compute the log-likelihood using the guess.
        em_log = np.transpose(np.log(alpha)[:, ax] +
                              np.array(list(map(lambda x: x.logpdf(data_input), dist_mix))))

        # Step 2 - Compute the posterior probabilities.
        em_prob = np.exp(em_log - logsumexp(em_log))

        # Step 3 - Update the guess of the mixture parameters.
        alpha = em_prob.sum(axis=0)
        mu = np.sum(em_prob * data_input[:, ax], axis=0)/alpha
        sig = np.sqrt(np.sum(em_prob * np.power(data_input[:, ax] - mu[ax, :], 2),
                             axis=0)/alpha)

    return alpha, mu, sig


input_mix = {'mu_sig': np.array([[2.0, 0.5], [5.0, 0.7]]),
             'weights': np.array([0.3, 0.7])}

data = gen_gaussian_mixture(input_mix, num_sample=10000, do_plot=True)
result = exp_max_numpy(data)
