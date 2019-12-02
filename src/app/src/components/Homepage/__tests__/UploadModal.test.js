import React from 'react';
import { Provider } from 'react-redux'
import UploadModal, { removeFileFromUploadedFiles, readFile } from '../UploadModal';
import configureStore from 'redux-mock-store' 
import { mount } from 'enzyme';
import "../../../setupTests"

const initialState = {
    alert: {
        id: '',
        title: '',
        show: false,
        intent: 'none',
    },
    userFiles: { initialData: {} },
}
const mockStore = configureStore(initialState);

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

test('readFile should read a single file and returns its contents', () => { 
    const file = readFile(new File(["foojkhjkhkjhkhhj"], "foo.txt", {
        type: "text/plain",
      }));
    file.then(value => expect(value).toEqual("foojkhjkhkjhkhhj"));
});

test('readFile should read multiple files and returns their contents', () => { 
    const file = readFile([new File(["foojkhjkhkjhkhhj"], "foo.txt", {
        type: "text/plain",
      }), new File(["test"], "test.txt", {
        type: "text/plain",
      })]);
    file.then(value => expect(value).toEqual(["foojkhjkhkjhkhhj", "test"]));
});