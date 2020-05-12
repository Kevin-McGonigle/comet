import { connect } from 'react-redux';
import CreateModal from './CreateModal';
import { actions as alertActions } from '../../store/alert/alert';
import { actions as metricsActions } from '../../store/metrics/metrics';
import { actions as fileDataActions } from '../../store/fileData/fileData';

const mapStateToProps = state => ({
    alertInfo: state.alert,
})

const mapDispatchToProps = (dispatch) => {        
    return {
        setMetrics: (metrics) => dispatch(metricsActions.setMetrics(metrics)),
        setFileData: (data) => dispatch(fileDataActions.setFileData(data)),
        setAlertSuccess: (text) => dispatch(alertActions.setAlertSuccess(text)),
        setAlertDanger: (text) => dispatch(alertActions.setAlertDanger(text)),
        setAlertNone: () => dispatch(alertActions.setAlertNone())
    }
}

export const CreateModalContainer = connect(mapStateToProps, mapDispatchToProps)(CreateModal)



