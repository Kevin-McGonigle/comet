from unittest import TestCase
from unittest.mock import patch, MagicMock

from metrics.structures.ast import *
from metrics.structures.base.graph import Graph, Node


class TestAST(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    @patch.object(Graph, "accept")
    def test_accept(self, mock_accept: MagicMock, mock_visitor: MagicMock) -> None:
        """
        Test accept method.

        :param mock_accept: Mock of Graph's accept method.
        :param mock_visitor: Mock of ASTVisitor.
        """
        AST().accept(mock_visitor)
        mock_accept.assert_called_with(mock_visitor)


class TestASTNode(TestCase):
    def test_values(self) -> None:
        """
        Test values method.
        """
        node = ASTNode({"test": ASTNode()})

        self.assertEqual(node.values(), list(node.children.values()))

    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    @patch.object(Node, "accept")
    def test_accept(self, mock_accept: MagicMock, mock_visitor: MagicMock) -> None:
        """
        Test accept method.

        :param mock_accept: Mock of Node's accept method.
        :param mock_visitor: Mock of ASTVisitor.
        """
        ASTNode().accept(mock_visitor)
        mock_accept.assert_called_with(mock_visitor)


class TestASTIdentifierNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTIdentifierNode("test"), mock_visitor, mock_visitor.visit_identifier)


class TestASTLiteralNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTLiteralNode(ASTLiteralType.STRING, "test"), mock_visitor, mock_visitor.visit_literal)


class TestASTMultiplesNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTMultiplesNode([]), mock_visitor, mock_visitor.visit_multiples)


class TestASTStatementsNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTStatementsNode([]), mock_visitor, mock_visitor.visit_statements)


class TestASTExpressionsNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTExpressionsNode([]), mock_visitor, mock_visitor.visit_expressions)


class TestASTVariablesNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTVariablesNode([]), mock_visitor, mock_visitor.visit_variables)


class TestASTElementsNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTElementsNode([]), mock_visitor, mock_visitor.visit_elements)


class TestASTParametersNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTParametersNode([]), mock_visitor, mock_visitor.visit_parameters)


class TestASTArgumentsNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTArgumentsNode([]), mock_visitor, mock_visitor.visit_arguments)


class TestASTSubscriptsNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTSubscriptsNode([]), mock_visitor, mock_visitor.visit_subscripts)


class TestASTCatchesNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTCatchesNode([]), mock_visitor, mock_visitor.visit_catches)


class TestASTDecoratorsNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTDecoratorsNode([]), mock_visitor, mock_visitor.visit_decorators)


class TestASTSwitchSectionsNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTSwitchSectionsNode([]), mock_visitor, mock_visitor.visit_switch_sections)


class TestASTSwitchLabelsNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.
        
        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTSwitchLabelsNode([]), mock_visitor, mock_visitor.visit_switch_labels)


class TestASTVariableDeclarationsNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.

        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTVariableDeclarationsNode([]), mock_visitor, mock_visitor.visit_variable_declarations)


class TestASTConstantDeclarationsNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.

        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTConstantDeclarationsNode([]), mock_visitor, mock_visitor.visit_constant_declarations)


class TestASTAttributesNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.

        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTAttributesNode([]), mock_visitor, mock_visitor.visit_attributes)


class TestASTAttributeSectionsNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.

        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTAttributeSectionsNode([]), mock_visitor, mock_visitor.visit_attribute_sections)


class TestASTConstraintsClausesNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        """
        Test accept method.

        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTConstraintsClausesNode([]), mock_visitor, mock_visitor.visit_constraints_clauses)


class TestASTConstraintsNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock):
        """
        Test accept method.

        :param mock_visitor: Mock of ASTVisitor.
        """
        test_accept(ASTConstraintsNode([]), mock_visitor, mock_visitor.visit_constraints)


class TestASTStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTStatementNode(), mock_visitor, mock_visitor.visit_statement)


class TestASTDelStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTDelStatementNode(ASTNode({})), mock_visitor, mock_visitor.visit_del_statement)


class TestASTAssignmentStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTAssignmentStatementNode(ASTNode({}), ASTNode({})), mock_visitor,
                    mock_visitor.visit_assignment_statement)


class TestASTAugmentedAssignmentStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTAugmentedAssignmentStatementNode(ASTInPlaceOperation.ADD, ASTNode({}), ASTNode({})),
                    mock_visitor, mock_visitor.visit_augmented_assignment_statement)


class TestASTYieldStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTYieldStatementNode(), mock_visitor, mock_visitor.visit_yield_statement)


class TestASTPassStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTPassStatementNode(), mock_visitor, mock_visitor.visit_pass_statement)


class TestASTBreakStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTBreakStatementNode(), mock_visitor, mock_visitor.visit_break_statement)


class TestASTContinueStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTContinueStatementNode(), mock_visitor, mock_visitor.visit_continue_statement)


class TestASTReturnStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTReturnStatementNode(), mock_visitor, mock_visitor.visit_return_statement)


class TestASTThrowStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTThrowStatementNode(), mock_visitor, mock_visitor.visit_throw_statement)


class TestASTImportStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTImportStatementNode(ASTNode({})), mock_visitor, mock_visitor.visit_import_statement)


class TestASTGlobalStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTGlobalStatementNode(ASTNode({})), mock_visitor, mock_visitor.visit_global_statement)


class TestASTNonLocalStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTNonLocalStatementNode(ASTNode({})), mock_visitor, mock_visitor.visit_non_local_statement)


class TestASTAssertStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTAssertStatementNode(ASTNode({})), mock_visitor, mock_visitor.visit_assert_statement)


class TestASTIfStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTIfStatementNode(ASTNode({})), mock_visitor, mock_visitor.visit_if_statement)


class TestASTLoopStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTLoopStatementNode(ASTNode({})), mock_visitor, mock_visitor.visit_loop_statement)


class TestASTTryStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTTryStatementNode(ASTNode({})), mock_visitor, mock_visitor.visit_try_statement)


class TestASTWithStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTWithStatementNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_with_statement)


class TestASTNamespaceDeclarationNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTNamespaceDeclarationNode(ASTNode({})), mock_visitor, mock_visitor.visit_namespace_declaration)


class TestASTSwitchStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTSwitchStatementNode(ASTNode({})), mock_visitor, mock_visitor.visit_switch_statement)


class TestASTJumpStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTJumpStatementNode(ASTNode({})), mock_visitor, mock_visitor.visit_jump_statement)


class TestASTLockStatementNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTLockStatementNode(ASTNode({})), mock_visitor, mock_visitor.visit_lock_statement)


class TestASTExternAliasDirectiveNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTExternAliasDirectiveNode(ASTNode({})), mock_visitor, mock_visitor.visit_extern_alias_directive)


class TestASTVariableDeclarationNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTVariableDeclarationNode(ASTNode({})), mock_visitor, mock_visitor.visit_variable_declaration)


class TestASTConstantDeclarationNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTConstantDeclarationNode(ASTNode({}), ASTNode({}), ASTNode({})), mock_visitor,
                    mock_visitor.visit_constant_declaration)


class TestASTDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTDefinitionNode(ASTNode({})), mock_visitor, mock_visitor.visit_definition)


class TestASTClassDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTClassDefinitionNode(ASTNode({})), mock_visitor, mock_visitor.visit_class_definition)


class TestASTFunctionDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTFunctionDefinitionNode(ASTNode({})), mock_visitor, mock_visitor.visit_function_definition)


class TestASTEventDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTEventDefinitionNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_event_definition)


class TestASTConversionOperatorDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTConversionOperatorDefinitionNode(ASTNode({}), ASTConversionType.IMPLICIT, ASTNode({})),
                    mock_visitor, mock_visitor.visit_conversion_operator_definition)


class TestASTConstructorDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTConstructorDefinitionNode(ASTNode({})), mock_visitor, mock_visitor.visit_constructor_definition)


class TestASTDestructorDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTDestructorDefinitionNode(ASTNode({})), mock_visitor, mock_visitor.visit_destructor_definition)


class TestASTAccessorDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTAccessorDefinitionNode(ASTNode({})), mock_visitor, mock_visitor.visit_accessor_definition)


class TestASTStructDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTStructDefinitionNode(ASTNode({})), mock_visitor, mock_visitor.visit_struct_definition)


class TestASTInterfaceDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTInterfaceDefinitionNode(ASTNode({})), mock_visitor, mock_visitor.visit_interface_definition)


class TestASTPropertyDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTPropertyDefinitionNode(ASTNode({})), mock_visitor, mock_visitor.visit_property_definition)


class TestASTEnumDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTEnumDefinitionNode(ASTNode({})), mock_visitor, mock_visitor.visit_enum_definition)


class TestASTDelegateDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTDelegateDefinitionNode(ASTNode({})), mock_visitor, mock_visitor.visit_delegate_definition)


class TestASTIndexerDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTIndexerDefinitionNode(ASTNode({})), mock_visitor, mock_visitor.visit_indexer_definition)


class TestASTOperatorOverloadDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTOperatorOverloadDefinitionNode(ASTNode({})), mock_visitor,
                    mock_visitor.visit_operator_overload_definition)


class TestASTFixedSizeBufferDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTFixedSizeBufferDefinitionNode(ASTNode({})), mock_visitor,
                    mock_visitor.visit_fixed_size_buffer_definition)


class TestASTCatchNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTCatchNode(), mock_visitor, mock_visitor.visit_catch)


class TestASTFinallyNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTFinallyNode(), mock_visitor, mock_visitor.visit_finally)


class TestASTYieldExpressionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTYieldExpressionNode(), mock_visitor, mock_visitor.visit_yield_expression)


class TestASTBinaryOperationNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTBinaryOperationNode(ASTArithmeticOperation.ADD, ASTNode({}), ASTNode({})), mock_visitor,
                    mock_visitor.visit_binary_operation)


class TestASTUnaryOperationNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTUnaryOperationNode(ASTUnaryOperation.POSITIVE, ASTNode({})), mock_visitor,
                    mock_visitor.visit_unary_operation)


class TestASTAliasNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTAliasNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_alias)


class TestASTFromNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTFromNode(ASTNode({})), mock_visitor, mock_visitor.visit_from)


class TestASTAnonymousFunctionDefinitionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTAnonymousFunctionDefinitionNode(ASTNode({})), mock_visitor,
                    mock_visitor.visit_anonymous_function_definition)


class TestASTParameterNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTParameterNode(ASTNode({})), mock_visitor, mock_visitor.visit_parameter)


class TestASTPositionalOnlyParameterNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTPositionalOnlyParameterNode(ASTNode({})), mock_visitor,
                    mock_visitor.visit_positional_only_parameter)


class TestASTKeywordOnlyParameterNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTKeywordOnlyParameterNode(ASTNode({})), mock_visitor, mock_visitor.visit_keyword_only_parameter)


class TestASTPositionalArgumentsParameterNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTPositionalArgumentsParameterNode(ASTNode({})), mock_visitor,
                    mock_visitor.visit_positional_arguments_parameter)


class TestASTKeywordArgumentsParameterNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTKeywordArgumentsParameterNode(ASTNode({})), mock_visitor,
                    mock_visitor.visit_keyword_arguments_parameter)


class TestASTPositionalUnpackExpressionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTPositionalUnpackExpressionNode(ASTNode({})), mock_visitor,
                    mock_visitor.visit_positional_unpack_expression)


class TestASTKeywordUnpackExpressionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTKeywordUnpackExpressionNode(ASTNode({})), mock_visitor,
                    mock_visitor.visit_keyword_unpack_expression)


class TestASTAsyncNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTAsyncNode(ASTNode({})), mock_visitor, mock_visitor.visit_async)


class TestASTAwaitNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTAwaitNode(ASTNode({})), mock_visitor, mock_visitor.visit_await)


class TestASTMemberNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTMemberNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_member)


class TestASTAccessNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTAccessNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_access)


class TestASTIndexNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTIndexNode(ASTNode({})), mock_visitor, mock_visitor.visit_index)


class TestASTSliceNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTSliceNode(), mock_visitor, mock_visitor.visit_slice)


class TestASTCallNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTCallNode(ASTNode({})), mock_visitor, mock_visitor.visit_call)


class TestASTArgumentNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTArgumentNode(ASTNode({})), mock_visitor, mock_visitor.visit_argument)


class TestASTKeywordArgumentNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTKeywordArgumentNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_keyword_argument)


class TestASTGeneratorExpressionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTGeneratorExpressionNode(ASTNode({})), mock_visitor, mock_visitor.visit_generator_expression)


class TestASTComprehensionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTComprehensionNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_comprehension)


class TestASTListNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTListNode(ASTNode({})), mock_visitor, mock_visitor.visit_list)


class TestASTTupleNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTTupleNode(ASTNode({})), mock_visitor, mock_visitor.visit_tuple)


class TestASTSetNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTSetNode(ASTNode({})), mock_visitor, mock_visitor.visit_set)


class TestASTMapNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTMapNode(ASTNode({})), mock_visitor, mock_visitor.visit_map)


class TestASTKeyValuePairNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTKeyValuePairNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_key_value_pair)


class TestASTDecoratedNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTDecoratedNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_decorated)


class TestASTDecoratorNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTDecoratorNode(ASTNode({})), mock_visitor, mock_visitor.visit_decorator)


class TestASTConditionalExpressionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTConditionalExpressionNode(ASTNode({}), ASTNode({}), ASTNode({})), mock_visitor,
                    mock_visitor.visit_conditional_expression)


class TestASTNullCoalescingExpressionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTNullCoalescingExpressionNode(ASTNode({}), ASTNode({})), mock_visitor,
                    mock_visitor.visit_null_coalescing_expression)


class TestASTTypeCastNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTTypeCastNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_type_cast)


class TestASTTypeNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTTypeNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_type)


class TestASTObjectCreationNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTObjectCreationNode(), mock_visitor, mock_visitor.visit_object_creation)


class TestASTArrayCreationNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTArrayCreationNode(), mock_visitor, mock_visitor.visit_array_creation)


class TestASTInitializerNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTInitializerNode(), mock_visitor, mock_visitor.visit_initializer)


class TestASTQueryNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTQueryNode(ASTNode({})), mock_visitor, mock_visitor.visit_query)


class TestASTFromClauseNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTFromClauseNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_from_clause)


class TestASTLetClauseNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTLetClauseNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_let_clause)


class TestASTWhereClauseNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTWhereClauseNode(ASTNode({})), mock_visitor, mock_visitor.visit_where_clause)


class TestASTJoinClauseNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTJoinClauseNode(ASTNode({}), ASTNode({}), ASTNode({}), ASTNode({})), mock_visitor,
                    mock_visitor.visit_join_clause)


class TestASTOrderByClauseNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTOrderByClauseNode(ASTNode({})), mock_visitor, mock_visitor.visit_order_by_clause)


class TestASTOrderingNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTOrderingNode(ASTNode({})), mock_visitor, mock_visitor.visit_ordering)


class TestASTSelectClauseNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTSelectClauseNode(ASTNode({})), mock_visitor, mock_visitor.visit_select_clause)


class TestASTGroupByClauseNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTGroupByClauseNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_group_by_clause)


class TestASTIntoClauseNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTIntoClauseNode(ASTNode({})), mock_visitor, mock_visitor.visit_into_clause)


class TestASTLabelNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTLabelNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_label)


class TestASTSwitchSectionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTSwitchSectionNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_switch_section)


class TestASTCaseLabelNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTCaseLabelNode(ASTNode({})), mock_visitor, mock_visitor.visit_case_label)


class TestASTDefaultLabelNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTDefaultLabelNode(), mock_visitor, mock_visitor.visit_default_label)


class TestASTAttributeSectionNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTAttributeSectionNode(ASTNode({})), mock_visitor, mock_visitor.visit_attribute_section)


class TestASTAttributeNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTAttributeNode(ASTNode({})), mock_visitor, mock_visitor.visit_attribute)


class TestASTPointerTypeNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTPointerTypeNode(ASTNode({})), mock_visitor, mock_visitor.visit_pointer_type)


class TestASTNullableTypeNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTNullableTypeNode(ASTNode({})), mock_visitor, mock_visitor.visit_nullable_type)


class TestASTArrayTypeNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTArrayTypeNode(ASTNode({})), mock_visitor, mock_visitor.visit_array_type)


class TestASTConstraintsClauseNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTConstraintsClauseNode(ASTNode({}), ASTNode({})), mock_visitor,
                    mock_visitor.visit_constraints_clause)


class TestASTStackAllocationNode(TestCase):
    @patch("metrics.visitors.base.ast_visitor.ASTVisitor")
    def test_accept(self, mock_visitor: MagicMock) -> None:
        test_accept(ASTStackAllocationNode(ASTNode({}), ASTNode({})), mock_visitor, mock_visitor.visit_stack_allocation)


def test_accept(node: ASTNode, visitor: "ASTVisitor", visit_method: MagicMock) -> None:
    """
    General test for common accept behaviour.
    :param node: The node to test.
    :param visitor: The mocked visitor to accept.
    :param visit_method: The visit method to check for.
    """
    node.accept(visitor)
    visit_method.assert_called_with(node)
