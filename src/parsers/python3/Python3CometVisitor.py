from astree import *
from cfgraph import CFG, CFGNode
from comet_visitor import CometResult, CometNodeResult
from python3.Python3Parser import Python3Parser
from python3.Python3Visitor import Python3Visitor

binary_operators = {
    "|": "BITWISE_OR",
    "^": "BITWISE_XOR",
    "&": "BITWISE_AND",
    "<<": "LEFT_SHIFT",
    ">>": "RIGHT_SHIFT",
    "+": "ADD",
    "-": "SUBTRACT",
    "*": "MULTIPLY",
    "@": "MATRIX_MULTIPLY",
    "%": "MODULO",
    "//": "FLOOR_DIVIDE",
    "**": "POWER",
}

unary_operators = {
    "+": "POSITIVE",
    "-": "ARITH_NEGATION",
    "~": "BITWISE_INVERSION",
}

logical_operators = {
    "and": "AND",
    "or": "OR",
    "not": "NOT"
}

comparison_operators = {
    "<": "LESS_THAN",
    ">": "GREATER_THAN",
    "==": "EQUAL",
    ">=": "GREATER_THAN_OR_EQUAL",
    "<=": "LESS_THAN_OR_EQUAL",
    "!=": "NOT_EQUAL",
    "<>": "NOT_EQUAL",
    "in": "IN",
    "is": "IS"
}


def r_ast_bin_op(children):
    if not children:
        return None

    if isinstance(children[-1], ASTNode) or isinstance(children[-1], str):
        if len(children) == 1:
            return children[0]
        return ASTBinOpNode(binary_operators[children[-2]], r_ast_bin_op(children[:-2]), children[-1])

    raise ValueError(f"Invalid children list: {children}")


class Python3CometVisitor(Python3Visitor):
    # Overrides
    def __init__(self) -> None:
        super().__init__()

    # Behaviour
    def visit(self, tree):
        node_result = super().visit(tree)
        ast = AST(node_result.ast_node)
        print(ast)
        cfg = CFG(node_result.cfg_node)

        return CometResult(ast, cfg)

    def visitChildren(self, node):
        result = []
        for i in range(node.getChildCount()):
            if not self.shouldVisitNextChild(node, result):
                return result

            result = self.aggregateResult(result, node.getChild(i).accept(self))

        return result

    def visitTerminal(self, node):
        return node.getText()

    def visitErrorNode(self, node):
        super().visitErrorNode(node)

    def defaultResult(self):
        return CometNodeResult(None, None)

    def aggregateResult(self, aggregate, next_result):
        if next_result:
            if isinstance(next_result, list):
                return aggregate + next_result
            return aggregate + [next_result]

    def shouldVisitNextChild(self, node, current_result):
        return super().shouldVisitNextChild(node, current_result)

    # Utilities
    def ast_children(self, ctx):
        return [child.ast_node if isinstance(child, CometNodeResult) else child for child in self.visitChildren(ctx)]

    def ast_bin_op(self, ctx):
        return r_ast_bin_op(self.ast_children(ctx))

    def ast_un_op(self, ctx):
        children = self.ast_children(ctx)
        return ASTUnOpNode(unary_operators[children[0]], children[1])

    # Visits
    def visitSingle_input(self, ctx: Python3Parser.Single_inputContext):
        return super().visitSingle_input(ctx)

    def visitFile_input(self, ctx: Python3Parser.File_inputContext):
        return CometNodeResult(ASTStatementsNode(self.ast_children(ctx)), None)

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
        return super().visitFuncdef(ctx)

    def visitParameters(self, ctx: Python3Parser.ParametersContext):
        return super().visitParameters(ctx)

    def visitTypedargslist(self, ctx: Python3Parser.TypedargslistContext):
        return super().visitTypedargslist(ctx)

    def visitTfpdef(self, ctx: Python3Parser.TfpdefContext):
        return super().visitTfpdef(ctx)

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
        return super().visitExpr_stmt(ctx)

    def visitAnnassign(self, ctx: Python3Parser.AnnassignContext):
        return super().visitAnnassign(ctx)

    def visitTestlist_star_expr(self, ctx: Python3Parser.Testlist_star_exprContext):
        return super().visitTestlist_star_expr(ctx)

    def visitAugassign(self, ctx: Python3Parser.AugassignContext):
        return super().visitAugassign(ctx)

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
        children = self.visitChildren(ctx)
        success = super().visitIf_stmt(ctx).cfg_node
        if success is None:
            success = CFGNode()

        if_node = CFGNode()
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
        return CometNodeResult(self.ast_bin_op(ctx), None)

    def visitXor_expr(self, ctx: Python3Parser.Xor_exprContext):
        return CometNodeResult(self.ast_bin_op(ctx), None)

    def visitAnd_expr(self, ctx: Python3Parser.And_exprContext):
        return CometNodeResult(self.ast_bin_op(ctx), None)

    def visitShift_expr(self, ctx: Python3Parser.Shift_exprContext):
        return CometNodeResult(self.ast_bin_op(ctx), None)

    def visitArith_expr(self, ctx: Python3Parser.Arith_exprContext):
        return CometNodeResult(self.ast_bin_op(ctx), None)

    def visitTerm(self, ctx: Python3Parser.TermContext):
        return CometNodeResult(self.ast_bin_op(ctx), None)

    def visitFactor(self, ctx: Python3Parser.FactorContext):
        if ctx.getChildCount() == 2:
            return CometNodeResult(self.ast_un_op(ctx), None)
        return super().visitFactor(ctx)

    def visitPower(self, ctx: Python3Parser.PowerContext):
        return CometNodeResult(self.ast_bin_op(ctx), None)

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
        return ASTExpressionsNode(self.visitChildren(ctx))

    def visitTestlist(self, ctx: Python3Parser.TestlistContext):
        return super().visitTestlist(ctx)

    def visitDictorsetmaker(self, ctx: Python3Parser.DictorsetmakerContext):
        return super().visitDictorsetmaker(ctx)

    def visitClassdef(self, ctx: Python3Parser.ClassdefContext):
        return super().visitClassdef(ctx)

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
