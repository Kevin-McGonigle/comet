import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import TreeGraph from './TreeGraph';
// import { selectors as treeSelectors } from '../../store/tree/selectors';
import { actions as treeActions } from '../../../store/tree/tree';

const mapStateToProps = state => ({
    tree: state.tree,
})

const mapDispatchToProps = dispatch => bindActionCreators(treeActions, dispatch)


export const TreeGraphContainer = connect(mapStateToProps, mapDispatchToProps)(TreeGraph)



