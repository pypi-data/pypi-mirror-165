# The sampler interface

Note: this tutorial requires that the user is already familiar with the [flexible interface](https://www.mackelab.org/sbi/tutorial/02_flexible_interface/).

`sbi` implements three methods: SNPE, SNLE, and SNRE. When using SNPE, the trained neural network directly approximates the posterior. Thus, sampling from the posterior can be done by sampling from the trained neural network. The neural networks trained in SNLE and SNRE approximate the likelihood(-ratio). Thus, in order to draw samples from the posterior, one has to perform additional sampling steps, e.g. Markov-chain Monte-Carlo (MCMC). In `sbi`, the implemented samplers are:
- Markov-chain Monte-Carlo (MCMC)
- Rejection sampling  
- Variational inference (VI)

When using the flexible interface, the sampler as well as its attributes can be set with `sample_with="mcmc"`, `mcmc_method="slice_np"`, and `mcmc_parameters={}`. However, for full flexibility in customizing the sampler, we recommend using the **sampler interface**. This interface is described here. Further details can be found [here](https://github.com/mackelab/sbi/pull/573).

## Main syntax for SNLE


```python
import torch

from sbi.inference import SNLE
from sbi.inference import likelihood_estimator_based_potential, MCMCPosterior

# dummy Gaussian simulator for demonstration
num_dim = 2
prior = torch.distributions.MultivariateNormal(torch.zeros(num_dim), torch.eye(num_dim))
theta = prior.sample((1000,))
x = theta + torch.randn((1000, num_dim))
x_o = torch.randn((1, num_dim))

inference = SNLE(show_progress_bars=False)
likelihood_estimator = inference.append_simulations(theta, x).train()

potential_fn, parameter_transform = likelihood_estimator_based_potential(likelihood_estimator, prior, x_o)
posterior = MCMCPosterior(potential_fn, proposal=prior, theta_transform=parameter_transform)
```

     Neural network successfully converged after 52 epochs.

## Further explanation

The first lines are the same as for the flexible interface:


```python
inference = SNLE()
likelihood_estimator = inference.append_simulations(theta, x).train()
```

     Neural network successfully converged after 33 epochs.

Next, we obtain the potential function. A potential function is a function of the parameter $f(\theta)$. The posterior is proportional to the product of likelihood and prior: $p(\theta | x_o) \propto p(x_o | \theta)p(\theta)$. The potential function is the logarithm of the right-hand side of this equation: $f(\theta) = \log(p(x_o | \theta)p(\theta))$


```python
potential_fn, parameter_transform = likelihood_estimator_based_potential(likelihood_estimator, prior, x_o)
```

By calling the `potential_fn`, you can evaluate the potential:


```python
# Assuming that your parameters are 1D.
potential = potential_fn(torch.zeros(1, num_dim))  # -> returns f(0) = log( p(x_o|0) p(0) )
```

The other object that is returned by `likelihood_estimator_based_potential` is a `parameter_transform`. The `parameter_transform` is a [pytorch transform](https://github.com/pytorch/pytorch/blob/master/torch/distributions/transforms.py). The `parameter_transform` is a fixed transform that is can be applied to parameter `theta`. It transforms the parameters into unconstrained space (if the prior is bounded, e.g. `BoxUniform`), and standardizes the parameters (i.e. zero mean, one std). Using `parameter_transform` during sampling is optional, but it usually improves the performance of MCMC.


```python
theta_tf = parameter_transform(torch.zeros(1, num_dim))
theta_original = parameter_transform.inv(theta_tf)
print(theta_original)  # -> tensor([[0.0]])
```

    tensor([[0., 0.]])


After having obtained the `potential_fn`, we can sample from the posterior with MCMC or rejection sampling:


```python
from sbi.inference import MCMCPosterior, RejectionPosterior

posterior = MCMCPosterior(potential_fn, proposal=prior, theta_transform=parameter_transform)
posterior = RejectionPosterior(potential_fn, proposal=prior)
```

## Main syntax for SNPE

SNPE usually does not require MCMC or rejection sampling (if you still need it, you can use the same syntax as above with the `posterior_estimator_based_potential` function). Instead, SNPE samples from the neural network. If the support of the prior is bounded, some samples can lie outside of the support of the prior. The `DirectPosterior` class automatically rejects these samples:


```python
from sbi.inference import SNPE
from sbi.inference import DirectPosterior

inference = SNPE()
posterior_estimator = inference.append_simulations(theta, x).train()

posterior = DirectPosterior(posterior_estimator, prior=prior)
```

     Neural network successfully converged after 57 epochs.


```python

```
