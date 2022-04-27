from django.shortcuts import render
from django.conf import settings
import requests
from django.utils  import timezone

ms_identity_web = settings.MS_IDENTITY_WEB

def index(request):

    print(">>>>>>  Received request "+request.path+ " from " + request.META['REMOTE_ADDR']+"  <<<<<<")
    print(">>>>>>  Received Time "+str(timezone.now()))

    return render(request, "auth/status.html")

@ms_identity_web.login_required
def token_details(request):
    return render(request, 'auth/token.html' , context={"title":"Token Details"})

@ms_identity_web.login_required
def call_ms_graph(request):
    ms_identity_web.acquire_token_silently()
    graph = 'https://graph.microsoft.com/v1.0/users'
    authZ = f'Bearer {ms_identity_web.id_data._access_token}'
    results = requests.get(graph, headers={'Authorization': authZ}).json()


    print(results)

    if 'value' in results:
        results ['num_results'] = len(results['value'])
        results['value'] = results['value'][:20]

    context = {
        "results":results , 
        "title":"Tenant Users" 
    }
    return render(request, 'auth/call-graph.html', context=context)


@ms_identity_web.login_required
def get_a_user(request ,  user_id=None):
    ms_identity_web.acquire_token_silently()
    graph = 'https://graph.microsoft.com/v1.0/users/'+user_id
    authZ = f'Bearer {ms_identity_web.id_data._access_token}'
    results = requests.get(graph, headers={'Authorization': authZ}).json()

    
    print(results)
    if 'value' in results:
        
        results ['num_results'] = len(results['value'])
        results['value'] = results['value'][:20]
    context = {
        "object":results , 
        "title":"User Details for "+results['displayName'] 
    }
    return render(request, 'graph/view_user.html', context=context)

@ms_identity_web.login_required
def call_ms_graph(request):
    ms_identity_web.acquire_token_silently()
    graph = 'https://graph.microsoft.com/v1.0/users'
    authZ = f'Bearer {ms_identity_web.id_data._access_token}'
    results = requests.get(graph, headers={'Authorization': authZ}).json()

    print(results)

    if 'value' in results:
        results ['num_results'] = len(results['value'])
        results['value'] = results['value'][:20]

    context = {
        "results":results , 
        "title":"Tenant Users" 
    }
    return render(request, 'auth/call-graph.html', context=context)


@ms_identity_web.login_required
def userroles(request ,  user_id=None):
    ms_identity_web.acquire_token_silently()
    graph =  "https://graph.microsoft.com/v1.0/users/"+user_id+"/appRoleAssignments"
    authZ = f'Bearer {ms_identity_web.id_data._access_token}'
    results = requests.get(graph, headers={'Authorization': authZ}).json()
    
    print(results['value'])

    if 'value' in results:
        
        results ['num_results'] = len(results['value'])
        results['value'] = results['value'][:20]
    context = {
        "object":results['value'] , 
        "title":"Roles for user  "+user_id
    }
    return render(request, 'graph/user_roles.html', context=context)

@ms_identity_web.login_required
def allroles(request ):
    ms_identity_web.acquire_token_silently()
    graph = " https://graph.microsoft.com/v1.0/servicePrincipals/"
  
    authZ = f'Bearer {ms_identity_web.id_data._access_token}'
    results = requests.get(graph, headers={'Authorization': authZ}).json()

    
    print(results['value'].json)


   
    if 'value' in results:
        
        results ['num_results'] = len(results['value'])
        results['value'] = results['value'][:20]
    context = {
        "object":results['value'] , 
        "title":"Roles for user  "
    }
    return render(request, 'graph/allroles.html', context=context)
