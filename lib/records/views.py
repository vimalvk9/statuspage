""" This file contains all functions corresponding to their urls"""


from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from yellowant import YellowAnt
import json
import uuid
from yellowant.messageformat import MessageClass, \
    MessageAttachmentsClass, MessageButtonsClass
import traceback
from django.views.decorators.csrf import csrf_exempt
from .models import YellowUserToken, YellowAntRedirectState, \
     AppRedirectState, StatuspageUserToken, PageDetail
from .commandcentre import CommandCentre
from django.contrib.auth.models import User


def redirectToYellowAntAuthenticationPage(request):

    '''Initiate the creation of a new user integration on YA
       YA uses oauth2 as its authorization framework.
       This method requests for an oauth2 code from YA to start creating a
       new user integration for this application on YA.
    '''

    # Generate a unique ID to identify the user when YA returns an oauth2 code
    user = User.objects.get(id=request.user.id)
    state = str(uuid.uuid4())

    # Save the relation between user and state so that we can identify the user
    # when YA returns the oauth2 code
    YellowAntRedirectState.objects.create(user=user.id, state=state)

    # Redirect the application user to the YA authentication page.
    # Note that we are passing state, this app's client id,
    # oauth response type as code, and the url to return the oauth2 code at.
    return HttpResponseRedirect("{}?state={}&client_id={}&response_type=code&redirect_url={}".format
                                (settings.YELLOWANT_OAUTH_URL, state, settings.YELLOWANT_CLIENT_ID,
                                 settings.YELLOWANT_REDIRECT_URL))


def yellowantRedirecturl(request):

    ''' Receive the oauth2 code from YA to generate a new user integration
        This method calls utilizes the YA Python SDK to create a new user integration on YA.
        This method only provides the code for creating a new user integration on YA.
        Beyond that, you might need to authenticate the user on
        the actual application (whose APIs this application will be calling) and store a relation
        between these user auth details and the YA user integration.
    '''

    # Oauth2 code from YA, passed as GET params in the url
    code = request.GET.get('code')

    # The unique string to identify the user for which we will create an integration
    state = request.GET.get("state")

    # Fetch user with help of state from database
    yellowant_redirect_state = YellowAntRedirectState.objects.get(state=state)
    user = yellowant_redirect_state.user

    # Initialize the YA SDK client with your application credentials
    y = YellowAnt(app_key=settings.YELLOWANT_CLIENT_ID,
                  app_secret=settings.YELLOWANT_CLIENT_SECRET,
                  access_token=None, redirect_uri=settings.YELLOWANT_REDIRECT_URL)

    # Getting the acccess token
    access_token_dict = y.get_access_token(code)
    access_token = access_token_dict['access_token']

    # Getting YA user details
    yellowant_user = YellowAnt(access_token=access_token)
    profile = yellowant_user.get_user_profile()

    # Creating a new user integration for the application
    user_integration = yellowant_user.create_user_integration()
    hash_str = str(uuid.uuid4()).replace("-", "")[:25]
    ut = YellowUserToken.objects.create(user=user, yellowant_token=access_token,
                                        yellowant_id=profile['id'],
                                        yellowant_integration_invoke_name=user_integration\
                                            ["user_invoke_name"],
                                        yellowant_integration_id=user_integration\
                                            ['user_application'],
                                        webhook_id=hash_str)
    state = str(uuid.uuid4())
    AppRedirectState.objects.create(user_integration=ut, state=state)
    sp_token = ""                 # "11649b9b-ea84-47fa-aecb-9faf3ab447bd"
    page_id = ""
    sut = StatuspageUserToken.objects.create(user_integration=ut, statuspage_access_token=sp_token, webhook_id=hash_str)

    #print("------------------")
    #print(sut.user_integration_id)

    ''' No need to create a page detail object here '''
    #page_detail_object = PageDetail.objects.create(user_integration_id=sut.user_integration_id, page_id=page_id)
    #print(page_detail_object)
    # Redirecting to home page
    return HttpResponseRedirect("/")




@csrf_exempt
def webhook(request,hash_str=""):
    print("In webhook")
    data = (request.body.decode('utf-8'))
    response_json = json.loads(data)
    print(response_json)

    if "incident" not in response_json:
        update_component(request,hash_str)
    else:
        update_incident(request,hash_str)

    return HttpResponse("OK",status=200)


def update_incident(request,webhook_id):
    print("In update_incident")
    """
    Webhook function to notify user about update in incident
    """

    # Extracting necessary data
    data = (request.body.decode('utf-8'))
    response_json = json.loads(data)

    page_id = response_json['page']['id']
    unsubscribe = response_json['meta']['unsubscribe']
    incident_id = response_json['incident']['id']
    name = response_json['incident']['name']

    try:
        # Fetching yellowant object
        yellow_obj = YellowUserToken.objects.get(webhook_id=webhook_id)
        print(yellow_obj)
        access_token = yellow_obj.yellowant_token
        print(access_token)
        integration_id = yellow_obj.yellowant_integration_id
        service_application = str(integration_id)
        print(service_application)

        # Creating message object for webhook message

        webhook_message = MessageClass()
        webhook_message.message_text = "Updates in incident with Id : " + str(incident_id) + "\nName : " + str(name)
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
        #print(integration_id)

        # Creating yellowant object
        yellowant_user_integration_object = YellowAnt(access_token=access_token)

        # Sending webhook message to user
        send_message = yellowant_user_integration_object.create_webhook_message(
        requester_application=integration_id,
        webhook_name="incident_updates_webhook", **webhook_message.get_dict())
        return HttpResponse("OK", status=200)

    except YellowUserToken.DoesNotExist:
        return HttpResponse("Not Authorized", status=403)


def update_component(request,webhook_id):
    print("In update_component")
    """
    Webhook function to notify user about update in component
    """

    #Extracting necessary data
    data = (request.body.decode('utf-8'))
    response_json = json.loads(data)
    print(response_json)

    page_id = response_json['page']['id']
    unsubscribe = response_json['meta']['unsubscribe']
    component_id = response_json['component_update']['id']
    component_old_status = response_json['component_update']['old_status']
    component_new_status = response_json['component_update']['new_status']
    name = response_json['component']['name']


        # Fetching yellowant object
    try:
        yellow_obj = YellowUserToken.objects.get(webhook_id=webhook_id)
        print(yellow_obj)
        access_token = yellow_obj.yellowant_token
        print(access_token)
        integration_id = yellow_obj.yellowant_integration_id
        service_application = str(integration_id)
        print(service_application)


        # Creating message object for webhook message
        webhook_message = MessageClass()
        webhook_message.message_text = "Updates in component with Id : " + str(component_id) + "\nName : " + str(name) \
        + "\nStatus changed from " + str(component_old_status) + " to " + str(component_new_status)

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
        #print(integration_id)

        # Creating yellowant object
        yellowant_user_integration_object = YellowAnt(access_token=access_token)

        # Sending webhook message to user
        send_message = yellowant_user_integration_object.create_webhook_message(
        requester_application=integration_id,
        webhook_name="component_updates_webhook", **webhook_message.get_dict())

        return HttpResponse("OK", status=200)

    except YellowUserToken.DoesNotExist:
        return HttpResponse("Not Authorized", status=403)

@csrf_exempt
def yellowantapi(request):
    try:
        """
        Recieve user commands from YA
        """
        # Extracting the necessary data
        print("In yellowant api")
        data = json.loads(request.POST['data'])
        args = data["args"]
        service_application = data["application"]
        verification_token = data['verification_token']
        function_name = data['function_name']
        # print(data)

        # Verifying whether the request is actually from YA using verification token
        if verification_token == settings.YELLOWANT_VERIFICATION_TOKEN:
            print("--------")
            print(data)
            print("--------")


        # Processing command in some class Command and sending a Message Object
            message = CommandCentre(data["user"], service_application, function_name, args).parse()

        # Returning message response
            return HttpResponse(message)
        else:
            # Handling incorrect verification token
            error_message = {"message_text": "Incorrect Verification token"}
            return HttpResponse(json.dumps(error_message), content_type="application/json")

    except Exception as e:
        # Handling exception
        print(str(e))
        traceback.print_exc()
        return HttpResponse("Something went wrong !")

