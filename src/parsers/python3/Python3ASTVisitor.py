from python3.Python3Parser import Python3Parser
from python3.Python3Visitor import Python3Visitor
from tree import AST, Statements


class Python3ASTVisitor(Python3Visitor):
    def __init__(self) -> None:
        super().__init__()

    def visit(self, tree):
        return AST(super().visit(tree))

    def visitChildren(self, node):
        return super().visitChildren(node)

    def visitTerminal(self, node):
        super().visitTerminal(node)

    def visitErrorNode(self, node):
        super().visitErrorNode(node)

    def defaultResult(self):
        super().defaultResult()

    def aggregateResult(self, aggregate, next_result):
        return super().aggregateResult(aggregate, next_result)

    def shouldVisitNextChild(self, node, current_result):
        return super().shouldVisitNextChild(node, current_result)

    def visitSingle_input(self, ctx: Python3Parser.Single_inputContext):
        return super().visitSingle_input(ctx)

    def visitFile_input(self, ctx: Python3Parser.File_inputContext):
        return Statements(ctx.getChild(0).accept(self), ctx.getChild(1).accept(self))

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
        return super().visitExpr(ctx)

    def visitXor_expr(self, ctx: Python3Parser.Xor_exprContext):
        return super().visitXor_expr(ctx)

    def visitAnd_expr(self, ctx: Python3Parser.And_exprContext):
        return super().visitAnd_expr(ctx)

    def visitShift_expr(self, ctx: Python3Parser.Shift_exprContext):
        return super().visitShift_expr(ctx)

    def visitArith_expr(self, ctx: Python3Parser.Arith_exprContext):
        return super().visitArith_expr(ctx)

    def visitTerm(self, ctx: Python3Parser.TermContext):
        return super().visitTerm(ctx)

    def visitFactor(self, ctx: Python3Parser.FactorContext):
        return super().visitFactor(ctx)

    def visitPower(self, ctx: Python3Parser.PowerContext):
        return super().visitPower(ctx)

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
        return super().visitExprlist(ctx)

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
