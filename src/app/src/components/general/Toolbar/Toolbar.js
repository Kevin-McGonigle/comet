
import React, { useState } from 'react';
import styles from './Toolbar.css';
import classnames from 'classnames';
import { Tab, Tablist, Pane } from 'evergreen-ui';
import ToolbarMenu from '../Menu/Menu';

const cx = args => classnames(styles, args);

const Toolbar  = props => {
    const {} = props;
    const [tabState, setTabState] = useState({
        selectedIndex: 0,
        tabs: ["Metrics", "Metric Graph", "Tree"]
    });

    const onClickHandler = (event) => {
        const tabTitle = event.currentTarget.id;
        const tabIndex = tabState.tabs.indexOf(tabTitle);
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
                            id={tab}
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