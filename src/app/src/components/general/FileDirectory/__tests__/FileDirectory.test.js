import React from 'react';
import FileDirectory from '../FileDirectory';
import { shallow, mount } from 'enzyme';
import "../../../../setupTests"

const fileNames = ["FileName1.py", "FileName2.py"];

test('should render FileDirectory succesfully', () => { 
    const component = shallow(<FileDirectory fileNames={fileNames}/>);
    expect(component.html()).toMatchSnapshot();
});

test('should call setSelectedFile upon itemFile click', () => { 
    const setSelectedFile = jest.fn();
    const component = shallow(<FileDirectory fileNames={fileNames} setSelectedFile={setSelectedFile}/>);
    const button = component.find({ id: 'FileName2.py' }).parent();
    button.simulate('click', { currentTarget: { textContent: "FileName2.py" }});
    expect(setSelectedFile).toHaveBeenCalled();
});

