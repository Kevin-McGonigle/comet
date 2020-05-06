from typing import TYPE_CHECKING, Any

from metrics.visitors.base.graph_visitor import GraphVisitor

if TYPE_CHECKING:
    from metrics.structures.ast import *


class ASTVisitor(GraphVisitor):
    """
    Abstract syntax tree visitor.

    Base class for visiting abstract syntax tree structures.
    """

    def visit(self, ast: AST):
        """
        Visit an AST structure.
        :param ast: The AST to visit.
        :return: The output of the visiting process.
        """
        return super().visit(ast)

    def visit_children(self, node: ASTNode) -> Any:
        """
        Visit each of an AST node's children.
        :param node: The parent AST node whose children to visit.
        :return: Mapping of each child to their visit result.
        """
        return {child: child.accept(self) for child in node.children}

    @staticmethod
    def visit_identifier(node: ASTIdentifierNode):
        """
        Visit AST identifier node.
        :param node: The AST identifier node to visit.
        :return: The result of the visit.
        """
        return node.name

    @staticmethod
    def visit_literal(node: ASTLiteralNode):
        """
        Visit AST literal node.
        :param node: The AST literal node to visit.
        :return: The result of the visit.
        """
        return node.value

    def visit_multiples(self, node: ASTMultiplesNode):
        """
        Visit AST multi node.
        :param node: The AST multi node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_statements(self, node: ASTStatementsNode):
        """
        Visit AST statements node.
        :param node: The AST statements node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_expressions(self, node: ASTExpressionsNode):
        """
        Visit AST expressions node.
        :param node: The AST expressions node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_variables(self, node: ASTVariablesNode):
        """
        Visit AST variables node.
        :param node: The AST variables node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_elements(self, node: ASTElementsNode):
        """
        Visit AST elements node.
        :param node: The AST elements node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_parameters(self, node: ASTParametersNode):
        """
        Visit AST parameters node.
        :param node: The AST parameters node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_arguments(self, node: ASTArgumentsNode):
        """
        Visit AST arguments node.
        :param node: The AST arguments node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_subscripts(self, node: ASTSubscriptsNode):
        """
        Visit AST subscripts node.
        :param node: The AST subscripts node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_catches(self, node: ASTCatchesNode):
        """
        Visit AST catches node.
        :param node: The AST catches node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_decorators(self, node: ASTDecoratorsNode):
        """
        Visit AST decorators node.
        :param node: The AST decorators node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_statement(self, node: ASTStatementNode):
        """
        Visit AST statement node.
        :param node: The AST statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_del_statement(self, node: ASTDelStatementNode):
        """
        Visit AST delete statement node.
        :param node: The AST delete statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_variable_declaration(self, node: ASTVariableDeclarationNode):
        """
        Visit AST variable declaration node.
        :param node: The AST variable declaration node to visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_assignment_statement(self, node: ASTAssignmentStatementNode):
        """
        Visit AST assignment statement node.
        :param node: The AST assignment statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_augmented_assignment_statement(self, node: ASTAugmentedAssignmentStatementNode):
        """
        Visit AST augmented assignment statement node.
        :param node: The AST augmented assignment statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_annotated_assignment_statement(self, node: ASTAnnotatedAssignmentStatementNode):
        """
        Visit AST annotated assignment statement node.
        :param node: The AST annotated assignment statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_yield_statement(self, node: ASTYieldStatementNode):
        """
        Visit AST yield statement node.
        :param node: The AST yield statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_pass_statement(self, node: ASTPassStatementNode):
        """
        Visit AST pass statement node.
        :param node: The AST pass statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_break_statement(self, node: ASTBreakStatementNode):
        """
        Visit AST break statement node.
        :param node: The AST break statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_continue_statement(self, node: ASTContinueStatementNode):
        """
        Visit AST continue statement node.
        :param node: The AST continue statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_return_statement(self, node: ASTReturnStatementNode):
        """
        Visit AST return statement node.
        :param node: The AST return statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_throw_statement(self, node: ASTThrowStatementNode):
        """
        Visit AST throw statement node.
        :param node: The AST throw statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_import_statement(self, node: ASTImportStatementNode):
        """
        Visit AST import statement node.
        :param node: The AST import statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_global_statement(self, node: ASTGlobalStatementNode):
        """
        Visit AST global statement node.
        :param node: The AST global statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_non_local_statement(self, node: ASTNonLocalStatementNode):
        """
        Visit AST non-local statement node.
        :param node: The AST non-local statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_assert_statement(self, node: ASTAssertStatementNode):
        """
        Visit AST assert statement node.
        :param node: The AST assert statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_if_statement(self, node: ASTIfStatementNode):
        """
        Visit AST if statement node.
        :param node: The AST if statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_if_else_statement(self, node: ASTIfElseStatementNode):
        """
        Visit AST if-else statement node.
        :param node: The AST if-else statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_loop_statement(self, node: ASTLoopStatementNode):
        """
        Visit AST loop statement node.
        :param node: The AST loop statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_loop_else_statement(self, node: ASTLoopElseStatementNode):
        """
        Visit AST loop-else statement node.
        :param node: The AST loop-else statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_try_statement(self, node: ASTTryStatementNode):
        """
        Visit AST try statement node.
        :param node: The AST try statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_catch(self, node: ASTCatchNode):
        """
        Visit AST catch node.
        :param node: The AST catch node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_finally(self, node: ASTFinallyNode):
        """
        Visit AST finally node.
        :param node: The AST finally node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_with_statement(self, node: ASTWithStatementNode):
        """
        Visit AST with statement node.
        :param node: The AST with statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_function_definition(self, node: ASTFunctionDefinitionNode):
        """
        Visit AST function definition node.
        :param node: The AST function definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_class_definition(self, node: ASTClassDefinitionNode):
        """
        Visit AST class definition node.
        :param node: The AST class definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_yield_expression(self, node: ASTYieldExpressionNode):
        """
        Visit AST yield expression node.
        :param node: The AST yield expression node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_binary_operation(self, node: ASTBinaryOperationNode):
        """
        Visit AST binary operation node.
        :param node: The AST binary operation node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_unary_operation(self, node: ASTUnaryOperationNode):
        """
        Visit AST unary operation node.
        :param node: The AST unary operation node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_alias(self, node: ASTAliasNode):
        """
        Visit AST alias node.
        :param node: The AST alias node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_from(self, node: ASTFromNode):
        """
        Visit AST from node.
        :param node: The AST from node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_parameter(self, node: ASTParameterNode):
        """
        Visit AST parameter node.
        :param node: The AST parameter node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_positional_arguments_parameter(self, node: ASTPositionalArgumentsParameterNode):
        """
        Visit AST positional arguments parameter node.
        :param node: The AST positional arguments parameter node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_keyword_arguments_parameter(self, node: ASTKeywordArgumentsParameterNode):
        """
        Visit AST keyword arguments parameter node.
        :param node: The AST keyword arguments parameter node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_anonymous_function_definition(self, node: ASTAnonymousFunctionDefinitionNode):
        """
        Visit AST anonymous function definition node.
        :param node: The AST anonymous function definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_positional_unpack_expression(self, node: ASTPositionalUnpackExpressionNode):
        """
        Visit AST positional unpack expression node.
        :param node: The AST positional unpack expression node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_keyword_unpack_expression(self, node: ASTKeywordUnpackExpressionNode):
        """
        Visit AST keyword unpack expression node.
        :param node: The AST keyword unpack expression node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_async(self, node: ASTAsyncNode):
        """
        Visit AST async node.
        :param node: The AST async node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_await(self, node: ASTAwaitNode):
        """
        Visit AST await node.
        :param node: The AST await node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_member(self, node: ASTMemberNode):
        """
        Visit AST member node.
        :param node: The AST member node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_access(self, node: ASTAccessNode):
        """
        Visit AST access node.
        :param node: The AST access node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_index(self, node: ASTIndexNode):
        """
        Visit AST index node.
        :param node: The AST index node.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_slice(self, node: ASTSliceNode):
        """
        Visit AST slice node.
        :param node: The AST slice node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_call(self, node: ASTCallNode):
        """
        Visit AST call node.
        :param node: The AST call node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_argument(self, node: ASTArgumentNode):
        """
        Visit AST argument node.
        :param node: The AST argument node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_keyword_argument(self, node: ASTKeywordArgumentNode):
        """
        Visit AST keyword argument node.
        :param node: The AST keyword argument node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_generator_expression(self, node: ASTGeneratorExpressionNode):
        """
        Visit AST generator expression node.
        :param node: The AST generator expression node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_comprehension(self, node: ASTComprehensionNode):
        """
        Visit AST comprehension node.
        :param node: The AST comprehension node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_list(self, node: ASTListNode):
        """
        Visit AST list node.
        :param node: The AST list node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_tuple(self, node: ASTTupleNode):
        """
        Visit AST tuple node.
        :param node: The AST tuple node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_set(self, node: ASTSetNode):
        """
        Visit AST set node.
        :param node: The AST set node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_map(self, node: ASTMapNode):
        """
        Visit AST map node.
        :param node: The AST map node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_key_value_pair(self, node: ASTKeyValuePairNode):
        """
        Visit AST key-value pair node.
        :param node: The AST key-value pair node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_decorated(self, node: ASTDecoratedNode):
        """
        Visit AST decorated node.
        :param node: The AST decorated node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_decorator(self, node: ASTDecoratorNode):
        """
        Visit AST decorator node.
        :param node: The AST decorator node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)
