import React from 'react';
import styles from './UploadModal.css';
import classnames from 'classnames';
import { Textarea, Alert, Dialog } from 'evergreen-ui';

const cx = args => classnames(styles, args)

const CreateModal = props => {
    const {
        alertInfo,
        setTextArea,
        createModal,
        createModalOnConfirmHandler,
        createModalOnCloseHandler,
        setAlertSuccess,
        setAlertDanger,
    } = props; 

    const onChangeHandler = (event) => {
        setAlertSuccess();
        setTextArea({ value:  event.target.value })
    }

    const createAlert = () => {
        if (alertInfo.show){
            return (
                <Alert
                    id={`${alertInfo.intent}Alert`}
                    intent={alertInfo.intent}
                    hasIcon
                    title={alertInfo.title}
                    marginTop={2}
                    marginBottom={8}
                />
            )}
    }

    return (
        <Dialog
            isShown={createModal.isOpen}
            title="Create"
            onConfirm={createModalOnConfirmHandler}
            isConfirmLoading={createModal.isLoading}
            confirmLabel={createModal.isLoading ? "Creating & Uploading" : "Upload"}
            onCloseComplete={createModalOnCloseHandler}
        >
            <div className={cx('createModeContainer')}>
                { createAlert() }
                <div className={cx('textAreaContainer')}>
                    <Textarea 
                        name="textArea"
                        id="textAreaId"
                        placholder="Input your code here.."
                        onChange={onChangeHandler}
                    />
                </div>
            </div>
        </Dialog>
    );
};

export default CreateModal;




