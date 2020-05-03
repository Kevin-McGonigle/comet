import React from 'react';
import styles from './MetricPaneContainer.css';
import classnames from 'classnames';
import { Pane } from 'evergreen-ui';
import RadarGraph from '../Charts/RadarGraph';
import ForceDirectedGraph from '../Charts/ForceDirectedGraph';
import MetricPane from './MetricPane';

const cx = args => classnames(styles, args)

const metricInfo = {
    "Cyclomatic Complexity": {
        metricValue: 10,
        metricColour: "green"
    },
    "Logical Lines of Code": {
        metricValue: 10,
        metricColour: "orange"
    },
    "Lines of Comment": {
        metricValue: 10,
        metricColour: "green"
    },
    "Afferent Coupling": {
        metricValue: 10,
        metricColour: "green"
    },
    "Efferent Coupling": {
        metricValue: 10,
        metricColour: "red"
    },
    "Instability": {
        metricValue: 10,
        metricColour: "green"
    },
    "Method Cohesion": {
        metricValue: 10,
        metricColour: "red"
    },
    "Relational Cohesion": {
        metricValue: 10,
        metricColour: "green"
    },
    "Nesting Depth": {
        metricValue: 10,
        metricColour: "orange"
    }
}

const MetricPaneContainer = props => {
    return (
        <>
            <div className={cx("metricPaneContainer")}>
                <Pane
                    display="flex"
                    flexWrap="wrap"
                    background="tint2"
                    elevation={4}
                >
                    { Object.keys(metricInfo).map(metric => {
                        return (
                            <MetricPane 
                                key={metric}
                                metricName={metric}
                                metricValue={metricInfo[metric].metricValue}
                                metricColour={metricInfo[metric].metricColour}
                            />  
                        ) 
                    })}
                </Pane>      
            </div> 

            <div className={cx("overviewContainer")}>
                <Pane
                    display="flex"
                    flexDirection="column"
                    width="100%"
                    background="tint2"
                    elevation={4}
                >
                    <RadarGraph />
                </Pane>
            </div>
        </>
    )
};

export default MetricPaneContainer;
