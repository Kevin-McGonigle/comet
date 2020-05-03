import React, { useState } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import styles from './Metrics.css';
import classnames from 'classnames';
import Toolbar from '../general/Toolbar/Toolbar';
import MetricPaneContainer  from '../general/MetricPane/MetricPaneContainer';
import { FileDirectoryContainer } from '../general/FileDirectory/FileDirectoryContainer';
import AbstractSyntaxTree from '../general/Charts/AbstractSyntaxTree';
import InheritanceTreeContainer from '../general/Charts/InheritanceTreeContainer';
import { controlFlowGraphData, dependencyGraphData } from '../general/Charts/configs';
import ForceDirectedGraph from '../general/Charts/ForceDirectedGraph';

const cx = args => classnames(styles, args)

const Metrics = props => {
    const [tabState, setTabState] = useState({
        selectedIndex: 0,
        tabs: ["Metrics", "Inheritance Tree", "Abstract Syntax Tree", "Control Flow Diagram", "Dependency Graph"],
        tabContent: [
            <MetricPaneContainer />, 
            <InheritanceTreeContainer title="Inheritance Tree"/>,
            <AbstractSyntaxTree />, 
            <ForceDirectedGraph 
                title="Control Flow Graph"
                data={controlFlowGraphData} 
                graphType="controlFlow"         
            />,
            <ForceDirectedGraph 
                title="Dependency Graph"
                data={dependencyGraphData} 
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