from typing import TYPE_CHECKING

from metrics.visitors.base.ast_visitor import ASTVisitor

if TYPE_CHECKING:
    from metrics.structures.ast import *


class ASTFormattingVisitor(ASTVisitor):
    def visit(self, ast: "AST"):
        return super().visit(ast)

    def visit_children(self, node: "ASTNode"):
        return [child.accept(self) for child in node.children.values() if child is not None] if node.children else None

    @staticmethod
    def visit_identifier(node: "ASTIdentifierNode"):
        return {"name": node.name}

    @staticmethod
    def visit_literal(node: "ASTLiteralNode"):
        return {"name": node.value}

    def visit_multiples(self, node: "ASTMultiplesNode"):
        return {"name": "Multiples", "children": self.visit_children(node)}

    def visit_statements(self, node: "ASTStatementsNode"):
        return {"name": "Statements", "children": self.visit_children(node)}

    def visit_expressions(self, node: "ASTExpressionsNode"):
        return {"name": "Expressions", "children": self.visit_children(node)}

    def visit_variables(self, node: "ASTVariablesNode"):
        return {"name": "Variables", "children": self.visit_children(node)}

    def visit_elements(self, node: "ASTElementsNode"):
        return {"name": "Elements", "children": self.visit_children(node)}

    def visit_parameters(self, node: "ASTParametersNode"):
        return {"name": "Parameters", "children": self.visit_children(node)}

    def visit_arguments(self, node: "ASTArgumentsNode"):
        return {"name": "Arguments", "children": self.visit_children(node)}

    def visit_subscripts(self, node: "ASTSubscriptsNode"):
        return {"name": "Subscripts", "children": self.visit_children(node)}

    def visit_catches(self, node: "ASTCatchesNode"):
        return {"name": "Catches", "children": self.visit_children(node)}

    def visit_decorators(self, node: "ASTDecoratorsNode"):
        return {"name": "Decorators", "children": self.visit_children(node)}

    def visit_statement(self, node: "ASTStatementNode"):
        return {"name": "Statement", "children": self.visit_children(node)}

    def visit_del_statement(self, node: "ASTDelStatementNode"):
        return {"name": "Del statement", "children": self.visit_children(node)}

    def visit_variable_declaration(self, node: "ASTVariableDeclarationNode"):
        return {"name": "Variable declaration", "children": self.visit_children(node)}

    def visit_assignment_statement(self, node: "ASTAssignmentStatementNode"):
        return {"name": "Assignment statement", "children": self.visit_children(node)}

    def visit_augmented_assignment_statement(self, node: "ASTAugmentedAssignmentStatementNode"):
        return {"name": f"Augmented Assignment: {node.operation}", "children": self.visit_children(node)}

    def visit_annotated_assignment_statement(self, node: "ASTAnnotatedAssignmentStatementNode"):
        return {"name": "Annotated Assignment", "children": self.visit_children(node)}

    def visit_yield_statement(self, node: "ASTYieldStatementNode"):
        return {"name": "Yield statement", "children": self.visit_children(node)}

    def visit_pass_statement(self, node: "ASTPassStatementNode"):
        return {"name": "Pass statement", "children": self.visit_children(node)}

    def visit_break_statement(self, node: "ASTBreakStatementNode"):
        return {"name": "Break statement", "children": self.visit_children(node)}

    def visit_continue_statement(self, node: "ASTContinueStatementNode"):
        return {"name": "Continue statement", "children": self.visit_children(node)}

    def visit_return_statement(self, node: "ASTReturnStatementNode"):
        return {"name": "Return statement", "children": self.visit_children(node)}

    def visit_throw_statement(self, node: "ASTThrowStatementNode"):
        return {"name": "Throw statement", "children": self.visit_children(node)}

    def visit_import_statement(self, node: "ASTImportStatementNode"):
        return {"name": "Import statement", "children": self.visit_children(node)}

    def visit_global_statement(self, node: "ASTGlobalStatementNode"):
        return {"name": "Global statement", "children": self.visit_children(node)}

    def visit_non_local_statement(self, node: "ASTNonLocalStatementNode"):
        return {"name": "Non-local statement", "children": self.visit_children(node)}

    def visit_assert_statement(self, node: "ASTAssertStatementNode"):
        return {"name": "Assert statement", "children": self.visit_children(node)}

    def visit_if_statement(self, node: "ASTIfStatementNode"):
        return {"name": "If statement", "children": self.visit_children(node)}

    def visit_loop_statement(self, node: "ASTLoopStatementNode"):
        return {"name": "Loop statement", "children": self.visit_children(node)}

    def visit_try_statement(self, node: "ASTTryStatementNode"):
        return {"name": "Try statement", "children": self.visit_children(node)}

    def visit_catch(self, node: "ASTCatchNode"):
        return {"name": "Catch clause", "children": self.visit_children(node)}

    def visit_finally(self, node: "ASTFinallyNode"):
        return {"name": "Finally clause", "children": self.visit_children(node)}

    def visit_with_statement(self, node: "ASTWithStatementNode"):
        return {"name": "With statement", "children": self.visit_children(node)}

    def visit_function_definition(self, node: "ASTFunctionDefinitionNode"):
        return {"name": "Function definition", "children": self.visit_children(node)}

    def visit_class_definition(self, node: "ASTClassDefinitionNode"):
        return {"name": "Class definition", "children": self.visit_children(node)}

    def visit_yield_expression(self, node: "ASTYieldExpressionNode"):
        return {"name": "Yield expression", "children": self.visit_children(node)}

    def visit_binary_operation(self, node: "ASTBinaryOperationNode"):
        return {"name": f"Binary operation: {node.operation}", "children": self.visit_children(node)}

    def visit_unary_operation(self, node: "ASTUnaryOperationNode"):
        return {"name": f"Unary operation: {node.operation}", "children": self.visit_children(node)}

    def visit_alias(self, node: "ASTAliasNode"):
        return {"name": "Alias", "children": self.visit_children(node)}

    def visit_from(self, node: "ASTFromNode"):
        return {"name": "From", "children": self.visit_children(node)}

    def visit_parameter(self, node: "ASTParameterNode"):
        return {"name": "Parameter", "children": self.visit_children(node)}

    def visit_positional_arguments_parameter(self, node: "ASTPositionalArgumentsParameterNode"):
        return {"name": "Positional arguments parameter", "children": self.visit_children(node)}

    def visit_keyword_arguments_parameter(self, node: "ASTKeywordArgumentsParameterNode"):
        return {"name": "Keyword arguments parameter", "children": self.visit_children(node)}

    def visit_anonymous_function_definition(self, node: "ASTAnonymousFunctionDefinitionNode"):
        return {"name": "Anonymous function definition", "children": self.visit_children(node)}

    def visit_positional_unpack_expression(self, node: "ASTPositionalUnpackExpressionNode"):
        return {"name": "Positional unpack expression", "children": self.visit_children(node)}

    def visit_keyword_unpack_expression(self, node: "ASTKeywordUnpackExpressionNode"):
        return {"name": "Keyword unpack expression", "children": self.visit_children(node)}

    def visit_async(self, node: "ASTAsyncNode"):
        return {"name": "Async", "children": self.visit_children(node)}

    def visit_await(self, node: "ASTAwaitNode"):
        return {"name": "Await", "children": self.visit_children(node)}

    def visit_member(self, node: "ASTMemberNode"):
        return {"name": "Member", "children": self.visit_children(node)}

    def visit_access(self, node: "ASTAccessNode"):
        return {"name": "Access", "children": self.visit_children(node)}

    def visit_index(self, node: "ASTIndexNode"):
        return {"name": "Index", "children": self.visit_children(node)}

    def visit_slice(self, node: "ASTSliceNode"):
        return {"name": "Slice", "children": self.visit_children(node)}

    def visit_call(self, node: "ASTCallNode"):
        return {"name": "Call", "children": self.visit_children(node)}

    def visit_argument(self, node: "ASTArgumentNode"):
        return {"name": "Argument", "children": self.visit_children(node)}

    def visit_keyword_argument(self, node: "ASTKeywordArgumentNode"):
        return {"name": "Keyword argument", "children": self.visit_children(node)}

    def visit_generator_expression(self, node: "ASTGeneratorExpressionNode"):
        return {"name": "Generator expression", "children": self.visit_children(node)}

    def visit_comprehension(self, node: "ASTComprehensionNode"):
        return {"name": "Comprehension", "children": self.visit_children(node)}

    def visit_list(self, node: "ASTListNode"):
        return {"name": "List", "children": self.visit_children(node)}

    def visit_tuple(self, node: "ASTTupleNode"):
        return {"name": "Tuple", "children": self.visit_children(node)}

    def visit_set(self, node: "ASTSetNode"):
        return {"name": "Set", "children": self.visit_children(node)}

    def visit_map(self, node: "ASTMapNode"):
        return {"name": "Map", "children": self.visit_children(node)}

    def visit_key_value_pair(self, node: "ASTKeyValuePairNode"):
        return {"name": "Key-value pair", "children": self.visit_children(node)}

    def visit_decorated(self, node: "ASTDecoratedNode"):
        return {"name": "Decorated", "children": self.visit_children(node)}

    def visit_decorator(self, node: "ASTDecoratorNode"):
        return {"name": "Decorator", "children": self.visit_children(node)}

    def visit_switch_sections(self, node: "ASTSwitchSectionsNode"):
        return {"name": "Switch sections", "children": self.visit_children(node)}

    def visit_switch_labels(self, node: "ASTSwitchLabelsNode"):
        return {"name": "Switch labels", "children": self.visit_children(node)}

    def visit_variable_declarations(self, node: "ASTVariableDeclarationsNode"):
        return {"name": "Variable declarations", "children": self.visit_children(node)}

    def visit_constant_declarations(self, node: "ASTConstantDeclarationsNode"):
        return {"name": "Constant declarations", "children": self.visit_children(node)}

    def visit_attributes(self, node: "ASTAttributesNode"):
        return {"name": "Attributes", "children": self.visit_children(node)}

    def visit_attribute_sections(self, node: "ASTAttributeSectionsNode"):
        return {"name": "Attribute", "children": self.visit_children(node)}

    def visit_constraints_clauses(self, node: "ASTConstraintsClausesNode"):
        return {"name": "Constraints clauses", "children": self.visit_children(node)}

    def visit_constraints(self, node: "ASTConstraintsNode"):
        return {"name": "Constraints", "children": self.visit_children(node)}

    def visit_namespace_declaration(self, node: "ASTNamespaceDeclarationNode"):
        return {"name": "Namespace declaration", "children": self.visit_children(node)}

    def visit_switch_statement(self, node: "ASTSwitchStatementNode"):
        return {"name": "Switch statement", "children": self.visit_children(node)}

    def visit_jump_statement(self, node: "ASTJumpStatementNode"):
        return {"name": "Jump statement", "children": self.visit_children(node)}

    def visit_lock_statement(self, node: "ASTLockStatementNode"):
        return {"name": "Lock statement", "children": self.visit_children(node)}

    def visit_extern_alias_directive(self, node: "ASTExternAliasDirectiveNode"):
        return {"name": "Extern aliasd directive", "children": self.visit_children(node)}

    def visit_constant_declaration(self, node: "ASTConstantDeclarationNode"):
        return {"name": "Constant declaration", "children": self.visit_children(node)}

    def visit_definition(self, node: "ASTDefinitionNode"):
        return {"name": "Definition", "children": self.visit_children(node)}

    def visit_event_definition(self, node: "ASTEventDefinitionNode"):
        return {"name": "Event definition", "children": self.visit_children(node)}

    def visit_conversion_operator_definition(self, node: "ASTConversionOperatorDefinitionNode"):
        return {"name": "Conversion operator definition", "children": self.visit_children(node)}

    def visit_constructor_definition(self, node: "ASTConstructorDefinitionNode"):
        return {"name": "Constructor definition", "children": self.visit_children(node)}

    def visit_destructor_definition(self, node: "ASTDestructorDefinitionNode"):
        return {"name": "Destructor definition", "children": self.visit_children(node)}

    def visit_accessor_definition(self, node: "ASTAccessorDefinitionNode"):
        return {"name": "Accessor definition", "children": self.visit_children(node)}

    def visit_struct_definition(self, node: "ASTStructDefinitionNode"):
        return {"name": "Struct definition", "children": self.visit_children(node)}

    def visit_interface_definition(self, node: "ASTInterfaceDefinitionNode"):
        return {"name": "Interface definition", "children": self.visit_children(node)}

    def visit_property_definition(self, node: "ASTPropertyDefinitionNode"):
        return {"name": "Property definition", "children": self.visit_children(node)}

    def visit_enum_definition(self, node: "ASTEnumDefinitionNode"):
        return {"name": "Enum definition", "children": self.visit_children(node)}

    def visit_delegate_definition(self, node: "ASTDelegateDefinitionNode"):
        return {"name": "Delegate definition", "children": self.visit_children(node)}

    def visit_indexer_definition(self, node: "ASTIndexerDefinitionNode"):
        return {"name": "Indexer definition", "children": self.visit_children(node)}

    def visit_operator_overload_definition(self, node: "ASTOperatorOverloadDefinitionNode"):
        return {"name": "Operator overload definition", "children": self.visit_children(node)}

    def visit_fixed_size_buffer_definition(self, node: "ASTFixedSizeBufferDefinitionNode"):
        return {"name": "Fixed size buffer definition", "children": self.visit_children(node)}

    def visit_positional_only_parameter(self, node: "ASTPositionalOnlyParameterNode"):
        return {"name": "Positional-only parameter", "children": self.visit_children(node)}

    def visit_keyword_only_parameter(self, node: "ASTKeywordOnlyParameterNode"):
        return {"name": "Keyword-only parameter", "children": self.visit_children(node)}

    def visit_conditional_expression(self, node: "ASTConditionalExpressionNode"):
        return {"name": "Conditional expression", "children": self.visit_children(node)}

    def visit_null_coalescing_expression(self, node: "ASTNullCoalescingExpressionNode"):
        return {"name": "Null-coalescing expression", "children": self.visit_children(node)}

    def visit_type_cast(self, node: "ASTTypeCastNode"):
        return {"name": "Type case", "children": self.visit_children(node)}

    def visit_type(self, node: "ASTTypeNode"):
        return {"name": "Type", "children": self.visit_children(node)}

    def visit_object_creation(self, node: "ASTObjectCreationNode"):
        return {"name": "Object creation", "children": self.visit_children(node)}

    def visit_array_creation(self, node: "ASTArrayCreationNode"):
        return {"name": "Array creation", "children": self.visit_children(node)}

    def visit_initializer(self, node: "ASTInitializerNode"):
        return {"name": "Initializer", "children": self.visit_children(node)}

    def visit_query(self, node: "ASTQueryNode"):
        return {"name": "Query", "children": self.visit_children(node)}

    def visit_from_clause(self, node: "ASTFromClauseNode"):
        return {"name": "From clause", "children": self.visit_children(node)}

    def visit_let_clause(self, node: "ASTLetClauseNode"):
        return {"name": "Let clause", "children": self.visit_children(node)}

    def visit_where_clause(self, node: "ASTWhereClauseNode"):
        return {"name": "Where clause", "children": self.visit_children(node)}

    def visit_join_clause(self, node: "ASTJoinClauseNode"):
        return {"name": "Join clause", "children": self.visit_children(node)}

    def visit_order_by_clause(self, node: "ASTOrderByClauseNode"):
        return {"name": "Order-by clause", "children": self.visit_children(node)}

    def visit_ordering(self, node: "ASTOrderingNode"):
        return {"name": "Ordering", "children": self.visit_children(node)}

    def visit_select_clause(self, node: "ASTSelectClauseNode"):
        return {"name": "Select clause", "children": self.visit_children(node)}

    def visit_group_by_clause(self, node: "ASTGroupByClauseNode"):
        return {"name": "Group-by clause", "children": self.visit_children(node)}

    def visit_into_clause(self, node: "ASTIntoClauseNode"):
        return {"name": "Into clause", "children": self.visit_children(node)}

    def visit_label(self, node: "ASTLabelNode"):
        return {"name": "Label", "children": self.visit_children(node)}

    def visit_switch_section(self, node: "ASTSwitchSectionNode"):
        return {"name": "Switch section", "children": self.visit_children(node)}

    def visit_case_label(self, node: "ASTCaseLabelNode"):
        return {"name": "Case label", "children": self.visit_children(node)}

    def visit_default_label(self, node: "ASTDefaultLabelNode"):
        return {"name": "Default label", "children": self.visit_children(node)}

    def visit_attribute_section(self, node: "ASTAttributeSectionNode"):
        return {"name": "Attribute section", "children": self.visit_children(node)}

    def visit_attribute(self, node: "ASTAttributeNode"):
        return {"name": "Attribute", "children": self.visit_children(node)}

    def visit_pointer_type(self, node: "ASTPointerTypeNode"):
        return {"name": "Pointer type", "children": self.visit_children(node)}

    def visit_nullable_type(self, node: "ASTNullableTypeNode"):
        return {"name": "Nullable type", "children": self.visit_children(node)}

    def visit_array_type(self, node: "ASTArrayTypeNode"):
        return {"name": "Array type", "children": self.visit_children(node)}

    def visit_constraints_clause(self, node: "ASTConstraintsClauseNode"):
        return {"name": "Constraints clause", "children": self.visit_children(node)}

    def visit_stack_allocation(self, node: "ASTStackAllocationNode"):
        return {"name": "Stack allocation", "children": self.visit_children(node)}
