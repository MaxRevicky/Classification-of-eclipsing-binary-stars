import numpy as np
import matplotlib.pyplot as plt
from elisa import BinarySystem, Observer
def curve_alignement_randomizer(curve):
    """
    Randomizes the alignment of the light curve from pre-determined
    phase interval, eg. (0.0, 1.0) to randomized interval (phs_0, phs_0+1).
    :param curve: numpy.array; fluxes
    :return: numpy.array; modified fluxes
    """
    split_index = np.random.randint(0, len(curve))
    return np.concatenate((curve[split_index:], curve[:split_index]))
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
    phases, lc = o.lc(phases=np.linspace(0.0, 1.0, 400), normalize=True)
    lc_r = curve_alignement_randomizer(lc[passband])
    fig = o.plot.lc(return_figure_instance=True)
    plt.plot(phases, lc_r)
    # plt.errorbar(phases, lc, lc_err, marker="o", ms=2)
    plt.show()