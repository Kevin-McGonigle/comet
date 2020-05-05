import React from 'react';
import InheritanceTreeContainer from '../InheritanceTreeContainer';
import { shallow } from 'enzyme';
import "../../../../setupTests"

test('should render ForceDirectedGraph as expected', () => { 
    const component = shallow(
        <InheritanceTreeContainer title="test" />
    );
    expect(component.html()).toMatchSnapshot();
});
