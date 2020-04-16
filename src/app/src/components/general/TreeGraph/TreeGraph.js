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
    name: '/src',
    children: [{
        name: 'A',
        children: [{
            name: 'B'
        }, {
            name: 'C',
            children: [{
                name: 'D',
            }]
        }]
    }]
};

const TreeGraph = props => {
    const {
        tree,
    } = props;

    console.log(shapeTreeGraphData(tree));
    const onClickHandler = (event) => {
        const nodeId = event.target.parentNode.id;
        // Set ClassDiagram 
        console.log(nodeId);
    };

    
    return (
        <Tree
            data={initialState}
            height={600}
            width={600}
            gProps={{
                onClick: onClickHandler
            }}
        />
    );
};

export default TreeGraph;