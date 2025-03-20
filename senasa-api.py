import requests
import json
import sys
argumentos = sys.argv
import logging
from conn.DBConnection import DBConnection as DBConnection
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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
        self.idDeposito=0
        self.nroComprobante = 0
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
            {"metodo": "Consulta_Envio", "tipo": "get"},
            {"metodo": "Cancelar_Envio", "tipo": "post"},
            {"metodo": "Consulta_Unidad_Medida", "tipo": "get"},
            {"metodo": "Alta_Autoconsumo_FP", "tipo": "post"}
        ]
        fechaHoraHoyTemp = datetime.now()
        formatoFechaHoy = "%Y-%m-%d %H:%M:%S"
        formatoFechaHoySimple = "%d/%m/%Y"
        self.fechaHoraHoy = fechaHoraHoyTemp.strftime(formatoFechaHoy)
        self.fechaHoraHoySimple = fechaHoraHoyTemp.strftime(formatoFechaHoySimple)






    def main(self):
        # argumentos por default
        # 0: nombre del metodo a ejecutar en el web service
        # 1: testingSn
        # 2: idEjecucion
        # 3: idDeposito (segun metodo)
        # 4: idProducto (segun metodo

        if len(argumentos) > 1:
            metodo = argumentos[1]
            ambiente =  self.ambiente

            # argumentos que recibo segun el metodo que ejecuta
            if len(argumentos) > 2:
                self.nroComprobante = argumentos[2]
            else:
                self.nroComprobante = 0
            if len(argumentos) > 3:
                self.idOperacion = argumentos[3]
            else:
                self.idOperacion = 0

            '''

            Alta_Envio // Parametros

            '''

            if metodo == str(self.metodosPermitidos[0]["metodo"]):
                    # Recibo estos parametros
                if len(argumentos) > 4:
                    idDeposito = argumentos[4]
                else:
                    idDeposito = 0

                if len(argumentos) > 4:
                    idDepositoRecibe = argumentos[5]
                else:
                    idDepositoRecibe = 0

                if len(argumentos) > 6:
                   idProducto = argumentos[6]
                else:
                   idProducto = 0

                if len(argumentos) > 7:
                   cuitEnvia = argumentos[7]
                else:
                   cuitEnvia = 0

                if len(argumentos) > 8:
                   cuitRecibe = argumentos[8]
                else:
                   cuitRecibe = 0


            '''
            
            Cancelar Envio
            
            '''
            if metodo == str(self.metodosPermitidos[12]["metodo"]):
                 # Recibo estos parametros


                if len(argumentos) > 5:
                   operacionId = argumentos[5]
                else:
                   operacionId = 0

                if len(argumentos) > 6:
                   movimientoId = argumentos[6]
                else:
                   movimientoId = 0

                logging.info("CANCELAR ENVIO: " + str(operacionId) + " " + str(movimientoId))



            ''''

            Consulta_Deposito // Parametros

            '''

            if metodo == str(self.metodosPermitidos[5]["metodo"]):

                    if len(argumentos) > 3:
                        cuit = argumentos[3]
                    else:
                        cuit = 0
                    print("---------------> "+cuit)


            '''
            
            Consulta_Stock_Producto_Formulado // Parametros

            '''

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

            '''
            
            Consulta_Envio // Parametros
            
            '''
            if metodo == str(self.metodosPermitidos[11]["metodo"]):


                if len(argumentos) > 4:
                    operationId = argumentos[4]
                else:
                    operationId = 0

                if len(argumentos) > 5:
                    movementId = argumentos[5]
                else:
                    movementId = 0





            if ambiente is None:
                ambiente = "TEST"


            logging.info(":: PROCESANDO DATOS... Aguarde! :: ")



            cursor = self.conn.cursor()
            cursor.execute("SELECT parametro_val  FROM senasa_parametros where parametro_id in ('ws_usu', 'ws_pass')")
            parametros = cursor.fetchall()
            etiquetas = ["ws_usuario", "ws_clave"]
            for idx, param in enumerate(parametros):
                self.paramsConn[etiquetas[idx]] = param[0]

            if ambiente == "TEST":
                val = "ws_url_test"
            else:
                val = "ws_url_prod"
            cursor.execute("SELECT parametro_val  FROM senasa_parametros where parametro_id = ?", (val, ))
            resp = cursor.fetchone()
            self.wsSenasaUrl = resp[0]

            if not self.validarMetodo(metodo):
                sys.exit("Método no permitido. El proceso se detuvo.")
                logging.info(":: Método no permitido. El proceso se detuvo :: ")

            if metodo == str(self.metodosPermitidos[1]["metodo"]):
                logging.info(":: CONSULTA STOCK PRODUCTO FORMULADO :: ")

                self.params['idDeposito'] = idDeposito
                self.params['idProducto'] = idProducto
                self.consultaStockProductoFormulado()

            elif metodo ==  str(self.metodosPermitidos[0]["metodo"]):
                logging.info(":: ALTA ENVIO ::")
                self.params['idDeposito'] = idDeposito
                self.params['idDepositoRecibe'] = idDepositoRecibe
                self.altaEnvioStockProducto(cuitEnvia, cuitRecibe)



            if metodo == str(self.metodosPermitidos[5]["metodo"]):
                logging.info(":: COSULTAR DEPOSITOS "+str(cuit)+" ::")
                self.consultarDeposito(cuit)


            if metodo == str(self.metodosPermitidos[11]["metodo"]):
                logging.info(":: COSULTAR ENVIO ::")
                self.consultarEnvio( operationId, movementId)

            if metodo == str(self.metodosPermitidos[12]["metodo"]):
                logging.info(":: BAJA ENVIO ::")
                self.bajaEnvio( operacionId, movimientoId)


            logging.info(":: PROCESO FINALIZADO :: ")
            sys.exit()
        else:
            logging.info(":: ERROR:  No se proporcionaron argumentos :: ")
            return "ERROR: No se proporcionaron argumentos."



    def consultaStockProductoFormulado(self):

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM senasa_consulta_stock_pf")
            cursor.close()
            metodoNombre = self.metodosPermitidos[1]["metodo"]
            url = self.wsSenasaUrl + self.metodosPermitidos[1]["metodo"]
            tipo = self.metodosPermitidos[1]["tipo"]
            usu = self.paramsConn['ws_usuario']
            cla = self.paramsConn['ws_clave']
            # debo traer el responsable del deposito de la tabla que me va a pasar adrian

            params_stock_depo = {
                'authUser': usu,
                'authPass': cla,
                'userTaxId': self.encargado,
                'depositId': self.params["idDeposito"],
                'productCodeId': self.params["idProducto"]
            }
            if tipo == "get":
                response = requests.get(url, params=params_stock_depo)
            else:

                logging.info(":: El método que intenta ejecutar debe ser det tipo get unicamente. ::")
                return False

            # Verificar el resultado
            responseStatusCode = response.status_code
            if responseStatusCode == 200:

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
                       try:
                         cursor.execute(sql, (deposito_id, producto_id, productoNombre, lote, fechaElaboracion, fechaExipracion, cantidad, descripcion))
                         cant = cant +1
                       except Exception as e:  # Captura cualquier otro tipo de excepción
                           logging.info(f"Se produjo un error inesperado: {e}")
                       finally:
                        self.conn.commit()
                    cursor.close()
                msgRespuesta = "Consulta de stock de producto formulado  se ha realizado con éxito y arrojó "+str(cant)+" registros."
                logging.info(msgRespuesta)
                self.registroRespuestas(response.status_code, msgRespuesta, metodoNombre)




            else:

                respuesta_str = response.content.decode('utf-8')
                mensaje = respuesta_str[2:-2]
                self.registroRespuestas(responseStatusCode, "Error en la solicitud: "+str(respuesta_str.strip('["]')), metodoNombre)
                logging.info("Error en la solicitud: "+str(respuesta_str.strip('["]')))
                return False
        except requests.exceptions.RequestException as e:
            self.registroRespuestas(400, "Error en la solicitud: "+str(e), metodoNombre)

            logging.info(f"Excepción de solicitud: {e}")

        except KeyError as e:
            self.registroRespuestas(400, "Excepción de clave: La clave: " + str(e)+ "no se encuentra en los parámetros", metodoNombre)
            logging.info(f"Excepción de clave: La clave {e} no se encuentra en los parámetros.")

        except Exception as e:
            self.registroRespuestas(400, "Error en la solicitud ", metodoNombre)
            logging.info(f"Excepción general: {e}")

    def altaEnvioStockProducto(self, cuitEnvia, cuitRecibe):

        try:
            metodoNombre = self.metodosPermitidos[0]["metodo"]
            url = self.wsSenasaUrl + self.metodosPermitidos[0]["metodo"]
            tipo = self.metodosPermitidos[0]["tipo"]
            usu = self.paramsConn['ws_usuario']
            cla = self.paramsConn['ws_clave']
            depEnvia = self.params["idDeposito"]
            depRecibe =  self.params["idDepositoRecibe"]
            # Debo traer el responsable del deposito de la tabla que me va a pasar adrian
            cuitEnvia = self.formatearCuit(cuitEnvia) # encargado del deposito
            cuitRecibe = self.formatearCuit(cuitRecibe)

            if depRecibe is None:
                logging.info(":: ERROR: No se encontró el depósito  que recibe en la consulta  ::")
                self.registroRespuestas(400, "No se encontró el deposito que recibe en la consulta", metodoNombre)
                return False

            else:




                    params_envio = {
                        'authUser': usu,
                        'authPass': cla,
                        'userTaxId': cuitEnvia,
                        'sendDate':self.fechaHoraHoySimple,
                        'senderDepositId': int(depEnvia),
                        'receiverDepositId' : int(depRecibe),
                        'receiverCompanyCuit': cuitRecibe,



                    }
                    # este objeto lo tengo que levantar de la tabla que me va a dejar adrian con el detalle del remito
                    productos = [
                        {'id_product_code': 4911, 'batchId': '14240610M0', 'amount': 3},
                    ]
                    for idx, producto in enumerate(productos):
                        params_envio[f"products[{idx}][id_product_code]"] = producto['id_product_code']
                        params_envio[f"products[{idx}][batchId]"] = producto['batchId']
                        params_envio[f"products[{idx}][amount]"] = producto['amount']

                    logging.info(json.dumps(params_envio, indent=4))
                    if tipo == "post":
                        response = ""
                        response = requests.post(url, params=params_envio)
                    else:

                        logging.info(":: El método que intenta ejecutar debe ser det tipo post unicamente. ::")
                        return False

                    # Verificar el resultado
                    if response.status_code == 200:

                        resp = response.content.decode('utf-8')
                        dataResp = json.loads(resp)
                        cursor = self.conn.cursor()
                        opId = dataResp['operationId']
                        movId = dataResp['movementId']
                        cursor.execute(
                            '''INSERT INTO senasa_alta_envio_resp (operacion_id, mov_id, nro_comp) VALUES (?, ?, ?) ''',
                            (opId, movId, self.nroComprobante))
                        self.conn.commit()
                        cursor.close()
                        cant = 0

                        msgRespuesta = "Alta realizada con éxito: (Remito "+str(self.nroComprobante)+")"
                        self.registroRespuestas(response.status_code, msgRespuesta, metodoNombre)
                        logging.info(msgRespuesta)




                    else:

                        respuesta_str = response.content.decode('utf-8')
                        mensaje = respuesta_str[2:-2]
                        self.registroRespuestas(response.status_code,"Error en la solicitud: " + str(respuesta_str.strip('["]')), metodoNombre)
                        logging.info("Error en la solicitud de Alta_Envio: " + str(respuesta_str.strip('["]')))
                        return False


        except requests.exceptions.RequestException as e:
            self.registroRespuestas(response.status_code, "Error en la solicitud: " + str(e), metodoNombre)

            logging.info(f"Excepción de solicitud: {e}")

        except KeyError as e:

            self.registroRespuestas(response.status_code, "Excepción de clave: La clave " + str(e) + "no se encuentra en los parámetros",
                                    metodoNombre)
            logging.info(f"Excepción de clave: La clave {e} no se encuentra en los parámetros.")

        except Exception as e:
            self.registroRespuestas(response.status_code, "Error en la solicitud ", metodoNombre)
            logging.info(f"Excepción general: {e}")










    def consultarDeposito(self, cuit):

        # 30503508725
        try:
            cursor = self.conn.cursor()
            cursor.execute('''delete from senasa_consulta_depositos ''')

            metodoNombre = self.metodosPermitidos[5]["metodo"]
            url = self.wsSenasaUrl + self.metodosPermitidos[5]["metodo"]
            tipo = self.metodosPermitidos[5]["tipo"]
            usu = self.paramsConn['ws_usuario']
            cla = self.paramsConn['ws_clave']
            # debo traer el responsable del deposito de la tabla que me va a pasar adrian

            params = {
                'authUser': usu,
                'authPass': cla,
                'userTaxId': self.encargado,
                'cuit': self.formatearCuit(cuit)

            }
            if tipo == "get":
                response = requests.get(url, params=params)
            else:

                logging.info(":: El método que intenta ejecutar debe ser det tipo get unicamente. ::")
                return False

            # Verificar el resultado
            if response.status_code == 200:

                resp = response.content.decode('utf-8')
                data = json.loads(resp)
                if len(data) == 0:
                    logging.info("No se encontraron depositos para el cuit: "+cuit)
                    self.registroRespuestas(response.status_code, "No se encontraron depositos para el cuit: "+str(cuit), metodoNombre)
                    return False
                else:
                    for depositos in data:
                        depositoId = depositos.get("depositId") or 0
                        empresaNombre = depositos.get("companyName") or ""
                        depositoNombre = depositos.get("depositName") or ""
                        provinciaId = depositos.get("provinceId") or 0
                        ciudadId = depositos.get("townId") or 0
                        districtoId = depositos.get("districtId") or 0
                        codigoPostal = depositos.get("postCode") or 0
                        direccion = depositos.get("addressStreet") or ""
                        direccionNro = depositos.get("addressNumber") or 0
                        estadoId = depositos.get("state") or 0
                        estadoNombre = depositos.get("stateName") or ""
                        plantaId = depositos.get("plantId") or 0
                        latitud = depositos.get("latitude") or ""
                        longitud = depositos.get("longitude") or ""

                        sql_insert = """
                        INSERT INTO DBA.senasa_consulta_depositos 
                        (deposito_id, empresa_nombre, deposito_nombre, provincia_id, ciudad_id, districto_id,  codigo_postal, 
                         direccion, direccion_nro, estado_id, estado_nombre, planta_id, latitud, longitud)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?)
                        """

                        # Datos a insertar (asegúrate de que estén en el mismo orden que los placeholders)
                        valores = ( depositoId,  # deposito_id
                            empresaNombre,  # empresa_nombre
                            depositoNombre,  # deposito_nombre
                            provinciaId,  # provincia_id
                            ciudadId,
                            districtoId,
                            codigoPostal,  # codigo_postal
                            direccion,  # direccion
                            direccionNro,  # direccion_nro
                            estadoId,  # estado_id
                            estadoNombre,  # estado_nombre
                            plantaId,  # planta_id
                            latitud,  # latitud
                            longitud  # longitud
                        )

                        # Ejecutar la sentencia con parámetros seguros
                        cursor.execute(sql_insert,valores)

                    # Confirmar cambios en la base de datos
                    cursor.commit()
                    logging.info("Se han encontrado "+str(len(data))+" depositos")
                    self.registroRespuestas(response.status_code, "Se han encontrado "+str(len(data))+" depositos", metodoNombre)
                    # Cerrar cursor y conexión
                    cursor.close()


            else:

                return False
        except requests.exceptions.RequestException as e:
            return False


    def bajaEnvio(self, operacionId, movimientoid):
        try:

            metodoNombre = self.metodosPermitidos[12]["metodo"]
            url = self.wsSenasaUrl + metodoNombre
            tipo = self.metodosPermitidos[12]["tipo"]
            usu = self.paramsConn['ws_usuario']
            cla = self.paramsConn['ws_clave']
            # debo traer el responsable del deposito de la tabla que me va a pasar adrian

            params = {
                'authUser': usu,
                'authPass': cla,
                'userTaxId': self.encargado,
                'operationId': operacionId,
                'movementId': movimientoid,
                'taskId' : 3,
                'observactions' : 'Baja por error en la carga de datos'

            }
            if tipo == "post":
                response = requests.post(url, params=params)
            else:

                logging.info(
                    ":: El método " + str(metodoNombre) + " que intenta ejecutar debe ser det tipo get unicamente. ::")
                return False

            # Verificar el resultado

            if response.status_code == 200:
                cursor = self.conn.cursor()
                cursor.execute('''delete from senasa_alta_envio_resp where operacion_id = ? and mov_id = ?''', (operacionId, movimientoid))

                resp = response.content.decode('utf-8')
                data = json.loads(resp)


                for clave, valor in data.items():
                    movement_id = data['movementId']
                    operation_id = data['operationId']
                    result = data['result']
                    text = str(result)+", operacion: "+str(operation_id)+", movimiento: "+movement_id
                logging.info(data)
                self.registroRespuestas(response.status_code, text, metodoNombre)
                return data
            else:
                resp = response.content.decode('utf-8')
                data = json.loads(resp)
                logging.info(data)
                self.registroRespuestas(response.status_code, data , metodoNombre)
                return False





        except requests.exceptions.RequestException as e:
            return False





    def consultarEnvio(self,  operationId, movementId ):


        try:

            metodoNombre = self.metodosPermitidos[11]["metodo"]
            url = self.wsSenasaUrl + metodoNombre
            tipo = "get"
            usu = self.paramsConn['ws_usuario']
            cla = self.paramsConn['ws_clave']
            # debo traer el responsable del deposito de la tabla que me va a pasar adrian

            params = {
                'authUser': usu,
                'authPass': cla,
                'userTaxId': self.encargado,
                'operationId': operationId,
                'movementId': movementId,



            }
            if tipo == "get":
                response = requests.get(url, params=params)
            else:

                logging.info(":: El método "+str(metodoNombre)+" que intenta ejecutar debe ser det tipo get unicamente. ::")
                return False

            # Verificar el resultado

            if response.status_code == 200:
                cursor = self.conn.cursor()
                cursor.execute('''delete from senasa_consultar_envio''')

                resp = response.content.decode('utf-8')
                data = json.loads(resp)

                # Lista de datos para insertar


                for dato in data:
                    cursor.execute('''
                        INSERT INTO senasa_consultar_envio (
                            operacion_id, nro_interno, movimiento_id, tipo, estado, fecha_mov,
                            tarea, tarea_nombre, deposito_id, target_deposito_id,
                            company_name_source, company_name_target, productos
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', (
                        dato["operationId"],
                        dato["internalNumber"],
                        dato["movementId"],
                        dato["type"],
                        dato["state"],
                        datetime.strptime(dato["movementDate"], "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
                        dato["taskId"],
                        dato["taskName"],
                        dato["sourceDepositId"],
                        dato["targetDepositId"],
                        dato["companyNameSource"],
                        dato["companyNameTarget"],
                        (json.dumps(dato['products']).strip('[]'))

                    ))

                # insertar en la tabla senasa_consulta_envio
                logging.info(data)
                return data
            else:

                return False
        except requests.exceptions.RequestException as e:
            return False




























    def registroRespuestas(self, codigo, descripcion, metodo):
        try:
            if codigo != 200:
                errorSn = "S"
            else:
                errorSn = "N"

            cursor = self.conn.cursor()

            sql = ("INSERT INTO senasa_respuestas(descripcion, codigo, nro_comprobante, fecha_hora, control, metodo_ws, operacion, maquina, errorSn) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")
            cursor.execute(sql, (str(descripcion).strip("[']"), codigo, self.nroComprobante, self.fechaHoraHoy, self.fechaHoraHoy, metodo, self.idOperacion, ".", errorSn))
            self.conn.commit()
            cursor.close()


        except requests.exceptions.RequestException as e:
            logging.info(f"Excepción de solicitud: {e}")

        except KeyError as e:
            logging.info(f"Excepción de clave: La clave {e} no se encuentra en los parámetros.")

        except Exception as e:
            logging.info(f"Excepción general: {e}")
    def validarMetodo(self, metodo):
        for metodo_permitido in self.metodosPermitidos:
            if metodo_permitido['metodo'] == metodo:
                return True
        logging.info(f"El método {metodo} que intenta ejecutar, no es válido en el servicio web al que inténta acceder.")
        return False

    def formatearCuit(self, cuit):
        # Asegúrate de que el CUIT sea una cadena
        cuit = str(cuit)
        if len(cuit) == 11:
            return f"{cuit[:2]}-{cuit[2:10]}-{cuit[10]}"
        else:
            raise ValueError("El CUIT debe tener exactamente 11 dígitos")





if __name__ == "__main__":
    senasaApi = SenasaApi()
    senasaApi.main()
