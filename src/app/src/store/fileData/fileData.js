export const initialState = {
    initialData: {},
}

export const SET_FILE_DATA = 'SET_FILE_DATA';

const fileDataReducer = (state = initialState, action) => {
    switch(action.type) {
        case SET_FILE_DATA:
            return {
                initialData: action.payload,
            }
        default:
            return state;
    }
}

export const actions = {
    setFileData: (data) => {
        return {
            type: SET_FILE_DATA,
            payload: data,
        }
    },
}

export default fileDataReducer;