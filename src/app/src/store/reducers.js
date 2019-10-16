import { combineReducers } from 'redux';
import treeReducer from './tree/tree';

const createRootReducer = () => {
    return combineReducers({
        tree: treeReducer
    })
}

export default createRootReducer;