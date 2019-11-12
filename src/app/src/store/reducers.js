import { combineReducers } from 'redux';
import treeReducer from './tree/tree';
import alertReducer from './alert/alert';

const createRootReducer = () => {
    return combineReducers({
        tree: treeReducer,
        alert: alertReducer,
    })
};

export default createRootReducer;