from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def login(request):
    return render(request, 'login.html')

@login_required(login_url='/')
def home(request):
    return render(request, 'home.html')

def logout(request):
    auth_logout(request)
    return redirect('/')


from rest_framework.views import APIView
from rest_framework.response import Response
from serializers import GmailSerializer
from google_client import get_message

class GmailListView(APIView):
    def get(self, request):
        mail_snippets = get_message()
        if mail_snippets:
            serializer = GmailSerializer(mail_snippets, many=True)
            return Response(serializer.data)

mail_list = GmailListView.as_view()
