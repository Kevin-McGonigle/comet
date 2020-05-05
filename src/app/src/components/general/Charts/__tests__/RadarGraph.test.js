import React from 'react';
import RadarGraph from '../RadarGraph';
import { shallow } from 'enzyme';
import "../../../../setupTests"

test('should render RadarGraph as expected', () => { 
    const component = shallow(
        <RadarGraph />
    );
    expect(component.html()).toMatchSnapshot();
});
