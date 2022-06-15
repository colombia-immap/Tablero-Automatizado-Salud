# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 12:04:26 2022

@author: Lisa
"""

import os
import pandas as pd
import numpy as np


# Selección de directorio
os.chdir("C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/Ciclo3/")

df_5w  = pd.read_excel("C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/Ciclo3/5W_Colombia_-_RMRP_2022_Consolidado tres_25052022 (1).xlsx")

#agrego una nueva columna concatenando departamento y municipio
df_5w["Full Name"] = df_5w["Admin Departamento"] + df_5w["Admin Municipio"]

df_5w['Mes de atención'].unique()

df_5w['Sector'].unique()

mes = ['04_Abril']
sector = ['Salud']

df_5w.columns 
#con la que trabajaré apartir de ahora 
df_5w_sector_mes = df_5w[(df_5w['Sector'].isin(sector))&(df_5w['Mes de atención'].isin(mes))]

#Otro Formato
#df_5w_sector_mes2 = df_5w[(df_5w['_ Sector']=='Educación')&(df_5w['Mes de atención'] == '03_Marzo')]

#Cargo api
df_api_ind_mpio  = pd.read_excel("C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/Ciclo3/API_Consolidado_ciclo_TRES_ GENERAL_27052022 (2).xlsx", sheet_name= "Indicador y Municipio")
df_api_sect_nac  = pd.read_excel("C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/Ciclo3/API_Consolidado_ciclo_TRES_ GENERAL_27052022 (2).xlsx", sheet_name= "Sector Nacional")
df_api_ind_mpio["Full Name"] = df_api_ind_mpio["Departamento"] + df_api_ind_mpio["Municipio"]

df_api_sector_mes = df_api_ind_mpio[(df_api_ind_mpio['Sector'].isin(sector))&(df_api_ind_mpio['Mesdeatención'].isin(mes))]
df_api_sect_nac = df_api_sect_nac[(df_api_sect_nac['Sector'].isin(sector))&(df_api_sect_nac['Mesdeatención'].isin(mes))]
#df_api_sector_mes2 = df_api_ind_mpio[(df_api_ind_mpio['Sector']=='Educación')&(df_api_ind_mpio['Mesdeatención'] == '03_Marzo')]


#divipola

divipola = pd.read_excel("C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/divipolita.xlsx")

#agrego una nueva columna concatenando departamento y municipio
divipola["Full Name"] = divipola["Departamento"] + divipola["Municipio"]
divipola["Full Name"] = divipola["Full Name"].drop_duplicates()


def standardize_territories(column):
    column = column.str.replace("_"," ", regex=True)
    column = column.map(lambda x: x.lower())
    column = column.map(lambda x: x.strip())
    column = column.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    column = column.str.replace(r'[^\w\s]+', '', regex=True)
    column = column.str.replace("narinotumaco","narinosan andres de tumaco", regex=True)
    return column


# Estandarizando nombres de departamentos ...
df_5w_sector_mes['Full Name'] = standardize_territories(df_5w_sector_mes['Full Name'])
df_api_sector_mes['Full Name'] = standardize_territories(df_api_sector_mes['Full Name'])
divipola['Full Name'] = standardize_territories(divipola['Full Name'])


#prueba = df_5w_sector_mes['Full Name'].sort_values()

#prueba1 = divipola['Full Name'].sort_values()

# Adicionar el divipola más adecuado
df_5w_sector_mes = pd.merge(df_5w_sector_mes, divipola, how= 'left', left_on = 'Full Name',
                 right_on = 'Full Name')

if df_5w_sector_mes['Full Name'].isna().sum() > 1:
    print('Ajustar full name')
    
if df_5w_sector_mes['dpto'].isna().sum() > 1:
    print('Ajustar Divipola dpto')
    
if df_5w_sector_mes['mpio'].isna().sum() > 1:
    print('Ajustar Divipola mpio')



# Adicionar el divipola más adecuado
df_api_sector_mes = pd.merge(df_api_sector_mes, divipola, how= 'left', left_on = 'Full Name',
                 right_on = 'Full Name')


if df_api_sector_mes['Full Name'].isna().sum() > 1:
    print('Ajustar full name')
    
if df_api_sector_mes['dpto'].isna().sum() > 1:
    print('Ajustar Divipola dpto')
    
if df_api_sector_mes['mpio'].isna().sum() > 1:
    print('Ajustar Divipola mpio')
    

df_api_sector_mes.columns

#df_api_sector_mes['col_a_b'] = df_api_sector_mes['Departamento_x'] + ' - ' +df_api_sector_mes['Municipio_x']


### tablas dinamicas

#Cifras claves 

Pobla_respuesta_rmrp = "2007580 (2M)"
reque_finan = "154.101.329 (154M) USD"

#obtengo el dato "Beneficiarios recibieron una o más asistencias por parte del SECTOR SALUD" todos, 
benef_mes = round(df_api_sector_mes['bene_mensuales'].sum())

#definir el nro de Departamentos
no_dpto= df_api_sector_mes['Departamento_x'].nunique()
depa = df_api_sector_mes['dpto'].unique()

#definir nro de Municipios alcanzados
#df_api_sector_mes.columns
no_mpio = df_api_sector_mes['Full Name'].nunique()          #Muni y no_mpio deben ser el mismo numero
muni = df_api_sector_mes.drop_duplicates(['Full Name']).reset_index(drop=True)
muni = muni[['Full Name','mpio']]

#indicadores
df_api_sector_mes.columns

ind1=df_api_sector_mes.loc[df_api_sector_mes['Indicador'] == 'Número de refugiados y migrantes beneficiándose de consultas de atención primaria de salud',  'bene_mensuales'].sum()
ind2=df_api_sector_mes.loc[df_api_sector_mes['Indicador'] == 'Número de dosis de vacunas administradas a los refugiados y migrantes de Venezuela según ciclo de vida y calendario nacional', 'bene_mensuales'].sum()
ind3=df_api_sector_mes.loc[df_api_sector_mes['Indicador'] == 'Número de refugiados y migrantes de Venezuela que recibieron insumos', 'bene_mensuales'].sum()

#definir nro de organizaciones que reportaron

no_org=df_5w_sector_mes['Socio Principal Nombre'].nunique()

#definir nro de IMPLEMENTADORES
no_imple=df_5w_sector_mes['Socio Implementador Nombre'].nunique()

#crear un nuevo dataframe con las variables calculadas, para introducir luego otra hoja de excel con ellas. 
cifras_clave= pd.DataFrame([{'Cifras':benef_mes, 'Indicador': 'Número de Beneficiarios recibieron una o más asistencias por parte del SECTOR SALUD-BENEFICIARIOS Mensual'},
                            {'Cifras':Pobla_respuesta_rmrp, 'Indicador':'poblacion respuesta del rmrp'}, 
                            {'Cifras':reque_finan, 'Indicador':'Requerimientos financieros para el sector Salud en Colombia en 2022'}, 
                            {'Cifras':no_dpto, 'Indicador':'nro de Departamentos'},
                            {'Cifras':no_mpio, 'Indicador':'nro de Municipios alcanzados'},
                            {'Cifras':no_org, 'Indicador':'nro de organizaciones que reportaron'},
                            {'Cifras':no_imple, 'Indicador':'nro de implementadores'},
                            {'Cifras':ind1, 'Indicador':'Número de refugiados y migrantes beneficiándose de consultas de atención primaria de salud'},
                            {'Cifras':ind2, 'Indicador':'Número de dosis de vacunas administradas a los refugiados y migrantes de Venezuela según ciclo de vida y calendario nacional'},
                            {'Cifras':ind3, 'Indicador':'Número de refugiados y migrantes de Venezuela que recibieron insumos'}, 
                            #{'Cifras':ind4, 'Indicador':'# de refugiados y migrantes de Venezuela o comunidades de acogida asistidos con consultas de salud de emergencia, incluso sobre COVID-19, atención del parto y del recién nacido'}, 
                           ],
                            columns=['Cifras', 'Indicador'])

#cifras_clave.head(20)


socios= df_5w_sector_mes[["Socio Principal Nombre","Socio Implementador Nombre"]]
socios = socios.replace(np.nan, '', regex=True)
socios = socios.pivot_table(index=["Socio Principal Nombre","Socio Implementador Nombre"])

Objetivos = ["Mejorar el acceso a los servicios y suministros de salud en todos los niveles de atención incluida la asistencia especializada", 
             "Fortalecer los marcos internacionales y nacionales que aseguren una mayor protección de la salud",
             "Mejorar el acceso a los servicios y suministros de salud en todos los niveles de atención incluida la asistencia especializada"]


Objetivos = pd.DataFrame(Objetivos, columns= ["Objetivos"])


#nuevamente pego las columnas basandome en el sector mes y genero unas tablas dinamicas
right_join = df_api_sector_mes 
right_join.nunique()
right_join= right_join[['Full Name','dpto','mpio','Departamento_x', 'Municipio_x']]
Municipios_Alcanzados = pd.pivot_table(right_join,index=['Full Name','dpto','mpio','Departamento_x', 'Municipio_x']).reset_index()
Municipios_Alcanzados.index = Municipios_Alcanzados.index + 1

right2_join = df_5w_sector_mes
right2_join.columns
right2_join = right2_join[['Full Name','dpto','mpio','Admin Departamento', 'Admin Municipio','Socio Principal Nombre']]
right2_join["mpio"] = right2_join["mpio"].astype('Int64')
right2_join["dpto"] = right2_join["dpto"].astype('Int64')
#sociosxmun = right2_join.pivot_table(index=['Full Name','dpto','mpio','Admin Departamento', 'Admin Municipio','Socio Principal Nombre'])
sociosxmun = pd.pivot_table(right2_join,index=['Full Name','dpto','mpio','Admin Departamento', 'Admin Municipio','Socio Principal Nombre']).reset_index()

sociosxmun.columns
sociosxmun = sociosxmun.assign(result=sociosxmun['mpio'].isin(muni['mpio']).astype(int))
sociosxmun.drop(sociosxmun[sociosxmun['result'] == 0].index, inplace = True)
sociosxmun["Numero"] = (sociosxmun.mpio.diff() != 0).cumsum()
sociosxmun = sociosxmun.set_index('Numero')
#sociosxmun = sociosxmun[["Numero",'dpto','mpio','Admin Departamento', 'Admin Municipio','Socio Principal Nombre']]
nsocioxmun = sociosxmun['mpio'].nunique()

if (nsocioxmun != no_mpio) :
    print("el numero de municipios no es igual, ERROR")
else: 
    print("son iguales")
    

Writer= pd.ExcelWriter("C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/tablero_Salud_04_2022.xlsx")

cifras_clave.to_excel(Writer, sheet_name='Cifras Clave.xlsx')
Objetivos.to_excel(Writer, sheet_name='Objetivos.xlsx')
Municipios_Alcanzados.to_excel(Writer, sheet_name='Municipios_Alcanzados.xlsx')
sociosxmun.to_excel(Writer, sheet_name='Socios_por_Municipio.xlsx')
socios.to_excel(Writer, sheet_name='Socios.xlsx')


Writer.save()
