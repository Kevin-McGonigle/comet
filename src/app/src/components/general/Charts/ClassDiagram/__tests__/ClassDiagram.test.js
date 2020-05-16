import React from 'react';
import ClassDiagram, {generateClassArgsText, generateFunctionText} from '../ClassDiagram';
import {shallow} from 'enzyme';
import "../../../../../setupTests"

const nodeData = {
    data: {
        id: "A",
        classArgs: {"Arg1": "String", "Arg2": "Int"},
        classFunctions: {
            "Function1": {
                arguments: {
                    "Arg1": "String",
                    "Arg2": "Int",
                },
                returnType: "String"
            }
        }
    }
}

test('should render ClassDiagram as expected', () => {
    const component = shallow(
        ClassDiagram(nodeData)
    );
    expect(component.html()).toMatchSnapshot();
});

test('should generate Class Argument information as expected', () => {
    const generatedInfo = generateClassArgsText(nodeData.data.classArgs);
    expect(generatedInfo[0].props.children).toEqual("+ Arg1 : String");
    expect(generatedInfo[1].props.children).toEqual("+ Arg2 : Int");
})


test('should generate Class Function information as expected', () => {
    const generatedInfo = generateFunctionText(nodeData.data.classFunctions);
    expect(generatedInfo).toStrictEqual(['+ Function1(Arg1 : String,Arg2 : Int) : String']);
})