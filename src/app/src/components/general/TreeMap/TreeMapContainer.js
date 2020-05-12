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
    const options = {
      "Cyclomatic Complexity": { metricName: "cyclomaticComplexity", valueUnit: "CC"},
      "Logical Lines of Code": { metricName: "logicalLinesOfCode", valueUnit: "LLOC"},
      "Afferent Coupling": { metricName: "afferentCoupling", valueUnit: "AC"},
      "Efferent Coupling": { metricName: "efferentCoupling", valueUnit: "EC"},
      "Max. Inheritance Depth": { metricName: "maximumInheritanceDepth", valueUnit: "MID"},
      "Max. Nesting Depth": { metricName: "maximumNestingDepth", valueUnit: "MND"},
    }

    const onSelectHandler = (item) => {
      setMenuState({ selected: item.value });
    }

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
                options={Object.keys(options).map(label => ({ label, value: label }))}
                selected={menuState.selected}
                onSelect={onSelectHandler}
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