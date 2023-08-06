'use strict';


// Menu Node Context
class Switch extends Component {

    updateLabel() {
        if (this.labelMode == 'top') {
            $(this.id + " label").css("margin-left", "0px");
            $(this.id + " label").css("display", "block");
            $(this.id + " label").css("height", (3 * 8) + "px");
            $(this.id + " label").css("line-height", (3 * 8) + "px");
            $(this.id + " .form-group").css("display", "flex");
            $(this.id + " .form-group").css("flex-direction", "column");
            $(this.id + " .form-group").css("align-items", "start");
            $(this.id).css("max-height", (6*8) + "px");
            $(this.id).css("height", (6*8) + "px");
            if (this.selectbox != null && this.selectbox != undefined) {
                this.selectbox.setHeight(6 * 8);
            }
            this.minHeight = 6 * 8;
            this.maxHeight = 6 * 8;
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
            $(this.id + " .form-group").css("align-items", "center");
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
        this.checked = false;
        this.labelText = "Input Label";
        this.labelMode = "top";

        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-switch");
        $(containerDiv).attr("data-type", "component");
        
        // Form group
        let formGroup = createElement("div", "", "form-group");
        containerDiv.appendChild(formGroup);

        // Form Label
        let formLabel = createElement("label", "", "");
        formLabel.innerHTML = this.labelText;
        $(formLabel).attr("for", this.id + "-input");
        formGroup.appendChild(formLabel);

        // Create input div
        let inputDiv = createElement("div", "", "form-check form-switch");
        let input = createElement("input", "", "component-element-switch form-check-input");
        inputDiv.appendChild(input);
        $(input).attr("type", "checkbox");
        $(input).attr("role", "switch");
        if (readonly) {
            $(input).attr("readonly", "true");
            $(input).attr("disabled", "true");
            $(input).attr("pointer-events", "none");           
        } else {
            let callbackThis = this;
            $(input).click(() => {
                callbackThis.checked = !callbackThis.checked;
            });
        }
        formGroup.appendChild(inputDiv);


        qs("#artemis-builder").appendChild(containerDiv);   
        this.updateLabel();
        
        // Setup size
        $(this.id).css('width', (12 * 8) + 'px');
        $(this.id).css('height', (6 * 8) + 'px');

        // Set constraints
        super.minHeight = 6 * 8;
        super.maxHeight = 6 * 8;

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
                "Switch Content", 
                "section-" + this.componentIndex + "-2"           
            )
        );
        this.menuSections.push(
            new MenuSection(
                "Label Content", 
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

        // Create switch
        let elementSwitchInput = new MenuSwitchInputElement(
            "switch-state-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Switch State",
            this.checked,
            (newState) => {
                callbackThis.checked = newState;
                if (!callbackThis.checked) {
                    $(callbackThis.id + " input").prop("checked", false);
                } else {
                    $(callbackThis.id + " input").prop("checked", true);
                }
            }
        );

        let inputLabel = new MenuTextInputElement(
            "switch-label-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
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
            "switch-label-side-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
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

    // Update content
    updateValue(value) {
        this.checked = value == 'true';
        if (!this.checked) {
            $(this.id + " input").prop("checked", false);
        } else {
            $(this.id + " input").prop("checked", true);
        }
    }

    getValue() {
        return this.checked;
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "switch";
        state["checked"] = this.checked;
        state["labelText"] = this.labelText;
        state["labelMode"] = this.labelMode;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.state = state["initialValue"];
        this.checked = state["checked"];
        this.labelText = state["labelText"];
        this.labelMode = state["labelMode"];

        if (this.labelText == undefined) {
            this.labelText = "Input Label";
        }
        if (this.labelMode == undefined) {
            this.labelMode = "top";
        }

        $(this.id + " label").html(this.labelText);
        if (this.checked) {
            $(this.id + " input").prop("checked", true);
        }
        this.updateLabel();
    }
}
