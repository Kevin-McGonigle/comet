import React from 'react';
import {Provider} from 'react-redux'
import CreateModal from '../CreateModal';
import configureStore from 'redux-mock-store'
import {mount} from 'enzyme';
import "../../../setupTests"

const initialState = {
    alert: {
        id: 'successAlert',
        title: "Please place your code and file type below",
        show: 'none',
        intent: 'none',
    }
}

const mockStore = configureStore(initialState);

test('should render CreateModal successfully', () => {
    const component = mount(
        <Provider store={mockStore()}>
            <CreateModal
                alertInfo={{show: 'none', intent: 'none', title: 'none'}}
                createModal={{isOpen: true, isLoading: false}}
                createModalOnConfirmHandler={jest.fn()}
                createModalOnCloseHandler={jest.fn()}
                setAlertSuccess={jest.fn()}
                setAlertDanger={jest.fn()}
            />
        </Provider>
    );
    expect(component.html()).toMatchSnapshot();
});

test('should render with alert when alertInfo is passed', () => {
    const success = {show: true, intent: 'success', title: 'success'};
    const warning = {show: true, intent: 'warning', title: 'warning'};
    const danger = {show: true, intent: 'danger', title: 'danger'};

    [success, warning, danger].forEach(alert => {
        const component = mount(
            <Provider store={mockStore()}>
                <CreateModal
                    alertInfo={alert}
                    createModal={{isOpen: true, isLoading: false}}
                    createModalOnConfirmHandler={jest.fn()}
                    createModalOnCloseHandler={jest.fn()}
                    setAlertSuccess={jest.fn()}
                    setAlertDanger={jest.fn()}
                    setTextArea={jest.fn()}
                />
            </Provider>
        );
        const alertDiv = component.find(`#${alert.intent}Alert`).first();
        const props = alertDiv.props();

        expect(props.id).toEqual(`${alert.intent}Alert`);
        expect(props.intent).toEqual(alert.intent);
        expect(props.title).toEqual(alert.title);
        expect(alertDiv.html()).toMatchSnapshot();
    })
});

test('should open create file dialog on plus icon click', () => {
    const component = mount(
        <Provider store={mockStore()}>
            <CreateModal
                alertInfo={{show: 'none', intent: 'none', title: 'none'}}
                createModal={{isOpen: true, isLoading: false}}
                createModalOnConfirmHandler={jest.fn()}
                createModalOnCloseHandler={jest.fn()}
                setAlertSuccess={jest.fn()}
                setAlertDanger={jest.fn()}
            />
        </Provider>
    );
    const plusButton = component.find('#plus').first();
    plusButton.simulate('click');
    expect(component.html()).toMatchSnapshot();
});