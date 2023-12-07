import datetime
import os
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from MyApp.models import Product
from MyApp.serailizer import ProductSerializer


# Create your views here.
@api_view(["GET"])
def index(request):
    try:
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as ex:
        return JsonResponse(ex, safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def store(request):
    try:
        product = Product()
        product.name = request.data["name"]
        product.category_id = request.data["category"]
        product.createBy_id = request.data["createBy"]
        product.barcode = request.data["barcode"]
        product.unitPrice = request.data["unitPrice"]
        product.qtyInstock = request.data["qtyInstock"]
        product.amount = float(product.unitPrice) * int(product.qtyInstock)
        if len(request.data["photo"]) > 0:
            product.photo = request.data["photo"]
        else:
            product.photo = ""

        product.save()
        return JsonResponse({"message": "insert successfully"})
    except Exception as ex:
        return JsonResponse(str(ex), safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT"])
def update(request, id):
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Id " + id + " not found!"})

    currentDate = datetime.datetime.now().strftime("%Y-%m-%d")
    product.name = request.data["name"]
    product.updateBy_id = request.data["updateBy"]
    product.category_id = request.data["category"]
    product.barcode = request.data["barcode"]
    product.unitPrice = request.data["unitPrice"]
    product.qtyInstock = request.data["qtyInstock"]
    product.amount = product.unitPrice * product.qtyInstock

    if product.photo:
        if len(request.data["photo"]) > 0:
            os.remove(product.photo.path)
            product.photo = request.data["photo"]
    else:
        if len(request.data["photo"]) > 0:
            product.photo = request.data["photo"]
        else:
            product.photo = ""

    data = {
        "name": product.name,
        "category": product.category_id,
        "barcode": product.barcode,
        "unitPrice": product.unitPrice,
        "qtyInstock": product.qtyInstock,
        "amount": product.amount,
        "photo": product.photo,
        "createBy": 1,
        "updateBy": product.updateBy_id,
        "updateAt": currentDate,
    }

    serializer = ProductSerializer(product, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(
            {"message": "Product Updated"}, status=status.HTTP_201_CREATED
        )
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE"])
def delete(request, id):
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Id " + id + " not found!"})
    if product.photo:
        os.remove(product.photo.path)
    product.delete()
    return JsonResponse({"message": "Category Deleted"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def show(request, id):
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Id " + id + " not found!"})
    serializer = ProductSerializer(product)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def search(request):
    sname = request.GET.get("name")
    sid = request.GET.get("id")

    query = Q()

    if sname:
        query |= Q(name__icontains=sname)

    if sid:
        query |= Q(id=sid)

    product = Product.objects.filter(query)

    serializer = ProductSerializer(product, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
