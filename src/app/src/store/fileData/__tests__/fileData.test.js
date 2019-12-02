import fileDataReducer, { initialState, actions } from '../fileData';

test('should set the state to the expected value', () => {
    const reducedState = fileDataReducer(initialState, actions.setFileData({ test: 'test' }));
    expect(reducedState).toEqual({ initialData: { test: 'test' } });
});
