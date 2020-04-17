from metrics.parsers.python3.base.Python3Parser import Python3Parser
from metrics.parsers.python3.base.Python3Visitor import Python3Visitor
from metrics.structures.ast import *
from metrics.structures.ast import ASTTryStatementNode, ASTCatchStatementNode


class Python3ASTVisitor(Python3Visitor):
    # Behaviour
    def visit(self, tree):
        return AST(super().visit(tree))

    def visitChildren(self, node):
        result = []
        n = node.getChildCount()
        for i in range(n):
            if not self.shouldVisitNextChild(node, result):
                return result

            c = node.getChild(i)
            child_result = c.accept(self)
            result = self.aggregateResult(result, child_result)

        return result

    def visitTerminal(self, node):
        return super().visitTerminal(node)

    def visitErrorNode(self, node):
        return super().visitErrorNode(node)

    def defaultResult(self):
        return super().defaultResult()

    def aggregateResult(self, aggregate, next_result):
        return aggregate + [next_result]

    def shouldVisitNextChild(self, node, current_result):
        return super().shouldVisitNextChild(node, current_result)

    # Visits
    def visitSingle_input(self, ctx: Python3Parser.Single_inputContext):
        stmt = ctx.simple_stmt()

        if stmt:
            return stmt.accept(self)
        else:
            stmt = ctx.compound_stmt()
            if stmt:
                return stmt.accept(self)

        return self.defaultResult()

    def visitFile_input(self, ctx: Python3Parser.File_inputContext):
        statements = ctx.stmt()

        if statements:
            return build_right_associative_sequence([statement.accept(self) for statement in statements],
                                                    ASTStatementsNode)

        return self.defaultResult()

    def visitEval_input(self, ctx: Python3Parser.Eval_inputContext):
        return ctx.testlist().accept(self)

    def visitDecorator(self, ctx: Python3Parser.DecoratorContext):
        return super().visitDecorator(ctx)

    def visitDecorators(self, ctx: Python3Parser.DecoratorsContext):
        return super().visitDecorators(ctx)

    def visitDecorated(self, ctx: Python3Parser.DecoratedContext):
        return super().visitDecorated(ctx)

    def visitAsync_funcdef(self, ctx: Python3Parser.Async_funcdefContext):
        return ASTAsyncNode(ctx.funcdef().accept(self))

    def visitFuncdef(self, ctx: Python3Parser.FuncdefContext):
        name = ctx.NAME().getText()
        body = ctx.suite().accept(self)
        parameters = ctx.parameters().accept(self)
        return_type = ctx.test()

        if return_type:
            return ASTFunctionDefinitionNode(name, body, parameters, return_type.accept(self))

        return ASTFunctionDefinitionNode(name, body, parameters)

    def visitParameters(self, ctx: Python3Parser.ParametersContext):
        parameters = ctx.typedargslist()

        if parameters:
            return build_right_associative_sequence(parameters.accept(self), ASTParametersNode)

        return self.defaultResult()

    def visitTypedargslist(self, ctx: Python3Parser.TypedargslistContext):
        parameters = []

        child_count = ctx.getChildCount()
        i = 0
        while i < child_count:
            child = ctx.getChild(i)
            if child.getText() == "*" or child.getText() == "**":
                i += 1
                parameter = ctx.getChild(i).accept(self)
                if child.getText() == "*":
                    parameters.append(ASTPositionalArgumentsParameter(parameter.name, parameter.type))
                else:
                    parameters.append(ASTKeywordArgumentsParameter(parameter.name, parameter.type))
            else:
                parameter = ctx.getChild(i).accept(self)
                if parameter:
                    if i + 1 < child_count and i < ctx.getChild(i + 1).getText == "=":
                        i += 2
                        parameter.default = ctx.getChild(i).accept(self)
                    parameters.append(parameter)
            i += 1

        return parameters

    def visitTfpdef(self, ctx: Python3Parser.TfpdefContext):
        name = ctx.NAME().getText()
        return_type = ctx.test()

        if return_type:
            return ASTParameterNode(name, return_type.accept(self))

        return ASTParameterNode(name)

    def visitVarargslist(self, ctx: Python3Parser.VarargslistContext):
        parameters = []

        child_count = ctx.getChildCount()
        i = 0
        while i < child_count:
            child = ctx.getChild(i)
            if child.getText() == "*" or child.getText() == "**":
                i += 1
                name = ctx.getChild(i).accept(self)
                if child.getText() == "*":
                    parameters.append(ASTPositionalArgumentsParameter(name))
                else:
                    parameters.append(ASTKeywordArgumentsParameter(name))
            else:
                name = ctx.getChild(i).accept(self)
                if name:
                    parameter = ASTParameterNode(name)
                    if i + 1 < child_count and i < ctx.getChild(i + 1).getText == "=":
                        i += 2
                        parameter.default = ctx.getChild(i).accept(self)

                    parameters.append(parameter)
            i += 1

        return parameters

    def visitVfpdef(self, ctx: Python3Parser.VfpdefContext):
        return ctx.NAME().getText()

    def visitStmt(self, ctx: Python3Parser.StmtContext):
        return super().visitStmt(ctx)

    def visitSimple_stmt(self, ctx: Python3Parser.Simple_stmtContext):
        statements = ctx.small_stmt()

        if statements:
            return build_right_associative_sequence([statement.accept(self) for statement in statements],
                                                    ASTStatementsNode)

        return self.defaultResult()

    def visitSmall_stmt(self, ctx: Python3Parser.Small_stmtContext):
        return super().visitSmall_stmt(ctx)

    def visitExpr_stmt(self, ctx: Python3Parser.Expr_stmtContext):
        # Assignment, Annotation Assignment or Augmented Assignment
        annotation_assignment = ctx.annassign()
        if annotation_assignment:
            return ASTAnnotationAssignmentNode(**annotation_assignment.accept(self),
                                               variables=ctx.testlist_star_expr(0).accept(self))
        else:
            augmented_assignment = ctx.augassign()
            if augmented_assignment:
                return ASTAugmentedAssignmentNode(augmented_assignment.accept(self),
                                                  ctx.testlist_star_expr(0).accept(self),
                                                  ctx.yield_expr(0).accept(self)
                                                  if ctx.yield_expr(0)
                                                  else ctx.testlist().accept(self))
            else:
                children = ctx.getChildren(lambda child: filter_child(child, Python3Parser.Testlist_star_exprContext,
                                                                      Python3Parser.Yield_exprContext))

                return build_right_associative_sequence([child.accept(self) for child in children], ASTAssignmentNode)

    def visitAnnassign(self, ctx: Python3Parser.AnnassignContext):
        return {
            "annotation": ctx.test(0).accept(self),
            "values": ctx.test(1).accept(self)
        }

    def visitTestlist_star_expr(self, ctx: Python3Parser.Testlist_star_exprContext):
        children = ctx.getChildren(
            lambda child: filter_child(child, Python3Parser.TestContext, Python3Parser.Star_exprContext))
        return build_right_associative_sequence([child.accept(self) for child in children], ASTExpressionsNode)

    def visitAugassign(self, ctx: Python3Parser.AugassignContext):
        return {
            "+=": AST.INPLACE_ADD,
            "-=": AST.INPLACE_SUBTRACT,
            "*=": AST.INPLACE_MULTIPLY,
            "/=": AST.INPLACE_DIVIDE,
            "//=": AST.INPLACE_FLOOR_DIVIDE,
            "%=": AST.INPLACE_MODULO,
            "**=": AST.INPLACE_POWER,
            "&=": AST.INPLACE_BITWISE_AND,
            "|=": AST.INPLACE_BITWISE_OR,
            "^=": AST.INPLACE_BITWISE_XOR,
            "<<=": AST.INPLACE_LEFT_SHIFT,
            ">>=": AST.INPLACE_RIGHT_SHIFT,
            "@=": AST.INPLACE_MATRIX_MULTIPLY,
        }[ctx.getText()]

    def visitDel_stmt(self, ctx: Python3Parser.Del_stmtContext):
        return ASTDelStatementNode(ctx.exprlist().accept(self))

    def visitPass_stmt(self, ctx: Python3Parser.Pass_stmtContext):
        return ASTPassStatementNode()

    def visitFlow_stmt(self, ctx: Python3Parser.Flow_stmtContext):
        return super().visitFlow_stmt(ctx)

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
        return super().visitYield_stmt(ctx)

    def visitRaise_stmt(self, ctx: Python3Parser.Raise_stmtContext):
        exception = ctx.test(0)
        _from = ctx.test(1)

        if _from:
            return ASTThrowStatementNode(ASTFromNode(exception.accept(self), _from.accept(self)))
        elif exception:
            return ASTThrowStatementNode(exception.accept(self))

        return ASTThrowStatementNode()

    def visitImport_stmt(self, ctx: Python3Parser.Import_stmtContext):
        return super().visitImport_stmt(ctx)

    def visitImport_name(self, ctx: Python3Parser.Import_nameContext):
        return ASTImportStatementNode(ctx.dotted_as_names().accept(self))

    def visitImport_from(self, ctx: Python3Parser.Import_fromContext):
        _from = "".join(
            [child.accept(self) if isinstance(child, Python3Parser.Dotted_nameContext) else child.getText() for child in
             ctx.getChildren(lambda child: filter_child(child, Python3Parser.DOT, Python3Parser.ELLIPSIS,
                                                        Python3Parser.Dotted_nameContext))])
        _import = ctx.import_as_names()
        if not _import:
            _import = "*"

        return ASTImportStatementNode(ASTFromNode(_from, _import))

    def visitImport_as_name(self, ctx: Python3Parser.Import_as_nameContext):
        name = ctx.NAME(0)
        alias = ctx.NAME(1)

        if alias:
            return ASTAsNode(name.getText(), alias.getText())

        return name.getText()

    def visitDotted_as_name(self, ctx: Python3Parser.Dotted_as_nameContext):
        dotted_name = ctx.dotted_name()
        alias = ctx.NAME()

        if alias:
            return ASTAsNode(dotted_name.accept(self), alias.getText())

        return dotted_name.accept(self)

    def visitImport_as_names(self, ctx: Python3Parser.Import_as_namesContext):
        return build_right_associative_sequence(self.visitChildren(ctx), ASTExpressionsNode)

    def visitDotted_as_names(self, ctx: Python3Parser.Dotted_as_namesContext):
        return build_right_associative_sequence(self.visitChildren(ctx), ASTExpressionsNode)

    def visitDotted_name(self, ctx: Python3Parser.Dotted_nameContext):
        return ctx.getText()

    def visitGlobal_stmt(self, ctx: Python3Parser.Global_stmtContext):
        return ASTGlobalStatementNode(
            build_right_associative_sequence([child.getText() for child in ctx.NAME()], ASTExpressionsNode))

    def visitNonlocal_stmt(self, ctx: Python3Parser.Nonlocal_stmtContext):
        return ASTNonLocalStatementNode(
            build_right_associative_sequence([child.getText() for child in ctx.NAME()], ASTExpressionsNode))

    def visitAssert_stmt(self, ctx: Python3Parser.Assert_stmtContext):
        condition = ctx.test(0)
        message = ctx.test(1)

        if message:
            return ASTAssertStatementNode(condition.accept(self), message.accept(self))

        return ASTAssertStatementNode(condition.accept(self))

    def visitCompound_stmt(self, ctx: Python3Parser.Compound_stmtContext):
        return super().visitCompound_stmt(ctx)

    def visitAsync_stmt(self, ctx: Python3Parser.Async_stmtContext):
        return ASTAsyncNode(ctx.getChild(1).accept(self))

    def visitIf_stmt(self, ctx: Python3Parser.If_stmtContext):
        return build_if_else(ctx.getChildren(), self)

    def visitWhile_stmt(self, ctx: Python3Parser.While_stmtContext):
        condition = ctx.test()
        body = ctx.suite(0)
        else_body = ctx.suite(1)

        if else_body:
            return ASTLoopElseStatementNode(condition.accept(self), body.accept(self), else_body.accept(self))

        return ASTLoopStatementNode(condition.accept(self), body.accept(self))

    def visitFor_stmt(self, ctx: Python3Parser.For_stmtContext):
        exprlist = ctx.exprlist()
        testlist = ctx.testlist()
        body = ctx.suite(0)
        else_body = ctx.suite(1)

        if else_body:
            return ASTLoopElseStatementNode(
                ASTBinOpNode(AST.IN, exprlist.accept(self), testlist.accept(self)),
                body.accept(self), else_body.accept(self))

        return ASTLoopStatementNode(
            ASTBinOpNode(AST.IN, exprlist.accept(self), testlist.accept(self)), body.accept(self))

    def visitTry_stmt(self, ctx: Python3Parser.Try_stmtContext):
        bodies = ctx.suite()
        except_clauses = ctx.except_clause()

        i = 1
        catches = []
        if except_clauses:
            for except_clause in except_clauses:
                catches.append(ASTCatchStatementNode(except_clause.accept(self), bodies[i].accept(self)))
                i += 1

        if ctx.ELSE():
            _else = bodies[i].accept(self)
            i += 1
        else:
            _else = None

        _finally = bodies[i].accept(self) if ctx.FINALLY() else None

        return ASTTryStatementNode(bodies[0].accept(self), catches, _else, _finally)

    def visitWith_stmt(self, ctx: Python3Parser.With_stmtContext):
        return ASTWithStatementNode(
            build_right_associative_sequence([item.accept(self) for item in (ctx.with_item())], ASTExpressionsNode),
            ctx.suite().accept(self))

    def visitWith_item(self, ctx: Python3Parser.With_itemContext):
        expression = ctx.test()
        alias = ctx.expr()

        if alias:
            return ASTAsNode(expression.accept(self), alias.accept(self))

        return expression.accept(self)

    def visitExcept_clause(self, ctx: Python3Parser.Except_clauseContext):
        expression = ctx.test()
        alias = ctx.NAME()

        if alias:
            return ASTAsNode(expression.accept(self), alias.getText())

        if expression:
            return expression.accept(self)

        return None

    def visitSuite(self, ctx: Python3Parser.SuiteContext):
        simple_stmt = ctx.simple_stmt()

        if simple_stmt:
            return simple_stmt.accept(self)

        return build_right_associative_sequence(self.visitChildren(ctx), ASTStatementsNode)

    def visitTest(self, ctx: Python3Parser.TestContext):
        condition = ctx.or_test(1)

        if condition:
            return ASTIfElseStatementNode(condition.accept(self), ctx.getChild(0).accept(self), ctx.test().accept(self))

        return ctx.getChild(0).accept(self)

    def visitTest_nocond(self, ctx: Python3Parser.Test_nocondContext):
        return ctx.getChild(0).accept(self)

    def visitLambdef(self, ctx: Python3Parser.LambdefContext):
        parameters = ctx.varargslist()
        body = ctx.test()

        if parameters:
            return ASTAnonymousFunctionDefinitionNode(body.accept(self), parameters.accept(self))

        return ASTAnonymousFunctionDefinitionNode(body.accept(self))

    def visitLambdef_nocond(self, ctx: Python3Parser.Lambdef_nocondContext):
        parameters = ctx.varargslist()
        body = ctx.test_nocond()

        if parameters:
            return ASTAnonymousFunctionDefinitionNode(body.accept(self), parameters.accept(self))

        return ASTAnonymousFunctionDefinitionNode(body.accept(self))

    def visitOr_test(self, ctx: Python3Parser.Or_testContext):
        build_bin_op(AST.LOGICAL_OR, self.visitChildren(ctx))

    def visitAnd_test(self, ctx: Python3Parser.And_testContext):
        build_bin_op(AST.LOGICAL_AND, self.visitChildren(ctx))

    def visitNot_test(self, ctx: Python3Parser.Not_testContext):
        return ASTUnOpNode(AST.LOGICAL_NEGATION, ctx.getChild(1).accept(self))

    def visitComparison(self, ctx: Python3Parser.ComparisonContext):
        build_bin_op_choice(self.visitChildren(ctx))

    def visitComp_op(self, ctx: Python3Parser.Comp_opContext):
        comparison_operators = {
            "==": AST.EQUAL,
            "!=": AST.NOT_EQUAL,
            "<>": AST.NOT_EQUAL,
            "<": AST.LESS_THAN,
            ">": AST.GREATER_THAN,
            "<=": AST.LESS_THAN_OR_EQUAL,
            ">=": AST.GREATER_THAN_OR_EQUAL,
            "in": AST.IN,
            "not in": [AST.LOGICAL_NEGATION, AST.IS],
            "is": AST.IS,
            "is not": [AST.LOGICAL_NEGATION, AST.IN]
        }

        return comparison_operators[ctx.getText()]

    def visitStar_expr(self, ctx: Python3Parser.Star_exprContext):
        return ASTUnpackExpressionNode(ctx.expr().accept(self))

    def visitExpr(self, ctx: Python3Parser.ExprContext):
        return build_bin_op(AST.BITWISE_OR, self.visitChildren(ctx))

    def visitXor_expr(self, ctx: Python3Parser.Xor_exprContext):
        return build_bin_op(AST.BITWISE_XOR, self.visitChildren(ctx))

    def visitAnd_expr(self, ctx: Python3Parser.And_exprContext):
        return build_bin_op(AST.BITWISE_AND, self.visitChildren(ctx))

    def visitShift_expr(self, ctx: Python3Parser.Shift_exprContext):
        operators = {
            "<<": AST.LEFT_SHIFT,
            ">>": AST.RIGHT_SHIFT
        }

        return build_bin_op_choice(
            [child.accept(self) if isinstance(child, Python3Parser.Arith_exprContext) else operators[child.getText] for
             child in ctx.getChildren()])

    def visitArith_expr(self, ctx: Python3Parser.Arith_exprContext):
        operators = {
            "+": AST.ADD,
            "-": AST.SUBTRACT
        }

        return build_bin_op_choice(
            [child.accept(self) if isinstance(child, Python3Parser.Arith_exprContext) else operators[child.getText] for
             child in ctx.getChildren()])

    def visitTerm(self, ctx: Python3Parser.TermContext):
        operators = {
            "*": AST.MULTIPLY,
            "@": AST.MATRIX_MULTIPLY,
            "/": AST.DIVIDE,
            "%": AST.MODULO,
            "//": AST.FLOOR_DIVIDE
        }

        return build_bin_op_choice(
            [child.accept(self) if isinstance(child, Python3Parser.Arith_exprContext) else operators[child.getText] for
             child in ctx.getChildren()])

    def visitFactor(self, ctx: Python3Parser.FactorContext):
        operators = {
            "+": AST.POSITIVE,
            "-": AST.ARITH_NEGATION,
            "~": AST.BITWISE_INVERSION
        }

        power = ctx.power()
        if power:
            return power.accept(self)

        return ASTUnOpNode(operators[ctx.getChild(0).getText()], ctx.factor().accept(self))

    def visitPower(self, ctx: Python3Parser.PowerContext):
        return build_bin_op_rassoc(AST.POWER, self.visitChildren(ctx))

    def visitAtom_expr(self, ctx: Python3Parser.Atom_exprContext):
        _await = ctx.AWAIT()

        if _await:
            return ASTAwaitNode(build_atom_expr(self.visitChildren(ctx), self))

        return build_atom_expr(self.visitChildren(ctx), self)

    def visitAtom(self, ctx: Python3Parser.AtomContext):
        testlist_comp = ctx.testlist_comp()
        if testlist_comp:
            if ctx.OPEN_PAREN():
                return ASTGeneratorExpressionNode(testlist_comp.accept(self))
            return ASTListNode(testlist_comp.accept(self))

        yield_expr = ctx.yield_expr()
        if yield_expr:
            return yield_expr.accept(self)

        dictorsetmaker = ctx.dictorsetmaker()
        if dictorsetmaker:
            return dictorsetmaker.accept(self)

        return ctx.getText()

    def visitTestlist_comp(self, ctx: Python3Parser.Testlist_compContext):
        comp_for = ctx.comp_for()
        if comp_for:
            return ASTComprehensionNode(ctx.getChild(0).accept(self), comp_for.accept(self))

        return build_right_associative_sequence(self.visitChildren(ctx), ASTItemsNode)

    def visitTrailer(self, ctx: Python3Parser.TrailerContext):
        arguments = ctx.arglist()
        if arguments:
            return arguments.accept(self)

        subscripts = ctx.subscriptlist()
        if subscripts:
            return subscripts.accept(self)

        return ctx.NAME()

    def visitSubscriptlist(self, ctx: Python3Parser.SubscriptlistContext):
        return build_right_associative_sequence(self.visitChildren(ctx), ASTSubscriptsNode)

    def visitSubscript(self, ctx: Python3Parser.SubscriptContext):
        if not ctx.COLON():
            return ASTIndexNode(ctx.test(0).accept(self))

        children = ctx.getChildren()

        start = children[0].accept(self) if isinstance(children[0], Python3Parser.TestContext) else None

        if start:
            stop = ctx.test(1)
        else:
            stop = ctx.test(0)

        step = ctx.sliceop().accept(self) if ctx.sliceop() else None

        return ASTSliceNode(start, stop, step)

    def visitSliceop(self, ctx: Python3Parser.SliceopContext):
        test = ctx.test()
        return test.accept(self) if test else None

    def visitExprlist(self, ctx: Python3Parser.ExprlistContext):
        return build_expressions(self.visitChildren(ctx))

    def visitTestlist(self, ctx: Python3Parser.TestlistContext):
        return build_expressions(self.visitChildren(ctx))

    def visitDictorsetmaker(self, ctx: Python3Parser.DictorsetmakerContext):
        comp_for = ctx.comp_for()
        tests = ctx.test()

        # Dictionary
        if ctx.COLON() or ctx.POWER():
            if comp_for:
                expr = ctx.expr(0)
                if expr:
                    return ASTMapNode(
                        ASTComprehensionNode(ASTUnpackExpressionNode(expr.accept(self)), comp_for.accept(self)))
                return ASTMapNode(
                    ASTComprehensionNode(ASTKeyValuePairNode(tests[0].accept(self), tests[1].accept(self)),
                                         comp_for.accept(self)))

            children = ctx.getChildren(
                lambda child: filter_child(child, Python3Parser.ExprContext, Python3Parser.TestContext))
            items = []
            i = 0
            while i < len(children):
                if isinstance(children[i], Python3Parser.ExprContext):
                    items.append(ASTUnpackExpressionNode(children[i].accept(self)))
                    i += 1
                else:
                    items.append(ASTKeyValuePairNode(children[i].accept(self), children[i + 1].accept(self)))
                    i += 2
            return build_right_associative_sequence(items, ASTItemsNode)

        # Set
        if comp_for:
            star_expr = ctx.star_expr(0)
            if star_expr:
                return ASTMapNode(
                    ASTComprehensionNode(ASTUnpackExpressionNode(star_expr.accept(self)), comp_for.accept(self)))
            return ASTMapNode(ASTComprehensionNode(tests[0].accept(self), comp_for.accept(self)))

        items = [ASTUnpackExpressionNode(child.accept(self))
                 if isinstance(child, Python3Parser.Star_exprContext)
                 else child.accept(self)
                 for child in ctx.getChildren(lambda child:
                                              filter_child(child, Python3Parser.Star_exprContext,
                                                           Python3Parser.TestContext))]
        return build_right_associative_sequence(items, ASTItemsNode)

    def visitClassdef(self, ctx: Python3Parser.ClassdefContext):
        arguments = ctx.arglist()

        if arguments:
            return ASTClassDefinitionNode(ctx.NAME().getText(), ctx.suite().accept(self), arguments.accept(self))

        return ASTClassDefinitionNode(ctx.NAME().getText(), ctx.suite().accept(self))

    def visitArglist(self, ctx: Python3Parser.ArglistContext):
        return build_right_associative_sequence(self.visitChildren(ctx), ASTArgumentsNode)

    def visitArgument(self, ctx: Python3Parser.ArgumentContext):
        test = ctx.test(0).accept(self)

        if ctx.POWER() or ctx.STAR():
            return ASTUnpackExpressionNode(test)

        if ctx.ASSIGN():
            return ASTAssignmentNode(test, ctx.test(1).accept(self))

        comp_for = ctx.comp_for()
        if comp_for:
            return ASTComprehensionNode(test, comp_for.accept(self))

        return test

    def visitComp_iter(self, ctx: Python3Parser.Comp_iterContext):
        return super().visitComp_iter(ctx)

    def visitComp_for(self, ctx: Python3Parser.Comp_forContext):
        exprlist = ctx.exprlist().accept(self)
        or_test = ctx.or_test().accept(self)
        comprehension = ctx.comp_iter()

        if comprehension:
            output = ASTLoopStatementNode(
                ASTBinOpNode(AST.IN, exprlist, ASTComprehensionNode(or_test, comprehension.accept(self))), None)
        else:
            output = ASTLoopStatementNode(ASTBinOpNode(AST.IN, exprlist, or_test), None)

        return ASTAsyncNode(output) if ctx.ASYNC() else output

    def visitComp_if(self, ctx: Python3Parser.Comp_ifContext):
        test_nocond = ctx.test_nocond().accept(self)
        comprehension = ctx.comp_iter()

        if comprehension:
            return ASTIfStatementNode(ASTComprehensionNode(test_nocond, comprehension.accept(self)), None)
        return ASTIfStatementNode(test_nocond, None)

    def visitEncoding_decl(self, ctx: Python3Parser.Encoding_declContext):
        return ctx.getText()

    def visitYield_expr(self, ctx: Python3Parser.Yield_exprContext):
        argument = ctx.yield_arg()
        return ASTYieldNode(argument) if argument else ASTYieldNode()

    def visitYield_arg(self, ctx: Python3Parser.Yield_argContext):
        if ctx.FROM():
            return ASTFromNode(ctx.test().accept(self), None)
        return ctx.testlist().accept(self)


def build_expressions(expressions):
    return ASTExpressionsNode(expressions[0], build_expressions(expressions[1:]) if len(expressions) > 1 else None)


def build_if_else(children, visitor):
    if children[0].getText() == "if" or children[0].getText() == "elif":
        if len(children) == 4:
            return ASTIfStatementNode(children[1].accept(visitor), children[3].accept(visitor))
        else:
            return ASTIfElseStatementNode(children[1].accept(visitor), children[3].accept(visitor),
                                          build_if_else(children[4:], visitor))
    else:
        return children[-1].accept(visitor)


def build_bin_op(operation, expressions):
    if len(expressions) == 1:
        return expressions[0]
    return ASTBinOpNode(operation, build_bin_op(operation, expressions[:-1]), expressions[-1])


def build_bin_op_choice(children):
    if len(children) == 1:
        return children[0]

    operator = children[-2]
    if isinstance(operator, list):
        return ASTUnOpNode(operator[0], ASTBinOpNode(operator[1], build_bin_op_choice(children[:-2]), children[-1]))

    return ASTBinOpNode(operator, build_bin_op_choice(children[:-2]), children[-1])


def build_bin_op_rassoc(operation, expressions):
    if len(expressions) == 1:
        return expressions[0]
    return ASTBinOpNode(operation, expressions[0], build_bin_op_rassoc(operation, expressions[1:]))


def build_right_associative_sequence(sequence, node_type):
    if len(sequence) == 1:
        return sequence[0]

    return node_type(sequence[0], build_right_associative_sequence(sequence[1:], node_type))


def build_left_associative_sequence(sequence, node_type):
    if len(sequence) == 1:
        return sequence[0]

    return node_type(build_left_associative_sequence(sequence[:-1], node_type), sequence[-1])


def build_atom_expr(children, visitor):
    if len(children) == 1:
        return children[0]

    if isinstance(children[-1], Python3Parser.SubscriptlistContext):
        return ASTAccessNode(build_atom_expr(children[:-1], visitor), children[-1].accept(visitor))
    elif isinstance(children[-1], Python3Parser.ArglistContext):
        return ASTArgumentsNode(build_atom_expr(children[:-1], visitor), children[-1].accept(visitor))

    return ASTMemberNode(build_atom_expr(children[:-1], visitor), children[-1])


def filter_child(child, *contexts):
    for context in contexts:
        if isinstance(child, context):
            return True
    return False
