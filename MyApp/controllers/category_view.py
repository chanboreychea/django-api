import datetime
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from MyApp.models import Category
from MyApp.serailizer import CategorySerializer


# Create your views here.
@api_view(["GET"])
def index(request):
    try:
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as ex:
        return JsonResponse(ex, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def store(request):
    category = Category()
    category.name = request.data["name"]
    category.createBy_id = request.data["createBy"]
    data = {"name": category.name, "createBy": category.createBy_id}
    serializer = CategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT"])
def update(request, id):
    try:
        category = Category.objects.get(pk=id)
    except Category.DoesNotExist:
        return JsonResponse({"message": "Id " + id + " not found!"})
    currentDate = datetime.datetime.now().strftime("%Y-%m-%d")
    category.name = request.data["name"]
    category.updateBy_id = request.data["updateBy"]

    data = {
        "name": category.name,
        "updateBy": category.updateBy_id,
        "updateAt": currentDate,
    }

    serializer = CategorySerializer(category, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(
            {"message": "Category Updated"}, status=status.HTTP_201_CREATED
        )
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE"])
def delete(request, id):
    try:
        category = Category.objects.get(pk=id)
    except Category.DoesNotExist:
        return JsonResponse({"message": "Id " + id + " not found!"})
    category.delete()
    return JsonResponse({"message": "Category Deleted"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def show(request, id):
    try:
        category = Category.objects.get(pk=id)
    except Category.DoesNotExist:
        return JsonResponse({"message": "Id " + id + " not found!"})
    serializer = CategorySerializer(category)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
