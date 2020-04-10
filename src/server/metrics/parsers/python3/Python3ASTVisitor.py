from metrics.parsers.python3.base.Python3Parser import Python3Parser
from metrics.parsers.python3.base.Python3Visitor import Python3Visitor
from metrics.structures.ast import *
from metrics.structures.inheritance_tree import *
from metrics.structures.results import *

binary_operators = {
    "+": AST.ADD,
    "-": AST.SUBTRACT,
    "*": AST.MULTIPLY,
    "/": AST.DIVIDE,
    "//": AST.FLOOR_DIVIDE,
    "%": AST.MODULO,
    "**": AST.POWER,
    "|": AST.BITWISE_OR,
    "^": AST.BITWISE_XOR,
    "&": AST.BITWISE_AND,
    "<<": AST.LEFT_SHIFT,
    ">>": AST.RIGHT_SHIFT,
    "@": AST.MATRIX_MULTIPLY,
}

unary_operators = {
    "+": AST.POSITIVE,
    "-": AST.ARITH_NEGATION,
    "~": AST.BITWISE_INVERSION,
}

logical_operators = {
    "and": AST.LOGICAL_AND,
    "or": AST.LOGICAL_OR,
    "not": AST.LOGICAL_NEGATION,
}

comparison_operators = {
    "==": AST.EQUAL,
    "!=": AST.NOT_EQUAL,
    "<>": AST.NOT_EQUAL,
    "<": AST.LESS_THAN,
    ">": AST.GREATER_THAN,
    "<=": AST.LESS_THAN_OR_EQUAL,
    ">=": AST.GREATER_THAN_OR_EQUAL,
    "in": AST.IN,
    "is": AST.IS,
}

augmented_assignment = {
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
}


class Python3ASTVisitor(Python3Visitor):
    # Overrides
    def __init__(self) -> None:
        super().__init__()

    # Behaviour
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
        super().visitErrorNode(node)

    def defaultResult(self):
        return super().defaultResult()

    def aggregateResult(self, aggregate, next_result):
        if next_result:
            if isinstance(next_result, list):
                return aggregate + next_result
            return aggregate + [next_result]

    def shouldVisitNextChild(self, node, current_result):
        return super().shouldVisitNextChild(node, current_result)

    # Visits
    def visitSingle_input(self, ctx: Python3Parser.Single_inputContext):
        return super().visitSingle_input(ctx)

    def visitFile_input(self, ctx: Python3Parser.File_inputContext):
        return build_statements(self.visitChildren(ctx))

    def visitEval_input(self, ctx: Python3Parser.Eval_inputContext):
        return super().visitEval_input(ctx)

    def visitDecorator(self, ctx: Python3Parser.DecoratorContext):
        return super().visitDecorator(ctx)

    def visitDecorators(self, ctx: Python3Parser.DecoratorsContext):
        return super().visitDecorators(ctx)

    def visitDecorated(self, ctx: Python3Parser.DecoratedContext):
        return super().visitDecorated(ctx)

    def visitAsync_funcdef(self, ctx: Python3Parser.Async_funcdefContext):
        return super().visitAsync_funcdef(ctx)

    def visitFuncdef(self, ctx: Python3Parser.FuncdefContext):
        name = ctx.getChild(1).getText()
        arguments = ctx.getChild(2).accept(self)
        if ctx.getChildCount() == 5:
            return ASTFunctionDefinitionNode(name, ctx.getChild(4).accept(self), arguments)
        else:
            return ASTFunctionDefinitionNode(name, ctx.getChild(6).accept(self), arguments,
                                             ctx.getChild(4).accept(self))

    def visitParameters(self, ctx: Python3Parser.ParametersContext):
        if ctx.getChildCount() == 3:
            return ctx.getChild(1).accept(self)
        return self.defaultResult()

    def visitTypedargslist(self, ctx: Python3Parser.TypedargslistContext):
        parameters = []
        i = 0
        child_count = ctx.getChildCount()
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

    def visitTfpdef(self, ctx: Python3Parser.TfpdefContext):
        if ctx.getChildCount() > 1:
            return ASTParameterNode(ctx.getChild(0).getText(), ctx.getChild(1).getText())
        return ASTParameterNode(ctx.getChild(0).getText())

    def visitVarargslist(self, ctx: Python3Parser.VarargslistContext):
        return super().visitVarargslist(ctx)

    def visitVfpdef(self, ctx: Python3Parser.VfpdefContext):
        return super().visitVfpdef(ctx)

    def visitStmt(self, ctx: Python3Parser.StmtContext):
        return super().visitStmt(ctx)

    def visitSimple_stmt(self, ctx: Python3Parser.Simple_stmtContext):
        return super().visitSimple_stmt(ctx)

    def visitSmall_stmt(self, ctx: Python3Parser.Small_stmtContext):
        return super().visitSmall_stmt(ctx)

    def visitExpr_stmt(self, ctx: Python3Parser.Expr_stmtContext):
        # Assignment, Annotation Assignment or Augmented Assignment
        children = self.visitChildren(ctx)

        if isinstance(children[1], ASTAugmentedAssignmentNode) or isinstance(children[1], ASTAnnotationAssignmentNode):
            children[1].variables = children[0]
            if isinstance(children[1], ASTAugmentedAssignmentNode):
                children[1].values = children[2]
            return children[1]

        return build_assignments(children)

    def visitAnnassign(self, ctx: Python3Parser.AnnassignContext):
        children = self.visitChildren(ctx)
        if len(children) == 1:
            return ASTAnnotationAssignmentNode(children[0])
        else:
            return ASTAnnotationAssignmentNode(children[1], values=children[1])

    def visitTestlist_star_expr(self, ctx: Python3Parser.Testlist_star_exprContext):
        return super().visitTestlist_star_expr(ctx)

    def visitAugassign(self, ctx: Python3Parser.AugassignContext):
        return ASTAugmentedAssignmentNode(augmented_assignment[ctx.getText()])

    def visitDel_stmt(self, ctx: Python3Parser.Del_stmtContext):
        return super().visitDel_stmt(ctx)

    def visitPass_stmt(self, ctx: Python3Parser.Pass_stmtContext):
        return super().visitPass_stmt(ctx)

    def visitFlow_stmt(self, ctx: Python3Parser.Flow_stmtContext):
        return super().visitFlow_stmt(ctx)

    def visitBreak_stmt(self, ctx: Python3Parser.Break_stmtContext):
        return super().visitBreak_stmt(ctx)

    def visitContinue_stmt(self, ctx: Python3Parser.Continue_stmtContext):
        return super().visitContinue_stmt(ctx)

    def visitReturn_stmt(self, ctx: Python3Parser.Return_stmtContext):
        return super().visitReturn_stmt(ctx)

    def visitYield_stmt(self, ctx: Python3Parser.Yield_stmtContext):
        return super().visitYield_stmt(ctx)

    def visitRaise_stmt(self, ctx: Python3Parser.Raise_stmtContext):
        return super().visitRaise_stmt(ctx)

    def visitImport_stmt(self, ctx: Python3Parser.Import_stmtContext):
        return super().visitImport_stmt(ctx)

    def visitImport_name(self, ctx: Python3Parser.Import_nameContext):
        return super().visitImport_name(ctx)

    def visitImport_from(self, ctx: Python3Parser.Import_fromContext):
        return super().visitImport_from(ctx)

    def visitImport_as_name(self, ctx: Python3Parser.Import_as_nameContext):
        return super().visitImport_as_name(ctx)

    def visitDotted_as_name(self, ctx: Python3Parser.Dotted_as_nameContext):
        return super().visitDotted_as_name(ctx)

    def visitImport_as_names(self, ctx: Python3Parser.Import_as_namesContext):
        return super().visitImport_as_names(ctx)

    def visitDotted_as_names(self, ctx: Python3Parser.Dotted_as_namesContext):
        return super().visitDotted_as_names(ctx)

    def visitDotted_name(self, ctx: Python3Parser.Dotted_nameContext):
        return super().visitDotted_name(ctx)

    def visitGlobal_stmt(self, ctx: Python3Parser.Global_stmtContext):
        return super().visitGlobal_stmt(ctx)

    def visitNonlocal_stmt(self, ctx: Python3Parser.Nonlocal_stmtContext):
        return super().visitNonlocal_stmt(ctx)

    def visitAssert_stmt(self, ctx: Python3Parser.Assert_stmtContext):
        return super().visitAssert_stmt(ctx)

    def visitCompound_stmt(self, ctx: Python3Parser.Compound_stmtContext):
        return super().visitCompound_stmt(ctx)

    def visitAsync_stmt(self, ctx: Python3Parser.Async_stmtContext):
        return super().visitAsync_stmt(ctx)

    def visitIf_stmt(self, ctx: Python3Parser.If_stmtContext):
        return super().visitIf_stmt(ctx)

    def visitWhile_stmt(self, ctx: Python3Parser.While_stmtContext):
        return super().visitWhile_stmt(ctx)

    def visitFor_stmt(self, ctx: Python3Parser.For_stmtContext):
        return super().visitFor_stmt(ctx)

    def visitTry_stmt(self, ctx: Python3Parser.Try_stmtContext):
        return super().visitTry_stmt(ctx)

    def visitWith_stmt(self, ctx: Python3Parser.With_stmtContext):
        return super().visitWith_stmt(ctx)

    def visitWith_item(self, ctx: Python3Parser.With_itemContext):
        return super().visitWith_item(ctx)

    def visitExcept_clause(self, ctx: Python3Parser.Except_clauseContext):
        return super().visitExcept_clause(ctx)

    def visitSuite(self, ctx: Python3Parser.SuiteContext):
        return super().visitSuite(ctx)

    def visitTest(self, ctx: Python3Parser.TestContext):
        return super().visitTest(ctx)

    def visitTest_nocond(self, ctx: Python3Parser.Test_nocondContext):
        return super().visitTest_nocond(ctx)

    def visitLambdef(self, ctx: Python3Parser.LambdefContext):
        return super().visitLambdef(ctx)

    def visitLambdef_nocond(self, ctx: Python3Parser.Lambdef_nocondContext):
        return super().visitLambdef_nocond(ctx)

    def visitOr_test(self, ctx: Python3Parser.Or_testContext):
        return super().visitOr_test(ctx)

    def visitAnd_test(self, ctx: Python3Parser.And_testContext):
        return super().visitAnd_test(ctx)

    def visitNot_test(self, ctx: Python3Parser.Not_testContext):
        return super().visitNot_test(ctx)

    def visitComparison(self, ctx: Python3Parser.ComparisonContext):
        return super().visitComparison(ctx)

    def visitComp_op(self, ctx: Python3Parser.Comp_opContext):
        return super().visitComp_op(ctx)

    def visitStar_expr(self, ctx: Python3Parser.Star_exprContext):
        return super().visitStar_expr(ctx)

    def visitExpr(self, ctx: Python3Parser.ExprContext):
        return CometNodeResult(self.ast_bin_op(ctx), None, None)

    def visitXor_expr(self, ctx: Python3Parser.Xor_exprContext):
        return CometNodeResult(self.ast_bin_op(ctx), None, None)

    def visitAnd_expr(self, ctx: Python3Parser.And_exprContext):
        return CometNodeResult(self.ast_bin_op(ctx), None, None)

    def visitShift_expr(self, ctx: Python3Parser.Shift_exprContext):
        return CometNodeResult(self.ast_bin_op(ctx), None, None)

    def visitArith_expr(self, ctx: Python3Parser.Arith_exprContext):
        return CometNodeResult(self.ast_bin_op(ctx), None, None)

    def visitTerm(self, ctx: Python3Parser.TermContext):
        return CometNodeResult(self.ast_bin_op(ctx), None, None)

    def visitFactor(self, ctx: Python3Parser.FactorContext):
        if ctx.getChildCount() == 2:
            return CometNodeResult(self.ast_un_op(ctx), None, None)
        return super().visitFactor(ctx)

    def visitPower(self, ctx: Python3Parser.PowerContext):
        return CometNodeResult(self.ast_bin_op(ctx), None, None)

    def visitAtom_expr(self, ctx: Python3Parser.Atom_exprContext):
        return super().visitAtom_expr(ctx)

    def visitAtom(self, ctx: Python3Parser.AtomContext):
        return super().visitAtom(ctx)

    def visitTestlist_comp(self, ctx: Python3Parser.Testlist_compContext):
        return super().visitTestlist_comp(ctx)

    def visitTrailer(self, ctx: Python3Parser.TrailerContext):
        return super().visitTrailer(ctx)

    def visitSubscriptlist(self, ctx: Python3Parser.SubscriptlistContext):
        return super().visitSubscriptlist(ctx)

    def visitSubscript(self, ctx: Python3Parser.SubscriptContext):
        return super().visitSubscript(ctx)

    def visitSliceop(self, ctx: Python3Parser.SliceopContext):
        return super().visitSliceop(ctx)

    def visitExprlist(self, ctx: Python3Parser.ExprlistContext):
        # return ASTExpressionsNode(, self.visitChildren(ctx)
        pass

    def visitTestlist(self, ctx: Python3Parser.TestlistContext):
        return super().visitTestlist(ctx)

    def visitDictorsetmaker(self, ctx: Python3Parser.DictorsetmakerContext):
        return super().visitDictorsetmaker(ctx)

    def visitClassdef(self, ctx: Python3Parser.ClassdefContext):
        self.inheritance_tree.add_node(InheritanceNode(self.visitChildren(ctx)))
        return CometNodeResult(None, None, InheritanceNode(self.visitChildren(ctx)))

    def visitArglist(self, ctx: Python3Parser.ArglistContext):
        return super().visitArglist(ctx)

    def visitArgument(self, ctx: Python3Parser.ArgumentContext):
        return super().visitArgument(ctx)

    def visitComp_iter(self, ctx: Python3Parser.Comp_iterContext):
        return super().visitComp_iter(ctx)

    def visitComp_for(self, ctx: Python3Parser.Comp_forContext):
        return super().visitComp_for(ctx)

    def visitComp_if(self, ctx: Python3Parser.Comp_ifContext):
        return super().visitComp_if(ctx)

    def visitEncoding_decl(self, ctx: Python3Parser.Encoding_declContext):
        return super().visitEncoding_decl(ctx)

    def visitYield_expr(self, ctx: Python3Parser.Yield_exprContext):
        return super().visitYield_expr(ctx)

    def visitYield_arg(self, ctx: Python3Parser.Yield_argContext):
        return super().visitYield_arg(ctx)


def build_statements(statements):
    return ASTStatementsNode(statements[0], build_statements(statements[1:]) if len(statements) > 1 else None)


def build_expressions(expressions):
    return ASTExpressionsNode(expressions[0], build_expressions(expressions[1:]) if len(expressions) > 1 else None)


def build_assignments(assignments):
    return ASTAssignmentNode(assignments[0],
                             build_assignments(assignments[1:]) if len(assignments) > 1 else assignments[1])


def build_parameters(parameters):
    return ASTParametersNode(parameters[0], build_parameters(parameters[1:]) if len(parameters) > 1 else None)
