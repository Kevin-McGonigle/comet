import { combineReducers } from 'redux';
import treeReducer from './tree/tree';
import alertReducer from './alert/alert';
import userFilesReducer from './fileData/fileData';
import metricsReducer from './metrics/metrics';

const createRootReducer = () => {
    return combineReducers({
        tree: treeReducer,
        alert: alertReducer,
        files: userFilesReducer,
        metrics: metricsReducer,
    })
};

export default createRootReducer;