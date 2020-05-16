from antlr4 import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl

from metrics.parsers.csharp.base.CSharpParser import CSharpParser
from metrics.parsers.csharp.base.CSharpParserVisitor import CSharpParserVisitor
from metrics.structures.ast import *
from metrics.visitors.structures.ast_generation_visitor import ASTGenerationVisitor as BaseASTGenerationVisitor


class ASTGenerationVisitor(BaseASTGenerationVisitor, CSharpParserVisitor):
    # region Helpers

    def build_type(self, base_type: ASTNode,
                   extensions: Optional[Sequence[Union[TerminalNodeImpl, ParserRuleContext]]] = None) -> ASTNode:
        if not extensions:
            return base_type

        extension = extensions[-1]
        if isinstance(extension, TerminalNodeImpl):
            if extension.getSymbol() == CSharpParser.INTERR:
                return ASTNullableTypeNode(self.build_type(base_type, extensions[:-1]))

            if extension.getSymbol() == CSharpParser.STAR:
                return ASTPointerTypeNode(self.build_type(base_type, extensions[:-1]))

        if isinstance(extension, CSharpParser.Rank_specifierContext):
            return ASTArrayTypeNode(self.build_type(base_type, extensions[:-1]), extension.accept(self))

        return self.build_type(base_type, extensions[:-1])

    def build_primary_expression(self, children: Optional[Sequence[Union[TerminalNodeImpl, ParserRuleContext]]] = None):
        if not children:
            return None

        if len(children) == 1:
            return children[0].accept(self)

        child = children[-1]
        if isinstance(child, TerminalNodeImpl):
            # Increment
            if child.getSymbol() == CSharpParser.OP_INC:
                return ASTUnaryOperationNode(ASTUnaryOperation.INCREMENT, self.build_primary_expression(children[:-1]))

            # Decrement
            if child.getSymbol() == CSharpParser.OP_DEC:
                return ASTUnaryOperationNode(ASTUnaryOperation.DECREMENT, self.build_primary_expression(children[:-1]))

        # Bracket expression
        if isinstance(child, CSharpParser.Bracket_expressionContext):
            index, null_conditional = child.accept(self)
            sequence = self.build_primary_expression(children[:-1])

            if null_conditional:
                return ASTAccessNode(ASTUnaryOperationNode(ASTUnaryOperation.NULL_CONDITIONAL, sequence), index)

            return ASTAccessNode(sequence, index)

        # Pointer target member access
        if isinstance(child, CSharpParser.IdentifierContext):
            return ASTMemberNode(ASTUnaryOperationNode(ASTUnaryOperation.POINTER_DEREFERENCE,
                                                       self.build_primary_expression(children[:-2])),
                                 child.accept(self))

        # Method call
        if isinstance(child, CSharpParser.Method_invocationContext):
            return ASTCallNode(self.build_primary_expression(children[:-1]), child.accept(self))

        # Member access
        if isinstance(child, CSharpParser.Member_accessContext):
            member, null_conditional = child.accept(self)
            parent = self.build_primary_expression(children[:-1])

            if null_conditional:
                return ASTMemberNode(ASTUnaryOperationNode(ASTUnaryOperation.NULL_CONDITIONAL, parent), member)

            return ASTMemberNode(parent, member)

        # Skip
        return self.build_primary_expression(children[:-1])

    def build_array_or_pointer_type(self,
                                    children: Optional[Sequence[Union[TerminalNodeImpl, ParserRuleContext]]] = None):
        if not children:
            return None

        if len(children) == 1:
            return children[0].accept(self)

        child = children[-1]
        if isinstance(child, TerminalNodeImpl):
            if isinstance(child, CSharpParser.STAR):
                return ASTPointerTypeNode(self.build_array_or_pointer_type(children[:-1]))
            else:
                return ASTNullableTypeNode(self.build_array_or_pointer_type(children[:-1]))

        if isinstance(child, CSharpParser.Rank_specifierContext):
            return ASTArrayTypeNode(self.build_array_or_pointer_type(children[:-1]), child.accept(self))

        return self.build_array_or_pointer_type(children[:-1])

    @staticmethod
    def add_to_multi(multi: ASTMultiplesNode, child: ASTNode):
        if isinstance(child, ASTMultiplesNode):
            for child in child.children:
                multi.add_child(child)
        elif child:
            multi.add_child(child)

    # endregion

    # region Visits

    def visitCompilation_unit(self, ctx: CSharpParser.Compilation_unitContext):
        statements = ASTStatementsNode([])

        extern_alias_directives = ctx.extern_alias_directives()
        if extern_alias_directives:
            self.add_to_multi(statements, extern_alias_directives.accept(self))

        using_directives = ctx.using_directives()
        if using_directives:
            self.add_to_multi(statements, using_directives.accept(self))

        global_attribute_sections = ctx.global_attribute_section()
        if global_attribute_sections:
            self.add_to_multi(statements, self.build_multi([gas.accept(self) for gas in global_attribute_sections],
                                                           ASTStatementsNode))

        namespace_member_declarations = ctx.namespace_member_declarations()
        if namespace_member_declarations:
            self.add_to_multi(statements, namespace_member_declarations.accept(self))

        return statements

    def visitNamespace_or_type_name(self, ctx: CSharpParser.Namespace_or_type_nameContext):
        children = ctx.getChildren(lambda child: self.filter_child(child, CSharpParser.IdentifierContext,
                                                                   CSharpParser.Type_argument_listContext))

        members = []
        i = 0
        while i < len(children):
            if isinstance(children[i], CSharpParser.IdentifierContext):
                if isinstance(children[i + 1], CSharpParser.Type_argument_listContext):
                    members.append(ASTTypeNode(children[i].accept(self), children[i + 1].accept(self)))
                    i += 1
                else:
                    members.append(children[i].accept(self))
            i += 1

        qualified_alias_member = ctx.qualified_alias_member()
        if qualified_alias_member:
            members = [(qualified_alias_member.accept(self))] + [members]

        return self.build_left_associated(members, ASTMemberNode)

    def visitType_(self, ctx: CSharpParser.Type_Context):
        base = ctx.base_type().accept(self)
        extensions = ctx.getChildren(
            lambda child: self.filter_child(child, CSharpParser.INTERR, CSharpParser.Rank_specifierContext,
                                            CSharpParser.STAR))
        return self.build_type(base, extensions)

    def visitBase_type(self, ctx: CSharpParser.Base_typeContext):
        simple_type = ctx.simple_type()
        if simple_type:
            return simple_type.accept(self)

        class_type = ctx.class_type()
        if class_type:
            return class_type.accept(self)

        return ASTPointerTypeNode(ctx.VOID().getText())

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
        value = ctx.expression().accept(self)

        modifiers = ctx.refout()
        if modifiers:
            modifiers = [modifiers.getText()]

        if ctx.VAR():
            value = ASTVariableDeclarationNode(value, ASTIdentifierNode(ctx.VAR().getText()))
        elif ctx.type_():
            value = ASTVariableDeclarationNode(value, ASTIdentifierNode(ctx.type_().accept(self)))

        parameter = ctx.identifier()
        if parameter:
            return ASTKeywordArgumentNode(parameter.accept(self), value, modifiers)

        return ASTArgumentNode(value, modifiers)

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
        children = [
            child.accept(self) if isinstance(child, CSharpParser.Multiplicative_expressionContext) else operators[
                child.getText()] for child in ctx.getChildren()]
        return self.build_bin_op_choice(children)

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
        return self.build_primary_expression(ctx.getChildren())

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
        type_ = ctx.type_()
        if type_:
            type_ = type_.accept(self)

            # Object creation with constructor call - C() {...}
            object_creation = ctx.object_creation_expression()
            if object_creation:
                object_creation = object_creation.accept(self)
                object_creation['type'] = type_
                return object_creation

            # Object creation without constructor call - C {...}
            initializer = ctx.object_or_collection_initializer()
            if initializer:
                return ASTObjectCreationNode(type_, initializer=initializer.accept(self))

            # Array creation with size explicitly specified - C[...] {...}
            size = ctx.expression_list()
            if size:
                size = size.accept(self)

                rank_specifiers = ctx.rank_specifier()
                if rank_specifiers:
                    type_ = self.build_left_associated(
                        [type_] + [dimensions.accept(self) for dimensions in rank_specifiers], ASTArrayTypeNode)

                initializer = ctx.array_initializer()
                if initializer:
                    initializer = initializer.accept(self)

                return ASTArrayCreationNode(type_, size=size, initializer=initializer)

            # Array creation with size implied by initializer - C[] {...}
            rank_specifiers = ctx.rank_specifier()

            dimensions = rank_specifiers.accept(self)[0]

            if len(rank_specifiers) > 1:
                type_ = self.build_left_associated(
                    [type_] + [dimensions.accept(self) for dimensions in ctx.rank_specifiers()[1:]], ASTArrayTypeNode)

            initializer = ctx.array_initializer().accept(self)

            return ASTArrayCreationNode(type_, dimensions=dimensions, initializer=initializer)

        # Anonymous object creation - {...}
        initializer = ctx.anonymous_object_initializer()
        if initializer:
            return ASTObjectCreationNode(initializer=initializer)

        # Implied type array - [] {...}
        return ASTArrayCreationNode(dimensions=ctx.rank_specifier(0).accept(self),
                                    initializer=ctx.array_initializer().accept(self))

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
            return ASTTypeNode(ctx.identifier().accept(self),
                               type_argument_list.accept(self)), null_conditional_operator

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
        return ctx.getChildCount() - 1

    def visitIsType(self, ctx: CSharpParser.IsTypeContext):
        base = ctx.base_type().accept(self)
        extensions = ctx.getChildren(
            lambda child: self.filter_child(child, CSharpParser.INTERR, CSharpParser.Rank_specifierContext,
                                            CSharpParser.STAR))
        return self.build_type(base, extensions)

    def visitLambda_expression(self, ctx: CSharpParser.Lambda_expressionContext):
        anonymous_function = ASTAnonymousFunctionDefinitionNode(ctx.anonymous_function_body().accept(self),
                                                                ctx.anonymous_function_signature().accept(self))
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
        return self.build_multi([ASTParameterNode(identifier) for identifier in self.visitChildren(ctx)],
                                ASTParametersNode)

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
            return [ASTJoinClauseNode(target_range_variable, target_source, left_key, right_key),
                    ASTIntoClauseNode(ctx.identifier(1).accept(self))]

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
        return ctx.expression().accept(self)

    def visitIfStatement(self, ctx: CSharpParser.IfStatementContext):
        condition = ctx.expression().accept(self)
        body = ctx.if_body(0).accept(self)

        if ctx.ELSE():
            return ASTIfStatementNode(condition, body, ctx.if_body(1).accept(self))

        return ASTIfStatementNode(condition, body)

    def visitSwitchStatement(self, ctx: CSharpParser.SwitchStatementContext):
        return ASTSwitchStatementNode(ctx.expression().accept(self), self.build_multi(
            [switch_section.accept(self) for switch_section in ctx.switch_section()], ASTSwitchSectionsNode))

    def visitWhileStatement(self, ctx: CSharpParser.WhileStatementContext):
        return ASTLoopStatementNode(ctx.expression().accept(self), ctx.embedded_statement().accept(self))

    def visitDoStatement(self, ctx: CSharpParser.DoStatementContext):
        return ASTLoopStatementNode(ctx.expression().accept(self), ctx.embedded_statement().accept(self))

    def visitForStatement(self, ctx: CSharpParser.ForStatementContext):
        initializer = ctx.for_initializer()
        if initializer:
            initializer = initializer.accept(self)

        condition = ctx.expression()
        if condition:
            condition = condition.accept(self)

        iterator = ctx.for_iterator()
        if iterator:
            iterator = iterator.accept(self)

        body = ctx.embedded_statement().accept(self)

        if iterator:
            if isinstance(body, ASTStatementsNode):
                body.add_child(iterator)
            else:
                body = ASTStatementsNode([body, iterator])

        loop = ASTLoopStatementNode(condition, body)

        if initializer:
            return ASTStatementsNode([initializer, loop])

        return loop

    def visitForeachStatement(self, ctx: CSharpParser.ForeachStatementContext):
        condition = ASTBinaryOperationNode(ASTComparisonOperation.IN,
                                           ASTVariableDeclarationNode(ctx.identifier().accept(self),
                                                                      ctx.local_variable_type().accept(self)),
                                           ctx.expression().accept(self))
        return ASTLoopStatementNode(condition, ctx.embedded_statement().accept(self))

    def visitBreakStatement(self, ctx: CSharpParser.BreakStatementContext):
        return ASTBreakStatementNode()

    def visitContinueStatement(self, ctx: CSharpParser.ContinueStatementContext):
        return ASTContinueStatementNode()

    def visitGotoStatement(self, ctx: CSharpParser.GotoStatementContext):
        identifier = ctx.identifier()
        if identifier:
            return ASTJumpStatementNode(identifier.accept(self))

        if ctx.CASE():
            return ASTJumpStatementNode(ASTCaseLabelNode(ctx.expression().accept(self)))

        return ASTJumpStatementNode(ASTDefaultLabelNode())

    def visitReturnStatement(self, ctx: CSharpParser.ReturnStatementContext):
        expression = ctx.expression()
        if expression:
            return ASTReturnStatementNode(expression.accept(self))

        return ASTReturnStatementNode()

    def visitThrowStatement(self, ctx: CSharpParser.ThrowStatementContext):
        expression = ctx.expression()
        if expression:
            return ASTThrowStatementNode(expression.accept(self))

        return ASTThrowStatementNode()

    def visitTryStatement(self, ctx: CSharpParser.TryStatementContext):
        catches = ctx.catch_clauses()
        if catches:
            catches = catches.accept(self)

        finally_ = ctx.finally_clause()
        if finally_:
            finally_ = finally_.accept(self)

        return ASTTryStatementNode(ctx.block().accept(self), catches, finally_=finally_)

    def visitCheckedStatement(self, ctx: CSharpParser.CheckedStatementContext):
        return ctx.block().accept(self)

    def visitUncheckedStatement(self, ctx: CSharpParser.UncheckedStatementContext):
        return ctx.block().accept(self)

    def visitLockStatement(self, ctx: CSharpParser.LockStatementContext):
        return ASTLockStatementNode(ctx.expression().accept(self), ctx.embedded_statement().accept(self))

    def visitUsingStatement(self, ctx: CSharpParser.UsingStatementContext):
        return ASTWithStatementNode(ctx.resource_acquisition().accept(self), ctx.embedded_statement().accept(self))

    def visitYieldStatement(self, ctx: CSharpParser.YieldStatementContext):
        if ctx.BREAK():
            return ASTYieldStatementNode(ASTBreakStatementNode())

        return ASTYieldStatementNode(ASTReturnStatementNode(ctx.expression().accept(self)))

    def visitUnsafeStatement(self, ctx: CSharpParser.UnsafeStatementContext):
        return ctx.block().accept(self)

    def visitFixedStatement(self, ctx: CSharpParser.FixedStatementContext):
        return ctx.embedded_statement().accept(self)

    def visitBlock(self, ctx: CSharpParser.BlockContext):
        return ctx.statement_list().accept(self)

    def visitLocal_variable_declaration(self, ctx: CSharpParser.Local_variable_declarationContext):
        type_ = ctx.local_variable_type()
        if type_:
            type_ = type_.accept(self)

        return self.build_multi([ASTVariableDeclarationNode(type_=type_, **(declarator.accept(self))) for declarator in
                                 ctx.local_variable_declarator()], ASTVariableDeclarationsNode)

    def visitLocal_variable_type(self, ctx: CSharpParser.Local_variable_typeContext):
        var = ctx.VAR()
        if var:
            return ASTIdentifierNode(var.getText())

        return ctx.type_().accept(self)

    def visitLocal_variable_declarator(self, ctx: CSharpParser.Local_variable_declaratorContext):
        identifier = ctx.identifier().accept(self)

        local_variable_initializer = ctx.local_variable_initializer()
        if local_variable_initializer:
            return {
                "name": identifier,
                "initial_value": local_variable_initializer.accept(self)
            }

        return {
            "variable": identifier
        }

    def visitLocal_variable_initializer(self, ctx: CSharpParser.Local_variable_initializerContext):
        return ctx.getChild(0).accept(self)

    def visitLocal_constant_declaration(self, ctx: CSharpParser.Local_constant_declarationContext):
        type_ = ctx.type_().accept(self)

        return self.build_multi([ASTConstantDeclarationNode(type_=type_, **(declarator.accept(self))) for declarator in
                                 ctx.constant_declarators().accept(self)], ASTConstantDeclarationsNode)

    def visitIf_body(self, ctx: CSharpParser.If_bodyContext):
        return ctx.getChild(0).accept(self)

    def visitSwitch_section(self, ctx: CSharpParser.Switch_sectionContext):
        return ASTSwitchSectionNode(
            self.build_multi([label.accept(self) for label in ctx.switch_label()], ASTSwitchLabelsNode),
            ctx.statement_list().accept(self))

    def visitSwitch_label(self, ctx: CSharpParser.Switch_labelContext):
        if ctx.CASE():
            return ASTCaseLabelNode(ctx.expression().accept(self))

        return ASTDefaultLabelNode()

    def visitStatement_list(self, ctx: CSharpParser.Statement_listContext):
        return self.build_multi(self.visitChildren(ctx), ASTStatementsNode)

    def visitFor_initializer(self, ctx: CSharpParser.For_initializerContext):
        if ctx.expression():
            return self.build_multi(self.visitChildren(ctx), ASTExpressionsNode)

        return ctx.local_variable_declaration().accept(self)

    def visitFor_iterator(self, ctx: CSharpParser.For_iteratorContext):
        return self.build_multi(self.visitChildren(ctx), ASTExpressionsNode)

    def visitCatch_clauses(self, ctx: CSharpParser.Catch_clausesContext):
        return self.build_multi(self.visitChildren(ctx), ASTCatchesNode)

    def visitSpecific_catch_clause(self, ctx: CSharpParser.Specific_catch_clauseContext):
        type_ = ctx.class_type().accept(self)

        identifier = ctx.identifier()
        if identifier:
            identifier = identifier.accept(self)

        condition = ctx.exception_filter()
        if condition:
            condition = condition.accept(self)

        body = ctx.block().accept(self)

        if identifier:
            return ASTCatchNode(ASTAliasNode(type_, identifier), condition, body)

        return ASTCatchNode(type_, condition, body)

    def visitGeneral_catch_clause(self, ctx: CSharpParser.General_catch_clauseContext):
        body = ctx.block().accept(self)

        condition = ctx.exception_filter()
        if condition:
            return ASTCatchNode(condition=condition.accept(self), body=body)

        return ASTCatchNode(body=body)

    def visitException_filter(self, ctx: CSharpParser.Exception_filterContext):
        return ctx.expression().accept(self)

    def visitFinally_clause(self, ctx: CSharpParser.Finally_clauseContext):
        return ASTFinallyNode(ctx.block().accept(self))

    def visitResource_acquisition(self, ctx: CSharpParser.Resource_acquisitionContext):
        return ctx.getChild(0).accept(self)

    def visitNamespace_declaration(self, ctx: CSharpParser.Namespace_declarationContext):
        return ASTNamespaceDeclarationNode(ctx.qualified_identifier().accept(self), ctx.namespace_body().accept(self))

    def visitQualified_identifier(self, ctx: CSharpParser.Qualified_identifierContext):
        return self.build_left_associated(self.visitChildren(ctx), ASTMemberNode)

    def visitNamespace_body(self, ctx: CSharpParser.Namespace_bodyContext):
        statements = ASTStatementsNode([])

        extern_alias_directives = ctx.extern_alias_directives()
        if extern_alias_directives:
            self.add_to_multi(statements, extern_alias_directives.accept(self))

        using_directives = ctx.using_directives()
        if using_directives:
            self.add_to_multi(statements, using_directives.accept(self))

        namespace_member_declarations = ctx.namespace_member_declarations()
        if namespace_member_declarations:
            self.add_to_multi(statements, namespace_member_declarations.accept(self))

        return statements

    def visitExtern_alias_directives(self, ctx: CSharpParser.Extern_alias_directivesContext):
        return self.build_multi(self.visitChildren(ctx), ASTStatementsNode)

    def visitExtern_alias_directive(self, ctx: CSharpParser.Extern_alias_directiveContext):
        return ASTExternAliasDirectiveNode(ctx.identifier().accept(self))

    def visitUsing_directives(self, ctx: CSharpParser.Using_directivesContext):
        return self.build_multi(self.visitChildren(ctx), ASTStatementsNode)

    def visitUsingAliasDirective(self, ctx: CSharpParser.UsingAliasDirectiveContext):
        return ASTImportStatementNode(
            ASTAliasNode(ctx.namespace_or_type_name().accept(self), ctx.identifier().accept(self)))

    def visitUsingNamespaceDirective(self, ctx: CSharpParser.UsingNamespaceDirectiveContext):
        return ASTImportStatementNode(ctx.namespace_or_type_name().accept(self))

    def visitUsingStaticDirective(self, ctx: CSharpParser.UsingStaticDirectiveContext):
        return ASTImportStatementNode(ctx.namespace_or_type_name().accept(self), [ASTMiscModifier.STATIC])

    def visitNamespace_member_declarations(self, ctx: CSharpParser.Namespace_member_declarationsContext):
        return self.build_multi(self.visitChildren(ctx), ASTStatementsNode)

    def visitNamespace_member_declaration(self, ctx: CSharpParser.Namespace_member_declarationContext):
        return ctx.getChild(0).accept(self)

    def visitType_declaration(self, ctx: CSharpParser.Type_declarationContext):
        declared_type = ctx.getChild(ctx.getChildCount() - 1).accept(self)

        modifiers = ctx.all_member_modifiers()
        if modifiers:
            declared_type.modifiers.extend(modifiers)

        attributes = ctx.attributes()
        if attributes:
            declared_type["attributes"] = attributes.accept(self)

        return declared_type

    def visitQualified_alias_member(self, ctx: CSharpParser.Qualified_alias_memberContext):
        alias = ctx.identifier(0).accept(self)
        member = ctx.identifier(1).accept(self)

        type_arguments = ctx.type_argument_list()
        if type_arguments:
            return ASTMemberNode(alias, ASTTypeNode(member, type_arguments))

        return ASTMemberNode(alias, member)

    def visitType_parameter_list(self, ctx: CSharpParser.Type_parameter_listContext):
        return self.build_multi(self.visitChildren(ctx), ASTParametersNode)

    def visitType_parameter(self, ctx: CSharpParser.Type_parameterContext):
        identifier = ctx.identifier().accept(self)

        attributes = ctx.attributes()
        if attributes:
            return ASTParameterNode(identifier, attributes=attributes.accept(self))

        return ASTParameterNode(identifier)

    def visitClass_base(self, ctx: CSharpParser.Class_baseContext):
        return self.build_multi(self.visitChildren(ctx), ASTArgumentsNode)

    def visitInterface_type_list(self, ctx: CSharpParser.Interface_type_listContext):
        return self.build_multi(self.visitChildren(ctx), ASTArgumentsNode)

    def visitType_parameter_constraints_clauses(self, ctx: CSharpParser.Type_parameter_constraints_clausesContext):
        return self.build_multi(self.visitChildren(ctx), ASTConstraintsClausesNode)

    def visitType_parameter_constraints_clause(self, ctx: CSharpParser.Type_parameter_constraints_clauseContext):
        return ASTConstraintsClauseNode(ctx.identifier().accept(self), ctx.type_parameter_constraints().accept(self))

    def visitType_parameter_constraints(self, ctx: CSharpParser.Type_parameter_constraintsContext):
        return self.build_multi(self.visitChildren(ctx), ASTConstraintsNode)

    def visitPrimary_constraint(self, ctx: CSharpParser.Primary_constraintContext):
        class_type = ctx.class_type()
        if class_type:
            return class_type.accept(self)

        return ASTIdentifierNode(ctx.getText())

    def visitSecondary_constraints(self, ctx: CSharpParser.Secondary_constraintsContext):
        return self.visitChildren(ctx)

    def visitConstructor_constraint(self, ctx: CSharpParser.Constructor_constraintContext):
        return ASTIdentifierNode(ctx.getText())

    def visitClass_body(self, ctx: CSharpParser.Class_bodyContext):
        body = ctx.class_member_declarations()
        if body:
            return body.accept(self)

    def visitClass_member_declarations(self, ctx: CSharpParser.Class_member_declarationsContext):
        return self.build_multi(self.visitChildren(ctx), ASTStatementsNode)

    def visitClass_member_declaration(self, ctx: CSharpParser.Class_member_declarationContext):
        class_member = ctx.getChild(ctx.getChildCount() - 1).accept(self)

        modifiers = ctx.all_member_modifiers()
        if modifiers:
            class_member.modifiers.extend(modifiers)

        attributes = ctx.attributes()
        if attributes:
            class_member["attributes"] = attributes.accept(self)

        return class_member

    def visitAll_member_modifiers(self, ctx: CSharpParser.All_member_modifiersContext):
        return self.visitChildren(ctx)

    def visitAll_member_modifier(self, ctx: CSharpParser.All_member_modifierContext):
        return {
            "new": ASTMiscModifier.NEW,
            "public": ASTVisibilityModifier.PUBLIC,
            "protected": ASTVisibilityModifier.PROTECTED,
            "internal": ASTVisibilityModifier.INTERNAL,
            "private": ASTVisibilityModifier.PRIVATE,
            "readonly": ASTMiscModifier.READONLY,
            "volatile": ASTMiscModifier.VOLATILE,
            "virtual": ASTMiscModifier.VIRTUAL,
            "sealed": ASTMiscModifier.SEALED,
            "override": ASTMiscModifier.OVERRIDE,
            "abstract": ASTMiscModifier.ABSTRACT,
            "static": ASTMiscModifier.STATIC,
            "unsafe": ASTMiscModifier.UNSAFE,
            "extern": ASTMiscModifier.EXTERN,
            "partial": ASTMiscModifier.PARTIAL,
            "async": ASTMiscModifier.ASYNC
        }[ctx.getText()]

    def visitCommon_member_declaration(self, ctx: CSharpParser.Common_member_declarationContext):
        if ctx.VOID():
            return ctx.method_declaration().accept(self)

        definition = ctx.getChild(0).accept(self)
        if ctx.getChildCount() == 2:
            definition["body"] = ctx.getChild(1).accept(self)

        return definition

    def visitTyped_member_declaration(self, ctx: CSharpParser.Typed_member_declarationContext):
        if ctx.getChildCount() == 2:
            declaration = ctx.getChild(1).accept(self)
            declaration["name"] = ASTMemberNode(ctx.namespace_or_type_name().accept(self), declaration["name"])
        else:
            declaration = ctx.getChild(0).accept(self)

        type_ = ctx.type_().accept(self)
        if isinstance(declaration, (ASTIndexerDefinitionNode, ASTFunctionDefinitionNode, ASTOperatorOverloadDefinitionNode)):
            declaration["return_type"] = type_
        else:
            declaration["type"] = type_

        return declaration

    def visitConstant_declarators(self, ctx: CSharpParser.Constant_declaratorsContext):
        return self.visitChildren(ctx)

    def visitConstant_declarator(self, ctx: CSharpParser.Constant_declaratorContext):
        return {
            "name": ctx.identifier().accept(self),
            "initial_value": ctx.expression().accept(self)
        }

    def visitVariable_declarators(self, ctx: CSharpParser.Variable_declaratorsContext):
        return self.visitChildren(ctx)

    def visitVariable_declarator(self, ctx: CSharpParser.Variable_declaratorContext):
        identifier = ctx.identifier().accept(self)

        local_variable_initializer = ctx.variable_initializer()
        if local_variable_initializer:
            return {
                "name": identifier,
                "initial_value": local_variable_initializer.accept(self)
            }

        return {
            "variable": identifier
        }

    def visitVariable_initializer(self, ctx: CSharpParser.Variable_initializerContext):
        return ctx.getChild(0).accept(self)

    def visitReturn_type(self, ctx: CSharpParser.Return_typeContext):
        if ctx.VOID():
            return ASTIdentifierNode(ctx.getText())

        return ctx.type_().accept(self)

    def visitMember_name(self, ctx: CSharpParser.Member_nameContext):
        return ctx.namespace_or_type_name().accept(self)

    def visitMethod_body(self, ctx: CSharpParser.Method_bodyContext):
        block = ctx.block()
        if block:
            return block.accept(self)

    def visitFormal_parameter_list(self, ctx: CSharpParser.Formal_parameter_listContext):
        return self.build_multi(self.visitChildren(ctx), ASTParametersNode)

    def visitFixed_parameters(self, ctx: CSharpParser.Fixed_parametersContext):
        return self.visitChildren(ctx)

    def visitFixed_parameter(self, ctx: CSharpParser.Fixed_parameterContext):
        if ctx.ARGLIST():
            return ASTIdentifierNode(ctx.getText())

        attributes = ctx.attributes()
        if attributes:
            attributes = attributes.accept(self)

        modifier = ctx.parameter_modifier()
        if modifier:
            modifier = modifier.accept(self)

        return ASTParameterNode(attributes=attributes, modifiers=modifier, **ctx.arg_declaration().accept(self))

    def visitParameter_modifier(self, ctx: CSharpParser.Parameter_modifierContext):
        return {
            "ref": ASTMiscModifier.REF,
            "out": ASTMiscModifier.OUT,
            "this": ASTMiscModifier.THIS
        }[ctx.getText()]

    def visitParameter_array(self, ctx: CSharpParser.Parameter_arrayContext):
        attributes = ctx.attributes()
        if attributes:
            return ASTPositionalArgumentsParameterNode(ctx.identifier().accept(self), ctx.array_type().accept(self),
                                                       attributes.accept(self))

        return ASTPositionalArgumentsParameterNode(ctx.identifier().accept(self), ctx.array_type().accept(self))

    def visitAccessor_declarations(self, ctx: CSharpParser.Accessor_declarationsContext):
        attributes = ctx.attributes()
        if attributes:
            attributes = attributes().accept(self)

        modifiers = ctx.accessor_modifier()
        if modifiers:
            modifiers = modifiers.accept(self)

        if ctx.GET():
            getter = ASTAccessorDefinitionNode(ASTIdentifierNode(ctx.GET().getText()), ctx.accessor_body().accept(self),
                                               attributes, modifiers)
            setter = ctx.set_accessor_declaration()
            if setter:
                setter = setter.accept(self)
                return ASTStatementsNode([getter, setter])

            return getter

        setter = ASTAccessorDefinitionNode(ASTIdentifierNode(ctx.SET().getText()), ctx.accessor_body().accept(self),
                                           attributes, modifiers)
        getter = ctx.set_accessor_declaration()
        if getter:
            getter = getter.accept(self)
            return ASTStatementsNode([setter, getter])

        return setter

    def visitGet_accessor_declaration(self, ctx: CSharpParser.Get_accessor_declarationContext):
        attributes = ctx.attributes()
        if attributes:
            attributes = attributes().accept(self)

        modifiers = ctx.accessor_modifier()
        if modifiers:
            modifiers = modifiers.accept(self)

        return ASTAccessorDefinitionNode(ASTIdentifierNode(ctx.GET().getText()), ctx.accessor_body().accept(self),
                                         attributes, modifiers)

    def visitSet_accessor_declaration(self, ctx: CSharpParser.Set_accessor_declarationContext):
        attributes = ctx.attributes()
        if attributes:
            attributes = attributes().accept(self)

        modifiers = ctx.accessor_modifier()
        if modifiers:
            modifiers = modifiers.accept(self)

        return ASTAccessorDefinitionNode(ASTIdentifierNode(ctx.SET().getText()), ctx.accessor_body().accept(self),
                                         attributes, modifiers)

    def visitAccessor_modifier(self, ctx: CSharpParser.Accessor_modifierContext):
        return {
            "protected": ASTVisibilityModifier.PROTECTED,
            "internal": ASTVisibilityModifier.INTERNAL,
            "private": ASTVisibilityModifier.PRIVATE,
            "protected internal": ASTVisibilityModifier.PROTECTED_INTERNAL,
            "private protected": ASTVisibilityModifier.PRIVATE_PROTECTED
        }[ctx.getText() if ctx.getChildCount() == 1 else ctx.getChild(0).getText() + " " + ctx.getChild(1).getText()]

    def visitAccessor_body(self, ctx: CSharpParser.Accessor_bodyContext):
        block = ctx.block()
        if block:
            return block.accept(self)

    def visitEvent_accessor_declarations(self, ctx: CSharpParser.Event_accessor_declarationsContext):
        attributes = ctx.attributes()
        if attributes:
            attributes = attributes().accept(self)

        if ctx.ADD():
            adder = ASTAccessorDefinitionNode(ASTIdentifierNode(ctx.ADD().getText()), ctx.block().accept(self),
                                              attributes)
            remover = ctx.remove_accessor_declaration()
            if remover:
                remover = remover.accept(self)
                return ASTStatementsNode([adder, remover])

            return adder

        remover = ASTAccessorDefinitionNode(ASTIdentifierNode(ctx.REMOVE().getText()), ctx.block().accept(self),
                                            attributes)
        adder = ctx.add_accessor_declaration()
        if adder:
            adder = adder.accept(self)
            return ASTStatementsNode([remover, adder])

        return remover

    def visitAdd_accessor_declaration(self, ctx: CSharpParser.Add_accessor_declarationContext):
        attributes = ctx.attributes()
        if attributes:
            attributes = attributes().accept(self)

        return ASTAccessorDefinitionNode(ASTIdentifierNode(ctx.ADD().getText()), ctx.block().accept(self), attributes)

    def visitRemove_accessor_declaration(self, ctx: CSharpParser.Remove_accessor_declarationContext):
        attributes = ctx.attributes()
        if attributes:
            attributes = attributes().accept(self)

        return ASTAccessorDefinitionNode(ASTIdentifierNode(ctx.REMOVE().getText()), ctx.block().accept(self),
                                         attributes)

    def visitOverloadable_operator(self, ctx: CSharpParser.Overloadable_operatorContext):
        return ASTIdentifierNode(ctx.getText())

    def visitConversion_operator_declarator(self, ctx: CSharpParser.Conversion_operator_declaratorContext):
        return ASTConversionOperatorDefinitionNode(ctx.type_().accept(self), {"implicit": ASTConversionType.IMPLICIT,
                                                                              "explicit": ASTConversionType.EXPLICIT}[
            ctx.getChild(0).getText()], ctx.arg_declaration().accept(self))

    def visitConstructor_initializer(self, ctx: CSharpParser.Constructor_initializerContext):
        arguments = ctx.argument_list()
        if arguments:
            return ASTCallNode(ASTIdentifierNode(ctx.getChild(1).getText()), arguments.accept(self))

        return ASTCallNode(ASTIdentifierNode(ctx.getChild(1).getText()))

    def visitBody(self, ctx: CSharpParser.BodyContext):
        block = ctx.block()
        if block:
            return block.accept(self)

    def visitStruct_interfaces(self, ctx: CSharpParser.Struct_interfacesContext):
        interface_type_list = ctx.interface_type_list()
        if interface_type_list:
            return interface_type_list.accept(self)

    def visitStruct_body(self, ctx: CSharpParser.Struct_bodyContext):
        return self.build_multi(self.visitChildren(ctx), ASTStatementsNode)

    def visitStruct_member_declaration(self, ctx: CSharpParser.Struct_member_declarationContext):
        attributes = ctx.attributes()
        if attributes:
            attributes = attributes.accept(self)

        modifiers = ctx.all_member_modifiers()
        if modifiers:
            modifiers = modifiers.accept(self)

        if ctx.FIXED():
            type_ = ctx.type_().accept(self)

            declarations = [declarator.accept(self) for declarator in ctx.fixed_size_buffer_declarator()]
            for declarators in declarations:
                declarators['type'] = type_
                declarators['attributes'] = attributes
                declarators.modifiers = modifiers

            return self.build_multi(declarations, ASTStatementsNode)

        declaration = ctx.common_member_declaration().accept(self)

        declaration['attributes'] = attributes
        declaration.modifiers.extend(modifiers)

        return declaration

    def visitArray_type(self, ctx: CSharpParser.Array_typeContext):
        return self.build_array_or_pointer_type(ctx.getChildren())

    def visitRank_specifier(self, ctx: CSharpParser.Rank_specifierContext):
        return ctx.getChildCount() - 1

    def visitArray_initializer(self, ctx: CSharpParser.Array_initializerContext):
        return self.build_multi(self.visitChildren(ctx), ASTExpressionsNode)

    def visitVariant_type_parameter_list(self, ctx: CSharpParser.Variant_type_parameter_listContext):
        return self.build_multi(self.visitChildren(ctx), ASTParametersNode)

    def visitVariant_type_parameter(self, ctx: CSharpParser.Variant_type_parameterContext):
        attributes = ctx.attributes()
        if attributes:
            attributes = attributes.accept(self)

        modifiers = ctx.variance_annotation()
        if modifiers:
            modifiers = [modifiers.accept(self)]

        return ASTParameterNode(ctx.identifier().accept(self), attributes=attributes, modifiers=modifiers)

    def visitVariance_annotation(self, ctx: CSharpParser.Variance_annotationContext):
        return {
            "in": ASTMiscModifier.IN,
            "out": ASTMiscModifier.OUT
        }[ctx.getText()]

    def visitInterface_base(self, ctx: CSharpParser.Interface_baseContext):
        return ctx.interface_type_list().accept(self)

    def visitInterface_body(self, ctx: CSharpParser.Interface_bodyContext):
        return self.build_multi(self.visitChildren(ctx), ASTStatementsNode)

    def visitInterface_member_declaration(self, ctx: CSharpParser.Interface_member_declarationContext):
        attributes = ctx.attributes()
        if attributes:
            attributes = attributes.accept(self)

        modifiers = []
        if ctx.NEW():
            modifiers.append(ASTMiscModifier.NEW)

        # Event definition
        if ctx.EVENT():
            return ASTEventDefinitionNode(ctx.identifier().accept(self), ctx.type_().accept(self),
                                          attributes=attributes, modifiers=modifiers)

        if ctx.UNSAFE():
            modifiers.append(ASTMiscModifier.UNSAFE)

        # Indexer definition
        if ctx.THIS():
            return ASTIndexerDefinitionNode(ASTIdentifierNode(ctx.THIS().getText()), ctx.type_().accept(self),
                                            ctx.formal_parameter_list().accept(self),
                                            ctx.interface_accessors().accept(self), attributes, modifiers)

        name = ctx.identifier().accept(self)

        # Property definition
        accessors = ctx.interface_accessors()
        if accessors:
            return ASTPropertyDefinitionNode(ctx.identifier().accept(self), accessors.accept(self),
                                             attributes=attributes, modifiers=modifiers)

        # Method definition
        if ctx.VOID():
            type_ = ASTIdentifierNode(ctx.VOID().getText())
        else:
            type_ = ctx.type_().accept(self)

        type_parameters = ctx.type_parameter_list()
        if type_parameters:
            name = ASTTypeNode(name, type_parameters.accept(self))

        parameters = ctx.formal_parameter_list()
        if parameters:
            parameters = parameters.accept(self)

        constraints = ctx.type_parameter_constraints_clauses()
        if constraints:
            constraints = constraints.accept(self)

        return ASTFunctionDefinitionNode(name, type_, parameters, constraints, attributes=attributes,
                                         modifiers=modifiers)

    def visitInterface_accessors(self, ctx: CSharpParser.Interface_accessorsContext):
        accessors = []
        children = ctx.getChildren(
            lambda child: self.filter_child(child, CSharpParser.AttributesContext, CSharpParser.GET, CSharpParser.SET))

        i = 0
        while i < len(children):
            if isinstance(children[i], CSharpParser.AttributesContext):
                accessors.append(
                    ASTAccessorDefinitionNode(children[i + 1].getText(), attributes=children[i].accept(self)))
                i += 1
            else:
                accessors.append(ASTAccessorDefinitionNode(children[i].getText()))

            i += 1

        return self.build_multi(accessors, ASTStatementsNode)

    def visitEnum_base(self, ctx: CSharpParser.Enum_baseContext):
        return ctx.type_().accept(self)

    def visitEnum_body(self, ctx: CSharpParser.Enum_bodyContext):
        return self.build_multi(self.visitChildren(ctx), ASTStatementsNode)

    def visitEnum_member_declaration(self, ctx: CSharpParser.Enum_member_declarationContext):
        name = ctx.identifier().accept(self)

        attributes = ctx.attributes()
        if attributes:
            attributes = attributes.accept(self)

        initial_value = ctx.expression()
        if initial_value:
            return ASTVariableDeclarationNode(name, initial_value=initial_value.accept(self), attributes=attributes)

        return ASTVariableDeclarationNode(name, attributes=attributes)

    def visitGlobal_attribute_section(self, ctx: CSharpParser.Global_attribute_sectionContext):
        return ASTAttributeSectionNode(ctx.global_attribute_target().accept(self), ctx.attribute_list().accept(self))

    def visitGlobal_attribute_target(self, ctx: CSharpParser.Global_attribute_targetContext):
        return ctx.getChild(0).accept(self)

    def visitAttributes(self, ctx: CSharpParser.AttributesContext):
        return self.build_multi(self.visitChildren(ctx), ASTAttributeSectionsNode)

    def visitAttribute_section(self, ctx: CSharpParser.Attribute_sectionContext):
        attributes = ctx.attribute_list().accept(self)

        target = ctx.attribute_target()
        if target:
            return ASTAttributeSectionNode(attributes, target)

        return ASTAttributeSectionNode(attributes)

    def visitAttribute_target(self, ctx: CSharpParser.Attribute_targetContext):
        return ctx.getChild(0).accept(self)

    def visitAttribute_list(self, ctx: CSharpParser.Attribute_listContext):
        return self.build_multi(self.visitChildren(ctx), ASTAttributesNode)

    def visitAttribute(self, ctx: CSharpParser.AttributeContext):
        return ASTAttributeNode(ctx.namespace_or_type_name().accept(self),
                                self.build_multi([argument.accept(self) for argument in ctx.attribute_argument()],
                                                 ASTArgumentsNode))

    def visitAttribute_argument(self, ctx: CSharpParser.Attribute_argumentContext):
        value = ctx.expression().accept(self)

        name = ctx.identifier()
        if name:
            return ASTKeywordArgumentNode(name.accept(self), value)

        return ASTArgumentNode(value)

    def visitPointer_type(self, ctx: CSharpParser.Pointer_typeContext):
        void = ctx.VOID()
        if void:
            return ASTPointerTypeNode(ASTIdentifierNode(void.getText()))

        return self.build_array_or_pointer_type(ctx.getChildren())

    def visitFixed_pointer_declarators(self, ctx: CSharpParser.Fixed_pointer_declaratorsContext):
        return self.build_multi(self.visitChildren(ctx), ASTStatementsNode)

    def visitFixed_pointer_declarator(self, ctx: CSharpParser.Fixed_pointer_declaratorContext):
        name = ctx.identifier().accept(self)

        initial_value = ctx.fixed_pointer_initializer()
        if initial_value:
            return {
                "name": name,
                "intial_value": initial_value.accept(self)
            }

        return {
            "name": name
        }

    def visitFixed_pointer_initializer(self, ctx: CSharpParser.Fixed_pointer_initializerContext):
        if ctx.AMP():
            return ASTUnaryOperationNode(ASTUnaryOperation.ADDRESS, ctx.expression().accept(self))

        return ctx.getChild(0).accept(self)

    def visitFixed_size_buffer_declarator(self, ctx: CSharpParser.Fixed_size_buffer_declaratorContext):
        return ASTFixedSizeBufferDefinitionNode(ctx.identifier().accept(self), size=ctx.expression().accept(self))

    def visitLocal_variable_initializer_unsafe(self, ctx: CSharpParser.Local_variable_initializer_unsafeContext):
        return ASTStackAllocationNode(ctx.type_().accept(self), ctx.expression().accept(self))

    def visitRight_arrow(self, ctx: CSharpParser.Right_arrowContext):
        return ctx.getText()

    def visitRight_shift(self, ctx: CSharpParser.Right_shiftContext):
        return ctx.getText()

    def visitRight_shift_assignment(self, ctx: CSharpParser.Right_shift_assignmentContext):
        return ctx.getText()

    def visitLiteral(self, ctx: CSharpParser.LiteralContext):
        literal = ctx.boolean_literal()
        if literal:
            return literal.accept(self)

        literal = ctx.string_literal()
        if literal:
            return literal.accept(self)

        if ctx.NULL():
            return ASTLiteralNode(ASTLiteralType.NULL)

        if ctx.CHARACTER_LITERAL():
            return ASTLiteralNode(ASTLiteralType.CHAR, ctx.getText())

        return ASTLiteralNode(ASTLiteralType.NUMBER, ctx.getText())

    def visitBoolean_literal(self, ctx: CSharpParser.Boolean_literalContext):
        return ASTLiteralNode(ASTLiteralType.BOOLEAN, ctx.getText())

    def visitString_literal(self, ctx: CSharpParser.String_literalContext):
        return ASTLiteralNode(ASTLiteralType.STRING, ctx.getText())

    def visitInterpolated_regular_string(self, ctx: CSharpParser.Interpolated_regular_stringContext):
        return ctx.getText()

    def visitInterpolated_verbatium_string(self, ctx: CSharpParser.Interpolated_verbatium_stringContext):
        return ctx.getText()

    def visitInterpolated_regular_string_part(self, ctx: CSharpParser.Interpolated_regular_string_partContext):
        return ctx.getText()

    def visitInterpolated_verbatium_string_part(self, ctx: CSharpParser.Interpolated_verbatium_string_partContext):
        return ctx.getText()

    def visitInterpolated_string_expression(self, ctx: CSharpParser.Interpolated_string_expressionContext):
        return ctx.getText()

    def visitKeyword(self, ctx: CSharpParser.KeywordContext):
        return ASTIdentifierNode(ctx.getText())

    def visitClass_definition(self, ctx: CSharpParser.Class_definitionContext):
        name = ctx.identifier().accept(self)
        type_parameters = ctx.type_parameter_list()
        if type_parameters:
            name = ASTTypeNode(name, type_parameters)

        bases = ctx.class_base()
        if bases:
            bases = bases.accept(self)

        constraints = ctx.type_parameter_constraints_clauses()
        if constraints:
            constraints = constraints.accept(self)

        body = ctx.class_body().accept(self)

        return ASTClassDefinitionNode(name, body, bases, constraints)

    def visitStruct_definition(self, ctx: CSharpParser.Struct_definitionContext):
        name = ctx.identifier().accept(self)
        type_parameters = ctx.type_parameter_list()
        if type_parameters:
            name = ASTTypeNode(name, type_parameters)

        interfaces = ctx.struct_interfaces()
        if interfaces:
            interfaces = interfaces.accept(self)

        constraints = ctx.type_parameter_constraints_clauses()
        if constraints:
            constraints = constraints.accept(self)

        body = ctx.struct_body().accept(self)

        return ASTStructDefinitionNode(name, interfaces, constraints, body)

    def visitInterface_definition(self, ctx: CSharpParser.Interface_definitionContext):
        name = ctx.identifier().accept(self)
        type_parameters = ctx.variant_type_parameter_list()
        if type_parameters:
            name = ASTTypeNode(name, type_parameters)

        bases = ctx.interface_base()
        if bases:
            bases = bases.accept(self)

        constraints = ctx.type_parameter_constraints_clauses()
        if constraints:
            constraints = constraints.accept(self)

        body = ctx.interface_body().accept(self)

        return ASTInterfaceDefinitionNode(name, bases, constraints, body)

    def visitEnum_definition(self, ctx: CSharpParser.Enum_definitionContext):
        name = ctx.identifier().accept(self)

        underlying_type = ctx.enum_base()
        if underlying_type:
            underlying_type = underlying_type.accept(self)

        body = ctx.enum_body().accept(self)

        return ASTEnumDefinitionNode(name, underlying_type, body)

    def visitDelegate_definition(self, ctx: CSharpParser.Delegate_definitionContext):
        return_type = ctx.return_type().accept(self)

        name = ctx.identifier().accept(self)
        type_parameters = ctx.variant_type_parameter_list()
        if type_parameters:
            name = ASTTypeNode(name, type_parameters)

        parameters = ctx.formal_parameter_list()
        if parameters:
            parameters = parameters.accept(self)

        constraints = ctx.type_parameter_constraints_clauses()
        if constraints:
            constraints = constraints.accept(self)

        return ASTDelegateDefinitionNode(name, return_type, constraints, parameters)

    def visitEvent_declaration(self, ctx: CSharpParser.Event_declarationContext):
        type_ = ctx.type_().accept(self)

        variable_declarations = ctx.variable_declarators()
        if variable_declarations:
            variable_declarations = variable_declarations.accept(self)
            events = []
            if isinstance(variable_declarations, ASTMultiplesNode):
                for variable in variable_declarations.values():
                    events.append(ASTEventDefinitionNode(variable, type_))
            elif isinstance(variable_declarations, ASTNode):
                events.append(ASTEventDefinitionNode(variable_declarations, type_))
            return self.build_multi(events, ASTStatementsNode)

        return ASTEventDefinitionNode(ctx.member_name().accept(self), type_,
                                      ctx.event_accessor_declarations().accept(self))

    def visitField_declaration(self, ctx: CSharpParser.Field_declarationContext):
        return ctx.getChild(0).accept(self)

    def visitProperty_declaration(self, ctx: CSharpParser.Property_declarationContext):
        name = ctx.member_name().accept(self)
        body = ctx.accessor_declarations()
        if body:
            body = body.accept(self)

            initial_value = ctx.variable_initializer()
            if initial_value:
                initial_value = initial_value.accept(self)

            return ASTPropertyDefinitionNode(name, body=body, initial_value=initial_value)

        return ASTPropertyDefinitionNode(name, body=(ctx.expression().accept(self)))

    def visitConstant_declaration(self, ctx: CSharpParser.Constant_declarationContext):
        type_ = ctx.type_().accept(self)

        return self.build_multi([ASTConstantDeclarationNode(type_=type_, **(declarator.accept(self))) for declarator in
                                 ctx.constant_declarators().accept(self)], ASTConstantDeclarationsNode)

    def visitIndexer_declaration(self, ctx: CSharpParser.Indexer_declarationContext):
        name = ASTIdentifierNode(ctx.THIS().getText())

        parameters = ctx.formal_parameter_list().accept(self)

        body = ctx.accessor_declarations()
        if body:
            return ASTIndexerDefinitionNode(name, parameters=parameters, body=body.accept(self))

        return ASTIndexerDefinitionNode(name, parameters=parameters, body=ctx.expression().accept(self))

    def visitDestructor_definition(self, ctx: CSharpParser.Destructor_definitionContext):
        return ASTDestructorDefinitionNode(ctx.identifier().accept(self), ctx.body().accept(self))

    def visitConstructor_declaration(self, ctx: CSharpParser.Constructor_declarationContext):
        name = ctx.identifier().accept(self)

        parameters = ctx.formal_parameter_list()
        if parameters:
            parameters = parameters.accept(self)

        initializer = ctx.constructor_initializer()
        if initializer:
            initializer = initializer.accept(self)

        body = ctx.body().accept(self)

        return ASTConstructorDefinitionNode(name, parameters, initializer, body)

    def visitMethod_declaration(self, ctx: CSharpParser.Method_declarationContext):
        name = ctx.method_member_name().accept(self)
        type_parameters = ctx.type_parameter_list()
        if type_parameters:
            name = ASTTypeNode(name, type_parameters)

        parameters = ctx.formal_parameter_list()
        if parameters:
            parameters = parameters.accept(self)

        constraints = ctx.type_parameter_constraints_clauses()
        if constraints:
            constraints = constraints.accept(self)

        body = ctx.method_body()
        if body:
            return ASTFunctionDefinitionNode(name, parameters=parameters, constraints_clauses=constraints,
                                             body=body.accept(self))

        return ASTFunctionDefinitionNode(name, parameters=parameters, constraints_clauses=constraints,
                                         body=ctx.expression().accept(self))

    def visitMethod_member_name(self, ctx: CSharpParser.Method_member_nameContext):
        children = ctx.getChildren(lambda child: self.filter_child(child, CSharpParser.IdentifierContext,
                                                                   CSharpParser.Type_argument_listContext))

        members = []

        i = 0
        while i < len(children):
            if i + 1 < len(children) and isinstance(children[i + 1], CSharpParser.Type_argument_listContext):
                members.append(ASTTypeNode(children[i].accept(self), children[i + 1].accept(self)))
                i += 2
            else:
                members.append(children[i].accept(self))
                i += 1

        return self.build_left_associated(members, ASTMemberNode)

    def visitOperator_declaration(self, ctx: CSharpParser.Operator_declarationContext):
        operator = ctx.overloadable_operator().accept(self)

        parameters = self.build_multi([parameter.accept(self) for parameter in ctx.arg_declaration()],
                                      ASTParametersNode)

        body = ctx.body()
        if body:
            body = body.accept(self)
        else:
            body = ctx.expression().accept(self)

        return ASTOperatorOverloadDefinitionNode(operator, parameters=parameters, body=body)

    def visitArg_declaration(self, ctx: CSharpParser.Arg_declarationContext):
        name = ctx.identifier().accept(self)
        type_ = ctx.type_().accept(self)

        default = ctx.expression()
        if default:
            return {
                "name": name,
                "type_": type_,
                "default": default
            }

        return {
            "name": name,
            "type_": type_
        }

    def visitMethod_invocation(self, ctx: CSharpParser.Method_invocationContext):
        argument_list = ctx.argument_list()
        if argument_list:
            return argument_list.accept(self)

    def visitObject_creation_expression(self, ctx: CSharpParser.Object_creation_expressionContext):
        arguments = ctx.argument_list()
        if arguments:
            arguments = arguments.accept(self)

        initializer = ctx.object_or_collection_initializer()
        if initializer:
            initializer = initializer.accept(self)

        return ASTObjectCreationNode(arguments=arguments, initializer=initializer)

    def visitIdentifier(self, ctx: CSharpParser.IdentifierContext):
        return ASTIdentifierNode(ctx.getText())

    # endregion
