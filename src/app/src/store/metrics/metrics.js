const initialState = {
    hash: {},
    inheritanceTree: {},
};

export const SET_INHERITANCE_TREE = 'SET_INHERITANCE_TREE';

const metricsReducer = (state = initialState, action) => {
    switch(action.type) {
        case SET_INHERITANCE_TREE:
            const { hash, inheritance_tree } = action.payload;
            return {
                inheritance_tree,
                hash,
                ...state.metrics,
            }

        default:
            return state;
    }
};

export const actions = {
    setInheritanceTree: (data) => {
        return {
            type: SET_INHERITANCE_TREE,
            payload: data
        }
    }
};

export default metricsReducer;