'use strict';

// Menu Node Context
class Range extends Component {

    
    updateLabel() {
        if (this.labelMode == 'top') {
            $(this.id + " label").css("margin-left", "0px");
            $(this.id + " label").css("display", "block");
            $(this.id + " label").css("height", (3 * 8) + "px");
            $(this.id + " label").css("line-height", (3 * 8) + "px");
            $(this.id + " .form-group").css("display", "flex");
            $(this.id + " .form-group").css("flex-direction", "column");
            $(this.id).css("max-height", (6*8) + "px");
            $(this.id).css("height", (6*8) + "px");
            $(this.id + " .range").css("display", "flex");
            $(this.id + " .range").css("align-items", "start");
            if (this.selectbox != null && this.selectbox != undefined) {
                this.selectbox.setHeight(6 * 8);
            }
            this.minHeight = 6 * 8;
            this.maxHeight = 6 * 8;
        } else if (this.labelMode == "none") {
            $(this.id + " label").css("display", "none");                    
            $(this.id).css("max-height", (3 * 8) + "px");
            $(this.id).css("height", (3 * 8) + "px")
            if (this.selectbox != null && this.selectbox != undefined) {
                this.selectbox.setHeight(3 * 8);
            }
            this.minHeight = 3 * 8;
            this.maxHeight = 3 * 8;
        } else if (this.labelMode == "left") {
            $(this.id + " label").css("margin-left", "8px");
            $(this.id + " label").css("height", (3 * 8) + "px");
            $(this.id + " label").css("line-height", (3 * 8) + "px");
            $(this.id + " label").css("display", "block");
            $(this.id + " .form-group").css("display", "flex");
            $(this.id + " .form-group").css("flex-direction", "row");
            $(this.id + " .range").css("display", "flex");
            $(this.id + " .range").css("align-items", "center");

            $(this.id).css("max-height", (3 * 8) + "px");
            $(this.id).css("height", (3 * 8) + "px")
            if (this.selectbox != null && this.selectbox != undefined) {
                this.selectbox.setHeight(3 * 8);
            }
            if($(this.id + " label").width() % 8 != 0) {
                let correction = (8 - ($(this.id + " label").width() % 8));
                $(this.id + " label").css("margin-left", correction);
            }
            this.minHeight = 3 * 8;
            this.maxHeight = 3 * 8;
        }   
    }
    
    constructor(componentIndex, readonly = true) {

        // Call parent constructor
        super(componentIndex);

        // Set input features
        this.min = 0;
        this.max = 10;
        this.step = 1;
        this.val = 0;
        this.labelText = "Slider Label";
        this.labelMode = "top";

        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-range");     
        $(containerDiv).attr("data-type", "component");

        // Form group
        let formGroup = createElement("div", "", "form-group");
        containerDiv.appendChild(formGroup);

        // Form Label
        let formLabel = createElement("label", "", "");
        formLabel.innerHTML = this.labelText;
        $(formLabel).attr("for", this.id + "-input");
        formGroup.appendChild(formLabel);

        // Range div
        let rangeDiv = createElement("div", "", "range");
        $(rangeDiv).css("display", "flex");
        $(rangeDiv).css("flex-direction", "row");
        formGroup.appendChild(rangeDiv);

        // Create input 
        let input = createElement("input", "", "form-range component-element-range");
        rangeDiv.appendChild(input);
        $(input).attr("min", this.min);
        $(input).attr("max", this.max);
        $(input).val(this.val);
        $(input).attr("step", this.step);
        $(input).attr("type", "range");
        if (readonly) {
            $(input).attr("readonly", "true");
            $(input).attr("disabled", "true");
        }       
        
        // Enable itself
        new mdb.Range(rangeDiv);
     
        // Add to DOM
        qs("#artemis-builder").appendChild(containerDiv);      
        this.updateLabel();  
                
        // Setup size
        $(this.id).css('width', (16 * 8) + 'px');
        $(this.id).css('height', (6 * 8) + 'px');

        // Set constraints
        super.minWidth = 8 * 8;
        super.minHeight = 6 * 8;
        super.maxHeight = 6 * 8;

        // Setup click callback
        super.setupClickCallback();
    }

    // Update content
    updateValue(state) {
        const value = parseFloat(state);
        let fraction = 100 * (value - this.min) / (this.max - this.min);
        let perTickOffset = 15 / ((this.max - this.min) / this.step);
        let tickOffset = 8 - (value - this.min) / this.step;
        $(this.id + " input").val(value);
        $(this.id + " .thumb-value").html(value);
        $(this.id + " .thumb").css('left', 'calc(' + fraction + '% - ' + tickOffset + 'px)');
    }

    // Get value
    getValue() {
        return $(this.id + " input").val();
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
                "Slider Content", 
                "section-" + this.componentIndex + "-2"           
            )
        );

        this.menuSections.push(
            new MenuSection(
                "Label Content", 
                "section-" + this.componentIndex + "-4"           
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

        let valInput = new MenuTextInputElement(
            "input-val-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Starting Value",
            callbackThis.val,
            (val) => {
                callbackThis.val = val;
                $(callbackThis.id + " input").val(val);
            }
        );

        let minInput = new MenuTextInputElement(
            "input-min-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Range Minimum",
            callbackThis.min,
            (val) => {
                callbackThis.min = val;
                $(callbackThis.id + " input").attr("min", val);
                $(callbackThis.id + " input").val(callbackThis.val);
            }
        );

        let maxInput = new MenuTextInputElement(
            "input-min-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Range Maximum",
            callbackThis.max,
            (val) => {
                callbackThis.max = val;
                $(callbackThis.id + " input").attr("max", val);
                $(callbackThis.id + " input").val(callbackThis.val);
            }
        );

        let stepInput = new MenuTextInputElement(
            "input-min-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Step Size",
            callbackThis.step,
            (val) => {
                callbackThis.step = val;
                $(callbackThis.id + " input").attr("step", val);
                $(callbackThis.id + " input").val(callbackThis.val);
            }
        );

        let inputLabel = new MenuTextInputElement(
            "slider-label-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-4",
            "Label Text",
            this.labelText,
            (newText) => {
                callbackThis.labelText = newText;
                qs(callbackThis.id + " label").innerHTML = newText;
                if($(this.id + " label").width() % 8 != 0) {
                    let correction = (8 - ($(this.id + " label").width() % 8));
                    $(this.id + " label").css("margin-left", correction);
                }
            }
        );

        let inputLabelSide = new MenuDropDownInput(
            "slider-label-side-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-4",
            "Label Mode",            
            this.labelMode,
            {
                "Top" : "top",
                "Left " : "left",
                "None" : "none"
            },
            (labelMode) => {

                callbackThis.labelMode = labelMode;
                callbackThis.updateLabel();
            }
        );
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "range";
        state["min"] = this.min;
        state["max"] = this.max;
        state["step"] = this.step;
        state["val"] = this.val;
        state["labelText"] = this.labelText;
        state["labelMode"] = this.labelMode;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        
        this.min = state["min"];
        this.max = state["max"];
        this.step = state["step"];
        this.val = state["val"];
        this.labelText = state["labelText"];
        this.labelMode = state["labelMode"];

        if (this.labelText == undefined) {
            this.labelText = "Input Label";
        }
        if (this.labelMode == undefined) {
            this.labelMode = "top";
        }

        $(this.id + " label").html(this.labelText);
        $(this.id + " input").attr("min", this.min);
        $(this.id + " input").attr("max", this.max);
        $(this.id + " input").attr("step", this.step);
        $(this.id + " input").val(this.val);
        $(this.id + " output").val(this.val);
        this.updateLabel();
    }
}
