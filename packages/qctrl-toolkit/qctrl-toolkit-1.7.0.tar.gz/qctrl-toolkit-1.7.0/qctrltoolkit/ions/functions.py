# Copyright 2022 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

"""
Utility functions for trapped ion systems.
"""
from typing import (
    Any,
    List,
    Tuple,
    Union,
)

import numpy as np
from qctrlcommons.preconditions import check_argument

from qctrltoolkit.namespace import Namespace
from qctrltoolkit.toolkit_utils import expose


@expose(Namespace.IONS)
def obtain_ion_chain_properties(
    qctrl: Any,
    atomic_mass: float,
    ion_count: int,
    center_of_mass_frequencies: List,
    wave_numbers: List,
    laser_detuning: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Obtain the Lamb–Dicke parameters and relative detunings for an ion chain.

    This is essentially a wrapper of the Boulder Opal function
    :func:`~qctrl.dynamic.namespaces.FunctionNamespace.calculate_ion_chain_properties`,
    but returns the result as NumPy arrays.

    Parameters
    ----------
    qctrl : qctrl.Qctrl
        Boulder Opal session object.
    atomic_mass : float
        The atomic mass of the ions of the chain in atomic units.
        This function assumes that all the ions in the chain are from the same atomic species.
    ion_count : int
        The number of ions in the chain, :math:`N`.
    center_of_mass_frequencies : List
        A list of three positive numbers representing the center-of-mass trapping frequency
        in the order of radial x-direction, radial y-direction, and axial z-direction,
        which correspond to the unit vectors :math:`(1, 0, 0)`, :math:`(0, 1, 0)`,
        and :math:`(0, 0, 1)` respectively.
    wave_numbers : List
        A list of three elements representing the the laser difference angular wave vector
        (in units of rad/m) in the order of radial x-direction, radial y-direction, and
        the axial z-direction, which correspond to the unit vectors :math:`(1, 0, 0)`,
        :math:`(0, 1, 0)`, and :math:`(0, 0, 1)` respectively.
    laser_detuning : float
        The detuning of the control laser.

    Returns
    -------
    np.ndarray
        A 3D array of shape ``(3, N, N)`` representing the Lamb–Dicke parameters of the ions.
        Its dimensions indicate, respectively, the direction (radial x-direction,
        radial y-direction, and axial z-direction), the collective mode, and the ion.
    np.ndarray
        A 2D array of shape ``(3, N)`` representing the relative detunings.
        Its dimensions indicate, respectively, the direction (radial x-direction,
        radial y-direction, and axial z-direction) and the collective mode.

    See Also
    --------
    :func:`~qctrl.dynamic.namespaces.FunctionNamespace.calculate_ion_chain_properties` :
        Function to calculate the properties of an ion chain.

    Examples
    --------
    Refer to the `How to optimize error-robust Mølmer–Sørensen gates for trapped ions
    <https://docs.q-ctrl.com/boulder-opal/user-guides/how-to-optimize-error-robust
    -molmer-sorensen-gates-for-trapped-ions>`_ user guide to find how to use this function.
    """

    check_argument(
        isinstance(ion_count, (int, np.integer)) and ion_count >= 1,
        "The ion count must be an integer and greater than 0.",
        {"ion_count": ion_count},
    )
    check_argument(
        _is_positive(atomic_mass),
        "The atomic mass must be positive.",
        {"atomic_mass": atomic_mass},
    )
    check_argument(
        len(center_of_mass_frequencies) == 3,
        "The center_of_mass_frequencies list must have three elements, representing the frequency "
        "in the order of radial x-direction, radial y-direction, and the axial z-direction.",
        {"center_of_mass_frequencies": center_of_mass_frequencies},
    )
    check_argument(
        _is_positive(np.asarray(center_of_mass_frequencies)),
        "All center of mass frequencies must be positive.",
        {"center_of_mass_frequencies": center_of_mass_frequencies},
    )
    check_argument(
        len(wave_numbers) == 3,
        "The wave_numbers list must have three elements, representing the wave vector "
        "in the order of radial x-direction, radial y-direction, and the axial z-direction.",
        {"wave_numbers": wave_numbers},
    )
    check_argument(
        not np.allclose(wave_numbers, 0),
        "At least one of the wave numbers must be non-zero.",
        {"wave_numbers": wave_numbers},
    )

    ion_chain_properties = qctrl.functions.calculate_ion_chain_properties(
        atomic_mass=float(atomic_mass),
        ion_count=int(ion_count),
        radial_x_center_of_mass_frequency=float(center_of_mass_frequencies[0]),
        radial_y_center_of_mass_frequency=float(center_of_mass_frequencies[1]),
        axial_center_of_mass_frequency=float(center_of_mass_frequencies[2]),
        radial_x_wave_number=float(wave_numbers[0]),
        radial_y_wave_number=float(wave_numbers[1]),
        axial_wave_number=float(wave_numbers[2]),
    )

    # The first axis of lamb_dicke_parameters and detuning are directions (x, y, z).
    lamb_dicke_parameters = []
    frequencies = []

    for properties_per_direction in [
        ion_chain_properties.radial_x_mode_properties,
        ion_chain_properties.radial_y_mode_properties,
        ion_chain_properties.axial_mode_properties,
    ]:

        lamb_dicke_parameters.append(
            [p.lamb_dicke_parameters for p in properties_per_direction]
        )
        frequencies.append([p.frequency for p in properties_per_direction])

    return np.asarray(lamb_dicke_parameters), np.asarray(frequencies) - laser_detuning


def _is_positive(x: Union[float, np.ndarray, int]):
    """
    Check the value must be greater than zero, taking into account rounding errors.
    """
    return not np.any(np.isclose(x, 0)) and np.all(x > 0)
