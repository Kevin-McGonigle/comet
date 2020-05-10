import React from "react";
import ClassDiagram from "./ClassDiagram/ClassDiagram";
import { DependencyGraphNodeContainer } from './DependencyGraph/DependencyGraphContainer'

export const staticConfig = {
    "automaticRearrangeAfterDropNode": false,
    "collapsible": false,
    "directed": true,
    "focusAnimationDuration": 0.75,
    "focusZoom": 1,
    "highlightDegree": 1,
    "highlightOpacity": 1,
    "linkHighlightBehavior": false,
    "maxZoom": 8,
    "minZoom": 1,
    "nodeHighlightBehavior": true,
    "staticGraphWithDragAndDrop": true,
    "panAndZoom": true,
    "d3": {
        "alphaTarget": 0.05,
        "gravity": -100,
        "linkLength": 100,
        "linkStrength": 1,
        "disableLinkForce": false
    },
    "node": {
        "color": "#3498db",
        "fontColor": "#1e272e",
        "fontSize": 20,
        "fontWeight": "normal",
        "highlightColor": "SAME",
        "highlightFontSize": 8,
        "highlightFontWeight": "normal",
        "highlightStrokeColor": "SAME",
        "highlightStrokeWidth": "SAME",
        "labelProperty": "id",
        "mouseCursor": "pointer",
        "opacity": 1,
        "renderLabel": true,
        "size": 200,
        "strokeColor": "#3498db",
        "strokeWidth": 1.5,
        "svg": "",
        "symbolType": "square"
    },
    "link": {
        "color": "#2c3e50",
        "fontColor": "black",
        "fontSize": 8,
        "fontWeight": "normal",
        "highlightColor": "true",
        "highlightFontSize": 8,
        "highlightFontWeight": "normal",
        "labelProperty": "label",
        "mouseCursor": "pointer",
        "opacity": 1,
        "renderLabel": false,
        "semanticStrokeWidth": false,
        "strokeWidth": 1.5,
        "markerHeight": 6,
        "markerWidth": 6
    }   
};

export const dynamicConfig = {
    "automaticRearrangeAfterDropNode": true,
    "collapsible": false,
    "directed": true,
    "focusAnimationDuration": 0.75,
    "focusZoom": 1,
    "height": 400,
    "highlightDegree": 1,
    "highlightOpacity": 1,
    "linkHighlightBehavior": false,
    "maxZoom": 8,
    "minZoom": 1,
    "nodeHighlightBehavior": false,
    "panAndZoom": false,
    "staticGraph": false,
    "staticGraphWithDragAndDrop": false,
    "width": 800,
    "d3": {
      "alphaTarget": 0.05,
      "gravity": -100,
      "linkLength": 100,
      "linkStrength": 1,
      "disableLinkForce": false
    },
    "node": {
      "color": "#3498db",
      "fontColor": "black",
      "fontSize": 8,
      "fontWeight": "normal",
      "highlightColor": "SAME",
      "highlightFontSize": 8,
      "highlightFontWeight": "normal",
      "highlightStrokeColor": "SAME",
      "highlightStrokeWidth": "SAME",
      "labelProperty": "id",
      "mouseCursor": "pointer",
      "opacity": 1,
      "renderLabel": true,
      "size": 200,
      "strokeColor": "#3498db",
      "strokeWidth": 1.5,
      "svg": "",
      "symbolType": "circle"
    },
    "link": {
      "color": "#2c3e50",
      "fontColor": "black",
      "fontSize": 8,
      "fontWeight": "normal",
      "highlightColor": "true",
      "highlightFontSize": 8,
      "highlightFontWeight": "normal",
      "labelProperty": "label",
      "mouseCursor": "pointer",
      "opacity": 1,
      "renderLabel": false,
      "semanticStrokeWidth": false,
      "strokeWidth": 1.5,
      "markerHeight": 6,
      "markerWidth": 6,
      "type": "CURVE_SMOOTH"
    }
}

export const classDiagramConfig = {
    "automaticRearrangeAfterDropNode": true,
    "collapsible": false,
    "directed": true,
    "focusAnimationDuration": 0.75,
    "focusZoom": 1,
    "highlightDegree": 1,
    "highlightOpacity": 1,
    "linkHighlightBehavior": false,
    "maxZoom": 2,
    "minZoom": 1,
    "nodeHighlightBehavior": true,
    "panAndZoom": true,
    "d3": {
        "alphaTarget": 0.05,
        "gravity": -100,
        "linkLength": 100,
        "linkStrength": 1,
        "disableLinkForce": false
    },
    "node": {
        "color": "#3498db",
        "fontColor": "#1e272e",
        "fontWeight": "normal",
        "highlightColor": "SAME",
        "highlightFontSize": 8,
        "highlightFontWeight": "normal",
        "highlightStrokeColor": "SAME",
        "highlightStrokeWidth": "SAME",
        "labelProperty": "id",
        "mouseCursor": "pointer",
        "opacity": 1,
        "renderLabel": true,
        "size": 200,
        "strokeColor": "#3498db",
        "strokeWidth": 1.5,
        "svg": "",
        "symbolType": "square",
        viewGenerator: node => <ClassDiagram data={node} />,

    },
    "link": {
        "color": "#2c3e50",
        "fontColor": "black",
        "fontSize": 8,
        "fontWeight": "normal",
        "highlightColor": "true",
        "highlightFontSize": 8,
        "highlightFontWeight": "normal",
        "labelProperty": "label",
        "mouseCursor": "pointer",
        "opacity": 1,
        "renderLabel": true,
        "semanticStrokeWidth": false,
        "strokeWidth": 1.5,
        "markerHeight": 6,
        "markerWidth": 6
    }   
}

export const dependencyGraphConfig = {
    "automaticRearrangeAfterDropNode": true,
    "collapsible": false,
    "directed": true,
    "focusAnimationDuration": 0.75,
    "focusZoom": 1,
    "highlightDegree": 1,
    "highlightOpacity": 1,
    "linkHighlightBehavior": false,
    "maxZoom": 2,
    "minZoom": 1,
    "nodeHighlightBehavior": true,
    "panAndZoom": true,
    "d3": {
        "alphaTarget": 0.05,
        "gravity": -100,
        "linkLength": 100,
        "linkStrength": 1,
        "disableLinkForce": false
    },
    "node": {
        "color": "#3498db",
        "fontColor": "#1e272e",
        "fontWeight": "normal",
        "highlightColor": "SAME",
        "highlightFontSize": 8,
        "highlightFontWeight": "normal",
        "highlightStrokeColor": "SAME",
        "highlightStrokeWidth": "SAME",
        "labelProperty": "id",
        "mouseCursor": "pointer",
        "opacity": 1,
        "renderLabel": true,
        "size": 200,
        "strokeColor": "#3498db",
        "strokeWidth": 1.5,
        "svg": "",
        "symbolType": "square",
        viewGenerator: node => <DependencyGraphNodeContainer data={node} />,
    },
    "link": {
        "color": "#2c3e50",
        "fontColor": "black",
        "fontSize": 8,
        "fontWeight": "normal",
        "highlightColor": "true",
        "highlightFontSize": 8,
        "highlightFontWeight": "normal",
        "labelProperty": "label",
        "mouseCursor": "pointer",
        "opacity": 1,
        "renderLabel": true,
        "semanticStrokeWidth": false,
        "strokeWidth": 1.5,
        "markerHeight": 6,
        "markerWidth": 6,
    }   
}




export const basicRelationshipData = {
    nodes: [
        {id: "object", group: 1},
        {id: "Class A", group: 1},
        {id: "Class B", group: 1},
        {id: "Class C", group: 1},
        {id: "Class D", group: 1},
        {id: "Class E", group: 1},
        {id: "Class F", group: 1},
    ],
    links: [
        {source: "object", target: "Class A", value: 1},
        {source: "Class A", target: "Class B", value: 1},
        {source: "Class A", target: "Class C", value: 1},
        {source: "Class B", target: "Class D", value: 1},
        {source: "Class D", target: "Class E", value: 1},
        {source: "Class E", target: "Class F", value: 1},
    ]
}

export const controlFlowGraphData = {
    nodes: [
        {id: "A = 0", group: 1},
        {id: "B > C", group: 1},
        {id: "A = B", group: 1},
        {id: "A = C", group: 1},
        {id: "end-if", group: 1},
        {id: "end-if-complete", group: 1},
    ],
    links: [
        {source: "A = 0", target: "B > C", value: 1},
        {source: "B > C", target: "A = B", value: 1},
        {source: "B > C", target: "A = C", value: 1},
        {source: "A = B", target: "end-if", value: 1},
        {source: "A = C", target: "end-if", value: 1},
        {source: "end-if", target: "end-if-complete", value: 1},
    ]
}

export const dependencyGraphData = {
    nodes: [
        {id: "preact.js", group: 1},
        {id: "render.js", group: 1},
        {id: "render-queue.js", group: 1},
        {id: "clone-element.js", group: 1},
        {id: "h.js", group: 1},
        {id: "vnode.js", group: 1},
        {id: "options.js", group: 1},
        {id: "util.js", group: 1},
        {id: "diff.js", group: 1},
        {id: "component.js", group: 1},
        {id: "index.js", group: 1},
        {id: "constants.js", group: 1},
    ],
    links: [
        {source: "preact.js", target: "render.js", value: 1},
        {source: "preact.js", target: "component.js", value: 1},
        {source: "preact.js", target: "clone-element.js", value: 1},
        {source: "preact.js", target: "h.js", value: 1},
        {source: "preact.js", target: "render-queue.js", value: 1},
        {source: "component.js", target: "util.js", value: 1},
        {source: "component.js", target: "options.js", value: 1},
        {source: "component.js", target: "constants.js", value: 1},
        {source: "render.js", target: "diff.js", value: 1},
        {source: "h.js", target: "options.js", value: 1},
        {source: "h.js", target: "vnode.js", value: 1},
        {source: "diff.js", target: "index.js", value: 1},
        {source: "index.js", target: "options.js", value: 1},
    ]
}

export const classDiagramData = {
    nodes: [
        {   id: "A",
            classArgs: {"Arg1": "String", "Arg2": "Int"}, 
            classFunctions: {
                "Function1": {
                    arguments: {
                        "Arg1": "String",
                        "Arg2": "Int",
                    },
                    returnType: "String"
            }}
        },
        {   id: "B", 
            classArgs: {"Arg1": "String", "Arg2": "Int"}, 
            classFunctions: {
                "Function1": {
                    arguments: {
                        "Arg1": "String",
                        "Arg2": "Int",
                    },
                    returnType: "String"
            }}
        }
    ],
    links: [
        {source: "A", target: "B", label: "test", value: 1},
 
    ]
}


export const configMapping = {
    "static": staticConfig,
    "dynamic": dynamicConfig,
    "classDiagram": classDiagramConfig,
    "dependencyGraph": dependencyGraphConfig,
}
