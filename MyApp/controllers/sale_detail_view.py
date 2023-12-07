import datetime
import os
import json
from django.db.models import Q
from django.db import transaction
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from MyApp.models import SaleDetail
from MyApp.serailizer import SaleDetailSerializer


# Create your views here.
@api_view(["GET"])
def index(request):
    try:
        sale = SaleDetail.objects.all()
        serializer = SaleDetailSerializer(sale, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as ex:
        return JsonResponse(ex, status=status.HTTP_400_BAD_REQUEST)


api_view(["GET"])


def show(request, id):
    try:
        saleDetail = SaleDetail.objects.get(pk=id)
    except SaleDetail.DoesNotExist:
        return JsonResponse({"message": "Id " + id + " not found!"})
    serializer = SaleDetailSerializer(saleDetail)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
