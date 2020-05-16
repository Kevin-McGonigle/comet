import React from 'react';
import {Button, Menu, Popover, Position} from 'evergreen-ui';

const ToolbarMenu = props => {
    const {} = props;

    return (
        <Popover
            position={Position.BOTTOM_LEFT}
            content={
                <Menu>
                    <Menu.Group title="Actions">
                        <Menu.Item icon="people">Create</Menu.Item>
                        <Menu.Item icon="circle-arrow-right">Upload</Menu.Item>
                    </Menu.Group>
                    <Menu.Divider/>
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