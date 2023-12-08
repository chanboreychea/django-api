import datetime
import os
from django.db.models import Q
from django.db import transaction
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from MyApp.models import Product, Sale, SaleDetail
from MyApp.serailizer import SaleSerializer


# Create your views here.
@api_view(["GET"])
def index(request):
    try:
        sale = Sale.objects.all()
        serializer = SaleSerializer(sale, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(str(ex))


@api_view(["POST"])
def sale_commit(request):
    try:
        with transaction.atomic():
            sale = Sale()
            sale.totalAmount = 0
            sale.createBy_id = request.data["createBy"]
            sale.save()

            saleId = Sale.objects.last()
            total = 0
            for i in range(len(request.data["saleDetail"])):
                saleDetail = SaleDetail()
                saleDetail.sale_id = saleId.id
                saleDetail.product_id = request.data["saleDetail"][i]["product_id"]
                product = Product.objects.get(pk=saleDetail.product_id)
                if product:
                    saleDetail.qty = request.data["saleDetail"][i]["qty"]
                    saleDetail.price = product.unitPrice
                    saleDetail.amount = saleDetail.qty * product.unitPrice
                    total += saleDetail.amount
                    saleDetail.save()

                    # if qty sale more than qtyInstock
                    product.qtyInstock = product.qtyInstock - saleDetail.qty
                    product.amount = product.amount - saleDetail.amount
                    product.save()

            sale1 = Sale.objects.get(pk=saleId.id)
            sale1.totalAmount = total
            sale1.save()

        transaction.commit()
        return Response({"message": "Insert Successfully"})
    except Exception as e:
        return Response(str(e))

    # product = Product()
    # sale = Sale()
    # sale.createBy_id = request.data["createBy"]
    # data = {"createBy": sale.createBy_id, "totalAmount": sale.totalAmount}
    # a = []
    # amount = 0
    # for i in range(len(request.data["saleDetail"])):
    #     product.id = request.data["saleDetail"][i]["product_id"]
    #     p = Product.objects.get(pk=product.id)
    #     product.qtyInstock = request.data["saleDetail"][i]["qty"]
    #     a.append(
    #         {
    #             "id": product.id,
    #             "qty": product.qtyInstock,
    #             "price": p.unitPrice,
    #             "amount": product.qtyInstock * p.unitPrice,
    #         }
    #     )
    #     amount += product.qtyInstock * p.unitPrice
    # sale.totalAmount = amount
    # return JsonResponse(
    #     {
    #         "createBy": sale.createBy_id,
    #         "totalAmount": sale.totalAmount,
    #         "saleDetail": a,
    #     },
    #     safe=False,
    # )


api_view(["GET"])


def show(request, id):
    try:
        sale = Sale.objects.get(pk=id)
    except Sale.DoesNotExist:
        return JsonResponse({"message": "Id " + id + " not found!"})
    serializer = SaleSerializer(sale)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
