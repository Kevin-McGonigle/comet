import React from 'react';
import MetricPane from '../MetricPane';
import { mount } from 'enzyme';
import "../../../../setupTests"

test('should render green MetricPane as expected', () => { 
    const component = mount(
        <MetricPane metricName="greenPane" metricValue="test" metricColour="green" />
    );
    expect(component.html()).toMatchSnapshot();
});

test('should render orange MetricPane as expected', () => { 
    const component = mount(
        <MetricPane metricName="orangePane" metricValue="test" metricColour="orange" />
    );
    expect(component.html()).toMatchSnapshot();
});

test('should render red MetricPane as expected', () => { 
    const component = mount(
        <MetricPane metricName="redPane" metricValue="test" metricColour="red" />
    );
    expect(component.html()).toMatchSnapshot();
});