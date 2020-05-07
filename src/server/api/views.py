from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from api.serializers import *
from metrics.visitors.base.inheritance_tree_visitor import InheritanceTreeVisitor
from metrics.calculator import CalculatorStub
from metrics.parsers.python3.ast_generation_visitor import ASTGenerationVisitor
from metrics.parsers.python3.base.Python3Lexer import Python3Lexer
from metrics.parsers.python3.base.Python3Parser import Python3Parser

calc_args = {
    "python3": {
        "parser": Python3Parser,
        "lexer": Python3Lexer,
        "visitor": ASTGenerationVisitor,
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
        print('REQUEST', request.data, request.FILES)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)


        file_name = str(self.queryset.get(hash=serializer.data['hash']).file)
        # with open(f'../server/uploads/{file_name}') as f:
        #    content = f.read()

        calc = CalculatorStub()
        # Structures
        inheritance_tree = InheritanceTreeVisitor().visit(calc.inheritance_tree(None))
        control_flow_graph = calc.control_flow_graph(None)
        dependency_graph = calc.dependency_graph(None)
        class_diagram = calc.class_diagram(None)
        # Metrics
        lloc = calc.logical_lines_of_code(None)
        ac = calc.afferent_coupling(None)
        ec = calc.efferent_coupling(None)
        cc = calc.cyclomatic_complexity(None)
        mid = calc.maximum_inheritance_depth(None)
        mnd = calc.maximum_nesting_depth(None)

        inheritance_tree_graph_data = {
            "nodes": [],
            "links": [],
        }

        def rec_visit(node):
            if len(node.subclasses) == 0:
                return node.name
            else:
                for item in node.subclasses:
                    return node.name, rec_visit(item)

        nodes = [rec_visit(node) for node in inheritance_tree]
        print(nodes)


        # nodes [{"id": A}, {"id": B}, {"id": C}, {"id": D}]
        # links [{"source": "object", "target": "A"}, {"source": "object", "target": "B"}
        # {"source": "A", "target": "C"}, {"source": "A", "target": "D"}, {"source": "B", "target": "D"}]

        print(inheritance_tree_graph_data)

        dependency_graph_graph_data = {
            "nodes": [],
            "links": [],
        }

        for node in dependency_graph.classes:
            dependency_graph_graph_data["nodes"].append({"id": node.name})

            for dependency in node.dependencies:
                dependency_graph_graph_data["links"].append({"source": dependency.name, "target": node.name})

        ac_graph_data = [{"name": node.name, "value": ac[node]} for node in ac]
        ec_graph_data = [{"name": node.name, "value": ec[node]} for node in ec]

        data_dict = {
            "fileName": "_".join(file_name.split("_")[2:]),
            "structures": {
                "controlFlowGraph": "cfg",
                "classDiagram": "cd",
                "inheritanceTree": "it",
                "abstractSyntaxTree": "ast",
                "dependencyGraph": dependency_graph_graph_data,
            },
            "metrics": {
                "afferentCoupling": ac_graph_data,
                "efferentCoupling": ec_graph_data,
                "logicalLinesOfCode": lloc,
                "cyclomaticComplexity": cc,
                "maximumInheritanceDepth": mid,
                "maximumNestingDepth": mnd,
            }
        }
        
        # Hardcoded for now
        # file_type = calc_args["python3"]
        # calc = Calculator(content, file_type['lexer'], file_type['parser'], file_type['visitor'])
        
        return JsonResponse(data_dict, status=status.HTTP_201_CREATED, safe=False)


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
