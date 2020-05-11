import { combineReducers } from 'redux';
import alertReducer from './alert/alert';
import userFilesReducer from './fileData/fileData';
import metricsReducer from './metrics/metrics';

const createRootReducer = () => {
    return combineReducers({
        alert: alertReducer,
        fileData: userFilesReducer,
        metrics: metricsReducer,
    })
};

export default createRootReducer;