export const initialState = {
    selected: null,
    files: [],
}

export const SET_FILE_DATA = 'SET_FILE_DATA';
export const SET_SELECTED_FILE = 'SET_SELECTED_FILE';


const fileDataReducer = (state = initialState, action) => {
    switch(action.type) {
        case SET_FILE_DATA:
            const files = action.payload;
            return {
                selected: files[0].name,
                files
            }
        case SET_SELECTED_FILE:
            const selectedFile = action.payload;
            return {
                ...state,
                selected: selectedFile,
            }
        default:
            return state;
    }
}

export const actions = {
    setFileData: (files) => {
        return {
            type: SET_FILE_DATA,
            payload: files,
        }
    },
    setSelectedFile: (fileName) => {
        return {
            type: SET_SELECTED_FILE,
            payload: fileName,
        }
    }
}

export default fileDataReducer;