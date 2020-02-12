from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .serializers import *


@csrf_exempt
def file(request):
    if request.method == "GET":
        files_list = File.objects.all()
        serializer = FileSerializer(files_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        serializer = FileSerializer(data=JSONParser().parse(request))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    return HttpResponse(status=405)


@csrf_exempt
def file_detail(request, pk):
    try:
        f = File.objects.get(pk=pk)
    except File.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        return JsonResponse(FileSerializer(f).data)
    elif request.method == "PUT":
        serializer = FileSerializer(f, data=JSONParser().parse(request))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        f.delete()
        return HttpResponse(status=204)


@csrf_exempt
def class_(request):
    if request.method == "GET":
        classes_list = Class.objects.all()
        serializer = ClassSerializer(classes_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        serializer = ClassSerializer(data=JSONParser().parse(request))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    return HttpResponse(status=405)


@csrf_exempt
def class_detail(request, pk):
    try:
        c = Class.objects.get(pk=pk)
    except Class.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        return JsonResponse(ClassSerializer(c).data)
    elif request.method == "PUT":
        serializer = ClassSerializer(c, data=JSONParser().parse(request))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        c.delete()
        return HttpResponse(status=204)


@csrf_exempt
def method(request):
    if request.method == "GET":
        methods_list = Method.objects.all()
        serializer = MethodSerializer(methods_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        serializer = MethodSerializer(data=JSONParser().parse(request))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    return HttpResponse(status=405)


@csrf_exempt
def method_detail(request, pk):
    try:
        m = Method.objects.get(pk=pk)
    except Method.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        return JsonResponse(MethodSerializer(m).data)
    elif request.method == "PUT":
        serializer = MethodSerializer(m, data=JSONParser().parse(request))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        m.delete()
        return HttpResponse(status=204)
