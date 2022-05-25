def main():
    var ={
        'responseId': '515a5f7c-0a4a-4da8-a3f4-377f91e0dfdb-d678412e',
        'queryResult': {
            'queryText': 'mañana a las 3 pm',
            'action': 'AgendarCita.AgendarCita-custom',
            'parameters': {
                'date': '2022-05-25T12:00:00-05:00',
                'time': '2022-05-25T15:00:00-05:00'
                },
            'allRequiredParamsPresent': True,
            'fulfillmentText': 'Gracias , vuelva pronto!',
            'fulfillmentMessages': [{
                'text': {'text': ['Listo la cita fue agendada el día: 2022-05-25 a las - 15:00:00']}
		}, {
		'text': {'text': ['Gracias , vuelva pronto!']}
		}],
	    'outputContexts': [{
			'name': 'projects/proyecto-juan-lopez-dialogflow/agent/sessions/bb8f3ad0-11c7-31ec-f2ea-c7908e379985/contexts/setcaptura',
			'parameters': {
				'Documento': '0000000000',
				'Documento.original': '0000000000',
				'given-name': 'Hernesto',
				'given-name.original': 'hernesto',
				'music-artist': '',
				'music-artist.original': '',
				'last-name': '',
				'last-name.original': '',
				'date': '2022-05-25T12:00:00-05:00',
				'date.original': 'mañana',
				'time': '2022-05-25T15:00:00-05:00',
				'time.original': '3 pm'
			}
		}, {
			'name': 'projects/proyecto-juan-lopez-dialogflow/agent/sessions/bb8f3ad0-11c7-31ec-f2ea-c7908e379985/contexts/agendarcita-followup',
			'lifespanCount': 4,
			'parameters': {
				'date': '2022-05-25T12:00:00-05:00',
				'date.original': 'mañana',
				'time': '2022-05-25T15:00:00-05:00',
				'time.original': '3 pm',
				'Documento': '0000000000',
				'Documento.original': '0000000000',
				'given-name': 'Hernesto',
				'given-name.original': 'hernesto',
				'music-artist': '',
				'music-artist.original': '',
				'last-name': '',
				'last-name.original': ''
			}
		}, {
			'name': 'projects/proyecto-juan-lopez-dialogflow/agent/sessions/bb8f3ad0-11c7-31ec-f2ea-c7908e379985/contexts/__system_counters__',
			'parameters': {
				'no-input': 0.0,
				'no-match': 0.0,
				'date': '2022-05-25T12:00:00-05:00',
				'date.original': 'mañana',
				'time': '2022-05-25T15:00:00-05:00',
				'time.original': '3 pm'
			}
		}],
		'intent': {
			'name': 'projects/proyecto-juan-lopez-dialogflow/agent/intents/ea648fb8-24af-47f5-9f02-bd443ff8b907',
			'displayName': 'PedidoAgendamientoC'
		},
		'intentDetectionConfidence': 1.0,
		'languageCode': 'es',
		'sentimentAnalysisResult': {
			'queryTextSentiment': {
				'score': 0.2,
				'magnitude': 0.2
			}
		}
	},
	'originalDetectIntentRequest': {
		'source': 'DIALOGFLOW_CONSOLE',
		'payload': {}
	},
	'session': 'projects/proyecto-juan-lopez-dialogflow/agent/sessions/bb8f3ad0-11c7-31ec-f2ea-c7908e379985'
        }
    json = var['queryResult']['outputContexts'][1]
    data = {
        'Nombre Cliente':json['parameters']['given-name'],
        'Documento':json['parameters']['Documento'],
        'Dia_Cita':json['parameters']['date'],
        'Hora_Cita':json['parameters']['time']
    }
    print(data)
main()
