import datetime
import os
from django.db.models import Q
from django.db import transaction
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from MyApp.models import Product, Purchase
from MyApp.serailizer import PurchaseSerializer


# Create your views here.
@api_view(["GET"])
def index(request):
    try:
        purchase = Purchase.objects.all()
        serializer = PurchaseSerializer(purchase, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(str(ex))


@api_view(["POST"])
def purchase_commit(request):
    try:
        with transaction.atomic():
            # average cost
            purchase = Purchase()
            purchase.createBy_id = request.data["createBy"]
            purchase.product_id = request.data["product_id"]
            purchase.qty = request.data["qty"]
            purchase.cost = request.data["cost"]
            purchase.total = purchase.qty * purchase.cost
            purchase.save()

            product = Product.objects.get(pk=purchase.product_id)
            if product:
                product.qtyInstock = product.qtyInstock + purchase.qty
                product.amount = product.amount + purchase.total
                product.unitPrice = product.amount / product.qtyInstock
                product.save()
                
        transaction.commit()
        return Response({"message": "Insert Successfully"})
    except Exception as e:
        return Response(str(e))


api_view(["GET"])


def show(request, id):
    try:
        purchase = Purchase.objects.get(pk=id)
    except Purchase.DoesNotExist:
        return JsonResponse({"message": "Id " + id + " not found!"})
    serializer = PurchaseSerializer(purchase)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
