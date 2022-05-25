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
    
    data = {
        'Nombre Cliente':RequestJson['parameters']['given-name'],
        'Documento':RequestJson['parameters']['Documento'],
        'Dia_Cita':RequestJson['parameters']['date'],
        'Hora_Cita':RequestJson['parameters']['time']
    }
    
    # Add a new document
    db = firestore.Client()
    doc_ref = db.collection(u'users').document(str(RequestJson['parameters']['Documento']))
    doc_ref.set(data)

    users_ref = db.collection(u'users').get()
    print(type(users_ref))
