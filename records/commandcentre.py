# This is the command centre for all the commands created in the YA developer console


from django.http import HttpResponse
from yellowant import YellowAnt
import json
from yellowant.messageformat import MessageClass, MessageAttachmentsClass, MessageButtonsClass, AttachmentFieldsClass
from .models import StatuspageUserToken, YellowUserToken
import traceback
import requests
import datetime
import pytz
from django.conf import settings

class CommandCentre(object):
    def __init__(self,yellowant_user_id,yellowant_integration_id,function_name,args):
        self.yellowant_user_id = yellowant_user_id
        self.yellowant_integration_id = yellowant_integration_id
        self.function_name = function_name
        self.args = args

    def parse(self):
        self.commands = {
            'page_profile'  : self.page_profile,
            'all_component' : self.all_component,
            'all_incidents'  : self.all_incidents,
            'unresolved_incidents' : self.unresolved_incidents,
            'create_incident' : self.create_incident,
            'create_component' : self.create_component,
            'api_key'   : self.api_key,
        }

        self.user_integration = YellowUserToken.objects.get(yellowant_integration_id=self.yellowant_integration_id)
        self.statuspage_access_token_object = StatuspageUserToken.objects.get(user_integration=self.user_integration)
        self.statuspage_access_token = self.statuspage_access_token_object.statuspage_access_token
        self.headers = {
            "Authorization": "OAuth %s" %(self.statuspage_access_token),
            "Content-Type": "application/json"
        }

        return self.commands[self.function_name](self.args)

    # page_profile function gives relevant page deatils about the the page in the statuspage account

    def page_profile(self,args):
        print("In Page Profile")
        page_id = args['page_id']
        url = (settings.SP_API_BASE1 + settings.USER_PROFILE_ENDPOINT)
        response = requests.get(url, headers=self.headers)
        response_json = response.json()
        print("-----------------------------------------------------------------------------------")
        print(response_json)

        message = MessageClass()
        message.message_text = "Page Profile Details:"

        attachment = MessageAttachmentsClass()
        field1 = AttachmentFieldsClass()
        field1.title = "Incident Subscribers Allowed"
        field1.value = response_json['allow_incident_subscribers']
        attachment.attach_field(field1)

        field2 = AttachmentFieldsClass()
        field2.title = "Created at"
        field2.value = response_json['created_at']
        attachment.attach_field(field2)

        field6 = AttachmentFieldsClass()
        field6.title = "Subdomain"
        field6.value = response_json['subdomain']
        attachment.attach_field(field6)

        field3 = AttachmentFieldsClass()
        field3.title = "ID"
        field3.value = response_json['id']
        attachment.attach_field(field3)

        field4 = AttachmentFieldsClass()
        field4.title = "Last Update"
        field4.value = response_json['updated_at']
        attachment.attach_field(field4)

        message.attach(attachment)
        return message.to_json()

    # all_component function gives the list of all components of the user's page

    def all_component(self,args):
        print("In all components : ")
        page_id = args['page_id']
        url = (settings.SP_API_BASE1 + settings.USER_COMPONENTS_ENDPOINT)
        response = requests.get(url,headers=self.headers)
        response_json = response.json()
        print("-------------------------------------------------")
        print(response_json)

        if bool(response_json) == False:
            message = MessageClass()
            message.message_text = "All components : "
            attachment = MessageAttachmentsClass()
            field1 = AttachmentFieldsClass()
            field1.title = "Number of components"
            field1.value = "0"
            attachment.attach_field(field1)
            return message.to_json()
        else:
            message = MessageClass()
            message.message_text = "All components : "
            for i in range(len(response_json)):
                print(i)
                attachment = MessageAttachmentsClass()
                field1 = AttachmentFieldsClass()
                field1.title = "ID"
                field1.value = response_json[i]['id']
                attachment.attach_field(field1)

                field2 = AttachmentFieldsClass()
                field2.title = "Name"
                field2.value = response_json[i]['name']
                attachment.attach_field(field2)

                field3 = AttachmentFieldsClass()
                field3.title = "Status"
                field3.value = response_json[i]['status']
                attachment.attach_field(field3)

                field4 = AttachmentFieldsClass()
                field4.title = "Updated at"
                field4.value = response_json[i]['updated_at']
                attachment.attach_field(field4)

                field5 = AttachmentFieldsClass()
                field5.title = "Position"
                field5.value = response_json[i]['position']
                attachment.attach_field(field5)

                field6 = AttachmentFieldsClass()
                field6.title = "Page Id"
                field6.value = response_json[i]["page_id"]
                attachment.attach_field(field6)
                message.attach(attachment)
            return message.to_json()

    # all_incidents function gives the list of all components of the user's page

    def all_incidents(self,args):
        print("In all incidents")
        page_id = args['page_id']
        data = {}
        url = (settings.SP_API_BASE1 + settings.USER_ALL_INCIDENTS_ENDPOINT)
        response = requests.get(url, headers=self.headers)
        response_json = response.json()
        print("-----------------------------------------------------------------------------------")
        print(response_json)

        if bool(response_json) == False:
            message = MessageClass()
            message.message_text = "All incidents : "
            attachment = MessageAttachmentsClass()
            field1 = AttachmentFieldsClass()
            field1.title = "Number of incidents"
            field1.value = "0"
            attachment.attach_field(field1)
            return message.to_json()
        else:
            message = MessageClass()
            message.message_text = "All incidents : "
            for i in range(len(response_json)):
                print(i)
                attachment = MessageAttachmentsClass()
                field1 = AttachmentFieldsClass()
                field1.title = "ID"
                field1.value = response_json[i]['id']
                attachment.attach_field(field1)

                field2 = AttachmentFieldsClass()
                field2.title = "Name"
                field2.value = response_json[i]['name']
                attachment.attach_field(field2)

                field3 = AttachmentFieldsClass()
                field3.title = "Status"
                field3.value = response_json[i]['status']
                attachment.attach_field(field3)

                field4 = AttachmentFieldsClass()
                field4.title = "Updated at"
                field4.value = response_json[i]['updated_at']
                attachment.attach_field(field4)

                field5 = AttachmentFieldsClass()
                field5.title = "Shortlink"
                field5.value = response_json[i]['shortlink']
                attachment.attach_field(field5)

                field6 = AttachmentFieldsClass()
                field6.title = "Page Id"
                field6.value = response_json[i]["page_id"]
                attachment.attach_field(field6)
                message.attach(attachment)
            return message.to_json()

    # unresolved_incidents function gives the list of all unresolved incidents of the user's page

    def unresolved_incidents(self,args):
        print("In all unresolved incidents")
        page_id = args['page_id']
        url = (settings.SP_API_BASE1 + settings.USER_UNRESOLVED_ENDPOINT)
        response = requests.get(url, headers=self.headers)
        response_json = response.json()
        print("-----------------------------------------------------------------------------------")
        print(response_json)

        if bool(response_json) == False:
            message = MessageClass()
            message.message_text = "All unresolved incidents : "
            attachment = MessageAttachmentsClass()
            field1 = AttachmentFieldsClass()
            field1.title = "Number of unresolved incidents"
            field1.value = "0"
            attachment.attach_field(field1)
            return message.to_json()
        else:
            message = MessageClass()
            message.message_text = "All unresolved incidents : "
            for i in range(len(response_json)):
                print(i)
                attachment = MessageAttachmentsClass()
                field1 = AttachmentFieldsClass()
                field1.title = "ID"
                field1.value = response_json[i]['id']
                attachment.attach_field(field1)

                field2 = AttachmentFieldsClass()
                field2.title = "Name"
                field2.value = response_json[i]['name']
                attachment.attach_field(field2)

                field3 = AttachmentFieldsClass()
                field3.title = "Status"
                field3.value = response_json[i]['status']
                attachment.attach_field(field3)

                field4 = AttachmentFieldsClass()
                field4.title = "Updated at"
                field4.value = response_json[i]['updated_at']
                attachment.attach_field(field4)

                field5 = AttachmentFieldsClass()
                field5.title = "Shortlink"
                field5.value = response_json[i]['shortlink']
                attachment.attach_field(field5)

                field6 = AttachmentFieldsClass()
                field6.title = "Page Id"
                field6.value = response_json[i]["page_id"]
                attachment.attach_field(field6)
                message.attach(attachment)
            return message.to_json()

    # create_incident function creates a new incident for a specific page of user

    def create_incident(self,args):
        print("In create incident")
        page_id = args['page_id']

        data = {
            "incident" :{
	                    "name" 	: "Slow API Response Times",
	                    "status"	: "identified",
	                    "body" 	: "We've identified an issue with and are rolling back a recent code push that is causing slow API response times.",
	                    "wants_twitter_update" : "f",
	                    "components_ids" :["gynp8g27p5xw", "4g812xxgm6ws"],
                        "deliver_notifications" : "true"
                        }
        }

        url = (settings.SP_API_BASE1 + settings.CREATE_INCIDENT)
        response = requests.post(url,headers=self.headers,json=(data))
        response_json = response.json()
        print("------------------------------------")
        print(response_json)

        message = MessageClass()
        message.message_text = "New Incident Details:"

        attachment = MessageAttachmentsClass()
        field1 = AttachmentFieldsClass()
        field1.title = "ID"
        field1.value = response_json['id']
        attachment.attach_field(field1)

        field2 = AttachmentFieldsClass()
        field2.title = "Status"
        field2.value = response_json['status']
        attachment.attach_field(field2)
        message.attach(attachment)
        return message.to_json()

    # create_component function creates a new component for a specific page of user

    def create_component(self,args):
        print("In create component")
        page_id = args['page_id']

        data =  {"component":{
                    "name": "Widgets API",
                    "description": "The API to access all of the widgets"
                }}

        # url = https://api.statuspage.io/v1/pages/gvl671ncn9wm.json
        url = (settings.SP_API_BASE1 + settings.USER_COMPONENTS_ENDPOINT)
        response = requests.post(url, headers=self.headers, json=(data))
        response_json = response.json()

        print("------------------------------------")
        print(response_json)
        message = MessageClass()
        message.message_text = "New Component Details:"

        attachment = MessageAttachmentsClass()
        field1 = AttachmentFieldsClass()
        field1.title = "ID"
        field1.value = response_json['id']
        attachment.attach_field(field1)

        field2 = AttachmentFieldsClass()
        field2.title = "Status"
        field2.value = response_json['status']
        attachment.attach_field(field2)
        message.attach(attachment)
        return message.to_json()

    # api_key function updates the user's api key in case it is regenerated by user

    def api_key(self,args):
        print("In api key")
        api = args['api']
        api_new = StatuspageUserToken.objects.get(user_integration_id=self.user_integration)
        print(api_new.statuspage_access_token)
        api_new.statuspage_access_token  = api
        api_new.save()
        print(api_new.statuspage_access_token)
        m = MessageClass()
        m.message_text = "Your api key is stored! You can now access the account using the other commands."
        return m.to_json()
