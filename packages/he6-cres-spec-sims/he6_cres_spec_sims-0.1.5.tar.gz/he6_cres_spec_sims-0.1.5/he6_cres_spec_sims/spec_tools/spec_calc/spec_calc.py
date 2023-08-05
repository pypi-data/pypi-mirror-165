"""spec_calc

This set of calculators takes cres electron properties (such as energy, pitch angle), as 
well as information about the trap (instance of a trap_profile object) and outputs other 
cres electron properties such as axial frequency, z_max, B_avg.

---
Units for all module functions' inputs/outputs: 

Energy   : eV
B-field  : T
Time     : s
Angle    : degrees
Distance : m
Frequency: Hz
Power    : W


---
"""
# TODO: Organize the imports.
import math
import os

import numpy as np

# from numpy.random import uniform

import scipy.integrate as integrate
from scipy.fft import fft
from scipy.optimize import fmin, fminbound
from scipy.interpolate import interp1d
import scipy.special as ss

# Math constants.

PI = math.pi
RAD_TO_DEG = 180 / math.pi
P11_PRIME = 1.84118  # first zero of J1 prime (bessel functions)

# Physics constants.

ME = 5.10998950e5  # Electron rest mass (eV).
M = 9.1093837015e-31  # Electron rest mass (kg).
Q = 1.602176634e-19  # Electron charge (Coulombs).
C = 299792458  # Speed of light in vacuum, in m/s
J_TO_EV = 6.241509074e18  # Joule-ev conversion
EPS_0 = 8.8541878128 * 10**-12  # Vacuum Permittivity (F/m)


# Simple special relativity functions.


def gamma(energy):
    gamma = (energy + ME) / ME
    return gamma


def momentum(energy):
    momentum = (((energy + ME) ** 2 - ME**2) / C**2) ** 0.5 / J_TO_EV
    return momentum


def velocity(energy):
    velocity = momentum(energy) / (gamma(energy) * M)
    return velocity


# CRES functions.


def energy_to_freq(energy, field):

    """Converts kinetic energy to cyclotron frequency."""

    cycl_freq = Q * field / (2 * PI * gamma(energy) * M)

    return cycl_freq


def freq_to_energy(frequency, field):

    """Calculates energy of beta particle in eV given cyclotron
    frequency in Hz, magnetic field in Tesla, and pitch angle
    at 90 degrees.
    """

    gamma = Q * field / (2 * PI * frequency * M)
    if np.any(gamma < 1):
        gamma = 1
        max_freq = Q * field / (2 * PI * M)
        warning = "Warning: {} higher than maximum cyclotron frequency {}".format(
            frequency, max_freq
        )
        print(warning)
    return gamma * ME - ME


def energy_and_freq_to_field(energy, freq):

    """Converts kinetic energy to cyclotron frequency."""

    field = (2 * PI * gamma(energy) * M * freq) / Q

    return field


def power_from_slope(energy, slope, field):

    """Converts slope, energy, field into the associated cres power."""

    energy_Joules = (energy + ME) / J_TO_EV

    power = slope * (2 * PI) * ((energy_Joules) ** 2) / (Q * field * C**2)

    return power


def random_beta_generator(parameter_dict, rand_seed):

    """TODO(byron): Think about if the phi_initial parameter has an
    effect.

    Generates a random beta in the trap with pitch angle between
    min_theta and max_theta , and initial position (rho,0,z) between
    min_rho and max_rho and min_z and max_z.
    """
    # Initialize rng. Mult by arbitrary int because seed may be used elsewhere.
    rng = np.random.default_rng(rand_seed * 11)

    min_rho = parameter_dict["min_rho"]
    max_rho = parameter_dict["max_rho"]

    min_z = parameter_dict["min_z"]
    max_z = parameter_dict["max_z"]

    min_theta = parameter_dict["min_theta"] / RAD_TO_DEG
    max_theta = parameter_dict["max_theta"] / RAD_TO_DEG

    # TODO: Explain this in words. Had to change this 10122021 because
    # it only worked if min_rho was zero.
    rho_initial = min_rho + np.sqrt(rng.uniform(0, 1) * (max_rho**2 - min_rho**2))
    phi_initial = 2 * PI * rng.uniform(0, 1) * RAD_TO_DEG
    # phi_initial = 0
    z_initial = rng.uniform(min_z, max_z)

    u_min = (1 - np.cos(min_theta)) / 2
    u_max = (1 - np.cos(max_theta)) / 2

    sphere_theta_initial = np.arccos(1 - 2 * (rng.uniform(u_min, u_max))) * RAD_TO_DEG
    sphere_phi_initial = 2 * PI * rng.uniform(0, 1) * RAD_TO_DEG

    position = [rho_initial, phi_initial, z_initial]
    direction = [sphere_theta_initial, sphere_phi_initial]

    return position, direction


def theta_center(zpos, rho, pitch_angle, trap_profile):

    """Calculates the pitch angle an electron with current z-coordinate
    zpos, rho, and current pitch angle pitch_angle takes at the center
    of given trap.
    """

    if trap_profile.is_trap:

        Bmin = trap_profile.field_strength(rho, 0.0)
        Bcurr = trap_profile.field_strength(rho, zpos)

        theta_center_calc = (
            np.arcsin((np.sqrt(Bmin / Bcurr)) * np.sin(pitch_angle / RAD_TO_DEG))
            * RAD_TO_DEG
        )

        return theta_center_calc

    else:
        print("ERROR: Given trap profile is not a valid trap")
        return False


def cyc_radius(energy, field, pitch_angle):

    """Calculates the instantaneous cyclotron radius of a beta electron
    given the energy, magnetic field, and current pitch angle.
    """

    vel_perp = velocity(energy) * np.sin(pitch_angle / RAD_TO_DEG)

    cyc_radius = (gamma(energy) * M * vel_perp) / (Q * field)

    return cyc_radius


def max_radius(energy, center_pitch_angle, rho, trap_profile):

    """Calculates the maximum cyclotron radius of a beta electron given
    the kinetic energy, trap_profile, and center pitch angle (pitch angle
    at center of trap).
    """

    if trap_profile.is_trap:

        min_field = trap_profile.field_strength(rho, 0)
        max_field = min_field / (np.sin(center_pitch_angle / RAD_TO_DEG)) ** 2

        center_radius = cyc_radius(energy, min_field, center_pitch_angle)
        end_radius = cyc_radius(energy, max_field, pitch_angle=90)

        if np.all(center_radius >= end_radius):
            return center_radius
        else:
            print(
                "Warning: max_radius is occuring at end of trap (theta=90). \
                Something odd may be going on."
            )
            return False

    else:
        print("ERROR: Given trap profile is not a valid trap")
        return False


def min_radius(energy, center_pitch_angle, rho, trap_profile):

    """Calculates the minimum cyclotron radius of a beta electron given
    the kinetic energy, trap_profile, and center pitch angle (pitch angle
    at center of trap).
    """

    if trap_profile.is_trap:

        min_field = trap_profile.field_strength(rho, 0)
        max_field = min_field / (np.sin(center_pitch_angle / RAD_TO_DEG)) ** 2

        center_radius = cyc_radius(energy, min_field, center_pitch_angle)
        end_radius = cyc_radius(energy, max_field, pitch_angle=90)

        if np.all(center_radius >= end_radius):
            return end_radius
        else:
            print(
                "Warning: min_radius is occuring at center of trap, something \
                odd may be going on."
            )
            return False

    else:
        print("ERROR: Given trap profile is not a valid trap")
        return False


def min_theta(rho, zpos, trap_profile):

    """Calculates the minimum pitch angle theta at which an electron at
    zpos is trapped given trap_profile.
    """

    if trap_profile.is_trap:

        # Be careful here. Technically the Bmax doesn't occur at a constant z.
        Bmax = trap_profile.field_strength(rho, trap_profile.trap_width[1])
        Bz = trap_profile.field_strength(rho, zpos)

        theta = np.arcsin((Bz / Bmax) ** 0.5) * RAD_TO_DEG
        return theta

    else:
        print("ERROR: Given trap profile is not a valid trap")
        return False


def max_zpos_not_vectorized(energy, center_pitch_angle, rho, trap_profile, debug=False):

    """Calculates the maximum axial length from center of trap as a
    function of center_pitch_angle and rho. Not vectorized. See below
    for vectorized version.
    """

    if trap_profile.is_trap:

        if center_pitch_angle < min_theta(rho, 0, trap_profile):
            print("WARNING: Electron not trapped (zpos)")
            return False

        else:
            # Ok, so does this mean we now have an energy dependence on zmax? Yes.
            c_r = cyc_radius(
                energy, trap_profile.field_strength(rho, 0), center_pitch_angle
            )
            rho_p = np.sqrt(rho**2 + c_r**2 / 2)

            min_field = trap_profile.field_strength(rho_p, 0)
            max_field = trap_profile.field_strength(rho_p, trap_profile.trap_width[1])

            max_reached_field = min_field / pow(
                math.sin(center_pitch_angle * math.pi / 180), 2
            )

            # initial guess based on treating magnetic well as v-shaped
            slope = (max_field - min_field) / (trap_profile.trap_width[1])
            initial_z = (max_reached_field - min_field) / slope

            if initial_z == trap_profile.trap_width[1]:
                return initial_z

            def func(z):
                curr_field = trap_profile.field_strength(rho_p, z)
                return abs(curr_field - max_reached_field)

            max_z = fminbound(func, 0, trap_profile.trap_width[1], xtol=1e-14)
            curr_field = trap_profile.field_strength(rho_p, max_z)

            if (curr_field > max_reached_field) and debug == True:
                print(
                    "Final field greater than max allowed field by: ",
                    curr_field - max_reached_field,
                )
                print("Bmax reached: ", curr_field)

            if debug == True:
                print("zlength: ", max_z)

            if max_z > trap_profile.trap_width[1]:
                print("Error Rate: ", max_z - trap_profile.trap_width[1])

            return max_z

    else:
        print("ERROR: Given trap profile is not a valid trap")
        return False


def max_zpos(energy, center_pitch_angle, rho, trap_profile, debug=False):

    """Vectorized version of max_zpos_not_vectorized function."""

    max_zpos_vectorized = np.vectorize(max_zpos_not_vectorized)

    return max_zpos_vectorized(energy, center_pitch_angle, rho, trap_profile)


def mod_index(avg_cycl_freq, zmax):

    """Calculates modulation index from average cyclotron frequency
    (avg_cycl_freq) and maximum axial amplitude (zmax).
    """

    # fixed experiment parameters
    waveguide_radius = 0.578e-2
    kc = P11_PRIME / waveguide_radius

    # calculated parameters
    omega = 2 * PI * avg_cycl_freq
    k_wave = omega / C
    beta = np.sqrt(k_wave**2 - kc**2)

    mod_index = zmax * beta

    return mod_index


def df_dt(energy, field, power):

    """Calculates cyclotron frequency rate of change of electron with
    given kinetic energy at field in T radiating energy at rate power.
    """

    energy_Joules = (energy + ME) / J_TO_EV

    slope = (Q * field * C**2) / (2 * PI) * (power) / (energy_Joules) ** 2

    return slope


def curr_pitch_angle(rho, zpos, center_pitch_angle, trap_profile):

    """Calculates the current pitch angle of an electron at zpos given
    center pitch angle and main field strength.
    """

    if trap_profile.is_trap:

        min_field = trap_profile.field_strength(rho, 0)
        max_z = max_zpos(center_pitch_angle, rho, trap_profile)
        max_reached_field = trap_profile.field_strength(rho, max_z)

        if np.any(abs(zpos) > max_z):
            print("Electron does not reach given zpos")
            curr_pitch = "FAIL"
        else:
            curr_field = trap_profile.field_strength(rho, zpos)
            curr_pitch = np.arcsin(np.sqrt(curr_field / max_reached_field)) * RAD_TO_DEG

        return curr_pitch

    else:
        print("ERROR: Given trap profile is not a valid trap")
        return False


def axial_freq_not_vect(energy, center_pitch_angle, rho, trap_profile):

    """Caculates the axial frequency of a trapped electron."""

    if trap_profile.is_trap:
        # center_pitch_angle = np.where(center_pitch_angle == 90.0, 89.999, center_pitch_angle)
        if center_pitch_angle == 90.0:
            center_pitch_angle = 89.999

        zmax = max_zpos(energy, center_pitch_angle, rho, trap_profile)

        c_r = cyc_radius(
            energy, trap_profile.field_strength(rho, 0), center_pitch_angle
        )
        rho_p = np.sqrt(rho**2 + c_r**2 / 2)

        B = lambda z: trap_profile.field_strength(rho_p, z)
        Bmax = trap_profile.field_strength(rho_p, zmax)

        # Secant of theta as function of z. Use conserved mu to derive.
        sec_theta = lambda z: (1 - B(z) / Bmax) ** (-0.5)
        T_a = 4 / velocity(energy) * integrate.quad(sec_theta, 0, zmax)[0]

        axial_frequency = 1 / T_a

        return axial_frequency

    else:
        print("ERROR: Given trap profile is not a valid trap")
        return False


def axial_freq(energy, center_pitch_angle, rho, trap_profile):

    """Vectorized version of axial_freq_not_vectorized function."""

    axial_freq_vect = np.vectorize(axial_freq_not_vect)

    return axial_freq_vect(energy, center_pitch_angle, rho, trap_profile)


def avg_cycl_freq_not_vect(energy, center_pitch_angle, rho, trap_profile):

    """Calculates the average cyclotron frquency of an electron given
    kinetic energy, main field, and center pitch angle.
    Returns 0 if electron is not trapped.
    """

    if trap_profile.is_trap:

        Bmin = trap_profile.field_strength(rho, 0)
        min_trapped_angle = min_theta(rho, 0, trap_profile)

        if center_pitch_angle < min_trapped_angle:
            print("Warning: (avg_cyc) electron not trapped.")
            return False

        if center_pitch_angle == 90.0:
            avg_cyc_freq = energy_to_freq(energy, Bmin)

        else:
            zmax = max_zpos(energy, center_pitch_angle, rho, trap_profile)
            B = lambda z: trap_profile.field_strength(rho, z)
            Bmax = trap_profile.field_strength(rho, zmax)
            integrand = lambda z: B(z) * ((1 - B(z) / Bmax) ** (-0.5))

            ax_freq = axial_freq(energy, center_pitch_angle, rho, trap_profile)

            # Similar to axial_freq calculation.
            avg_cyc_freq = (
                4
                * Q
                * ax_freq
                / (2 * PI * momentum(energy))
                * integrate.quad(integrand, 0, zmax, epsrel=10**-2)[0]
            )

        return avg_cyc_freq

    else:
        print("ERROR: Given trap profile is not a valid trap")
        return False


def avg_cycl_freq(energy, center_pitch_angle, rho, trap_profile):

    field = b_avg(energy, center_pitch_angle, rho, trap_profile)

    return energy_to_freq(energy, field)


def b_avg_not_vect(energy, center_pitch_angle, rho, trap_profile):

    """Calculates the average magnetic field experienced by an electron
    of a given kinetic energy, main field, and center pitch angle.
    Returns 0 if electron is not trapped.
    """

    c_r = cyc_radius(energy, trap_profile.field_strength(rho, 0), center_pitch_angle)

    rho_p = np.sqrt(rho**2 + c_r**2 / 2)
    rho_pp = np.sqrt(rho**2 + c_r**2)

    if trap_profile.is_trap:

        Bmin = trap_profile.field_strength(rho_p, 0)
        min_trapped_angle = min_theta(rho_p, 0, trap_profile)

        if center_pitch_angle < min_trapped_angle:
            print("Warning: (avg_cyc) electron not trapped.")
            return False

        if center_pitch_angle == 90.0:
            avg_cyc_freq = energy_to_freq(energy, Bmin)

        else:

            zmax = max_zpos(energy, center_pitch_angle, rho, trap_profile)
            B1 = lambda z: trap_profile.field_strength(rho_pp, z)
            B = lambda z: trap_profile.field_strength(rho_p, z)
            Bmax = trap_profile.field_strength(rho_p, zmax)
            integrand = lambda z: B1(z) * ((1 - B(z) / Bmax) ** (-0.5))

            ax_freq = axial_freq(energy, center_pitch_angle, rho, trap_profile)

            # Similar to axial_freq calculation.
            b_avg = (
                4
                * ax_freq
                / (velocity(energy))
                * integrate.quad(integrand, 0, zmax, epsrel=10**-3)[0]
            )

        return b_avg

    else:
        print("ERROR: Given trap profile is not a valid trap")
        return False


def b_avg(energy, center_pitch_angle, rho, trap_profile):

    """Vectorized version of b_avg_not_vectorized function."""

    b_avg_vect = np.vectorize(b_avg_not_vect)

    return b_avg_vect(energy, center_pitch_angle, rho, trap_profile)


def t_not_vect(energy, zpos, center_pitch_angle, rho, trap_profile):

    """DEBUG(byron): This is returning negative times.
    Caculates the time for electron to travel from z = 0 to zpos.
    """

    if trap_profile.is_trap:

        if center_pitch_angle == 90.0:
            center_pitch_angle = 89.999

        zmax = max_zpos(energy, center_pitch_angle, rho, trap_profile)
        B = lambda z: trap_profile.field_strength(rho, z)
        Bmax = trap_profile.field_strength(rho, zmax)

        # Secant of theta as function of z. Use conserved mu to derive.
        sec_theta = lambda z: (1 - B(z) / Bmax) ** (-0.5)
        t = (
            1
            / velocity(energy)
            * integrate.quad(sec_theta, 0, zpos, epsrel=10**-2)[0]
        )

        if zpos > zmax:
            print("ERROR: zpos equal to or larger than zmax.")

        return t

    else:
        print("ERROR: Given trap profile is not a valid trap")
        return False


def t(energy, zpos, center_pitch_angle, rho, trap_profile):

    """Vectorized version of t_not_vect function."""

    t_vect = np.vectorize(t_not_vect)

    return t_vect(energy, zpos, center_pitch_angle, rho, trap_profile)


def sideband_calc(avg_cycl_freq, axial_freq, zmax, num_sidebands=7):

    """Calculates relative magnitudes of num_sidebands sidebands from
    average cyclotron frequency (avg_cycl_freq), axial frequency
    (axial_freq), and maximum axial amplitude (zmax).
    """

    # fixed experiment parameters
    waveguide_radius = 0.578e-2
    kc = P11_PRIME / waveguide_radius

    # calculated parameters
    omega = 2 * PI * avg_cycl_freq
    k_wave = omega / C
    beta = np.sqrt(k_wave**2 - kc**2)

    phase_vel = omega / beta

    mod_index = omega * zmax / phase_vel

    # Calculate K factor
    K = 2 * PI * avg_cycl_freq * zmax / phase_vel

    # Calculate list of (frequency, amplitude) of sidebands
    sidebands = []

    for k in range(-num_sidebands, num_sidebands + 1):

        freq = avg_cycl_freq + k * axial_freq
        magnitude = abs(ss.jv(k, K))

        pair = (freq, magnitude)
        sidebands.append(pair)

    return sidebands, mod_index

def anharmonic_axial_trajectory():
    """ Computes the time series of the beta axial motion over a single
    found by integrating the relevant ODE. Returns [z(t), vz(t)].
    """
    T  = 1. / axial_freq()
    nHarmonics = 128
    dt = T/ nHarmonics
    t = np.arange(0,T,dt)

    mu = p0**2 * np.sin(theta0)**2 / (2. * me * B0) #### XXX: Check gammas!!!
    ### Coupled ODE for z-motion: z = y[0], vz = y[1]. z'=vz. vz' = -mu * B'(z) / m
    ode = lambda t, y: [y[1], - mu / me * dfTot(y[0])]
    result = integrate.solve_ivp(ode, [t[0], t[-1]], (zmax, 0), t_eval=t,rtol=1e-7)

    ####### [0] is z array, [1] is vz array ######
    return result.y

def instantaneous_frequency(z, vz):
    """ Computes the instantaneous (angular) frequency as a function of time
    """
    return q * B(z) / (me * gamma) * ( 1. + vz / v_ph)

def anharmonic_sideband_powers(num_sidebands=7):
    omega_c -= np.mean(omega_c)
    Phi = np.cumsum(omega_c) * dt
    expPhi = np.exp(1j * Phi)
    yf = np.abs(fft(expPhi,norm="forward"))
    yf = yf[:nHarmonics//2]

    # Calculate list of (frequency, amplitude) of sidebands
    sidebands = []

    for k in range(-num_sidebands, num_sidebands + 1):
        freq = avg_cycl_freq + k * axial_freq
        magnitude = yf[abs(k)]
        pair = (freq, magnitude)
        sidebands.append(pair)

    ### Intentionally returns modulation index of nan as it is not (meaningfully) defined for harmonic traps
    return sidebands, np.nan

def power_larmor(field, frequency):

    omega = 2 * PI * frequency
    energy = freq_to_energy(frequency, field)
    r_c = cyc_radius(energy, field, 90)
    beta = velocity(energy) / C
    p = gamma(energy) * M * velocity(energy)

    power_larmor = (2 / 3 * Q**2 * C * beta**4 * gamma(energy) ** 4) / (
        4 * PI * EPS_0 * r_c**2
    )

    return power_larmor
