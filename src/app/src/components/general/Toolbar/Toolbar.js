import React from 'react';
import styles from './Toolbar.css';
import classnames from 'classnames';
import {Pane, Tab, Tablist} from 'evergreen-ui';
import ToolbarMenu from '../Menu/Menu';

const cx = args => classnames(styles, args);

const Toolbar = props => {
    const {tabState, setTabState, tabMapping} = props;

    const onClickHandler = (event) => {
        const tabTitle = event.currentTarget.id;
        const tabIndex = tabState.tabs.indexOf(tabMapping[tabTitle]);
        setTabState({
            ...tabState,
            selectedIndex: tabIndex,
        });
    }

    return (
        <div className={cx("tabMenu")}>
            <Pane marginTop={12} marginBottom={12} marginLeft={300}>
                <Tablist>
                    {tabState.tabs.map((tab, index) => (
                        <Tab
                            key={tab}
                            id={tab.split(" ").join('')}
                            isSelected={index === tabState.selectedIndex}
                            aria-controls={`panel-${tab}`}
                            color="white"
                            onClick={event => onClickHandler(event)}
                        >
                            {tab}
                        </Tab>
                    ))}
                </Tablist>
            </Pane>

            <div className={cx("menu")}><ToolbarMenu/></div>
        </div>
    )
};

export default Toolbar;