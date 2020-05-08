import React, { useState } from 'react';
import TreeMap from 'react-d3-treemap';
import { Pane, SelectMenu, Button } from 'evergreen-ui';
import "react-d3-treemap/dist/react.d3.treemap.css";

const data = {
    name: "flare",
    children: [
      {
        name: "analytics",
        children: [
          {
            name: "cluster",
            children: [
              {
                name: "AgglomerativeCluster",
                value: 10,
              },
              { name: "CommunityStructure", value: 20 },
              { name: "HierarchicalCluster", value: 20 },
            ]
        }]
      }
    ]
};
  

const TreeMapContainer = props => {
    const [menuState, setMenuState] = useState({ selected: null })

    return (
        <Pane
            display="flex"
            flexWrap="wrap"
            flexGrow={1}
            margin="10"
            background="tint2"
            elevation={4}  
        >
            <SelectMenu
                title="Select metric"
                options={["Cycolmatic Complexity", "Lines of Comment", "Afferent Coupling", 
                    "Efferent Coupling", "Instability", "Abstractness", 
                    "Method Cohesion", "Relational Cohesion", "Nesting Depth"].map(label => ({ label, value: label }))}
                selected={menuState.selected}
                onSelect={item => setMenuState({ selected: item.value })}
            >
                <Button float="right">{ menuState.selected || "Select metric" }</Button>
            </SelectMenu>

            <TreeMap
                height={450}
                width={1000}
                data={data}
                valueUnit={"MB"}
            />
        </Pane>
       
    );
};

export default TreeMapContainer;