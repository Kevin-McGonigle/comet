import React from 'react';
import { Pane, Text } from 'evergreen-ui';
import styles from './MetricPane.css';
import classnames from 'classnames';

const cx = args => classnames(styles, args)

const statusColours = {
    "green": "#7bed9f",
    "orange": "#ff9f43",
    "red": "#ff6b6b", 
}

const MetricPane = props => {
    const {
        metricName,
        metricValue,
        metricColour,
    } = props;

    return (
        <Pane
            elevation={4}
            background={statusColours[metricColour]}
            border="default"
            borderColor="black"
            float="left"
            width={120}
            height={120}
            margin={24}
            display="flex"
            flexDirection="row"
            alignItems="center"
            justifyContent="center"
        >
            <div className={cx('metricInfo')}>
                <Text color="black">{ metricName }</Text>
                <Text color="black">{ metricValue }</Text>
            </div>
        </Pane>
    )
};

export default MetricPane;