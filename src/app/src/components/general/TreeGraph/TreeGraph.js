import React from 'react';
import styles from './TreeGraph.css';
import classnames from 'classnames';
import Tree from 'react-tree-graph';

const cx = args => classnames(styles, args);

const TreeGraph = props => {
    const {
        tree,
        hideAllChildNodes,
    } = props;

    const onClickHandler = (event) => {
        const nodeId = event.target.parentNode.id;
        hideAllChildNodes(nodeId); // need to recursively hide all childNodes
    };

    const treeWithOnClickHandler = {
        ...tree,
        children: tree.children.reduce((acc, child) => {
            acc.push({
                ...child,
                gProps: {
                    onClick: onClickHandler,
                    ...child.gProps,
                }
            });
            return acc;
        }, [])
    };

    return (
        <Tree
            data={treeWithOnClickHandler}
            height={600}
            width={600}
            gProps={{
                onClick: onClickHandler
            }}
        />
    );
};

export default TreeGraph;