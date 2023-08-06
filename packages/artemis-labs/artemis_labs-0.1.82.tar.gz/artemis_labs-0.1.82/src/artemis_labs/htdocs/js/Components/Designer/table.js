'use strict';

// Menu Node Context
class Table extends Component {

    // Helper
    populateDummyRows(tbody) {

        // Clear content of tbody
        $(tbody).empty();

        // Populate
        let dummyFirstNames = ['Bob', 'Jennah', 'John', 'Mary', 'Sara', 'Tom', 'Tim'];
        let dummyLastNames = ['Smith', 'Jones', 'Williams', 'Brown', 'Davis', 'Miller', 'Wilson'];
        let dummyHandles = ['@bob', '@jennah', '@john', '@mary', '@sara', '@tom', '@tim'];
        for( let i = 0; i < this.numberOfDummyRows; i++ ) {
            let row = ['#' + (i + 1), dummyFirstNames[i % 7], dummyLastNames[i % 7], dummyHandles[i % 7]];
            let tr = createElement("tr", "", "");
            row.forEach((item) => {
                let td = createElement("td", "", "");
                td.innerHTML = item;
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        }     
    }

    // Constructor
    constructor(componentIndex) {

        // Call parent constructor
        super(componentIndex);

        // Setup box features
        this.headerHighlighted = false;
        this.striped = true;
        this.bordered = true;
        this.hoverableRows = true;
        this.numberOfDummyRows = 2;


        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-table");
        $(containerDiv).attr("data-type", "component");

        // Create table
        let table = createElement("table", "", "table table-bordered table-striped");
        containerDiv.appendChild(table);

        // Create table header
        let thead = createElement("thead", "", "");
        table.appendChild(thead);

        // Create table header row
        let tr = createElement("tr", "", "");
        thead.appendChild(tr);
        let row1 = ['#', 'First', 'Last', 'Handle'];
        row1.forEach((item) => { let col = createElement("th", "", ""); $(col).attr("scope", "col"); col.innerHTML = item; tr.appendChild(col); });

        // Create table body
        let tbody = createElement("tbody", "", "");
        table.appendChild(tbody);

        // Create sample content
        this.populateDummyRows(tbody); 
    
        // Add div to builder
        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Setup size
        $(this.id).css("width", (40 * 8) + "px");
        $(this.id).css("height", (16 * 8) + 'px');

        // Set constraints
        super.minWidth = 8 * 8;
        super.minHeight = 4 * 8;

        // Setup click callback
        super.setupClickCallback();
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
        this.menuSections.push(
            new MenuSection(
                "Style", 
                "section-" + this.componentIndex + "-2"           
            )
        );
        this.menuSections.push(
            new MenuSection(
                "Content", 
                "section-" + this.componentIndex + "-3"           
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

        let headerHighlightedInput = new MenuCheckboxElement(
            "table-header-highlighted-input-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Header Highlighted",
            callbackThis.headerHighlighted,
            (checkboxValue)=>{
                callbackThis.headerHighlighted = checkboxValue;
                if (checkboxValue) {
                    $(callbackThis.id + ' thead').addClass("thead-light");
                } else {
                    $(callbackThis.id + ' thead').removeClass("thead-light");
                }   
            }
        );

        let stripedInput = new MenuCheckboxElement(
            "table-striped-input-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Rows Striped",
            callbackThis.striped,
            (checkboxValue)=>{
                callbackThis.striped = checkboxValue;
                if (checkboxValue) {
                    $(callbackThis.id + ' table').addClass("table-striped");
                } else {
                    $(callbackThis.id + ' table').removeClass("table-striped");

                }   
            }
        );

        let borderedInput = new MenuCheckboxElement(
            "table-bordered-input-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Table Bordered",
            callbackThis.bordered,
            (checkboxValue)=>{
                callbackThis.bordered = checkboxValue;
                if (checkboxValue) {
                    $(callbackThis.id + ' table').addClass("table-bordered");
                } else {
                    $(callbackThis.id + ' table').removeClass("table-bordered");

                }   
            }
        );

        let hoverableRowsInput = new MenuCheckboxElement(
            "table-hoverable-rows-input-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Hoverable Rows",
            callbackThis.hoverableRows,
            (checkboxValue)=>{
                callbackThis.hoverableRows = checkboxValue;
                if (checkboxValue) {
                    $(callbackThis.id + ' table').addClass("table-hover");
                } else {
                    $(callbackThis.id + ' table').removeClass("table-hover");

                }   
            }
        );

        let dummyRowsInput = new MenuNumberWheel(
            "table-dummy-rows-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
            "Number Of Dummy Rows",
            this.numberOfDummyRows,
            0, 10, 1,
            (val) => {
                callbackThis.numberOfDummyRows = parseInt(val);
                let newHeight = 40 + (40 * callbackThis.numberOfDummyRows);
                callbackThis.setHeight(newHeight);
                if (callbackThis.selectbox != null && callbackThis.selectbox != undefined) {
                    callbackThis.selectbox.setHeight(newHeight);
                }
                let tbody = qs(callbackThis.id + ' tbody');
                callbackThis.populateDummyRows(tbody);
            }
        );    

    }

    // Remove header
    removeHeader() {
        $(this.id + ' thead').remove();
    }

    // Get value
    updateValue(value) {

        // Get table header
        let headerRowDOM = qs(this.id + ' thead tr');
        if (headerRowDOM) {
            headerRowDOM.innerHTML = "";
            for (let i = 0; i < value[0].length; i++) {
                let col = createElement("th", "", "");
                $(col).attr("scope", "col");
                col.innerHTML = value[0][i];
                headerRowDOM.appendChild(col);
            }
        }

        // Get table body
        let tableBody = qs(this.id + ' tbody');
        tableBody.innerHTML = "";

        // Get header dimension
        let numColumns = qs(this.id + ' thead tr').children.length;

        // Validate
        if (value.length > 0) {
            for (let i = 0; i < value.length; i++) {
                let row = value[i];
                if (row.length != numColumns) {
                    console.log("Invalid row length");
                    return;
                }
            }
        }

        // Add rows
        for (let i = 0; i < value.length; i++) {
            let rowDOM = createElement("tr", "", "");
            let rowData = value[i];
            for (let j = 0; j < rowData.length; j++) {
                let cell = createElement("td", "", "");
                let cellContent = createElement('span','','');
                cellContent.textContent = rowData[j];
                cell.appendChild(cellContent);
                rowDOM.appendChild(cell);
            }
            tableBody.appendChild(rowDOM);
        }

        // Add filler
        console.log('Create Table: ' + this.numberOfDummyRows)
        if (value.length < this.numberOfDummyRows) {
            for (let i = value.length; i < this.numberOfDummyRows; i++) {
                let rowDOM = createElement("tr", "", "");
                for (let j = 0; j < numColumns; j++) {
                    let cell = createElement("td", "", "");
                    cell.innerHTML = "";
                    rowDOM.appendChild(cell);
                }
                tableBody.appendChild(rowDOM);
            }
        }
    }

    // Get value
    getValue() {
        console.log(this.id + " tbody tr");
        let tableRows = qsa(this.id + " tbody tr");
        let tableData = [];
        for (let i = 0; i < tableRows.length; i++) {
            let row = tableRows[i];
            let rowData = [];
            let rowCells = row.children;
            for (let j = 0; j < rowCells.length; j++) {
                let cell = rowCells[j];
                rowData.push(cell.innerHTML);
            }
            tableData.push(rowData);
        }
        return tableData;
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "table";
        state['headerHighlighted'] = this.headerHighlighted;
        state['striped'] = this.striped;
        state['bordered'] = this.bordered;
        state['hoverableRows'] = this.hoverableRows;
        state['numberOfDummyRows'] = this.numberOfDummyRows;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);

        this.headerHighlighted = state['headerHighlighted'];
        this.striped = state['striped'];
        this.bordered = state['bordered'];
        this.hoverableRows = state['hoverableRows'];
        this.numberOfDummyRows = state['numberOfDummyRows'];


        if(this.headerHighlighted) {
            this.headerHighlighted = true;
        }
        if(this.striped) {
            this.striped = true;
        }
        if(this.bordered) {
            this.bordered = true;
        }
        if(this.hoverableRows) {
            this.hoverableRows = true;
        }
        if (this.numberOfDummyRows) {
            this.numberOfDummyRows = parseInt(this.numberOfDummyRows);
        }
        
        let newHeight = 40 + (40 * this.numberOfDummyRows);
        this.setHeight(newHeight);
        let tbody = qs(this.id + ' tbody');
        this.populateDummyRows(tbody);

        if (this.headerHighlighted) {
            $(this.id + ' thead').addClass("thead-light");
        } else {
            $(this.id + ' thead').removeClass("thead-light");
        }
        if (this.striped) {
            $(this.id + ' table').addClass("table-striped");
        } else {
            $(this.id + ' table').removeClass("table-striped");
        }
        if (this.bordered) {
            $(this.id + ' table').addClass("table-bordered");
        } else {
            $(this.id + ' table').removeClass("table-bordered");
        }
        if (this.hoverableRows) {
            $(this.id + ' table').addClass("table-hover");
        } else {
            $(this.id + ' table').removeClass("table-hover");
        }
    }
}
