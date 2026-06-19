import numpy as np


def monte_carlo(price):

    simulations = []

    for i in range(1000):

        p = price

        for day in range(30):

            p *= np.random.normal(

                1,

                0.015

            )

        simulations.append(p)

    minimum = min(simulations)

    maximum = max(simulations)

    average = np.mean(simulations)

    gain_probability = (

        sum(

            i > price

            for i in simulations

        )

        / len(simulations)

    ) * 100

    return (

        minimum,

        average,

        maximum,

        gain_probability

    )
