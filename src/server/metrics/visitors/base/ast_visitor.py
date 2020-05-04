from typing import TYPE_CHECKING

from metrics.visitors.base.graph_visitor import GraphVisitor

if TYPE_CHECKING:
    from metrics.structures.ast import *


class ASTVisitor(GraphVisitor):
    """
    Abstract syntax tree visitor.

    Base class for visiting abstract syntax tree structures.
    """
    def visit(self, ast):
        """
        Visit an AST structure.
        :param ast: The AST to visit.
        :type ast: AST
        :return: The output of the visiting process.
        :rtype: Any
        """
        return super().visit(ast)

    @staticmethod
    def visit_identifier(node):
        """
        Visit AST identifier node.
        :param node: The AST identifier node.
        :type node: ASTIdentifierNode
        :return: The result of the visit.
        :rtype: Any
        """
        return node.name

    @staticmethod
    def visit_literal(node):
        """
        Visit AST literal node.
        :param node: The AST literal node.
        :type node: ASTLiteralNode
        :return: The result of the visit.
        :rtype: Any
        """
        return node.value

    def visit_multi(self, node):
        """
        Visit AST multi node.
        :param node: The AST multi node.
        :type node: ASTMultiNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_statements(self, node):
        """
        Visit AST statements node.
        :param node: The AST statements node.
        :type node: ASTStatementsNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_multi(node)

    def visit_expressions(self, node):
        """
        Visit AST expressions node.
        :param node: The AST expressions node.
        :type node: ASTExpressionsNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_multi(node)

    def visit_elements(self, node):
        """
        Visit AST elements node.
        :param node: The AST elements node.
        :type node: ASTElementsNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_multi(node)

    def visit_parameters(self, node):
        """
        Visit AST parameters node.
        :param node: The AST parameters node.
        :type node: ASTParametersNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_multi(node)

    def visit_arguments(self, node):
        """
        Visit AST arguments node.
        :param node: The AST arguments node.
        :type node: ASTArgumentsNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_multi(node)

    def visit_subscripts(self, node):
        """
        Visit AST subscripts node.
        :param node: The AST subscripts node.
        :type node: ASTSubscriptsNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_multi(node)

    def visit_catches(self, node):
        """
        Visit AST catches node.
        :param node: The AST catches node.
        :type node: ASTCatchesNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_multi(node)

    def visit_decorators(self, node):
        """
        Visit AST decorators node.
        :param node: The AST decorators node.
        :type node: ASTDecoratorsNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_multi(node)

    def visit_statement(self, node):
        """
        Visit AST statement node.
        :param node: The AST statement node.
        :type node: ASTStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_del_statement(self, node):
        """
        Visit AST delete statement node.
        :param node: The AST delete statement node.
        :type node: ASTDelStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_assignment_statement(self, node):
        """
        Visit AST assignment statement node.
        :param node: The AST assignment statement node.
        :type node: ASTAssignmentStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_augmented_assignment_statement(self, node):
        """
        Visit AST augmented assignment statement node.
        :param node: The AST augmented assignment statement node.
        :type node: ASTAugmentedAssignmentStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_annotated_assignment_statement(self, node):
        """
        Visit AST annotated assignment statement node.
        :param node: The AST annotated assignment statement node.
        :type node: ASTAnnotatedAssignmentStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_yield_statement(self, node):
        """
        Visit AST yield statement node.
        :param node: The AST yield statement node.
        :type node: ASTYieldStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_pass_statement(self, node):
        """
        Visit AST pass statement node.
        :param node: The AST pass statement node.
        :type node: ASTPassStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_break_statement(self, node):
        """
        Visit AST break statement node.
        :param node: The AST break statement node.
        :type node: ASTBreakStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_continue_statement(self, node):
        """
        Visit AST continue statement node.
        :param node: The AST continue statement node.
        :type node: ASTContinueStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_return_statement(self, node):
        """
        Visit AST return statement node.
        :param node: The AST return statement node.
        :type node: ASTReturnStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_throw_statement(self, node):
        """
        Visit AST throw statement node.
        :param node: The AST throw statement node.
        :type node: ASTThrowStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_import_statement(self, node):
        """
        Visit AST import statement node.
        :param node: The AST import statement node.
        :type node: ASTImportStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_global_statement(self, node):
        """
        Visit AST global statement node.
        :param node: The AST global statement node.
        :type node: ASTGlobalStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_non_local_statement(self, node):
        """
        Visit AST non-local statement node.
        :param node: The AST non-local statement node.
        :type node: ASTNonLocalStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_assert_statement(self, node):
        """
        Visit AST assert statement node.
        :param node: The AST assert statement node.
        :type node: ASTAssertStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_if_statement(self, node):
        """
        Visit AST if statement node.
        :param node: The AST if statement node.
        :type node: ASTIfStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_if_else_statement(self, node):
        """
        Visit AST if-else statement node.
        :param node: The AST if-else statement node.
        :type node: ASTIfElseStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_loop_statement(self, node):
        """
        Visit AST loop statement node.
        :param node: The AST loop statement node.
        :type node: ASTLoopStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_loop_else_statement(self, node):
        """
        Visit AST loop-else statement node.
        :param node: The AST loop-else statement node.
        :type node: ASTLoopElseStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_try_statement(self, node):
        """
        Visit AST try statement node.
        :param node: The AST try statement node.
        :type node: ASTTryStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_with_statement(self, node):
        """
        Visit AST with statement node.
        :param node: The AST with statement node.
        :type node: ASTWithStatementNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_function_definition(self, node):
        """
        Visit AST function definition node.
        :param node: The AST function definition node.
        :type node: ASTFunctionDefinitionNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_class_definition(self, node):
        """
        Visit AST class definition node.
        :param node: The AST class definition node.
        :type node: ASTClassDefinitionNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_yield_expression(self, node):
        """
        Visit AST yield expression node.
        :param node: The AST yield expression node.
        :type node: ASTYieldExpressionNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_catch(self, node):
        """
        Visit AST catch node.
        :param node: The AST catch node.
        :type node: ASTCatchNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_finally(self, node):
        """
        Visit AST finally node.
        :param node: The AST finally node.
        :type node: ASTFinallyNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_binary_operation(self, node):
        """
        Visit AST binary operation node.
        :param node: The AST binary operation node.
        :type node: ASTBinaryOperationNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_unary_operation(self, node):
        """
        Visit AST unary operation node.
        :param node: The AST unary operation node.
        :type node: ASTUnaryOperationNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_as(self, node):
        """
        Visit AST as node.
        :param node: The AST as node.
        :type node: ASTAliasNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_async(self, node):
        """
        Visit AST async node.
        :param node: The AST async node.
        :type node: ASTAsyncNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_parameter(self, node):
        """
        Visit AST parameter node.
        :param node: The AST parameter node.
        :type node: ASTParameterNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_positional_arguments_parameter(self, node):
        """
        Visit AST positional arguments parameter node.
        :param node: The AST positional arguments parameter node.
        :type node: ASTPositionalArgumentsParameterNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_keyword_arguments_parameter(self, node):
        """
        Visit AST keyword arguments parameter node.
        :param node: The AST keyword arguments parameter node.
        :type node: ASTKeywordArgumentsParameterNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_from(self, node):
        """
        Visit AST from node.
        :param node: The AST from node.
        :type node: ASTFromNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_anonymous_function_definition(self, node):
        """
        Visit AST anonymous function definition node.
        :param node: The AST anonymous function definition node.
        :type node: ASTAnonymousFunctionDefinitionNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_positional_unpack_expression(self, node):
        """
        Visit AST positional unpack expression node.
        :param node: The AST positional unpack expression node.
        :type node: ASTPositionalUnpackExpressionNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_keyword_unpack_expression(self, node):
        """
        Visit AST keyword unpack expression node.
        :param node: The AST keyword unpack expression node.
        :type node: ASTKeywordUnpackExpressionNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_await(self, node):
        """
        Visit AST await node.
        :param node: The AST await node.
        :type node: ASTAwaitNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_access(self, node):
        """
        Visit AST access node.
        :param node: The AST access node.
        :type node: ASTAccessNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_index(self, node):
        """
        Visit AST index node.
        :param node: The AST index node.
        :type node: ASTIndexNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_slice(self, node):
        """
        Visit AST slice node.
        :param node: The AST slice node.
        :type node: ASTSliceNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_call(self, node):
        """
        Visit AST call node.
        :param node: The AST call node.
        :type node: ASTCallNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_argument(self, node):
        """
        Visit AST argument node.
        :param node: The AST argument node.
        :type node: ASTArgumentNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_keyword_argument(self, node):
        """
        Visit AST keyword argument node.
        :param node: The AST keyword argument node.
        :type node: ASTKeywordArgumentNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_member(self, node):
        """
        Visit AST member node.
        :param node: The AST member node.
        :type node: ASTMemberNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_list(self, node):
        """
        Visit AST list node.
        :param node: The AST list node.
        :type node: ASTListNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_tuple(self, node):
        """
        Visit AST tuple node.
        :param node: The AST tuple node.
        :type node: ASTTupleNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_generator_expression(self, node):
        """
        Visit AST generator expression node.
        :param node: The AST generator expression node.
        :type node: ASTGeneratorExpressionNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_comprehension(self, node):
        """
        Visit AST comprehension node.
        :param node: The AST comprehension node.
        :type node: ASTComprehensionNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_map(self, node):
        """
        Visit AST map node.
        :param node: The AST map node.
        :type node: ASTMapNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_set(self, node):
        """
        Visit AST set node.
        :param node: The AST set node.
        :type node: ASTSetNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_key_value_pair(self, node):
        """
        Visit AST key-value pair node.
        :param node: The AST key-value pair node.
        :type node: ASTKeyValuePairNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_decorated(self, node):
        """
        Visit AST decorated node.
        :param node: The AST decorated node.
        :type node: ASTDecoratedNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)

    def visit_decorator(self, node):
        """
        Visit AST decorator node.
        :param node: The AST decorator node.
        :type node: ASTDecoratorNode
        :return: The result of the visit.
        :rtype: Any
        """
        return self.visit_children(node)
