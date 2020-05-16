export const initialState = [];

export const SET_METRICS = 'SET_METRICS';
export const ADD_TO_METRICS = 'ADD_TO_METRICS';

const metricsReducer = (state = initialState, action) => {
    switch (action.type) {
        case SET_METRICS:
            return {
                ...action.payload,
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
    },
};

export default metricsReducer;