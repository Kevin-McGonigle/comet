import React from 'react';
import { Provider } from 'react-redux'
import configureStore from 'redux-mock-store' 
import Homepage from '../Homepage';
import { shallow, mount } from 'enzyme';
import "../../../setupTests"

jest.mock('react-router-dom', () => ({
    useHistory: () => ({
      push: jest.fn(),
    }),
}));

const initialState = {
    alert: {
        id: 'something',
        title: 'something',
        show: 'something',
        intent: 'something',
    },
    fileData: { selected: null, files: []},
};
const mockStore = configureStore(initialState);

test('should render Homepage succesfully', () => { 
    const store = mockStore(initialState);
    const component = shallow(<Provider store={store}><Homepage/></Provider>);
    expect(component.html()).toMatchSnapshot();
});

test('render should contain all div items specified', () => {
    const divs = ['homepageContainer', 'logoContainer', 'logo', 'createButton', 'uploadButton'];
    const store = mockStore(initialState);
    const component = mount(<Provider store={store}><Homepage/></Provider>);

    divs.forEach(divName => {
        const foundBool = component.find(`.${divName}`) || component.find(`#${divName}`)
        expect(foundBool.first().props().className);
    })
});