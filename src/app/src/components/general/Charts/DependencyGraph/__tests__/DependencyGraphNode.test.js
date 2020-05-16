import React from 'react';
import DependencyGraphNode from '../DependencyGraphNode';
import {shallow} from 'enzyme';
import "../../../../../setupTests"

test('should render DependencyGraphNode as expected', () => {
    const component = shallow(
        <DependencyGraphNode
            data={{id: "file"}}
            selectedFile="file"
            metrics={[{
                fileName: "file",
                metrics: {
                    afferentCoupling: [{name: "file", value: 1}],
                    efferentCoupling: [{name: "file", value: 1}],
                }
            }
            ]}
        />
    );
    expect(component.html()).toMatchSnapshot();
});
