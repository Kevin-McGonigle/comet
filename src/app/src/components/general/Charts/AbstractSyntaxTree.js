import React from 'react';
import { TreeGraphContainer } from '../TreeGraph/TreeGraphContainer';
import styles from './AbstractSyntaxTree.css';
import classnames from 'classnames';
import { Pane } from 'evergreen-ui';

const cx = args => classnames(styles, args)

const AbstractSyntaxTree = props => {
    return (
        <Pane
            display="flex"
            flexWrap="wrap"
            flexGrow={1}
            marginRight="10"
            background="tint2"
            elevation={4}   
        >
           <TreeGraphContainer />
        </Pane>
    )
};

export default AbstractSyntaxTree;
