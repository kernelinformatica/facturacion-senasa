import requests
import json
import pandas as pd
import requests
import json
import conn.DBConnection
from datetime import datetime
import sys
argumentos = sys.argv

from conn.DBConnection import DBConnection as DBConnection

from datetime import datetime, timedelta
class SenasaApi(DBConnection):
    def __init__(self):
        super().__init__()

        self.hoy = datetime.now()
        self.maskCuenta = "0000000"
        self.maskNorComp = "0000-00000000"
        self.maskCosecha = "0000"
        self.config = []
        self.paramsConn = {}
        self.params = {}
        self.resp = []
        self.datos=[]
        self.idOperacion=0
        self.wsSenasaUrl = ""

        self.metodosPermitidos = [
            {"metodo": "Alta_Envio", "tipo": "post"},
            {"metodo": "Consulta_Stock_Producto_Formulado", "tipo": "get"},
            {"metodo": "Consulta_Producto_Formulado_Total", "tipo": "get"},
            {"metodo": "Consulta_Producto_Formulado", "tipo": "get"},
            {"metodo": "Consulta_Material_Envase", "tipo": "get"},
            {"metodo": "Consulta_Deposito", "tipo": "get"},
            {"metodo": "Consulta_Productos", "tipo": "get"},
            {"metodo": "Consulta_Estados_Deposito", "tipo": "get"},
            {"metodo": "Consulta_Tipo_Envase", "tipo": "get"},
            {"metodo": "Consulta_Tipo_Formulacion", "tipo": "get"},
            {"metodo": "Consulta_Aptitud_Uso", "tipo": "get"},
            {"metodo": "Consulta_Unidad_Medida", "tipo": "get"},
            {"metodo": "Alta_Autoconsumo_FP", "tipo": "post"}
        ]
        fechaHoraHoyTemp = datetime.now()
        formatoFechaHoy = "%Y-%m-%d %H:%M:%S"
        self.fechaHoraHoy = fechaHoraHoyTemp.strftime(formatoFechaHoy)






    def main(self):
        # argumentos por default
        # 0: nombre del metodo a ejecutar en el web service
        # 1: testingSn
        # 2: idEjecucion


        # 3: idDeposito (segun metodo)
        # 4: idProducto (segun metodo

        if len(argumentos) > 1:
            metodo = argumentos[1]
            testingSn = argumentos[2]
            # argumentos que recibo segun el metodo que ejecuta
            if len(argumentos) > 3:
                self.idOperacion = argumentos[3]
            else:
                self.idOperacion = 0

            # Si se ejecuta 'Consulta_Stock_Producto_Formulado'
            if metodo == str(self.metodosPermitidos[1]["metodo"]):
                # Recibo estos parametros
                if len(argumentos) > 4:
                    idDeposito = argumentos[4]
                else:
                    idDeposito = 0

                if len(argumentos) > 5:
                    idProducto = argumentos[5]
                else:
                    idProducto = 0





            if testingSn is None:
                testingSn = "S"

            print(":: PROCESANDO DATOS... Aguarde! :: ")
            cursor = self.conn.cursor()
            cursor.execute("SELECT parametro_val  FROM senasa_parametros where parametro_id in ('ws_usu', 'ws_pass')")
            parametros = cursor.fetchall()
            etiquetas = ["ws_usuario", "ws_clave"]
            for idx, param in enumerate(parametros):
                self.paramsConn[etiquetas[idx]] = param[0]

            if testingSn == "S":
                val = "ws_url_test"
            else:
                val = "ws_url_prod"
            cursor.execute("SELECT parametro_val  FROM senasa_parametros where parametro_id = ?", (val, ))
            resp = cursor.fetchone()
            self.wsSenasaUrl = resp[0]
            if not self.validarMetodo(metodo):
                sys.exit("Método no permitido. El proceso se detuvo.")
            if metodo == str(self.metodosPermitidos[1]["metodo"]):
                self.params['idDeposito'] = idDeposito
                self.params['idProducto'] = idProducto
                self.consultaStockProductoFormulado()



            #response = requests.get(urlDeposito, params=params_stock_depo)




            print(":: PROCESO FINALIZADO ::")
            sys.exit()
        else:
            return "ERROR: No se proporcionaron argumentos."
            print("ERROR:  No se proporcionaron argumentos.")



    def consultaStockProductoFormulado(self):

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM senasa_consulta_stock_pf")
            cursor.close()
            metodoNombre = self.metodosPermitidos[1]["metodo"]
            urlDeposito = self.wsSenasaUrl + self.metodosPermitidos[1]["metodo"]
            tipo = self.metodosPermitidos[1]["tipo"]
            usu = self.paramsConn['ws_usuario']
            cla = self.paramsConn['ws_clave']
            # debo traer el responsable del deposito
            cuitJose = '20352969053'
            params_stock_depo = {
                'authUser': usu,
                'authPass': cla,
                'userTaxId': cuitJose,
                'depositId': self.params["idDeposito"],
                'productCodeId': self.params["idProducto"]
            }
            if tipo == "get":
                response = requests.get(urlDeposito, params=params_stock_depo)
            else:
                print("El metdo que intenta ejecutar debe ser det tipo get unicamente.")
                return False

            # Verificar el resultado
            if response.status_code == 200:

                resp = response.content.decode('utf-8')
                data = json.loads(resp)
                cursor = self.conn.cursor()
                cant = 0
                if len(data) > 0:
                    for row in data:
                       lote = row['batch']
                       deposito_id = row['depositId']
                       producto_id = row['productCodeId']
                       productoNombre = row['product']
                       cantidad, descripcion = row['amount'].split(' ', 1)
                       fechaElaboracion = row['elaborationDate']
                       fechaExipracion = row['expirationDate']
                       sql = ("INSERT INTO senasa_consulta_stock_pf (deposito_id, producto_id, producto_nombre, lote, fecha_elab, fecha_expira, cantidad, unidad) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
                       cursor.execute(sql, (deposito_id, producto_id, productoNombre, lote, fechaElaboracion, fechaExipracion, cantidad, descripcion))
                       cant = cant +1
                    self.conn.commit()
                    cursor.close()
                msgRespuesta = "Consulta de stock de producto formulado realizada con éxito, arrojó "+str(cant)+" registros."
                self.registroRespuestas(response.status_code, msgRespuesta, metodoNombre)




            else:

                respuesta_str = response.content.decode('utf-8')
                mensaje = respuesta_str[2:-2]
                self.registroRespuestas(response.status_code, "Error en la solicitud: "+str(respuesta_str.strip('["]')), metodoNombre)
                print("Error en la solicitud: "+str(respuesta_str.strip('["]')))
                return False
        except requests.exceptions.RequestException as e:
            self.registroRespuestas(response.status_code, "Error en la solicitud: "+str(e), metodoNombre)

            print(f"Excepción de solicitud: {e}")

        except KeyError as e:
            self.registroRespuestas(response.status_code, "Excepción de clave: La clav: " + str(e)+ "no se encuentra en los parámetros", metodoNombre)
            print(f"Excepción de clave: La clave {e} no se encuentra en los parámetros.")

        except Exception as e:
            self.registroRespuestas(response.status_code, "Error en la solicitud ", metodoNombre)
            print(f"Excepción general: {e}")




    def registroRespuestas(self, codigo, descripcion, metodo):
        try:
            if codigo != 200:
                errorSn = "S"
            else:
                errorSn = "N"
            nroComprobante = 0
            cursor = self.conn.cursor()
            sql = ("INSERT INTO senasa_respuestas(descripcion, codigo, nro_comprobante, fecha_hora, control, metodo_ws, operacion, maquina, errorSn) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")
            cursor.execute(sql, (descripcion, codigo, nroComprobante, self.fechaHoraHoy, self.fechaHoraHoy, metodo, self.idOperacion, ".", errorSn))
            self.conn.commit()
            cursor.close()


        except requests.exceptions.RequestException as e:
            print(f"Excepción de solicitud: {e}")

        except KeyError as e:
            print(f"Excepción de clave: La clave {e} no se encuentra en los parámetros.")

        except Exception as e:
            print(f"Excepción general: {e}")
    def validarMetodo(self, metodo):
        for metodo_permitido in self.metodosPermitidos:
            if metodo_permitido['metodo'] == metodo:
                return True
        print(f"El método {metodo} que intenta ejecutar, no es válido en el servicio web al que inténta acceder.")
        return False

if __name__ == "__main__":
    senasaApi = SenasaApi()
    senasaApi.main()
