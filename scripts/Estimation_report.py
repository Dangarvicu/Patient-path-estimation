# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:42:05 2022

@author: daniel
"""

from config.config import *
from functions.functions import *


#Primero se generan los diccionarios donde se van a guardar los datos.
dictionary_estimated_parameters = {}
for estimator in ESTIMATOR_LIST:
    dictionary_estimated_parameters[estimator] = {}
    for key in ESTIMATION_KEYS:
        dictionary_estimated_parameters[estimator][key] = {}
        dictionary_estimated_parameters[estimator][key][KEY_RESULTS] = []
        dictionary_estimated_parameters[estimator][key][KEY_MEAN] = []
        dictionary_estimated_parameters[estimator][key][KEY_STD] = []
        dictionary_estimated_parameters[estimator][key][KEY_INTERVAL_BOT] = []
        dictionary_estimated_parameters[estimator][key][KEY_INTERVAL_TOP] = []        
        dictionary_estimated_parameters[estimator][key][KEY_PMINIMO] = []
        dictionary_estimated_parameters[estimator][key][KEY_PMEDIANA] = []
        dictionary_estimated_parameters[estimator][key][KEY_PMAXIMO] = []
        for day in range(ESTIMATION_DAYS):
            dictionary_estimated_parameters[estimator][key][KEY_RESULTS].append([])



# Se repite el bucle varias veces
for escenario in LISTA_ESCENARIOS:
    Path = f'{EXCEL_DATA_ROUTE}{PARAMETER_ESTIMATION_EXCEL} {escenario}.xlsx'
    if os.path.isfile(Path):
        for estimator in ESTIMATOR_LIST:
            if estimator == "EM":
                Sheet = "EMW"
            else:
                Sheet = estimator
            df_Paremeters_Estimation=pd.read_excel(Path,Sheet)
            for key in ESTIMATION_KEYS:
                for day in range(ESTIMATION_DAYS):
                    dictionary_estimated_parameters[estimator][key][KEY_RESULTS][day].append(df_Paremeters_Estimation[key][day])
    else:
        print(f'{Path} does not exist.')

for estimator in ESTIMATOR_LIST:
    for key in ESTIMATION_KEYS:
        for day in range(ESTIMATION_DAYS):
            vector_statistics = []
            for value in dictionary_estimated_parameters[estimator][key][KEY_RESULTS][day]:
                if value > 0:
                    vector_statistics.append(value)
            # Mean and interval
            dictionary_estimated_parameters[estimator][key][KEY_MEAN].append(np.array(vector_statistics).mean())
            dictionary_estimated_parameters[estimator][key][KEY_STD].append(np.array(vector_statistics).std(ddof=1))
            interval_bot_value = dictionary_estimated_parameters[estimator][key][KEY_MEAN][day] - INTERVAL_CONSTANT*dictionary_estimated_parameters[estimator][key][KEY_STD][day]
            interval_top_value = dictionary_estimated_parameters[estimator][key][KEY_MEAN][day] + INTERVAL_CONSTANT*dictionary_estimated_parameters[estimator][key][KEY_STD][day]            
            dictionary_estimated_parameters[estimator][key][KEY_INTERVAL_BOT].append(interval_bot_value)
            dictionary_estimated_parameters[estimator][key][KEY_INTERVAL_TOP].append(interval_top_value)
            # Percentiles
            if len(vector_statistics) > 0:
                dictionary_estimated_parameters[estimator][key][KEY_PMINIMO].append(np.percentile(np.array(vector_statistics),MINIMO))
                dictionary_estimated_parameters[estimator][key][KEY_PMEDIANA].append(np.percentile(np.array(vector_statistics),MEDIANA))
                dictionary_estimated_parameters[estimator][key][KEY_PMAXIMO].append(np.percentile(np.array(vector_statistics),MAXIMO))
            else:
                dictionary_estimated_parameters[estimator][key][KEY_PMINIMO].append(NAN)
                dictionary_estimated_parameters[estimator][key][KEY_PMEDIANA].append(NAN)
                dictionary_estimated_parameters[estimator][key][KEY_PMAXIMO].append(NAN)

# Se guardan los resultados en un Excel.
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer_Parameter_Estimation_Results = pd.ExcelWriter(f'{EXCEL_RESULTS_ROUTE}{PARAMETER_ESTIMATION_RESULTS_EXCEL}.xlsx',engine='xlsxwriter')
for key in ESTIMATION_KEYS:
    # Mean and interval
    df_Parameter_Mean_and_Interval= pd.DataFrame()
    df_Parameter_Mean_and_Interval[f'{COLUMN_DAY}'] = df_Paremeters_Estimation[f'{COLUMN_DAY}'].to_numpy().tolist() 
    df_Parameter_Mean_and_Interval[REAL] = generate_real_values_list(key)    
    # Percentiles
    df_Parameter_Percentiles= pd.DataFrame()
    df_Parameter_Percentiles[f'{COLUMN_DAY}'] = df_Paremeters_Estimation[f'{COLUMN_DAY}'].to_numpy().tolist() 
    df_Parameter_Percentiles[REAL] = generate_real_values_list(key)
    for estimator in ESTIMATOR_LIST:
        # Mean and interval
        df_Parameter_Mean_and_Interval[f'{KEY_MEAN}_{estimator}'] = dictionary_estimated_parameters[estimator][key][KEY_MEAN]
        df_Parameter_Mean_and_Interval[f'{KEY_INTERVAL_BOT}_{estimator}'] = dictionary_estimated_parameters[estimator][key][KEY_INTERVAL_BOT]
        df_Parameter_Mean_and_Interval[f'{KEY_INTERVAL_TOP}_{estimator}'] = dictionary_estimated_parameters[estimator][key][KEY_INTERVAL_TOP]
        # Percentiles
        df_Parameter_Percentiles[f'{KEY_PMINIMO}_{estimator}'] = dictionary_estimated_parameters[estimator][key][KEY_PMINIMO]
        df_Parameter_Percentiles[f'{KEY_PMEDIANA}_{estimator}'] = dictionary_estimated_parameters[estimator][key][KEY_PMEDIANA]
        df_Parameter_Percentiles[f'{KEY_PMAXIMO}_{estimator}'] = dictionary_estimated_parameters[estimator][key][KEY_PMAXIMO]
    
    df_Parameter_Mean_and_Interval.to_excel(writer_Parameter_Estimation_Results, sheet_name=f'{key}_mean', index=False)
    df_Parameter_Percentiles.to_excel(writer_Parameter_Estimation_Results, sheet_name=f'{key}_percentiles', index=False)
    

    
# Close the Pandas Excel writer and output the Excel file.
writer_Parameter_Estimation_Results.save()

#Para cambiar los tamaños por defecto.
plt.rcParams.update({'font.size': FONT_SIZE})

x_values = df_Paremeters_Estimation[f'{COLUMN_DAY}'].to_numpy().tolist() 
for key in ESTIMATION_KEYS:
    fig, ax = plt.subplots(figsize=(10,6))
    plt.grid()
    y_values = generate_real_values_list(key)
    max_value = max([x for x in y_values[INITIAL_DAY_OF_REPRESENTATION:] if math.isnan(x) == False])
    if key != KEY_ISE_Z:
        ax.plot(x_values,
            y_values,
            label= f'Real',
            color= 'red')
        key_variable = KEY_PMEDIANA
        key_variable_label = "median"
    else:
        key_variable = KEY_PMEDIANA
        key_variable_label = "median"
    for estimator in ESTIMATOR_LIST:
        label_graph = f'{estimator}'
        if key == KEY_A_Z or key == KEY_B_Z or key == KEY_C_Z or key == KEY_ISE_Z:
            # No se dibujan las gráficas de CI porque se corresponden con las de I.
            if estimator == ESTIMATOR_CI:
                continue
            elif estimator == ESTIMATOR_I:
                label_graph = f'{estimator}, {ESTIMATOR_CI}'
                    
        y_values = dictionary_estimated_parameters[estimator][key][key_variable]
        
        ax.plot(x_values,
        y_values,
        label= label_graph,
        color= DICTIONARY_COLORS[estimator][KEY_COLOR])
        lista_sin_nan = [x for x in y_values[INITIAL_DAY_OF_REPRESENTATION:] if math.isnan(x) == False]
        if len(lista_sin_nan):
            new_max_value = max(lista_sin_nan)
            if max_value < new_max_value:
                max_value = new_max_value

    
    plt.xlim([INITIAL_DAY_OF_REPRESENTATION, x_values[-1]])
    plt.ylim([0, max_value*1.1])
    
    plt.title(f'{key} {key_variable_label}')
    plt.xlabel('Day')
    plt.ylabel('Value')
    
    
    plt.legend()
    plt.show()
    


# =============================================================================
# for i in range(len(ESTIMATOR_LIST)):
#     estimator_i = ESTIMATOR_LIST[i]
#     for j in range(i+1,len(ESTIMATOR_LIST)):
#         estimator_j = ESTIMATOR_LIST[j]
#         print(f'({i},{j})')
#         for key in ESTIMATION_KEYS:
#             for day in DAY_LIST:
#                 print(f'({day}->{ESTIMATOR_LIST[i]},{ESTIMATOR_LIST[j]})')
#                 graph_estimation_in_pairs(day,
#                                           key,
#                                           dictionary_estimated_parameters[estimator_i][key][KEY_RESULTS][day],
#                                           dictionary_estimated_parameters[estimator_j][key][KEY_RESULTS][day],
#                                           estimator_i,
#                                           estimator_j)
#     
#  
# =============================================================================
