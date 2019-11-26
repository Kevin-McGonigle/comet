import React from 'react';
import styles from './UploadModal.css';
import classnames from 'classnames';
import { FilePicker, Alert, Dialog } from 'evergreen-ui';
import UploadedItem from './UploadedItem';

const cx = args => classnames(styles, args)

const readFileContent = files => {
    // #TODO: read file/s content/s
    console.log(files);
}

const UploadModal = props => {
    const {
        alertInfo,
        uploadModal,
        uploadedFiles,
        setUploadedFiles,
        uploadModalOnConfirmHandler,
        uploadModalOnCloseHandler,
        setAlertSuccess,
        setAlertDanger,
    } = props;

    const createFileItem = (file) => {
        return (
            <UploadedItem 
                name={file.name}
                size={file.size}
                fileType={file.type}
                uploadedFiles={uploadedFiles}
                setUploadedFiles={setUploadedFiles}
            />
            )
    }

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
       
    const onChangeHandler = (files) => {
        const currentFiles = Object.values(files).reduce((acc, file) => {
            acc.push({
                name: file.name,
                size: file.size,
                type: file.type,
            });
            return acc;
        }, []);
        setUploadedFiles(currentFiles);
        setAlertSuccess();
    }

    return (
            <Dialog
                isShown={uploadModal.isOpen}
                title="Upload"
                isConfirmLoading={uploadModal.isLoading}
                confirmLabel={uploadModal.isLoading ? "Uploading.." : 'Upload'}
                onConfirm={uploadModalOnConfirmHandler}
                onCloseComplete={uploadModalOnCloseHandler}
            >
                <div className={cx('uploadModalContainer')}>
                    <div className={cx('filePicker')}>
                        { createAlert() }
                        <FilePicker
                            id='filePicker'
                            multiple
                            width={'100%'}
                            height={24}
                            onChange={onChangeHandler}
                            placeholder={uploadedFiles && "Choose file or folder" || `${uploadedFiles.length} file/s`}
                        />
                    </div>

                    {uploadedFiles && (
                        <div className={cx('fileListContainer')} > 
                                { uploadedFiles.map(file => createFileItem(file)) }
                            </div>
                    )}
                </div>
            </Dialog>
    );
};

export default UploadModal;