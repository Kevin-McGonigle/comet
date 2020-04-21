const initialState = {
    name: '/src',
    children: [{
        name: 'A',
        children: [{
            name: 'B',
            children: [{
                name: 'C',
            }, {
                name: 'D',

            }]
        },]
    }, {
        name: 'E',
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