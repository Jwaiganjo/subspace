import base64
import json

from django.shortcuts import render, redirect
from requests.auth import HTTPBasicAuth

from subspaceapp.models import Member, Products
from subspaceapp.forms import ProductsForm
from django.http import HttpResponse
from subspaceapp.credentials import LipanaMpesaPpassword,MpesaAccessToken,MpesaC2bCredential

import requests



# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def inner(request):
    return render(request, 'inner-page.html')

def subscription(request):
    return render(request, 'subscription.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        member = Member(fullname=request.POST['fullname'], username=request.POST['username'],
                        email=request.POST['email'], password=request.POST['password'])
        member.save()
        return redirect("/")
    else:
        return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def add(request):
    if request.method=="POST":
        form = ProductsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    else:
        form = ProductsForm()
        return render(request, "add.html",{'form':form})


def renewal(request):
    products = Products.objects.all()
    return render(request, 'renewal.html', {'products': products})

def delete(request, id):
    product = Products.objects.get(id=id)
    product.delete()
    return redirect('/renewal')

def edit(request, id):
    product = Products.objects.get(id=id)
    return render(request, 'edit.html', {'product': product})

def update(request, id):
    product = Products.objects.get(id=id)
    form = ProductsForm(request.POST, instance=product)
    if form.is_valid():
        form.save()
        return redirect('/renewal')
    else:
        return render(request, 'edit.html', {'product': product})

def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'pay.html')



def stk(request):
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Apen Softwares",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")