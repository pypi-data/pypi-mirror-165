'use strict';    

// Components
import { Button } from "./Designer/button.js";
import { Input } from "./Designer/input.js";
import { Range } from "./Designer/range.js";
import { SelectInput } from "./Designer/select_input.js";
import { Image } from "./Designer/image.js";
import { Video } from "./Designer/video.js";
import { Header } from "./Designer/header.js";
import { HorizontalRule } from "./Designer/horizontal_rule.js";
import { TextArea } from "./Designer/text_area.js";
import { RadioButton } from "./Designer/radio_button.js";
import { Checkbox } from "./Designer/checkbox.js";
import { Box } from "./Designer/box.js";
import { Paragraph } from "./Designer/paragraph.js";
import { VerticalRule } from "./Designer/vertical_rule.js";
import { NumberWheel } from "./Designer/number_wheel.js";
import { Switch } from "./Designer/switch.js";
import { LineGraph } from "./Designer/line_graph.js";
import { BarGraph } from "./Designer/bar_graph.js";
import { Table } from "./Designer/table.js";
import { ScatterGraph } from "./Designer/scatter_graph.js";
import { Model } from "./Designer/model.js";

// Create component
function createComponentFromPlacement(componentBeingPlaced, componentIndex) {
    const componentType = $(componentBeingPlaced).attr('data-search');
    return createComponentFromType(componentType, componentIndex);
}

// Create componnet from type
function createComponentFromType(componentType, componentIndex) {
    let component = null;
    switch(componentType) {
        case "horizontal rule":
            component = new HorizontalRule(componentIndex);
            break;
        case "vertical rule":
            component = new VerticalRule(componentIndex);
            break;
        case "button":
            component = new Button(componentIndex);
            break;
        case "heading":
            component = new Header(componentIndex);
            break;
        case "paragraph":
            component = new Paragraph(componentIndex);
            break;
        case "input":
            component = new Input(componentIndex);
            break;
        case "switch":
            component = new Switch(componentIndex);
            break;
        case "number-wheel":
            component = new NumberWheel(componentIndex);
            break;
        case "range":
            component = new Range(componentIndex);
            break;
        case "image":
            component = new Image(componentIndex);
            break;
        case "model":
            component = new Model(componentIndex);
            break;
        case "video":
            component = new Video(componentIndex);
            break;
        case "text area":
            component = new TextArea(componentIndex);
            break;
        case "select input":
            component = new SelectInput(componentIndex);
            break;
        case "radio button":
            component = new RadioButton(componentIndex);
            break;
        case "checkbox":
            component = new Checkbox(componentIndex);
            break;
        case "box":
            component = new Box(componentIndex);
            break;
        case "card":
            component = new Card(componentIndex);
            break;
        case "line-graph":
            component = new LineGraph(componentIndex);
            break;
        case "bar-graph":
            component = new BarGraph(componentIndex);
            break;        
        case "table":
            component = new Table(componentIndex);
            break;
        case "scatter-graph":
            component = new ScatterGraph(componentIndex);
            break;
    }
    return component;
}

// Get component size class
function getComponentSizeClass(componentBeingPlaced) {
    const componentType = $(componentBeingPlaced).attr('data-search');
    let component = null;
    switch(componentType) {
        case "button":
            return "component-button-size";
            break;
        case "heading":
            return "component-header-size";
            break;
        case "paragraph":
            return "component-paragraph-size";
            break;
        case "input":
            return "component-input-size";
            break;
        case "number-wheel":
            return "component-number-wheel-size";
            break;
        case "range":
            return "component-range-size";
            break;
        case "image":
            return "component-image-size";
            break;
        case "model":
            return "component-model-size";
            break;
        case "switch":
            return "component-switch-size";
            break;
        case "video":
            return "component-video-size";
            break;
        case "horizontal rule":
            return "component-hr-size";
            break;
        case "vertical rule":
            return "component-vr-size";
            break;
        case "text area":
            return "component-text-area-size";
            break;
        case "select input":
            return "component-select-input-size";
            break;
        case "radio button":
            return "component-radio-button-size";
            break;
        case "checkbox":
            return "component-checkbox-size";
            break;
        case "box":
            return "component-box-size";
            break;
        case "card":
            return "component-card-size";
            break;
        case "line-graph":
            return "component-line-graph-size";
            break;
        case "bar-graph":
            return "component-bar-graph-size";
            break;
        case "table":
            return "component-table-size";
            break;
        case "scatter-graph":
            return "component-scatter-graph-size";
            break;
    }
    return "";
}

// Export
export {createComponentFromPlacement, getComponentSizeClass, createComponentFromType};