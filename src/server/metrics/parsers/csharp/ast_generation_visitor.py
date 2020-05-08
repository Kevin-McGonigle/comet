from metrics.parsers.csharp.base.CSharpParser import CSharpParser
from metrics.parsers.csharp.base.CSharpParserVisitor import CSharpParserVisitor
from metrics.visitors.structures.ast_generation_visitor import ASTGenerationVisitor as BaseASTGenerationVisitor


class ASTGenerationVisitor(BaseASTGenerationVisitor, CSharpParserVisitor):
    # region Helpers

    # endregion

    # region Visits

    def visitCompilation_unit(self, ctx: CSharpParser.Compilation_unitContext):
        extern_alias_directives = ctx.extern_alias_directives()
        if extern_alias_directives:
            extern_alias_directives = extern_alias_directives.accept(self)

        using_directives = ctx.using_directives()
        if using_directives:
            using_directives = using_directives.accept(self)

        global_attribute_section = ctx.global_attribute_section()
        if global_attribute_section:
            global_attribute_section = [gas.accept(self) for gas in global_attribute_section]

        namespace_member_declarations = ctx.namespace_member_declarations()
        if namespace_member_declarations:
            namespace_member_declarations = namespace_member_declarations.accept(self)

    def visitNamespace_or_type_name(self, ctx: CSharpParser.Namespace_or_type_nameContext):
        qualified_alias_member = ctx.qualified_alias_member()
        if qualified_alias_member:
            qualified_alias_member = qualified_alias_member.accept(self)

        children = ctx.getChildren(lambda child: self.filter_child(child, CSharpParser.IdentifierContext,
                                                                   CSharpParser.Type_argument_listContext))
        return super().visitNamespace_or_type_name(ctx)

    def visitType_(self, ctx: CSharpParser.Type_Context):
        return super().visitType_(ctx)

    def visitBase_type(self, ctx: CSharpParser.Base_typeContext):
        return super().visitBase_type(ctx)

    def visitSimple_type(self, ctx: CSharpParser.Simple_typeContext):
        return super().visitSimple_type(ctx)

    def visitNumeric_type(self, ctx: CSharpParser.Numeric_typeContext):
        return super().visitNumeric_type(ctx)

    def visitIntegral_type(self, ctx: CSharpParser.Integral_typeContext):
        return super().visitIntegral_type(ctx)

    def visitFloating_point_type(self, ctx: CSharpParser.Floating_point_typeContext):
        return super().visitFloating_point_type(ctx)

    def visitClass_type(self, ctx: CSharpParser.Class_typeContext):
        return super().visitClass_type(ctx)

    def visitType_argument_list(self, ctx: CSharpParser.Type_argument_listContext):
        return super().visitType_argument_list(ctx)

    def visitArgument_list(self, ctx: CSharpParser.Argument_listContext):
        return super().visitArgument_list(ctx)

    def visitArgument(self, ctx: CSharpParser.ArgumentContext):
        return super().visitArgument(ctx)

    def visitExpression(self, ctx: CSharpParser.ExpressionContext):
        return super().visitExpression(ctx)

    def visitNon_assignment_expression(self, ctx: CSharpParser.Non_assignment_expressionContext):
        return super().visitNon_assignment_expression(ctx)

    def visitAssignment(self, ctx: CSharpParser.AssignmentContext):
        return super().visitAssignment(ctx)

    def visitAssignment_operator(self, ctx: CSharpParser.Assignment_operatorContext):
        return super().visitAssignment_operator(ctx)

    def visitConditional_expression(self, ctx: CSharpParser.Conditional_expressionContext):
        return super().visitConditional_expression(ctx)

    def visitNull_coalescing_expression(self, ctx: CSharpParser.Null_coalescing_expressionContext):
        return super().visitNull_coalescing_expression(ctx)

    def visitConditional_or_expression(self, ctx: CSharpParser.Conditional_or_expressionContext):
        return super().visitConditional_or_expression(ctx)

    def visitConditional_and_expression(self, ctx: CSharpParser.Conditional_and_expressionContext):
        return super().visitConditional_and_expression(ctx)

    def visitInclusive_or_expression(self, ctx: CSharpParser.Inclusive_or_expressionContext):
        return super().visitInclusive_or_expression(ctx)

    def visitExclusive_or_expression(self, ctx: CSharpParser.Exclusive_or_expressionContext):
        return super().visitExclusive_or_expression(ctx)

    def visitAnd_expression(self, ctx: CSharpParser.And_expressionContext):
        return super().visitAnd_expression(ctx)

    def visitEquality_expression(self, ctx: CSharpParser.Equality_expressionContext):
        return super().visitEquality_expression(ctx)

    def visitRelational_expression(self, ctx: CSharpParser.Relational_expressionContext):
        return super().visitRelational_expression(ctx)

    def visitShift_expression(self, ctx: CSharpParser.Shift_expressionContext):
        return super().visitShift_expression(ctx)

    def visitAdditive_expression(self, ctx: CSharpParser.Additive_expressionContext):
        return super().visitAdditive_expression(ctx)

    def visitMultiplicative_expression(self, ctx: CSharpParser.Multiplicative_expressionContext):
        return super().visitMultiplicative_expression(ctx)

    def visitUnary_expression(self, ctx: CSharpParser.Unary_expressionContext):
        return super().visitUnary_expression(ctx)

    def visitPrimary_expression(self, ctx: CSharpParser.Primary_expressionContext):
        return super().visitPrimary_expression(ctx)

    def visitLiteralExpression(self, ctx: CSharpParser.LiteralExpressionContext):
        return super().visitLiteralExpression(ctx)

    def visitSimpleNameExpression(self, ctx: CSharpParser.SimpleNameExpressionContext):
        return super().visitSimpleNameExpression(ctx)

    def visitParenthesisExpressions(self, ctx: CSharpParser.ParenthesisExpressionsContext):
        return super().visitParenthesisExpressions(ctx)

    def visitMemberAccessExpression(self, ctx: CSharpParser.MemberAccessExpressionContext):
        return super().visitMemberAccessExpression(ctx)

    def visitLiteralAccessExpression(self, ctx: CSharpParser.LiteralAccessExpressionContext):
        return super().visitLiteralAccessExpression(ctx)

    def visitThisReferenceExpression(self, ctx: CSharpParser.ThisReferenceExpressionContext):
        return super().visitThisReferenceExpression(ctx)

    def visitBaseAccessExpression(self, ctx: CSharpParser.BaseAccessExpressionContext):
        return super().visitBaseAccessExpression(ctx)

    def visitObjectCreationExpression(self, ctx: CSharpParser.ObjectCreationExpressionContext):
        return super().visitObjectCreationExpression(ctx)

    def visitTypeofExpression(self, ctx: CSharpParser.TypeofExpressionContext):
        return super().visitTypeofExpression(ctx)

    def visitCheckedExpression(self, ctx: CSharpParser.CheckedExpressionContext):
        return super().visitCheckedExpression(ctx)

    def visitUncheckedExpression(self, ctx: CSharpParser.UncheckedExpressionContext):
        return super().visitUncheckedExpression(ctx)

    def visitDefaultValueExpression(self, ctx: CSharpParser.DefaultValueExpressionContext):
        return super().visitDefaultValueExpression(ctx)

    def visitAnonymousMethodExpression(self, ctx: CSharpParser.AnonymousMethodExpressionContext):
        return super().visitAnonymousMethodExpression(ctx)

    def visitSizeofExpression(self, ctx: CSharpParser.SizeofExpressionContext):
        return super().visitSizeofExpression(ctx)

    def visitNameofExpression(self, ctx: CSharpParser.NameofExpressionContext):
        return super().visitNameofExpression(ctx)

    def visitMember_access(self, ctx: CSharpParser.Member_accessContext):
        return super().visitMember_access(ctx)

    def visitBracket_expression(self, ctx: CSharpParser.Bracket_expressionContext):
        return super().visitBracket_expression(ctx)

    def visitIndexer_argument(self, ctx: CSharpParser.Indexer_argumentContext):
        return super().visitIndexer_argument(ctx)

    def visitPredefined_type(self, ctx: CSharpParser.Predefined_typeContext):
        return super().visitPredefined_type(ctx)

    def visitExpression_list(self, ctx: CSharpParser.Expression_listContext):
        return super().visitExpression_list(ctx)

    def visitObject_or_collection_initializer(self, ctx: CSharpParser.Object_or_collection_initializerContext):
        return super().visitObject_or_collection_initializer(ctx)

    def visitObject_initializer(self, ctx: CSharpParser.Object_initializerContext):
        return super().visitObject_initializer(ctx)

    def visitMember_initializer_list(self, ctx: CSharpParser.Member_initializer_listContext):
        return super().visitMember_initializer_list(ctx)

    def visitMember_initializer(self, ctx: CSharpParser.Member_initializerContext):
        return super().visitMember_initializer(ctx)

    def visitInitializer_value(self, ctx: CSharpParser.Initializer_valueContext):
        return super().visitInitializer_value(ctx)

    def visitCollection_initializer(self, ctx: CSharpParser.Collection_initializerContext):
        return super().visitCollection_initializer(ctx)

    def visitElement_initializer(self, ctx: CSharpParser.Element_initializerContext):
        return super().visitElement_initializer(ctx)

    def visitAnonymous_object_initializer(self, ctx: CSharpParser.Anonymous_object_initializerContext):
        return super().visitAnonymous_object_initializer(ctx)

    def visitMember_declarator_list(self, ctx: CSharpParser.Member_declarator_listContext):
        return super().visitMember_declarator_list(ctx)

    def visitMember_declarator(self, ctx: CSharpParser.Member_declaratorContext):
        return super().visitMember_declarator(ctx)

    def visitUnbound_type_name(self, ctx: CSharpParser.Unbound_type_nameContext):
        return super().visitUnbound_type_name(ctx)

    def visitGeneric_dimension_specifier(self, ctx: CSharpParser.Generic_dimension_specifierContext):
        return super().visitGeneric_dimension_specifier(ctx)

    def visitIsType(self, ctx: CSharpParser.IsTypeContext):
        return super().visitIsType(ctx)

    def visitLambda_expression(self, ctx: CSharpParser.Lambda_expressionContext):
        return super().visitLambda_expression(ctx)

    def visitAnonymous_function_signature(self, ctx: CSharpParser.Anonymous_function_signatureContext):
        return super().visitAnonymous_function_signature(ctx)

    def visitExplicit_anonymous_function_parameter_list(self,
                                                        ctx: CSharpParser.Explicit_anonymous_function_parameter_listContext):
        return super().visitExplicit_anonymous_function_parameter_list(ctx)

    def visitExplicit_anonymous_function_parameter(self,
                                                   ctx: CSharpParser.Explicit_anonymous_function_parameterContext):
        return super().visitExplicit_anonymous_function_parameter(ctx)

    def visitImplicit_anonymous_function_parameter_list(self,
                                                        ctx: CSharpParser.Implicit_anonymous_function_parameter_listContext):
        return super().visitImplicit_anonymous_function_parameter_list(ctx)

    def visitAnonymous_function_body(self, ctx: CSharpParser.Anonymous_function_bodyContext):
        return super().visitAnonymous_function_body(ctx)

    def visitQuery_expression(self, ctx: CSharpParser.Query_expressionContext):
        return super().visitQuery_expression(ctx)

    def visitFrom_clause(self, ctx: CSharpParser.From_clauseContext):
        return super().visitFrom_clause(ctx)

    def visitQuery_body(self, ctx: CSharpParser.Query_bodyContext):
        return super().visitQuery_body(ctx)

    def visitQuery_body_clause(self, ctx: CSharpParser.Query_body_clauseContext):
        return super().visitQuery_body_clause(ctx)

    def visitLet_clause(self, ctx: CSharpParser.Let_clauseContext):
        return super().visitLet_clause(ctx)

    def visitWhere_clause(self, ctx: CSharpParser.Where_clauseContext):
        return super().visitWhere_clause(ctx)

    def visitCombined_join_clause(self, ctx: CSharpParser.Combined_join_clauseContext):
        return super().visitCombined_join_clause(ctx)

    def visitOrderby_clause(self, ctx: CSharpParser.Orderby_clauseContext):
        return super().visitOrderby_clause(ctx)

    def visitOrdering(self, ctx: CSharpParser.OrderingContext):
        return super().visitOrdering(ctx)

    def visitSelect_or_group_clause(self, ctx: CSharpParser.Select_or_group_clauseContext):
        return super().visitSelect_or_group_clause(ctx)

    def visitQuery_continuation(self, ctx: CSharpParser.Query_continuationContext):
        return super().visitQuery_continuation(ctx)

    def visitLabeledStatement(self, ctx: CSharpParser.LabeledStatementContext):
        return super().visitLabeledStatement(ctx)

    def visitDeclarationStatement(self, ctx: CSharpParser.DeclarationStatementContext):
        return super().visitDeclarationStatement(ctx)

    def visitEmbeddedStatement(self, ctx: CSharpParser.EmbeddedStatementContext):
        return super().visitEmbeddedStatement(ctx)

    def visitLabeled_Statement(self, ctx: CSharpParser.Labeled_StatementContext):
        return super().visitLabeled_Statement(ctx)

    def visitEmbedded_statement(self, ctx: CSharpParser.Embedded_statementContext):
        return super().visitEmbedded_statement(ctx)

    def visitTheEmptyStatement(self, ctx: CSharpParser.TheEmptyStatementContext):
        return super().visitTheEmptyStatement(ctx)

    def visitExpressionStatement(self, ctx: CSharpParser.ExpressionStatementContext):
        return super().visitExpressionStatement(ctx)

    def visitIfStatement(self, ctx: CSharpParser.IfStatementContext):
        return super().visitIfStatement(ctx)

    def visitSwitchStatement(self, ctx: CSharpParser.SwitchStatementContext):
        return super().visitSwitchStatement(ctx)

    def visitWhileStatement(self, ctx: CSharpParser.WhileStatementContext):
        return super().visitWhileStatement(ctx)

    def visitDoStatement(self, ctx: CSharpParser.DoStatementContext):
        return super().visitDoStatement(ctx)

    def visitForStatement(self, ctx: CSharpParser.ForStatementContext):
        return super().visitForStatement(ctx)

    def visitForeachStatement(self, ctx: CSharpParser.ForeachStatementContext):
        return super().visitForeachStatement(ctx)

    def visitBreakStatement(self, ctx: CSharpParser.BreakStatementContext):
        return super().visitBreakStatement(ctx)

    def visitContinueStatement(self, ctx: CSharpParser.ContinueStatementContext):
        return super().visitContinueStatement(ctx)

    def visitGotoStatement(self, ctx: CSharpParser.GotoStatementContext):
        return super().visitGotoStatement(ctx)

    def visitReturnStatement(self, ctx: CSharpParser.ReturnStatementContext):
        return super().visitReturnStatement(ctx)

    def visitThrowStatement(self, ctx: CSharpParser.ThrowStatementContext):
        return super().visitThrowStatement(ctx)

    def visitTryStatement(self, ctx: CSharpParser.TryStatementContext):
        return super().visitTryStatement(ctx)

    def visitCheckedStatement(self, ctx: CSharpParser.CheckedStatementContext):
        return super().visitCheckedStatement(ctx)

    def visitUncheckedStatement(self, ctx: CSharpParser.UncheckedStatementContext):
        return super().visitUncheckedStatement(ctx)

    def visitLockStatement(self, ctx: CSharpParser.LockStatementContext):
        return super().visitLockStatement(ctx)

    def visitUsingStatement(self, ctx: CSharpParser.UsingStatementContext):
        return super().visitUsingStatement(ctx)

    def visitYieldStatement(self, ctx: CSharpParser.YieldStatementContext):
        return super().visitYieldStatement(ctx)

    def visitUnsafeStatement(self, ctx: CSharpParser.UnsafeStatementContext):
        return super().visitUnsafeStatement(ctx)

    def visitFixedStatement(self, ctx: CSharpParser.FixedStatementContext):
        return super().visitFixedStatement(ctx)

    def visitBlock(self, ctx: CSharpParser.BlockContext):
        return super().visitBlock(ctx)

    def visitLocal_variable_declaration(self, ctx: CSharpParser.Local_variable_declarationContext):
        return super().visitLocal_variable_declaration(ctx)

    def visitLocal_variable_type(self, ctx: CSharpParser.Local_variable_typeContext):
        return super().visitLocal_variable_type(ctx)

    def visitLocal_variable_declarator(self, ctx: CSharpParser.Local_variable_declaratorContext):
        return super().visitLocal_variable_declarator(ctx)

    def visitLocal_variable_initializer(self, ctx: CSharpParser.Local_variable_initializerContext):
        return super().visitLocal_variable_initializer(ctx)

    def visitLocal_constant_declaration(self, ctx: CSharpParser.Local_constant_declarationContext):
        return super().visitLocal_constant_declaration(ctx)

    def visitIf_body(self, ctx: CSharpParser.If_bodyContext):
        return super().visitIf_body(ctx)

    def visitSwitch_section(self, ctx: CSharpParser.Switch_sectionContext):
        return super().visitSwitch_section(ctx)

    def visitSwitch_label(self, ctx: CSharpParser.Switch_labelContext):
        return super().visitSwitch_label(ctx)

    def visitStatement_list(self, ctx: CSharpParser.Statement_listContext):
        return super().visitStatement_list(ctx)

    def visitFor_initializer(self, ctx: CSharpParser.For_initializerContext):
        return super().visitFor_initializer(ctx)

    def visitFor_iterator(self, ctx: CSharpParser.For_iteratorContext):
        return super().visitFor_iterator(ctx)

    def visitCatch_clauses(self, ctx: CSharpParser.Catch_clausesContext):
        return super().visitCatch_clauses(ctx)

    def visitSpecific_catch_clause(self, ctx: CSharpParser.Specific_catch_clauseContext):
        return super().visitSpecific_catch_clause(ctx)

    def visitGeneral_catch_clause(self, ctx: CSharpParser.General_catch_clauseContext):
        return super().visitGeneral_catch_clause(ctx)

    def visitException_filter(self, ctx: CSharpParser.Exception_filterContext):
        return super().visitException_filter(ctx)

    def visitFinally_clause(self, ctx: CSharpParser.Finally_clauseContext):
        return super().visitFinally_clause(ctx)

    def visitResource_acquisition(self, ctx: CSharpParser.Resource_acquisitionContext):
        return super().visitResource_acquisition(ctx)

    def visitNamespace_declaration(self, ctx: CSharpParser.Namespace_declarationContext):
        return super().visitNamespace_declaration(ctx)

    def visitQualified_identifier(self, ctx: CSharpParser.Qualified_identifierContext):
        return super().visitQualified_identifier(ctx)

    def visitNamespace_body(self, ctx: CSharpParser.Namespace_bodyContext):
        return super().visitNamespace_body(ctx)

    def visitExtern_alias_directives(self, ctx: CSharpParser.Extern_alias_directivesContext):
        return super().visitExtern_alias_directives(ctx)

    def visitExtern_alias_directive(self, ctx: CSharpParser.Extern_alias_directiveContext):
        return super().visitExtern_alias_directive(ctx)

    def visitUsing_directives(self, ctx: CSharpParser.Using_directivesContext):
        return super().visitUsing_directives(ctx)

    def visitUsingAliasDirective(self, ctx: CSharpParser.UsingAliasDirectiveContext):
        return super().visitUsingAliasDirective(ctx)

    def visitUsingNamespaceDirective(self, ctx: CSharpParser.UsingNamespaceDirectiveContext):
        return super().visitUsingNamespaceDirective(ctx)

    def visitUsingStaticDirective(self, ctx: CSharpParser.UsingStaticDirectiveContext):
        return super().visitUsingStaticDirective(ctx)

    def visitNamespace_member_declarations(self, ctx: CSharpParser.Namespace_member_declarationsContext):
        return super().visitNamespace_member_declarations(ctx)

    def visitNamespace_member_declaration(self, ctx: CSharpParser.Namespace_member_declarationContext):
        return super().visitNamespace_member_declaration(ctx)

    def visitType_declaration(self, ctx: CSharpParser.Type_declarationContext):
        return super().visitType_declaration(ctx)

    def visitQualified_alias_member(self, ctx: CSharpParser.Qualified_alias_memberContext):
        return super().visitQualified_alias_member(ctx)

    def visitType_parameter_list(self, ctx: CSharpParser.Type_parameter_listContext):
        return super().visitType_parameter_list(ctx)

    def visitType_parameter(self, ctx: CSharpParser.Type_parameterContext):
        return super().visitType_parameter(ctx)

    def visitClass_base(self, ctx: CSharpParser.Class_baseContext):
        return super().visitClass_base(ctx)

    def visitInterface_type_list(self, ctx: CSharpParser.Interface_type_listContext):
        return super().visitInterface_type_list(ctx)

    def visitType_parameter_constraints_clauses(self, ctx: CSharpParser.Type_parameter_constraints_clausesContext):
        return super().visitType_parameter_constraints_clauses(ctx)

    def visitType_parameter_constraints_clause(self, ctx: CSharpParser.Type_parameter_constraints_clauseContext):
        return super().visitType_parameter_constraints_clause(ctx)

    def visitType_parameter_constraints(self, ctx: CSharpParser.Type_parameter_constraintsContext):
        return super().visitType_parameter_constraints(ctx)

    def visitPrimary_constraint(self, ctx: CSharpParser.Primary_constraintContext):
        return super().visitPrimary_constraint(ctx)

    def visitSecondary_constraints(self, ctx: CSharpParser.Secondary_constraintsContext):
        return super().visitSecondary_constraints(ctx)

    def visitConstructor_constraint(self, ctx: CSharpParser.Constructor_constraintContext):
        return super().visitConstructor_constraint(ctx)

    def visitClass_body(self, ctx: CSharpParser.Class_bodyContext):
        return super().visitClass_body(ctx)

    def visitClass_member_declarations(self, ctx: CSharpParser.Class_member_declarationsContext):
        return super().visitClass_member_declarations(ctx)

    def visitClass_member_declaration(self, ctx: CSharpParser.Class_member_declarationContext):
        return super().visitClass_member_declaration(ctx)

    def visitAll_member_modifiers(self, ctx: CSharpParser.All_member_modifiersContext):
        return super().visitAll_member_modifiers(ctx)

    def visitAll_member_modifier(self, ctx: CSharpParser.All_member_modifierContext):
        return super().visitAll_member_modifier(ctx)

    def visitCommon_member_declaration(self, ctx: CSharpParser.Common_member_declarationContext):
        return super().visitCommon_member_declaration(ctx)

    def visitTyped_member_declaration(self, ctx: CSharpParser.Typed_member_declarationContext):
        return super().visitTyped_member_declaration(ctx)

    def visitConstant_declarators(self, ctx: CSharpParser.Constant_declaratorsContext):
        return super().visitConstant_declarators(ctx)

    def visitConstant_declarator(self, ctx: CSharpParser.Constant_declaratorContext):
        return super().visitConstant_declarator(ctx)

    def visitVariable_declarators(self, ctx: CSharpParser.Variable_declaratorsContext):
        return super().visitVariable_declarators(ctx)

    def visitVariable_declarator(self, ctx: CSharpParser.Variable_declaratorContext):
        return super().visitVariable_declarator(ctx)

    def visitVariable_initializer(self, ctx: CSharpParser.Variable_initializerContext):
        return super().visitVariable_initializer(ctx)

    def visitReturn_type(self, ctx: CSharpParser.Return_typeContext):
        return super().visitReturn_type(ctx)

    def visitMember_name(self, ctx: CSharpParser.Member_nameContext):
        return super().visitMember_name(ctx)

    def visitMethod_body(self, ctx: CSharpParser.Method_bodyContext):
        return super().visitMethod_body(ctx)

    def visitFormal_parameter_list(self, ctx: CSharpParser.Formal_parameter_listContext):
        return super().visitFormal_parameter_list(ctx)

    def visitFixed_parameters(self, ctx: CSharpParser.Fixed_parametersContext):
        return super().visitFixed_parameters(ctx)

    def visitFixed_parameter(self, ctx: CSharpParser.Fixed_parameterContext):
        return super().visitFixed_parameter(ctx)

    def visitParameter_modifier(self, ctx: CSharpParser.Parameter_modifierContext):
        return super().visitParameter_modifier(ctx)

    def visitParameter_array(self, ctx: CSharpParser.Parameter_arrayContext):
        return super().visitParameter_array(ctx)

    def visitAccessor_declarations(self, ctx: CSharpParser.Accessor_declarationsContext):
        return super().visitAccessor_declarations(ctx)

    def visitGet_accessor_declaration(self, ctx: CSharpParser.Get_accessor_declarationContext):
        return super().visitGet_accessor_declaration(ctx)

    def visitSet_accessor_declaration(self, ctx: CSharpParser.Set_accessor_declarationContext):
        return super().visitSet_accessor_declaration(ctx)

    def visitAccessor_modifier(self, ctx: CSharpParser.Accessor_modifierContext):
        return super().visitAccessor_modifier(ctx)

    def visitAccessor_body(self, ctx: CSharpParser.Accessor_bodyContext):
        return super().visitAccessor_body(ctx)

    def visitEvent_accessor_declarations(self, ctx: CSharpParser.Event_accessor_declarationsContext):
        return super().visitEvent_accessor_declarations(ctx)

    def visitAdd_accessor_declaration(self, ctx: CSharpParser.Add_accessor_declarationContext):
        return super().visitAdd_accessor_declaration(ctx)

    def visitRemove_accessor_declaration(self, ctx: CSharpParser.Remove_accessor_declarationContext):
        return super().visitRemove_accessor_declaration(ctx)

    def visitOverloadable_operator(self, ctx: CSharpParser.Overloadable_operatorContext):
        return super().visitOverloadable_operator(ctx)

    def visitConversion_operator_declarator(self, ctx: CSharpParser.Conversion_operator_declaratorContext):
        return super().visitConversion_operator_declarator(ctx)

    def visitConstructor_initializer(self, ctx: CSharpParser.Constructor_initializerContext):
        return super().visitConstructor_initializer(ctx)

    def visitBody(self, ctx: CSharpParser.BodyContext):
        return super().visitBody(ctx)

    def visitStruct_interfaces(self, ctx: CSharpParser.Struct_interfacesContext):
        return super().visitStruct_interfaces(ctx)

    def visitStruct_body(self, ctx: CSharpParser.Struct_bodyContext):
        return super().visitStruct_body(ctx)

    def visitStruct_member_declaration(self, ctx: CSharpParser.Struct_member_declarationContext):
        return super().visitStruct_member_declaration(ctx)

    def visitArray_type(self, ctx: CSharpParser.Array_typeContext):
        return super().visitArray_type(ctx)

    def visitRank_specifier(self, ctx: CSharpParser.Rank_specifierContext):
        return super().visitRank_specifier(ctx)

    def visitArray_initializer(self, ctx: CSharpParser.Array_initializerContext):
        return super().visitArray_initializer(ctx)

    def visitVariant_type_parameter_list(self, ctx: CSharpParser.Variant_type_parameter_listContext):
        return super().visitVariant_type_parameter_list(ctx)

    def visitVariant_type_parameter(self, ctx: CSharpParser.Variant_type_parameterContext):
        return super().visitVariant_type_parameter(ctx)

    def visitVariance_annotation(self, ctx: CSharpParser.Variance_annotationContext):
        return super().visitVariance_annotation(ctx)

    def visitInterface_base(self, ctx: CSharpParser.Interface_baseContext):
        return super().visitInterface_base(ctx)

    def visitInterface_body(self, ctx: CSharpParser.Interface_bodyContext):
        return super().visitInterface_body(ctx)

    def visitInterface_member_declaration(self, ctx: CSharpParser.Interface_member_declarationContext):
        return super().visitInterface_member_declaration(ctx)

    def visitInterface_accessors(self, ctx: CSharpParser.Interface_accessorsContext):
        return super().visitInterface_accessors(ctx)

    def visitEnum_base(self, ctx: CSharpParser.Enum_baseContext):
        return super().visitEnum_base(ctx)

    def visitEnum_body(self, ctx: CSharpParser.Enum_bodyContext):
        return super().visitEnum_body(ctx)

    def visitEnum_member_declaration(self, ctx: CSharpParser.Enum_member_declarationContext):
        return super().visitEnum_member_declaration(ctx)

    def visitGlobal_attribute_section(self, ctx: CSharpParser.Global_attribute_sectionContext):
        return super().visitGlobal_attribute_section(ctx)

    def visitGlobal_attribute_target(self, ctx: CSharpParser.Global_attribute_targetContext):
        return super().visitGlobal_attribute_target(ctx)

    def visitAttributes(self, ctx: CSharpParser.AttributesContext):
        return super().visitAttributes(ctx)

    def visitAttribute_section(self, ctx: CSharpParser.Attribute_sectionContext):
        return super().visitAttribute_section(ctx)

    def visitAttribute_target(self, ctx: CSharpParser.Attribute_targetContext):
        return super().visitAttribute_target(ctx)

    def visitAttribute_list(self, ctx: CSharpParser.Attribute_listContext):
        return super().visitAttribute_list(ctx)

    def visitAttribute(self, ctx: CSharpParser.AttributeContext):
        return super().visitAttribute(ctx)

    def visitAttribute_argument(self, ctx: CSharpParser.Attribute_argumentContext):
        return super().visitAttribute_argument(ctx)

    def visitPointer_type(self, ctx: CSharpParser.Pointer_typeContext):
        return super().visitPointer_type(ctx)

    def visitFixed_pointer_declarators(self, ctx: CSharpParser.Fixed_pointer_declaratorsContext):
        return super().visitFixed_pointer_declarators(ctx)

    def visitFixed_pointer_declarator(self, ctx: CSharpParser.Fixed_pointer_declaratorContext):
        return super().visitFixed_pointer_declarator(ctx)

    def visitFixed_pointer_initializer(self, ctx: CSharpParser.Fixed_pointer_initializerContext):
        return super().visitFixed_pointer_initializer(ctx)

    def visitFixed_size_buffer_declarator(self, ctx: CSharpParser.Fixed_size_buffer_declaratorContext):
        return super().visitFixed_size_buffer_declarator(ctx)

    def visitLocal_variable_initializer_unsafe(self, ctx: CSharpParser.Local_variable_initializer_unsafeContext):
        return super().visitLocal_variable_initializer_unsafe(ctx)

    def visitRight_arrow(self, ctx: CSharpParser.Right_arrowContext):
        return super().visitRight_arrow(ctx)

    def visitRight_shift(self, ctx: CSharpParser.Right_shiftContext):
        return super().visitRight_shift(ctx)

    def visitRight_shift_assignment(self, ctx: CSharpParser.Right_shift_assignmentContext):
        return super().visitRight_shift_assignment(ctx)

    def visitLiteral(self, ctx: CSharpParser.LiteralContext):
        return super().visitLiteral(ctx)

    def visitBoolean_literal(self, ctx: CSharpParser.Boolean_literalContext):
        return super().visitBoolean_literal(ctx)

    def visitString_literal(self, ctx: CSharpParser.String_literalContext):
        return super().visitString_literal(ctx)

    def visitInterpolated_regular_string(self, ctx: CSharpParser.Interpolated_regular_stringContext):
        return super().visitInterpolated_regular_string(ctx)

    def visitInterpolated_verbatium_string(self, ctx: CSharpParser.Interpolated_verbatium_stringContext):
        return super().visitInterpolated_verbatium_string(ctx)

    def visitInterpolated_regular_string_part(self, ctx: CSharpParser.Interpolated_regular_string_partContext):
        return super().visitInterpolated_regular_string_part(ctx)

    def visitInterpolated_verbatium_string_part(self, ctx: CSharpParser.Interpolated_verbatium_string_partContext):
        return super().visitInterpolated_verbatium_string_part(ctx)

    def visitInterpolated_string_expression(self, ctx: CSharpParser.Interpolated_string_expressionContext):
        return super().visitInterpolated_string_expression(ctx)

    def visitKeyword(self, ctx: CSharpParser.KeywordContext):
        return super().visitKeyword(ctx)

    def visitClass_definition(self, ctx: CSharpParser.Class_definitionContext):
        return super().visitClass_definition(ctx)

    def visitStruct_definition(self, ctx: CSharpParser.Struct_definitionContext):
        return super().visitStruct_definition(ctx)

    def visitInterface_definition(self, ctx: CSharpParser.Interface_definitionContext):
        return super().visitInterface_definition(ctx)

    def visitEnum_definition(self, ctx: CSharpParser.Enum_definitionContext):
        return super().visitEnum_definition(ctx)

    def visitDelegate_definition(self, ctx: CSharpParser.Delegate_definitionContext):
        return super().visitDelegate_definition(ctx)

    def visitEvent_declaration(self, ctx: CSharpParser.Event_declarationContext):
        return super().visitEvent_declaration(ctx)

    def visitField_declaration(self, ctx: CSharpParser.Field_declarationContext):
        return super().visitField_declaration(ctx)

    def visitProperty_declaration(self, ctx: CSharpParser.Property_declarationContext):
        return super().visitProperty_declaration(ctx)

    def visitConstant_declaration(self, ctx: CSharpParser.Constant_declarationContext):
        return super().visitConstant_declaration(ctx)

    def visitIndexer_declaration(self, ctx: CSharpParser.Indexer_declarationContext):
        return super().visitIndexer_declaration(ctx)

    def visitDestructor_definition(self, ctx: CSharpParser.Destructor_definitionContext):
        return super().visitDestructor_definition(ctx)

    def visitConstructor_declaration(self, ctx: CSharpParser.Constructor_declarationContext):
        return super().visitConstructor_declaration(ctx)

    def visitMethod_declaration(self, ctx: CSharpParser.Method_declarationContext):
        return super().visitMethod_declaration(ctx)

    def visitMethod_member_name(self, ctx: CSharpParser.Method_member_nameContext):
        return super().visitMethod_member_name(ctx)

    def visitOperator_declaration(self, ctx: CSharpParser.Operator_declarationContext):
        return super().visitOperator_declaration(ctx)

    def visitArg_declaration(self, ctx: CSharpParser.Arg_declarationContext):
        return super().visitArg_declaration(ctx)

    def visitMethod_invocation(self, ctx: CSharpParser.Method_invocationContext):
        return super().visitMethod_invocation(ctx)

    def visitObject_creation_expression(self, ctx: CSharpParser.Object_creation_expressionContext):
        return super().visitObject_creation_expression(ctx)

    def visitIdentifier(self, ctx: CSharpParser.IdentifierContext):
        return super().visitIdentifier(ctx)

    # endregion
