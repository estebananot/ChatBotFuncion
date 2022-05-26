import requests
import json
from google.cloud import firestore

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    
    RequestJson = request_json['queryResult']['outputContexts'][0]

    #Consultar data
    db = firestore.Client()
    users_ref = db.collection(u'users')
    docs = users_ref.stream()

    #Nueva data
    newData = {
            'Nombre Cliente':RequestJson['parameters']['given-name'],
            'Documento':RequestJson['parameters']['Documento'],
            'Dia_Cita':RequestJson['parameters']['date'],
            'Hora_Cita':RequestJson['parameters']['time']            
            }
            
    #Busqueda de usuario
    flag = False
    count = 0
    data = {}
    for doc in docs:
        if(doc.id == str(RequestJson['parameters']['Documento'])):
            count += 1
            print(f'{doc.id} => {doc.to_dict()}')
            data[str(count)] = doc.to_dict()
            flag = True
    
    #Existe el usuario con id agrega la cita nueva
    if(flag):
        data[str(count+1)] = newData
        print(data)
        doc_ref = db.collection(u'users').document(str(RequestJson['parameters']['Documento']))
        doc_ref.set(data)
    #No existe usuario con id agrega el usuario
    else:
        # Add a new document
        doc_ref = db.collection(u'users').document(str(RequestJson['parameters']['Documento']))
        doc_ref.set(newData)
            
    return "{A}"
