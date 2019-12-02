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
        deleteOnClickHandler,
    } = props;

    return (
        <div className={cx('fileItemContainer')}>
            <div className={cx('fileItems')}>
                <div className={'fileItem'}>Name: <i>{ name }</i></div>
                <div className={'fileItem'}>Size: <i>{ size }</i></div>
                <div className={'fileItem'}>File Type: <i>{ fileType }</i></div>
            </div>
            <div className={cx('deleteIcon')}>
                <Icon icon="trash" id='deleteIcon' onClick={name => deleteOnClickHandler(name)} />
            </div>
        </div>
    )
}

export default UploadedItem;