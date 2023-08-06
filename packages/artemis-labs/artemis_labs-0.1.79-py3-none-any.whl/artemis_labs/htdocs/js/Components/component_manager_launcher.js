'use strict';    

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
            component = new Input(componentIndex, false);
            break;
        case "switch":
            component = new Switch(componentIndex, false);
            break;
        case "number-wheel":
            component = new NumberWheel(componentIndex, false);
            break;
        case "image":
            component = new Image(componentIndex);
            break;
        case "model":
            component = new Model(componentIndex);
            break;
        case "video":
            component = new Video(componentIndex, false);
            break;
        case "text area":
            component = new TextArea(componentIndex, false);
            break;
        case "select input":
            component = new SelectInput(componentIndex, false);
            break;
        case "radio button":
            component = new RadioButton(componentIndex);
            break;
        case "checkbox":
            component = new Checkbox(componentIndex, false);
            break;
        case "box":
            component = new Box(componentIndex, false);
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
        case "range":
            return "component-range-size";
            break;
        case "model":
            return "component-model-size";
            break;
        case "image":
            return "component-image-size";
            break;
        case "switch":
            return "component-switch-size";
            break;
        case "video":
            return "component-video-size";
            break;
        case "number-wheel":
            return "component-number-wheel-size";
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
        case "scatter-graph":
            return "component-scatter-graph-size";
            break;
        case "table":
            return "component-table-size";
            break;
    }
    return "";
}
