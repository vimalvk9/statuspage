from django.http import HttpResponse
from django.shortcuts import render



from django.http import HttpResponse
from django.shortcuts import render
from yellowant import YellowAnt
from records.models import YellowUserToken, StatuspageUserToken,YellowAntRedirectState
import json


#   Sample login view

def UserLogin(request):
    return render(request,"login.html")

#  index function loads the home.html page

def index(request):
    print('test')

    context = {
        "user_integrations": []
    }
    if request.user.is_authenticated:
        user_integrations = YellowUserToken.objects.filter(user=request.user)
        print(user_integrations)
        for user_integration in user_integrations:
            context["user_integrations"].append(user_integration)

        return render(request, "home.html", context)
    else:
        UserLogin(request)

#   userdetails function shows the vital integration details of the user

def userdetails(request):
    print("in userdetails")
    user_integrations_list = []
    if request.user.is_authenticated:
        user_integrations = YellowUserToken.objects.filter(user=request.user)
        print(user_integrations)
        for user_integration in user_integrations:
            try:
                smut = StatuspageUserToken.objects.get(user_integration=user_integration)
                print(smut)
                user_integrations_list.append({"user_invoke_name":user_integration.yellowant_integration_invoke_name, "id":user_integration.id, "app_authenticated":True})
            except StatuspageUserToken.DoesNotExist:
                user_integrations_list.append({"user_invoke_name":user_integration.yellowant_integration_invoke_name, "id":user_integration.id, "app_authenticated":False})
    return HttpResponse(json.dumps(user_integrations_list), content_type="application/json")

#   delete_integration function deletes the particular integration

def delete_integration(request, id=None):
    print("In delete_integration")
    print(id)

    access_token_dict = YellowUserToken.objects.get(id=id)
    access_token = access_token_dict.yellowant_token
    print(access_token)
    user_integration_id = access_token_dict.yellowant_integration_id
    print(user_integration_id)
    url = "https://api.yellowant.com/api/user/integration/%s"%(user_integration_id)
    yellowant_user = YellowAnt(access_token=access_token)
    print(yellowant_user)
    yellowant_user.delete_user_integration(id=user_integration_id)
    response_json = YellowUserToken.objects.get(yellowant_token=access_token).delete()
    print(response_json)
    return HttpResponse("successResponse", status=204)

'''
def stateDetails(request, id=None):
    print("In stateDetails")
    print(id)
    app_redirect_details = YellowAntRedirectState.objects.get(user = id)
    state = app_redirect_details.state
    print(state) '''
