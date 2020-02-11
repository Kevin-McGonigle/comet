import React from 'react';
import UploadedItem from '../UploadedItem';
import { mount } from 'enzyme';

test('should render UploadedItem succesfully', () => { 
    const component = mount(
        <UploadedItem 
            name='name'
            fileType='file type'
            size='size'
            deleteOnClickHandler={() => {}}
       />);
    expect(component.html()).toMatchSnapshot();
});

test('should call deleteOnClickHandler on delete icon click', () => {
    const component = mount(
        <UploadedItem 
            name='name'
            fileType='file type'
            size='size'
            deleteOnClickHandler={jest.fn()}
        />
    );
    const deleteButton = component.find('#deleteIcon').first();
    deleteButton.simulate('click');
    expect(component.props().deleteOnClickHandler).toHaveBeenCalled();
});