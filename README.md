


**alexa_template**

*This repo contains the  template for Alexa Skills in Python. It also includes the companion tutorial. Both written by [Jason Rigden](https://jasonrigden.com/). 
Additionally the  tutorial is also available in video form on [Mr. Rigden's Channel on Youtube](https://www.youtube.com/watch?v=i8QCO0YWJRY&list=PLLlMDtI0KL5pK4-6N4hGK7_wwayF_naDG)* 

**If you find this code or this tutorial useful, would you please star this github project.**

# How to make an Alexa Skill with Python
This guide will assume that you have already completed the [Alexa Python Tutorial](https://developer.amazon.com/alexa-skills-kit/alexa-skill-quick-start-tutorial) from Amazon. If you have done this then you should have a good handle on how to create new Alexa Skills and Lambda functions. But you probably still have no idea how to write code for an Alexa Skill. The code for “`alexa-skills-kit-color-expert-python”` is almost unreadable. Maybe [Amazon](https://twitter.com/alexadevs) should hire me to write tutorials. :stuck_out_tongue_winking_eye: Seriously, if you really like this tutorial tell the [Alexa Devs](https://twitter.com/alexadevs) they should hire me to make more.

This tutorial will show you a template with some nice clean readable code.

## JSON Everywhere
Almost everything you will be dealing with is JSON. Check out the “[JSON Interface Reference for Custom Skills](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference)” as a reference. Those JSON objects will be represented by Python dictionaries. You will be seeing many dictionaries within dictionaries.

## The Lambda Function
Lambda functions start with `lambda_handler` function. Think of it like a `main()`.

    def lambda_handler(event, context):
        if event['request']['type'] == "LaunchRequest":
            return on_launch(event, context)
        elif event['request']['type'] == "IntentRequest":
            return intent_router(event, context)

This function is given two arguments: `event`, `context`. `event` is a Python dictionary. First we check `event[‘request’][‘type’]` to see what type of request we have received. [Standard Request Types](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-standard-request-types-reference) can be one of three values:

 - LaunchRequest
 - IntentRequest
 - SessionEndedRequest

## on_launch
This happens when the skill is invoked with no intent. When called, Alexa will say, “This is the body”. It will also create a card with the title, “This is the title”. In this function we see out first helper function from the template. The `statement` function.

    def on_launch(event, context):
        return statement("This is the title", "This is the body")

## statement
This is a simple helper function that builds a response. It takes a `title` and a `body`. It uses these to build the [spoken output](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#outputspeech-object) and the [card output](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#card-object).

    def statement(title, body):
        speechlet = {}
        speechlet['outputSpeech'] = build_PlainSpeech(body)
        speechlet['card'] = build_SimpleCard(title, body)
        speechlet['shouldEndSession'] = True
        return build_response(speechlet)

In this function we create a dictionary. Remember, these dictionaries will be turned into JSON objects. We give the key `outputSpeech` the value returned by `build_PlainSpeech`. We give the key card the value returned by `build_SimpleCard`. And we set the key `shouldEndSession` to `True`. Then we give that dictionary to `build_response` and return the result.

Let’s deconstruct some of the functions called here.

## build_PlainSpeech
This function builds the [OutputSpeech](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#outputspeech-object) object.

    def build_PlainSpeech(body):
        speech = {}
        speech['type'] = 'PlainText'
        speech['text'] = body
        return speech

## build_SimpleCard
This function builds the [Card](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#card-object) object. Cards need titles.

    def build_SimpleCard(title, body):
        card = {}
        card['type'] = 'Simple'
        card['title'] = title
        card['content'] = body
        return card

## build_response
This function builds the [Response body](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#response-body-syntax).

    def build_response(message, session_attributes={}):
        response = {}
        response['version'] = '1.0'
        response['sessionAttributes'] = session_attributes
        response['response'] = message
        return response

## intent_router
This happens when the skill is invoked with an intent. We need to do another check now. This time we need to route the right intent to the right function. I am assigning `event[‘request’][‘intent’][‘name’]` to intent just for readability. Those nested dictionaries can get hard to read.

    def intent_router(event, context):
        intent = event['request']['intent']['name']
        # Custom Intents
        if intent == "SingIntent":
            return sing_intent(event, context)
        if intent == "TripIntent":
            return trip_intent(event, context)
        if intent == "CounterIntent":
            return counter_intent(event, context)
        # Required Intents
        if intent == "AMAZON.CancelIntent":
            return cancel_intent()
        if intent == "AMAZON.HelpIntent":
            return help_intent()
        if intent == "AMAZON.StopIntent":
            return stop_intent()

You may have noticed that I skipped over adding intents to the Alexa Skill Kit interface. This is a bit beyond the scope of this tutorial. The Skill Builder is complex. For now just open the Builder’s code editor and paste in the code from [intents.json](https://github.com/jrigden/alexa_template/blob/master/intents.json) from the GitHub repo. There are many good guides for the Skill Builder available online.

Let’s take a look at some of these functions.

## sing_intent
This function gets called when we receive the `SingIntent`. It uses the `statement` function from earlier to sing a short song to the user.

    def sing_intent(event, context):
        song = "Daisy, Daisy. Give me your answer, do. I'm half crazy all for the love of you"
        return statement("daisy_bell_intent", song)

## trip_intent
This function gets called when we receive the `TripIntent`. This intent uses the [Dialog Model](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/ask-define-the-vui-with-gui#define-dialog). A dialog helps the collection multipart data by asking follow up questions. We need to return a [Delegate Directive](http://delegate%20directive/) to continue the dialog.

We check the `dialogState`. If it is `STARTED` or `IN_PROGRESS` we call the `continue_dialog` function. When the `dialogState` is `COMPLETED`, we can access the information in the slots.

    def trip_intent(event, context):
        dialog_state = event['request']['dialogState']
        if dialog_state in ("STARTED", "IN_PROGRESS"):
            return continue_dialog()
        elif dialog_state == "COMPLETED":
            return statement("trip_intent", "Have a good trip")
        else:
            return statement("trip_intent", "No dialog")

## continue_dialog
This function creates and returns a `Dialog.Delegate`.

    def continue_dialog():
        message = {}
        message['shouldEndSession'] = False
        message['directives'] = [{'type': 'Dialog.Delegate'}]
        return build_response(message)

## counter_intent
This function gets called when we receive the `CounterIntent`. This function introduces the [Session object](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#session-object) and the template’s `conversation` function. The session allows us store key value pairs in `event[‘session’][‘attributes’]` . These key value pairs disappear at the end of a session.

In this function we are incrementing a counter in the session. Then we return the result of template’s `conversation` function.

    def counter_intent(event, context):
        session_attributes = event['session']['attributes']
    
        if "counter" in session_attributes:
            session_attributes['counter'] += 1
    
        else:
            session_attributes['counter'] = 1
    
        return conversation("counter_intent",
                            session_attributes['counter'],
                            session_attributes)

## conversation
This function is very similar to the `statement` function. It does two thing differently. First it sets the `shouldEndSession` to `False`, because we want to continue the session. It also sends back the session in the response. This maintains the information in the session.

    def conversation(title, body, session_attributes):
        speechlet = {}
        speechlet['outputSpeech'] = build_PlainSpeech(body)
        speechlet['card'] = build_SimpleCard(title, body)
        speechlet['shouldEndSession'] = False
        return build_response(speechlet,
                              session_attributes=session_attributes)

## Conclusion
I hope you found this useful. Although this was not an complete guide to making Alexa Skill with Python, it should get you started. Go out there and make awesome Alexa Skills! If you publish a skill send it to me. I would love to try it out. 

*Questions, Suggestions, or Problems*
Please [open a new issue](https://github.com/jrigden/alexa_template/issues/new) in this repo.






----------

**MIT License**

Copyright (c) 2017 Jason Rigden

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
