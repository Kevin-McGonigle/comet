from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from api.serializers import *
from metrics.calculator import Calculator
from metrics.formatter import Formatter
from metrics.parsers.csharp.ast_generation_visitor import ASTGenerationVisitor as CSharpASTGenerationVisitor
from metrics.parsers.csharp.base.ModifiedCSharpLexer import CSharpLexer
from metrics.parsers.csharp.parser import CSharpParser
from metrics.parsers.python3.ast_generation_visitor import ASTGenerationVisitor as Python3ASTGenerationVisitor
from metrics.parsers.python3.base.Python3Lexer import Python3Lexer
from metrics.parsers.python3.parser import Python3Parser

calculator_args = {
    "py": {
        "lexer_type": Python3Lexer,
        "parser_type": Python3Parser,
        "visitor_type": Python3ASTGenerationVisitor,
    },
    "cs": {
        "lexer_type": CSharpLexer,
        "parser_type": CSharpParser,
        "visitor_type": CSharpASTGenerationVisitor,
    }
}


class FileUploadViewset(viewsets.ModelViewSet):
    """
    API endpoint to upload file data.
    """
    queryset = File.objects.all()
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = FileSerializer

    def create(self, request, *args, **kwargs):
        return_data = []
        data_dict = dict(request.data.lists())
        for i, file in enumerate(data_dict["name"]):
            data = {
                "name": file,
                "size": data_dict["size"][i],
                "file_type": data_dict["file_type"][i],
                "file": data_dict["file"][i]
            }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            file_name = str(self.queryset.get(hash=serializer.data['hash']).file)

            with open(f'../server/uploads/{file_name}') as f:
                content = f.read()

            calculator = Calculator(content, **(calculator_args[file_name.rsplit(".")[-1]]))
            formatter = Formatter(calculator, file_name)

            return_data.append(formatter.generate())

        return JsonResponse(return_data, status=status.HTTP_201_CREATED, safe=False)


class FileInformationViewset(viewsets.ModelViewSet):
    """
    API endpoint to return a file's information from a given hash
    """
    serializer_class = FileSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            file_hash = self.request.GET.get('hash', None)
            if file_hash is not None:
                return File.objects.all().filter(hash=file_hash)

            return File.objects.all()


class MethodViewpoint(viewsets.ModelViewSet):
    """
    API endpoint to return a method's information from a given hash
    """
    serializer_class = MethodSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            method_hash = self.request.GET.get('method_hash', None)
            if method_hash is not None:
                return Method.objects.all().filter(method_hash=method_hash)

            return Method.objects.all()


class ClassViewpoint(viewsets.ModelViewSet):
    """
    API endpoint to return a class' information from a given hash
    """
    serializer_class = ClassSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse({'hash': serializer.data['class_hash']}, status=status.HTTP_201_CREATED, safe=False)

    def get_queryset(self):
        if self.request.method == "GET":
            class_hash = self.request.GET.get('class_hash', None)
            if class_hash is not None:
                return Class.objects.all().filter(class_hash=class_hash)

            return Class.objects.all()
