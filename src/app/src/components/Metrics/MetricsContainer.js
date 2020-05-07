import { connect } from 'react-redux';
import Metrics from './Metrics';

const mapStateToProps = state => ({
    selected: state.fileData.selected,
    metrics: state.metrics,
    fileData: state.fileData.files,
})

export const MetricsContainer = connect(mapStateToProps, null)(Metrics)



