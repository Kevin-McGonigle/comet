import React from 'react';
import Toolbar from '../Toolbar';
import { shallow } from 'enzyme';
import "../../../../setupTests";

test('should render Toolbar succesfully', () => { 
    const tabState= {
        selectedIndex: 0,
        tabs: ["Metrics", "Inheritance Tree", "Abstract Syntax Tree", "Control Flow Diagram", "Dependency Graph"],
        tabContent: []
    };
    const setTabState = jest.fn();
    const component = shallow(<Toolbar tabState={tabState} setTabState={setTabState}/>);
    expect(component.html()).toMatchSnapshot();
});
