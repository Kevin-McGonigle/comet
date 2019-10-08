import React from 'react';
import TreeGraph from '../TreeGraph';
import initialState from '../../../../store/tree/tree';
import { shallow } from 'enzyme';
import "../../../../setupTests"

describe('TreeGraph', () => {
    test('Should render TreeGraph succesfully', () => { 
        const component = shallow(<TreeGraph tree={initialState} />);
        expect(component).toMatchSnapshot();
    });
    test('Should call hideAllChildNodes on node click', () => {
        const hideAllChildNodes = jest.fn();
        const component = shallow(<TreeGraph tree={initialState} hideAllChildNodes={hideAllChildNodes} />);
        const node = component.find('#TreeGraph.js');
        node.simulate('click');
        expect(hideAllChildNodes).toHaveBeenCalled();
    });
})
