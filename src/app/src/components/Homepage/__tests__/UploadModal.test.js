import React from 'react';
import { Provider } from 'react-redux'
import UploadModal from '../UploadModal';
import configureStore from 'redux-mock-store' 
import { mount } from 'enzyme';
import "../../../setupTests"

const initialState = {
    alert: {
        id: '',
        title: '',
        show: true,
        intent: '',
    }
}

const mockStore = configureStore(initialState)

test('Should render UploadModal succesfully', () => { 
    const component = mount(
        <Provider store={mockStore()}>
            <UploadModal 
                alertInfo={initialState.alert}
                uploadModal={{ isOpen: true, isLoading: false }}
                uploadModalOnConfirmHandler={jest.fn()}
                uploadModalOnCloseHandler={jest.fn()}
                setAlertSuccess={jest.fn()}
                setAlertDanger={jest.fn()}
            />
        </Provider>
    );
    expect(component.html()).toMatchSnapshot();
});

test('should render with specified alert information', () => {
    const success = { show: true, intent: 'success', title: 'success' };
    const warning = { show: true, intent: 'warning', title: 'warning' };
    const danger = { show: true, intent: 'danger', title: 'danger' };

    [success, warning, danger].forEach(alert => {
        const component = mount(
            <Provider store={mockStore()}>
                <UploadModal 
                    alertInfo={alert}
                    uploadModal={{ isOpen: true, isLoading: false}}
                    uploadModalOnConfirmHandler={jest.fn()}
                    uploadModalOnCloseHandler={jest.fn()}
                    setAlertSuccess={jest.fn()}
                    setAlertDanger={jest.fn()}
                />
            </Provider>
        );
        expect(component.html()).toMatchSnapshot();
    })
});
