import {connect} from 'react-redux';
import Metrics from './Metrics';

const mapStateToProps = state => ({
    fileDirectory: true,
    selected: state.fileData.selected,
    metrics: state.metrics,
})

export const MetricsContainer = connect(mapStateToProps, null)(Metrics)



