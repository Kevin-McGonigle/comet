import React from 'react';
import {Button, Menu, Popover, Position} from 'evergreen-ui';
import { useHistory } from 'react-router';


const ToolbarMenu = () => {
    const history = useHistory();
    return (
        <Popover
            position={Position.BOTTOM_LEFT}
            content={
                <Menu>
                    <Menu.Group title="Return">
                        <Menu.Item icon="home" onClick={() => history.push('/')}>Try again</Menu.Item>
                    </Menu.Group>
                </Menu>
            }
        >
            <Button marginRight={16}>Menu</Button>
        </Popover>
    )
};

export default ToolbarMenu;