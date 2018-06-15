""" This is the command centre for all the commands created in the YA developer console
    This file contains the logic to understand a user message request from YA
    and return a response in the format of a YA message object accordingly

"""

#from django.http import HttpResponse
#from yellowant import YellowAnt
import json
from yellowant.messageformat import MessageClass, MessageAttachmentsClass, AttachmentFieldsClass
from .models import StatuspageUserToken, YellowUserToken, PageDetail
#import traceback
import requests
#import datetime
#import pytz
from django.conf import settings

### Statuspage specific settings ###


# # Common part for the endpoints
# SP_API_BASE1 = "https://api.statuspage.io/v1/pages/"
# SP_API_BASE2 = "https://api.statuspage.io/v0/organizations/"
# END = ".json"
#
#
# # URL for getting page profile details
# USER_PROFILE_ENDPOINT = PAGE_ID + END
#
# # URL for getting components as well as creating components
# USER_COMPONENTS_ENDPOINT = PAGE_ID + "/components" + END
#
# # URL for getting incidents
# USER_ALL_INCIDENTS_ENDPOINT = PAGE_ID + "/incidents" + END
#
# # URL for getting unresolved incidents
# USER_UNRESOLVED_ENDPOINT = PAGE_ID + "/incidents/unresolved" + END
#
# # URL for creating incidents
# CREATE_INCIDENT = PAGE_ID + "/incidents" + END
#
# ### End of Statuspage specific settings ###


class CommandCentre(object):

    """ Handles user commands

        Args:
            yellowant_integration_id (int): The integration id of a YA user
            function_name (str): Invoke name of the command the user is calling
            args (dict): Any arguments required for the command to run
    """
    def __init__(self, yellowant_user_id, yellowant_integration_id, function_name, args):
        self.yellowant_user_id = yellowant_user_id
        self.yellowant_integration_id = yellowant_integration_id
        self.function_name = function_name
        self.args = args

    def parse(self):
        """
        Matching which function to call
        """

        self.commands = {
            'page_profile'  : self.page_profile,
            'all_component' : self.all_component,
            'all_incidents'  : self.all_incidents,
            'unresolved_incidents' : self.unresolved_incidents,
            'create_incident' : self.create_incident,
            'create_component' : self.create_component,
            'api_key'   : self.api_key,
            'all_page_ids' : self.all_page_ids
        }

        self.user_integration = YellowUserToken.objects.get\
            (yellowant_integration_id=self.yellowant_integration_id)

        self.statuspage_access_token_object = StatuspageUserToken.objects.\
            get(user_integration=self.user_integration)

        self.statuspage_access_token = self.statuspage_access_token_object.\
            statuspage_access_token



        self.headers = {
            "Authorization": "OAuth %s" %(self.statuspage_access_token),
            "Content-Type": "application/json"
        }

        return self.commands[self.function_name](self.args)


    def page_profile(self, args):
        """
        page_profile function gives relevant page deatils about
        the the page in the statuspage account

        """
        print("In Page Profile")
        page_id = args['page_id']

        # Get request from statuspage server
        #url = (settings.SP_API_BASE1 + settings.USER_PROFILE_ENDPOINT)
        url = (settings.SP_API_BASE1 + page_id + ".json")
        response = requests.get(url, headers=self.headers)

        if (response.status_code == requests.codes.ok):

            response_json = response.json()

            # print("--------------------------------\
            # ---------------------------------------------------")
            print(response_json)
            # Creating message objects to structure the message to be shown
            message = MessageClass()
            message.message_text = "Page Profile Details:"

            attachment = MessageAttachmentsClass()

            try:

                field1 = AttachmentFieldsClass()
                field1.title = "ID"
                field1.value = response_json['id']
                attachment.attach_field(field1)
            except:
                pass

            try:
                field2 = AttachmentFieldsClass()
                field2.title = "Name"
                field2.value = response_json['name']
                attachment.attach_field(field2)
            except:
                pass

            try:
                field3 = AttachmentFieldsClass()
                field3.title = "Created at"
                field3.value = response_json['created_at']
                attachment.attach_field(field3)
            except:
                pass

            try:
                field4 = AttachmentFieldsClass()
                field4.title = "Subdomain"
                field4.value = response_json['subdomain']
                attachment.attach_field(field4)
            except:
                pass

            try:
                field5 = AttachmentFieldsClass()
                field5.title = "Url"
                field5.value = response_json['url']
                attachment.attach_field(field5)
            except:
                pass

            message.attach(attachment)
            return message.to_json()
        else:

            return "{0}: {1}".format(response.status_code, response.text)

    def all_component(self, args):
        """
        all_component function gives the
        list of all components of the user's page
        """
        #print("In all components : ")
        page_id = args['page_id']

        # Get request from statuspage server
        #url = (settings.SP_API_BASE1 + settings.USER_COMPONENTS_ENDPOINT)
        url = settings.SP_API_BASE1 + page_id + "/components.json"
        response = requests.get(url, headers=self.headers)

        if (response.status_code == requests.codes.ok):
            response_json = response.json()

            print("all_component -------------------------------------------------")
            print(response_json)


            # Checking if response is empty or not
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

                    try:
                        field1 = AttachmentFieldsClass()
                        field1.title = "ID"
                        field1.value = response_json[i]['id']
                        attachment.attach_field(field1)
                    except:
                        pass

                    try:
                        field2 = AttachmentFieldsClass()
                        field2.title = "Name"
                        field2.value = response_json[i]['name']
                        attachment.attach_field(field2)
                    except:
                        pass

                    try:

                        field3 = AttachmentFieldsClass()
                        field3.title = "Status"
                        field3.value = response_json[i]['status']
                        attachment.attach_field(field3)
                    except:
                        pass

                    try:
                        field4 = AttachmentFieldsClass()
                        field4.title = "Updated at"
                        field4.value = response_json[i]['updated_at']
                        attachment.attach_field(field4)
                    except:
                        pass

                    try:
                        field5 = AttachmentFieldsClass()
                        field5.title = "Position"
                        field5.value = response_json[i]['position']
                        attachment.attach_field(field5)
                    except:
                        pass

                    try:
                        field6 = AttachmentFieldsClass()
                        field6.title = "Page Id"
                        field6.value = response_json[i]["page_id"]
                        attachment.attach_field(field6)
                    except:
                        pass


                    message.attach(attachment)
                return message.to_json()
        else:
            return "{0}: {1}".format(response.status_code, response.text)

    def all_incidents(self, args):
        """
        all_incidents function gives the list of all components of the user's page
        """
        #print("In all incidents")
        page_id = args['page_id']
        #data = {}

        # Get request from statuspage server
        url = (settings.SP_API_BASE1 + page_id + "/incidents.json")
        response = requests.get(url, headers=self.headers)

        if (response.status_code == requests.codes.ok):
            response_json = response.json()

            #print("----------------------------------------------\
            # -------------------------------------")
            print(response_json)

            # Checking if response json is empty or not
            if bool(response_json) == False:
                message = MessageClass()
                message.message_text = "No incidents : "
                #attachment = MessageAttachmentsClass()
                #field1 = AttachmentFieldsClass()
                #field1.title = "Number of incidents"
                #field1.value = "0"
                #attachment.attach_field(field1)
                return message.to_json()
            else:
                message = MessageClass()
                message.message_text = "All incidents : "
                for i in range(len(response_json)):
                    print(i)
                    attachment = MessageAttachmentsClass()

                    try:
                        field1 = AttachmentFieldsClass()
                        field1.title = "ID"
                        field1.value = response_json[i]['id']
                        attachment.attach_field(field1)
                    except:
                        pass

                    try:
                        field2 = AttachmentFieldsClass()
                        field2.title = "Name"
                        field2.value = response_json[i]['name']
                        attachment.attach_field(field2)
                    except:
                        pass

                    try:
                        field3 = AttachmentFieldsClass()
                        field3.title = "Status"
                        field3.value = response_json[i]['status']
                        attachment.attach_field(field3)
                    except:
                        pass

                    try:
                        field4 = AttachmentFieldsClass()
                        field4.title = "Updated at"
                        field4.value = response_json[i]['updated_at']
                        attachment.attach_field(field4)
                    except:
                        pass

                    try:
                        field5 = AttachmentFieldsClass()
                        field5.title = "Shortlink"
                        field5.value = response_json[i]['shortlink']
                        attachment.attach_field(field5)
                    except:
                        pass

                    try:
                        field6 = AttachmentFieldsClass()
                        field6.title = "Page Id"
                        field6.value = response_json[i]["page_id"]
                        attachment.attach_field(field6)
                    except:
                        pass

                    message.attach(attachment)
                return message.to_json()
        else:
            return "{0}: {1}".format(response.status_code, response.text)


    def unresolved_incidents(self, args):
        """
        unresolved_incidents function gives
        the list of all unresolved incidents of the user's page
        """

        print("In all unresolved incidents")
        page_id = args['page_id']

        # Get request from statuspage server
        url = (settings.SP_API_BASE1 + page_id + "/incidents/unresolved.json")
        response = requests.get(url, headers=self.headers)

        if (response.status_code == requests.codes.ok):
            response_json = response.json()

            # Check if response json is empty or not
            if bool(response_json) == False:
                message = MessageClass()
                message.message_text = "No unresolved incidents "
                #attachment = MessageAttachmentsClass()
                #field1 = AttachmentFieldsClass()
                #field1.title = "Number of unresolved incidents"
                #field1.value = "0"
                #attachment.attach_field(field1)
                return message.to_json()
            else:
                message = MessageClass()
                message.message_text = "All unresolved incidents : "
                for i in range(len(response_json)):
                    print(i)
                    attachment = MessageAttachmentsClass()
                    try:
                        field1 = AttachmentFieldsClass()
                        field1.title = "ID"
                        field1.value = response_json[i]['id']
                        attachment.attach_field(field1)
                    except:
                        pass

                    try:
                        field2 = AttachmentFieldsClass()
                        field2.title = "Name"
                        field2.value = response_json[i]['name']
                        attachment.attach_field(field2)
                    except:
                        pass

                    try:
                        field3 = AttachmentFieldsClass()
                        field3.title = "Status"
                        field3.value = response_json[i]['status']
                        attachment.attach_field(field3)
                    except:
                        pass

                    try:
                        field4 = AttachmentFieldsClass()
                        field4.title = "Updated at"
                        field4.value = response_json[i]['updated_at']
                        attachment.attach_field(field4)
                    except:
                        pass

                    try:
                        field5 = AttachmentFieldsClass()
                        field5.title = "Shortlink"
                        field5.value = response_json[i]['shortlink']
                        attachment.attach_field(field5)
                    except:
                        pass

                    try:
                        field6 = AttachmentFieldsClass()
                        field6.title = "Page Id"
                        field6.value = response_json[i]["page_id"]
                        attachment.attach_field(field6)
                    except:
                        pass

                    message.attach(attachment)
                return message.to_json()
        else:
            return "{0}: {1}".format(response.status_code, response.text)


    def create_incident(self, args):
        """
        create_incident function creates a new incident for a specific page of user
        """
        print("In create incident")
        print(args)
        page_id = args['page_id']
        status = args['status']
        components_id = args['components_id']
        name = args['name']
        body = args['body']

        data = {
            "incident" : {
                "name": name,
                "status": status,
	            "body": body,
	            "wants_twitter_update":"f",
	            "components_ids": components_id,
                "deliver_notifications":"true"
                }
            }

        # POST request to statuspage server
        url = (settings.SP_API_BASE1 + page_id + "/incidents.json")
        response = requests.post(url,headers=self.headers,json=data)

        if (response.status_code == requests.codes.ok):
            response_json = response.json()

            #print("------------------------------------")
            print(response_json)

            message = MessageClass()
            message.message_text = "New Incident Details:"

            attachment = MessageAttachmentsClass()

            try:
                field1 = AttachmentFieldsClass()
                field1.title = "ID"
                field1.value = response_json['id']
                attachment.attach_field(field1)
            except:
                pass

            try:
                field2 = AttachmentFieldsClass()
                field2.title = "Status"
                field2.value = response_json['status']
                attachment.attach_field(field2)
            except:
                pass

            message.attach(attachment)
            return message.to_json()
        else:
            return "{0}: {1}".format(response.status_code, response.text)


    def create_component(self, args):
        """
        create_component function creates a new component for a specific page of user
        """
        #print("In create component")
        page_id = args['page_id']
        name = args['name']
        description = args['description']
        data = {"component": {
                    "name": name,
                    "description": description
            }}

        # POST request to statuspage server
        url = settings.SP_API_BASE1 + page_id + "/components.json"
        response = requests.post(url, headers=self.headers, json=data)

        if (response.status_code == requests.codes.ok):
            response_json = response.json()
            #print("------------------------------------")
            #print(response_json)
            message = MessageClass()
            message.message_text = "New Component Details:"

            attachment = MessageAttachmentsClass()
            try:
                field1 = AttachmentFieldsClass()
                field1.title = "ID"
                field1.value = response_json['id']
                attachment.attach_field(field1)
            except:
                pass

            try:
                field2 = AttachmentFieldsClass()
                field2.title = "Status"
                field2.value = response_json['status']
                attachment.attach_field(field2)
            except:
                pass

            message.attach(attachment)
            return message.to_json()
        else:
            return "{0}: {1}".format(response.status_code, response.text)


    def api_key(self, args):
        """
        api_key function updates the user's api key in case it is regenerated by user
        """
        print("In api key")
        api = args['api']

        # Fetching object from database and updating the api_key and flag
        api_new = StatuspageUserToken.objects.get\
            (user_integration_id=self.user_integration)
        #print(api_new.statuspage_access_token)
        api_new.statuspage_access_token = api
        api_new.apikey_login_update_flag = True
        api_new.save()
        #print(api_new.statuspage_access_token)
        m = MessageClass()
        m.message_text = "Your api key is stored! \
        You can now access the account using the other commands."


        return m.to_json()


    ## Change
    def all_page_ids(self,args):
        '''
        Get all page ids for the user
        Basic inactive function to get dynamic inputs in  all other functions.
        '''

        sot = self.statuspage_access_token_object
        print(sot.user_integration_id)
        page_objects = PageDetail.objects.filter(user_integration_id=sot)


        m = MessageClass()
        data = []

        m.message_text = "Here are your pages"            #:\n" if len(page_objects) > 0 else "You don't have any pages."
        for page_object in page_objects:
            url = (settings.SP_API_BASE1 + page_object.page_id + ".json")
            response = requests.get(url, headers=self.headers)
            response_json = response.json()
            m.message_text += "{} - {}\n".format(response_json["name"], page_object.page_id)
            data.append({"name": response_json["name"],"page_id":str(page_object.page_id)})
        # m = MessageClass()
        # data = []
        # data.append({"page_id":"dfdsdfvd"})
        # m.message_text = "Lol"

        m.data = data
        print(m.data)
        return m.to_json()
