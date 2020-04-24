import React from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import styles from './Metrics.css';
import classnames from 'classnames';
import { FileDirectoryContainer } from '../general/FileDirectory/FileDirectoryContainer';

const cx = args => classnames(styles, args)

const Metrics = props => {
    return (
        <div className={cx("metricContainer")}>
            <FileDirectoryContainer />
        </div>
    )
};

const mapDispatchToProps = dispatch => bindActionCreators({}, dispatch);

export default connect(null, mapDispatchToProps)(Metrics);