import React from 'react';
import { Pane } from 'evergreen-ui';
import ClassDiagram from '../ClassDiagram/ClassDiagram';
import ForceDirectedGraph from './ForceDirectedGraph';
import { basicRelationshipData } from './configs';

const InheritanceTreeContainer = (props) => {
    const {
        data,
        title,
    } = props;

    return (
        <>
            <ForceDirectedGraph 
                data={basicRelationshipData} 
                graphType="basic"
                title={title}
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
