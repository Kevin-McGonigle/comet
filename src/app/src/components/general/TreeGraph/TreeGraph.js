import React from 'react';
import styles from './TreeGraph.css';
import classnames from 'classnames';
import Tree from 'react-tree-graph';

const cx = args => classnames(styles, args);

const shapeTreeGraphData = (fileName, data) => {
    let treeGraph = {
        name: fileName,
        children: [],
    };
}

// { A: ['B', 'C'], B: [], C: ['D']}

const initialState = {
    name: 'WHILE',
    children: [{
        name: 'LESS',
        children: [{
            name: 'VARIABLE',
            children: [{ name: "x" }],
        },
        { 
            name: "CONST",
            children: [{ name: 20 }]
        }],
        name: 'ASSIGN',
        children: [{
            name: 'VARIABLE',
            children: [{ name: 'X' },
        {
            name: "PLUS",
            children: [{
                name: "VARIABLE",
                children: [{
                    name: "X"
                }, 
                {
                name: "TIMES",
                children: [{
                    name: "VARIABLE",
                    children: [{
                        name: "Y"
                    }, 
                    {
                    name: "CONST",
                    children: [{
                        name: "2"
                    }]
                    }]
                }]    
                }]
            }]
        }],
        }]
    }]
};

const TreeGraph = props => {
    const {
        tree,
    } = props;

    return (
        <div className={cx('treeGraphContainer')}>
            <Tree
                data={initialState}
                height={900}
                width={800}
                svgProps={{ transform: 'rotate(90)'}}
            />
        </div>
    );
};

export default TreeGraph;