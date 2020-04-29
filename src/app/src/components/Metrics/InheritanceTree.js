import React from 'react';
import { TreeGraphContainer } from '../general/TreeGraph/TreeGraphContainer';
import ClassDiagram from '../general/ClassDiagram/ClassDiagram';
import styles from './InheritanceTree.css';
import classnames from 'classnames';

const cx = args => classnames(styles, args)

const InheritanceTree = props => {
    return (
       <div className={cx('inheritanceTreeContainer')}>
           <TreeGraphContainer />
           <ClassDiagram />
       </div>
    )
};

export default InheritanceTree;
