import React from 'react';
import Toolbar from '../Toolbar';
import { mount } from 'enzyme';
import "../../../../setupTests";

test('should render Toolbar succesfully', () => { 
    const component = mount(<Toolbar />);
    expect(component.html()).toMatchSnapshot();
});
