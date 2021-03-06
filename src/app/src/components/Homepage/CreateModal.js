import React, {useState} from 'react';
import styles from './CreateModal.css';
import classnames from 'classnames';
import {Alert, Dialog, IconButton, Pane, Tab, Tablist, Textarea, TextInput} from 'evergreen-ui';
import {createFileInformation, shapeFileData} from '../../helpers/helpers';
import upload_files from '../../api/API';
import { Redirect } from 'react-router';

const cx = args => classnames(styles, args);

const CreateModal = props => {
    const {
        alertInfo,
        createModal,
        createModalOnConfirmHandler,
        createModalOnCloseHandler,
        createModalOnFailureHandler,
        setMetrics,
        setAlertSuccess,
        setAlertDanger,
        setFileData,
        setRedirect,
    } = props;

    const [fileTabs, setFileTabs] = useState({
        selectedIndex: 0,
        tabs: ['File'],
        tabContent: [''],
    })

    const [newFileDialog, setNewFileDialog] = useState({
        isShown: false,
        fileName: '',
    })

    const onTextAreaChangeHandler = (event) => {
        const newFileContent = fileTabs.tabContent;
        newFileContent[fileTabs.selectedIndex] = event.target.value;
        setFileTabs({...fileTabs, tabContent: newFileContent});
    }

    const onPlusIconHandler = () => {}

    const onDeleteIconHandler = () => {
        const newTabs = fileTabs.tabs.filter(name => fileTabs.tabs.indexOf(name) !== fileTabs.selectedIndex)
        const newTabContent = fileTabs.tabContent.filter(name => fileTabs.tabs.indexOf(name) !== fileTabs.selectedIndex)

        setFileTabs({
            selectedIndex: fileTabs.selectedIndex,
            tabs: newTabs,
            tabContent: newTabContent,
        });
    }

    const upload = () => {
        createModalOnConfirmHandler();
        // need to shape data into file 
        const fileData = createFileInformation(fileTabs.tabs, fileTabs.tabContent)
        const shapedData = shapeFileData(fileData);
        upload_files(fileData).then((data) => {
            if (data) {
                setFileData(shapedData);
                setMetrics(data);
                setAlertSuccess("Uploaded successfully!")
            } else {
                createModalOnFailureHandler();
                setAlertDanger("Could not upload: " + data.statusText)
            }
        });
    }

    const onDialogCloseHandler = () => {
        const newTabs = fileTabs.tabs;
        newTabs.push(newFileDialog.fileName)
        const newTabContent = fileTabs.tabContent;
        newTabContent.push('');

        setFileTabs({
            selectedIndex: fileTabs.selectedIndex +1,
            tabContent: newTabContent,
            tabs: newTabs
        });
        setNewFileDialog({isShown: false, fileName: ''});
    }

    const onTextInputChange = (event) => {
        const value = event.target.value;
        setNewFileDialog({...newFileDialog, fileName: value});
    }

    const createAlert = () => {
        if (alertInfo.show) {
            return (
                <Alert
                    id={`${alertInfo.intent}Alert`}
                    intent={alertInfo.intent}
                    hasIcon
                    title={alertInfo.title}
                    marginTop={2}
                    marginBottom={8}
                />
            )
        }
    }

    return (
        <Dialog
            isShown={createModal.isOpen}
            title="Create"
            onConfirm={upload}
            isConfirmLoading={createModal.isLoading}
            confirmLabel={createModal.isLoading ? "Creating & Uploading" : "Upload"}
            onCloseComplete={createModalOnCloseHandler}
        >
            {createAlert()}

            <div className={cx('fileTab')}>
                <div className={cx('icons')}>
                    <Dialog
                        isShown={newFileDialog.isShown}
                        title="Create new file"
                        onCloseComplete={onDialogCloseHandler}
                        confirmLabel="Create"
                    >
                        <TextInput
                            name="File name"
                            placeholder="Filename.py"
                            onChange={onTextInputChange}
                        />
                    </Dialog>

                    <IconButton id="plus" icon="plus" onClick={onPlusIconHandler}/>
                    <IconButton id="edit" icon="edit" />
                    <IconButton id="trash" icon="trash" intent="danger" onClick={onDeleteIconHandler}/>
                </div>

                <Pane height={16}>
                    <Tablist marginBottom={14} flexBasis={240} marginRight={24}>
                        {fileTabs.tabs.map((tab, index) => (
                            <Tab
                                key={tab}
                                id={tab}
                                onSelect={() => setFileTabs({...fileTabs, selectedIndex: index})}
                                isSelected={index === fileTabs.selectedIndex}
                                aria-controls={`panel-${tab}`}
                            >
                                {tab}
                            </Tab>
                        ))}
                    </Tablist>
                </Pane>
            </div>

            <div className={cx('createModeContainer')}>
                <div className={cx('textAreaContainer')}>
                    <Textarea
                        name="textArea"
                        id="textAreaId"
                        placholder="Input your code here.."
                        onChange={onTextAreaChangeHandler}
                        value={fileTabs.tabContent[fileTabs.selectedIndex]}
                    />
                </div>
            </div>
        </Dialog>
    );
};

export default CreateModal;




