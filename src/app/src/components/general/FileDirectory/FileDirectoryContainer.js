import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import FileDirectory from './FileDirectory';
import { actions as fileActions } from '../../../store/fileData/fileData';

const mapStateToProps = state => ({
    files: state.files.files,
});

const mapDispatchToProps = dispatch => bindActionCreators(fileActions, dispatch);

export const FileDirectoryContainer = connect(mapStateToProps, mapDispatchToProps)(FileDirectory);



