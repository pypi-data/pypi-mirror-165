'use strict';


// Menu Node Context
class TextArea extends Component {
    constructor(componentIndex, readonly = true) {

        // Call parent constructor
        super(componentIndex);

        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-text-area");
        $(containerDiv).attr("data-type", "component");

        // Create text area 
        let textarea = createElement("textarea", this.id.substring(1), "component-element-text-area form-control");
        if (readonly) {
            $(textarea).attr("readonly", "true");
            $(textarea).attr("disabled", "true");
        }

        // Setup features
        this.borderRadius = 0;
        this.transparentBackground = false;

        // Add text area to container and append to DOM
        containerDiv.appendChild(textarea);
        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Setup size
        $(this.id).css('width', (16 * 8) + 'px');
        $(this.id).css('height', (8 * 8) + 'px');

        // Setup min size
        super.minWidth = 8 * 8;
        super.minHeight = 4 * 8;

        // Setup click callback
        super.setupClickCallback();
    }

    // Update content
    updateValue(value) {
        $(this.id + " textarea").val(value);
    }
    
    getValue() {
        return $(this.id + " textarea").val();
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
        this.menuSections.push(
            new MenuSection(
                "Style", 
                "section-" + this.componentIndex + "-3"           
            )
        );

        // Create style elements
        let borderRadiusInput = new MenuTextInputElement(
            "textarea-border-radius-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
            "Border Radius",
            callbackThis.borderRadius,
            (borderRadius) => {
                callbackThis.borderRadius = borderRadius;
                $(callbackThis.id + " textarea").css("border-radius", borderRadius + "px");
            }
        );
        let transparentBackground = new MenuCheckboxElement(
            "input-transparent-background-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
            "Transparent Background",
            callbackThis.transparentBackground,
            (checkboxValue)=>{
                callbackThis.transparentBackground = checkboxValue;
                if (checkboxValue) {
                    $(callbackThis.id + " textarea").css("background-color", "transparent");
                } else {
                    $(callbackThis.id + " textarea").css("background-color", "#ffffff");
                }   
            }
        );
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "text area";
        state["borderRadius"] = this.borderRadius;
        state["transparentBackground"] = this.transparentBackground;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.borderRadius = state["borderRadius"];
        $(this.id + " textarea").css("border-radius", this.borderRadius + "px");
        this.transparentBackground = state["transparentBackground"];
        if (this.transparentBackground) {
            $(this.id + " textarea").css("background-color", "transparent");
        } else {
            $(this.id + " textarea").css("background-color", "#ffffff");
        }
    }
}
