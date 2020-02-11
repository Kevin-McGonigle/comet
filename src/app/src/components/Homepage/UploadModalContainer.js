import { connect } from 'react-redux';
import UploadModal from './UploadModal';
import { actions as alertActions } from '../../store/alert/alert';
import { actions as fileDataActions } from '../../store/fileData/fileData';

const mapStateToProps = state => ({
    alertInfo: state.alert,
    fileData: state.userFiles.initialData,
})

const mapDispatchToProps = (dispatch) => {
    return {
        setFileData: (data) => dispatch(fileDataActions.setFileData(data)),
        setAlertSuccess: () => dispatch(alertActions.setAlertSuccess()),
        setAlertError: () => dispatch(alertActions.setAlertError()),
        setAlertNone: () => dispatch(alertActions.setAlertNone()),
    }
};

export const UploadModalContainer = connect(mapStateToProps, mapDispatchToProps)(UploadModal)



