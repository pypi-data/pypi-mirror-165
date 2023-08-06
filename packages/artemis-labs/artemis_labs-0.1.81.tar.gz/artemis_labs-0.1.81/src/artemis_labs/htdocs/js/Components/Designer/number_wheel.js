'use strict';




// Menu Node Context
class NumberWheel extends Component {

    updateLabel() {
        if (this.labelMode == 'top') {
            $(this.id + " label").css("margin-left", "0px");
            $(this.id + " label").css("display", "block");
            $(this.id + " label").css("height", (3 * 8) + "px");
            $(this.id + " label").css("line-height", (3 * 8) + "px");
            $(this.id + " .form-group").css("display", "flex");
            $(this.id + " .form-group").css("flex-direction", "column");
            $(this.id).css("max-height", (7*8) + "px");
            $(this.id).css("height", (7*8) + "px");
            if (this.selectbox != null && this.selectbox != undefined) {
                this.selectbox.setHeight(7 * 8);
            }
            this.minHeight = 7 * 8;
            this.maxHeight = 7 * 8;
        } else if (this.labelMode == "none") {
            $(this.id + " label").css("display", "none");                    
            $(this.id).css("max-height", (4*8) + "px");
            $(this.id).css("height", (4*8) + "px")
            if (this.selectbox != null && this.selectbox != undefined) {
                this.selectbox.setHeight(4 * 8);
            }
            this.minHeight = 4 * 8;
            this.maxHeight = 4 * 8;
        } else if (this.labelMode == "left") {
            $(this.id + " label").css("margin-left", "8px");
            $(this.id + " label").css("height", (4 * 8) + "px");
            $(this.id + " label").css("line-height", (4 * 8) + "px");
            $(this.id + " label").css("display", "block");
            $(this.id + " .form-group").css("display", "flex");
            $(this.id + " .form-group").css("flex-direction", "row");
            $(this.id).css("max-height", (4*8) + "px");
            $(this.id).css("height", (4*8) + "px")
            if (this.selectbox != null && this.selectbox != undefined) {
                this.selectbox.setHeight(4 * 8);
            }
            if($(this.id + " label").width() % 8 != 0) {
                let correction = (8 - ($(this.id + " label").width() % 8));
                $(this.id + " label").css("margin-left", correction);
            }
            this.minHeight = 4 * 8;
            this.maxHeight = 4 * 8;
        }   
    }
    
    constructor(componentIndex, readonly = true) {

        // Call parent constructor
        super(componentIndex);

        // Set input features
        this.initialValue = 0;
        this.inputType = "number";
        this.stepSize = 1.0;
        this.minimum = 0;
        this.maximum = 100;
        this.labelText = "Input Label";
        this.labelMode = "top";

        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-number-wheel");
        $(containerDiv).attr("data-type", "component");
        
        // Form group
        let formGroup = createElement("div", "", "form-group");
        containerDiv.appendChild(formGroup);

        // Form Label
        let formLabel = createElement("label", "", "");
        formLabel.innerHTML = this.labelText;
        $(formLabel).attr("for", this.id + "-input");
        formGroup.appendChild(formLabel);

        // Create input 
        let input = createElement("input", this.id + "-input", "component-element-number-wheel form-control");
        $(input).attr("type", this.inputType);
        $(input).attr("name", "input");
        $(input).val(this.initialValue);
        if (readonly) {
            $(input).attr("readonly", "true");
            $(input).attr("disabled", "true");
            $(input).attr("pointer-events", "none");
        }
        formGroup.appendChild(input);

        qs("#artemis-builder").appendChild(containerDiv);        
        this.updateLabel();

        // Callback
        let callbackThis = this;
        $(input).on("input", (event) => {
            let newValue = $(event.target).val();
            if(newValue > callbackThis.maximum) {
                $(input).val(callbackThis.maximum);
            }
            if(newValue < callbackThis.minimum) {
                $(input).val(callbackThis.minimum);
            }
        });
        
        // Setup size
        $(this.id).css('width', (16 * 8) + 'px');
        $(this.id).css('height', (7 * 8) + 'px');

        // Set constraints
        super.minWidth = 8 * 8;
        super.minHeight = 7 * 8;
        super.maxHeight = 7 * 8;

        // Setup click callback
        super.setupClickCallback();
    }

    // Update content
    updateValue(value) {
        $(this.id + '-input').val(value);
    }

    // Get value
    getValue() {
        return $(this.id + '-input').val();
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
                "Input Content", 
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

        // Create placeholder text input
        let initialValue = new MenuTextInputElement(
            "number-wheel-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Initial Value",
            this.initialValue,
            (newValue) => {
                callbackThis.initialValue = newValue;
                $(callbackThis.id + " input").val(callbackThis.initialValue);
            }
        );

        // Create step input
        let stepSizeInput = new MenuTextInputElement(
            "step-size-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Step Size",
            this.stepSize,
            (newValue) => {
                callbackThis.stepSize = newValue;
                $(callbackThis.id + " input").attr('step', callbackThis.stepSize);
            }
        );

         // Minimum input
         let minimumInput = new MenuTextInputElement(
            "minimum-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Minimum",
            this.minimum,
            (newValue) => {
                callbackThis.minimum = newValue;
            }
        );

        // Minimum input
        let maximumInput = new MenuTextInputElement(
            "maximum-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Maximum",
            this.maximum,
            (newValue) => {
                callbackThis.maximum = newValue;
            }
        );     
        
        let inputLabel = new MenuTextInputElement(
            "number-wheel-label-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-4",
            "Label Text",
            this.labelText,
            (newText) => {
                callbackThis.labelText = newText;
                qs(callbackThis.id + " label").innerHTML = newText;
                if($(callbackThis.id + " label").width() % 8 != 0) {
                    let correction = (8 - ($(this.id + " label").width() % 8));
                    $(callbackThis.id + " label").css("margin-left", correction);
                }
            }
        );

        let inputLabelSide = new MenuDropDownInput(
            "number-wheel-label-side-" + this.componentIndex + "-1",
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
        state["type"] = "number-wheel";
        state["initialValue"] = this.initialValue;
        state["stepSize"] = this.stepSize;
        state["minimum"] = this.minimum;
        state["maximum"] = this.maximum;
        state["labelText"] = this.labelText;
        state["labelMode"] = this.labelMode;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.initialValue = state["initialValue"];
        this.stepSize = state["stepSize"];
        this.inputType = state["inputType"];
        this.minimum = state["minimum"];
        this.maximum = state["maximum"];
        this.labelText = state["labelText"];
        this.labelMode = state["labelMode"];

        if (this.stepSize == undefined) {
            this.stepSize = 1;
        }
        if (this.initialValue == undefined) {
            this.initialValue = 0;
        }
        if (this.minimum == undefined) {
            this.minimum = 0;
        }
        if (this.maximum == undefined) {
            this.maximum = 100;
        }
        if (this.labelText == undefined) {
            this.labelText = "Input Label";
        }
        if (this.labelMode == undefined) {
            this.labelMode = "top";
        }

        $(this.id + " label").html(this.labelText);
        $(this.id + " input").text(this.buttonText);
        $(this.id + " input").val(this.initialValue);
        $(this.id + " input").attr("step", this.stepSize);
        this.updateLabel();
    }
}
