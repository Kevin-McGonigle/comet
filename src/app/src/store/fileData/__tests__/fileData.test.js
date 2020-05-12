import fileDataReducer, { initialState, actions } from '../fileData';

test('should set the state to the expected value', () => {
    const reducedState = fileDataReducer(initialState, actions.setFileData([{name: "test"}]));
    expect(reducedState).toEqual({ selected: 'test', files: [{name: 'test'}]});
});

test('should set the selected to expected value', () => {
    const reducedState = fileDataReducer(initialState, actions.setSelectedFile('test'));
    expect(reducedState).toEqual({ selected: 'test', files: []});
});