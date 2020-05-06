import React from 'react';
import TreeMapContainer from '../TreeMapContainer';
import { shallow } from 'enzyme';
import "../../../../setupTests"

test('Should render TreeMapContainer successfully', () => {
    const component = shallow(<TreeMapContainer />);
    expect(component.html()).toMatchSnapshot();
});
