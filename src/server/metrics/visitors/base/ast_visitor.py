from typing import TYPE_CHECKING, Any

from metrics.visitors.base.graph_visitor import GraphVisitor

if TYPE_CHECKING:
    from metrics.structures.ast import *


class ASTVisitor(GraphVisitor):
    """
    Abstract syntax tree visitor.

    Base class for visiting abstract syntax tree structures.
    """

    def visit(self, ast: "AST"):
        """
        Visit an AST structure.

        :param ast: The AST to visit.
        :return: The output of the visiting process.
        """
        return super().visit(ast)

    def visit_children(self, node: "ASTNode") -> Any:
        """
        Visit each of an AST node's children.

        :param node: The parent AST node whose children to visit.
        :return: Mapping of each child to their visit result.
        """
        return {child: child.accept(self) for child in node.children.values()}

    # region Terminals

    @staticmethod
    def visit_identifier(node: "ASTIdentifierNode"):
        """
        Visit AST identifier node.

        :param node: The AST identifier node to visit.
        :return: The result of the visit.
        """
        return node.name

    @staticmethod
    def visit_literal(node: "ASTLiteralNode"):
        """
        Visit AST literal node.

        :param node: The AST literal node to visit.
        :return: The result of the visit.
        """
        return node.value

    # endregion

    # region Multiples

    def visit_multiples(self, node: "ASTMultiplesNode"):
        """
        Visit AST multi node.

        :param node: The AST multi node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_statements(self, node: "ASTStatementsNode"):
        """
        Visit AST statements node.

        :param node: The AST statements node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_expressions(self, node: "ASTExpressionsNode"):
        """
        Visit AST expressions node.

        :param node: The AST expressions node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_variables(self, node: "ASTVariablesNode"):
        """
        Visit AST variables node.

        :param node: The AST variables node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_elements(self, node: "ASTElementsNode"):
        """
        Visit AST elements node.

        :param node: The AST elements node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_parameters(self, node: "ASTParametersNode"):
        """
        Visit AST parameters node.

        :param node: The AST parameters node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_arguments(self, node: "ASTArgumentsNode"):
        """
        Visit AST arguments node.

        :param node: The AST arguments node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_subscripts(self, node: "ASTSubscriptsNode"):
        """
        Visit AST subscripts node.

        :param node: The AST subscripts node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_catches(self, node: "ASTCatchesNode"):
        """
        Visit AST catches node.

        :param node: The AST catches node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_decorators(self, node: "ASTDecoratorsNode"):
        """
        Visit AST decorators node.

        :param node: The AST decorators node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_switch_sections(self, node: ASTSwitchSectionsNode):
        """
        Visit AST switch sections node.

        :param node: The AST switch sections node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_switch_labels(self, node: ASTSwitchLabelsNode):
        """
        Visit AST switch labels node.

        :param node: The AST switch labels node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_variable_declarations(self, node: ASTVariableDeclarationsNode):
        """
        Visit AST variable declarations node.

        :param node: The AST variable declarations node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_constant_declarations(self, node: ASTConstantDeclarationsNode):
        """
        Visit AST constant declarations node.

        :param node: The AST constant declarations node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_attributes(self, node: ASTAttributesNode):
        """
        Visit AST attributes node.

        :param node: The AST attributes node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_attribute_sections(self, node: ASTAttributeSectionsNode):
        """
        Visit AST attribute sections node.

        :param node: The AST attribute sections node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_constraints_clauses(self, node: ASTConstraintsClausesNode):
        """
        Visit AST constraints clauses node.

        :param node: The AST constraints clauses node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    def visit_constraints(self, node: ASTConstraintsNode):
        """
        Visit AST constraints  node.

        :param node: The AST constraints  node to visit.
        :return: The result of the visit.
        """
        return self.visit_multiples(node)

    # endregion

    # region Statements

    def visit_statement(self, node: ASTStatementNode):
        """
        Visit AST statement node.

        :param node: The AST statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_del_statement(self, node: "ASTDelStatementNode"):
        """
        Visit AST delete statement node.

        :param node: The AST delete statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_variable_declaration(self, node: "ASTVariableDeclarationNode"):
        """
        Visit AST variable declaration node.

        :param node: The AST variable declaration node to visit.
        :rtype: Any
        """
        return self.visit_statement(node)

    def visit_assignment_statement(self, node: "ASTAssignmentStatementNode"):
        """
        Visit AST assignment statement node.

        :param node: The AST assignment statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_augmented_assignment_statement(self, node: "ASTAugmentedAssignmentStatementNode"):
        """
        Visit AST augmented assignment statement node.

        :param node: The AST augmented assignment statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_annotated_assignment_statement(self, node: "ASTAnnotatedAssignmentStatementNode"):
        """
        Visit AST annotated assignment statement node.

        :param node: The AST annotated assignment statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_yield_statement(self, node: "ASTYieldStatementNode"):
        """
        Visit AST yield statement node.

        :param node: The AST yield statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_pass_statement(self, node: "ASTPassStatementNode"):
        """
        Visit AST pass statement node.

        :param node: The AST pass statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_break_statement(self, node: "ASTBreakStatementNode"):
        """
        Visit AST break statement node.

        :param node: The AST break statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_continue_statement(self, node: "ASTContinueStatementNode"):
        """
        Visit AST continue statement node.

        :param node: The AST continue statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_return_statement(self, node: "ASTReturnStatementNode"):
        """
        Visit AST return statement node.

        :param node: The AST return statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_throw_statement(self, node: "ASTThrowStatementNode"):
        """
        Visit AST throw statement node.

        :param node: The AST throw statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_import_statement(self, node: "ASTImportStatementNode"):
        """
        Visit AST import statement node.

        :param node: The AST import statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_global_statement(self, node: "ASTGlobalStatementNode"):
        """
        Visit AST global statement node.

        :param node: The AST global statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_non_local_statement(self, node: "ASTNonLocalStatementNode"):
        """
        Visit AST non-local statement node.

        :param node: The AST non-local statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_assert_statement(self, node: "ASTAssertStatementNode"):
        """
        Visit AST assert statement node.

        :param node: The AST assert statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_if_statement(self, node: "ASTIfStatementNode"):
        """
        Visit AST if statement node.

        :param node: The AST if statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_loop_statement(self, node: "ASTLoopStatementNode"):
        """
        Visit AST loop statement node.

        :param node: The AST loop statement node to visit.
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

    def visit_catch(self, node: "ASTCatchNode"):
        """
        Visit AST catch node.

        :param node: The AST catch node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_finally(self, node: "ASTFinallyNode"):
        """
        Visit AST finally node.

        :param node: The AST finally node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_with_statement(self, node: "ASTWithStatementNode"):
        """
        Visit AST with statement node.

        :param node: The AST with statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_namespace_declaration(self, node: ASTNamespaceDeclarationNode):
        """
        Visit AST namespace declaration node.

        :param node: The AST namespace declaration node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_switch_statement(self, node: ASTSwitchStatementNode):
        """
        Visit AST switch statement node.

        :param node: The AST switch statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_jump_statement(self, node: ASTJumpStatementNode):
        """
        Visit AST jump statement node.

        :param node: The AST jump statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_lock_statement(self, node: ASTLockStatementNode):
        """
        Visit AST lock statement node.

        :param node: The AST lock statement node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_extern_alias_directive(self, node: ASTExternAliasDirectiveNode):
        """
        Visit AST extern alias directive node.

        :param node: The AST extern alias directive node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_constant_declaration(self, node: ASTConstantDeclarationNode):
        """
        Visit AST constant declaration node.

        :param node: The AST constant declaration node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_function_definition(self, node: "ASTFunctionDefinitionNode"):
        """
        Visit AST function definition node.

        :param node: The AST function definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    def visit_class_definition(self, node: "ASTClassDefinitionNode"):
        """
        Visit AST class definition node.

        :param node: The AST class definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_statement(node)

    # region Definitions

    def visit_definition(self, node: ASTDefinitionNode):
        """
        Visit AST definition node.

        :param node: The AST definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_event_definition(self, node: ASTEventDefinitionNode):
        """
        Visit AST event definition node.

        :param node: The AST event definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_conversion_operator_definition(self, node: ASTConversionOperatorDefinitionNode):
        """
        Visit AST conversion operator definition node.

        :param node: The AST conversion operator definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_constructor_definition(self, node: ASTConstructorDefinitionNode):
        """
        Visit AST constructor definition node.

        :param node: The AST constructor definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_destructor_definition(self, node: ASTDestructorDefinitionNode):
        """
        Visit AST destructor definition node.

        :param node: The AST destructor definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_accessor_definition(self, node: ASTAccessorDefinitionNode):
        """
        Visit AST accessor definition node.

        :param node: The AST accessor definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_struct_definition(self, node: ASTStructDefinitionNode):
        """
        Visit AST struct definition node.

        :param node: The AST struct definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_interface_definition(self, node: ASTInterfaceDefinitionNode):
        """
        Visit AST interface definition node.

        :param node: The AST interface definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_property_definition(self, node: ASTPropertyDefinitionNode):
        """
        Visit AST property definition node.

        :param node: The AST property definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_enum_definition(self, node: ASTEnumDefinitionNode):
        """
        Visit AST enum definition node.

        :param node: The AST enum definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_delegate_definition(self, node: ASTDelegateDefinitionNode):
        """
        Visit AST delegate definition node.

        :param node: The AST delegate definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_indexer_definition(self, node: ASTIndexerDefinitionNode):
        """
        Visit AST indexer definition node.

        :param node: The AST indexer definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_operator_overload_definition(self, node: ASTOperatorOverloadDefinitionNode):
        """
        Visit AST operator overload definition node.

        :param node: The AST operator overload definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_fixed_size_buffer_definition(self, node: ASTFixedSizeBufferDefinitionNode):
        """
        Visit AST fixed size buffer definition node.

        :param node: The AST fixed size buffer definition node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    # endregion

    # endregion

    # region Expressions and Misc.

    def visit_yield_expression(self, node: "ASTYieldExpressionNode"):
        """
        Visit AST yield expression node.

        :param node: The AST yield expression node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_binary_operation(self, node: "ASTBinaryOperationNode"):
        """
        Visit AST binary operation node.

        :param node: The AST binary operation node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_unary_operation(self, node: "ASTUnaryOperationNode"):
        """
        Visit AST unary operation node.

        :param node: The AST unary operation node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_alias(self, node: "ASTAliasNode"):
        """
        Visit AST alias node.

        :param node: The AST alias node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_from(self, node: "ASTFromNode"):
        """
        Visit AST from node.

        :param node: The AST from node to visit.
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

    def visit_parameter(self, node: ASTParameterNode):
        """
        Visit AST parameter node.

        :param node: The AST parameter node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_positional_only_parameter(self, node: ASTPositionalOnlyParameterNode):
        """
        Visit AST positional-only parameter node.

        :param node: The AST positional-only parameter node to visit.
        :return: The result of the visit.
        """
        return self.visit_parameter(node)

    def visit_keyword_only_parameter(self, node: ASTKeywordOnlyParameterNode):
        """
        Visit AST keyword-only parameter node.

        :param node: The AST keyword-only parameter node to visit.
        :return: The result of the visit.
        """
        return self.visit_parameter(node)

    def visit_positional_arguments_parameter(self, node: ASTPositionalArgumentsParameterNode):
        """
        Visit AST positional arguments parameter node.

        :param node: The AST positional arguments parameter node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_keyword_arguments_parameter(self, node: "ASTKeywordArgumentsParameterNode"):
        """
        Visit AST keyword arguments parameter node.

        :param node: The AST keyword arguments parameter node to visit.
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

    def visit_keyword_unpack_expression(self, node: "ASTKeywordUnpackExpressionNode"):
        """
        Visit AST keyword unpack expression node.

        :param node: The AST keyword unpack expression node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_async(self, node: "ASTAsyncNode"):
        """
        Visit AST async node.

        :param node: The AST async node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_await(self, node: "ASTAwaitNode"):
        """
        Visit AST await node.

        :param node: The AST await node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_member(self, node: "ASTMemberNode"):
        """
        Visit AST member node.

        :param node: The AST member node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_access(self, node: "ASTAccessNode"):
        """
        Visit AST access node.

        :param node: The AST access node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_index(self, node: "ASTIndexNode"):
        """
        Visit AST index node.

        :param node: The AST index node.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_slice(self, node: "ASTSliceNode"):
        """
        Visit AST slice node.

        :param node: The AST slice node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_call(self, node: "ASTCallNode"):
        """
        Visit AST call node.

        :param node: The AST call node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_argument(self, node: "ASTArgumentNode"):
        """
        Visit AST argument node.

        :param node: The AST argument node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_keyword_argument(self, node: "ASTKeywordArgumentNode"):
        """
        Visit AST keyword argument node.

        :param node: The AST keyword argument node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_generator_expression(self, node: "ASTGeneratorExpressionNode"):
        """
        Visit AST generator expression node.

        :param node: The AST generator expression node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_comprehension(self, node: "ASTComprehensionNode"):
        """
        Visit AST comprehension node.

        :param node: The AST comprehension node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_list(self, node: "ASTListNode"):
        """
        Visit AST list node.

        :param node: The AST list node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_tuple(self, node: "ASTTupleNode"):
        """
        Visit AST tuple node.

        :param node: The AST tuple node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_set(self, node: "ASTSetNode"):
        """
        Visit AST set node.

        :param node: The AST set node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_map(self, node: "ASTMapNode"):
        """
        Visit AST map node.

        :param node: The AST map node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_key_value_pair(self, node: "ASTKeyValuePairNode"):
        """
        Visit AST key-value pair node.

        :param node: The AST key-value pair node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_decorated(self, node: "ASTDecoratedNode"):
        """
        Visit AST decorated node.

        :param node: The AST decorated node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_decorator(self, node: "ASTDecoratorNode"):
        """
        Visit AST decorator node.

        :param node: The AST decorator node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_conditional_expression(self, node: ASTConditionalExpressionNode):
        """
        Visit AST conditional expression node.

        :param node: The AST conditional expression node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_null_coalescing_expression(self, node: ASTNullCoalescingExpressionNode):
        """
        Visit AST null coalescing expression node.

        :param node: The AST null coalescing expression node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_type_cast(self, node: ASTTypeCastNode):
        """
        Visit AST type cast node.

        :param node: The AST type cast node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_type(self, node: ASTTypeNode):
        """
        Visit AST type node.

        :param node: The AST type node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_object_creation(self, node: ASTObjectCreationNode):
        """
        Visit AST object creation node.

        :param node: The AST object creation node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_array_creation(self, node: ASTArrayCreationNode):
        """
        Visit AST array creation node.

        :param node: The AST array creation node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_initializer(self, node: ASTInitializerNode):
        """
        Visit AST initializer node.

        :param node: The AST initializer node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_query(self, node: ASTQueryNode):
        """
        Visit AST query node.

        :param node: The AST query node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_from_clause(self, node: ASTFromClauseNode):
        """
        Visit AST from clause node.

        :param node: The AST from clause node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_let_clause(self, node: ASTLetClauseNode):
        """
        Visit AST let clause node.

        :param node: The AST let clause node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_where_clause(self, node: ASTWhereClauseNode):
        """
        Visit AST where clause node.

        :param node: The AST where clause node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_join_clause(self, node: ASTJoinClauseNode):
        """
        Visit AST join clause node.

        :param node: The AST join clause node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_order_by_clause(self, node: ASTOrderByClauseNode):
        """
        Visit AST order by clause node.

        :param node: The AST order by clause node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_ordering(self, node: ASTOrderingNode):
        """
        Visit AST ordering node.

        :param node: The AST ordering node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_select_clause(self, node: ASTSelectClauseNode):
        """
        Visit AST select clause node.

        :param node: The AST select clause node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_group_by_clause(self, node: ASTGroupByClauseNode):
        """
        Visit AST group by clause node.

        :param node: The AST group by clause node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_into_clause(self, node: ASTIntoClauseNode):
        """
        Visit AST into clause node.

        :param node: The AST into clause node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_label(self, node: ASTLabelNode):
        """
        Visit AST label node.

        :param node: The AST label node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_switch_section(self, node: ASTSwitchSectionNode):
        """
        Visit AST switch section node.

        :param node: The AST switch section node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_case_label(self, node: ASTCaseLabelNode):
        """
        Visit AST case label node.

        :param node: The AST case label node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_default_label(self, node: ASTDefaultLabelNode):
        """
        Visit AST default label node.

        :param node: The AST default label node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_attribute_section(self, node: ASTAttributeSectionNode):
        """
        Visit AST attribute section node.

        :param node: The AST attribute section node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_attribute(self, node: ASTAttributeNode):
        """
        Visit AST attribute node.

        :param node: The AST attribute node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_pointer_type(self, node: ASTPointerTypeNode):
        """
        Visit AST pointer type node.

        :param node: The AST pointer type node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_nullable_type(self, node: ASTNullableTypeNode):
        """
        Visit AST nullable type node.

        :param node: The AST nullable type node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_array_type(self, node: ASTArrayTypeNode):
        """
        Visit AST array type node.

        :param node: The AST array type node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_constraints_clause(self, node: ASTConstraintsClauseNode):
        """
        Visit AST constraints clause node.

        :param node: The AST constraints clause node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    def visit_stack_allocation(self, node: ASTStackAllocationNode):
        """
        Visit AST stack allocation node.

        :param node: The AST stack allocation node to visit.
        :return: The result of the visit.
        """
        return self.visit_children(node)

    # endregion
