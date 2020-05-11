import metricReducer, { initialState, actions } from '../metrics';

const metricExample =   {
    "fileName": null,
    "structures": {
        "controlFlowGraph": null,
        "classDiagram": null,
        "inheritanceTree": null,
        "abstractSyntaxTree": null,
    },
    "metrics": {
        "dependencyGraph": null,
        "afferentCoupling": null,
        "efferentCoupling": null,
        "logicalLinesOfCode": null,
        "cyclomaticComplexity": null,
        "maximumInheritanceDepth": null,
        "maximumNestingDepth": null,
    }
}

test('SET_METRICS should set the state to expected value', () => {
    const reducedState = metricReducer(initialState, actions.setMetrics(metricExample));
    expect(reducedState).toEqual(metricExample);
});

