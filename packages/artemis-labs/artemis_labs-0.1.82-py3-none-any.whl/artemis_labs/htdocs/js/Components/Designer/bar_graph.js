'use strict';

// Menu Node Context
class BarGraph extends Component {

    // Build graph
    buildGraph(ctx = null) {
        if (ctx == null) {
            ctx = qs(this.id + " canvas").getContext('2d');
        }
        this.chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                datasets: [{
                    label: '# of Votes',
                    data: [12, 19, 3, 5, 2, 3],
                    backgroundColor: [
                        this.barColor,
                        this.barColor,
                        this.barColor,
                        this.barColor,
                        this.barColor,
                        this.barColor
                    ],
                    borderColor: [
                        this.borderColor,
                        this.borderColor,
                        this.borderColor,
                        this.borderColor,
                        this.borderColor,
                        this.borderColor
                    ],
                    borderWidth: this.borderWidth,
                }]
            },
            options: {
                indexAxis: this.indexAxis,
                maintainAspectRatio : false,
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

        // Save features
        this.borderWidth = 1;
        this.indexAxis = 'x';
        this.showLegend = true;
        this.displayGridLines = true;
        this.barColor = "#48b6fa";
        this.borderColor = "#48b6fa";

        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-bar-graph");
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
        
        let barStyle = new MenuDropDownInput(
            "bar-graph-bar-style-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Bar Style",            
            this.indexAxis,
            {
                "Vertical" : "x",
                "Horizontal" : "y"
            },
            (val) => {
                callbackThis.indexAxis = val;
                callbackThis.refreshGraph();
            }
        );


        let barColorInput = new MenuColorInput(
            "bar-graph-bar-color-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Bar Color",
            this.barColor,
            (color) => {
                callbackThis.barColor = color;
                let numDataSets = callbackThis.chart.data.datasets.length;
                for (let i = 0; i < numDataSets; i++) {
                    callbackThis.chart.data.datasets[i].backgroundColor = color;
                }
                callbackThis.chart.update();
            }
        );

        let barBorderColorInput = new MenuColorInput(
            "bar-graph-border-color-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Bar Border Color",
            this.borderColor,
            (color) => {
                callbackThis.borderColor = color;
                let numDataSets = callbackThis.chart.data.datasets.length;
                for (let i = 0; i < numDataSets; i++) {
                    callbackThis.chart.data.datasets[i].borderColor = color;
                }
                callbackThis.chart.update();
            }
        );

             
        let borderWidth = new MenuNumberWheel(
            "bar-graph-border-width-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Bar Border Width",
            this.borderWidth,
            0, 10, 1,
            (val) => {
                let borderWidth;
                try {
                    borderWidth = parseFloat(val);
                } catch (e) {
                    $("#bar-graph-border-width-" + callbackThis.componentIndex + "-1").val(callbackThis.borderWidth);
                }
                callbackThis.borderWidth = borderWidth;
                let numDataSets = callbackThis.chart.data.datasets.length;
                for (let i = 0; i < numDataSets; i++) {
                    callbackThis.chart.data.datasets[i].borderWidth = borderWidth;
                }
                callbackThis.chart.update();
            }
        );    

        let showLegendInput = new MenuCheckboxElement(
            "bar-graph-show-legend-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Show Legend",
            this.showLegend,
            (checkboxValue)=>{
                callbackThis.showLegend = checkboxValue;
                this.refreshGraph();
            }
        );

        let showGridLinesInput = new MenuCheckboxElement(
            "bar-graph-show-grid-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Show Gridlines",
            this.displayGridLines,
            (checkboxValue)=>{
                callbackThis.displayGridLines = checkboxValue;
                this.refreshGraph();
            }
        );
    }

    // Update value
    updateValue(data) {
        if ('labels' in data && 'title' in data && 'y' in data) {
            this.chart.data.labels = data.labels;
            this.chart.data.datasets[0].data = data.y;
            this.chart.data.datasets[0].label = data.title;
        }
        this.chart.update();
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "bar-graph";
        state["borderWidth"] = this.borderWidth;
        state['indexAxis'] = this.indexAxis;
        state['showLegend'] = this.showLegend;
        state['displayGridLines'] = this.displayGridLines;
        state['barColor'] = this.barColor;
        state['borderColor'] = this.borderColor;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.borderWidth = state["borderWidth"];
        this.indexAxis = state['indexAxis'];
        this.showLegend = state['showLegend'];
        this.displayGridLines = state['displayGridLines'];
        this.barColor = state['barColor'];
        this.borderColor = state['borderColor'];

        if (this.borderColor == null) {
            this.borderColor = "#48b6fa";
        }
        if (this.barColor == null) {
            this.barColor = "#48b6fa";
        }
        
        if (this.displayGridLines == undefined) {
            this.displayGridLines = true;
        }

        if (this.borderWidth == undefined) {
            this.borderWidth = 1;
        }
        if (this.indexAxis == undefined) {
            this.indexAxis = 'x';
        }
        if (this.showLegend == undefined) {
            this.showLegend = true;
        }

        if (this.indexAxis != 'x' || this.showLegend != true || !this.displayGridLines) {
            this.refreshGraph();
        }

        let numDataSets = this.chart.data.datasets.length;
        for (let i = 0; i < numDataSets; i++) {
            this.chart.data.datasets[i].borderWidth = this.borderWidth;
            this.chart.data.datasets[i].backgroundColor = this.barColor;
            this.chart.data.datasets[i].borderColor = this.borderColor;
        }
        this.chart.update();
    }
}
