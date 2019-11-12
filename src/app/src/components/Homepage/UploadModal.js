import React from 'react';
import styles from './UploadModal.css';
import classnames from 'classnames';
import { FilePicker, Alert, Dialog } from 'evergreen-ui';

const cx = args => classnames(styles, args)

const readFileContent = files => {
    // #TODO: read file/s content/s
    console.log(files);
}

const UploadModal = props => {
    const {
        alertInfo,
        uploadModal,
        uploadModalOnConfirmHandler,
        uploadModalOnCloseHandler,
        setAlertSuccess,
        setAlertDanger,
    } = props;
    const onChangeHandler = (files) => readFileContent(files);

    const createAlert = () => {
        if (alertInfo.show){
            return (
                <Alert 
                    id={`${alertInfo.intent}Alert`}
                    intent={alertInfo.intent}
                    title={alertInfo.title}
                    hasIcon
                    marginTop={2}
                    marginBottom={8}
                />
            );
        }
    }

    return (
            <Dialog
                isShown={uploadModal.isOpen}
                title="Upload"
                onConfirm={uploadModalOnConfirmHandler}
                isConfirmLoading={uploadModal.isLoading}
                confirmLabel={uploadModal.isLoading ? "Uploading.." : 'Upload'}
                onCloseComplete={uploadModalOnCloseHandler}
                >
                <div className={cx('uploadModalContainer')}>
                    <div className={cx('filePicker')}>
                    { createAlert() }
                        <FilePicker
                            id='filePicker'
                            multiple
                            width={350}
                            height={24}
                            onChange={onChangeHandler}
                            placeholder="Choose file or folder"
                        />
                    </div>
                </div>
            </Dialog>
    );
};

export default UploadModal;