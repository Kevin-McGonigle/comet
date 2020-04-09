const initialState = {
    name: '/src',
    children: [{
        name: 'A',
        gProps: {
            className: 'class',
            id: 'A',
            'data-testid': 'TreeGraph.js'
        },
        children: [{
            name: 'B',
            gProps: {
                className: 'variable',
                id: 'B'
            },
            pathProps: {
                className: 'class-link'
            },
            children: [{
                name: 'C',
                gProps: {
                    className: 'variable',
                    id: 'C'
                },
                pathProps: {
                    className: 'class-link'
                }
            }, {
                name: 'D',
                gProps: {
                    className: 'variable',
                    id: 'D'
                },
                pathProps: {
                    className: 'class-link'
                }
            }]
        },]
    }, {
        name: 'E',
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