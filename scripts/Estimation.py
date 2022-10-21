# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:42:05 2022

@author: daniel
"""

from config.config import *
from functions.functions import *



start_DT = datetime.now()
print ('Comienzo programa: '+str(start_DT))

# Se repite el bucle varias veces
for escenario in LISTA_ESCENARIOS:
    print(f'Escenario {escenario}')

    # Se genera la curva de llegadas
    if FIT_FUNCTION == DERIVADA:
        fit_function = Gompertz_Temp_Derivada
    elif FIT_FUNCTION == ACUMULADA:
        fit_function = Gompertz_Temp
    y_new_cases_Poisson, x_personalized, y_personalized = generate_arrivals_curve(START_DATE,
                                                                                  X0_FIXED_DAY_POINT,
                                                                                  DATE_FORMAT,
                                                                                  POPULATION_AFFECTED,
                                                                                  TOTAL_CASES,
                                                                                  NUMBER_OF_PANDEMIC_DAYS,
                                                                                  Y0_FIXED_CASES_POINT,
                                                                                  HORIZON_VISUALIZATION,
                                                                                  fit_function,
                                                                                  ESTIMATION)
    # Simulación de llegadas y estancias
    rows_list,aux_1,aux_2,aux_3,aux_4,aux_5,aux_6,aux_7,aux_8 = simulate_stays_and_pathway(y_new_cases_Poisson,[],0,[],0,[],0,[],0,[],0,[],0,[],0,[],0)
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    save_file_stays_and_arrivals(f'{EXCEL_DATA_ROUTE}{INPUT_DATA_EXCEL} {escenario}_TEST.xlsx',
                                 rows_list,
                                 x_personalized,
                                 y_personalized,
                                 y_new_cases_Poisson)
    
        
# =============================================================================
#     ########
#     ESTIMATOR_LIST = [ESTIMATOR_NP
#                   ]
#     df_Estancias_simuladas=pd.read_excel(f'{EXCEL_DATA_ROUTE}Input data {escenario}.xlsx')
#     rows_list = []
#     for date_HA, date_HD, date_IA, date_ID in zip(df_Estancias_simuladas['date_HA'],df_Estancias_simuladas['date_HD'],df_Estancias_simuladas['date_IA'],df_Estancias_simuladas['date_ID']):
#         rows_list.append([date_HA, date_HD, date_IA, date_ID])
#     ########
# =============================================================================
    
    
    # Estimación de los parámetros
    # En cada día se calculan las estimaciones de todos los métodos incluidos en el estudio.
    
    #Primero se generan los diccionarios donde se van a guardar los datos.
    dictionary_estimated_parameters = {}
    for estimator in ESTIMATOR_LIST:
        dictionary_estimated_parameters[estimator] = {}
        dictionary_estimated_parameters[estimator][KEY_DAILY_ROW_LIST] = []
    
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer_Parameter_Estimation = pd.ExcelWriter(f'{EXCEL_DATA_ROUTE}{PARAMETER_ESTIMATION_EXCEL} {escenario}_TEST.xlsx',engine='xlsxwriter')
    
    for dia_simulacion in range(ESTIMATION_DAYS):
        print('*******')
        #dia_simulacion = 42
        print(dia_simulacion)
        
        
        df_Stays = generate_data_frame_stays_in_day_d(rows_list,dia_simulacion)
        
         
        
        #####################################################################
        
        # Algoritmo de estimación de los parámetros.
        # Realizamos diferentes algoritmos
        for estimator in ESTIMATOR_LIST:
            parametros_list = []
            parametros_list.append(dia_simulacion)
            # Se elige el algoritmo
            algorithm = chose_algorithm(estimator)
            # Empieza el algoritmo
            estimated_parameters = algorithm(parametros_list,df_Stays,STAYS_PROBABILITY_DISTRIBUTION)
            
            # Se añaden los parámetros a la lista correspondiente
            dictionary_estimated_parameters[estimator][KEY_DAILY_ROW_LIST].append(estimated_parameters)
        
        
    for estimator in ESTIMATOR_LIST:
        df_Parameters = pd.DataFrame(dictionary_estimated_parameters[estimator][KEY_DAILY_ROW_LIST], columns=(COLUMN_DAY,COLUMN_P_WI,COLUMN_DISTRIBUTION_X,COLUMN_A_X,COLUMN_B_X,COLUMN_C_X,COLUMN_DISTRIBUTION_Z,COLUMN_A_Z,COLUMN_B_Z,COLUMN_C_Z,COLUMN_ISE_Z))  
        df_Parameters.to_excel(writer_Parameter_Estimation, sheet_name=estimator, index=False)
    
    
    
    # Close the Pandas Excel writer and output the Excel file.
    writer_Parameter_Estimation.save()
    
end_DT = datetime.now()
print ('Finalización programa: '+str(end_DT))


diff = end_DT - start_DT

days = diff.days
seconds = diff.seconds
hours = days * 24 + seconds // 3600
minutes = (seconds % 3600) // 60
seconds = seconds % 60

tiempo_resolucion = str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s"

print(tiempo_resolucion)