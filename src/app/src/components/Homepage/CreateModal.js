import React, { useState } from 'react';
import styles from './CreateModal.css';
import classnames from 'classnames';
import { Textarea, Alert, Dialog, Pane, Tablist, Tab, IconButton, TextInput } from 'evergreen-ui';
import upload_files from '../../api/API';

const cx = args => classnames(styles, args);

const createFileInformation = (fileNames, fileContent) => {
    const fileData = fileNames.map((file, ind) => {
        return new File([fileContent[ind]], file, { type: "text/plain", lastModified: "test" })
    });
    return fileData;
}

export const shapeFileData = (fileData) => {
    const shapedData = fileData.map((file) => {
        const data = readFile(file);
        return {
            name: file.name,
            lastModified: file.lastModified,
            size: file.size,
            type: file.type,
            content: data,
        };
    });
    return shapedData;
}

const CreateModal = props => {
    const {
        alertInfo,
        createModal,
        createModalOnConfirmHandler,
        createModalOnCloseHandler,
        createModalOnFailureHandler,
        setInheritanceTree,
        setAlertSuccess,
        setAlertDanger,
        setFileData,
        history,
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
        setFileTabs({ ...fileTabs, tabContent: newFileContent });
    }

    const onPlusIconHandler = () => {
        setNewFileDialog({ ...newFileDialog, isShown: true });
    }

    const onDeleteIconHandler = () => {
        const selectedInd = fileTabs.selectedIndex;
        const newTabs = fileTabs.tabs.splice(selectedInd, 1);
        const newContent = fileTabs.tabContent.splice(selectedInd, 1);

        setFileTabs({
            selectedIndex: 0,
            tabs: newTabs,
            tabContent: newContent,
        });
    }

    const onEditIconHandler = () => {

    }

    const upload = () => {
        createModalOnConfirmHandler();
        // need to shape data into file 
        const fileData = createFileInformation(fileTabs.tabs, fileTabs.tabContent)
        const shapedData = shapeFileData(fileData);
        upload_files(fileData).then((data) => {
            if (data) {
                setFileData(shapedData);
                setInheritanceTree(data);
                setAlertSuccess("Uploaded succesfully!")
                history.push('/metrics');
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
            ...fileTabs,
            tabContent: newTabContent,
            tabs: newTabs
        });
        setNewFileDialog({ isShown: false, fileName: '' });
    }

    const onTextInputChange = (event) => {
        const value = event.target.value;
        setNewFileDialog({ ...newFileDialog, fileName: value });
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
            onConfirm={upload}
            isConfirmLoading={createModal.isLoading}
            confirmLabel={createModal.isLoading ? "Creating & Uploading" : "Upload"}
            onCloseComplete={createModalOnCloseHandler}
        >
            { createAlert() }

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

                    <IconButton icon="plus" onClick={onPlusIconHandler}/>
                    <IconButton icon="edit" onClick={onEditIconHandler}/>
                    <IconButton icon="trash" intent="danger" onClick={onDeleteIconHandler}/>
                </div>
            
                <Pane height={16}>
                    <Tablist marginBottom={14} flexBasis={240} marginRight={24}>
                        { fileTabs.tabs.map((tab, index) => (
                            <Tab
                                key={tab}
                                id={tab}
                                onSelect={() => setFileTabs({ ...fileTabs, selectedIndex: index })}
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




