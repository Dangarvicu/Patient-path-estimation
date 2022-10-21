# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:42:05 2022

@author: daniel
"""

from config.config import *
from functions.functions import *

lista_estimadores = ESTIMATOR_LIST + [R]
lista_dias = SIMULATION_DAYS_LIST + [HORIZON_VISUALIZATION]

#Primero se generan los diccionarios donde se van a guardar los datos.
dictionary_simulation_results = {}
for day in lista_dias:
    dictionary_simulation_results[f'{day}'] = {}
    Path = f'{EXCEL_RESULTS_ROUTE}{ICU_SIMULATION_RESULTS_EXCEL} day {day}.xlsx'
    if os.path.isfile(Path):
        for estimator in lista_estimadores:
            dictionary_simulation_results[f'{day}'][estimator] = {}
            if estimator == "EM":
                Sheet = "EMW"
            else:
                Sheet = estimator
            df_Simulation_Results=pd.read_excel(Path,Sheet)
            for key in SIMULATION_RESULTS_KEYS_LIST:
                dictionary_simulation_results[f'{day}'][estimator][key] = [x for x in df_Simulation_Results[key] if math.isnan(x) == False]
    else:
        print(f'{Path} does not exist.')

# Se generan las diferencias de los máximos entre los estimadores y el real.
for day in lista_dias:
    for estimator in lista_estimadores:
        for key in [KEY_MAXIMUM_ICU__BED_OCCUPANCY,KEY_DAY_OF_MAXIMUM_ICU_BED_OCCUPANCY]:
            lista_diferencias_estimado_real = []
            for valor_estimado,valor_real in zip(dictionary_simulation_results[f'{day}'][estimator][key],dictionary_simulation_results[f'{day}'][R][key]):
                lista_diferencias_estimado_real.append(valor_estimado-valor_real)
            if key == KEY_MAXIMUM_ICU__BED_OCCUPANCY:
                new_key = 'Difference in the maximum\nICU bed occupancy'
            else:
                new_key = 'Difference in the day of maximum\nICU bed occupancy'
            dictionary_simulation_results[f'{day}'][estimator][new_key] = lista_diferencias_estimado_real


#Para cambiar los tamaños por defecto.
plt.rcParams.update({'font.size': 20})

# Dibujamos las gráficas
for day in SIMULATION_DAYS_LIST:
    for estimator in lista_estimadores:        
        fig, ax = plt.subplots(figsize=(10,6))
        plt.grid()
        x_values = dictionary_simulation_results[f'{day}'][estimator][KEY_DAY][(day-1):]
        for key,text_label in zip([KEY_ICU_BED_OCCUPANCY_P05,KEY_ICU_BED_OCCUPANCY_P95],[f'{P}{MINIMO}',f'{P}{MAXIMO}']):
            y_values = dictionary_simulation_results[f'{day}'][estimator][key][(day-1):]
            ax.plot(x_values,
                    y_values,
                    label= f'{estimator} {text_label}',
                    color= 'orange')
                    #color= DICTIONARY_COLORS[estimator][KEY_COLOR])
        for key,text_label in zip([KEY_ICU_BED_OCCUPANCY_P05,KEY_ICU_BED_OCCUPANCY_P95],[f'{P}{MINIMO}',f'{P}{MAXIMO}']):   
            y_values = dictionary_simulation_results[f'{day}'][R][key][(day-1):]
            ax.plot(x_values,
                    y_values,
                    label= f'{R} {text_label}',
                    color= DICTIONARY_COLORS[R][KEY_COLOR])
            
        x_values = dictionary_simulation_results[f'{day}'][estimator][KEY_DAY][0:day]
        y_values = dictionary_simulation_results[f'{day}'][R][KEY_ICU_BED_OCCUPANCY_P50][0:day]
        ax.plot(x_values,
                y_values,
                label= f'Real',
                color= 'green')
        x_point = dictionary_simulation_results[f'{day}'][estimator][KEY_DAY][(day-1)]
        y_point = dictionary_simulation_results[f'{day}'][R][KEY_ICU_BED_OCCUPANCY_P50][(day-1)]
        ax.scatter(x_point,
                   y_point,
                   label= f'SSP',
                   color= 'black')
        
        
        plt.title(f'ICU {estimator} ({day}th day)')
        plt.xlabel('Day')
        plt.ylabel('Beds')
        
        
        plt.legend()
        plt.show()
        
    # Medianas en la misma gráfica
    fig, ax = plt.subplots(figsize=(10,6))
    plt.grid()
    x_values = dictionary_simulation_results[f'{HORIZON_VISUALIZATION}'][R][KEY_DAY]
    for estimator in lista_estimadores:
        y_values = dictionary_simulation_results[f'{day}'][estimator][KEY_ICU_BED_OCCUPANCY_P50]
        ax.plot(x_values,
                y_values,
                label= f'{estimator}',
                color= DICTIONARY_COLORS[estimator][KEY_COLOR])
    
    y_values = dictionary_simulation_results[f'{HORIZON_VISUALIZATION}'][R][KEY_ICU_BED_OCCUPANCY_P50]
    ax.plot(x_values,
            y_values,
            label= f'Real',
            color= 'green')
    
    x_point = dictionary_simulation_results[f'{day}'][estimator][KEY_DAY][(day-1)]
    y_point = dictionary_simulation_results[f'{day}'][R][KEY_ICU_BED_OCCUPANCY_P50][(day-1)]
    ax.scatter(x_point,
               y_point,
               label= f'SSP',
               color= 'black')
    
    plt.title(f'ICU ({day}th day)')
    plt.xlabel('Day')
    plt.ylabel('Beds')
    
    
    plt.legend()
    plt.show()

    # Dibujamos boxplots
    draw_boxplot(lista_estimadores,dictionary_simulation_results,KEY_MAXIMUM_ICU__BED_OCCUPANCY,day,False)
    draw_boxplot(lista_estimadores,dictionary_simulation_results,KEY_DAY_OF_MAXIMUM_ICU_BED_OCCUPANCY,day,False)
    # Diferencias
    draw_boxplot(lista_estimadores,dictionary_simulation_results,f'Difference in the maximum\nICU bed occupancy',day,True)
    draw_boxplot(lista_estimadores,dictionary_simulation_results,f'Difference in the day of maximum\nICU bed occupancy',day,True)
    
