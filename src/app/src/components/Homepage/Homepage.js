import React, {useState} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import styles from './Homepage.css';
import classnames from 'classnames';
import comet from './comet.png';
import {Button} from 'evergreen-ui';
import {UploadModalContainer} from './UploadModalContainer';
import {CreateModalContainer} from './CreateModalContainer';
import {actions as alertActions} from '../../store/alert/alert';

const cx = args => classnames(styles, args)

const Homepage = props => {
    const {
        setAlertNone,
    } = props;
    const [createModal, setCreateModal] = useState({ isOpen: false, isLoading: false});
    const [uploadModal, setUploadModal] = useState({ isOpen: false, isLoading: false });

    // Handlers stop the creation of new functions each render 
    const createButtonOnClickHandler = () => setCreateModal({isOpen: true, isLoading: false});
    const createModalOnCloseHandler = () => {
        setAlertNone();
        setCreateModal({isOpen: false, isLoading: false});
    }
    const createModalOnConfirmHandler = () => {
        setAlertNone();
        setCreateModal({isOpen: true, isLoading: true})
    }

    const createModalOnFailureHandler = () => {
        setCreateModal({isOpen: true, isLoading: false})
    }

    const uploadButtonOnClickHandler = () => {
        setUploadModal({isOpen: true, isLoading: false});
    }

    const uploadModalOnCloseHandler = () => {
        setAlertNone();
        setUploadModal({isOpen: false, isLoading: false});
    }

    const uploadModalOnConfirmHandler = () => {
        setAlertNone();
        setUploadModal({isOpen: true, isLoading: true})
    }


    return (
        <div className={cx('homepageContainer')}>
            <div className={cx('topBar')}>
                <p>by James Miles & Kevin McGonigle</p>
            </div>
            <div className={cx('logoContainer')}>
                <h1>comet.</h1>
                <h2>code metrics - made simple</h2>
                <div className={cx('logo')}>
                    <img src={comet} width="200px" height="200px" alt={"Comet logo."}/>

                    <div>
                        <CreateModalContainer
                            createModal={createModal}
                            createModalOnConfirmHandler={createModalOnConfirmHandler}
                            createModalOnCloseHandler={createModalOnCloseHandler}
                            createModalOnFailureHandler={createModalOnFailureHandler}
                        />

                        <UploadModalContainer
                            uploadModal={uploadModal}
                            uploadModalOnConfirmHandler={uploadModalOnConfirmHandler}
                            uploadModalOnCloseHandler={uploadModalOnCloseHandler}
                        />

                        <Button
                            id='createButton'
                            className={cx('createButton')}
                            onClick={createButtonOnClickHandler}
                            marginRight={12}
                            height={48}>
                            Create
                        </Button>

                        <Button
                            id='uploadButton'
                            className={cx('uploadButton')}
                            onClick={uploadButtonOnClickHandler}
                            marginRight={12}
                            height={48}>
                            Upload
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
};

const mapDispatchToProps = dispatch => bindActionCreators(alertActions, dispatch);

export default connect(null, mapDispatchToProps)(Homepage);