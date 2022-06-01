import requests
import json
import logging
from google.cloud import firestore

def agc(request):
    #Obtener el request de dialogFlow
    request_json = request.get_json()
     
    #Detectar que intent estamos analizando. 
    detect_intent = request_json["queryResult"]["intent"]["displayName"]

    print('Intent detectado: '+ str(detect_intent))
    responseText = ''
    if(detect_intent == 'PedidoAgendamientoC'):
        RequestJson = request_json['queryResult']['outputContexts'][0]
        responseText = agendar_cita(RequestJson) 
    elif(detect_intent == 'PedidoCancelarCita'):
        RequestJson = request_json['queryResult']['outputContexts'][0]
        responseText = agendar_cita(RequestJson) 

    res = {"fulfillmentMessages": [{"text": {"text": [responseText]}}]}
    return res

def cancelar_cita(requestJson):
    #Consultar data de usuarios
    db = firestore.Client()
    users_ref = db.collection(u'users')
    docs = users_ref.stream()

    #Busqueda de usuario
    count = 0
    data = {}
    #Variable que determina si ya existe una cita
    flagUser = False
    flagCita = False
    for doc in docs:
        if(doc.id == str(requestJson['parameters']['Documento'])):
            #Consultar cita de usuario si existe en la base
            #Almacena la data en un arreglo
            flagUser = True
            users_refUser = db.collection(u'users').document(str(requestJson['parameters']['Documento']))
            docsCitas = users_refUser.get()
            count = len(docsCitas.to_dict())
            for i in range(count):
                var = i+1
                data[str(var)] = docsCitas.to_dict()[str(var)]
                if(str(requestJson['parameters']['date']) ==  docsCitas.to_dict()[str(var)][str('Dia_Cita')]):
                    if(str(requestJson['parameters']['time']) ==  docsCitas.to_dict()[str(var)][str('Hora_Cita')]):
                        flagCita = True
    
    if(flagCita and flagUser):
        responseText = ('Señor@ '+requestJson['parameters']['given-name']+'.\n'+'Su cita fue cancelada existosamente para el dia :\n'+requestJson['parameters']['date']+' a las ' + requestJson['parameters']['time'])
    elif(flagCita and flagUser == False):
        responseText = ('Señor@ '+requestJson['parameters']['given-name']+'.\n'+'Usted no tiene cita para ser cancelada el dia :\n'+requestJson['parameters']['date']+' a las ' + requestJson['parameters']['time']+'\n'+'Verifique de nuevo e intente nuevamente.')
    elif(flagUser == False):
        responseText = ('Señor@ '+requestJson['parameters']['given-name']+'.\n'+'Usted no se encuentra con citas registradas en este momento.')
    return responseText
    
def agendar_cita(requestJson):
    #Consultar data de usuarios
    db = firestore.Client()
    #Almacena la data en un arreglo
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
            
    #Nueva data
    newData = {
        'Nombre Cliente':requestJson['parameters']['given-name'],
        'Documento':requestJson['parameters']['Documento'],
        'Dia_Cita':requestJson['parameters']['date'],
        'Hora_Cita':requestJson['parameters']['time']            
        }

    #Busqueda de usuario
    count = 0
    data = {}
    #Variable que determina si ya existe una cita
    flag = False
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
                if(str(requestJson['parameters']['date']) ==  docsCitas.to_dict()[str(var)][str('Dia_Cita')]):
                    if(str(requestJson['parameters']['time']) ==  docsCitas.to_dict()[str(var)][str('Hora_Cita')]):
                        flag = True

        
    
    #Existe el usuario con id agrega la cita nueva
    if flag == False:
        data[str(count+1)] = newData
        print(data)
        doc_ref = db.collection(u'users').document(str(requestJson['parameters']['Documento']))
        doc_ref.set(data)
        
        responseText = ('Señor@ '+newData['Nombre Cliente']+'.\n'+'Su cita fue agendada existosamente para el dia :\n'+newData['Dia_Cita']+' a las ' + newData['Hora_Cita'])
    elif flag == True:
        responseText = ('Señor@ '+newData['Nombre Cliente']+'.\n'+'Su cita no pudo ser agendada.\n'+'Ya tiene una cita agendada para esa hora y fecha.')
    
    return responseText
