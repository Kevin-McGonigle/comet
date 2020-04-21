import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import TreeGraph from './TreeGraph';
import { actions as treeActions } from '../../../store/tree/tree';

const mapStateToProps = state => ({
    tree: state.metrics.inheritanceTree,
});

const mapDispatchToProps = dispatch => bindActionCreators(treeActions, dispatch);

export const TreeGraphContainer = connect(mapStateToProps, mapDispatchToProps)(TreeGraph);



