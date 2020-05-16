import React from 'react';
import {Provider} from 'react-redux'
import Metrics from '../Metrics';
import {shallow} from 'enzyme';
import configureStore from 'redux-mock-store'
import "../../../setupTests"


const state = {
    fileData: {
        selected: 'file',
        files: [{"file": {"name": "file"}}]
    },
    metrics: [
        {
            "fileName": "file",
            "structures": {
                "controlFlowGraph": null,
                "classDiagram": null,
                "inheritanceTree": null,
                "abstractSyntaxTree": null,
            },
            "metrics": {
                "dependencyGraph": null,
                "afferentCoupling": null,
                "efferentCoupling": null,
                "logicalLinesOfCode": null,
                "cyclomaticComplexity": null,
                "maximumInheritanceDepth": null,
                "maximumNestingDepth": null,
            }
        }
    ]
}
const mockStore = configureStore(state);

test('Should render Metrics successfully', () => {
    const component = shallow(
        <Provider store={mockStore()}>
            <Metrics fileDirectory={false} selected={state.fileData.selected} metrics={state.metrics}/>
        </Provider>
    )
    expect(component.html()).toMatchSnapshot()
})
