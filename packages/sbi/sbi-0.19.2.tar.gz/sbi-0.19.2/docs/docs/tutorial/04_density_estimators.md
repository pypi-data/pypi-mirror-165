# Customizing the density estimator

`sbi` allows to specify a custom density estimator for each of the implemented methods. For all options, check the API reference [here](https://www.mackelab.org/sbi/reference/#models).

## Changing the type of density estimator

One option is to use one of set of preconfigured density estimators by passing a string in the `density_estimator` keyword argument to the inference object (`SNPE` or `SNLE`), e.g., "maf" to use a Masked Autoregressive Flow, of "nsf" to use a Neural Spline Flow with default hyperparameters.


```python
inference = SNPE(prior=prior, density_estimator='maf')
```

In the case of `SNRE`, the argument is called `classifier`:


```python
inference = SNRE(prior=prior, classifier='resnet')
```

## Changing hyperparameters of density estimators

Alternatively, you can use a set of utils functions to configure a density estimator yourself, e.g., use a MAF with hyperparameters chosen for your problem at hand.

Here, because we want to use SN*P*E, we specifiy a neural network targeting the *posterior* (using the utils function `posterior_nn`). In this example, we will create a neural spline flow (`'nsf'`) with `60` hidden units and `3` transform layers:


```python
from sbi.utils.get_nn_models import posterior_nn  # For SNLE: likelihood_nn(). For SNRE: classifier_nn()

density_estimator_build_fun = posterior_nn(model='nsf', hidden_features=60, num_transforms=3)
inference = SNPE(prior=prior, density_estimator=density_estimator_build_fun)
```

It is also possible to pass an `embedding_net` to `posterior_nn()` which learn summary statistics from high-dimensional simulation outputs. You can find a more detailed tutorial on this [here](https://www.mackelab.org/sbi/tutorial/05_embedding_net/).

## Building new density estimators from scratch

Finally, it is also possible to implement your own density estimator from scratch, e.g., including embedding nets to preprocess data, or to a density estimator architecture of your choice. 

For this, the `density_estimator` argument needs to be a function that takes `theta` and `x` batches as arguments to then construct the density estimator after the first set of simulations was generated. Our utils functions in `sbi/utils/get_nn_models.py` return such a function. 
