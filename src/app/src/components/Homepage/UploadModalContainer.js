import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import UploadModal from './UploadModal';
import { actions as alertActions } from '../../store/alert/alert';

const mapStateToProps = state => ({
    alertInfo: state.alert,
})

const mapDispatchToProps = dispatch => bindActionCreators(alertActions, dispatch)

export const UploadModalContainer = connect(mapStateToProps, mapDispatchToProps)(UploadModal)



