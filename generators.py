import random as rnd
import math
import numpy as np
import matplotlib.pyplot as plt


def validate_input_number(n: int, min: int, max: int | None = None, message: str | None = None) -> int:
    while n < min or (max is not None and n > max):
        n = int(input(message if message else ''))
    return n


def uniform_distribution_generator(min: int, max: int) -> float:
    return min + (rnd.random() * (max - min))


def negative_exponential_distribution_generator(lamb: float) -> float:
    """Generates a random number from a negative exponential distribution.

    Args:
        lamb (float): The rate parameter (lambda) of the distribution.

    Returns:
        float | None: A random number from the negative exponential distribution or None if lamb is invalid.
    """
    return -1/lamb * math.log(1 - rnd.random())


def normal_distribution_generator(mu: float, sigma: float) -> float:
    """Generates a random number from a normal distribution using de convolution method.

    Args:
        mu (float): The mean of the distribution.
        sigma (float): The standard deviation of the distribution.

    Returns:
        float: A random number from the normal distribution.

    Returns:
        float: A random number from the normal distribution.
    """
    return (np.sum(np.array([rnd.random() for _ in range(12)])) - 6) * sigma + mu


def normal_distribution_generator_box_muller(mu: float, sigma: float) -> float:
    """Generates a random number from a normal distribution using de convolution method.

    Args:
        mu (float): The mean of the distribution.
        sigma (float): The standard deviation of the distribution.

    Returns:
        float: A random number from the normal distribution.
    """
    return math.sqrt(-2.0 * math.log(rnd.random())) * math.cos(2.0 * math.pi * rnd.random()) * sigma + mu

def generate_random_variable_distribution(n: int, callback, ndigits: int = -1, **kwargs) -> np.ndarray:
    """Generates a random variable distribution.

    Args:
        n (int): The number of samples to generate.
        callback (function): The function used to generate each sample.
        ndigits (int, optional): The number of decimal places to round the samples. Defaults to -1.

    Returns:
        np.ndarray: An array of generated samples.
    """
    return np.array([callback(**kwargs) for _ in range(n)]) if ndigits == -1 else np.array([round(callback(**kwargs), ndigits) for _ in range(n)])


def generate_random_normal_variable_box_muller(n: int, mu: float, sigma: float, ndigits: int = -1) -> np.ndarray:
    return np.array([normal_distribution_generator_box_muller(mu, sigma) for _ in range(n)]) if ndigits == -1 else np.array([round(normal_distribution_generator_box_muller(mu, sigma), ndigits) for _ in range(n)])


def show_graph(uniform, normal_distribution, exponential_distribution, uniform_intervals: int = 5, exponential_intervals: int = 5, normal_intervals: int = 5):
    plt.figure(figsize=(15, 10))
    plt.subplot(3, 1, 1)
    plt.hist(uniform, bins=uniform_intervals, alpha=0.7, label='Uniform')
    plt.legend()
    plt.subplot(3, 1, 2)
    plt.hist(normal_distribution, bins=normal_intervals, alpha=0.7, label='Normal')
    plt.legend()
    plt.subplot(3, 1, 3)
    plt.hist(exponential_distribution, bins=exponential_intervals, alpha=0.7, label='Exponential')
    plt.legend()
    plt.show()


def run_test():
    n = int(input('Enter a number: '))
    min = int(input('Enter min value: '))
    max = int(input('Enter max value: '))
    
    n = validate_input_number(n, 1, 1_000_000, 'Please enter a number between 1 and 1.000.000: ')
    min = validate_input_number(min, -1_000_000, 1_000_000, 'Please enter a number between -1.000.000 and 1.000.000: ')
    max = validate_input_number(max, min + 1, 1_000_000, f'Please enter a number between {min + 1} and 1.000.000: ')
    uniform = generate_random_variable_distribution(n, uniform_distribution_generator, min=min, max=max)
    normal_distribution = generate_random_variable_distribution(n, normal_distribution_generator, mu=(min + max) / 2, sigma=(max - min) / 6)
    exponential_distribution = generate_random_variable_distribution(n, negative_exponential_distribution_generator, lamb=1/((min + max) / 2))

    show_graph(uniform, normal_distribution, exponential_distribution)
    input('Press Enter to next interval density...')
    show_graph(uniform, normal_distribution, exponential_distribution, uniform_intervals=10, normal_intervals=10, exponential_intervals=10)
    input('Press Enter to next interval density...')
    show_graph(uniform, normal_distribution, exponential_distribution, uniform_intervals=15, normal_intervals=15, exponential_intervals=15)
    input('Press Enter to next interval density...')
    show_graph(uniform, normal_distribution, exponential_distribution, uniform_intervals=20, normal_intervals=20, exponential_intervals=20)
    input('Press Enter to next interval density...')
    show_graph(uniform, normal_distribution, exponential_distribution, uniform_intervals=25, normal_intervals=25, exponential_intervals=25)

if __name__ == '__main__':
    run_test()
