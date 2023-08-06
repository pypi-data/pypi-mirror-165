from termios import FF0
from tkinter import W
from xmlrpc.client import Boolean
from como.logistic_susie import loglik_susie
from como.utils import bernoulli_entropy
import jax.numpy as jnp
import jax.scipy as jsp
from functools import partial
import jax
import numpy as np

from .component_distributions import ComponentDistribution, NormalFixedLocComponent, NormalScaleMixtureComponent, PointMassComponent
from .logistic_regression import InterceptOnly, LogisticRegression, LogisticSusie

class TwoComponentCoMo:
    def __init__(self, data, f0: ComponentDistribution, f1: ComponentDistribution, logreg: LogisticRegression):
        """
        Initialize Two component covariate moderated EBNM
    
        Parameters:
            data: dictionary with keys 'beta' and 'se' for observations and standard errors
            f0: a ComponentDistribution object for the null distribtuion
            f1: a ComponentDistribution object for the active distribtuion
            logreg: a LogisticRegression model (e.g. LogisticSusie)
        """
        self.data = data
        self.f0 = f0
        self.f1 = f1
        self.logreg = logreg
        self.data['y'] = twococomo_compute_responsibilities(
            self.data, self.logreg, self.f0, self.f1
        )
        self.elbo_history = []

    @property
    def responsibilities(self):
        """
        posterior assignment probability to the non-null component (f1)
        """
        return np.array(self.data['y'])

    @property
    def prior_log_odds(self):
        """
        return the (expected) prior log odds for each observation
        this is the (expectation of) the prediction from the logistic regression model
        """
        return np.array(self.logreg.predict())

    @property
    def beta(self):
        return self.data['beta']
    
    @property
    def se(self):
        return self.data['se']
    
    @property
    def X(self):
        return self.data['X']

    @property
    def Z(self):
        return self.data['Z']

    @property
    def post_mean(self):
        """
        posterior mean of two component mixture
        """
        mu0 = self.f0.mu(self.data)
        mu1 = self.f1.mu(self.data)
        mu = mu0 * (1 - self.responsibilities) \
            + mu1 * self.responsibilities
        return mu

    @property
    def post_mean2(self):
        # compute mixture 2nd moment
        mu20 = self.f0.mu2(self.data)
        mu21 = self.f1.mu2(self.data)
        mu2 = mu20 * (1 - self.responsibilities) \
            + mu21 * self.responsibilities 
        return mu2

    @property
    def post_var(self):
        """
        posterior variance
        """ 
        # compute mixture mean
        post_mu2 = self.post_mean2
        post_mu = self.post_mean 
        post_var = post_mu2 - post_mu**2
        return post_var

    def loglik(self):
        return twococomo_loglik(
            self.data, self.responsibilities, self.f0, self.f1 
        )

    def elbo(self, record: Boolean = False):
        new_elbo = twococomo_elbo(
            self.data, self.responsibilities, self.f0, self.f1, self.logreg  
        )
        if record:
            self.elbo_history.append(new_elbo['total_elbo'])
        return new_elbo
    
    def update_responsibilities(self):
        """
        update the responsibilities and pass values to logreg
        """
        self.data['y'] = twococomo_compute_responsibilities(
            self.data, self.logreg, self.f0, self.f1)
        # self.logreg.data['y'] = self.responsibilities

    def update_logreg(self):
        """
        Update the logistic regression
        """
        self.logreg.update()

    def update_f0(self):
        """
        Update the null component
        """
        self.f0.update(self.data)

    def update_f1(self):
        """
        Update the alternate component
        """
        self.f1.update(self.data)

    def iter(self):
        """
        iteration updates responsibilities, logistic regression, f0, and f1
        """
        self.update_responsibilities()
        self.logreg.update()
        self.f0.update(self.data)
        self.f1.update(self.data)


    def fit(self, niter=100, tol=1e-3):
        for i in range(niter):
            self.iter()
            self.elbo_history.append(self.elbo()['total_elbo'])
            if self.converged(tol):
                break

    def converged(self, tol=1e-3):
        return ((len(self.elbo_history) > 2)
            and ((self.elbo_history[-1] - self.elbo_history[-2]) < tol))


class PointNormalSuSiE(TwoComponentCoMo):
    def __init__(self, data, scale=1.0):
        """
        Initialize Point Normal SuSiE
        (Covariatiate EBNM with "point-normal" effects,
        and SuSiE prior on the mixture proportion)

        Parameters:
            data: dictionary with keys
                'beta' and 'se' for observations and standard errors,
                'X' and 'Z' for annotations and (fixed) covariates resp.
            scale: (initial) scale parameter for the normal mixture component
        """
        f0 = PointMassComponent(0.0)
        f1 = NormalFixedLocComponent(0, scale)
        
        # TODO: make sure `y` is a key in data, otherwise make it
        data['y'] = np.random.uniform(data['beta'].size)
        logreg = LogisticSusie(data, L=10)
        super().__init__(data, f0, f1, logreg)

class PointNormalMixtureSuSiE(TwoComponentCoMo):
    def __init__(self, data, f0_args: dict = {}, f1_args: dict = {}):
        """
        Initialize Point Normal SuSiE
        (Covariatiate EBNM with "point-normal" effects,
        and SuSiE prior on the mixture proportion)

        Parameters:
            data: dictionary with keys
                'beta' and 'se' for observations and standard errors,
                'X' and 'Z' for annotations and (fixed) covariates resp.
            scale: (initial) scale parameter for the normal mixture component
        """
        f0 = PointMassComponent(**f0_args)
        f1 = NormalScaleMixtureComponent(**f1_args)
        
        # TODO: make sure `y` is a key in data, otherwise make it
        data['y'] = np.random.uniform(data['beta'].size)
        logreg = LogisticSusie(data, L=10)
        super().__init__(data, f0, f1, logreg)
    

class PointNormal(TwoComponentCoMo):
    def __init__(self, data, scale=1.0):
        """
        Intercept-only "point-normal" model no covariate moderation

        Parameters:
            data: dictionary with keys
                'beta' and 'se' for observations and standard errors,
                'X' and 'Z' for annotations and (fixed) covariates resp.
            scale: (initial) scale parameter for the normal mixture component
        """
        f0 = PointMassComponent(0.0)
        f1 = NormalFixedLocComponent(0, scale)
        
        # TODO: make sure `y` is a key in data, otherwise make it
        data['y'] = np.random.uniform(data['beta'].size)
        logreg = InterceptOnly(data)
        super().__init__(data, f0, f1, logreg)
    
class PointNormalMixture(TwoComponentCoMo):
    def __init__(self, data, f0_args: dict = {}, f1_args: dict = {}):
        """
        Mixture of a point mass and a scale normal mixture
        Equivalent to ASH when point mass and normal mixture all share same loc
    
        Parameters:
            data: dictionary with keys
                'beta' and 'se' for observations and standard errors,
                'X' and 'Z' for annotations and (fixed) covariates resp.
        """
        f0 = PointMassComponent(**f0_args)
        f1 = NormalScaleMixtureComponent(**f1_args)
        
        # TODO: make sure `y` is a key in data, otherwise make it
        data['y'] = np.ones(data['beta'].size) - 1e-10
        logreg = InterceptOnly(data)
        super().__init__(data, f0, f1, logreg)

# The two component covariate moderated EBNM
def twococomo_compute_responsibilities(data, logreg, f0, f1):
    """
    compute p(\gamma | data, f0, f1)
    """
    logit_pi = logreg.predict()
    #logit_pi = loglik_susie(logreg.data, logreg.params)
    f0_loglik = f0.convolved_logpdf(data['beta'], data['se'])
    f1_loglik = f1.convolved_logpdf(data['beta'], data['se'])

    logits = f1_loglik - f0_loglik + logit_pi
    responsibilities = jax.nn.sigmoid(logits) 
    return responsibilities

def twococomo_loglik(data, responsibilities, f0, f1, sum=True):
    """
    compute E[p(\beta | s, \gamma, f_0, f_1)]
    """
    f0_loglik = f0.convolved_logpdf(data['beta'], data['se'])
    f1_loglik = f1.convolved_logpdf(data['beta'], data['se'])
    loglik = (1 - responsibilities) * f0_loglik + responsibilities * f1_loglik
    if sum:
        loglik = jnp.sum(loglik)
    return loglik

def twococomo_elbo(data, responsibilities, f0, f1, logreg):
    data_loglik = twococomo_loglik(data, responsibilities, f0, f1, sum = False)
    assignment_entropy = bernoulli_entropy(responsibilities)
    logreg_elbo = logreg.evidence()
    total_elbo = jnp.sum(data_loglik + assignment_entropy) + logreg_elbo
    return dict(
        data_loglik=data_loglik,
        assignment_entropy=assignment_entropy,
        logistic_elbo=logreg_elbo,
        total_elbo=total_elbo)

def twococomo_iter(data, f0, f1, logreg):
    # update responsibilities, stored as ['y']
    res = twococomo_compute_responsibilities(data, logreg, f0, f1)
    logreg.data['y'] = res
    logreg.update()
    f0.update()
    f1.update()








