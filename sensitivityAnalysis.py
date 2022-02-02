from mapProximity import calculate_radius
import os
import numpy as np
import matplotlib.pyplot as plt

def plot_magnitude_radius():
    """
    Plots the relation between earthquake magnitude and EQIL area radius
    """
    csfont = {'fontname': 'Times New Roman'}
    fig = plt.figure(figsize=(12,7))
    magnitude_range = np.linspace(1, 9, 81)
    # area = [calculate_radius(m, in_pixels=False, return_A_d=True)[0] for m in magnitude_range]
    rad = [calculate_radius(m, in_pixels=False, return_A_d=True)[1] for m in magnitude_range]

    plt.axvline(5.3, c='black', ls='--', alpha=.6)
    # plt.plot(magnitude_range, area, '.')
    plt.plot(magnitude_range, rad, '.')
    plt.title(
        'Sensitivity analysis of the EQIL area for various earthquake magnitudes',
        fontsize=14, **csfont
    )
    plt.xlabel('Earthquake magnitude', **csfont, fontsize=12)
    plt.ylabel('EQIL area radius [km]', **csfont, fontsize=12)
    # plt.legend()
    plt.show()

    if not os.path.isdir('visualizations'):
        os.mkdir('visualizations')
    fig.savefig('visualizations/sensitivity_analysis.png')
