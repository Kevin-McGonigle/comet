import React from 'react';
import MetricPaneContainer from '../MetricPaneContainer';
import { shallow } from 'enzyme';
import "../../../../setupTests"

test('should render MetricPaneContainer as expected', () => { 
    const component = shallow(<MetricPaneContainer />);
    expect(component.html()).toMatchSnapshot();
});

