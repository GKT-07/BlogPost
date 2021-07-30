from django.shortcuts import render,  redirect


def goback(request):
    return redirect('api/')