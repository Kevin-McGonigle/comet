import React from 'react';
import styles from './Menu.css';
import classnames from 'classnames';
import { Menu, Popover, Button, Position } from 'evergreen-ui';

const cx = args => classnames(styles, args);

const ToolbarMenu  = props => {
    const {
        metricInfo,
    } = props;

    return (
        <Popover
        position={Position.BOTTOM_LEFT}
        content={
          <Menu>
            <Menu.Group title="Actions">
              <Menu.Item icon="people">Share...</Menu.Item>
              <Menu.Item icon="circle-arrow-right">Move...</Menu.Item>
              <Menu.Item icon="edit" secondaryText="⌘R">
                Rename...
              </Menu.Item>
            </Menu.Group>
            <Menu.Divider />
            <Menu.Group title="destructive">
              <Menu.Item icon="trash" intent="danger">
                Delete...
              </Menu.Item>
            </Menu.Group>
          </Menu>
        }
      >
        <Button marginRight={16}>Menu</Button>
      </Popover>
    )
};

export default ToolbarMenu;