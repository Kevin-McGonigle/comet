export const initialState = {
    id: 'none',
    show: 'false',
    title: 'Please place your code and filetype below',
    intent: 'none',
}

export const SET_ALERT_DANGER = 'SET_ALERT_DANGER';
export const SET_ALERT_SUCCESS = 'SET_ALERT_SUCCESS';
export const SET_ALERT_NONE = 'SET_ALERT_NONE';

const alertReducer = (state = initialState, action) => {
    switch(action.type) {
        case SET_ALERT_DANGER:
            return {
                id: 'dangerAlert',
                show: true,
                title: 'something dangerous',
                intent: 'danger',
            }
        case SET_ALERT_SUCCESS:
            return {
                id: 'successAlert',
                show: true,
                title: 'success',
                intent: 'success',
            }
        case SET_ALERT_NONE:
            return {
                id: 'none',
                show: false,
                title: 'Please place your code and filetype below',
                intent: 'none',
            }
        default:
            return state;
    }
}

export const actions = {
    setAlertSuccess: () => {
        return {
            type: SET_ALERT_SUCCESS,
        }
    },
    setAlertDanger: () => {
        return {
            type: SET_ALERT_DANGER,
        }
    },
    setAlertNone: () => {
        return {
            type: SET_ALERT_NONE,
        }
    },
}

export default alertReducer;