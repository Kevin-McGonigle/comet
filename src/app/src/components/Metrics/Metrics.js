import React, { useState } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import styles from './Metrics.css';
import classnames from 'classnames';
import Toolbar from '../general/Toolbar/Toolbar';
import MetricPaneContainer  from '../general/MetricPane/MetricPaneContainer';
import { FileDirectoryContainer } from '../general/FileDirectory/FileDirectoryContainer';
import AbstractSyntaxTree from '../general/Charts/AbstractSyntaxTree';
import { controlFlowGraphData, classDiagramData } from '../general/Charts/configs';
import ForceDirectedGraph from '../general/Charts/ForceDirectedGraph';
import TreeMapContainer from '../general/TreeMap/TreeMapContainer';

const cx = args => classnames(styles, args)

const Metrics = props => {
    const { selected, metrics } = props;

    const selectedMetrics = Object.values(metrics).filter(value => value.fileName === selected)[0]

    const [tabState, setTabState] = useState({
        selectedIndex: 0,
        tabs: ["TreeMap", "Metrics", "Class Diagram", "Inheritance Tree", "Abstract Syntax Tree", "Control Flow Diagram", "Dependency Graph"],
        tabContent: [
            <TreeMapContainer />,
            <MetricPaneContainer />, 
            <ForceDirectedGraph
                title="Class Diagram"
                data={classDiagramData}
                graphType="classDiagram"
            />,
            <ForceDirectedGraph
                title="Inheritance Tree"
                data={selectedMetrics.structures.inheritanceTree}
                graphType="static"
            />,
            <AbstractSyntaxTree />, 
            <ForceDirectedGraph 
                title="Control Flow Graph"
                data={controlFlowGraphData} 
                graphType="controlFlow"         
            />,
            <ForceDirectedGraph 
                title="Dependency Graph"
                data={selectedMetrics.structures.dependencyGraph} 
                graphType="controlFlow"         
            />
        ]
    });

    return (
        <>
            <FileDirectoryContainer />
            <div className={cx("metricContainer")}>
                <Toolbar tabState={tabState} setTabState={setTabState} />
                <div className={cx("metricTabContainer")}>
                    { tabState.tabContent[tabState.selectedIndex] }
                </div>
            </div>
        </>
    )
};

const mapDispatchToProps = dispatch => bindActionCreators({}, dispatch);

export default connect(null, mapDispatchToProps)(Metrics);