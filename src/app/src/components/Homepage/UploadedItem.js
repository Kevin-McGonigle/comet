import React from 'react';
import styles from './UploadModal.css';
import classnames from 'classnames';
import { Icon } from 'evergreen-ui';

const cx = args => classnames(styles, args)

const UploadedItem = (props) => {
    const {
        name,
        fileType,
        size,
        uploadedFiles,
        setUploadedFiles
    } = props;

    const deleteOnClickHandler = () => {
        const removedFileObj = Object.values(uploadedFiles).reduce((acc, file) => {
            if (file.name !== name) {
                acc.push(file);
            }
            return acc;
        }, []);
        setUploadedFiles(removedFileObj);
    }
    
    return (
        <div className={cx('fileItemContainer')}>
            <div className={cx('fileItems')}>
                <div className={'fileItem'}>Name: <i>{ name }</i></div>
                <div className={'fileItem'}>Size: <i>{ size }</i></div>
                <div className={'fileItem'}>File Type: <i>{ fileType }</i></div>
            </div>
            <div className={cx('deleteIcon')}>
                <Icon icon="trash" onClick={deleteOnClickHandler} />
            </div>
        </div>

    )
}

export default UploadedItem;