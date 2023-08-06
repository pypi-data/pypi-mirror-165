'use strict';

// Menu Node Context
class ScatterGraph extends Component {

    // Build graph
    buildGraph(ctx = null) {

        if (ctx == null) {
            ctx = qs(this.id + " canvas").getContext('2d');
        }

        const data = {
            datasets: [{
              label: 'Scatter Dataset',
              data: [{
                x: -10,
                y: 0
              }, {
                x: 0,
                y: 10
              }, {
                x: 10,
                y: 5
              }, {
                x: 0.5,
                y: 5.5
              }],
              backgroundColor: 'rgb(255, 99, 132)'
            }],
        };

        this.chart = new Chart(ctx, {
            type: 'scatter',
            data: data,
            options: {
                maintainAspectRatio : false,
                plugins : {
                    legend: this.showLegend
                },
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        grid: {
                            display: this.displayGridLines
                        }
                    },
                    y: {
                        grid: {
                            display: this.displayGridLines
                        }
                    }
                }
            }
        });

        let numDataSets = this.chart.data.datasets.length;
        for (let i = 0; i < numDataSets; i++) {
            this.chart.data.datasets[i].pointBorderColor = this.pointColor;
            this.chart.data.datasets[i].pointBackgroundColor = this.pointColor;
            this.chart.data.datasets[i].borderColor = this.pointColor;
            this.chart.data.datasets[i].backgroundColor = this.pointColor;
            this.chart.data.datasets[i].pointRadius = this.pointRadius;
        }
        this.chart.update();
    }

    // Refresh graph
    refreshGraph() {
        this.chart.destroy();
        this.buildGraph();
    }

    // Constructor
    constructor(componentIndex) {

        // Call parent constructor
        super(componentIndex);

        // Save features
        this.showLegend = true;
        this.pointColor = "#48b6fa";
        this.pointRadius = 3;
        this.displayGridLines = true;

        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-scatter-graph");
        $(containerDiv).attr("data-type", "component");

        // Create graph
        let graphCanvas = createElement("canvas", "", "graph-canvas");
        containerDiv.appendChild(graphCanvas);
        $(graphCanvas).css("width", "100%");
        $(graphCanvas).css("height", "100%");
        this.buildGraph(graphCanvas.getContext('2d'));
            
        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Setup size
        $(this.id).css("width", (31 * 8) + "px");
        $(this.id).css("height", (28 * 8) + 'px');

        // Update select type
        this.selectType = "border";

        // Set constraints
        super.minWidth = 4 * 8;
        super.minHeight = 4 * 8;

        // Setup click callback
        super.setupClickCallback();
    }

    // Get chart
    getChart() {
        return this.chart;
    }

    // Add editable content
    addEditableContent() {

        // Create new menu sections
        let callbackThis = this;
        this.menuSections.push(
            new MenuSection(
                "General", 
                "section-" + this.componentIndex + "-1"       
            )
        );

        // Create new menu sections
        this.menuSections.push(
            new MenuSection(
                "Chart Style", 
                "section-" + this.componentIndex + "-2"       
            )
        );

        // Create general inputs
        let elementNameInput = new MenuTextInputElement(
            "element-name-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-1",
            "Component Name",
            this.elementName,
            (elementName) => {
                callbackThis.elementName = elementName;
            }
        );   

        let showGridLinesInput = new MenuCheckboxElement(
            "scatter-graph-show-grid-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Show Gridlines",
            this.displayGridLines,
            (checkboxValue)=>{
                callbackThis.displayGridLines = checkboxValue;
                this.refreshGraph();
            }
        );
       
        let showLegendInput = new MenuCheckboxElement(
            "scatter-graph-show-legend-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Show Legend",
            callbackThis.showLegend,
            (checkboxValue)=>{
                callbackThis.showLegend = checkboxValue;
                this.refreshGraph();
            }
        );

        
        let scatterColorInput = new MenuColorInput(
            "scatter-graph-point-color-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Point Color",
            this.pointColor,
            (color) => {
                callbackThis.pointColor = color;
                let numDataSets = callbackThis.chart.data.datasets.length;
                for (let i = 0; i < numDataSets; i++) {
                    callbackThis.chart.data.datasets[i].pointBorderColor = callbackThis.pointColor;
                    callbackThis.chart.data.datasets[i].pointBackgroundColor = callbackThis.pointColor;
                    callbackThis.chart.data.datasets[i].borderColor = callbackThis.pointColor;
                    callbackThis.chart.data.datasets[i].backgroundColor = callbackThis.pointColor;
                }
                callbackThis.chart.update();
            }
        );

        let pointRadiusInput = new MenuNumberWheel(
            "scatter-graph-point-radius-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Point Radius",
            this.pointRadius,
            1, 10, 0.5,
            (val) => {
                let pointRadius;
                try {
                    pointRadius = parseFloat(val);
                } catch (e) {
                    $("#scatter-graph-point-color-" + callbackThis.componentIndex + "-1").val(callbackThis.pointRadius);
                }
                callbackThis.pointRadius = pointRadius;

                let numDataSets = callbackThis.chart.data.datasets.length;
                for (let i = 0; i < numDataSets; i++) {
                    callbackThis.chart.data.datasets[i].pointRadius = pointRadius;
                }
                callbackThis.chart.update();
            }
        );    
    }

    // Update value
    updateValue(state) {
        console.log(state);

        if ('x' in state && 'y' in state) {
            let dataSet = [];
            if (state.x.length != state.y.length) {
                console.log("Unable to update scatter plot! Length of x and y arrays differ");
                return;
            }
            for (let i = 0; i < state.x.length; i++) {
                dataSet.push({
                    x: state.x[i],
                    y: state.y[i]
                });
            }
            this.chart.data.datasets[0].data = dataSet;
            this.chart.update();
        }

        if ('title' in state) {
            this.chart.data.datasets[0].label = state.title;
            this.chart.update();
        }
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "scatter-graph";
        state['showLegend'] = this.showLegend;
        state['pointColor'] = this.pointColor;
        state['pointRadius'] = this.pointRadius;
        state['displayGridLines'] = this.displayGridLines;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.showLegend = state['showLegend'];
        this.pointColor = state['pointColor'];
        this.pointRadius = state['pointRadius'];
        this.displayGridLines = state['displayGridLines'];

        if (this.showLegend == undefined) {
            this.showLegend = true;
        }

        if (this.displayGridLines == undefined) {
            this.displayGridLines = true;
        }

        if (this.pointColor == undefined) {
            this.pointColor = '#48b6fa';
        }

        if (this.pointRadius == undefined) {
            this.pointRadius = 3;
        }

        if (this.showLegend != true || !this.displayGridLines) {
            this.refreshGraph();
        }

        let numDataSets = this.chart.data.datasets.length;
        for (let i = 0; i < numDataSets; i++) {
            this.chart.data.datasets[i].pointBorderColor = this.pointColor;
            this.chart.data.datasets[i].pointBackgroundColor = this.pointColor;
            this.chart.data.datasets[i].borderColor = this.pointColor;
            this.chart.data.datasets[i].backgroundColor = this.pointColor;
            this.chart.data.datasets[i].pointRadius = this.pointRadius;
        }
        this.chart.update();
    }
}
