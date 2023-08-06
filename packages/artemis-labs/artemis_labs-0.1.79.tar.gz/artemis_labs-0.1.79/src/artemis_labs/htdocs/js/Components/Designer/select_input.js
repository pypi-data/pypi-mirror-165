'use strict';


// Menu Node Context
class SelectInput extends Component {

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

        // Select options
        this.selectOptions = [];
        this.placeholderText = "Select an option";
        this.labelText = "Dropdown Label";
        this.labelMode = "top";

        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-select-input");
        $(containerDiv).attr("data-type", "component");

        // Form group
        let formGroup = createElement("div", "", "form-group");
        containerDiv.appendChild(formGroup);

        // Form Label
        let formLabel = createElement("label", "", "");
        formLabel.innerHTML = this.labelText;
        $(formLabel).attr("for", this.id + "-input");
        formGroup.appendChild(formLabel);

           
        // Create select dropdown
        let select = createElement("select", "", "form-select component-element-select-input");

        // Create placeholder option
        let placeholderOption = createElement("option", "", "");
        $(placeholderOption).attr("value", "");
        $(placeholderOption).prop('selected', true);
        $(placeholderOption).prop('disabled', true);
        $(placeholderOption).text("Select an option");
        $(select).append(placeholderOption);
        formGroup.appendChild(select);

        // Add select dropdown to container and append to DOM
        containerDiv.appendChild(formGroup);
        qs("#artemis-builder").appendChild(containerDiv);  
        this.updateLabel();  
        
        // Prevent dropdown form opening when clicked
        if (readonly) {
            $(this.id + " select").on('mousedown', function(e) {
                e.preventDefault();
                this.blur();
                window.focus();
            });
        }
        
        // Setup size
        $(this.id).css('width', (19 * 8) + 'px');
        $(this.id).css('height', (7 * 8) + 'px');

        // Init click callback
        this.clickCallback = null;

        // Set constraints
        super.minWidth = 8 * 8;
        super.minHeight = 7 * 8;
        super.maxHeight = 7 * 8;

        // Setup click callback
        super.setupClickCallback();
    }

    updateValue(state) {
        return $(this.id + " select").val(state);
    }

    getValue() {
        return $(this.id + " select").val();
    }

    // Add editable content
    addEditableContent() {

        // Create new menu section for content
        let callbackThis = this;
        this.menuSections.push(
            new MenuSection(
                "General", 
                "section-" + this.componentIndex + "-1"           
            )
        );

        // Create name input
        let elementNameInput = new MenuTextInputElement(
            "element-name-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-1",
            "Component Name",
            this.elementName,
            (elementName) => {
                callbackThis.elementName = elementName;
            }
        );

        // Create new menu section for options
        this.menuSections.push(
            new MenuSection(
                "Content", 
                "section-" + this.componentIndex + "-2"           
            )
        );

        this.menuSections.push(
            new MenuSection(
                "Label Content", 
                "section-" + this.componentIndex + "-4"           
            )
        );

        // Create new menu section for options
        this.menuSections.push(
            new MenuSection(
                "Dropdown Options", 
                "section-" + this.componentIndex + "-3"           
            )
        );

        let placeHolderTextInput = new MenuTextInputElement(
            "placeholder-text-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Placeholder Text",
            this.placeholderText,
            (placeholderText) => {
                callbackThis.placeholderText = placeholderText;
                $(this.id + " option").text(callbackThis.placeholderText);
            }
        );

        // Create multiple input
        this.multipleInput = new MultipleInputElement(
            "section-" + this.componentIndex + "-3",
            (state) => {
                
                // clear options
                let options = qsa(this.id + " select");
                for(let i = 1; i < options.length; i++) {
                    $(options[i]).remove();
                }

                // Update select options
                callbackThis.selectOptions = state;

                // Update select dropdown
                for(let i = 0; i < state.length; i++) {
                    $(this.id + " select").append(new Option(state[i], state[i]));
                }
            },
            callbackThis.selectOptions
        );

        let inputLabel = new MenuTextInputElement(
            "select-label-content-" + this.componentIndex + "-1",
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
            "select-label-side-" + this.componentIndex + "-1",
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
        state["type"] = "select input";
        state["selectOptions"] = this.selectOptions;
        state["placeholderText"] = this.placeholderText;
        state["labelText"] = this.labelText;
        state["labelMode"] = this.labelMode;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.selectOptions = state["selectOptions"] ;
        let options = qsa(this.id + " option");
        this.labelText = state["labelText"];
        this.labelMode = state["labelMode"];
        this.placeholderText = state["placeholderText"];

        if (this.labelText == undefined) {
            this.labelText = "Input Label";
        }

        if (this.labelMode == undefined) {
            this.labelMode = "top";
        }
        if(this.placeholderText == undefined) {
            this.placeholderText = "Select an option";
        }
        $(options[0]).text(this.placeholderText);

        $(this.id + " label").html(this.labelText);
        for(let i = 1; i < options.length; i++) {
            $(options[i]).remove();
        }
        for(let i = 0; i < this.selectOptions.length; i++) {
            $(this.id + " select").append(new Option(this.selectOptions[i], this.selectOptions[i]));
        }
        this.updateLabel();
    }
}
