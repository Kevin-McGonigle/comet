import React from 'react';
import Toolbar from '../Toolbar';
import { shallow, mount } from 'enzyme';
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


test('should change to new tab on tab click succesfully', () => { 
    const tabState = {
        selectedIndex: 0,
        tabs: ["Tab", "Tab2"],
        tabContent: []
    };
    const tabMapping = {
        "Tab": "Tab",
        "Tab2": "Tab 2",
    }

    const setTabState = jest.fn();
    const component = mount(<Toolbar tabMapping={tabMapping} tabState={tabState} setTabState={setTabState}/>);
    const tabButton = component.find("#Tab2").first();
    tabButton.simulate('click');
    expect(setTabState).toHaveBeenCalled();
    expect(tabState.selectedIndex == 1);

});
