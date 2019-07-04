def on_session_started(session_started_request, session):
	print("on_session_started requestId=" + session_started_request['requestId']+ ", sessionId=" + session['sessionId'])
def on_launch(launch_request, session):
	return get_welcome_response()

def on_session_ended(session_ended_request, session):
	print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])

def get_welcome_response():
	session_attributes = {}
	card_title = "Welcome"
	speech_output = "Welcome to home. To get some examples of what this skill can do, ask for help now."
	reprompt_text = speech_output
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_help_response():
	session_attributes = {}
	card_title = "Help"
	speech_output = "Welcome to the help section for the home. A couple of examples of phrases that I can except are... switch on the light"
	reprompt_text = speech_output
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))

def on_intent(intent_request, session):
	print("on_intent requestId=" + intent_request['requestId'] +", sessionId=" + session['sessionId'])
	intent = intent_request['intent']
	intent_name = intent_request['intent']['name']
	if intent_name == "lighton":
		return get_lighton_response()
	elif intent_name == "AMAZON.HelpIntent":
		return get_help_response()
	elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
		return handle_session_end_request()
	else:
		raise ValueError("Invalid intent")

def get_lighton_response():
	import boto3
	client = boto3.client('iot-data')
	session_attributes = {}
	card_title = "lighTon"
	reprompt_text ='light '
	client.publish(topic ='led',qos =1,payload ="led on")
	should_end_session = False
	speech_output = "light on"
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
