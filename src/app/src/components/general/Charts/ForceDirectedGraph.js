import React from 'react';
import { Graph } from 'react-d3-graph';
import { Pane } from 'evergreen-ui';
import { configMapping } from './configs';
import styles from './ForceDirectedGraph.css';
import classnames from 'classnames';

const cx = args => classnames(styles, args)

const ForceDirectedGraph = (props) => {
    const {
        data,
        graphType,
        title,
    } = props;

    const windowHeight = window.screen.height - 200;
    const windowWidth = window.screen.width - 350;
    const config = configMapping[graphType];
    config.height = windowHeight;
    config.width = windowWidth;

    return (
        <Pane
            display="flex"
            flexWrap="wrap"
            flexGrow={1}
            marginRight="10"
            background="tint2"
            elevation={4}   
        >
                        
            <div className={cx("title")}>{ title }<hr/></div>
            <Graph
                borderStyle="solid"
                id="graph-id"
                data={data}
                config={config}
            />
        </Pane>
    )
}

export default ForceDirectedGraph;
