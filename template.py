##############################
# Builders
##############################


def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech


def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response


def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card


##############################
# Responses
##############################


def conversation(title, body, session_attributes):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet, session_attributes=session_attributes)


def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)


def continue_dialog():
    message = {}
    message['shouldEndSession'] = False
    message['directives'] = [{'type': 'Dialog.Delegate'}]
    return build_response(message)


##############################
# Custom Intents
##############################


def nonstop_intent(event, context):
    if "Monkey" in event['session']['attributes']:
        event['session']['attributes']['Shit'] = "Lots of it"
    event['session']['attributes']['Monkey'] = "bobo"
    return conversation("This never ends", "This is nonstop",
                        event['session']['attributes'])
    #return statement("Nonstao", "You Nonstao to count something")


def plan_my_trip(event, context):
    dialog_state = event['request']['dialogState']

    if dialog_state in ("STARTED", "IN_PROGRESS"):
        return continue_dialog()

    elif dialog_state == "COMPLETED":
        return statement("plan_my_trip", "Plan complete. Good Job")

    else:
        return statement("plan_my_trip", "No dialog")


def count_intent():
    return statement("CountIntent", "You want to count something")


##############################
# Required Intents
##############################


def cancel_intent():
    return statement("CancelIntent", "You want to cancel")


def help_intent():
    return statement("CancelIntent", "You want help")


def stop_intent():
    return statement("StopIntent", "You want to stop")


##############################
# On Launch
##############################


def on_launch(event, context):
    return statement("title", "body")


##############################
# Routing
##############################


def intent_router(event, context):
    intent = event['request']['intent']['name']

    # Custom Intents

    if intent == "NonStopIntent":
        return nonstop_intent(event, context)

    if intent == "PlanMyTrip":
        return plan_my_trip(event, context)

    if intent == "CountIntent":
        return count_intent()

    if intent == "PickANumberIntent":
        return count_intent()

    # Required Intents

    if intent == "AMAZON.CancelIntent":
        return cancel_intent()

    if intent == "AMAZON.HelpIntent":
        return help_intent()

    if intent == "AMAZON.StopIntent":
        return stop_intent()


##############################
# Program Entry
##############################


def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)

    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)

