import alertReducer, { initialState, actions } from '../alert';

test('should change state to dangerAlert info on SET_ALERT_DANGER', () => {
    const reducedState = alertReducer(initialState, actions.setAlertDanger('Upload error'));
    expect(reducedState).toEqual({
        id: 'dangerAlert',
        show: true,
        title: 'Upload error',
        intent: 'danger',
    });
});

test('should change state to successAlert info on SET_ALERT_SUCCESS', () => {
    const reducedState = alertReducer(initialState, actions.setAlertSuccess('Upload success'));
    expect(reducedState).toEqual({
        id: 'successAlert',
        show: true,
        title: 'Upload success',
        intent: 'success',
    });
});

test('should change state to none on SET_ALERT_NONE', () => {
    const reducedState = alertReducer(initialState, actions.setAlertNone(initialState));
    expect(reducedState).toEqual({
        id: 'none',
        show: false,
        title: "Please place your code and filetype below",
        intent: 'none',
    });
});