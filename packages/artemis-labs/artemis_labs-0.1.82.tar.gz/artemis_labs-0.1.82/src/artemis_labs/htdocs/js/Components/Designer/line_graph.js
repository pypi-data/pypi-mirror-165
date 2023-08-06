'use strict';

// Menu Node Context
class LineGraph extends Component {

    // Build graph
    buildGraph(ctx = null) {
        if (ctx == null) {
            ctx = qs(this.id + " canvas").getContext('2d');
        }
        const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
        const data = {
          labels: labels,
          datasets: [{
            label: 'My First Dataset',
            borderDash: [],
            data: [65, 59, 80, 81, 56, 55, 40],
            fill: false,
            borderColor: '#48b6fa',
            tension: 0.1
          }]
        };
        const config = {
            type: 'line',
            data: data,
        };
        this.chart = new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                maintainAspectRatio: false,
                plugins : {
                    legend: this.showLegend
                },
                scales: {
                    x: {
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

        // Settings
        this.showLines = true;
        this.fill = false;
        this.tension = 0.1;
        this.lineColor = "#48b6fa";
        this.borderDash = [];
        this.displayGridLines = true;
        this.showLegend = true;

        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-line-graph");
        $(containerDiv).attr("data-type", "component");

        // Create graph
        let graphCanvas = createElement("canvas", "", "graph-canvas");
        containerDiv.appendChild(graphCanvas);
        $(graphCanvas).css("width", "100%");
        $(graphCanvas).css("height", "100%");
        this.buildGraph(graphCanvas.getContext('2d'));
        
       
        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Setup size
        $(this.id).css("width", (40 * 8) + "px");
        $(this.id).css("height", (20 * 8) + 'px');

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

        // Create chart styles
        let showGridLinesInput = new MenuCheckboxElement(
            "line-graph-show-grid-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Show Gridlines",
            this.displayGridLines,
            (checkboxValue)=>{
                callbackThis.displayGridLines = checkboxValue;
                this.refreshGraph();
            }
        );

        let showlineInput = new MenuCheckboxElement(
            "line-graph-show-line-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Show Line",
            callbackThis.showLines,
            (checkboxValue)=>{
                callbackThis.showLines = checkboxValue;
                if (checkboxValue) {
                    let numDataSets = callbackThis.chart.data.datasets.length;
                    for (let i = 0; i < numDataSets; i++) {
                        callbackThis.chart.data.datasets[i].showLine = true;
                    }
                    callbackThis.chart.update();
                } else {
                    let numDataSets = callbackThis.chart.data.datasets.length;
                    $("#line-graph-fill-" + callbackThis.componentIndex + "-1-input").prop("checked", false);
                    for (let i = 0; i < numDataSets; i++) {
                        callbackThis.chart.data.datasets[i].fill = false;
                    }
                    callbackThis.chart.update();
                    for (let i = 0; i < numDataSets; i++) {
                        callbackThis.chart.data.datasets[i].showLine = false;
                    }
                    callbackThis.chart.update();
                }   
            }
        );

        let fillInput = new MenuCheckboxElement(
            "line-graph-fill-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Fill Graph",
            callbackThis.fill,
            (checkboxValue)=>{
                callbackThis.fill = checkboxValue;
                if (checkboxValue) {
                    let numDataSets = callbackThis.chart.data.datasets.length;
                    for (let i = 0; i < numDataSets; i++) {
                        callbackThis.chart.data.datasets[i].fill = true;
                    }
                    callbackThis.chart.update();
                } else {
                    let numDataSets = callbackThis.chart.data.datasets.length;
                    for (let i = 0; i < numDataSets; i++) {
                        callbackThis.chart.data.datasets[i].fill = false;
                    }
                    callbackThis.chart.update();
                }   
            }
        );

        let tensionInput = new MenuNumberWheel(
            "line-graph-tension-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Tension",
            this.tension,
            0, 1, 0.05,
            (tension) => {
                let tensionNumerical;
                try {
                    tensionNumerical = parseFloat(tension);
                } catch (e) {
                    $("#line-graph-tension-" + callbackThis.componentIndex + "-1").val(callbackThis.tension);
                }
                callbackThis.tension = tension;
                let numDataSets = callbackThis.chart.data.datasets.length;
                for (let i = 0; i < numDataSets; i++) {
                    callbackThis.chart.data.datasets[i].lineTension = tensionNumerical;
                }
                console.log(callbackThis.chart.data.datasets);
                callbackThis.chart.update();
            }
        );    

        let lineColorInput = new MenuColorInput(
            "line-graph-line-color-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Line Color",
            this.lineColor,
            (color) => {
                callbackThis.lineColor = color;
                let numDataSets = callbackThis.chart.data.datasets.length;
                for (let i = 0; i < numDataSets; i++) {
                    callbackThis.chart.data.datasets[i].borderColor = color;
                }
                callbackThis.chart.update();
            }
        );

        let borderDashInput = new MenuNumberWheel(
            "line-graph-border-dash-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Line Dash Width",
            (this.borderDash.length == 0) ? 0 : this.borderDash[0],
            0, 20, 1,
            (input) => {
                let borderDash;
                try {
                    borderDash = parseInt(input);
                } catch (e) {
                    if (callbackThis.borderDash == []) {
                        $("#line-graph-border-dash-" + callbackThis.componentIndex + "-1").val(0);
                    } else {
                        $("#line-graph-border-dash-" + callbackThis.componentIndex + "-1").val(callbackThis.borderDash[0]);
                    }
                }
                if (input > 0) {
                    callbackThis.borderDash = [borderDash];
                    let numDataSets = callbackThis.chart.data.datasets.length;
                    for (let i = 0; i < numDataSets; i++) {
                        callbackThis.chart.data.datasets[i].borderDash = callbackThis.borderDash;
                    }
                    callbackThis.chart.update();   
                } else {
                    callbackThis.borderDash = [];
                    let numDataSets = callbackThis.chart.data.datasets.length;
                    for (let i = 0; i < numDataSets; i++) {
                        callbackThis.chart.data.datasets[i].borderDash = callbackThis.borderDash;
                    }
                    callbackThis.chart.update();   
                }             
            }
        );    
        console.log(this.showLegend);

        let showLegendInput = new MenuCheckboxElement(
            "line-graph-show-legend-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Show Legend",
            this.showLegend,
            (checkboxValue)=>{
                callbackThis.showLegend = checkboxValue;
                this.refreshGraph();
            }
        );
    }

    // Update value
    updateValue(data) {
        console.log(this.chart);
        if ('x' in data) {
            this.chart.data.labels = data.x;
        }
        if ('y' in data && 'index' in data) {
            this.chart.data.datasets[data.index].data = data.y;
        }
        if ('title' in data) {
            this.chart.data.datasets[0].label = data.title;
        }
        this.chart.update();
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "line-graph";
        state['tension'] = this.tension;
        state['lineColor'] = this.lineColor;
        state['fill'] = this.fill;
        state['showLines'] = this.showLines;
        state['showLegend'] = this.showLegend;
        state['displayGridLines'] = this.displayGridLines;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);

        this.tension = state['tension'];
        this.lineColor = state['lineColor'];
        this.fill = state['fill'];
        this.showLines = state['showLines'];
        this.showLegend = state['showLegend'];
        this.displayGridLines = state['displayGridLines'];

        if (this.showLegend == undefined) {
            this.showLegend = true;
        }

        if (this.displayGridLines == undefined) {
            this.displayGridLines = true;
        }

        if (!this.showLegend || !this.displayGridLines) {
            this.refreshGraph();
        }

        let numDataSets = this.chart.data.datasets.length;
        for (let i = 0; i < numDataSets; i++) {
            this.chart.data.datasets[i].lineTension = this.tension;
            this.chart.data.datasets[i].borderColor = this.lineColor;
            this.chart.data.datasets[i].fill = this.fill;
            this.chart.data.datasets[i].showLine = this.showLines;
        }
        this.chart.update();
    }
}

