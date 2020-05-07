const initialState = [
    {
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
];

export const SET_METRICS = 'SET_METRICS';

const metricsReducer = (state = initialState, action) => {
    switch(action.type) {
        case SET_METRICS:
            const metrics = state;
            metrics.push(action.payload);
            return {
                ...metrics,
            }

        default:
            return state;
    }
};

export const actions = {
    setMetrics: (data) => {
        return {
            type: SET_METRICS,
            payload: data
        }
    }
};

export default metricsReducer;