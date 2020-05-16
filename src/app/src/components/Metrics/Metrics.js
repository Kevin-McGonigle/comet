import React, {useState} from 'react';
import styles from './Metrics.css';
import classnames from 'classnames';
import Toolbar from '../general/Toolbar/Toolbar';
import { FileDirectoryContainer } from '../general/FileDirectory/FileDirectoryContainer';
import AbstractSyntaxTree from '../general/Charts/AbstractSyntaxTree';
import { classDiagramData } from '../general/Charts/configs';
import ForceDirectedGraph from '../general/Charts/ForceDirectedGraph';
import { useHistory } from 'react-router';

const cx = args => classnames(styles, args)


const tabMapping = {
    "ClassDiagram": "Class Diagram",
    "InheritanceTree": "Inheritance Tree",
    "AbstractSyntaxTree": "Abstract Syntax Tree",
    "ControlFlowDiagram": "Control Flow Diagram",
    "DependencyGraph": "Dependency Graph",
}

const Metrics = props => {
    const { fileDirectory, selected, metrics } = props;
    
    const history = useHistory();
    const selectedMetrics = Object.values(metrics).filter(value => value.fileName === selected)[0]

    if (selectedMetrics === null) {
        history.push('/');
    }

    const [tabState, setTabState] = useState({
        selectedIndex: 0,
        tabs: Object.values(tabMapping),
        tabContent: [
            <ForceDirectedGraph
                title="Class Diagram"
                data={classDiagramData}
                graphType="classDiagram"
            />,
            <ForceDirectedGraph
                title="Inheritance Tree"
                data={selectedMetrics.structures.inheritanceTree}
                graphType="dynamic"
            />,
            <AbstractSyntaxTree data={selectedMetrics.structures.abstractSyntaxTree}/>,
            <ForceDirectedGraph
                title="Control Flow Graph"
                data={selectedMetrics.structures.controlFlowGraph}
                graphType="dynamic"
            />,
            <ForceDirectedGraph
                title="Dependency Graph"
                data={selectedMetrics.structures.dependencyGraph}
                graphType="dependencyGraph"
            />
        ]
    });

    return (
        <>
            {fileDirectory && <FileDirectoryContainer/>}
            <div className={cx("metricContainer")}>
                <Toolbar tabMapping={tabMapping} tabState={tabState} setTabState={setTabState}/>
                <div className={cx("metricTabContainer")}>
                    {tabState.tabContent[tabState.selectedIndex]}
                </div>
            </div>
        </>
    )
};

export default Metrics;