import React from 'react';
import TreeGraph from '../TreeGraph/TreeGraph';
import { Pane } from 'evergreen-ui';

const AbstractSyntaxTree = props => {
    const { data } = props;
    
    return (
        <Pane
            display="flex"
            flexWrap="wrap"
            flexGrow={1}
            marginRight="10"
            background="tint2"
            elevation={4}   
        >
           <TreeGraph tree={data}/>
        </Pane>
    )
};

export default AbstractSyntaxTree;
