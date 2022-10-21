# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:46:40 2022

@author: daniel
"""

from config.config import *

import pandas as pd
import numpy as np
import random as rnd

from datetime import datetime

import matplotlib.pyplot as plt
import math
import os.path

from scipy.stats import poisson
from scipy.stats import weibull_min
from scipy.stats import lognorm
from scipy.stats import expon
from scipy.stats import triang
import scipy.integrate as integrate
from scipy.integrate import simps

from reliability.Fitters import Fit_Weibull_2P
from reliability.Fitters import Fit_Lognormal_2P


# Funciones

# Función de ajuste de la evolución del coronavirus
def gompertz_calc(x, A, u, d):
    """Gompertz growth model. 
    
    Proposed in Zwietering et al., 1990 (PMID: 16348228) 
    """ 
    y = (A * np.exp(-np.exp((((u * np.e) / A) * (d - x)) + 1)))
    
    return y


# Nueva función de ajuste de la evolución del coronavirus. Tiene en cuenta el tiempo de duración.
def Gompertz_Temp(x, A, C, d):
    """Gompertz growth model. 
    
    Proposed in Zwietering et al., 1990 (PMID: 16348228) 
    """ 
    return A * np.exp(-np.exp(((C * np.e) * (d - x)) + 1)) 


def Gompertz_Temp_Derivada(x, A, C, d):
    """Gompertz growth model. 
    
    Proposed in Zwietering et al., 1990 (PMID: 16348228) 
    """ 
    
    y = (A*C * np.exp(-np.exp(((C * np.e) * (d - x)) + 1) - C * np.e*x + C * np.e*d + 2))
    
    return y

def Gompertz_Temp_Derivada_2(x, A2, C2, d2):
    """Gompertz growth model. 
    
    Proposed in Zwietering et al., 1990 (PMID: 16348228) 
    """ 
    
    y = (A2*C2 * np.exp(-np.exp(((C2 * np.e) * (d2 - x)) + 1) - C2 * np.e*x + C2 * np.e*d2 + 2))
    
    return y

def weibull_survival_expression(x, scale, shape):
    y = np.exp(-(x/scale)**shape)
    
    return y

def generate_arrivals_curve(dia_comienzo,
                            x0_dia_punto_fijo,
                            formato_fecha_entrada,
                            porcentaje_poblacion_afectada,
                            numero_esperado_casos_totales,
                            numero_dias_pandemia,
                            y0_casos_punto_fijo,
                            horizonte_visualizacion,
                            funcion,
                            experiment):
    # Se genera la curva de llegadas
    # Se convierten los Strings a fechas
    date_comienzo = datetime.strptime(dia_comienzo, formato_fecha_entrada)
    date0 = datetime.strptime(x0_dia_punto_fijo, formato_fecha_entrada)
    gap_between_data_and_start = 1
    
    
    
    # El valor de k depende del porcentaje de la población contagiada que queremos meter en el tiempo.
    a = -(math.log(-math.log(porcentaje_poblacion_afectada+(1-porcentaje_poblacion_afectada)/2))-1)/np.e
    b = -(math.log(-math.log((1-porcentaje_poblacion_afectada)/2))-1)/np.e
    k = a-b
    
    
    # Fijando parámetro A, C, d
    A_fixed = numero_esperado_casos_totales
    
    T_fixed = numero_dias_pandemia
    k_fixed = k
    C_fixed = k_fixed/T_fixed
    
    d_fixed = 1/(C_fixed*np.e)*(math.log(-math.log(y0_casos_punto_fijo/A_fixed))-1)-gap_between_data_and_start
    
    
    params = [A_fixed, C_fixed, d_fixed]
    #print(params)
    
    params3 = np.array(params)
    
    x_personalizada = []
    for i in range(horizonte_visualizacion):
        x_personalizada.append(i)  
    
    
    y_personalizada = []
    for dato in x_personalizada:
        y_personalizada.append(funcion(dato, A_fixed, C_fixed, d_fixed))
    
    #######
    # Distinguir si es esrtimación o simulación.
    y_nuevos_casos_Poisson = generate_Poisson_Arrivals(y_personalizada,experiment)
        
 
    
    
    
    plt.plot(x_personalizada, y_personalizada, 'g-', label='Daily Gompertz curve')#'Original'
    #plt.plot(x_personalizada, y_nuevos_casos_Poisson, 'k-', label='Poisson')
    
    plt.legend(loc='best')
    plt.show()

    return y_nuevos_casos_Poisson, x_personalizada, y_personalizada


def generate_Poisson_Arrivals(y_personalizada,experiment):
    y_nuevos_casos_Poisson = []
    # Se calcula el número de casos de coronarvirus nuevos cada día
    for i in range(len(y_personalizada)):
        # Solo se recalcula el valor de los nuevos casos a prtir del día de comienzo de la simulación.
        casos_decimal = y_personalizada[i]
        # Se simula un número aleatorio de poisson para aleatorizar las llegadas.
        if experiment == ESTIMATION:
            casos_entero = poisson.rvs(casos_decimal)
        elif experiment == SIMULATION:
            casos_entero = int(round(casos_decimal))            
            
        y_nuevos_casos_Poisson.append(casos_entero)
        
    return y_nuevos_casos_Poisson
    

def simulate_stays_and_pathway(y_new_cases_Poisson,lista_random_pacientes_P_I,contador_random_pacientes_P_I,lista_random_sorteo_entrada_coronavirus,contador_random_sorteo_entrada_coronavirus,lista_random_pacientes_P_IW,contador_random_pacientes_P_IW,lista_random_pacientes_P_WI,contador_random_pacientes_P_WI,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q):
    rows_list = []
    
    # Simulación de llegadas y estancias
    for dia in range(len(y_new_cases_Poisson)):
        for patient in range(y_new_cases_Poisson[dia]):
            date_HA = 0
            date_HD = 0
            date_IA = 0
            date_ID = 0
            # Paciente que ingresa en el hospital
            # Se sortea si el paciente ingresa en el hospital o en la UCI directamente
            if len(lista_random_pacientes_P_I) == 0:
                r = rnd.random()
            else:
                r = lista_random_pacientes_P_I[contador_random_pacientes_P_I]
                contador_random_pacientes_P_I += 1
                if contador_random_pacientes_P_I == RANDOM_LSIT_SIZE:
                    contador_random_pacientes_P_I = 0
            if r < P_I:
                # El paciente ingresa en la UCI directamente.
                # Ahora a este paciente hay que calcularle la estancia en UCI
                tipo_estancia = 'LOS_UCI'
                if len(lista_random_sorteo_entrada_coronavirus) == 0:
                    r = rnd.random()
                else:
                    r = lista_random_sorteo_entrada_coronavirus[contador_random_sorteo_entrada_coronavirus]
                    contador_random_sorteo_entrada_coronavirus += 1
                    if contador_random_sorteo_entrada_coronavirus == RANDOM_LSIT_SIZE:
                        contador_random_sorteo_entrada_coronavirus = 0
                ingreso = dia + r
                date_HA = ingreso
                date_IA = ingreso
                parametro_a, parametro_b, parametro_c = obtain_distribution_parameters_fixed(tipo_estancia)
                estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parametro_a,parametro_b,parametro_c,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                salida = ingreso + estancia
                date_ID = salida
                
                
                # Ahora se calcula si el paciente va de la UCI a planta.
                if len(lista_random_pacientes_P_IW) == 0:
                    r = rnd.random()
                else:
                    r = lista_random_pacientes_P_IW[contador_random_pacientes_P_IW]
                    contador_random_pacientes_P_IW += 1
                    if contador_random_pacientes_P_IW == RANDOM_LSIT_SIZE:
                        contador_random_pacientes_P_IW = 0
                if r < P_IW:
                    # El paciente va a planta.
                    recorrido = 'UCI_P'
                    
                    
                    
                    # Se le genera un tiempo de estancia.
                    tipo_estancia = 'LOS_UCI_P'
                    ingreso = salida
                    parametro_a, parametro_b, parametro_c = obtain_distribution_parameters_fixed(tipo_estancia)
                    estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parametro_a,parametro_b,parametro_c,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                    salida = ingreso + estancia
                    date_HD = salida
                    
                    
                
                else:
                    # El paciente sale de la UCI directamente.
                    date_HD = date_ID
                    
            else:
                # El paciente ingresa en el hospital.
                # Ahora se calcula si el paciente va de la planta a la UCI.
                if len(lista_random_pacientes_P_WI) == 0:
                    r = rnd.random()
                else:
                    r = lista_random_pacientes_P_WI[contador_random_pacientes_P_WI]
                    contador_random_pacientes_P_WI += 1
                    if contador_random_pacientes_P_WI == RANDOM_LSIT_SIZE:
                        contador_random_pacientes_P_WI = 0
                if r < P_WI:
                    # El paciente va a la UCI desde planta.                                
                    # Ahora a este paciente hay que calcularle la estancia en planta hasta UCI
                    tipo_estancia = 'LOS_P_UCI'
                    if len(lista_random_sorteo_entrada_coronavirus) == 0:
                        r = rnd.random()
                    else:
                        r = lista_random_sorteo_entrada_coronavirus[contador_random_sorteo_entrada_coronavirus]
                        contador_random_sorteo_entrada_coronavirus += 1
                        if contador_random_sorteo_entrada_coronavirus == RANDOM_LSIT_SIZE:
                            contador_random_sorteo_entrada_coronavirus = 0
                    ingreso = dia + r
                    date_HA = ingreso
                    parametro_a, parametro_b, parametro_c = obtain_distribution_parameters_fixed(tipo_estancia)
                    estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parametro_a,parametro_b,parametro_c,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                    salida = ingreso + estancia
                    date_IA = salida
                                                   
                    
                    # Ahora este paciente hay que calcularle la estancia en UCI
                    tipo_estancia = 'LOS_UCI'
                    ingreso = salida
                    parametro_a, parametro_b, parametro_c = obtain_distribution_parameters_fixed(tipo_estancia)
                    estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parametro_a,parametro_b,parametro_c,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                    salida = ingreso + estancia
                    date_ID = salida
                                                                                 
                                                 
                    # Ahora se calcula si el paciente va de la UCI a planta.
                    if len(lista_random_pacientes_P_IW) == 0:
                        r = rnd.random()
                    else:
                        r = lista_random_pacientes_P_IW[contador_random_pacientes_P_IW]
                        contador_random_pacientes_P_IW += 1
                        if contador_random_pacientes_P_IW == RANDOM_LSIT_SIZE:
                            contador_random_pacientes_P_IW = 0
                    if r < P_IW:
                        # Se le genera un tiempo de estancia.
                        tipo_estancia = 'LOS_UCI_P'
                        recorrido = 'UCI_P'
                        ingreso = salida
                        parametro_a, parametro_b, parametro_c = obtain_distribution_parameters_fixed(tipo_estancia)
                        estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parametro_a,parametro_b,parametro_c,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                        salida = ingreso + estancia
                        date_HD = salida
                        
                    else:
                        # El paciente no sale de la UCI a planta.
                        date_HD = date_ID
                       
                else:
                    # El paciente se queda en planta todo el tiempo.
                    # Ahora a este paciente hay que calcularle la estancia en planta
                    tipo_estancia = 'LOS_H'
                    if len(lista_random_sorteo_entrada_coronavirus) == 0:
                        r = rnd.random()
                    else:
                        r = lista_random_sorteo_entrada_coronavirus[contador_random_sorteo_entrada_coronavirus]
                        contador_random_sorteo_entrada_coronavirus += 1
                        if contador_random_sorteo_entrada_coronavirus == RANDOM_LSIT_SIZE:
                            contador_random_sorteo_entrada_coronavirus = 0
                    ingreso = dia + r
                    date_HA = ingreso
                    parametro_a, parametro_b, parametro_c = obtain_distribution_parameters_fixed(tipo_estancia)
                    estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q = generate_stay_in_simulation(tipo_estancia,parametro_a,parametro_b,parametro_c,STAYS_PROBABILITY_DISTRIBUTION,0,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q)
                    salida = ingreso + estancia
                    date_HD = salida
                    
    
    
            rows_list.append([date_HA,date_HD,date_IA,date_ID])
   

    return rows_list,contador_random_pacientes_P_I,contador_random_sorteo_entrada_coronavirus,contador_random_pacientes_P_IW,contador_random_pacientes_P_WI,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q

def save_file_stays_and_arrivals(excel_name,rows_list,x_personalized,y_personalized,y_new_cases_Poisson):
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer_Input_Data = pd.ExcelWriter(excel_name,engine='xlsxwriter')
    
    df_Estancias_simuladas = pd.DataFrame(rows_list, columns=(COLUMN_DATE_HA,COLUMN_DATE_HD,COLUMN_DATE_IA,COLUMN_DATE_ID))  
    # Se ordena el datFrame en base a la columna Tiempo.
    df_Estancias_simuladas = df_Estancias_simuladas.sort_values(COLUMN_DATE_HA)
    
    df_valores_Gompertz = pd.DataFrame()
    df_valores_Gompertz[COLUMN_DAY] = x_personalized
    df_valores_Gompertz[COLUMN_G_REAL] = y_personalized
    df_valores_Gompertz[COLUMN_G_POISSON] = y_new_cases_Poisson
    
    
    df_Estancias_simuladas.to_excel(writer_Input_Data, sheet_name=SHEET_SIMULATED_STAYS, index=False)
    df_valores_Gompertz.to_excel(writer_Input_Data, sheet_name=SHEET_GOMPERTZ_ARRIVALS, index=False)
    # Close the Pandas Excel writer and output the Excel file.
    writer_Input_Data.save()


def generate_data_frame_stays_in_day_d(rows_list,dia_simulacion):
    df_Estancias = pd.DataFrame(rows_list, columns=(COLUMN_DATE_HA,COLUMN_DATE_HD,COLUMN_DATE_IA,COLUMN_DATE_ID))  
             
    ind_UCI = []
    ind_P_UCI = []
    ind_UCI_P = []
    
    cens_H = []
    cens_UCI = []
    cens_P_UCI = []
    
    LOS_H = []
    LOS_P_UCI = []
    LOS_UCI = []
    LOS_UCI_P = []
    LOS_Total = []
    
    # Primero se preparan los indicadores, variables de censura, LOS...
    for i in range(len(df_Estancias)):
        # Se comprueba que el paciente haya ingresado en el periodo de estudio.
        if df_Estancias.loc[i, COLUMN_DATE_HA] <= dia_simulacion:
            # Se comprueba si el dato de estancia en el hospital es censurado.
            if df_Estancias.loc[i, COLUMN_DATE_HD] > dia_simulacion:
                # Dato censuarado de estancia en el hospital
                # Se le asigna la fecha de inicio como fecha de salida.
                df_Estancias.loc[i, COLUMN_DATE_HD] = dia_simulacion
                censura_H = 1
            else:
                censura_H = 0
            # Al principio se les asigna a todos los pacientes que no tienen censura para ir a la UCI desde planta.
            censura_P_UCI = 0
            # Se comprueba si tiene fecha de entrada en la UCI para asignarle el indicador
            if df_Estancias.loc[i, COLUMN_DATE_IA] == 0 or df_Estancias.loc[i, COLUMN_DATE_IA] > dia_simulacion:
                df_Estancias.loc[i, COLUMN_DATE_IA] = 0
                
                # Paciente solo en el hospital
                indicador_UCI = 0
                indicador_P_UCI = 0
                indicador_UCI_P = 0
                
                # Se le añade que no tiene censura en la UCI (esto no aporta información, pero así se mantiene la longitud del array)
                censura_UCI = 0            
                            
                # Se calcula la estancia en el hospital.
                estancia_H = df_Estancias.loc[i, COLUMN_DATE_HD] - df_Estancias.loc[i, COLUMN_DATE_HA]
                # Para evitar ceros de pacientes que ingresas y salen el mismo día.
                estancia_P_UCI = 0
                estancia_UCI = 0
                estancia_UCI_P = 0
                
            else:
                # Paciente que va a la UCI
                indicador_UCI = 1
                estancia_H = 0            
                
                # Se comprueba si el ingreso en UCI es directo            
                gap_between_P_UCI = df_Estancias.loc[i, COLUMN_DATE_IA] - df_Estancias.loc[i, COLUMN_DATE_HA]
                if gap_between_P_UCI == 0:
                    # Ingreso directo en UCI. No pasa por planta.
                    indicador_P_UCI = 0
                    estancia_P_UCI = 0                
                else:
                    indicador_P_UCI = 1
                    estancia_P_UCI = gap_between_P_UCI
                
                # Se comprueba si el dato de estancia en UCI es censurado.
                if df_Estancias.loc[i, COLUMN_DATE_ID] > dia_simulacion:
                    # Dato censuarado de estancia en UCI
                    # Se le asigna la fecha de inicio como fecha de alta
                    df_Estancias.loc[i, COLUMN_DATE_ID] = dia_simulacion
                    censura_UCI = 1
                else:
                    censura_UCI = 0
                
                # Se calcula la estancia en UCI.
                estancia_UCI = df_Estancias.loc[i, COLUMN_DATE_ID] - df_Estancias.loc[i, COLUMN_DATE_IA]
                        
                # Se comprueba si el paciente sale de la UCI a planta.
                if df_Estancias.loc[i, COLUMN_DATE_HD] > dia_simulacion:
                    # Se le asigna la fecha de inicio como fecha de alta
                    df_Estancias.loc[i, COLUMN_DATE_HD] = dia_simulacion
                
                gap_between_UCI_P = df_Estancias.loc[i, COLUMN_DATE_HD] - df_Estancias.loc[i, COLUMN_DATE_ID]
                if gap_between_UCI_P == 0:
                    # No va a planta después de UCI.
                    indicador_UCI_P = 0
                    estancia_UCI_P = 0
                else:
                    indicador_UCI_P = 1
                    estancia_UCI_P = gap_between_UCI_P
            
            
        else:
            # No se incluye el paciente, se introducen valores negativos de estancia para filtrar el dataFrame.
            indicador_UCI = -1
            indicador_P_UCI = -1
            indicador_UCI_P = -1
            
            censura_H = -1
            censura_UCI = -1
            censura_P_UCI = -1
            
            estancia_H = -1
            estancia_P_UCI = -1
            estancia_UCI = -1
            estancia_UCI_P = -1
            
            
            
        # Se añaden todos los indicadores y variables en los vectores.
        ind_UCI.append(indicador_UCI)
        ind_P_UCI.append(indicador_P_UCI)
        ind_UCI_P.append(indicador_UCI_P)
        
        cens_H.append(censura_H)
        cens_UCI.append(censura_UCI)
        cens_P_UCI.append(censura_P_UCI)
        
        LOS_H.append(estancia_H)
        LOS_P_UCI.append(estancia_P_UCI)
        LOS_UCI.append(estancia_UCI)
        LOS_UCI_P.append(estancia_UCI_P)
        LOS_Total.append(estancia_H+estancia_P_UCI+estancia_UCI+estancia_UCI_P)
        
    
    # Se añaden los vectores al dataframe.
    df_Estancias['LOS_H'] = LOS_H
    df_Estancias['LOS_P_UCI'] = LOS_P_UCI
    df_Estancias['LOS_UCI'] = LOS_UCI
    df_Estancias['LOS_UCI_P'] = LOS_UCI_P
    df_Estancias['LOS_Total'] = LOS_Total
    
    df_Estancias['Cens_H'] = cens_H
    df_Estancias['Cens_UCI'] = cens_UCI
    df_Estancias['Cens_P_UCI'] = cens_P_UCI
    
    df_Estancias['Ind_UCI'] = ind_UCI
    df_Estancias['Ind_P_UCI'] = ind_P_UCI
    df_Estancias['Ind_UCI_P'] = ind_UCI_P
    
    
    # Me quedo sólo con los registros de tiempo de estancia positivos
    df_Estancias = df_Estancias[(df_Estancias['LOS_H'] >= 0)]
    df_Estancias = df_Estancias.reset_index(drop=True)   
    
    
    return df_Estancias

def obtain_distribution_parameters_fixed(tipo_estancia):
    parametro_a = 0
    parametro_b = 0
    parametro_c = 0
    
    if tipo_estancia == 'LOS_H':
        parametro_a = PARAMETER_a_X
        parametro_b = PARAMETER_b_X
        parametro_c = PARAMETER_c_X
    elif tipo_estancia == 'LOS_P_UCI':
        parametro_a = PARAMETER_a_Z
        parametro_b = PARAMETER_b_Z
        parametro_c = PARAMETER_c_Z
    elif tipo_estancia == 'LOS_UCI':
        parametro_a = PARAMETER_a_Y
        parametro_b = PARAMETER_b_Y
        parametro_c = PARAMETER_c_Y
    elif tipo_estancia == 'LOS_UCI_P':
        parametro_a = PARAMETER_a_Q
        parametro_b = PARAMETER_b_Q
        parametro_c = PARAMETER_c_Q
    
    return parametro_a,parametro_b,parametro_c

# =============================================================================
# def generar_Tiempo_de_Estancia(tipo_estancia,probability_distribution):
#     global contador_random_pacientes_coronavirus
#     
#     estancia = 0
#     parametro_a, parametro_b, parametro_c = obtain_distribution_parameters_fixed(tipo_estancia)
#     distribucion = probability_distribution
#     
#     if distribucion == WEIBULL:
#         estancia = weibull_min.rvs(parametro_a, loc=0, scale=parametro_b)
#       
#     elif distribucion == LOGNORMAL:
#         estancia = lognorm.rvs(parametro_b, loc=0, scale=np.exp(parametro_a))
#     
#     return estancia
# =============================================================================


def generate_stay_with_estimation_NP(lista_tiempos_ordenados,vector_w,lista_random_estancia_Z,contador_random_estancia_Z):
    vector_w_acumulado = []
    suma_acumulada = 0
    for w in vector_w:
        suma_acumulada += w
        vector_w_acumulado.append(suma_acumulada)
    
    r = lista_random_estancia_Z[contador_random_estancia_Z]
    contador_random_estancia_Z += 1
    if contador_random_estancia_Z == RANDOM_LSIT_SIZE:
        contador_random_estancia_Z = 0
    for tiempo,w_acumulado in zip(lista_tiempos_ordenados,vector_w_acumulado):
        estancia = tiempo
        if w_acumulado > r:
            break
    
    return estancia,contador_random_estancia_Z

def generate_stay_in_simulation(tipo_estancia,parametro_a,parametro_b,parametro_c,probability_distribution,estancia_previa,lista_random_estancia_X,contador_random_estancia_X,lista_random_estancia_Z,contador_random_estancia_Z,lista_random_estancia_Y,contador_random_estancia_Y,lista_random_estancia_Q,contador_random_estancia_Q):
    estancia = 0    
    distribucion = probability_distribution
    
    if distribucion == "Weibull":
        p_Hazard_rate = weibull_min.cdf(estancia_previa,parametro_a,loc=0,scale=parametro_b)
# =============================================================================
#         print(p_Hazard_rate)
#         print(parametro_a)
#         print(parametro_b)
# =============================================================================
        if p_Hazard_rate <= PROBABILITY_DISTINGUISH_LONG_STAYS:            
            while estancia <= estancia_previa:
                if tipo_estancia == 'LOS_H':
                    if len(lista_random_estancia_X) == 0:
                        r = int(rnd.random()*(2**32-2))
                    else:
                        r = int(lista_random_estancia_X[contador_random_estancia_X]*(2**32-2))
                        contador_random_estancia_X += 1
                        if contador_random_estancia_X == RANDOM_LSIT_SIZE:
                            contador_random_estancia_X = 0
                elif tipo_estancia == 'LOS_P_UCI':
                    if len(lista_random_estancia_Z) == 0:
                        r = int(rnd.random()*(2**32-2))
                    else:
                        r = int(lista_random_estancia_Z[contador_random_estancia_Z]*(2**32-2))
                        contador_random_estancia_Z += 1
                        if contador_random_estancia_Z == RANDOM_LSIT_SIZE:
                            contador_random_estancia_Z = 0
                elif tipo_estancia == 'LOS_UCI':
                    if len(lista_random_estancia_Y) == 0:
                        r = int(rnd.random()*(2**32-2))
                    else:
                        r = int(lista_random_estancia_Y[contador_random_estancia_Y]*(2**32-2))
                        contador_random_estancia_Y += 1
                        if contador_random_estancia_Y == RANDOM_LSIT_SIZE:
                            contador_random_estancia_Y = 0
                elif tipo_estancia == 'LOS_UCI_P':
                    if len(lista_random_estancia_Q) == 0:
                        r = int(rnd.random()*(2**32-2))
                    else:
                        r = int(lista_random_estancia_Q[contador_random_estancia_Q]*(2**32-2))
                        contador_random_estancia_Q += 1
                        if contador_random_estancia_Q == RANDOM_LSIT_SIZE:
                            contador_random_estancia_Q = 0
                # Añadir random_state=int (entero que puede variar desde 0 hasta 2^32-1)
                estancia = weibull_min.rvs(parametro_a, loc=0, scale=parametro_b,random_state=r)
                
        else:
            if tipo_estancia == 'LOS_H':
                if len(lista_random_estancia_X) == 0:
                    r = int(rnd.random()*(2**32-2))
                else:
                    r = int(lista_random_estancia_X[contador_random_estancia_X]*(2**32-2))
                    contador_random_estancia_X += 1
                    if contador_random_estancia_X == RANDOM_LSIT_SIZE:
                        contador_random_estancia_X = 0
            elif tipo_estancia == 'LOS_P_UCI':
                if len(lista_random_estancia_Z) == 0:
                    r = int(rnd.random()*(2**32-2))
                else:
                    r = int(lista_random_estancia_Z[contador_random_estancia_Z]*(2**32-2))
                    contador_random_estancia_Z += 1
                    if contador_random_estancia_Z == RANDOM_LSIT_SIZE:
                        contador_random_estancia_Z = 0
            elif tipo_estancia == 'LOS_UCI':
                if len(lista_random_estancia_Y) == 0:
                    r = int(rnd.random()*(2**32-2))
                else:
                    r = int(lista_random_estancia_Y[contador_random_estancia_Y]*(2**32-2))
                    contador_random_estancia_Y += 1
                    if contador_random_estancia_Y == RANDOM_LSIT_SIZE:
                        contador_random_estancia_Y = 0
            elif tipo_estancia == 'LOS_UCI_P':
                if len(lista_random_estancia_Q) == 0:
                    r = int(rnd.random()*(2**32-2))
                else:
                    r = int(lista_random_estancia_Q[contador_random_estancia_Q]*(2**32-2))
                    contador_random_estancia_Q += 1
                    if contador_random_estancia_Q == RANDOM_LSIT_SIZE:
                        contador_random_estancia_Q = 0
            #print(estancia_previa)
            lamda_exp = weibull_min.pdf(estancia_previa+1,parametro_a,loc=0,scale=parametro_b)/(1-weibull_min.cdf(estancia_previa+1,parametro_a,loc=0,scale=parametro_b))
            #print(lamda_exp)
            estancia = estancia_previa + expon.rvs(loc=0, scale=1/lamda_exp, random_state=r)
        
        
        
      
    elif distribucion == "Lognormal":
        p_Hazard_rate = lognorm.cdf(estancia_previa,parametro_b,loc=0,scale=np.exp(parametro_a))
        if p_Hazard_rate <= PROBABILITY_DISTINGUISH_LONG_STAYS:            
            while estancia <= estancia_previa:
                if tipo_estancia == 'LOS_H':
                    if len(lista_random_estancia_X) == 0:
                        r = int(rnd.random()*(2**32-2))
                    else:
                        r = int(lista_random_estancia_X[contador_random_estancia_X]*(2**32-2))
                        contador_random_estancia_X += 1
                        if contador_random_estancia_X == RANDOM_LSIT_SIZE:
                            contador_random_estancia_X = 0
                elif tipo_estancia == 'LOS_P_UCI':
                    if len(lista_random_estancia_Z) == 0:
                        r = int(rnd.random()*(2**32-2))
                    else:
                        r = int(lista_random_estancia_Z[contador_random_estancia_Z]*(2**32-2))
                        contador_random_estancia_Z += 1
                        if contador_random_estancia_Z == RANDOM_LSIT_SIZE:
                            contador_random_estancia_Z = 0
                elif tipo_estancia == 'LOS_UCI':
                    if len(lista_random_estancia_Y) == 0:
                        r = int(rnd.random()*(2**32-2))
                    else:
                        r = int(lista_random_estancia_Y[contador_random_estancia_Y]*(2**32-2))
                        contador_random_estancia_Y += 1
                        if contador_random_estancia_Y == RANDOM_LSIT_SIZE:
                            contador_random_estancia_Y = 0
                elif tipo_estancia == 'LOS_UCI_P':
                    if len(lista_random_estancia_Q) == 0:
                        r = int(rnd.random()*(2**32-2))
                    else:
                        r = int(lista_random_estancia_Q[contador_random_estancia_Q]*(2**32-2))
                        contador_random_estancia_Q += 1
                        if contador_random_estancia_Q == RANDOM_LSIT_SIZE:
                            contador_random_estancia_Q = 0
                estancia = lognorm.rvs(parametro_b, loc=0, scale=np.exp(parametro_a), random_state=r)
        else:
            if tipo_estancia == 'LOS_H':
                if len(lista_random_estancia_X) == 0:
                    r = int(rnd.random()*(2**32-2))
                else:
                    r = int(lista_random_estancia_X[contador_random_estancia_X]*(2**32-2))
                    contador_random_estancia_X += 1
                    if contador_random_estancia_X == RANDOM_LSIT_SIZE:
                        contador_random_estancia_X = 0
            elif tipo_estancia == 'LOS_P_UCI':
                if len(lista_random_estancia_Z) == 0:
                    r = int(rnd.random()*(2**32-2))
                else:
                    r = int(lista_random_estancia_Z[contador_random_estancia_Z]*(2**32-2))
                    contador_random_estancia_Z += 1
                    if contador_random_estancia_Z == RANDOM_LSIT_SIZE:
                        contador_random_estancia_Z = 0
            elif tipo_estancia == 'LOS_UCI':
                if len(lista_random_estancia_Y) == 0:
                    r = int(rnd.random()*(2**32-2))
                else:
                    r = int(lista_random_estancia_Y[contador_random_estancia_Y]*(2**32-2))
                    contador_random_estancia_Y += 1
                    if contador_random_estancia_Y == RANDOM_LSIT_SIZE:
                        contador_random_estancia_Y = 0
            elif tipo_estancia == 'LOS_UCI_P':
                if len(lista_random_estancia_Q) == 0:
                    r = int(rnd.random()*(2**32-2))
                else:
                    r = int(lista_random_estancia_Q[contador_random_estancia_Q]*(2**32-2))
                    contador_random_estancia_Q += 1
                    if contador_random_estancia_Q == RANDOM_LSIT_SIZE:
                        contador_random_estancia_Q = 0
            lamda_exp = lognorm.pdf(estancia_previa+1,parametro_b,loc=0,scale=np.exp(parametro_a))/(1-lognorm.cdf(estancia_previa+1,parametro_b,loc=0,scale=np.exp(parametro_a)))
            estancia = estancia_previa + expon.rvs(loc=0, scale=1/lamda_exp, random_state=r)
            
           
    return estancia,contador_random_estancia_X,contador_random_estancia_Z,contador_random_estancia_Y,contador_random_estancia_Q
    


def fit_stay_distribution(fit_distribution,data_failure,data_censored):
    if(len(data_failure)>1):
        ajuste = True
        if fit_distribution == WEIBULL:
            wbf_AICc = 0
            lnf_AICc = 1
        elif fit_distribution == LOGNORMAL:
            wbf_AICc = 1
            lnf_AICc = 0
        elif fit_distribution == BEST:
            ajuste = False
            wbf = Fit_Weibull_2P(failures=data_failure, right_censored=data_censored, show_probability_plot=False, print_results=False)  # fit the Weibull_2P distribution
            lnf = Fit_Lognormal_2P(failures=data_failure, right_censored=data_censored, show_probability_plot=False, print_results=False)  # fit the Lognormal_2P distribution
            wbf_AICc = wbf.AICc
            lnf_AICc = lnf.AICc
            
        if wbf_AICc < lnf_AICc:
            if ajuste:
                wbf = Fit_Weibull_2P(failures=data_failure, right_censored=data_censored, show_probability_plot=False, print_results=False)  # fit the Weibull_2P distribution
            distribution = WEIBULL
            parameter_a = wbf.beta
            parameter_b = wbf.alpha
            parameter_c = parameter_b*math.gamma(1+1/parameter_a)
        else:
            if ajuste:
                lnf = Fit_Lognormal_2P(failures=data_failure, right_censored=data_censored, show_probability_plot=False, print_results=False)  # fit the Lognormal_2P distribution
            distribution = LOGNORMAL
            parameter_a = lnf.mu
            parameter_b = lnf.sigma
            parameter_c = np.exp(parameter_a+parameter_b**2/2)

    else:
        distribution = "None"
        parameter_a = 0
        parameter_b = 0
        parameter_c = 0
    
    
    
    return distribution, parameter_a, parameter_b, parameter_c






def chose_algorithm(estimator):
    if estimator == ESTIMATOR_CI:
        algorithm_function = algorithm_function_CI
    elif estimator == ESTIMATOR_I:
        algorithm_function = algorithm_function_I
    elif estimator == ESTIMATOR_IQ2:
        algorithm_function = algorithm_function_IQ2
    elif estimator == ESTIMATOR_IQ3:
        algorithm_function = algorithm_function_IQ3
    elif estimator == ESTIMATOR_EM_WEIBULL:
        algorithm_function = algorithm_function_EM_WEIBULL
    elif estimator == ESTIMATOR_EM_LOGNORMAL:
        algorithm_function = algorithm_function_EM_LOGNORMAL
    elif estimator == ESTIMATOR_EM_BEST:
        algorithm_function = algorithm_function_EM_BEST
    elif estimator == ESTIMATOR_NP:
        algorithm_function = algorithm_function_NP
    elif estimator == ESTIMATOR_EMNP:
        algorithm_function = algorithm_function_EMNP

    return algorithm_function


def algorithm_function_CI(parametros_list,df_Stays,distribution):
    #print(ESTIMATOR_CI)
    #parametros_list.append(ESTIMATOR_CI)
    
    # Algoritmo:
    
    # 1. p_WI
    df_W_ICU = []
    df_W_ICU = df_Stays['LOS_P_UCI'][df_Stays.Ind_UCI == 1][df_Stays.Ind_P_UCI == 1].values
    df_W_discharged = []
    df_W_discharged = df_Stays['LOS_H'][df_Stays.Ind_UCI == 0][df_Stays.Cens_H == 0].values
    if (len(df_W_ICU)+len(df_W_discharged)) > 0:
        p_WI = len(df_W_ICU)/(len(df_W_ICU)+len(df_W_discharged))
    else:
        p_WI = 0
    
    
    # 2. LZ distribution
    distribution_Z,parameter_a_Z,parameter_b_Z,parameter_c_Z = fit_stay_distribution(distribution,df_W_ICU,[])
    
    # 3. LX distribution
    distribution_X,parameter_a_X,parameter_b_X,parameter_c_X = fit_stay_distribution(distribution,df_W_discharged,[])
    
    # 4. ISE Z
    if parameter_b_Z == 0:
        ise_Z_estimation = 0
    else:
        if distribution == WEIBULL:
            ise_Z_estimation = integrate.quad(lambda x: (weibull_survival_expression(x,PARAMETER_b_Z,PARAMETER_a_Z) - weibull_survival_expression(x,parameter_b_Z,parameter_a_Z))**2, 0, ISE_T_MAX)[0]
        elif distribution == LOGNORMAL:
            ise_Z_estimation = 0
    
    parametros_list.append(p_WI)
    
    parametros_list.append(distribution_X)
    parametros_list.append(parameter_a_X)
    parametros_list.append(parameter_b_X)
    parametros_list.append(parameter_c_X)
    
    parametros_list.append(distribution_Z)
    parametros_list.append(parameter_a_Z)
    parametros_list.append(parameter_b_Z)
    parametros_list.append(parameter_c_Z)
    
    parametros_list.append(ise_Z_estimation)
    
    
    return parametros_list

def algorithm_function_I(parametros_list,df_Stays,distribution):
    #print(ESTIMATOR_I)
    #parametros_list.append(ESTIMATOR_I)
    
    # Algoritmo:
    
    # 1. p_WI
    df_W_ICU = []
    df_W_ICU = df_Stays['LOS_P_UCI'][df_Stays.Ind_UCI == 1][df_Stays.Ind_P_UCI == 1].values
    df_W_discharged = []
    df_W_discharged = df_Stays['LOS_H'][df_Stays.Ind_UCI == 0][df_Stays.Cens_H == 0].values
    df_W_censored = []
    df_W_censored = df_Stays['LOS_H'][df_Stays.Ind_UCI == 0][df_Stays.Cens_H == 1].values
    
    if (len(df_W_ICU)+len(df_W_discharged)+len(df_W_censored)) > 0:
        p_WI = len(df_W_ICU)/(len(df_W_ICU)+len(df_W_discharged)+len(df_W_censored))
    else:
        p_WI = 0
    
    
    # 2. LZ distribution
    distribution_Z,parameter_a_Z,parameter_b_Z,parameter_c_Z = fit_stay_distribution(distribution,df_W_ICU,[])
    
    # 3. LX distribution
    distribution_X,parameter_a_X,parameter_b_X,parameter_c_X = fit_stay_distribution(distribution,df_W_discharged,df_W_censored)
    
    # 4. ISE Z
    if parameter_b_Z == 0:
        ise_Z_estimation = 0
    else:
        if distribution == WEIBULL:
            ise_Z_estimation = integrate.quad(lambda x: (weibull_survival_expression(x,PARAMETER_b_Z,PARAMETER_a_Z) - weibull_survival_expression(x,parameter_b_Z,parameter_a_Z))**2, 0, ISE_T_MAX)[0]
        elif distribution == LOGNORMAL:
            ise_Z_estimation = 0
    
    parametros_list.append(p_WI)
    
    parametros_list.append(distribution_X)
    parametros_list.append(parameter_a_X)
    parametros_list.append(parameter_b_X)
    parametros_list.append(parameter_c_X)
    
    parametros_list.append(distribution_Z)
    parametros_list.append(parameter_a_Z)
    parametros_list.append(parameter_b_Z)
    parametros_list.append(parameter_c_Z)
    
    parametros_list.append(ise_Z_estimation)
    
    
    return parametros_list

def algorithm_function_IQ(parametros_list,df_Stays,Q,distribution):
    df_W_ICU = []
    df_W_ICU = df_Stays['LOS_P_UCI'][df_Stays.Ind_UCI == 1][df_Stays.Ind_P_UCI == 1].values
    distribution_Z0,parameter_a_Z0,parameter_b_Z0,parameter_c_Z0 = fit_stay_distribution(distribution,df_W_ICU,[])
    if distribution_Z0 == WEIBULL:
        d = weibull_min.ppf(Q,parameter_a_Z0,loc=0,scale=parameter_b_Z0)
    elif distribution_Z0 == LOGNORMAL:
        d = lognorm.ppf(Q,parameter_b_Z0,loc=0,scale=np.exp(parameter_a_Z0))
    else:
        d = 0
    if parametros_list[0] > d:
        df_Stays = df_Stays[(df_Stays['date_HA'] <= (parametros_list[0]-d))]
    df_Stays = df_Stays.reset_index(drop=True)
    
    parametros_list = algorithm_function_I(parametros_list,df_Stays,distribution)
    
    
    return(parametros_list)


def algorithm_function_IQ2(parametros_list,df_Stays,distribution):
    #print(ESTIMATOR_IQ2)
    #parametros_list.append(ESTIMATOR_IQ2)
    
    parametros_list = algorithm_function_IQ(parametros_list,df_Stays,Q2,distribution)
    
    return parametros_list
    
def algorithm_function_IQ3(parametros_list,df_Stays,distribution):
    #print(ESTIMATOR_IQ3)
    #parametros_list.append(ESTIMATOR_IQ3)
    
    parametros_list = algorithm_function_IQ(parametros_list,df_Stays,Q3,distribution)
    
    return parametros_list
    
def algorithm_function_EM(parametros_list,df_Stays,fit_distribution,initialization_parameters):
    # Algoritmo:
    
    p_WI_list = []
    parameter_a_X_list = []
    parameter_b_X_list = []
    parameter_c_X_list = []
    parameter_a_Z_list = []
    parameter_b_Z_list = []
    parameter_c_Z_list = []
    
    p_WI = initialization_parameters[POSITION_P_WI]
    distribucion_X = initialization_parameters[POSITION_DISTRIBUTION_X]
    parameter_a_X = initialization_parameters[POSITION_A_X]
    parameter_b_X = initialization_parameters[POSITION_B_X]
    parameter_c_X = initialization_parameters[POSITION_C_X]
    distribucion_Z = initialization_parameters[POSITION_DISTRIBUTION_Z]
    parameter_a_Z = initialization_parameters[POSITION_A_Z]
    parameter_b_Z = initialization_parameters[POSITION_B_Z]
    parameter_c_Z = initialization_parameters[POSITION_C_Z]
    
    p_WI_list.append(p_WI)
    parameter_a_X_list.append(parameter_a_X)
    parameter_b_X_list.append(parameter_b_X)
    parameter_c_X_list.append(parameter_c_X)
    parameter_a_Z_list.append(parameter_a_Z)
    parameter_b_Z_list.append(parameter_b_Z)
    parameter_c_Z_list.append(parameter_c_Z)
    
    
    epsilon_p_WI = 1
    epsilon_a_X = 1
    epsilon_b_X = 1
    epsilon_c_X = 1
    epsilon_a_Z = 1
    epsilon_b_Z = 1
    epsilon_c_Z = 1
    
    lista_epsilon = [epsilon_p_WI,
                     epsilon_a_X,
                     epsilon_b_X,
                     epsilon_c_X,
                     epsilon_a_Z,
                     epsilon_b_Z,
                     epsilon_c_Z]
    
    iteracion = 0
    # Se repite el bucle
    while (max(lista_epsilon) > 0.01 and iteracion < 50) or (max(lista_epsilon) > 0 and iteracion < 10):
        #print(f'Epsilon_maximo: {max(lista_epsilon)}')
        iteracion += 1
        #print(iteracion)
        # 4.
        #print('# 4')
        limite_para_considerar_censura_acumulada = 0
        lista_valores_censurados = []
        lista_probabilidad_UCI = []
        for i in range(len(df_Stays)):
            if df_Stays.loc[i, 'Ind_UCI'] == 0 and df_Stays.loc[i, 'Cens_H'] == 1:
                estancia = df_Stays.loc[i, 'LOS_H']
                lista_valores_censurados.append(estancia)
                p_Z = 0
                if distribucion_Z == "Weibull":
                    p_Z = 1 - weibull_min.cdf(estancia,parameter_a_Z,loc=0,scale=parameter_b_Z)
                elif distribucion_Z == "Lognormal":
                    p_Z = 1 - lognorm.cdf(estancia,parameter_b_Z,loc=0,scale=np.exp(parameter_a_Z))
                
                p_X = 0
                if distribucion_X == "Weibull":
                    p_X = 1 - weibull_min.cdf(estancia,parameter_a_X,loc=0,scale=parameter_b_X)
                elif distribucion_X == "Lognormal":
                    p_X = 1 - lognorm.cdf(estancia,parameter_b_X,loc=0,scale=np.exp(parameter_a_X))
                
                if (p_Z*p_WI+p_X*(1-p_WI)) > 0:
                    limite_para_considerar_censura = p_Z*p_WI/(p_Z*p_WI+p_X*(1-p_WI)) #  Ecuación 10 del artículo de la CJOR.
                else:
                    limite_para_considerar_censura = 0
                
                lista_probabilidad_UCI.append(limite_para_considerar_censura)
                limite_para_considerar_censura_acumulada = limite_para_considerar_censura_acumulada + limite_para_considerar_censura
                
       
        
        # 5.
        #print('# 5')
        df_P_UCI = []
        df_P_UCI = df_Stays[df_Stays.Ind_P_UCI == 1]
        df_UCI_directo = []
        df_UCI_directo = df_Stays[df_Stays.Ind_UCI == 1][df_Stays.Ind_P_UCI == 0]
        if (len(df_Stays)-len(df_UCI_directo)) > 0:
            p_WI = (len(df_P_UCI)+limite_para_considerar_censura_acumulada)/(len(df_Stays)-len(df_UCI_directo))
        else:
            p_WI = 0
    
    
        p_WI_list.append(p_WI)
        
        # 6.
        #print('# 6')
        datos_failure_LOS_H_inicial = df_Stays['LOS_H'][df_Stays.Cens_H == 0][df_Stays.Ind_UCI == 0][df_Stays.Ind_P_UCI == 0].values
        if(len(datos_failure_LOS_H_inicial)>(1)):
            numero_datos_LOS_H = len(datos_failure_LOS_H_inicial) + len(lista_valores_censurados)
            #print(numero_datos_LOS_H)
            multiplicador_LOS_H = int(round(1000000/numero_datos_LOS_H))
            #print('# 6.1')
            datos_failure_LOS_H = []
            for dato in datos_failure_LOS_H_inicial:
                for i in range(multiplicador_LOS_H):
                    datos_failure_LOS_H.append(dato)
            datos_censored_LOS_H = []
            for dato,probabilidad_UCI in zip(lista_valores_censurados,lista_probabilidad_UCI):
                repeticiones = int(round((1-probabilidad_UCI)*multiplicador_LOS_H))
                for i in range(repeticiones):
                    datos_censored_LOS_H.append(dato)         
            
            #print('# 6.2')
            ajuste = True
            if fit_distribution == WEIBULL:
                wbf_X_AICc = 0
                lnf_X_AICc = 1
            elif fit_distribution == LOGNORMAL:
                wbf_X_AICc = 1
                lnf_X_AICc = 0
            elif fit_distribution == BEST:
                ajuste = False
                wbf_X = Fit_Weibull_2P(failures=datos_failure_LOS_H, right_censored=datos_censored_LOS_H, show_probability_plot=False, print_results=False)  # fit the Weibull_2P distribution
                lnf_X = Fit_Lognormal_2P(failures=datos_failure_LOS_H, right_censored=datos_censored_LOS_H, show_probability_plot=False, print_results=False)  # fit the Lognormal_2P distribution
                wbf_X_AICc = wbf_X.AICc
                lnf_X_AICc = lnf_X.AICc
                
            if wbf_X_AICc < lnf_X_AICc:
                if ajuste:
                    wbf_X = Fit_Weibull_2P(failures=datos_failure_LOS_H, right_censored=datos_censored_LOS_H, show_probability_plot=False, print_results=False)  # fit the Weibull_2P distribution
                distribution_X = "Weibull"
                parameter_a_X = wbf_X.beta
                parameter_b_X = wbf_X.alpha
                parameter_c_X = parameter_b_X*math.gamma(1+1/parameter_a_X)
            else:
                if ajuste:
                    lnf_X = Fit_Lognormal_2P(failures=datos_failure_LOS_H, right_censored=datos_censored_LOS_H, show_probability_plot=False, print_results=False)  # fit the Lognormal_2P distribution
                distribution_X = "Lognormal"
                parameter_a_X = lnf_X.mu
                parameter_b_X = lnf_X.sigma
                parameter_c_X = np.exp(parameter_a_X+parameter_b_X**2/2)   
        else:
            distribution_X = "None"
            parameter_a_X = 0
            parameter_b_X = 0
            parameter_c_X = 0
        
        
        parameter_a_X_list.append(parameter_a_X)
        parameter_b_X_list.append(parameter_b_X)
        parameter_c_X_list.append(parameter_c_X)    
        
        # 7.
        #print('# 7')
        datos_failure_LOS_P_UCI_inicial = df_Stays['LOS_P_UCI'][df_Stays.Ind_UCI == 1][df_Stays.Ind_P_UCI == 1].values
        if(len(datos_failure_LOS_P_UCI_inicial)>(1)):
            numero_datos_LOS_P_UCI = len(datos_failure_LOS_P_UCI_inicial) + len(lista_valores_censurados)
            #print(numero_datos_LOS_P_UCI)
            multiplicador_LOS_P_UCI = int(round(1000000/numero_datos_LOS_P_UCI))
            #print('# 7.1')
            datos_failure_LOS_P_UCI = []
            for dato in datos_failure_LOS_P_UCI_inicial:
                for i in range(multiplicador_LOS_P_UCI):
                    datos_failure_LOS_P_UCI.append(dato)
            datos_censored_LOS_P_UCI = []
            for dato,probabilidad_UCI in zip(lista_valores_censurados,lista_probabilidad_UCI):
                repeticiones = int(round(probabilidad_UCI*multiplicador_LOS_P_UCI))
                for i in range(repeticiones):
                    datos_censored_LOS_P_UCI.append(dato)

            #print('# 7.2')
            ajuste = True
            if fit_distribution == WEIBULL:
                wbf_Z_AICc = 0
                lnf_Z_AICc = 1
            elif fit_distribution == LOGNORMAL:
                wbf_Z_AICc = 1
                lnf_Z_AICc = 0
            elif fit_distribution == BEST:
                ajuste = False
                wbf_Z = Fit_Weibull_2P(failures=datos_failure_LOS_P_UCI, right_censored=datos_censored_LOS_P_UCI, show_probability_plot=False, print_results=False)  # fit the Weibull_2P distribution
                lnf_Z = Fit_Lognormal_2P(failures=datos_failure_LOS_P_UCI, right_censored=datos_censored_LOS_P_UCI, show_probability_plot=False, print_results=False)  # fit the Lognormal_2P distribution
                wbf_Z_AICc = wbf_Z.AICc
                lnf_Z_AICc = lnf_Z.AICc
                
            if wbf_Z_AICc < lnf_Z_AICc:
                if ajuste:
                    wbf_Z = Fit_Weibull_2P(failures=datos_failure_LOS_P_UCI, right_censored=datos_censored_LOS_P_UCI, show_probability_plot=False, print_results=False)  # fit the Weibull_2P distribution
                distribution_Z = "Weibull"
                parameter_a_Z = wbf_Z.beta
                parameter_b_Z = wbf_Z.alpha
                parameter_c_Z = parameter_b_Z*math.gamma(1+1/parameter_a_Z)
            else:
                if ajuste:
                    lnf_Z = Fit_Lognormal_2P(failures=datos_failure_LOS_P_UCI, right_censored=datos_censored_LOS_P_UCI, show_probability_plot=False, print_results=False)  # fit the Lognormal_2P distribution
                distribution_Z = "Lognormal"
                parameter_a_Z = lnf_Z.mu
                parameter_b_Z = lnf_Z.sigma
                parameter_c_Z = np.exp(parameter_a_Z+parameter_b_Z**2/2)   
        else:
            distribution_Z = "None"
            parameter_a_Z = 0
            parameter_b_Z = 0
            parameter_c_Z = 0
        
        
        parameter_a_Z_list.append(parameter_a_Z)
        parameter_b_Z_list.append(parameter_b_Z)
        parameter_c_Z_list.append(parameter_c_Z)


        # 7. Criterio de parada
        
        if p_WI_list[-1] > 0:
            epsilon_p_WI = abs(p_WI_list[-1]-p_WI_list[-2])/p_WI_list[-1]
        else:
            epsilon_p_WI = 0
        if parameter_a_X_list[-1] > 0:
            epsilon_a_X = abs(parameter_a_X_list[-1]-parameter_a_X_list[-2])/parameter_a_X_list[-1]
        else:
            epsilon_a_X = 0
        if parameter_b_X_list[-1] > 0:
            epsilon_b_X = abs(parameter_b_X_list[-1]-parameter_b_X_list[-2])/parameter_b_X_list[-1]
        else:
            epsilon_b_X = 0
        if parameter_c_X_list[-1] > 0:
            epsilon_c_X = abs(parameter_c_X_list[-1]-parameter_c_X_list[-2])/parameter_c_X_list[-1]
        else:
            epsilon_c_X = 0
        if parameter_a_Z_list[-1] > 0:
            epsilon_a_Z = abs(parameter_a_Z_list[-1]-parameter_a_Z_list[-2])/parameter_a_Z_list[-1]
        else:
            epsilon_a_Z = 0
        if parameter_b_Z_list[-1] > 0:
            epsilon_b_Z = abs(parameter_b_Z_list[-1]-parameter_b_Z_list[-2])/parameter_b_Z_list[-1]
        else:
            epsilon_b_Z = 0
        if parameter_c_Z_list[-1] > 0:
            epsilon_c_Z = abs(parameter_c_Z_list[-1]-parameter_c_Z_list[-2])/parameter_c_Z_list[-1]
        else:
            epsilon_c_Z = 0
        
        
        
        
        
        
        
        lista_epsilon = [epsilon_p_WI,
                         epsilon_a_X,
                         epsilon_b_X,
                         epsilon_c_X,
                         epsilon_a_Z,
                         epsilon_b_Z,
                         epsilon_c_Z]
    
    
    
        
    #print(f'Iteraciones: {iteracion}')        
    
    # 4. ISE Z
    if parameter_b_Z_list[-1] == 0:
        ise_Z_estimation = 0
    else:
        if distribucion_Z == WEIBULL:
            ise_Z_estimation = integrate.quad(lambda x: (weibull_survival_expression(x,PARAMETER_b_Z,PARAMETER_a_Z) - weibull_survival_expression(x,parameter_b_Z_list[-1],parameter_a_Z_list[-1]))**2, 0, ISE_T_MAX)[0]
        elif distribucion_Z == LOGNORMAL:
            ise_Z_estimation = 0
    
    parametros_list.append(p_WI_list[-1])
    
    parametros_list.append(distribution_X)
    parametros_list.append(parameter_a_X_list[-1])
    parametros_list.append(parameter_b_X_list[-1])
    parametros_list.append(parameter_c_X_list[-1])
    
    parametros_list.append(distribution_Z)
    parametros_list.append(parameter_a_Z_list[-1])
    parametros_list.append(parameter_b_Z_list[-1])
    parametros_list.append(parameter_c_Z_list[-1])
    
    parametros_list.append(ise_Z_estimation)
    
    
    return parametros_list

def algorithm_function_EM_WEIBULL(parametros_list,df_Stays,distribution):
    #print(ESTIMATOR_EM_WEIBULL)
    #parametros_list.append(ESTIMATOR_EM_WEIBULL)
    
    distribution = "Weibull" 
    
    # Inicialización
    initialization_parameters = [0]
    initialization_parameters = algorithm_function_CI(initialization_parameters,df_Stays,distribution)
        
    parametros_list = algorithm_function_EM(parametros_list,df_Stays,distribution,initialization_parameters)
    
    
    return parametros_list
    
def algorithm_function_EM_LOGNORMAL(parametros_list,df_Stays,distribution):
    #print(ESTIMATOR_EM_LOGNORMAL)
    #parametros_list.append(ESTIMATOR_EM_LOGNORMAL)
    
    distribution = "Lognormal"
    
    # Inicialización
    initialization_parameters = [0]
    initialization_parameters = algorithm_function_CI(initialization_parameters,df_Stays,distribution)
    
    parametros_list = algorithm_function_EM(parametros_list,df_Stays,distribution,initialization_parameters)
    
    
    return parametros_list
    
def algorithm_function_EM_BEST(parametros_list,df_Stays,distribution):
    #print(ESTIMATOR_EM_BEST)
    #parametros_list.append(ESTIMATOR_EM_BEST)
    
    distribution = "Best"  
    
    # Inicialización
    initialization_parameters = [0]
    initialization_parameters = algorithm_function_CI(initialization_parameters,df_Stays,distribution)
    
    parametros_list = algorithm_function_EM(parametros_list,df_Stays,distribution,initialization_parameters)
    
    
    return parametros_list
    
def get_p_WI_sorted_times_and_weights_algorithm_NP(df_Stays):
    # Algoritmo:
    #Separamos los datos para identificar.
    df_W_ICU = []
    df_W_ICU = df_Stays['LOS_P_UCI'][df_Stays.Ind_UCI == 1][df_Stays.Ind_P_UCI == 1].values
    df_W_discharged = []
    df_W_discharged = df_Stays['LOS_H'][df_Stays.Ind_UCI == 0][df_Stays.Cens_H == 0].values
    df_W_censored = []
    df_W_censored = df_Stays['LOS_H'][df_Stays.Ind_UCI == 0][df_Stays.Cens_H == 1].values
    
    # Creamos una lista de tuplas para ordenar los tiempos y los valores d y v asociados.
    lista_tuplas_tiempos_ordenados = []
    for tiempo in df_W_ICU:
        lista_tuplas_tiempos_ordenados.append((tiempo,1,0))
    for tiempo in df_W_discharged:
        lista_tuplas_tiempos_ordenados.append((tiempo,0,1))
    for tiempo in df_W_censored:
        lista_tuplas_tiempos_ordenados.append((tiempo,0,0))
    
    lista_tuplas_tiempos_ordenados.sort(key = lambda x: x[0])
    
    
    
    # p_WI
    n = len(lista_tuplas_tiempos_ordenados)
    if n > 0 and lista_tuplas_tiempos_ordenados[0][1] > 0:
        vector_S = [1-1/n]
    else:
        vector_S = [1]
    
    for i in range(1,n):
        suma_acumulada_v = 0
        for j in range(i):
            suma_acumulada_v += lista_tuplas_tiempos_ordenados[j][2]
        producto = 1 - lista_tuplas_tiempos_ordenados[i][1]/(n-(i+1)+1+suma_acumulada_v)
        vector_S.append(vector_S[-1]*producto)
        
    p_WI = 1 - min(vector_S)
    
    # Estancia media Z.
    if p_WI > 0:
        vector_S0 = []
        for value in vector_S:
            vector_S0.append((value-(1-p_WI))/p_WI)
        
        vector_w = [1-vector_S0[0]]
        for i in range(1,len(vector_S0)):
            vector_w.append(vector_S0[i-1]-vector_S0[i])
        
        mean_stay_ward_ICU = 0
        lista_tiempos_ordenados = []
        for t,w in zip(lista_tuplas_tiempos_ordenados,vector_w):
            lista_tiempos_ordenados.append(t[0])
            mean_stay_ward_ICU += t[0]*w
    else:
        mean_stay_ward_ICU = 0
        lista_tiempos_ordenados = []
        vector_S0 = []
        vector_w = []
    
    return p_WI,mean_stay_ward_ICU,lista_tiempos_ordenados,vector_S0,vector_w

def algorithm_function_NP(parametros_list,df_Stays,distribution):
    #print(ESTIMATOR_NP)
    #parametros_list.append(ESTIMATOR_NP)
    
    # Algoritmo:        
    p_WI,mean_stay_ward_ICU,lista_tiempos_ordenados,vector_S0,vector_w = get_p_WI_sorted_times_and_weights_algorithm_NP(df_Stays)
    
    distribution_X = "None"
    parameter_a_X = 0
    parameter_b_X = 0
    parameter_c_X = 0
    distribution_Z = "None"
    parameter_a_Z = 0
    parameter_b_Z = 0
    parameter_c_Z = mean_stay_ward_ICU
    
    if len(vector_S0) > 0:
        ise_Z_estimation = calculate_ISE_method_NP(lista_tiempos_ordenados,vector_S0,distribution)
    else:
        ise_Z_estimation = 0
    
    parametros_list.append(p_WI)
    
    parametros_list.append(distribution_X)
    parametros_list.append(parameter_a_X)
    parametros_list.append(parameter_b_X)
    parametros_list.append(parameter_c_X)
    
    parametros_list.append(distribution_Z)
    parametros_list.append(parameter_a_Z)
    parametros_list.append(parameter_b_Z)
    parametros_list.append(parameter_c_Z)
    
    parametros_list.append(ise_Z_estimation)
    
    
    return parametros_list
    
def algorithm_function_EMNP(parametros_list,df_Stays,distribution):
    #print(ESTIMATOR_EMNP)
    #parametros_list.append(ESTIMATOR_EMNP)
    
        
    # Inicialización
    initialization_parameters_NP = [0]
    initialization_parameters_NP = algorithm_function_NP(initialization_parameters_NP,df_Stays,distribution)
    
    initialization_parameters = [0]
    initialization_parameters = algorithm_function_CI(initialization_parameters,df_Stays,distribution)
    
    distribucion_Z = initialization_parameters[POSITION_DISTRIBUTION_Z]
    parameter_a_Z = initialization_parameters[POSITION_A_Z]
    parameter_b_Z = initialization_parameters[POSITION_B_Z]
    parameter_c_Z = initialization_parameters_NP[POSITION_C_Z]
    
    if distribucion_Z == WEIBULL:
        parameter_b_Z = parameter_c_Z/math.gamma(1+1/parameter_a_Z)
    elif distribucion_Z == LOGNORMAL:
        parameter_a_Z = math.log(parameter_c_Z)-parameter_b_Z**2/2
        
    initialization_parameters[POSITION_P_WI] = initialization_parameters_NP[POSITION_P_WI]
    initialization_parameters[POSITION_A_Z] = parameter_a_Z
    initialization_parameters[POSITION_B_Z] = parameter_b_Z
    initialization_parameters[POSITION_C_Z] = parameter_c_Z
    
    parametros_list = algorithm_function_EM(parametros_list,df_Stays,distribution,initialization_parameters)
    
    
    return parametros_list
    

def calculate_ISE_method_NP(x_S0,y_S0,distribution):
    if x_S0[-1] < ISE_T_MAX:
        maximo_rejilla = ISE_T_MAX
        x_S0.append(maximo_rejilla)
        y_S0.append(y_S0[-1])
    else:
        maximo_rejilla = x_S0[-1]
    
    vector_x_rejilla = np.arange(0,(maximo_rejilla+STEP_ISE),STEP_ISE)
    vector_y_S0_rejilla = [1]
    
    ultima_posicion = 0
    adding_value = 1
    for valor_x_S0,valor_y_S0 in zip(x_S0,y_S0):
        for i in range((ultima_posicion+1),len(vector_x_rejilla)):
            if vector_x_rejilla[i] < valor_x_S0:
                vector_y_S0_rejilla.append(adding_value)
            else:            
                ultima_posicion = i
                adding_value = valor_y_S0
                vector_y_S0_rejilla.append(adding_value)
                break
        
    
    if distribution == WEIBULL:
        vector_y_real_rejilla = weibull_survival_expression(vector_x_rejilla,PARAMETER_b_Z,PARAMETER_a_Z)
    elif distribucion_Z == LOGNORMAL:
        vector_y_real_rejilla = []
        for value in vector_x_rejilla:
            vector_y_real_rejilla.append(0)
    
    vector_diferencias_cuadrado = (vector_y_real_rejilla-vector_y_S0_rejilla)**2
    
    
    # The y values.  It can be numpy array but a python list could also be used.
    # Compute the area using the composite Simpson's rule.
    ise_estimated = integrate.simps(vector_diferencias_cuadrado, dx=STEP_ISE)
    
    
    return ise_estimated



def generate_real_value_of_parameter(parameter):
    if parameter == KEY_P_WI:
        real_value = P_WI
    elif parameter == KEY_A_X:
        real_value = PARAMETER_a_X
    elif parameter == KEY_B_X:
        real_value = PARAMETER_b_X
    elif parameter == KEY_C_X:
        real_value = PARAMETER_c_X
    elif parameter == KEY_A_Z:
        real_value = PARAMETER_a_Z
    elif parameter == KEY_A_X:
        real_value = PARAMETER_a_X
    elif parameter == KEY_B_Z:
        real_value = PARAMETER_b_Z
    elif parameter == KEY_C_Z:
        real_value = PARAMETER_c_Z
    elif parameter == KEY_ISE_Z:
        real_value = ISE_Z
    
    return real_value


def generate_real_values_list(parameter):
    real_value = generate_real_value_of_parameter(parameter)
    real_value_list = [real_value]*ESTIMATION_DAYS
    
    return real_value_list
               


def graph_estimation_in_pairs(day,parameter,x_vector,y_vector,x_label,y_label):
    real_value = generate_real_value_of_parameter(parameter)
    
    
    def restar_valor(n):
        return n-real_value
    
# =============================================================================
#     x_values = list(map(restar_valor,x_vector))
#     y_values = list(map(restar_valor,y_vector))
# =============================================================================
    
    x_values = x_vector
    y_values = y_vector
    
    fig, ax = plt.subplots(figsize=(10,6))
    plt.grid()
    
    ax.scatter(x_values,
        y_values,
        label= f'{x_label} VS {y_label}',
        color= 'b')
    ax.scatter(real_value,
        real_value,
        label= parameter,
        color= 'r')
    
    
    
    plt.title(f'{parameter},{day}: {x_label} VS {y_label}')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    
    plt.legend()
    plt.show()


def draw_boxplot(lista_estimadores,dictionary_simulation_results,key_label,day,descartar_R):
    lista_arrays_box_plot = []
    for estimator in lista_estimadores:
        if descartar_R:
            if estimator == R:
                lista_estimadores = ESTIMATOR_LIST
                continue
        lista_arrays_box_plot.append(dictionary_simulation_results[f'{day}'][estimator][key_label])
    
    # Dibujamos un boxplot
    fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(12, 4))
    
    # rectangular box plot
    bplot = ax1.boxplot(lista_arrays_box_plot,
                         vert=True,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=lista_estimadores)  # will be used to label x-ticks
    ax1.set_title(f'{day}th day')
    
    
    
    # fill with colors
    for patch, estimator in zip(bplot['boxes'], lista_estimadores):
        patch.set_facecolor(DICTIONARY_COLORS[estimator][KEY_COLOR])
    
    # adding horizontal grid lines
    ax1.yaxis.grid(True)
    ax1.set_xlabel('Estimator')
    #ax1.set_ylabel(f'{key_label}')
    ax1.set_ylabel(f'Est. err. day')
    ax1.set_ylim(-20,20)
    
    plt.show()
    
    
    
    