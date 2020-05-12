import React from 'react';
import ForceDirectedGraph from '../ForceDirectedGraph';
import { dependencyGraphData } from '../configs';
import { shallow } from 'enzyme';
import "../../../../setupTests"

test('should render ForceDirectedGraph as expected', () => { 
    const component = shallow(
        <ForceDirectedGraph 
            title="Dependency Graph"
            data={dependencyGraphData} 
            graphType="dynamic"         
        />
    );
    expect(component.html()).toMatchSnapshot();
});
