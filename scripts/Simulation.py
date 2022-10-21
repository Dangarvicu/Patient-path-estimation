# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 16:51:26 2021

@author: daniel
"""

from config.config import *
from functions.functions import *



# Se repite el algoritmo varias veces
    
# En cada iteración se recorren todos los días.

#range(HORIZON_VISUALIZATION)
for dia_simulacion in SIMULATION_DAYS_LIST:
    print('*******')
    print(dia_simulacion)
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer_resultado_simulacion = pd.ExcelWriter(f'{EXCEL_RESULTS_ROUTE}{ICU_SIMULATION_RESULTS_EXCEL} day {dia_simulacion}_TEST.xlsx',engine='xlsxwriter')
    
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
                                                                                      SIMULATION)
    
    
    # Semilla de la simulación
    rnd.seed(RANDOM_SEED)
    # Crear listas para asegurar los mismos números aleatorios en los mismos eventos
    lista_random_pacientes_coronavirus = []
    contador_random_pacientes_coronavirus = 0
    lista_random_curvas_gompertz = []
    contador_random_curvas_gompertz = 0
    lista_random_pacientes_P_I = []
    contador_random_pacientes_P_I = 0
    lista_random_pacientes_P_WI = []
    contador_random_pacientes_P_WI = 0
    lista_random_pacientes_P_IW = []
    contador_random_pacientes_P_IW = 0
    lista_random_sorteo_entrada_coronavirus = []
    contador_random_sorteo_entrada_coronavirus = 0
    lista_random_estancia_X = []
    contador_random_estancia_X = 0
    lista_random_estancia_Y = []
    contador_random_estancia_Y = 0
    lista_random_estancia_Z = []
    contador_random_estancia_Z = 0
    lista_random_estancia_Q = []
    contador_random_estancia_Q = 0
    
       
    
    for i in range(RANDOM_LSIT_SIZE):
        r = rnd.random()
        lista_random_pacientes_coronavirus.append(r)
        r = rnd.random()
        lista_random_curvas_gompertz.append(r)
        r = rnd.random()
        lista_random_pacientes_P_I.append(r)
        r = rnd.random()
        lista_random_pacientes_P_WI.append(r)
        r = rnd.random()
        lista_random_pacientes_P_IW.append(r)
        r = rnd.random()
        lista_random_sorteo_entrada_coronavirus.append(r)
        r = rnd.random()
        lista_random_estancia_X.append(r)
        r = rnd.random()
        lista_random_estancia_Y.append(r)
        r = rnd.random()
        lista_random_estancia_Z.append(r)
        r = rnd.random()
        lista_random_estancia_Q.append(r)
    
    
    
    # Simulación de llegadas y estancias
    rows_list_simulated,contador_random_pacientes_P_I,contador_random_sorteo_entrada_coronavirus,contador_random_pacientes_P_IW,contador_random_pacientes_P_WI,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = simulate_stays_and_pathway(y_new_cases_Poisson,lista_random_pacientes_P_I,contador_random_pacientes_P_I,lista_random_sorteo_entrada_coronavirus,contador_random_sorteo_entrada_coronavirus,lista_random_pacientes_P_IW,contador_random_pacientes_P_IW,lista_random_pacientes_P_WI,contador_random_pacientes_P_WI,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                  
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    save_file_stays_and_arrivals(f'{EXCEL_DATA_ROUTE}{PARAMETER_SIMULATION_EXCEL}.xlsx',
                                 rows_list_simulated,
                                 x_personalized,
                                 y_personalized,
                                 y_new_cases_Poisson)
        
    
    
    
    
    
    
    #Primero se generan los diccionarios donde se van a guardar los datos.
    dictionary_estimated_parameters = {}
    for estimator in ESTIMATOR_LIST:
        dictionary_estimated_parameters[estimator] = {}
        dictionary_estimated_parameters[estimator][KEY_DAILY_ROW_LIST] = []
    
    
    
       
    
    df_Stays = generate_data_frame_stays_in_day_d(rows_list_simulated,dia_simulacion)
        
         
        
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
        

    
    
    




    lista_estimadores = ESTIMATOR_LIST + [R]
    
    # Se puede seleccionar menos estimadores de forma manual:
    # =============================================================================
    # lista_estimadores = [ESTIMATOR_CI,
    #                      ESTIMATOR_I,
    #                      ESTIMATOR_IQ2,
    #                      ESTIMATOR_IQ3,
    #                      ESTIMATOR_EM_WEIBULL,
    #                      ESTIMATOR_NP,
    #                      ESTIMATOR_EMNP
    #                      ]
    # =============================================================================
    
    
    distribution_stays = STAYS_PROBABILITY_DISTRIBUTION
    for estimator in lista_estimadores:
        print(estimator)
        
        if estimator == R:
            # Valores originales.
            p_WI = P_WI
            parameter_a_Z = PARAMETER_a_Z
            parameter_b_Z = PARAMETER_b_Z
            parameter_c_Z = PARAMETER_c_Z
        else:
            # Valores estimados.
            p_WI = dictionary_estimated_parameters[estimator][KEY_DAILY_ROW_LIST][0][POSITION_P_WI]
            parameter_a_Z = dictionary_estimated_parameters[estimator][KEY_DAILY_ROW_LIST][0][POSITION_A_Z]
            parameter_b_Z = dictionary_estimated_parameters[estimator][KEY_DAILY_ROW_LIST][0][POSITION_B_Z]
            parameter_c_Z = dictionary_estimated_parameters[estimator][KEY_DAILY_ROW_LIST][0][POSITION_C_Z]
            
    
    
    
        # Valores originales.
        parameter_a_X = PARAMETER_a_X
        parameter_b_X = PARAMETER_b_X
        parameter_c_X = PARAMETER_c_X
        parameter_a_Y = PARAMETER_a_Y
        parameter_b_Y = PARAMETER_b_Y
        parameter_c_Y = PARAMETER_c_Y
        parameter_a_Q = PARAMETER_a_Q
        parameter_b_Q = PARAMETER_b_Q
        parameter_c_Q = PARAMETER_c_Q
        # Porcentajes
        p_I = P_I
        p_IW = P_IW        
            
    
        # Preparación de los datos
        
        # Esta ocupación inicial, es por si se comienza sin datos y se quiere introducir una ocupación inicial manualmente.
        ocupacion_inicial = 0
            
                  
    #######################################################################################################
    
# =============================================================================
#         print(estimator)
#         print(f'Real p_WI: {P_WI} -> {p_WI}')
#         print(f'Real a_Z: {PARAMETER_a_Z} -> {parameter_a_Z}')
#         print(f'Real b_Z: {PARAMETER_b_Z} -> {parameter_b_Z}')
#         print(f'Real c_Z: {PARAMETER_c_Z} -> {parameter_c_Z}')
# =============================================================================
        
        
        
        
        lista_casos_diarios_por_replicacion = []
    
    
        global lista_pacientes_ingresados_agregado_por_replicacion
        global lista_pacientes_ingresados_hospital_por_replicacion
        global lista_pacientes_ingresados_UCI_por_replicacion
    
        lista_pacientes_ingresados_agregado_por_replicacion = []
        lista_pacientes_ingresados_hospital_por_replicacion = []
        lista_pacientes_ingresados_UCI0_por_replicacion = []
        lista_pacientes_ingresados_P_UCI_por_replicacion = []
        lista_pacientes_ingresados_UCI_por_replicacion = []
    
    
        lista_altas_agregado_por_replicacion = []
        lista_altas_hospital_por_replicacion = []
        lista_altas_UCI0_por_replicacion = []
        lista_altas_P_UCI_por_replicacion = []
        lista_altas_UCI_por_replicacion = []
    
    
        global lista_ocupaciones_agregado_por_replicacion
        global lista_ocupaciones_hospital_por_replicacion
        global lista_ocupaciones_UCI_por_replicacion
    
        lista_ocupaciones_agregado_por_replicacion = []
        lista_ocupaciones_hospital_por_replicacion = []
        lista_ocupaciones_UCI_por_replicacion = []
    
    
        # Comienza el bucle de las replicaciones
        for replicacion in range(SIMULATION_REPLICACTIONS):
            print(replicacion)
            #print("#1")
            
            # Lista donde se va a guardar los tiempos de entrada y salida de cada paciente.
            rows_list_Ingresos_Conocidos = []
            
            
            global contador_dias_ingreso
            contador_dias_ingreso = 0
            # Se pone para luego saber a partir de qué día se le debe asignar tiempos de estancia a los pacientes de coronavirus.
            
                    
            
        # =============================================================================
        #     # Se introducen las variables de las ocupaciones iniciales.
        #     ocupacion_hospital_inicial = 0
        #     ocupacion_UCI_inicial = 0    
        # =============================================================================
                   
            # Se recorre todo el archivo, asignando a cada paciente los tiempos que les corresponden.
            for i in range(len(df_Stays)):
                # Se calculan todos los tiempos y después se comprueba si quedan fuera de la ventana de simulación o dentro.
                # Para calcular los tiempos de un paciente hay que obtener el recorrido del paciente.
                # Habrá que ver si el paciente va a UCI o no y después cómo sale de la UCI, si a planta o fallecido.
                        
                if df_Stays.loc[i, 'LOS_H'] > 0:
                    # PACIENTES CON LOS_H > 0 (ESTANCIA HOSPITAL)
                    if df_Stays.loc[i, 'Cens_H'] == 0:
                        # Paciente que solo está en el hospital. Ya tiene completada su estancia.
                        tipo_estancia = 'LOS_H'
                        recorrido = 'Casa_P'
                        ingreso = df_Stays.loc[i, 'date_HA']
                        salida = df_Stays.loc[i, 'date_HD']
                        if ingreso > 0:
                            rows_list_Ingresos_Conocidos.append([ingreso,0,tipo_estancia,recorrido])
                        if salida > 0:
                            recorrido = 'P_Casa'
                            rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])                
                    else:
                        # Paciente que sigue en el hospital y puede ir a la UCI.
                        estancia_previa = df_Stays.loc[i, 'LOS_H']
                        
                        if estimator == ESTIMATOR_NP:
                            # Me quedo sólo con los registros de tiempo de estancia en H y P_UCI >= estancia_previa
                            df_Estancias_Condicionadas = df_Stays[(df_Stays['LOS_H'] >= estancia_previa) | (df_Stays['LOS_P_UCI'] >= estancia_previa)]
                            p_WI_conditioned,mean_stay_ward_ICU,lista_tiempos_ordenados,vector_S0,vector_w = get_p_WI_sorted_times_and_weights_algorithm_NP(df_Estancias_Condicionadas)
                            limite_para_considerar_traslado_UCI = p_WI_conditioned
                        else:
                            p_W = 0
                            if distribution_stays == WEIBULL:
                                p_W = 1 - weibull_min.cdf(estancia_previa,parameter_a_Z,loc=0,scale=parameter_b_Z)
                            elif distribution_stays == LOGNORMAL:
                                p_W = 1 - lognorm.cdf(estancia_previa,parameter_b_Z,loc=0,scale=np.exp(parameter_a_Z))
                            elif distribution_stays == TRIANGULAR:
                                c_T = (parameter_b_Z - parameter_a_Z) / (parameter_c_Z - parameter_a_Z)
                                loc_T = parameter_a_Z
                                scale_T = parameter_c_Z - parameter_a_Z
                                p_W = 1 - triang.cdf(estancia_previa, c_T, loc=loc_T, scale=scale_T)
                                
                            p_X = 0
                            if distribution_stays == WEIBULL:
                                p_X = 1 - weibull_min.cdf(estancia_previa,parameter_a_X,loc=0,scale=parameter_b_X)
                            elif distribution_stays == LOGNORMAL:
                                p_X = 1 - lognorm.cdf(estancia_previa,parameter_b_X,loc=0,scale=np.exp(parameter_a_X))
                            
                            if (p_W*p_WI+p_X*(1-p_WI)) > 0:
                                limite_para_considerar_traslado_UCI = p_W*p_WI/(p_W*p_WI+p_X*(1-p_WI)) #  Ecuación 10 del artículo de la CJOR.
                            else:
                                limite_para_considerar_traslado_UCI = 0
                        
                        
                        
                        
                        
                        r = lista_random_pacientes_P_I[contador_random_pacientes_P_I]
                        contador_random_pacientes_P_I = contador_random_pacientes_P_I + 1
                        if contador_random_pacientes_P_I == RANDOM_LSIT_SIZE:
                            contador_random_pacientes_P_I = 0                       
                        
                        if r < limite_para_considerar_traslado_UCI:
                            # Este paciente va a la UCI.
                            # Se le calcula el tiempo que le falta para ingresar.
                            tipo_estancia = 'LOS_P_UCI'
                            recorrido = 'Casa_P'
                            ingreso = df_Stays.loc[i, 'date_HA']
                            if estimator == ESTIMATOR_NP:
                                estancia,contador_random_estancia_Z = generate_stay_with_estimation_NP(lista_tiempos_ordenados,vector_w,lista_random_estancia_Z,contador_random_estancia_Z)                            
                            else:
                                estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parameter_a_Z,parameter_b_Z,parameter_c_Z,STAYS_PROBABILITY_DISTRIBUTION,estancia_previa,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                            salida = ingreso + estancia
                                                
                            if ingreso > 0:
                                rows_list_Ingresos_Conocidos.append([ingreso,0,tipo_estancia,recorrido])
                            if salida > 0:
                                recorrido = 'P_UCI'
                                rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])
                                
                               
                            # Ahora este paciente hay que calcularle la estancia en UCI
                            tipo_estancia = 'LOS_UCI'
                            recorrido = 'P_UCI'
                            ingreso = salida
                            estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parameter_a_Y,parameter_b_Y,parameter_c_Y,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                            salida = ingreso + estancia
                            rows_list_Ingresos_Conocidos.append([ingreso,0,tipo_estancia,recorrido])
                            
                                                            
                            # Ahora se calcula si el paciente va de la UCI a planta.
                            r = lista_random_pacientes_P_IW[contador_random_pacientes_P_IW]
                            contador_random_pacientes_P_IW = contador_random_pacientes_P_IW + 1
                            if contador_random_pacientes_P_IW == RANDOM_LSIT_SIZE:
                                contador_random_pacientes_P_IW = 0
                            if r < p_IW:
                                # El paciente va a planta.
                                recorrido = 'UCI_P'
                                rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])
                                # Se le genera un tiempo de estancia.
                                tipo_estancia = 'LOS_UCI_P'
                                recorrido = 'UCI_P'
                                ingreso = salida
                                estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parameter_a_Q,parameter_b_Q,parameter_c_Q,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                                salida = ingreso + estancia
                                rows_list_Ingresos_Conocidos.append([ingreso,0,tipo_estancia,recorrido])
                                recorrido = 'P_Casa'
                                rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])
                                
                            else:
                                # El paciente sale del hospital.
                                recorrido = 'UCI_Casa'
                                rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])
                                
                            
                            
                        else:
                            # Pacientes que siguen en el hospital pero que no han sido dados de alta.
                            tipo_estancia = 'LOS_H'
                            recorrido = 'Casa_P'
                            ingreso = df_Stays.loc[i, 'date_HA']
                            estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parameter_a_X,parameter_b_X,parameter_c_X,STAYS_PROBABILITY_DISTRIBUTION,estancia_previa,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                            salida = ingreso + estancia
                            if ingreso > 0:
                                rows_list_Ingresos_Conocidos.append([ingreso,0,tipo_estancia,recorrido])
                            if salida > 0:
                                recorrido = 'P_Casa'
                                rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])
                                
                                                    
                else:
                    # En esta parte entran los pacientes que van a la UCI.
                    if df_Stays.loc[i, 'LOS_P_UCI'] > 0:
                        # PACIENTES CON LOS_P_UCI > 0 (ESTANCIA HOSPITAL ANTES DE UCI)
                        # Paciente que está en el hospital antes de UCI que ya es conocido. Ya tiene completada su estancia.
                        tipo_estancia = 'LOS_P_UCI'
                        recorrido = 'Casa_P'
                        ingreso = df_Stays.loc[i, 'date_HA']
                        salida = df_Stays.loc[i, 'date_IA']
                        if ingreso > 0:
                            rows_list_Ingresos_Conocidos.append([ingreso,0,tipo_estancia,recorrido])
                        if salida > 0:
                            recorrido = 'P_UCI'
                            rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])
                        
                    # PACIENTES CON LOS_UCI > 0 (ESTANCIA EN UCI)
                    tipo_estancia = 'LOS_UCI'
                    # Para diferenciar la forma de ingreso en UCI
                    if df_Stays.loc[i, 'LOS_P_UCI'] > 0:
                        recorrido = 'P_UCI'
                    else:
                        recorrido = 'Casa_UCI'
                    
                    # Se introduce la fecha de entrada en UCI
                    ingreso = df_Stays.loc[i, 'date_IA']
                    if df_Stays.loc[i, 'Cens_UCI'] == 0:
                        # PACIENTES CON ESTANCIA TERMINADA EN UCI
                        salida = df_Stays.loc[i, 'date_ID']                
                        if ingreso > 0:
                            rows_list_Ingresos_Conocidos.append([ingreso,0,tipo_estancia,recorrido])
                                        
                        # Se comprueba si tiene estancia de LOS_UCI_P
                        if df_Stays.loc[i, 'LOS_UCI_P'] > 0:
                            # PACIENTES CON LOS_UCI_P > 0 (ESTANCIA EN PLANTA POSTERIOR A UCI)
                            if salida > 0:
                                recorrido = 'UCI_P'
                                rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])
                            tipo_estancia = 'LOS_UCI_P'
                            recorrido = 'UCI_P'
                            ingreso = df_Stays.loc[i, 'date_ID']
                            if df_Stays.loc[i, 'Cens_H'] == 0:
                                # Pacientes con toda la estancia terminada
                                salida = df_Stays.loc[i, 'date_HD']
                                if ingreso > 0:
                                    rows_list_Ingresos_Conocidos.append([ingreso,0,tipo_estancia,recorrido])
                                if salida > 0:
                                    recorrido = 'P_Casa'
                                    rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])
                                
                            else:
                                # Pacientes que siguen en el hospital después de salir de la UCI
                                estancia_previa = df_Stays.loc[i, 'LOS_UCI_P']
                                recorrido = 'UCI_P'
                                estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parameter_a_Q,parameter_b_Q,parameter_c_Q,STAYS_PROBABILITY_DISTRIBUTION,estancia_previa,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                                salida = ingreso + estancia
                                if ingreso > 0:
                                    rows_list_Ingresos_Conocidos.append([ingreso,0,tipo_estancia,recorrido])
                                if salida > 0:
                                    recorrido = 'P_Casa'
                                    rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])
                                
                        else:
                            # Paciente de UCI que no pasa por planta.
                            if salida > 0:
                                recorrido = 'UCI_Casa'
                                rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])
                                
                    
                    else:
                        # PACIENTES QUE SIGUEN EN LA UCI
                        estancia_previa = df_Stays.loc[i, 'LOS_UCI']
                        estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parameter_a_Y,parameter_b_Y,parameter_c_Y,STAYS_PROBABILITY_DISTRIBUTION,estancia_previa,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                        salida = ingreso + estancia
                        if ingreso > 0:
                            rows_list_Ingresos_Conocidos.append([ingreso,0,tipo_estancia,recorrido])
                        
                        # Ahora se calcula si el paciente va de la UCI a planta.
                        r = lista_random_pacientes_P_IW[contador_random_pacientes_P_IW]
                        contador_random_pacientes_P_IW = contador_random_pacientes_P_IW + 1
                        if contador_random_pacientes_P_IW == RANDOM_LSIT_SIZE:
                            contador_random_pacientes_P_IW = 0
                        if r < p_IW:
                            # El paciente va a planta.
                            if salida > 0:
                                recorrido = 'UCI_P'
                                rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])
                                   
                            
                            # Se le genera un tiempo de estancia.
                            tipo_estancia = 'LOS_UCI_P'
                            recorrido = 'UCI_P'
                            ingreso = salida
                            estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parameter_a_Q,parameter_b_Q,parameter_c_Q,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                            salida = ingreso + estancia
                            rows_list_Ingresos_Conocidos.append([ingreso,0,tipo_estancia,recorrido])
                            recorrido = 'P_Casa'
                            rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])
                            
                        else:
                            # El paciente no va a planta desde UCI.
                            if salida > 0:
                                recorrido = 'UCI_Casa'
                                rows_list_Ingresos_Conocidos.append([salida,1,tipo_estancia,recorrido])  
                                
                        
                    
            #print("#2")
            
            #######################################################################################
            # Para no simular llegadas los primeros días
            contador_dias_ingreso = dia_simulacion
            
        # =============================================================================
        #         # Se actualiza el día de comienzo
        #         contador_dias_paralelo = día_Comienzo_Simulacion_Numero
        # =============================================================================
            
            # Se añaden listas vacías para los contadores.
        # =============================================================================
        #         lista_casos_diarios_por_replicacion.append([])         
        # =============================================================================
        
        
            lista_pacientes_ingresados_agregado_por_replicacion.append([])
            lista_pacientes_ingresados_hospital_por_replicacion.append([])
            lista_pacientes_ingresados_UCI0_por_replicacion.append([])
            lista_pacientes_ingresados_P_UCI_por_replicacion.append([])
            lista_pacientes_ingresados_UCI_por_replicacion.append([])
                    
            lista_altas_agregado_por_replicacion.append([])
            lista_altas_hospital_por_replicacion.append([])
            lista_altas_UCI0_por_replicacion.append([])
            lista_altas_P_UCI_por_replicacion.append([])
            lista_altas_UCI_por_replicacion.append([])
                    
            lista_ocupaciones_agregado_por_replicacion.append([])
            lista_ocupaciones_hospital_por_replicacion.append([])
            lista_ocupaciones_UCI_por_replicacion.append([])
            
           
            
            lista_casos_diarios_por_replicacion.append(y_new_cases_Poisson)
            
                    
            
            #df_Tiempos = pd.DataFrame(columns=('Tiempo','Estado', 'Tipo'))
            # El Tipo servirá para distinguir urgentes(0), programados(1), coronavirus(19), iniciales(10)
            # Se crea una lista de listas que luego se convertirá en DataFrame
            rows_list = rows_list_Ingresos_Conocidos[:]
            
            #print("#3")
            
            # Se registran los vectores para la simulación con el método NP.
            p_WI_conditioned,mean_stay_ward_ICU,lista_tiempos_ordenados,vector_S0,vector_w = get_p_WI_sorted_times_and_weights_algorithm_NP(df_Stays)
                    
            for dia in range(HORIZON_VISUALIZATION):
                # Esto se añade para registrar el cambio de día en la simulación.
                # Los 8 se añaden para completar los campos necesarios (entrada(0)/salida(1),tipo)
                rows_list.append([dia+1,8,8,8])
            
                
                ###################### PACIENTES CORONAVIRUS ############################
                if dia >= contador_dias_ingreso:
                    for paciente_Potencial in range(y_new_cases_Poisson[dia]):
                        # Paciente que ingresa en el hospital
                        # Se sortea si el paciente ingresa en el hospital o en la UCI directamente
                        r = lista_random_pacientes_P_I[contador_random_pacientes_P_I]
                        contador_random_pacientes_P_I = contador_random_pacientes_P_I + 1
                        if contador_random_pacientes_P_I == RANDOM_LSIT_SIZE:
                            contador_random_pacientes_P_I = 0
                        if r < p_I:
                            # El paciente ingresa en la UCI directamente.
                            # Ahora a este paciente hay que calcularle la estancia en UCI
                            tipo_estancia = 'LOS_UCI'
                            recorrido = 'Casa_UCI'
                            r = lista_random_pacientes_coronavirus[contador_random_pacientes_coronavirus]
                            contador_random_pacientes_coronavirus = contador_random_pacientes_coronavirus + 1
                            if contador_random_pacientes_coronavirus == RANDOM_LSIT_SIZE:
                                contador_random_pacientes_coronavirus = 0
                            ingreso = dia + r
                            estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parameter_a_Y,parameter_b_Y,parameter_c_Y,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                            salida = ingreso + estancia
                            rows_list.append([ingreso,0,tipo_estancia,recorrido])                          
                            
                            
                            
                            # Ahora se calcula si el paciente va de la UCI a planta.
                            r = lista_random_pacientes_P_IW[contador_random_pacientes_P_IW]
                            contador_random_pacientes_P_IW = contador_random_pacientes_P_IW + 1
                            if contador_random_pacientes_P_IW == RANDOM_LSIT_SIZE:
                                contador_random_pacientes_P_IW = 0
                            if r < p_IW:
                                # El paciente va a planta.
                                recorrido = 'UCI_P'
                                rows_list.append([salida,1,tipo_estancia,recorrido])
                                
                                
                                # Se le genera un tiempo de estancia.
                                tipo_estancia = 'LOS_UCI_P'
                                recorrido = 'UCI_P'
                                r = lista_random_pacientes_coronavirus[contador_random_pacientes_coronavirus]
                                contador_random_pacientes_coronavirus = contador_random_pacientes_coronavirus + 1
                                if contador_random_pacientes_coronavirus == RANDOM_LSIT_SIZE:
                                    contador_random_pacientes_coronavirus = 0
                                ingreso = salida + r
                                estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parameter_a_Q,parameter_b_Q,parameter_c_Q,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                                salida = ingreso + estancia
                                rows_list.append([ingreso,0,tipo_estancia,recorrido])
                                recorrido = 'P_Casa'
                                rows_list.append([salida,1,tipo_estancia,recorrido])
                                
                            
                            else:
                                # El paciente sale de la UCI directamente.
                                recorrido = 'UCI_Casa'
                                rows_list.append([salida,1,tipo_estancia,recorrido])
                                
                        else:
                            # El paciente ingresa en el hospital.
                            # Ahora se calcula si el paciente va de la planta a la UCI.
                            r = lista_random_pacientes_P_WI[contador_random_pacientes_P_WI]
                            contador_random_pacientes_P_WI = contador_random_pacientes_P_WI + 1
                            if contador_random_pacientes_P_WI == RANDOM_LSIT_SIZE:
                                contador_random_pacientes_P_WI = 0
                            if r < p_WI:
                                # El paciente va a la UCI desde planta.                                
                                # Ahora a este paciente hay que calcularle la estancia en planta hasta UCI
                                tipo_estancia = 'LOS_P_UCI'
                                recorrido = 'Casa_P'
                                r = lista_random_pacientes_coronavirus[contador_random_pacientes_coronavirus]
                                contador_random_pacientes_coronavirus = contador_random_pacientes_coronavirus + 1
                                if contador_random_pacientes_coronavirus == RANDOM_LSIT_SIZE:
                                    contador_random_pacientes_coronavirus = 0
                                ingreso = dia + r
                                if estimator == ESTIMATOR_NP:                                
                                    estancia,contador_random_estancia_Z = generate_stay_with_estimation_NP(lista_tiempos_ordenados,vector_w,lista_random_estancia_Z,contador_random_estancia_Z)                            
                                else:
                                    estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parameter_a_Z,parameter_b_Z,parameter_c_Z,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                                salida = ingreso + estancia
                                rows_list.append([ingreso,0,tipo_estancia,recorrido])
                                recorrido = 'P_UCI'
                                rows_list.append([salida,1,tipo_estancia,recorrido])
                                                               
                                
                                # Ahora este paciente hay que calcularle la estancia en UCI
                                tipo_estancia = 'LOS_UCI'
                                recorrido = 'P_UCI'
                                ingreso = salida
                                estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parameter_a_Y,parameter_b_Y,parameter_c_Y,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                                salida = ingreso + estancia
                                rows_list.append([ingreso,0,tipo_estancia,recorrido])
                                                                                             
                                                             
                                # Ahora se calcula si el paciente va de la UCI a planta.
                                r = lista_random_pacientes_P_IW[contador_random_pacientes_P_IW]
                                contador_random_pacientes_P_IW = contador_random_pacientes_P_IW + 1
                                if contador_random_pacientes_P_IW == RANDOM_LSIT_SIZE:
                                    contador_random_pacientes_P_IW = 0
                                if r < p_IW:
                                    # El paciente va a planta.
                                    recorrido = 'UCI_P'
                                    rows_list.append([salida,1,tipo_estancia,recorrido]) 
                                    # Se le genera un tiempo de estancia.
                                    tipo_estancia = 'LOS_UCI_P'
                                    recorrido = 'UCI_P'
                                    ingreso = salida
                                    estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parameter_a_Q,parameter_b_Q,parameter_c_Q,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                                    salida = ingreso + estancia
                                    rows_list.append([ingreso,0,tipo_estancia,recorrido])
                                    recorrido = 'P_Casa'
                                    rows_list.append([salida,1,tipo_estancia,recorrido])
                                    
                                else:
                                    # El paciente no sale de la UCI a planta.
                                    recorrido = 'UCI_Casa'
                                    rows_list.append([salida,1,tipo_estancia,recorrido]) 
                                   
                            else:
                                # El paciente se queda en planta todo el tiempo.
                                # Ahora a este paciente hay que calcularle la estancia en planta.
                                tipo_estancia = 'LOS_H'
                                recorrido = 'Casa_P'
                                r = lista_random_pacientes_coronavirus[contador_random_pacientes_coronavirus]
                                contador_random_pacientes_coronavirus = contador_random_pacientes_coronavirus + 1
                                if contador_random_pacientes_coronavirus == RANDOM_LSIT_SIZE:
                                    contador_random_pacientes_coronavirus = 0
                                ingreso = dia + r
                                estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parameter_a_X,parameter_b_X,parameter_c_X,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                                salida = ingreso + estancia
                                rows_list.append([ingreso,0,tipo_estancia,recorrido])
                                recorrido = 'P_Casa'
                                rows_list.append([salida,1,tipo_estancia,recorrido])
        
            df_Tiempos = pd.DataFrame(rows_list, columns=('Tiempo','Estado','Tipo de estancia','Recorrido'))  
                
            # Se ordena el datFrame en base a la columna Tiempo. Y se sobreescribe.
            df_Tiempos = df_Tiempos.sort_values('Tiempo')
            
            #print("#4")
            # Se contabiliza la ocupación consecutivamente.
            # Se crea un nuevo dataFrame
            #df_Ocupaciones = pd.DataFrame(columns=('Tiempo','Ocupación'))
            # Se crean los contadores de los indicadores.
            contador_pacientes_ingresados_agregado = 0
            contador_pacientes_ingresados_hospital = 0
            contador_pacientes_ingresados_UCI0 = 0
            contador_pacientes_ingresados_P_UCI = 0
            contador_pacientes_ingresados_UCI = 0
            
            contador_altas_agregado = 0
            contador_altas_hospital = 0
            contador_altas_UCI0 = 0
            contador_altas_P_UCI = 0
            contador_altas_UCI = 0
            
            
            ocupaciones_agregado = 0
            ocupaciones_hospital = 0
            ocupaciones_UCI = 0
            
            
            
            tiempo_anterior = 0
            tiempo_actual = 0
            
            
            #########################################################################
                
            # Simulación en cada replicación
            
            for tiempo,estado,tipo_estancia,recorrido in zip(df_Tiempos['Tiempo'],df_Tiempos['Estado'],df_Tiempos['Tipo de estancia'],df_Tiempos['Recorrido']):
                if estado == 8:
                    # Contadores ingresos
                    contador_pacientes_ingresados_agregado = contador_pacientes_ingresados_hospital + contador_pacientes_ingresados_UCI0
                    contador_pacientes_ingresados_UCI = contador_pacientes_ingresados_UCI0 + contador_pacientes_ingresados_P_UCI
                    
                    # Contadores altas
                    contador_altas_agregado = contador_altas_hospital + contador_altas_UCI0
                    contador_altas_UCI = contador_altas_UCI0 + contador_altas_P_UCI
                    
                    # Ocupaciones
                    ocupaciones_agregado = ocupaciones_hospital + ocupaciones_UCI
                    
                    
                    
                    
                    lista_pacientes_ingresados_agregado_por_replicacion[replicacion].append([contador_pacientes_ingresados_agregado])
                    lista_pacientes_ingresados_hospital_por_replicacion[replicacion].append([contador_pacientes_ingresados_hospital])
                    lista_pacientes_ingresados_UCI0_por_replicacion[replicacion].append([contador_pacientes_ingresados_UCI0])
                    lista_pacientes_ingresados_P_UCI_por_replicacion[replicacion].append([contador_pacientes_ingresados_P_UCI])
                    lista_pacientes_ingresados_UCI_por_replicacion[replicacion].append([contador_pacientes_ingresados_UCI])
                            
                    lista_altas_agregado_por_replicacion[replicacion].append([contador_altas_agregado])
                    lista_altas_hospital_por_replicacion[replicacion].append([contador_altas_hospital])
                    lista_altas_UCI0_por_replicacion[replicacion].append([contador_altas_UCI0])
                    lista_altas_P_UCI_por_replicacion[replicacion].append([contador_altas_P_UCI])
                    lista_altas_UCI_por_replicacion[replicacion].append([contador_altas_UCI])
                            
                    lista_ocupaciones_agregado_por_replicacion[replicacion].append([ocupaciones_agregado])
                    lista_ocupaciones_hospital_por_replicacion[replicacion].append([ocupaciones_hospital])
                    lista_ocupaciones_UCI_por_replicacion[replicacion].append([ocupaciones_UCI])
                    
                    
                                  
                    
                    # Se resetean los contadores diarios
                    contador_pacientes_ingresados_hospital = 0
                    contador_pacientes_ingresados_UCI0 = 0
                    contador_pacientes_ingresados_P_UCI = 0
                    
                    contador_altas_hospital = 0
                    contador_altas_UCI0 = 0
                    contador_altas_P_UCI = 0
                else:            
                    if tiempo < HORIZON_VISUALIZATION:
                        # Se actualiza la ocupación
                        if estado == 0:
                            # Ingreso de un paciente.
                            if recorrido == 'Casa_P':
                                ocupaciones_hospital = ocupaciones_hospital + 1
                                contador_pacientes_ingresados_hospital = contador_pacientes_ingresados_hospital + 1
                                    
                            elif recorrido == 'Casa_UCI':
                                ocupaciones_UCI = ocupaciones_UCI + 1
                                contador_pacientes_ingresados_UCI0 = contador_pacientes_ingresados_UCI0 + 1
                            
                            elif recorrido == 'P_UCI':
                                ocupaciones_UCI = ocupaciones_UCI + 1
                                contador_pacientes_ingresados_P_UCI = contador_pacientes_ingresados_P_UCI + 1
                            
                            elif recorrido == 'UCI_P':
                                ocupaciones_hospital = ocupaciones_hospital + 1
                                    
                         
                        elif estado == 1:
                            # Salida de un paciente.
                            if recorrido == 'P_Casa':
                                ocupaciones_hospital = ocupaciones_hospital - 1
                                contador_altas_hospital = contador_altas_hospital + 1
                                    
                            elif recorrido == 'UCI_Casa':
                                ocupaciones_UCI = ocupaciones_UCI - 1
                                contador_altas_UCI0 = contador_altas_UCI0 + 1
                            
                            elif recorrido == 'UCI_P':
                                ocupaciones_UCI = ocupaciones_UCI - 1
                                contador_altas_P_UCI = contador_altas_P_UCI + 1
                            
                            elif recorrido == 'P_UCI':
                                ocupaciones_hospital = ocupaciones_hospital - 1
                                    
        
                            
                        
                        tiempo_actual = tiempo
                        
                        # Se almacena la ocupación en el tiempo actual.
                        #df_Ocupaciones.loc[len(df_Ocupaciones)]=[tiempo_actual,ocupacion]
                        
                        
        # =============================================================================
        #                 # Se actualizan los tiempos de ocupación de cada estado.
        #                 tiempos_ocupacion[ocupacion] = tiempos_ocupacion[ocupacion] + (tiempo_actual - tiempo_anterior)
        #                 
        # =============================================================================
                        
                        # Se actualiza el tiempo anterior
                        tiempo_anterior = tiempo
        
        
      
    
    
    
        #################
        
        
        lista_fechas = x_personalized
        
        lista_casos_diarios_por_dia = []
        
        lista_pacientes_ingresados_agregado_por_dia = []
        lista_pacientes_ingresados_hospital_por_dia = []
        lista_pacientes_ingresados_UCI0_por_dia = []
        lista_pacientes_ingresados_P_UCI_por_dia = []
        lista_pacientes_ingresados_UCI_por_dia = []
        
        
        lista_altas_agregado_por_dia = []
        lista_altas_hospital_por_dia = []
        lista_altas_UCI0_por_dia = []
        lista_altas_P_UCI_por_dia = []
        lista_altas_UCI_por_dia = []
        
        
        global lista_ocupaciones_hospital_por_dia
        global lista_ocupaciones_UCI_por_dia
        lista_ocupaciones_agregado_por_dia = []
        lista_ocupaciones_hospital_por_dia = []
        lista_ocupaciones_UCI_por_dia = []
        
        
        
        for j in range(HORIZON_VISUALIZATION):
            lista_casos_diarios_por_dia.append([])
            
            lista_pacientes_ingresados_agregado_por_dia.append([])
            lista_pacientes_ingresados_hospital_por_dia.append([])
            lista_pacientes_ingresados_UCI0_por_dia.append([])
            lista_pacientes_ingresados_P_UCI_por_dia.append([])
            lista_pacientes_ingresados_UCI_por_dia.append([])
                    
            lista_altas_agregado_por_dia.append([])
            lista_altas_hospital_por_dia.append([])
            lista_altas_UCI0_por_dia.append([])
            lista_altas_P_UCI_por_dia.append([])
            lista_altas_UCI_por_dia.append([])
                    
            lista_ocupaciones_agregado_por_dia.append([])
            lista_ocupaciones_hospital_por_dia.append([])
            lista_ocupaciones_UCI_por_dia.append([])
            
        
            
            for i in range(SIMULATION_REPLICACTIONS):
                lista_casos_diarios_por_dia[j].append(lista_casos_diarios_por_replicacion[i][j])
                
                lista_pacientes_ingresados_agregado_por_dia[j].append(lista_pacientes_ingresados_agregado_por_replicacion[i][j])
                lista_pacientes_ingresados_hospital_por_dia[j].append(lista_pacientes_ingresados_hospital_por_replicacion[i][j])
                lista_pacientes_ingresados_UCI0_por_dia[j].append(lista_pacientes_ingresados_UCI0_por_replicacion[i][j])
                lista_pacientes_ingresados_P_UCI_por_dia[j].append(lista_pacientes_ingresados_P_UCI_por_replicacion[i][j])
                lista_pacientes_ingresados_UCI_por_dia[j].append(lista_pacientes_ingresados_UCI_por_replicacion[i][j])
                
                lista_altas_agregado_por_dia[j].append(lista_altas_agregado_por_replicacion[i][j])
                lista_altas_hospital_por_dia[j].append(lista_altas_hospital_por_replicacion[i][j])
                lista_altas_UCI0_por_dia[j].append(lista_altas_UCI0_por_replicacion[i][j])
                lista_altas_P_UCI_por_dia[j].append(lista_altas_P_UCI_por_replicacion[i][j])
                lista_altas_UCI_por_dia[j].append(lista_altas_UCI_por_replicacion[i][j])
                
                lista_ocupaciones_agregado_por_dia[j].append(lista_ocupaciones_agregado_por_replicacion[i][j])
                lista_ocupaciones_hospital_por_dia[j].append(lista_ocupaciones_hospital_por_replicacion[i][j])
                lista_ocupaciones_UCI_por_dia[j].append(lista_ocupaciones_UCI_por_replicacion[i][j])
                
                
          
        
        lista_casos_diarios_minima = []
        lista_casos_diarios_mediana = []
        lista_casos_diarios_maxima = []
        
        
        global lista_pacientes_ingresados_agregado_minima
        global lista_pacientes_ingresados_agregado_mediana
        global lista_pacientes_ingresados_agregado_maxima
        global lista_pacientes_ingresados_hospital_minima
        global lista_pacientes_ingresados_hospital_mediana
        global lista_pacientes_ingresados_hospital_maxima
        global lista_pacientes_ingresados_UCI_minima
        global lista_pacientes_ingresados_UCI_mediana
        global lista_pacientes_ingresados_UCI_maxima
        
        lista_pacientes_ingresados_agregado_minima = []
        lista_pacientes_ingresados_agregado_mediana = []
        lista_pacientes_ingresados_agregado_maxima = []
        lista_pacientes_ingresados_hospital_minima = []
        lista_pacientes_ingresados_hospital_mediana = []
        lista_pacientes_ingresados_hospital_maxima = []
        lista_pacientes_ingresados_UCI0_minima = []
        lista_pacientes_ingresados_UCI0_mediana = []
        lista_pacientes_ingresados_UCI0_maxima = []
        lista_pacientes_ingresados_P_UCI_minima = []
        lista_pacientes_ingresados_P_UCI_mediana = []
        lista_pacientes_ingresados_P_UCI_maxima = []
        lista_pacientes_ingresados_UCI_minima = []
        lista_pacientes_ingresados_UCI_mediana = []
        lista_pacientes_ingresados_UCI_maxima = []
        
        
        lista_altas_agregado_minima = []
        lista_altas_agregado_mediana = []
        lista_altas_agregado_maxima = []
        lista_altas_hospital_minima = []
        lista_altas_hospital_mediana = []
        lista_altas_hospital_maxima = []
        lista_altas_UCI0_minima = []
        lista_altas_UCI0_mediana = []
        lista_altas_UCI0_maxima = []
        lista_altas_P_UCI_minima = []
        lista_altas_P_UCI_mediana = []
        lista_altas_P_UCI_maxima = []
        lista_altas_UCI_minima = []
        lista_altas_UCI_mediana = []
        lista_altas_UCI_maxima = []
        
        global lista_ocupaciones_agregado_minima
        global lista_ocupaciones_agregado_mediana
        global lista_ocupaciones_agregado_maxima
        global lista_ocupaciones_hospital_minima
        global lista_ocupaciones_hospital_mediana
        global lista_ocupaciones_hospital_maxima
        global lista_ocupaciones_UCI_minima
        global lista_ocupaciones_UCI_mediana
        global lista_ocupaciones_UCI_maxima
        
        lista_ocupaciones_agregado_minima = []
        lista_ocupaciones_agregado_mediana = []
        lista_ocupaciones_agregado_maxima = []
        lista_ocupaciones_hospital_minima = []
        lista_ocupaciones_hospital_mediana = []
        lista_ocupaciones_hospital_maxima = []
        lista_ocupaciones_UCI_minima = []
        lista_ocupaciones_UCI_mediana = []
        lista_ocupaciones_UCI_maxima = []
        
           
        
        
        minimo = MINIMO
        mediana = MEDIANA
        maximo = MAXIMO
        
        for i in range(HORIZON_VISUALIZATION):
            lista_casos_diarios_minima.append(np.percentile(np.array(y_new_cases_Poisson[i]),minimo))
            lista_casos_diarios_mediana.append(np.percentile(np.array(y_new_cases_Poisson[i]),mediana))
            lista_casos_diarios_maxima.append(np.percentile(np.array(y_new_cases_Poisson[i]),maximo))
            
            lista_pacientes_ingresados_agregado_minima.append(np.percentile(np.array(lista_pacientes_ingresados_agregado_por_dia[i]),minimo))
            lista_pacientes_ingresados_agregado_mediana.append(np.percentile(np.array(lista_pacientes_ingresados_agregado_por_dia[i]),mediana))
            lista_pacientes_ingresados_agregado_maxima.append(np.percentile(np.array(lista_pacientes_ingresados_agregado_por_dia[i]),maximo))
            lista_pacientes_ingresados_hospital_minima.append(np.percentile(np.array(lista_pacientes_ingresados_hospital_por_dia[i]),minimo))
            lista_pacientes_ingresados_hospital_mediana.append(np.percentile(np.array(lista_pacientes_ingresados_hospital_por_dia[i]),mediana))
            lista_pacientes_ingresados_hospital_maxima.append(np.percentile(np.array(lista_pacientes_ingresados_hospital_por_dia[i]),maximo))
            lista_pacientes_ingresados_UCI0_minima.append(np.percentile(np.array(lista_pacientes_ingresados_UCI0_por_dia[i]),minimo))
            lista_pacientes_ingresados_UCI0_mediana.append(np.percentile(np.array(lista_pacientes_ingresados_UCI0_por_dia[i]),mediana))
            lista_pacientes_ingresados_UCI0_maxima.append(np.percentile(np.array(lista_pacientes_ingresados_UCI0_por_dia[i]),maximo))
            lista_pacientes_ingresados_P_UCI_minima.append(np.percentile(np.array(lista_pacientes_ingresados_P_UCI_por_dia[i]),minimo))
            lista_pacientes_ingresados_P_UCI_mediana.append(np.percentile(np.array(lista_pacientes_ingresados_P_UCI_por_dia[i]),mediana))
            lista_pacientes_ingresados_P_UCI_maxima.append(np.percentile(np.array(lista_pacientes_ingresados_P_UCI_por_dia[i]),maximo))
            lista_pacientes_ingresados_UCI_minima.append(np.percentile(np.array(lista_pacientes_ingresados_UCI_por_dia[i]),minimo))
            lista_pacientes_ingresados_UCI_mediana.append(np.percentile(np.array(lista_pacientes_ingresados_UCI_por_dia[i]),mediana))
            lista_pacientes_ingresados_UCI_maxima.append(np.percentile(np.array(lista_pacientes_ingresados_UCI_por_dia[i]),maximo))
            
            
            lista_altas_agregado_minima.append(np.percentile(np.array(lista_altas_agregado_por_dia[i]),minimo))
            lista_altas_agregado_mediana.append(np.percentile(np.array(lista_altas_agregado_por_dia[i]),mediana))
            lista_altas_agregado_maxima.append(np.percentile(np.array(lista_altas_agregado_por_dia[i]),maximo))
            lista_altas_hospital_minima.append(np.percentile(np.array(lista_altas_hospital_por_dia[i]),minimo))
            lista_altas_hospital_mediana.append(np.percentile(np.array(lista_altas_hospital_por_dia[i]),mediana))
            lista_altas_hospital_maxima.append(np.percentile(np.array(lista_altas_hospital_por_dia[i]),maximo))
            lista_altas_UCI0_minima.append(np.percentile(np.array(lista_altas_UCI0_por_dia[i]),minimo))
            lista_altas_UCI0_mediana.append(np.percentile(np.array(lista_altas_UCI0_por_dia[i]),mediana))
            lista_altas_UCI0_maxima.append(np.percentile(np.array(lista_altas_UCI0_por_dia[i]),maximo))
            lista_altas_P_UCI_minima.append(np.percentile(np.array(lista_altas_P_UCI_por_dia[i]),minimo))
            lista_altas_P_UCI_mediana.append(np.percentile(np.array(lista_altas_P_UCI_por_dia[i]),mediana))
            lista_altas_P_UCI_maxima.append(np.percentile(np.array(lista_altas_P_UCI_por_dia[i]),maximo))
            lista_altas_UCI_minima.append(np.percentile(np.array(lista_altas_UCI_por_dia[i]),minimo))
            lista_altas_UCI_mediana.append(np.percentile(np.array(lista_altas_UCI_por_dia[i]),mediana))
            lista_altas_UCI_maxima.append(np.percentile(np.array(lista_altas_UCI_por_dia[i]),maximo))
            
            
            lista_ocupaciones_agregado_minima.append(np.percentile(np.array(lista_ocupaciones_agregado_por_dia[i]),minimo))
            lista_ocupaciones_agregado_mediana.append(np.percentile(np.array(lista_ocupaciones_agregado_por_dia[i]),mediana))
            lista_ocupaciones_agregado_maxima.append(np.percentile(np.array(lista_ocupaciones_agregado_por_dia[i]),maximo))
            lista_ocupaciones_hospital_minima.append(np.percentile(np.array(lista_ocupaciones_hospital_por_dia[i]),minimo))
            lista_ocupaciones_hospital_mediana.append(np.percentile(np.array(lista_ocupaciones_hospital_por_dia[i]),mediana))
            lista_ocupaciones_hospital_maxima.append(np.percentile(np.array(lista_ocupaciones_hospital_por_dia[i]),maximo))
            lista_ocupaciones_UCI_minima.append(np.percentile(np.array(lista_ocupaciones_UCI_por_dia[i]),minimo))
            lista_ocupaciones_UCI_mediana.append(np.percentile(np.array(lista_ocupaciones_UCI_por_dia[i]),mediana))
            lista_ocupaciones_UCI_maxima.append(np.percentile(np.array(lista_ocupaciones_UCI_por_dia[i]),maximo))
            
            
        #Guardar las ocupaciónes máximas de la UCI y días en los que se produce.
        lista_replicaciones = []
        lista_ocupaciones_maxima_UCI = []
        lista_dias_ocupaciones_maxima_UCI = []
        for replication in range(SIMULATION_REPLICACTIONS):
            ocupacion_maxima_UCI = max(lista_ocupaciones_UCI_por_replicacion[replication])
            dia_ocupaciones_maxima_UCI = lista_ocupaciones_UCI_por_replicacion[replication].index(ocupacion_maxima_UCI)
            lista_ocupaciones_maxima_UCI.append(ocupacion_maxima_UCI[0])
            lista_dias_ocupaciones_maxima_UCI.append(dia_ocupaciones_maxima_UCI)
            lista_replicaciones.append(replication+1)
            
            
        
        # Hay que generar 15 dataFrames con las salidas en las 15 combinaciones.
        # Estos dataFrames se guardarán en distintas hojas del Excel.
        
        df_output_UCI_1 = pd.DataFrame()
        df_output_UCI_2 = pd.DataFrame()
        
            
        ############################################################
        
        # DataFrame 3 UCI
        df_output_UCI_1[COLUMN_DAY] = lista_fechas
        df_output_UCI_1[COLUMN_DAILY_CASES_P05] = lista_casos_diarios_minima
        df_output_UCI_1[COLUMN_DAILY_CASES_P50] = lista_casos_diarios_mediana
        df_output_UCI_1[COLUMN_DAILY_CASES_P95] = lista_casos_diarios_maxima
        df_output_UCI_1[COLUMN_DIRECT_ADMISSIONS_IN_ICU_P05] = lista_pacientes_ingresados_UCI0_minima
        df_output_UCI_1[COLUMN_DIRECT_ADMISSIONS_IN_ICU_P50] = lista_pacientes_ingresados_UCI0_mediana
        df_output_UCI_1[COLUMN_DIRECT_ADMISSIONS_IN_ICU_P95] = lista_pacientes_ingresados_UCI0_maxima
        df_output_UCI_1[COLUMN_ICU_ADMISSIONS_FROM_WARDS_P05] = lista_pacientes_ingresados_P_UCI_minima
        df_output_UCI_1[COLUMN_ICU_ADMISSIONS_FROM_WARDS_P50] = lista_pacientes_ingresados_P_UCI_mediana
        df_output_UCI_1[COLUMN_ICU_ADMISSIONS_FROM_WARDS_P95] = lista_pacientes_ingresados_P_UCI_maxima
        df_output_UCI_1[COLUMN_ICU_ADMISSIONS_P05] = lista_pacientes_ingresados_UCI_minima
        df_output_UCI_1[COLUMN_ICU_ADMISSIONS_P50] = lista_pacientes_ingresados_UCI_mediana
        df_output_UCI_1[COLUMN_ICU_ADMISSIONS_P95] = lista_pacientes_ingresados_UCI_maxima
        df_output_UCI_1[COLUMN_DIRECT_ICU_DISCHARGES_P05] = lista_altas_UCI0_minima
        df_output_UCI_1[COLUMN_DIRECT_ICU_DISCHARGES_P50] = lista_altas_UCI0_mediana
        df_output_UCI_1[COLUMN_DIRECT_ICU_DISCHARGES_P95] = lista_altas_UCI0_maxima
        df_output_UCI_1[COLUMN_ICU_DISCHARGES_TO_WARDS_P05] = lista_altas_P_UCI_minima
        df_output_UCI_1[COLUMN_ICU_DISCHARGES_TO_WARDS_P50] = lista_altas_P_UCI_mediana
        df_output_UCI_1[COLUMN_ICU_DISCHARGES_TO_WARDS_P95] = lista_altas_P_UCI_maxima
        df_output_UCI_1[COLUMN_ICU_DISCHARGES_P05] = lista_altas_UCI_minima
        df_output_UCI_1[COLUMN_ICU_DISCHARGES_P50] = lista_altas_UCI_mediana
        df_output_UCI_1[COLUMN_ICU_DISCHARGES_P95] = lista_altas_UCI_maxima
        df_output_UCI_1[COLUMN_ICU_BED_OCCUPANCY_P05] = lista_ocupaciones_UCI_minima
        df_output_UCI_1[COLUMN_ICU_BED_OCCUPANCY_P50] = lista_ocupaciones_UCI_mediana
        df_output_UCI_1[COLUMN_ICU_BED_OCCUPANCY_P95] = lista_ocupaciones_UCI_maxima
        
        df_output_UCI_2[COLUMN_REPLICATION] = lista_replicaciones
        df_output_UCI_2[COLUMN_MAXIMUM_ICU__BED_OCCUPANCY] = lista_ocupaciones_maxima_UCI
        df_output_UCI_2[COLUMN_DAY_OF_MAXIMUM_ICU_BED_OCCUPANCY] = lista_dias_ocupaciones_maxima_UCI
        
        df = [df_output_UCI_1, df_output_UCI_2]
        df_output_UCI = pd.concat(df, axis=1)
        
        
        #df_output_agregado.to_excel(writer_resultado_simulacion, sheet_name="Agregado", index=False)
        #df_output_hospital.to_excel(writer_resultado_simulacion, sheet_name="Hospital", index=False)
        df_output_UCI.to_excel(writer_resultado_simulacion, sheet_name=estimator, index=False)
        
        
    # Close the Pandas Excel writer and output the Excel file.
    writer_resultado_simulacion.save()  
    


