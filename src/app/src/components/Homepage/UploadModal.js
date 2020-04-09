import React from 'react';
import styles from './UploadModal.css';
import classnames from 'classnames';
import { FilePicker, Alert, Dialog } from 'evergreen-ui';
import UploadedItem from './UploadedItem';
import POST from '../../api/API';

const cx = args => classnames(styles, args)

export const removeFileFromUploadedFiles = (files, name) => {
    return Object.values(files).reduce((acc, file) => {
            if (file.name !== name) {
                acc.push(file);
            }
            return acc;
        }, []);
}

export async function readFile(file) {
    const fileReader = new FileReader();
    const promise = new Promise((resolve, reject) => {
        fileReader.onerror = () => {
            fileReader.abort();
            reject('Problem parsing input files');
        };
        fileReader.onload = () => {
            resolve(fileReader.result);
        };
        fileReader.readAsText(file);
    });
    return await promise;
}

const UploadModal = props => {
    const {
        fileData,
        alertInfo,
        uploadModal,
        uploadModalOnConfirmHandler,
        uploadModalOnCloseHandler,
        setAlertSuccess,
        setAlertDanger,
        setFileData,
    } = props;

    const fileItemDeleteOnClickHandler = (name) => {
        const updatedUploadedFiles = removeFileFromUploadedFiles(fileData, name);
        setFileData(updatedUploadedFiles);
    }

    const createFileItem = (file) => {
        return (
            <UploadedItem 
                name={file.name}
                size={file.size}
                fileType={file.type}
                deleteOnClickHandler={() => fileItemDeleteOnClickHandler(file.name)}
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
        setFileData(files);
        setAlertSuccess('Successfully added');
    };

    const upload = () => {
        console.log(fileData);
        uploadModalOnConfirmHandler();
        POST(fileData);
    }

    return (
            <Dialog
                isShown={uploadModal.isOpen}
                id="uploadModal"
                title="Upload"
                isConfirmLoading={uploadModal.isLoading}
                confirmLabel={uploadModal.isLoading ? "Uploading.." : 'Upload'}
                onConfirm={upload}
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
                            placeholder={"Choose file or folder"}
                        />
                    </div>

                    { fileData && (
                        <div className={cx('fileListContainer')} > 
                                { Object.values(fileData).map(file => createFileItem(file)) }
                            </div>
                    )}
                </div>
            </Dialog>
    );
};

export default UploadModal;