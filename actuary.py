from dataclasses import dataclass
import numpy as np
import pandas as pd


mort_table = pd.read_csv('sa8990.csv', index_col=0)
lapse_table = pd.read_csv('lapses.csv', index_col=0)
eco_table = pd.read_csv('economic.csv', index_col=0)

def shift(xs, n, fill = np.nan):
    e = np.empty_like(xs)
    if n >= 0:
        e[:n] = fill
        e[n:] = xs[:-n]
    else:
        e[n:] = fill
        e[:n] = xs[-n:]
    return e

def pv(cashflows, v_t, p_t = None):
    discounted = cashflows * v_t
    # reverse cumulative sum of discounted
    cumulative = np.cumsum(discounted[::-1])[::-1]
    v_t_shifted = np.concatenate((np.array([1]), v_t[:-1]))
    if p_t:
        p_t_shifted = np.concatenate((np.array([1]), p_t[:-1]))
        v_t_shifted = v_t_shifted
    return cumulative / v_t_shifted

@dataclass
class Policy:
    age: int
    premium: float
    sum_assured: float
    term: int = 999



def project(policy: Policy, proj_term_m = 1200):
    t = np.arange(proj_term_m)
    dur_start = 7 #TODO make duration start a parameter
    dur_m = t + dur_start
    dur_y = dur_m // 12 + 1

    age_m = policy.age * 12 + t
    age_y = age_m // 12
    
    q_x = mort_table['qx'][age_y].to_numpy() * 0
    q_x[12] = 1
    
    p_x_m = (1 - q_x) ** (1/12)
    q_x_m = 1 - p_x_m
    p_t_mort = p_x_m.cumprod()

    lapse_rate = lapse_table['lapse_rate_pa'][dur_y].to_numpy()
    lapse_rate_p_m = (1 - lapse_rate) ** (1/12)
    p_t_lapse = lapse_rate_p_m.cumprod()

    surv_prob = p_x_m * lapse_rate_p_m
    no_pols_if = surv_prob.cumprod()

    no_pols_if_start = np.concatenate((np.array([1.0]), no_pols_if[:-1]))

    no_deaths = no_pols_if_start * (1 - p_x_m)
    no_lapses = (no_pols_if_start - no_deaths) * (1 - lapse_rate_p_m)

    sum_assured_pp = np.full_like(no_pols_if, policy.sum_assured)
    prem_inc_pp = np.full_like(no_pols_if, policy.premium)

    prem_inc = prem_inc_pp * no_pols_if_start
    death_outgo = sum_assured_pp * no_deaths


    discount_rate = eco_table['discount_rate'][t].to_numpy() * 0
    discount_factor = (1 + discount_rate) ** (-1/12)
    v_t = discount_factor.cumprod()

    pv_prem = pv(prem_inc, v_t) / no_pols_if_start
    pv_death_outgo = pv(death_outgo, v_t) / no_pols_if_start

    result = {
        'no_pols_if': no_pols_if,
        'no_deaths': no_deaths,
        'no_lapses': no_lapses,
        'no_pols_if_start': no_pols_if_start,
        'test': (no_pols_if_start - no_deaths - no_lapses - no_pols_if).round(10),
        'discount_rate': discount_rate,
        'discount_factor': discount_factor,
        'v_t': v_t,
        'pv_prem': pv_prem,
        'pv_death_outgo': pv_death_outgo,
    }
    print(pd.DataFrame(result))
    # print(p_x_m, lapse_rate_p_m, surv_prob, no_pols_if, no_pols_if_start, no_deaths, no_lapses, no_pols_if_start - no_deaths - no_lapses)
    # print(no_pols_if_start)
    # print(pd.DataFrame([no_pols_if, no_pols_if_start]))

    # print(p_x_m)
    # print(lapse_table['lapse_rate_pa'][dur_y])



    # q_x = mort

    # return t, dur_m, dur_y, age_m, age_y


project(Policy(age=25, premium=100, sum_assured=100000), 36)

# print(mort_table['qx'])

