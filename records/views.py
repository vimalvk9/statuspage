from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from yellowant import YellowAnt
import requests
import json, uuid
from yellowant.messageformat import MessageClass, MessageAttachmentsClass, MessageButtonsClass, AttachmentFieldsClass
import traceback
from django.views.decorators.csrf import csrf_exempt
from records.models import YellowUserToken, YellowAntRedirectState, AppRedirectState, StatuspageUserToken
from records.commandcentre import CommandCentre
from django.contrib.auth.models import User


def redirectToYellowAntAuthenticationPage(request):
    user = User.objects.get(id=request.user.id)
    state = str(uuid.uuid4())
    YellowAntRedirectState.objects.create(user = user, state = state)
    return HttpResponseRedirect("{}?state={}&client_id={}&response_type=code&redirect_url={}".format(settings.YELLOWANT_OAUTH_URL, state, settings.YELLOWANT_CLIENT_ID,settings.YELLOWANT_REDIRECT_URL))


def yellowantRedirecturl(request):
    print("In yellowantRedirecturl")
    #print('It is here')
    code = request.GET.get('code')
    #print(code)
    state = request.GET.get("state")
    yellowant_redirect_state = YellowAntRedirectState.objects.get(state = state)
    user = yellowant_redirect_state.user

    y = YellowAnt(app_key = settings.YELLOWANT_CLIENT_ID, app_secret= settings.YELLOWANT_CLIENT_SECRET, access_token=None,
    redirect_uri=settings.YELLOWANT_REDIRECT_URL)
    #access_token_dict is json structured
    access_token_dict = y.get_access_token(code)
    access_token = access_token_dict['access_token']
    yellowant_user = YellowAnt(access_token=access_token)
    profile = yellowant_user.get_user_profile()
    user_integration = yellowant_user.create_user_integration()
    hash_str = str(uuid.uuid4()).replace("-","")[:25]

    ut = YellowUserToken.objects.create(user = user, yellowant_token = access_token, yellowant_id = profile['id'], yellowant_integration_invoke_name = user_integration["user_invoke_name"], yellowant_integration_id = user_integration['user_application'], webhook_id=hash_str)
    state = str(uuid.uuid4())
    AppRedirectState.objects.create(user_integration = ut, state = state)

    sp_token = "11649b9b-ea84-47fa-aecb-9faf3ab447bd"

    sut = StatuspageUserToken.objects.create(user_integration=ut, statuspage_access_token=sp_token)

    return HttpResponse("Integrated!")

## Webhook function to notify user about newly created incident

@csrf_exempt
def add_new_incident(request):
    data = json.loads(request.POST['data'])
    args = data["args"]
    page_id = args['page_id']
    service_application = data["application"]
    integration_id = (
    YellowUserToken.objects.get(yellowant_integration_id=service_application)).yellowant_integration_id
    access_token = (YellowUserToken.objects.get(yellowant_integration_id=service_application)).yellowant_token

    service_application = str(integration_id)

    webhook_message = MessageClass()
    webhook_message.message_text = "New incident added"
    attachment = MessageAttachmentsClass()
    attachment.title = "Get incident details"

    button_get_incidents = MessageButtonsClass()
    button_get_incidents.name = "1"
    button_get_incidents.value = "1"
    button_get_incidents.text = "Get all incidents"
    button_get_incidents.command = {
        "service_application": service_application,
        "function_name": 'all_incidents',
        "data": {
            'page_id': page_id
        }
    }

    attachment.attach_button(button_get_incidents)
    webhook_message.attach(attachment)
    print(integration_id)
    yellowant_user_integration_object = YellowAnt(access_token=access_token)
    send_message = yellowant_user_integration_object.create_webhook_message(
        requester_application=integration_id,
        webhook_name="new_incident", **webhook_message.get_dict())
    return HttpResponse("OK", status=200)

## Webhook function to notify user about newly created component

@csrf_exempt
def add_new_component(request):
    data = json.loads(request.POST['data'])
    args = data["args"]
    page_id = args['page_id']
    service_application = data["application"]
    integration_id = (
    YellowUserToken.objects.get(yellowant_integration_id=service_application)).yellowant_integration_id
    access_token = (YellowUserToken.objects.get(yellowant_integration_id=service_application)).yellowant_token

    service_application = str(integration_id)

    webhook_message = MessageClass()
    webhook_message.message_text = "New component added"
    attachment = MessageAttachmentsClass()
    attachment.title = "Get all component details"

    button_get_components = MessageButtonsClass()
    button_get_components.name = "1"
    button_get_components.value = "1"
    button_get_components.text = "Get all components"
    button_get_components.command = {
        "service_application": service_application,
        "function_name": 'all_component',
        "data": {
            'page_id': page_id
        }
    }

    attachment.attach_button(button_get_components)
    webhook_message.attach(attachment)
    print(integration_id)
    yellowant_user_integration_object = YellowAnt(access_token=access_token)
    send_message = yellowant_user_integration_object.create_webhook_message(
        requester_application=integration_id,
        webhook_name="new_component", **webhook_message.get_dict())
    return HttpResponse("OK", status=200)


@csrf_exempt
def yellowantapi(request):
    try:
        data = json.loads(request.POST['data'])
        args = data["args"]
        service_application = data["application"]
        verification_token = data['verification_token']
        function_id = data['function']
        function_name = data['function_name']
        print(data)
        if verification_token == settings.YELLOWANT_VERIFICATION_TOKEN:
        # Processing command in some class Command and sending a Message Object
            message = CommandCentre(data["user"], service_application, function_name, args).parse()
            if function_name == 'create_incident':
                add_new_incident(request)
            if function_name == 'create_component':
                add_new_component(request)
        # Returning message response
            return HttpResponse(message)
        else:
        # Handling incorrect verification token
            error_message = {"message_text": "Incorrect Verification token"}
            return HttpResponse(json.dumps(error_message), content_type="application/json")
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return HttpResponse("Something returned")

