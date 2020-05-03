import React from 'react';
import { Pane } from 'evergreen-ui';
import ClassDiagram from '../ClassDiagram/ClassDiagram';
import ForceDirectedGraph from './ForceDirectedGraph';
import styles from './ForceDirectedGraph.css';
import classnames from 'classnames';
import { basicRelationshipData } from './configs';

const cx = args => classnames(styles, args)

const InheritanceTreeContainer = (props) => {
    const {
        data,
        title,
        info,
    } = props;

    return (
        <>
            <ForceDirectedGraph 
                data={basicRelationshipData} 
                graphType="basic"
                title={title}
                info={info} 
            />
            <Pane
                display="flex"
                flexWrap="wrap"
                alignItems="center"
                flexGrow={1}
                marginRight="10"
                background="tint2"
                elevation={4}   
                zIndex={-1}
                justifyContent="center"
            >
                <ClassDiagram />
            </Pane>
        </>
    )
}

export default InheritanceTreeContainer;
