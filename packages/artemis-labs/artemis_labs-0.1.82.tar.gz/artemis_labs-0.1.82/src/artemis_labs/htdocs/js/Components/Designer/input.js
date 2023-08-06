'use strict';


// Menu Node Context
class Input extends Component {

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
        this.placeholderText = "Input";
        this.inputType = "text";
        this.labelText = "Input Label";
        this.labelMode = "top";

        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-input");
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
        let input = createElement("input", this.id.substring(1) + '-input', "component-element-input form-control");
        $(input).attr("type", this.inputType);
        $(input).attr("name", "input");
        $(input).attr("placeholder", this.placeholderText);
        if (readonly) {
            $(input).attr("readonly", "true");
            $(input).attr("disabled", "true");
        }
        formGroup.appendChild(input);

        containerDiv.appendChild(formGroup);
        qs("#artemis-builder").appendChild(containerDiv);        
        this.updateLabel();
        
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
        this.menuSections.push(
            new MenuSection(
                "Style", 
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

        // Create placeholder text input
        let inputPlaceholder = new MenuTextInputElement(
            "input-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Placeholder Text",
            callbackThis.placeholderText,
            (newText) => {
                callbackThis.placeholderText = newText;
                $(callbackThis.id + " input").attr("placeholder", newText);
            }
        );

         // Input type
         let inputType = new MenuDropDownInput(
            "input-text-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
            "Input Type",            
            this.inputType,
            {
                "Text" : "text",
                "Email " : "email",
                "Password" : "password"
            },
            (inputType) => {
                callbackThis.inputType = inputType;
                $(callbackThis.id + " input").attr("type", inputType);
            }
        );

        let inputLabel = new MenuTextInputElement(
            "input-label-content-" + this.componentIndex + "-1",
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
            "input-label-side-" + this.componentIndex + "-1",
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
        state["type"] = "input";
        state["placeholderText"] = this.placeholderText;
        state["inputType"] = this.inputType;
        state["labelText"] = this.labelText;
        state["labelMode"] = this.labelMode;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.placeholderText = state["placeholderText"];
        this.inputType = state["inputType"];
        this.labelText = state["labelText"];
        this.labelMode = state["labelMode"];

        if (this.labelText == undefined) {
            this.labelText = "Input Label";
        }

        if (this.labelMode == undefined) {
            this.labelMode = "top";
        }

        $(this.id + " label").html(this.labelText);
        $(this.id + " input").text(this.buttonText);
        $(this.id + " input").attr("placeholder", this.placeholderText);
        $(this.id + " input").attr("type", this.inputType);
        this.updateLabel();
    }
}
