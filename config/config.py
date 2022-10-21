# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:40:37 2022

@author: daniel
"""


LISTA_ESCENARIOS = list(range(1, 101))
#LISTA_ESCENARIOS = [1,2,4,7,10]

REAL = 'Real'
R = 'R'

ESTIMATOR_CI = "CI"
ESTIMATOR_I = "I"
ESTIMATOR_IQ2 = "IQ2"
ESTIMATOR_IQ3 = "IQ3"
ESTIMATOR_EM_WEIBULL = "EM"
ESTIMATOR_EM_LOGNORMAL = "EML"
ESTIMATOR_EM_BEST = "EMB"
ESTIMATOR_NP = "NP"
ESTIMATOR_EMNP = "EMNP"

ESTIMATOR_LIST = [ESTIMATOR_NP,
                  ESTIMATOR_EM_WEIBULL,
                  ESTIMATOR_EMNP,
                  ESTIMATOR_CI,
                  ESTIMATOR_I,
                  ESTIMATOR_IQ2,
                  ESTIMATOR_IQ3
                  ]

# =============================================================================
# ESTIMATOR_LIST = [ESTIMATOR_CI,
#                   ESTIMATOR_NP
#                   ]
# =============================================================================


KEY_DAILY_ROW_LIST = "Daily Row list"
KEY_P_WI = 'p_WI'
KEY_A_X = 'β_X'
KEY_B_X = 'α_X'
KEY_C_X = 'µ_X'
KEY_A_Z = 'β_Z'
KEY_B_Z = 'α_Z'
KEY_C_Z = 'µ_Z'
KEY_ISE_Z = 'ISE_Z'
ESTIMATION_KEYS = [KEY_P_WI,
                   KEY_A_X,
                   KEY_B_X,
                   KEY_C_X,
                   KEY_A_Z,
                   KEY_B_Z,
                   KEY_C_Z,
                   KEY_ISE_Z]

INTERVAL_CONSTANT = 1.96

P = 'P'
MINIMO = 5
MEDIANA = 50
MAXIMO = 95

KEY_RESULTS = "Results"
KEY_MEAN = "Mean"
KEY_STD = "Std"
KEY_INTERVAL_BOT = "BI"
KEY_INTERVAL_TOP = "TI"
KEY_PMINIMO = f'P{MINIMO}'
KEY_PMEDIANA = f'P{MEDIANA}'
KEY_PMAXIMO = f'P{MAXIMO}'


DAY_LIST = [10,15,20,25,30]



ESTIMATION_DAYS = 81

NAN = float("NaN")


FONT_SIZE = 15

DATE_FORMAT = '%d/%m/%Y'

# GOMPERTZ DATA
HORIZON_VISUALIZATION = 150

DERIVADA = "Derivada"
ACUMULADA = "Acumulada"

FIT_FUNCTION = "Derivada" # "Acumulada", "Derivada"

TOTAL_CASES = 5000
NUMBER_OF_PANDEMIC_DAYS = 60

POPULATION_AFFECTED = 0.9

Y0_FIXED_CASES_POINT = 1
X0_FIXED_DAY_POINT = "01/01/2022"
START_DATE = "01/01/2022"

ESTIMATION = "Estimation"
SIMULATION = "Simulation"


# STAYS DATA
# 01/07/2020 - 01/10/2021
# 5037 patients

WEIBULL = "Weibull"
LOGNORMAL = "Lognormal"
TRIANGULAR = "Triangular"
BEST = "Best"

Q2 = 0.5
Q3 = 0.75

# Stays
PROBABILITY_DISTINGUISH_LONG_STAYS = 0.95

STAYS_PROBABILITY_DISTRIBUTION = WEIBULL
if STAYS_PROBABILITY_DISTRIBUTION == LOGNORMAL:
    PARAMETER_a_X = 1.947
    PARAMETER_b_X = 0.778
    PARAMETER_c_X = 9.488
    PARAMETER_a_Z = 1.061
    PARAMETER_b_Z = 0.770
    PARAMETER_c_Z = 3.886
    PARAMETER_a_Y = 2.365
    PARAMETER_b_Y = 0.950
    PARAMETER_c_Y = 16.711
    PARAMETER_a_Q = 2.105
    PARAMETER_b_Q = 0.744
    PARAMETER_c_Q = 10.824
elif STAYS_PROBABILITY_DISTRIBUTION == WEIBULL:
    PARAMETER_a_X = 1.25
    PARAMETER_b_X = 10.20
    PARAMETER_c_X = 9.50
    PARAMETER_a_Z = 1.15
    PARAMETER_b_Z = 4.10
    PARAMETER_c_Z = 3.90
    PARAMETER_a_Y = 1.10
    PARAMETER_b_Y = 17.30
    PARAMETER_c_Y = 16.70
    PARAMETER_a_Q = 1.40
    PARAMETER_b_Q = 11.85
    PARAMETER_c_Q = 10.80

# Porcentajes
P_I = 0.028
P_WI = 0.088
P_IW = 0.816

ISE_Z = 0

ISE_T_MAX = 81
STEP_ISE = 0.001


POSITION_DAY = 0
POSITION_P_WI = 1
POSITION_DISTRIBUTION_X = 2
POSITION_A_X = 3
POSITION_B_X = 4
POSITION_C_X = 5
POSITION_DISTRIBUTION_Z = 6
POSITION_A_Z = 7
POSITION_B_Z = 8
POSITION_C_Z = 9
POSITION_ISE_Z = 10



# Ruta Exceles
EXCEL_DATA_ROUTE = 'data/'
EXCEL_RESULTS_ROUTE = 'results/'

# Nombres de los exceles.
INPUT_DATA_EXCEL = "Input data"
SHEET_SIMULATED_STAYS = "Simulated stays"
SHEET_GOMPERTZ_ARRIVALS = "Gompertz arrivals"
COLUMN_DATE_HA = 'date_HA'
COLUMN_DATE_HD = 'date_HD'
COLUMN_DATE_IA = 'date_IA'
COLUMN_DATE_ID = 'date_ID'
COLUMN_DAY = "Day"
COLUMN_G_REAL = "G_real"
COLUMN_G_POISSON = "G_poisson"

PARAMETER_ESTIMATION_EXCEL = "Parameter estimation"
COLUMN_DAY = 'Day'
COLUMN_P_WI = 'p_WI'
COLUMN_DISTRIBUTION_X = 'Distribution X'
COLUMN_A_X = 'β_X'
COLUMN_B_X = 'α_X'
COLUMN_C_X = 'µ_X'
COLUMN_DISTRIBUTION_Z = 'Distribution Z'
COLUMN_A_Z = 'β_Z'
COLUMN_B_Z = 'α_Z'
COLUMN_C_Z = 'µ_Z'
COLUMN_ISE_Z = 'ISE_Z'

PARAMETER_ESTIMATION_RESULTS_EXCEL = "Parameter estimation results"


KEY_DAY = COLUMN_DAY
KEY_P_WI = COLUMN_P_WI
KEY_DISTRIBUTION_X = COLUMN_DISTRIBUTION_X
KEY_A_X = COLUMN_A_X
KEY_B_X = COLUMN_B_X
KEY_C_X = COLUMN_C_X
KEY_DISTRIBUTION_Z = COLUMN_DISTRIBUTION_Z
KEY_A_Z = COLUMN_A_Z
KEY_B_Z = COLUMN_B_Z
KEY_C_Z = COLUMN_C_Z
KEY_ISE_Z = COLUMN_ISE_Z



KEY_COLOR = 'color'
DICTIONARY_COLORS = {ESTIMATOR_CI: {KEY_COLOR: 'grey'},
                       ESTIMATOR_I: {KEY_COLOR: 'orange'},
                       ESTIMATOR_IQ2: {KEY_COLOR: 'pink'},
                       ESTIMATOR_IQ3: {KEY_COLOR: 'brown'},
                       ESTIMATOR_EM_WEIBULL: {KEY_COLOR: 'olive'},
                       ESTIMATOR_EM_LOGNORMAL: {KEY_COLOR: 'blue'},
                       ESTIMATOR_EM_BEST: {KEY_COLOR: 'red'},
                       ESTIMATOR_NP: {KEY_COLOR: 'purple'},
                       ESTIMATOR_EMNP: {KEY_COLOR: 'cyan'},
                       R: {KEY_COLOR: 'blue'}
                       }


INITIAL_DAY_OF_REPRESENTATION = 7



# SIMULATION
PARAMETER_SIMULATION_EXCEL = "Input data simulation"


# Semilla de la simulación
RANDOM_SEED = 357386
RANDOM_LSIT_SIZE = 1000000

SIMULATION_REPLICACTIONS = 10#500

SIMULATION_DAYS_LIST = [15, 20, 25, 30]



ICU_SIMULATION_RESULTS_EXCEL = "ICU simulation results"

COLUMN_DAILY_CASES_P05 = 'Daily cases (P_05)'
COLUMN_DAILY_CASES_P50 = 'Daily cases (P_50)'
COLUMN_DAILY_CASES_P95 = 'Daily cases (P_95)'
COLUMN_DIRECT_ADMISSIONS_IN_ICU_P05 = 'Daily direct admissions in ICU (P_05)'
COLUMN_DIRECT_ADMISSIONS_IN_ICU_P50 = 'Daily direct admissions in ICU (P_50)'
COLUMN_DIRECT_ADMISSIONS_IN_ICU_P95 = 'Daily direct admissions in ICU (P_95)'
COLUMN_ICU_ADMISSIONS_FROM_WARDS_P05 = 'Daily admissions in ICU from wards (P_05)'
COLUMN_ICU_ADMISSIONS_FROM_WARDS_P50 = 'Daily admissions in ICU from wards (P_50)'
COLUMN_ICU_ADMISSIONS_FROM_WARDS_P95 = 'Daily admissions in ICU from wards (P_95)'
COLUMN_ICU_ADMISSIONS_P05 = 'Daily ICU admissions (P_05)'
COLUMN_ICU_ADMISSIONS_P50 = 'Daily ICU admissions (P_50)'
COLUMN_ICU_ADMISSIONS_P95 = 'Daily ICU admissions (P_95)'
COLUMN_DIRECT_ICU_DISCHARGES_P05 = 'Direct ICU discharges (P_05)'
COLUMN_DIRECT_ICU_DISCHARGES_P50 = 'Direct ICU discharges (P_50)'
COLUMN_DIRECT_ICU_DISCHARGES_P95 = 'Direct ICU discharges (P_95)'
COLUMN_ICU_DISCHARGES_TO_WARDS_P05 = 'ICU discharges to wards (P_05)'
COLUMN_ICU_DISCHARGES_TO_WARDS_P50 = 'ICU discharges to wards (P_50)'
COLUMN_ICU_DISCHARGES_TO_WARDS_P95 = 'ICU discharges to wards (P_95)'
COLUMN_ICU_DISCHARGES_P05 = 'ICU discharges (P_05)'
COLUMN_ICU_DISCHARGES_P50 = 'ICU discharges (P_50)'
COLUMN_ICU_DISCHARGES_P95 = 'ICU discharges (P_95)'
COLUMN_ICU_BED_OCCUPANCY_P05 = 'ICU bed occupancy (P_05)'
COLUMN_ICU_BED_OCCUPANCY_P50 = 'ICU bed occupancy (P_50)'
COLUMN_ICU_BED_OCCUPANCY_P95 = 'ICU bed occupancy (P_95)'

COLUMN_REPLICATION = "Replication"
COLUMN_MAXIMUM_ICU__BED_OCCUPANCY = "Maximum ICU bed occupancy"
COLUMN_DAY_OF_MAXIMUM_ICU_BED_OCCUPANCY = "Day of maximum ICU bed occupancy"

KEY_ICU_BED_OCCUPANCY_P05 = COLUMN_ICU_BED_OCCUPANCY_P05
KEY_ICU_BED_OCCUPANCY_P50 = COLUMN_ICU_BED_OCCUPANCY_P50
KEY_ICU_BED_OCCUPANCY_P95 = COLUMN_ICU_BED_OCCUPANCY_P95
KEY_MAXIMUM_ICU__BED_OCCUPANCY = COLUMN_MAXIMUM_ICU__BED_OCCUPANCY
KEY_DAY_OF_MAXIMUM_ICU_BED_OCCUPANCY = COLUMN_DAY_OF_MAXIMUM_ICU_BED_OCCUPANCY

SIMULATION_RESULTS_KEYS_LIST = [KEY_DAY,
                                KEY_ICU_BED_OCCUPANCY_P05,
                                KEY_ICU_BED_OCCUPANCY_P50,
                                KEY_ICU_BED_OCCUPANCY_P95,
                                KEY_MAXIMUM_ICU__BED_OCCUPANCY,
                                KEY_DAY_OF_MAXIMUM_ICU_BED_OCCUPANCY
                                ]