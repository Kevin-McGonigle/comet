from typing import Type

from antlr4.tree.Tree import TerminalNodeImpl, ParserRuleContext

from metrics.parsers.python3.base.Python3Parser import Python3Parser
from metrics.parsers.python3.base.Python3Visitor import Python3Visitor
from metrics.structures.ast import *


class ASTGenerationVisitor(Python3Visitor):
    # region Behaviour
    def visit(self, tree):
        return AST(super().visit(tree))

    def visitChildren(self, node):
        result = []
        for i in range(node.getChildCount()):
            if not self.shouldVisitNextChild(node, result):
                return result

            result = self.aggregateResult(result, node.getChild(i).accept(self))

        return result

    def visitTerminal(self, node):
        return super().visitTerminal(node)

    def visitErrorNode(self, node):
        return super().visitErrorNode(node)

    def defaultResult(self):
        return super().defaultResult()

    def aggregateResult(self, aggregate, next_result):
        return aggregate + [next_result] if next_result is not None else aggregate

    def shouldVisitNextChild(self, node, current_result):
        return super().shouldVisitNextChild(node, current_result)

    # endregion

    # region Helpers

    def build_multi(self, sequence: Optional[Sequence[ASTNode]], multi_node: Type[ASTMultiplesNode]):
        if not sequence:
            return self.defaultResult()

        if len(sequence) == 1:
            return sequence[0]

        return multi_node(sequence)

    def build_right_associated(self, sequence: Optional[Sequence[ASTNode]], parent_node: Type[ASTNode]):
        if not sequence:
            return self.defaultResult()

        if len(sequence) == 1:
            return sequence[0]

        return parent_node(sequence[0], self.build_right_associated(sequence[1:], parent_node))

    def build_left_associated(self, sequence: Optional[Sequence[ASTNode]], parent_node: Type[ASTNode]):
        if not sequence:
            return self.defaultResult()

        if len(sequence) == 1:
            return sequence[0]

        return parent_node(self.build_right_associated(sequence[:-1], parent_node), sequence[-1])

    def build_if_else(self, children):
        if isinstance(children[0], TerminalNodeImpl) and (
                children[0].symbol.type == Python3Parser.IF or children[0].symbol.type == Python3Parser.ELIF):
            if len(children) == 3:
                return ASTIfStatementNode(children[1].accept(self), children[2].accept(self))
            return ASTIfElseStatementNode(children[1].accept(self), children[2].accept(self),
                                          self.build_if_else(children[3:]))

        return children[-1].accept(self)

    def build_bin_op(self, operation, expressions):
        if len(expressions) == 1:
            return expressions[0]
        return ASTBinaryOperationNode(operation, self.build_bin_op(operation, expressions[:-1]), expressions[-1])

    def build_bin_op_choice(self, children):
        if len(children) == 1:
            return children[0]

        operator = children[-2]
        if isinstance(operator, list):
            return ASTUnaryOperationNode(operator[0],
                                         ASTBinaryOperationNode(operator[1],
                                                                self.build_bin_op_choice(children[:-2]),
                                                                children[-1]))

        return ASTBinaryOperationNode(operator, self.build_bin_op_choice(children[:-2]), children[-1])

    def build_bin_op_rassoc(self, operation, expressions):
        if len(expressions) == 1:
            return expressions[0]
        return ASTBinaryOperationNode(operation, expressions[0],
                                      self.build_bin_op_rassoc(operation, expressions[1:]))

    def build_atom_expr(self, children):
        if len(children) == 1:
            return children[0].accept(self)

        if isinstance(children[-1], Python3Parser.SubscriptlistContext):
            return ASTAccessNode(self.build_atom_expr(children[:-1]), children[-1].accept(self))

        if isinstance(children[-1], Python3Parser.ArglistContext):
            return ASTCallNode(self.build_atom_expr(children[:-1]), children[-1].accept(self))

        return ASTMemberNode(self.build_atom_expr(children[:-1]), ASTIdentifierNode(children[-1].getText()))

    @staticmethod
    def filter_child(child, *contexts):
        for context in contexts:
            if isinstance(context, int) and isinstance(child, TerminalNodeImpl) and child.symbol.type == context:
                return True
            elif isinstance(context, ParserRuleContext) and isinstance(child, context):
                return True

        return False

    @staticmethod
    def get_visibility(name: str) -> ASTVisibilityModifier:
        """
        Get the corresponding visibility modifier for the member's name; with one leading underscore indicating a
        protected member and two indicating a private member
        (according to the PEP 8 style guide
        https://www.python.org/dev/peps/pep-0008/#method-names-and-instance-variables).

        :param name: The member's name/identifier.
        :return: The corresponding visibility/access modifier.
        """
        if name.startswith("__"):
            return ASTVisibilityModifier.PRIVATE

        if name.startswith("_"):
            return ASTVisibilityModifier.PROTECTED

        return ASTVisibilityModifier.PUBLIC

    # endregion

    # region Visits
    def visitSingle_input(self, ctx: Python3Parser.Single_inputContext):
        statement = ctx.simple_stmt()
        if not statement:
            statement = ctx.compound_stmt()

        if statement:
            return statement.accept(self)

        return self.defaultResult()

    def visitFile_input(self, ctx: Python3Parser.File_inputContext):
        return self.build_multi(self.visitChildren(ctx), ASTStatementsNode)

    def visitEval_input(self, ctx: Python3Parser.Eval_inputContext):
        return ctx.testlist().accept(self)

    def visitDecorator(self, ctx: Python3Parser.DecoratorContext):
        arguments = ctx.arglist()
        if arguments:
            return ASTDecoratorNode(ctx.dotted_name().accept(self), arguments.accept(self))

        return ASTDecoratorNode(ctx.dotted_name().accept(self))

    def visitDecorators(self, ctx: Python3Parser.DecoratorsContext):
        return self.build_multi(self.visitChildren(ctx), ASTDecoratorsNode)

    def visitDecorated(self, ctx: Python3Parser.DecoratedContext):
        return ASTDecoratedNode(*self.visitChildren(ctx))

    def visitAsync_funcdef(self, ctx: Python3Parser.Async_funcdefContext):
        return ASTAsyncNode(*self.visitChildren(ctx))

    def visitFuncdef(self, ctx: Python3Parser.FuncdefContext):
        name = ASTIdentifierNode(ctx.NAME().getText())
        parameters = ctx.parameters().accept(self)
        return_type = ctx.test()
        body = ctx.suite().accept(self)
        visibility = self.get_visibility(name.name)

        if return_type:
            return ASTFunctionDefinitionNode(name, parameters, return_type.accept(self), body, [visibility])

        return ASTFunctionDefinitionNode(name, parameters, body=body, modifiers=[visibility])

    def visitParameters(self, ctx: Python3Parser.ParametersContext):
        parameters = ctx.typedargslist()
        if parameters:
            return parameters.accept(self)

        return self.defaultResult()

    def visitTypedargslist(self, ctx: Python3Parser.TypedargslistContext):
        parameters = []

        children = ctx.getChildren()
        child_count = ctx.getChildCount()

        i = 0
        while i < child_count:
            child = children[i]
            if isinstance(child, TerminalNodeImpl):
                if child.symbol.type == Python3Parser.STAR:
                    if i + 1 < child_count and isinstance(children[i + 1], Python3Parser.TfpdefContext):
                        parameters.append(ASTPositionalArgumentsParameterNode(**children[i + 1].accept(self)))
                        i += 1
                    else:
                        parameters.append("*")
                elif child.symbol.type == Python3Parser.POWER:
                    parameters.append(ASTKeywordArgumentsParameterNode(**children[i + 1].accept(self)))
                    i += 1
            else:
                if isinstance(child, Python3Parser.TfpdefContext):
                    if i + 2 < child_count and isinstance(children[i + 2], Python3Parser.TestContext):
                        parameters.append(ASTParameterNode(**child.accept(self), default=children[i + 2].accept(self)))
                        i += 2
                    else:
                        parameters.append(ASTParameterNode(**child.accept(self)))
            i += 1

        return self.build_multi(parameters, ASTParametersNode)

    def visitTfpdef(self, ctx: Python3Parser.TfpdefContext):
        name = ASTIdentifierNode(ctx.NAME().getText())
        return_type = ctx.test()

        if return_type:
            return {"name": name, "type_": return_type.accept(self)}

        return {"name": name}

    def visitVarargslist(self, ctx: Python3Parser.VarargslistContext):
        parameters = []

        children = ctx.getChildren()
        child_count = ctx.getChildCount()

        i = 0
        while i < child_count:
            child = children[i]
            if isinstance(child, TerminalNodeImpl):
                if child.symbol.type == Python3Parser.STAR:
                    if i + 1 < child_count and isinstance(children[i + 1], Python3Parser.VfpdefContext):
                        parameters.append(ASTPositionalArgumentsParameterNode(**children[i + 1].accept(self)))
                        i += 1
                    else:
                        parameters.append("*")
                elif child.symbol.type == Python3Parser.POWER:
                    parameters.append(ASTKeywordArgumentsParameterNode(**children[i + 1].accept(self)))
                    i += 1
            else:
                if isinstance(child, Python3Parser.VfpdefContext):
                    if i + 2 < child_count and isinstance(children[i + 2], Python3Parser.TestContext):
                        parameters.append(ASTParameterNode(**child.accept(self), default=children[i + 2].accept(self)))
                        i += 2
                    else:
                        parameters.append(ASTParameterNode(**child.accept(self)))
            i += 1

        return self.build_multi(parameters, ASTParametersNode)

    def visitVfpdef(self, ctx: Python3Parser.VfpdefContext):
        return {"name": ASTIdentifierNode(ctx.NAME().getText())}

    def visitStmt(self, ctx: Python3Parser.StmtContext):
        return ctx.getChild(0).accept(self)

    def visitSimple_stmt(self, ctx: Python3Parser.Simple_stmtContext):
        return self.build_multi(self.visitChildren(ctx), ASTStatementsNode)

    def visitSmall_stmt(self, ctx: Python3Parser.Small_stmtContext):
        return ctx.getChild(0).accept(self)

    def visitExpr_stmt(self, ctx: Python3Parser.Expr_stmtContext):
        variables = ctx.testlist_star_expr(0).accept(self)
        if isinstance(variables, ASTMultiplesNode):
            variables = ASTVariablesNode(variables.children)

        annotation_assignment = ctx.annassign()
        if annotation_assignment:
            return ASTAnnotatedAssignmentStatementNode(**annotation_assignment.accept(self),
                                                       variables=variables)

        augmented_assignment = ctx.augassign()
        if augmented_assignment:
            return ASTAugmentedAssignmentStatementNode(augmented_assignment.accept(self), variables,
                                                       ctx.getChild(2).accept(self))

        if ctx.ASSIGN():
            values = self.build_left_associated([child.accept(self) for child in ctx.getChildren(
                lambda child: self.filter_child(child, Python3Parser.Testlist_star_exprContext,
                                                Python3Parser.Yield_exprContext))[1:]], ASTAssignmentStatementNode)
            return ASTAssignmentStatementNode(variables, values)

        return ASTExpressionsNode(variables.children) if isinstance(variables, ASTMultiplesNode) else variables

    def visitAnnassign(self, ctx: Python3Parser.AnnassignContext):
        annotation = ctx.test(0).accept(self)
        values = ctx.test(1)

        if values:
            return {
                "annotation": annotation,
                "values": values.accept(self)
            }

        return {"annotation": annotation}

    def visitTestlist_star_expr(self, ctx: Python3Parser.Testlist_star_exprContext):
        return self.build_multi(self.visitChildren(ctx), ASTExpressionsNode)

    def visitAugassign(self, ctx: Python3Parser.AugassignContext):
        return {
            "+=": ASTInPlaceOperation.ADD,
            "-=": ASTInPlaceOperation.SUBTRACT,
            "*=": ASTInPlaceOperation.MULTIPLY,
            "/=": ASTInPlaceOperation.DIVIDE,
            "//=": ASTInPlaceOperation.FLOOR_DIVIDE,
            "%=": ASTInPlaceOperation.MODULO,
            "**=": ASTInPlaceOperation.POWER,
            "&=": ASTInPlaceOperation.BITWISE_AND,
            "|=": ASTInPlaceOperation.BITWISE_OR,
            "^=": ASTInPlaceOperation.BITWISE_XOR,
            "<<=": ASTInPlaceOperation.LEFT_SHIFT,
            ">>=": ASTInPlaceOperation.RIGHT_SHIFT,
            "@=": ASTInPlaceOperation.MATRIX_MULTIPLY,
        }[ctx.getText()]

    def visitDel_stmt(self, ctx: Python3Parser.Del_stmtContext):
        return ASTDelStatementNode(ctx.exprlist().accept(self))

    def visitPass_stmt(self, ctx: Python3Parser.Pass_stmtContext):
        return ASTPassStatementNode()

    def visitFlow_stmt(self, ctx: Python3Parser.Flow_stmtContext):
        return ctx.getChild(0).accept(self)

    def visitBreak_stmt(self, ctx: Python3Parser.Break_stmtContext):
        return ASTBreakStatementNode()

    def visitContinue_stmt(self, ctx: Python3Parser.Continue_stmtContext):
        return ASTContinueStatementNode()

    def visitReturn_stmt(self, ctx: Python3Parser.Return_stmtContext):
        testlist = ctx.testlist()
        if testlist:
            return ASTReturnStatementNode(testlist.accept(self))

        return ASTReturnStatementNode()

    def visitYield_stmt(self, ctx: Python3Parser.Yield_stmtContext):
        yield_expression = ctx.yield_expr().accept(self)
        return ASTYieldStatementNode(yield_expression.values)

    def visitRaise_stmt(self, ctx: Python3Parser.Raise_stmtContext):
        exception = ctx.test(0)
        from_ = ctx.test(1)

        if from_:
            return ASTThrowStatementNode(ASTFromNode(exception.accept(self), from_.accept(self)))

        if exception:
            return ASTThrowStatementNode(exception.accept(self))

        return ASTThrowStatementNode()

    def visitImport_stmt(self, ctx: Python3Parser.Import_stmtContext):
        return ctx.getChild(0).accept(self)

    def visitImport_name(self, ctx: Python3Parser.Import_nameContext):
        return ASTImportStatementNode(ctx.dotted_as_names().accept(self))

    def visitImport_from(self, ctx: Python3Parser.Import_fromContext):
        leading_dots = "".join([dot.getText() for dot in ctx.DOT() + ctx.ELLIPSIS()])

        dotted_name = ctx.dotted_name()
        if dotted_name:
            dotted_name = dotted_name.accept(self)
            if leading_dots:
                from_ = ASTMemberNode(ASTIdentifierNode(leading_dots), dotted_name)
            else:
                from_ = dotted_name
        else:
            from_ = ASTIdentifierNode(leading_dots)

        import_ = ctx.import_as_names()
        if not import_:
            import_ = "*"

        return ASTImportStatementNode(ASTFromNode(from_, import_))

    def visitImport_as_name(self, ctx: Python3Parser.Import_as_nameContext):
        name = ASTIdentifierNode(ctx.NAME(0).getText())
        alias = ctx.NAME(1)

        if alias:
            return ASTAliasNode(name, ASTIdentifierNode(alias.getText()))

        return name

    def visitDotted_as_name(self, ctx: Python3Parser.Dotted_as_nameContext):
        name = ctx.dotted_name().accept(self)
        alias = ctx.NAME()

        if alias:
            return ASTAliasNode(name, ASTIdentifierNode(alias.getText()))

        return name

    def visitImport_as_names(self, ctx: Python3Parser.Import_as_namesContext):
        return self.build_multi(self.visitChildren(ctx), ASTExpressionsNode)

    def visitDotted_as_names(self, ctx: Python3Parser.Dotted_as_namesContext):
        return self.build_multi(self.visitChildren(ctx), ASTExpressionsNode)

    def visitDotted_name(self, ctx: Python3Parser.Dotted_nameContext):
        names = [ASTIdentifierNode(name.getText()) for name in ctx.NAME()]
        return self.build_right_associated(names, ASTMemberNode)

    def visitGlobal_stmt(self, ctx: Python3Parser.Global_stmtContext):
        return ASTGlobalStatementNode(
            self.build_multi([ASTIdentifierNode(name.getText()) for name in ctx.NAME()], ASTExpressionsNode))

    def visitNonlocal_stmt(self, ctx: Python3Parser.Nonlocal_stmtContext):
        return ASTNonLocalStatementNode(
            self.build_multi([ASTIdentifierNode(name.getText()) for name in ctx.NAME()], ASTExpressionsNode))

    def visitAssert_stmt(self, ctx: Python3Parser.Assert_stmtContext):
        condition = ctx.test(0).accept(self)
        message = ctx.test(1)

        if message:
            return ASTAssertStatementNode(condition, message.accept(self))

        return ASTAssertStatementNode(condition)

    def visitCompound_stmt(self, ctx: Python3Parser.Compound_stmtContext):
        return ctx.getChild(0).accept(self)

    def visitAsync_stmt(self, ctx: Python3Parser.Async_stmtContext):
        return ASTAsyncNode(ctx.getChild(1).accept(self))

    def visitIf_stmt(self, ctx: Python3Parser.If_stmtContext):
        return self.build_if_else(ctx.getChildren(
            lambda child: self.filter_child(child, Python3Parser.IF, Python3Parser.ELIF, Python3Parser.ELSE,
                                            Python3Parser.TestContext, Python3Parser.SuiteContext)))

    def visitWhile_stmt(self, ctx: Python3Parser.While_stmtContext):
        condition = ctx.test().accept(self)
        body = ctx.suite(0).accept(self)
        else_body = ctx.suite(1)

        if else_body:
            return ASTLoopElseStatementNode(condition, body, else_body.accept(self))

        return ASTLoopStatementNode(condition, body)

    def visitFor_stmt(self, ctx: Python3Parser.For_stmtContext):
        exprlist = ctx.exprlist().accept(self)
        testlist = ctx.testlist().accept(self)
        body = ctx.suite(0).accept(self)
        else_body = ctx.suite(1)

        if else_body:
            return ASTLoopElseStatementNode(ASTBinaryOperationNode(ASTComparisonOperation.IN, exprlist, testlist), body,
                                            else_body.accept(self))

        return ASTLoopStatementNode(ASTBinaryOperationNode(ASTComparisonOperation.IN, exprlist, testlist), body)

    def visitTry_stmt(self, ctx: Python3Parser.Try_stmtContext):
        body = None
        catches = []
        else_body = None
        finally_body = None

        children = ctx.getChildren(
            lambda child: self.filter_child(child, Python3Parser.TRY, Python3Parser.Except_clauseContext,
                                            Python3Parser.SuiteContext, Python3Parser.ELSE, Python3Parser.FINALLY))
        i = 0
        while i < len(children):
            if isinstance(children[i], TerminalNodeImpl):
                if children[i].symbol.type == Python3Parser.TRY:
                    body = children[i + 1].accept(self)
                elif children[i].symbol.type == Python3Parser.ELSE:
                    else_body = children[i + 1].accept(self)
                else:
                    finally_body = children[i + 1].accept(self)
            else:
                catches.append(ASTCatchNode(children[i].accept(self), children[i + 1].accept(self)))

        return ASTTryStatementNode(body, self.build_multi(catches, ASTCatchesNode), else_body, finally_body)

    def visitWith_stmt(self, ctx: Python3Parser.With_stmtContext):
        return ASTWithStatementNode(
            self.build_multi([item.accept(self) for item in (ctx.with_item())], ASTExpressionsNode),
            ctx.suite().accept(self))

    def visitWith_item(self, ctx: Python3Parser.With_itemContext):
        expression = ctx.test().accept(self)
        alias = ctx.expr()

        if alias:
            return ASTAliasNode(expression, alias.accept(self))

        return expression

    def visitExcept_clause(self, ctx: Python3Parser.Except_clauseContext):
        expression = ctx.test()
        alias = ctx.NAME()

        if alias:
            return ASTAliasNode(expression.accept(self), ASTIdentifierNode(alias.getText()))

        if expression:
            return expression.accept(self)

        return None

    def visitSuite(self, ctx: Python3Parser.SuiteContext):
        simple_stmt = ctx.simple_stmt()

        if simple_stmt:
            return simple_stmt.accept(self)

        return self.build_multi(self.visitChildren(ctx), ASTStatementsNode)

    def visitTest(self, ctx: Python3Parser.TestContext):
        condition = ctx.or_test(1)

        if condition:
            return ASTIfElseStatementNode(condition.accept(self), ctx.getChild(0).accept(self), ctx.test().accept(self))

        return ctx.getChild(0).accept(self)

    def visitTest_nocond(self, ctx: Python3Parser.Test_nocondContext):
        return ctx.getChild(0).accept(self)

    def visitLambdef(self, ctx: Python3Parser.LambdefContext):
        parameters = ctx.varargslist()
        body = ctx.test().accept(self)

        if parameters:
            return ASTAnonymousFunctionDefinitionNode(body, parameters.accept(self))

        return ASTAnonymousFunctionDefinitionNode(body)

    def visitLambdef_nocond(self, ctx: Python3Parser.Lambdef_nocondContext):
        parameters = ctx.varargslist()
        body = ctx.test_nocond().accept(self)

        if parameters:
            return ASTAnonymousFunctionDefinitionNode(body, parameters.accept(self))

        return ASTAnonymousFunctionDefinitionNode(body)

    def visitOr_test(self, ctx: Python3Parser.Or_testContext):
        self.build_bin_op(ASTLogicalOperation.OR, self.visitChildren(ctx))

    def visitAnd_test(self, ctx: Python3Parser.And_testContext):
        self.build_bin_op(ASTLogicalOperation.AND, self.visitChildren(ctx))

    def visitNot_test(self, ctx: Python3Parser.Not_testContext):
        return ASTUnaryOperationNode(ASTLogicalOperation.NOT, ctx.getChild(1).accept(self))

    def visitComparison(self, ctx: Python3Parser.ComparisonContext):
        self.build_bin_op_choice(self.visitChildren(ctx))

    def visitComp_op(self, ctx: Python3Parser.Comp_opContext):
        return {
            "==": ASTComparisonOperation.EQUAL,
            "!=": ASTComparisonOperation.NOT_EQUAL,
            "<>": ASTComparisonOperation.NOT_EQUAL,
            "<": ASTComparisonOperation.LESS_THAN,
            ">": ASTComparisonOperation.GREATER_THAN,
            "<=": ASTComparisonOperation.LESS_THAN_OR_EQUAL,
            ">=": ASTComparisonOperation.GREATER_THAN_OR_EQUAL,
            "in": ASTComparisonOperation.IN,
            "not in": [ASTLogicalOperation.NOT, ASTComparisonOperation.IN],
            "is": ASTComparisonOperation.IS,
            "is not": [ASTLogicalOperation.NOT, ASTComparisonOperation.IS]
        }[ctx.getText()]

    def visitStar_expr(self, ctx: Python3Parser.Star_exprContext):
        return ASTPositionalUnpackExpressionNode(ctx.expr().accept(self))

    def visitExpr(self, ctx: Python3Parser.ExprContext):
        return self.build_bin_op(ASTBitwiseOperation.OR, self.visitChildren(ctx))

    def visitXor_expr(self, ctx: Python3Parser.Xor_exprContext):
        return self.build_bin_op(ASTBitwiseOperation.XOR, self.visitChildren(ctx))

    def visitAnd_expr(self, ctx: Python3Parser.And_exprContext):
        return self.build_bin_op(ASTBitwiseOperation.AND, self.visitChildren(ctx))

    def visitShift_expr(self, ctx: Python3Parser.Shift_exprContext):
        operators = {
            "<<": ASTBitwiseOperation.LEFT_SHIFT,
            ">>": ASTBitwiseOperation.RIGHT_SHIFT
        }

        return self.build_bin_op_choice(
            [child.accept(self) if isinstance(child, Python3Parser.Arith_exprContext) else operators[child.getText()]
             for child in ctx.getChildren()])

    def visitArith_expr(self, ctx: Python3Parser.Arith_exprContext):
        operators = {
            "+": ASTArithmeticOperation.ADD,
            "-": ASTArithmeticOperation.SUBTRACT
        }

        return self.build_bin_op_choice(
            [child.accept(self) if isinstance(child, Python3Parser.Arith_exprContext) else operators[child.getText()]
             for child in ctx.getChildren()])

    def visitTerm(self, ctx: Python3Parser.TermContext):
        operators = {
            "*": ASTArithmeticOperation.MULTIPLY,
            "@": ASTArithmeticOperation.MATRIX_MULTIPLY,
            "/": ASTArithmeticOperation.DIVIDE,
            "%": ASTArithmeticOperation.MODULO,
            "//": ASTArithmeticOperation.FLOOR_DIVIDE
        }

        return self.build_bin_op_choice(
            [child.accept(self) if isinstance(child, Python3Parser.Arith_exprContext) else operators[child.getText()]
             for child in ctx.getChildren()])

    def visitFactor(self, ctx: Python3Parser.FactorContext):
        power = ctx.power()
        if power:
            return power.accept(self)

        operators = {
            "+": ASTArithmeticOperation.POSITIVE,
            "-": ASTArithmeticOperation.NEGATION,
            "~": ASTBitwiseOperation.INVERSION
        }

        return ASTUnaryOperationNode(operators[ctx.getChild(0).getText()], ctx.factor().accept(self))

    def visitPower(self, ctx: Python3Parser.PowerContext):
        return self.build_bin_op_rassoc(ASTArithmeticOperation.POWER, self.visitChildren(ctx))

    def visitAtom_expr(self, ctx: Python3Parser.Atom_exprContext):
        await_ = ctx.AWAIT()

        if await_:
            return ASTAwaitNode(self.build_atom_expr(self.visitChildren(ctx)))

        return self.build_atom_expr(self.visitChildren(ctx))

    def visitAtom(self, ctx: Python3Parser.AtomContext):
        testlist_comp = ctx.testlist_comp()
        if testlist_comp:
            testlist_comp = testlist_comp.accept(self)
            if ctx.OPEN_PAREN():
                if isinstance(testlist_comp, ASTComprehensionNode):
                    return ASTGeneratorExpressionNode(testlist_comp)
                return ASTTupleNode(testlist_comp)
            return ASTListNode(testlist_comp)

        yield_expr = ctx.yield_expr()
        if yield_expr:
            return yield_expr.accept(self)

        dictorsetmaker = ctx.dictorsetmaker()
        if dictorsetmaker:
            return dictorsetmaker.accept(self)

        name = ctx.NAME()
        if name:
            return ASTIdentifierNode(name.getText())

        number = ctx.NUMBER()
        if number:
            return ASTLiteralNode(ASTLiteralType.NUMBER, number.getText())

        strings = ctx.STRING()
        if strings:
            return self.build_bin_op(ASTSequenceOperation.CONCAT,
                                     [ASTLiteralNode(ASTLiteralType.STRING, string.getText()) for string in strings])

        ellipsis_ = ctx.ELLIPSIS()
        if ellipsis_:
            return ASTLiteralNode(ASTLiteralType.ELLIPSIS)

        none = ctx.NONE()
        if none:
            return ASTLiteralNode(ASTLiteralType.NULL)

        if ctx.TRUE():
            return ASTLiteralNode(ASTLiteralType.BOOLEAN, "True")

        return ASTLiteralNode(ASTLiteralType.BOOLEAN, "False")

    def visitTestlist_comp(self, ctx: Python3Parser.Testlist_compContext):
        comp_for = ctx.comp_for()
        if comp_for:
            return ASTComprehensionNode(ctx.getChild(0).accept(self), comp_for.accept(self))

        return self.build_multi(self.visitChildren(ctx), ASTElementsNode)

    def visitTrailer(self, ctx: Python3Parser.TrailerContext):
        arguments = ctx.arglist()
        if arguments:
            return arguments

        subscripts = ctx.subscriptlist()
        if subscripts:
            return subscripts

        return ctx.NAME()

    def visitSubscriptlist(self, ctx: Python3Parser.SubscriptlistContext):
        return self.build_multi(self.visitChildren(ctx), ASTSubscriptsNode)

    def visitSubscript(self, ctx: Python3Parser.SubscriptContext):
        if not ctx.COLON():
            return ASTIndexNode(ctx.test(0).accept(self))

        children = ctx.getChildren()

        start = children[0].accept(self) if isinstance(children[0], Python3Parser.TestContext) else None

        stop = ctx.test(1) if start else ctx.test(0)
        if stop:
            stop = stop.accept(self)

        step = ctx.sliceop().accept(self) if ctx.sliceop() else None

        return ASTSliceNode(start, stop, step)

    def visitSliceop(self, ctx: Python3Parser.SliceopContext):
        test = ctx.test()
        return test.accept(self) if test else None

    def visitExprlist(self, ctx: Python3Parser.ExprlistContext):
        return self.build_multi(self.visitChildren(ctx), ASTExpressionsNode)

    def visitTestlist(self, ctx: Python3Parser.TestlistContext):
        return self.build_multi(self.visitChildren(ctx), ASTExpressionsNode)

    def visitDictorsetmaker(self, ctx: Python3Parser.DictorsetmakerContext):
        comp_for = ctx.comp_for()
        tests = ctx.test()

        # Dictionary
        if ctx.COLON() or ctx.POWER():
            if comp_for:
                expr = ctx.expr(0)
                if expr:
                    return ASTMapNode(
                        ASTComprehensionNode(ASTKeywordUnpackExpressionNode(expr.accept(self)), comp_for.accept(self)))
                return ASTMapNode(
                    ASTComprehensionNode(ASTKeyValuePairNode(tests[0].accept(self), tests[1].accept(self)),
                                         comp_for.accept(self)))

            children = ctx.getChildren(
                lambda child: self.filter_child(child, Python3Parser.ExprContext, Python3Parser.TestContext))
            items = []
            i = 0
            while i < len(children):
                if isinstance(children[i], Python3Parser.ExprContext):
                    items.append(ASTKeywordUnpackExpressionNode(children[i].accept(self)))
                    i += 1
                else:
                    items.append(ASTKeyValuePairNode(children[i].accept(self), children[i + 1].accept(self)))
                    i += 2
            return self.build_multi(items, ASTElementsNode)

        # Set
        if comp_for:
            star_expr = ctx.star_expr(0)
            if star_expr:
                return ASTMapNode(
                    ASTComprehensionNode(star_expr.accept(self), comp_for.accept(self)))
            return ASTMapNode(ASTComprehensionNode(tests[0].accept(self), comp_for.accept(self)))

        items = [child.accept(self)
                 for child in ctx.getChildren(lambda child:
                                              self.filter_child(child, Python3Parser.Star_exprContext,
                                                                Python3Parser.TestContext))]
        return self.build_multi(items, ASTElementsNode)

    def visitClassdef(self, ctx: Python3Parser.ClassdefContext):
        name = ASTIdentifierNode(ctx.NAME().getText())
        arguments = ctx.arglist()
        body = ctx.suite().accept(self)
        visibility = self.get_visibility(name.name)

        if arguments:
            return ASTClassDefinitionNode(name, body, arguments.accept(self), modifiers=[visibility])

        return ASTClassDefinitionNode(name, body, modifiers=[visibility])

    def visitArglist(self, ctx: Python3Parser.ArglistContext):
        return self.build_multi(self.visitChildren(ctx), ASTArgumentsNode)

    def visitArgument(self, ctx: Python3Parser.ArgumentContext):
        test = ctx.test(0).accept(self)

        if ctx.STAR():
            return ASTArgumentNode(ASTPositionalUnpackExpressionNode(test))

        if ctx.POWER():
            return ASTArgumentNode(ASTKeywordUnpackExpressionNode(test))

        if ctx.ASSIGN():
            return ASTKeywordArgumentNode(test, ctx.test(1).accept(self))

        comp_for = ctx.comp_for()
        if comp_for:
            return ASTArgumentNode(ASTGeneratorExpressionNode(ASTComprehensionNode(test, comp_for.accept(self))))

        return ASTArgumentNode(test)

    def visitComp_iter(self, ctx: Python3Parser.Comp_iterContext):
        return ctx.getChild(0)

    def visitComp_for(self, ctx: Python3Parser.Comp_forContext):
        exprlist = ctx.exprlist().accept(self)
        or_test = ctx.or_test().accept(self)
        comprehension = ctx.comp_iter()

        if comprehension:
            output = ASTLoopStatementNode(ASTBinaryOperationNode(ASTComparisonOperation.IN, exprlist,
                                                                 ASTComprehensionNode(or_test,
                                                                                      comprehension.accept(self))),
                                          None)
        else:
            output = ASTLoopStatementNode(ASTBinaryOperationNode(ASTComparisonOperation.IN, exprlist, or_test))

        return ASTAsyncNode(output) if ctx.ASYNC() else output

    def visitComp_if(self, ctx: Python3Parser.Comp_ifContext):
        test_nocond = ctx.test_nocond().accept(self)
        comprehension = ctx.comp_iter()

        if comprehension:
            return ASTIfStatementNode(ASTComprehensionNode(test_nocond, comprehension.accept(self)))
        return ASTIfStatementNode(test_nocond)

    def visitEncoding_decl(self, ctx: Python3Parser.Encoding_declContext):
        return ASTIdentifierNode(ctx.getText())

    def visitYield_expr(self, ctx: Python3Parser.Yield_exprContext):
        argument = ctx.yield_arg()
        return ASTYieldExpressionNode(argument.accept(self)) if argument else ASTYieldExpressionNode()

    def visitYield_arg(self, ctx: Python3Parser.Yield_argContext):
        if ctx.FROM():
            return ASTFromNode(ctx.test().accept(self))
        return ctx.testlist().accept(self)

    # endregion
