import React from 'react';
import { Radar } from 'react-chartjs-2';

const RadarGraph = (props) => {
    // const { data } = props;
    const data = {
        labels: ['Cyclomatic Complexity', 'Logical Lines of Code', 'Lines of Comment', 'Afferent Coupling', 'Efferent Coupling', 'Instability', 'Method Cohesion', 'Relational Cohesion', 'Nesting Depth'],
        datasets: [
            {
                label: 'General Overview',
                data: [10, 20, 30, 40, 50, 35, 60, 20, 20],
                backgroundColor: "rgba(200,0,0,0.2)",
                title: {
                    display: true,
                    text: "Radar Graph"
                }
            }
        ]
    };

    return (
            <Radar 
                data={data}
                width={150}
                height={150}
                options={{ maintainAspectRatio: false, backgroundColor: "white" }}
            />
    )
}

export default RadarGraph;