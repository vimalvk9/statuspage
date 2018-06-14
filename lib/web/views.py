"""
Functions corresponding to URL patterns of web app

"""

#from django.http import HttpResponse
#from django.http import HttpResponseRedirect
#from django.shortcuts import render

import json
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from yellowant import YellowAnt
from ..records.models import YellowUserToken, StatuspageUserToken, PageDetail
from statuspage import settings


def index(request, path):
    """ Loads the homepage of the app.
        index function loads the home.html page
    """
    #print('test')

    # context = {
    #
    # }

    # Check if user is authenticated otherwise redirect user to login page

    context = {
                "base_href": settings.BASE_HREF,
                "application_id": settings.YA_APP_ID,
                "user_integrations": []
             }

    if request.user.is_authenticated:
        user_integrations = YellowUserToken.objects.filter(user=request.user.id)
        print(user_integrations)
        # for user_integration in user_integrations:
        #     context["user_integrations"].append(user_integration)



    return render(request, "home.html", context)
    # else:
    #     return HttpResponse("Please login !")

def user_list_view(request):
    """
    userdetails function shows the vital integration details of the user

    """
    #print("in userdetails")
    user_integrations_list = []

    # Check if user is authenticated otherwise redirect user to login page
    if request.user.is_authenticated:
        user_integrations = YellowUserToken.objects.filter(user=request.user.id)
        print(user_integrations)
        for user_integration in user_integrations:
            try:
                smut = StatuspageUserToken.objects.get(user_integration=user_integration)
                print(smut)
                user_integrations_list.append({"user_invoke_name":user_integration.\
                                              yellowant_integration_invoke_name,
                                               "id":user_integration.id, "app_authenticated":True,
                                               "is_valid":smut.apikey_login_update_flag})
            except StatuspageUserToken.DoesNotExist:
                user_integrations_list.append({"user_invoke_name":user_integration.\
                                              yellowant_integration_invoke_name,
                                               "id":user_integration.id, "app_authenticated":False})
    return HttpResponse(json.dumps(user_integrations_list), content_type="application/json")

@csrf_exempt
def user_detail_update_delete_view(request, id=None):
    """
    delete_integration function deletes the particular integration
    """

    #print("In user_detail_update_delete_view")
    #print(id)
    user_integration_id = id

    if request.method == "GET":
        # return user data
        smut = StatuspageUserToken.objects.get(user_integration=user_integration_id)
        # ct = PageDetail.objects.count()
        # pages = [None]*ct
        #
        # if smut.apikey_login_update_flag == True:
        #
        #     for page in range(0,ct):
        #         pages[page] = "*************"
        #
        #     return HttpResponse(json.dumps({
        #         "is_valid": smut.apikey_login_update_flag,
        #         "pages": pages,
        #         "api_key": "****************************************",
        #     }))
        #
        # else:
        return HttpResponse(json.dumps({
                "is_valid": smut.apikey_login_update_flag,
                "pages": [""],
                "api_key" : "",
                "email" : ""
            }))

    elif request.method == "DELETE":

        access_token_dict = YellowUserToken.objects.get(id=id)
        user_id = access_token_dict.user
        #print(access_token)
        if user_id == request.user.id:
            access_token = access_token_dict.yellowant_token
            user_integration_id = access_token_dict.yellowant_integration_id
            #print(user_integration_id)
            url = "https://api.yellowant.com/api/user/integration/%s"%(user_integration_id)
            yellowant_user = YellowAnt(access_token=access_token)
            #print(yellowant_user)
            yellowant_user.delete_user_integration(id=user_integration_id)
            response = YellowUserToken.objects.get(yellowant_token=access_token).delete()
            #print(response)
            return HttpResponse("successResponse", status=200)
        else:
            return HttpResponse("Not Authenticated", status=403)

    elif request.method == "PUT":

        data = json.loads(request.body.decode("utf-8"))
        print(data)
        api_key = data['statuspage_api_key']
        pages = data['pages']
        user_integration = data['user_integration']
        email = str(data['email'])


        print(email)

        headers = {
            "Authorization": "OAuth %s" % (api_key),
            "Content-Type": "application/json"
        }

        for page in pages:
            page_id = page
            url = "https://api.statuspage.io/v1/pages/" + page_id + ".json"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print("Invalid")
                return HttpResponse(json.dumps({
                    "ok": False,
                    "is_valid": False
                    }))
            else:
                print("Valid")
                sp_object = StatuspageUserToken.objects.get(user_integration_id=user_integration)
                print(sp_object.statuspage_access_token)
                sp_object.statuspage_access_token = api_key
                page_detail_object = PageDetail.objects.create(user_integration_id=user_integration,
                                                               page_id=page_id)
                sp_object.apikey_login_update_flag = True
                sp_object.save()
                print(sp_object.statuspage_access_token)
                print(page_detail_object.page_id)

                ### Subscribing for webhooks


                webhook_id = sp_object.webhook_id
                print(webhook_id)
                endpoint = settings.BASE_URL + "/webhook/" + str(webhook_id) + "/"
                print(endpoint)
                for page in pages:
                    page_id = page

                    # Endpoint
                    url = "https://api.statuspage.io/v1/pages/" + page_id + "/subscribers" + settings.END

                    payload = {
                        "subscriber": {
                            "email": email,
                            "endpoint": endpoint,
                            }
                        }

                    response = requests.post(url, headers=headers, json=payload)
                    print(response.json())


        return HttpResponse(json.dumps({
                "ok": True,
                "is_valid": True
            }))

