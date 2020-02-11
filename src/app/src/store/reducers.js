import { combineReducers } from 'redux';
import treeReducer from './tree/tree';
import alertReducer from './alert/alert';
import userFilesReducer from './fileData/fileData';

const createRootReducer = () => {
    return combineReducers({
        tree: treeReducer,
        alert: alertReducer,
        userFiles: userFilesReducer,
    })
};

export default createRootReducer;