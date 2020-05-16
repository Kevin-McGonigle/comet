import React from 'react';
import AbstractSyntaxTree from '../AbstractSyntaxTree';
import {shallow} from 'enzyme';
import "../../../../setupTests"

const AST = {
    name: "Statements",
    children: [
        {
            name: "if statement",
            children: [{
                name: "true"
            }, {
                name: "Pass statement",
                children: null
            }]
        }
    ]
}

test('should render ForceDirectedGraph as expected', () => {
    const component = shallow(
        <AbstractSyntaxTree
            data={AST}
        />
    );
    expect(component.html()).toMatchSnapshot();
});
