import React from 'react';
import TreeGraph from '../TreeGraph';
import { mount } from 'enzyme';
import "../../../../setupTests"

const initialState = {
    name: '/src',
    children: [{
        name: 'TreeGraph.js',
        gProps: {
            className: 'class',
            id: 'TreeGraph.js'
        },
        children: [{
            name: 'arguments',
            gProps: {
                className: 'variable',
                id: 'arguments'
            },
            pathProps: {
                className: 'class-link'
            },
            children: [{
                name: 'Int arg1',
                gProps: {
                    className: 'variable',
                    id: 'Int arg1'
                },
                pathProps: {
                    className: 'variable-link'
                }
            }, {
                name: 'Int arg2',
                gProps: {
                    className: 'variable',
                    id: 'Int arg2'
                },
                pathProps: {
                    className: 'variable-link'
                }
            }]
        }, {
            name: 'functions',
            pathProps: {
                className: 'class-link'
            },
            children: [{
                name: 'square -> Int arg1, Int arg2'
            }, {
                name: 'sum -> Int arg1, Int arg2'
            }]
        }]
    }, {
        name: 'TreeGraph.css',
        gProps: {
            className: 'variable'
        }
    }]
}

test('Should render TreeGraph succesfully', () => { 
    const component = mount(<TreeGraph tree={initialState} />);
    expect(component.html()).toMatchSnapshot();
});
