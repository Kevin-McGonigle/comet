import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import CreateModal from './CreateModal';
import { actions as alertActions } from '../../store/alert/alert';

const mapStateToProps = state => ({
    alertInfo: state.alert,
})

const mapDispatchToProps = dispatch => bindActionCreators(alertActions, dispatch)

export const CreateModalContainer = connect(mapStateToProps, mapDispatchToProps)(CreateModal)



