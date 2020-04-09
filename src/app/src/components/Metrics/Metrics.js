import React, { useState } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import styles from './Metrics.css';
import classnames from 'classnames';
import { TreeGraphContainer } from '../general/TreeGraph/TreeGraphContainer';

const cx = args => classnames(styles, args)

const Metrics = props => {
    return (<TreeGraphContainer />)
};

const mapDispatchToProps = dispatch => bindActionCreators({}, dispatch);

export default connect(null, mapDispatchToProps)(Metrics);