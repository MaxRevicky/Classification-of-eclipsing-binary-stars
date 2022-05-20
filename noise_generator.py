import numpy as np
import matplotlib.pyplot as plt

from elisa import BinarySystem, Observer


def generate_observation_sigma(space_obs_frac=0.5):
    """
    Draws a standard deviation of noise in light curve points from a "true" value provided in synthetic light curve.
    Noise sigma is drawn from bimodal distribution taking into account contributions from space based and earth based
    observations which have different levels of stochastic noise.

    :param space_obs_frac: ratio between earth based and space based observations
    :return: float; standard deviation of the light curve noise
    """
    earth_based_sigma = 4e-3
    space_based_sigma = 2e-4
    sigma = np.random.choice([earth_based_sigma, space_based_sigma], p=[1-space_obs_frac, space_obs_frac])
    return np.random.rayleigh(sigma)


def stochastic_noise_generator(curve):
    """
    Introduces gaussian noise into synthetic observation provided in `curve`.

    :param curve: numpy.array; normalized light curve
    :return: Tuple(numpy.array, float); normalized light curve with added noise, standard deviation of observations
    """
    sigma = generate_observation_sigma()
    return np.random.normal(curve, sigma), np.full(curve.shape, sigma)


if __name__ == "__main__":
    params = {
        "system": {
            "inclination": 85.00,
            "period": 2.72,
            "argument_of_periastron": 101,
            "gamma": 0.0,
            "eccentricity": 0.00,
            "primary_minimum_time": 0.0,
            "phase_shift": 0.0,
            "mass_ratio": 0.8,
            "semi_major_axis": 5.34
        },
        "primary": {
            "surface_potential": 4.0,
            "synchronicity": 1.2,
            "t_eff": 7000.0,
            "metallicity": 0.0
        },
        "secondary": {
            "surface_potential": 4.0,
            "synchronicity": 1.5,
            "t_eff": 5000.0,
            "metallicity": 0.0
        }
    }

    binary = BinarySystem.from_json(params)
    passband = "TESS"
    o = Observer(passband=passband, system=binary)
    phases, lc = o.lc(phases=np.linspace(-0.6, 0.6, 120), normalize=True)

    lc, lc_err = stochastic_noise_generator(lc[passband])

    print(f"Generated sigma: {lc_err}")

    fig = o.plot.lc(return_figure_instance=True)
    plt.errorbar(phases, lc, lc_err, elinewidth=1, lw=0.0, marker="o", ms=2)
    # plt.errorbar(phases, lc, lc_err, marker="o", ms=2)
    plt.show()

    # sigmas = [generate_observation_sigma() for _ in range(10000)]
    # plt.hist(np.log10(sigmas), bins=1000, density=True)
    # plt.xlabel("log(sigma/[normalized flux])")
    # plt.ylabel("Prob. density")
    # plt.show()
