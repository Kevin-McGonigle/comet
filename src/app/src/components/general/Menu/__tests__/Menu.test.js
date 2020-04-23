import React from 'react';
import ToolbarMenu from '../Menu';
import { shallow } from 'enzyme';
import "../../../../setupTests"

test('should render ToolbarMenu succesfully', () => { 
    const component = shallow(<ToolbarMenu/>);
    expect(component.html()).toMatchSnapshot();
});

