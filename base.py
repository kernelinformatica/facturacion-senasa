import requests
import json
import pandas as pd

response = ""
testing = "S"
if testing == "S":
    modo = "test"
else:
    modo = "aps2"
# URL del webservice de SENASA para la obtención de provincias
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Obtener_Provincia'
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Consulta_Tipo_Envase'
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Consulta_Material_Envase'
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Obtener_Partido'
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Obtener_Localidad'
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Consulta_Deposito'
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Consulta_Productos'
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Consulta_Estados_Deposito'
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Consulta_Planta_Nacional'

urlProductoFormulado = 'https://' + modo + '.senasa.gov.ar/agrotraza/src/api/Consulta_Producto_Formulado'
urlProductoFormuladoTotal = 'https://' + modo + '.senasa.gov.ar/agrotraza/src/api/Consulta_Producto_Formulado_Total'
urlDeposito = 'https://' + modo + '.senasa.gov.ar/agrotraza/src/api/Consulta_Stock_Producto_Formulado'
urlAltaEnvio = 'https://' + modo + '.senasa.gov.ar/agrotraza/src/api/Alta_Envio'

# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Consulta_Ingrediente_Activo'
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Consulta_Tipo_Formulacion'
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Consulta_Clase_Toxicologica'
# url = 'https://test.senasa.gov.ar/agrotraza/src/api/Consulta_Aptitud_Uso'
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Obtener_Pais'
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Consulta_Planta_Extranjera'
# url = 'https://aps2.senasa.gov.ar/agrotraza/src/api/Consulta_Unidad_Medida'

# urla = 'https://test.senasa.gov.ar/agrotraza/src/api/Alta_Autoconsumo_FP'
# Parámetros de la solicitud
# cuit de arnoldin 20250433922
# cuit de andres 20178257855
# cuit de andres 20178257855
# jose 20-35296905-3
cuitAndres = '20178257855'
cuitJose = '20352969053'
cuitCoopar = '30534003761'
# Romang
# Usuario : uarcoop
# Contraseña Uar2022
# Cuit : 20-27838405-6
# consulto deposito
params_base = {
    'authUser': 'Coopartr',
    'authPass': 'H4g90kmh7',
    'userTaxId': '20-35296905-3',
    'cuit': '30-53400376-1'
}
# DEPOSITO 2439 = 4911, 25818, 11496,
params_stock_depo = {
    'authUser': 'Coopartr',
    'authPass': 'H4g90kmh7',
    'userTaxId': cuitJose,
    'depositId': '2439',
    'productCodeId': '25818'
}

params_pla = {
    'authUser': 'Coopartr',
    'authPass': 'H4g90kmh7',
    'userTaxId': '20-17825785-5',
    'CompanyTax': '30-53400376-1',
    'RegSenasa': '0',
    'brand': '',
    'formulationId': '0',
    'toxicologicalClassId': '0'
}

params_envio_deta = {
    'actives[0][id]': '175267',
    'actives[0][batchid]': '01-25',
    'actives[0][amount]': '1',
    'products[0][id_product_code]': '8997',
    'products[0][batchid]': '04-25',
    'products[0][amount]': '2'
}

params_consumo = {
    'authUser': 'Coopartr',
    'authPass': 'H4g90kmh7',
    'userTaxId': '20178257855',
    'depositId': '2349',
    'consumptionDate': '02/11/2024',
    'id_product_code': "8718"
}
# 2439 :YX8RGL
# 6949: 5IGA2Q
# cuit coopar = 30-53400376-1
# cuit origin = 20-17825785-5
# userTaxId = 20-17825785-5
# userTaxId = 20-35296905-3 este funca

params_envio = {
    'authUser': 'Coopartr',
    'authPass': 'H4g90kmh7',
    'userTaxId': '20-35296905-3',
    'sendDate': '02/11/2024',
    'senderDepositId': '2439',

    'receiverCompanyCuit': '30-68051398-4',
    'receiverDepositId': '',
    'actives[0][id]': '175267',
    'actives[0][batchid]': '01-25',
    'actives[0][amount]': '1',
    'products[0][id_product_code]': '8997',
    'products[0][batchid]': '04-25',
    'products[0][amount]': '2'

}

params_envio_deta = {
    'actives[0][id]': '175267',
    'actives[0][batchid]': '01-25',
    'actives[0][amount]': '1',
    'products[0][id_product_code]': '8997',
    'products[0][batchid]': '04-25',
    'products[0][amount]': '2'
}

# Realizar la solicitud GET
# response = requests.post(urlAltaEnvio, params=params_envio)
response = requests.get(urlDeposito, params=params_stock_depo)

# Verificar el resultado
if response.status_code == 200:
    # 5IGA2Q

    data_string = response.json()
    df = pd.DataFrame(data_string)
    print(df.to_string())

#    print('Solicitud exitosa:', response.json())


#   print(response)


# urla, params=params_envio)

# Verificar el resultado
if response.status_code == 200:

    data_string = response.json()
    df = pd.DataFrame(data_string)
    print(df.to_string())


#    print('Solicitud exitosa:', response.json())

#   print(response)

else:

    print('Error:', response.status_code, response.text)

