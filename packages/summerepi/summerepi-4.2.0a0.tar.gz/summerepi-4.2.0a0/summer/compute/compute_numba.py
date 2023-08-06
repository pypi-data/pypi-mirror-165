"""
Optimized 'hot' functions used by CompartmentalModel and its runners.
"""

import numba
import numpy as np

# Use Numba to speed up the calculation of the population.
@numba.jit(nopython=True)
def find_sum(compartment_values: np.ndarray) -> float:
    return compartment_values.sum()


@numba.jit(nopython=True)
def accumulate_positive_flow_contributions(
    flow_rates: np.ndarray,
    comp_rates: np.ndarray,
    pos_flow_map: np.ndarray,
):
    """
    Fast accumulator for summing positive flow rates into their effects on compartments

    Args:
        flow_rates (np.ndarray): Flow rates to be accumulated
        comp_rates (np.ndarray): Output array of compartment rates
        pos_flow_map (np.ndarray): Array of src (flow), target (compartment) indices
    """
    for src, target in pos_flow_map:
        comp_rates[target] += flow_rates[src]
    return comp_rates


@numba.jit(nopython=True)
def accumulate_negative_flow_contributions(
    flow_rates: np.ndarray,
    comp_rates: np.ndarray,
    neg_flow_map: np.ndarray,
):
    """Fast accumulator for summing negative flow rates into their effects on compartments

    Args:
        flow_rates (np.ndarray): Flow rates to be accumulated
        comp_rates (np.ndarray): Output array of compartment rates
        neg_flow_map (np.ndarray): Array of src (flow), target (compartment) indices
    """
    for src, target in neg_flow_map:
        comp_rates[target] -= flow_rates[src]
    return comp_rates


@numba.jit
def get_strain_infection_values(
    strain_infectious_values,
    strain_compartment_infectiousness,
    strain_category_indexer,
    mixing_matrix,
    category_populations,
):
    infected_values = strain_infectious_values * strain_compartment_infectiousness
    # out_arr = np.zeros(num_cats)
    # infectious_populations = sparse_pairs_accum(compartment_category_map, infected_values, out_arr)
    infectious_populations = np.zeros(len(mixing_matrix))
    # infectious_populations = np.sum(infected_values[strain_category_indexer], axis=1)
    for i, cat in enumerate(strain_category_indexer):
        infectious_populations[i] = np.sum(infected_values[cat])
    infection_density = mixing_matrix @ infectious_populations
    category_prevalence = infectious_populations / category_populations
    infection_frequency = mixing_matrix @ category_prevalence

    return infection_density, infection_frequency
