from metrics.parsers.csharp.base.CSharpParser import CSharpParser
from metrics.parsers.csharp.base.CSharpParserVisitor import CSharpParserVisitor
from metrics.structures.ast import *
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

    def visitType_(self, ctx: CSharpParser.Type_Context):
        base_type = ctx.base_type().accept(self)

        children = ctx.getChildren(
            lambda child: self.filter_child(child, CSharpParser.INTERR, CSharpParser.Rank_specifierContext,
                                            CSharpParser.STAR))
        return super().visitType_(ctx)

    def visitBase_type(self, ctx: CSharpParser.Base_typeContext):
        simple_type = ctx.simple_type()
        if simple_type:
            return simple_type.accept(self)

        class_type = ctx.class_type()
        if class_type:
            return class_type.accept(self)

        # TODO: return unknown pointer

    def visitSimple_type(self, ctx: CSharpParser.Simple_typeContext):
        numeric_type = ctx.numeric_type()
        if numeric_type:
            return numeric_type.accept(self)

        return ASTIdentifierNode(ctx.BOOL().getText())

    def visitNumeric_type(self, ctx: CSharpParser.Numeric_typeContext):
        integral_type = ctx.integral_type()
        if integral_type:
            return integral_type.accept(self)

        floating_point_type = ctx.floating_point_type()
        if floating_point_type:
            return floating_point_type.accept(self)

        return ASTIdentifierNode(ctx.DECIMAL().getText())

    def visitIntegral_type(self, ctx: CSharpParser.Integral_typeContext):
        return ASTIdentifierNode(ctx.getChild(0).getText())

    def visitFloating_point_type(self, ctx: CSharpParser.Floating_point_typeContext):
        return ASTIdentifierNode(ctx.getChild(0).getText())

    def visitClass_type(self, ctx: CSharpParser.Class_typeContext):
        namespace_or_type_name = ctx.namespace_or_type_name()
        if namespace_or_type_name:
            return namespace_or_type_name.accept(self)

        return ASTIdentifierNode(ctx.getChild(0).getText())

    def visitType_argument_list(self, ctx: CSharpParser.Type_argument_listContext):
        type_ = [type_.accept(self) for type_ in ctx.type_()]
        return self.build_multi(type_, ASTArgumentsNode)

    def visitArgument_list(self, ctx: CSharpParser.Argument_listContext):
        argument = [argument.accept(self) for argument in ctx.argument()]
        return self.build_multi(argument, ASTArgumentsNode)

    def visitArgument(self, ctx: CSharpParser.ArgumentContext):
        expression = ctx.expression()

        identifier = ctx.identifier()
        if identifier:
            identifier = identifier.accept(self)

        if ctx.REF():
            pass
            # TODO: add support for reference arguments (maybe by adding a modifiers attribute to ASTArgumentNode)

        if ctx.OUT():
            pass
            # TODO: add support for output arguments

        if ctx.VAR():
            pass
            # TODO: handle variable declaration arguments

        if ctx.type_():
            pass
            # TODO: handle variable declaration arguments

        return expression.accept(self)

    def visitExpression(self, ctx: CSharpParser.ExpressionContext):
        return ctx.getChild(0).accept(self)

    def visitNon_assignment_expression(self, ctx: CSharpParser.Non_assignment_expressionContext):
        return ctx.getChild(0).accept(self)

    def visitAssignment(self, ctx: CSharpParser.AssignmentContext):
        unary_expression = ctx.unary_expression().accept(self)
        assignment_operator = ctx.assignment_operator().accept(self)
        expression = ctx.expression().accept(self)

        if assignment_operator == "=":
            return ASTAssignmentStatementNode(unary_expression, expression)

        return ASTAugmentedAssignmentStatementNode({
                                                       "+=": ASTInPlaceOperation.ADD,
                                                       "-=": ASTInPlaceOperation.SUBTRACT,
                                                       "*=": ASTInPlaceOperation.MULTIPLY,
                                                       "/=": ASTInPlaceOperation.DIVIDE,
                                                       "%=": ASTInPlaceOperation.MODULO,
                                                       "&=": ASTInPlaceOperation.BITWISE_AND,
                                                       "|=": ASTInPlaceOperation.BITWISE_OR,
                                                       "^=": ASTInPlaceOperation.BITWISE_XOR,
                                                       "<<=": ASTInPlaceOperation.LEFT_SHIFT,
                                                       ">>=": ASTInPlaceOperation.RIGHT_SHIFT
                                                   }[assignment_operator], unary_expression, expression)

    def visitAssignment_operator(self, ctx: CSharpParser.Assignment_operatorContext):
        return ctx.getChild(0).getText()

    def visitConditional_expression(self, ctx: CSharpParser.Conditional_expressionContext):
        if ctx.INTERR():
            return ASTConditionalExpressionNode(ctx.null_coalescing_expression().accept(self),
                                                ctx.expression(0).accept(self), ctx.expression(1).accept(self))

        return ctx.null_coalescing_expression().accept(self)

    def visitNull_coalescing_expression(self, ctx: CSharpParser.Null_coalescing_expressionContext):
        if ctx.OP_COALESCING():
            return ASTNullCoalescingExpressionNode(ctx.conditional_or_expression().accept(self),
                                                   ctx.null_coalescing_expression().accept(self))

        return ctx.conditional_or_expression().accept(self)

    def visitConditional_or_expression(self, ctx: CSharpParser.Conditional_or_expressionContext):
        return self.build_bin_op(ASTLogicalOperation.OR, self.visitChildren(ctx))

    def visitConditional_and_expression(self, ctx: CSharpParser.Conditional_and_expressionContext):
        return self.build_bin_op(ASTLogicalOperation.AND, self.visitChildren(ctx))

    def visitInclusive_or_expression(self, ctx: CSharpParser.Inclusive_or_expressionContext):
        return self.build_bin_op(ASTBitwiseOperation.OR, self.visitChildren(ctx))

    def visitExclusive_or_expression(self, ctx: CSharpParser.Exclusive_or_expressionContext):
        return self.build_bin_op(ASTBitwiseOperation.XOR, self.visitChildren(ctx))

    def visitAnd_expression(self, ctx: CSharpParser.And_expressionContext):
        return self.build_bin_op(ASTBitwiseOperation.AND, self.visitChildren(ctx))

    def visitEquality_expression(self, ctx: CSharpParser.Equality_expressionContext):
        operators = {
            "==": ASTComparisonOperation.EQUAL,
            "!=": ASTComparisonOperation.NOT_EQUAL
        }

        return self.build_bin_op_choice(
            [child.accept(self) if isinstance(child, CSharpParser.Relational_expressionContext) else operators[
                child.getText()] for child in ctx.getChildren()])

    def visitRelational_expression(self, ctx: CSharpParser.Relational_expressionContext):
        operators = {
            "<": ASTComparisonOperation.LESS_THAN,
            ">": ASTComparisonOperation.GREATER_THAN,
            "<=": ASTComparisonOperation.LESS_THAN_OR_EQUAL,
            ">=": ASTComparisonOperation.GREATER_THAN_OR_EQUAL
        }

        return self.build_bin_op_choice(
            [child.accept(self) if isinstance(child, CSharpParser.Shift_expressionContext) else operators[
                child.getText()] for child in ctx.getChildren()])

    def visitShift_expression(self, ctx: CSharpParser.Shift_expressionContext):
        operators = {
            "<<": ASTBitwiseOperation.LEFT_SHIFT,
            ">>": ASTBitwiseOperation.RIGHT_SHIFT
        }

        return self.build_bin_op_choice([child.accept(self) if isinstance(child,
                                                                          CSharpParser.Additive_expressionContext) else
                                         operators[child.getText()] for child in ctx.getChildren()])

    def visitAdditive_expression(self, ctx: CSharpParser.Additive_expressionContext):
        operators = {
            "+": ASTArithmeticOperation.ADD,
            "-": ASTArithmeticOperation.SUBTRACT
        }
        return self.build_bin_op_choice([child.accept(self) if isinstance(child,
                                                                          CSharpParser.Multiplicative_expressionContext) else
                                         operators[child.getText()] for child in ctx.getChildren()])

    def visitMultiplicative_expression(self, ctx: CSharpParser.Multiplicative_expressionContext):
        operators = {
            "*": ASTArithmeticOperation.MULTIPLY,
            "/": ASTArithmeticOperation.DIVIDE,
            "%": ASTArithmeticOperation.MODULO,
        }

        return self.build_bin_op_choice([child.accept(self) if isinstance(child,
                                                                          CSharpParser.Unary_expressionContext) else
                                         operators[child.getText()] for child in ctx.getChildren()])

    def visitUnary_expression(self, ctx: CSharpParser.Unary_expressionContext):
        primary_expression = ctx.primary_expression()
        if primary_expression:
            return primary_expression.accept(self)

        unary_expression = ctx.unary_expression().accept(self)

        if ctx.OPEN_PARENS():
            return ASTTypeCastNode(ctx.type_().accept(self), unary_expression)

        if ctx.AWAIT():
            return ASTAwaitNode(unary_expression)

        operators = {
            "+": ASTUnaryOperation.POSITIVE,
            "-": ASTUnaryOperation.ARITHMETIC_NEGATION,
            "!": ASTUnaryOperation.LOGICAL_NEGATION,
            "~": ASTUnaryOperation.BITWISE_INVERSION,
            "++": ASTUnaryOperation.INCREMENT,
            "--": ASTUnaryOperation.DECREMENT,
            "&": ASTUnaryOperation.ADDRESS,
            "*": ASTUnaryOperation.POINTER_DEREFERENCE
        }

        return ASTUnaryOperationNode(operators[ctx.getChild(0).getText()], unary_expression)

    def visitPrimary_expression(self, ctx: CSharpParser.Primary_expressionContext):
        return super().visitPrimary_expression(ctx)

    def visitLiteralExpression(self, ctx: CSharpParser.LiteralExpressionContext):
        return ctx.literal().accept(self)

    def visitSimpleNameExpression(self, ctx: CSharpParser.SimpleNameExpressionContext):
        identifier = ctx.identifier().accept(self)

        type_argument_list = ctx.type_argument_list()
        if type_argument_list:
            return ASTTypeNode(identifier, type_argument_list.accept(self))

        return identifier

    def visitParenthesisExpressions(self, ctx: CSharpParser.ParenthesisExpressionsContext):
        return ctx.expression().accept(self)

    def visitMemberAccessExpression(self, ctx: CSharpParser.MemberAccessExpressionContext):
        return ctx.getChild(0).accept(self)

    def visitLiteralAccessExpression(self, ctx: CSharpParser.LiteralAccessExpressionContext):
        return ASTIdentifierNode(ctx.getText())

    def visitThisReferenceExpression(self, ctx: CSharpParser.ThisReferenceExpressionContext):
        return ASTIdentifierNode(ctx.getText())

    def visitBaseAccessExpression(self, ctx: CSharpParser.BaseAccessExpressionContext):
        base = ASTIdentifierNode(ctx.BASE().getText())
        expression_list = ctx.expression_list()
        if expression_list:
            return ASTAccessNode(base, expression_list.accept(self))

        identifier = ctx.identifier().accept(self)
        type_argument_list = ctx.type_argument_list()
        if type_argument_list:
            return ASTMemberNode(base, ASTTypeNode(identifier, type_argument_list.accept(self)))

        return ASTMemberNode(base, identifier)

    def visitObjectCreationExpression(self, ctx: CSharpParser.ObjectCreationExpressionContext):
        return super().visitObjectCreationExpression(ctx)

    def visitTypeofExpression(self, ctx: CSharpParser.TypeofExpressionContext):
        return ASTCallNode(ASTIdentifierNode(ctx.TYPEOF().getText()), ctx.getChild(2).accept(self))

    def visitCheckedExpression(self, ctx: CSharpParser.CheckedExpressionContext):
        return ASTCallNode(ASTIdentifierNode(ctx.CHECKED().getText()), ctx.expression().accept(self))

    def visitUncheckedExpression(self, ctx: CSharpParser.UncheckedExpressionContext):
        return ASTCallNode(ASTIdentifierNode(ctx.UNCHECKED().getText()), ctx.expression().accept(self))

    def visitDefaultValueExpression(self, ctx: CSharpParser.DefaultValueExpressionContext):
        return ASTCallNode(ASTIdentifierNode(ctx.DEFAULT().getText()), ctx.type_().accept(self))

    def visitAnonymousMethodExpression(self, ctx: CSharpParser.AnonymousMethodExpressionContext):
        async_ = ctx.ASYNC() is not None
        block = ctx.block().accept(self)

        parameter_list = ctx.explicit_anonymous_function_parameter_list()
        if parameter_list:
            anonymous_function_definition = ASTAnonymousFunctionDefinitionNode(block, parameter_list.accept(self))
            if async_:
                return ASTAsyncNode(anonymous_function_definition)

            return anonymous_function_definition

        anonymous_function_definition = ASTAnonymousFunctionDefinitionNode(block)
        if async_:
            return ASTAsyncNode(anonymous_function_definition)

        return anonymous_function_definition

    def visitSizeofExpression(self, ctx: CSharpParser.SizeofExpressionContext):
        return ASTCallNode(ASTIdentifierNode(ctx.SIZEOF().getText()), ctx.type_().accept(self))

    def visitNameofExpression(self, ctx: CSharpParser.NameofExpressionContext):
        return ASTCallNode(ASTIdentifierNode(ctx.NAMEOF().getText()),
                           self.build_left_associated([identifier.accept(self) for identifier in ctx.identifier()],
                                                      ASTMemberNode))

    def visitMember_access(self, ctx: CSharpParser.Member_accessContext):
        null_conditional_operator = ctx.INTERR() is not None

        type_argument_list = ctx.type_argument_list()
        if type_argument_list:
            return ASTTypeNode(ctx.identifier().accept(self), type_argument_list.accept(self)), null_conditional_operator

        return ctx.identifier().accept(self), null_conditional_operator

    def visitBracket_expression(self, ctx: CSharpParser.Bracket_expressionContext):
        return self.build_multi(self.visitChildren(ctx), ASTSubscriptsNode), (ctx.INTERR() is not None)

    def visitIndexer_argument(self, ctx: CSharpParser.Indexer_argumentContext):
        expression = ctx.expression()

        identifier = ctx.identifier()
        if identifier:
            return ASTIndexNode(ASTKeywordArgumentNode(identifier.accept(self), expression.accept(self)))

        return ASTIndexNode(expression.accept(self))

    def visitPredefined_type(self, ctx: CSharpParser.Predefined_typeContext):
        return ASTIdentifierNode(ctx.getText())

    def visitExpression_list(self, ctx: CSharpParser.Expression_listContext):
        return self.build_multi(self.visitChildren(ctx), ASTExpressionsNode)

    def visitObject_or_collection_initializer(self, ctx: CSharpParser.Object_or_collection_initializerContext):
        return ctx.getChild(0).accept(self)

    def visitObject_initializer(self, ctx: CSharpParser.Object_initializerContext):
        member_initializer_list = ctx.member_initializer_list()
        if member_initializer_list:
            return ASTInitializerNode(member_initializer_list.accept(self))

        return ASTInitializerNode()

    def visitMember_initializer_list(self, ctx: CSharpParser.Member_initializer_listContext):
        return self.build_multi(self.visitChildren(ctx), ASTExpressionsNode)

    def visitMember_initializer(self, ctx: CSharpParser.Member_initializerContext):
        initializer_value = ctx.initializer_value().accept(self)

        identifier = ctx.identifier()
        if identifier:
            return ASTAssignmentStatementNode(identifier.accept(self), initializer_value)

        return ASTAssignmentStatementNode(ASTIndexNode(ctx.expression().accept(self)), initializer_value)

    def visitInitializer_value(self, ctx: CSharpParser.Initializer_valueContext):
        return ctx.getChild(0).accept(self)

    def visitCollection_initializer(self, ctx: CSharpParser.Collection_initializerContext):
        return ASTInitializerNode(self.build_multi(self.visitChildren(ctx), ASTElementsNode))

    def visitElement_initializer(self, ctx: CSharpParser.Element_initializerContext):
        non_assignment_expression = ctx.non_assignment_expression()
        if non_assignment_expression:
            return non_assignment_expression.accept(self)

        return ctx.expression_list().accept(self)

    def visitAnonymous_object_initializer(self, ctx: CSharpParser.Anonymous_object_initializerContext):
        member_declarator_list = ctx.member_declarator_list()
        if member_declarator_list:
            return ASTInitializerNode(member_declarator_list.accept(self))

        return ASTInitializerNode()

    def visitMember_declarator_list(self, ctx: CSharpParser.Member_declarator_listContext):
        return self.build_multi(self.visitChildren(ctx), ASTExpressionsNode)

    def visitMember_declarator(self, ctx: CSharpParser.Member_declaratorContext):
        primary_expression = ctx.primary_expression()
        if primary_expression:
            return primary_expression.accept(self)

        return ASTAssignmentStatementNode(ctx.identifier().accept(self), ctx.expression().accept(self))

    def visitUnbound_type_name(self, ctx: CSharpParser.Unbound_type_nameContext):
        return self.build_left_associated([identifier.accept(self) for identifier in ctx.identifier()], ASTMemberNode)

    def visitGeneric_dimension_specifier(self, ctx: CSharpParser.Generic_dimension_specifierContext):
        return super().visitGeneric_dimension_specifier(ctx)

    def visitIsType(self, ctx: CSharpParser.IsTypeContext):
        # TODO
        return ctx.base_type().accept(self)

    def visitLambda_expression(self, ctx: CSharpParser.Lambda_expressionContext):
        anonymous_function = ASTAnonymousFunctionDefinitionNode(ctx.anonymous_function_body().accept(self), ctx.anonymous_function_signature().accept(self))
        if ctx.ASYNC():
            return ASTAsyncNode(anonymous_function)

        return anonymous_function

    def visitAnonymous_function_signature(self, ctx: CSharpParser.Anonymous_function_signatureContext):
        identifier = ctx.identifier()
        if identifier:
            return identifier.accept(self)

        explicit_anonymous_function_parameter_list = ctx.explicit_anonymous_function_parameter_list()
        if explicit_anonymous_function_parameter_list:
            return explicit_anonymous_function_parameter_list.accept(self)

        implicit_anonymous_function_parameter_list = ctx.implicit_anonymous_function_parameter_list()
        if implicit_anonymous_function_parameter_list:
            return implicit_anonymous_function_parameter_list.accept(self)

    def visitExplicit_anonymous_function_parameter_list(self,
                                                        ctx: CSharpParser.Explicit_anonymous_function_parameter_listContext):
        return self.build_multi(self.visitChildren(ctx), ASTParametersNode)

    def visitExplicit_anonymous_function_parameter(self,
                                                   ctx: CSharpParser.Explicit_anonymous_function_parameterContext):
        modifiers = {
            "out": ASTMiscModifier.OUT,
            "ref": ASTMiscModifier.REF
        }

        type_ = ctx.type_().accept(self)
        identifier = ctx.identifier().accept(self)

        refout = ctx.refout()
        if refout:
            return ASTParameterNode(identifier, type_, modifiers=[modifiers[refout.getText()]])

        return ASTParameterNode(identifier, type_)

    def visitImplicit_anonymous_function_parameter_list(self,
                                                        ctx: CSharpParser.Implicit_anonymous_function_parameter_listContext):
        return self.build_multi([ASTParameterNode(identifier) for identifier in self.visitChildren(ctx)], ASTParametersNode)

    def visitAnonymous_function_body(self, ctx: CSharpParser.Anonymous_function_bodyContext):
        return ctx.getChild(0).accept(self)

    def visitQuery_expression(self, ctx: CSharpParser.Query_expressionContext):
        return ASTQueryNode([ctx.from_clause().accept(self)] + ctx.query_body().accept(self))

    def visitFrom_clause(self, ctx: CSharpParser.From_clauseContext):
        return ASTFromClauseNode(ctx.identifier().accept(self), ctx.expression().accept(self))

    def visitQuery_body(self, ctx: CSharpParser.Query_bodyContext):
        clauses = []

        for clause in ctx.query_body_clause():
            visited_clause = clause.accept(self)
            if isinstance(visited_clause, list):
                clauses.extend(visited_clause)
            else:
                clauses.append(visited_clause)

        clauses.append(ctx.select_or_group_clause().accept(self))

        query_continuation = ctx.query_continuation()
        if query_continuation:
            clauses.extend(query_continuation.accept(self))

        return clauses

    def visitQuery_body_clause(self, ctx: CSharpParser.Query_body_clauseContext):
        return ctx.getChild(0).accept(self)

    def visitLet_clause(self, ctx: CSharpParser.Let_clauseContext):
        return ASTLetClauseNode(ctx.identifier().accept(self), ctx.expression().accept(self))

    def visitWhere_clause(self, ctx: CSharpParser.Where_clauseContext):
        return ASTWhereClauseNode(ctx.expression().accept(self))

    def visitCombined_join_clause(self, ctx: CSharpParser.Combined_join_clauseContext):
        target_range_variable = ctx.identifier(0).accept(self)
        target_source = ctx.expression(0).accept(self)
        left_key = ctx.expression(1).accept(self)
        right_key = ctx.expression(2).accept(self)

        if ctx.INTO():
            return [ASTJoinClauseNode(target_range_variable, target_source, left_key, right_key), ASTIntoClauseNode(ctx.identifier(1).accept(self))]

        return ASTJoinClauseNode(target_range_variable, target_source, left_key, right_key)

    def visitOrderby_clause(self, ctx: CSharpParser.Orderby_clauseContext):
        return ASTOrderByClauseNode(self.build_multi(self.visitChildren(ctx), ASTExpressionsNode))

    def visitOrdering(self, ctx: CSharpParser.OrderingContext):
        expression = ctx.expression().accept(self)

        direction = ctx.dir_()
        if direction:
            return ASTOrderingNode(expression, direction.accept(self))

        return ASTOrderingNode(expression)

    def visitSelect_or_group_clause(self, ctx: CSharpParser.Select_or_group_clauseContext):
        if ctx.SELECT():
            return ASTSelectClauseNode(ctx.expression(0).accept(self))

        return ASTGroupByClauseNode(ctx.expression(0).accept(self), ctx.expression(1).accept(self))

    def visitQuery_continuation(self, ctx: CSharpParser.Query_continuationContext):
        return [ASTIntoClauseNode(ctx.identifier().accept(self))] + ctx.query_body().accept(self)

    def visitLabeledStatement(self, ctx: CSharpParser.LabeledStatementContext):
        return ctx.getChild(0).accept(self)

    def visitDeclarationStatement(self, ctx: CSharpParser.DeclarationStatementContext):
        return ctx.getChild(0).accept(self)

    def visitEmbeddedStatement(self, ctx: CSharpParser.EmbeddedStatementContext):
        return ctx.getChild(0).accept(self)

    def visitLabeled_Statement(self, ctx: CSharpParser.Labeled_StatementContext):
        return ASTLabelNode(ctx.identifier().accept(self), ctx.statement().accept(self))

    def visitEmbedded_statement(self, ctx: CSharpParser.Embedded_statementContext):
        return ctx.getChild(0).accept(self)

    def visitTheEmptyStatement(self, ctx: CSharpParser.TheEmptyStatementContext):
        return self.defaultResult()

    def visitExpressionStatement(self, ctx: CSharpParser.ExpressionStatementContext):
        return ctx.expression().accept(self)  # TODO: Convert to statement somehow

    def visitIfStatement(self, ctx: CSharpParser.IfStatementContext):
        condition = ctx.expression().accept(self)
        body = ctx.if_body(0).accept(self)

        if ctx.ELSE():
            return ASTIfElseStatementNode(condition, body, ctx.if_body(1).accept(self))

        return ASTIfStatementNode(condition, body)

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
