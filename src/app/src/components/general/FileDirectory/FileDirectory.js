import React from 'react';
import styles from './FileDirectory.css';
import comet from '../../Homepage/comet.png';
import classnames from 'classnames';
import {Pane, Table} from 'evergreen-ui';

const cx = args => classnames(styles, args)

const FileDirectory = props => {
    const {
        selectedFile,
        fileNames,
        setSelectedFile,
    } = props;

    const setSelectedFileHandler = (event) => {
        const fileName = event.currentTarget.textContent;
        setSelectedFile(fileName);
    }

    return (
        <div className={cx('fileDirectory')}>
            <div className={cx('fileDirLogo')}>
                Comet
                <img src={comet} width="50px" height="50px" alt={"Comet logo."}/>
            </div>

            <div className={cx('fileDirTitle')}>File Directory</div>

            <div className={cx('fileDirTable')}>
                <Table>
                    <Table.Head>
                        <Table.SearchHeaderCell/>
                    </Table.Head>

                    <div className={cx('fileItemContainer')}>
                        <Pane>
                            {fileNames && fileNames.map(file => {
                                return (
                                    <Table.Row
                                        key={file}
                                        isSelectable
                                        isSelected
                                        width="250px"
                                        textAlign="center"
                                        isHighlighted={selectedFile === file}
                                        onClick={e => setSelectedFileHandler(e)}
                                    >
                                        <Table.TextCell backgroundColor={selectedFile !== file && "grey"}
                                                        id={file}>{file}</Table.TextCell>
                                    </Table.Row>
                                )
                            })}
                        </Pane>
                    </div>
                </Table>
            </div>
        </div>
    )
};

export default FileDirectory;