import {connect} from 'react-redux';
import DependencyGraphNode from './DependencyGraphNode';

const mapStateToProps = state => ({
    selectedFile: state.fileData.selected,
    metrics: state.metrics,
});

export const DependencyGraphNodeContainer = connect(mapStateToProps, null)(DependencyGraphNode);



