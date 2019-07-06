def lambda_handler(event,context):
	print("event.session.application.applicationId=" +event['session']['application']['applicationId'])
	if event['session']['new']:
		on_session_started({'requestId': event['request']['requestId']},event['session'])
	if event['request']['type'] == "LaunchRequest":
		return on_launch(event['request'], event['session'])
	elif event['request']['type'] == "IntentRequest":
		return on_intent(event['request'], event['session'])
	elif event['request']['type'] == "SessionEndedRequest":
		return on_session_ended(event['request'], event['session'])

def on_session_started(session_started_request, session):
	print("check1")
	print("on_session_started requestId=" + session_started_request['requestId']+ ", sessionId=" + session['sessionId'])
	print("check")
	

def on_launch(launch_request, session):
	return get_welcome_response()

def on_session_ended(session_ended_request, session):
	print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])

def get_welcome_response():
	session_attributes = {}
	card_title = "Welcome"
	speech_output = "Welcome to the alexaml Skill. To get some examples of what this skill can do, ask for help now."
	reprompt_text = speech_output
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_help_response():
	session_attributes = {}
	card_title = "Help"
	speech_output = "Welcome to the help section for the alexaml. A couple of examples of phrases that I can except are... what is the value for 55."
	reprompt_text = speech_output
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))

def on_intent(intent_request, session):
	print("on_intent requestId=" + intent_request['requestId'] +", sessionId=" + session['sessionId'])
	intent = intent_request['intent']
	intent_name = intent_request['intent']['name']
	if intent_name == "predict":
		in1 = intent_request["intent"]["slots"]["input"]["value"]
		return predict(in1)
	elif intent_name == "AMAZON.HelpIntent":
		return get_help_response()
	elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
		return handle_session_end_request()
	else:
		raise ValueError("Invalid intent")

def predict(in1):
	import os
	import boto3
	import io
	import json
	import csv
	session_attributes = {}
	card_title = "lr predict"
	speech_output = ""
	ENDPOINT_NAME =os.environ['ENDPOINT_NAME']
	runtime= boto3.client('runtime.sagemaker')
	response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,ContentType='text/csv',Body=str(in1))
	result = json.loads(response['Body'].read().decode())
	print(result['predictions'][0]['score'])
	reprompt_text = "predicted value for "+ str(in1) +' is' + str(result['predictions'][0]['score'])
	speech_output = reprompt_text
	should_end_session = True
	return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
