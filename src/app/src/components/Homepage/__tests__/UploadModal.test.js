import React from 'react';
import { Provider } from 'react-redux'
import UploadModal, { removeFileFromUploadedFiles, readFile } from '../UploadModal';
import configureStore from 'redux-mock-store' 
import { mount } from 'enzyme';
import "../../../setupTests"

const historyMock = jest.mock('react-router-dom', () => {
    useHistory: () => ({
        push: jest.fn(),
    })
});

const initialState = {
    alert: {
        id: '',
        title: '',
        show: false,
        intent: 'none',
    },
    fileData: { selected: null, files: []},
}
const mockStore = configureStore(initialState);

test('Should render UploadModal succesfully', () => { 
    const component = mount(
        <Provider store={mockStore()}>
            <UploadModal 
                history={historyMock}
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
    });
});

test('removeFileFromUploadedFiles should return the expected value', () => { 
    const initial = [
        { name: 'name', fileType: '', size: '' }, 
        { name: 'name2', fileType: '', size: '' }
    ];
    const final = removeFileFromUploadedFiles(initial, 'name2');
    expect(final).toStrictEqual([{ name: 'name', fileType: '', size: '' }]);
});

