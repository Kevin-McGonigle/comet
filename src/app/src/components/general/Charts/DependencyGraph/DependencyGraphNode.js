import React from 'react';
import styles from './DependencyGraphNode.css';
import classnames from 'classnames';
import {Pane, Popover} from 'evergreen-ui';

const cx = args => classnames(styles, args)

function DependencyGraphNode(props) {
    const {
        data,
        selectedFile,
        metrics,
    } = props;

    const nodeId = data.id;
    const selectedMetrics = Object.values(metrics).filter(value => value.fileName === selectedFile)[0]
    const afferentCoupling = selectedMetrics.metrics.afferentCoupling.filter(item => item.name === nodeId)[0];
    const efferentCoupling = selectedMetrics.metrics.efferentCoupling.filter(item => item.name === nodeId)[0];
    const instability = efferentCoupling.value / (efferentCoupling.value + afferentCoupling.value);

    return (
        <Popover
            content={
                <Pane
                    width={400}
                    height={200}
                    display="flex"
                    alignItems="center"
                    justifyContent="center"
                    flexDirection="column"
                >
                    <div className={cx('dependencyGraphNode')} id="box">
                        <div className={cx('nodeItem')}>Afferent Coupling: {afferentCoupling.value}</div>
                        <div className={cx('nodeItem')}>Efferent Coupling: {efferentCoupling.value}</div>
                        <div className={cx('nodeItem')}>Instability: {instability}</div>
                    </div>
                </Pane>
            }>
            <Pane
                width={50}
                height={50}
                display="flex"
                alignItems="center"
                justifyContent="center"
                backgroundColor="#3498db"
            >
                {nodeId}
            </Pane>
        </Popover>
    )
}

export default DependencyGraphNode;
