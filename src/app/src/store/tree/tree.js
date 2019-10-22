const initialState = {
    name: '/src',
    children: [{
        name: 'TreeGraph.js',
        gProps: {
            className: 'class',
            id: 'TreeGraph.js',
            'data-testid': 'TreeGraph.js'
        },
        children: [{
            name: 'arguments',
            gProps: {
                className: 'variable',
                id: 'arguments'
            },
            pathProps: {
                className: 'class-link'
            },
            children: [{
                name: 'Int arg1',
                gProps: {
                    className: 'variable',
                    id: 'Int arg1'
                },
                pathProps: {
                    className: 'variable-link'
                }
            }, {
                name: 'Int arg2',
                gProps: {
                    className: 'variable',
                    id: 'Int arg2'
                },
                pathProps: {
                    className: 'variable-link'
                }
            }]
        }, {
            name: 'functions',
            pathProps: {
                className: 'class-link'
            },
            children: [{
                name: 'square -> Int arg1, Int arg2'
            }, {
                name: 'sum -> Int arg1, Int arg2'
            }]
        }]
    }, {
        name: 'TreeGraph.css',
        gProps: {
            className: 'variable'
        }
    }]
};

export const HIDE_ALL_CHILD_NODES = 'HIDE_ALL_CHILD_NODES';

const treeReducer = (state = initialState, action) => {
    switch(action.type) {
        case HIDE_ALL_CHILD_NODES:
            const nodeId = action.payload.nodeId;
            return state;

        default:
            return state;
    }
};

export const actions = {
    hideAllChildNodes: (nodeId) => {
        return {
            type: HIDE_ALL_CHILD_NODES,
            payload: nodeId
        }
    }
};

export default treeReducer;