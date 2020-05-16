import React from 'react';
import styles from './TreeGraph.css';
import classnames from 'classnames';
import Tree from 'react-tree-graph';

const cx = args => classnames(styles, args);

const TreeGraph = props => {
    const {
        tree,
    } = props;

    return (
        <div className={cx('treeGraphContainer')}>
            <Tree
                data={tree}
                height={900}
                width={800}
                svgProps={{transform: 'rotate(90)'}}
            />
        </div>
    );
};

export default TreeGraph;