import requests
import json
import logging
from google.cloud import firestore

def agc(request):
    #Obtener el request de dialogFlow
    request_json = request.get_json()
     
    #DEtectar que intent estamos analizando. 
    detect_intent = request_json["queryResult"]["intent"]["displayName"]
 
    print('Intent detectado: '+ str(detect_intent))
    

    if(detect_intent == 'PedidoAgendamientoC'):
        RequestJson = request_json['queryResult']['outputContexts'][0]
        data = agendar_cita(RequestJson) 
    
    return {'fulfillmentText':data}
    

def agendar_cita(requestJson):
    #Consultar data de usuarios
    db = firestore.Client()
    #Almacena la data en un arreglo
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
            
    #Busqueda de usuario
    flag = False
    count = 0
    data = {}
    for doc in docs:
        if(doc.id == str(requestJson['parameters']['Documento'])):
            #Consultar cita de usuario si existe en la base
            #Almacena la data en un arreglo
            users_refUser = db.collection(u'users').document(str(requestJson['parameters']['Documento']))
            docsCitas = users_refUser.get()
            count = len(docsCitas.to_dict())
            for i in range(count):
                var = i+1
                data[str(var)] = docsCitas.to_dict()[str(var)]
                
            flag = True
        
    
    #Existe el usuario con id agrega la cita nueva
    if(flag):
        #Nueva data
        newData = {
                'Nombre Cliente':requestJson['parameters']['given-name'],
                'Documento':requestJson['parameters']['Documento'],
                'Dia_Cita':requestJson['parameters']['date'],
                'Hora_Cita':requestJson['parameters']['time']            
                }

        data[str(count+1)] = newData
        print(data)
        doc_ref = db.collection(u'users').document(str(requestJson['parameters']['Documento']))
        doc_ref.set(data)
    #No existe usuario con id agrega el usuario
    else:
        #Nueva data
        newData = {
            '1': {
                'Nombre Cliente':requestJson['parameters']['given-name'],
                'Documento':requestJson['parameters']['Documento'],
                'Dia_Cita':requestJson['parameters']['date'],
                'Hora_Cita':requestJson['parameters']['time']            
                }
        }
        # Add a new document
        doc_ref = db.collection(u'users').document(str(requestJson['parameters']['Documento']))
        doc_ref.set(newData)

    return newData
