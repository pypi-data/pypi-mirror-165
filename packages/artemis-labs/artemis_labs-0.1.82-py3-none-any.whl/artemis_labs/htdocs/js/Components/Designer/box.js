'use strict';




// Menu Node Context
class Box extends Component {

    // Constructor
    constructor(componentIndex, acceptPointerEvents=true) {

        // Call parent constructor
        super(componentIndex);

        // Setup box features
        this.borderRadius = 0;
        this.borderWidth = 1;
        this.borderColor = "#000000";
        this.borderStyle = "dashed";
        
        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-box");
        $(containerDiv).attr("data-type", "component");
        if (!acceptPointerEvents) {
            $(containerDiv).css("pointer-events", "none");
        }
        $(containerDiv).css("border-color", this.borderColor);
        $(containerDiv).css("border-style", this.borderStyle);

        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Setup size
        $(this.id).css("width", (16 * 8) + "px");
        $(this.id).css("height", (4 * 8) + 'px');

        // Update select type
        this.selectType = "border";

        // Set constraints
        super.minWidth = 1 * 8;
        super.minHeight = 1 * 8;

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
                "Border", 
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

        // Create style inputs
        let borderRadiusInput = new MenuTextInputElement(
            "button-border-radius-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Border Radius (px)",
            callbackThis.borderRadius,
            (borderRadius) => {
                callbackThis.borderRadius = borderRadius;
                $(callbackThis.id).css("border-radius", borderRadius + "px");
            }
        );
        let borderWidthInput = new MenuTextInputElement(
            "button-border-width-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Border Width",
            callbackThis.borderWidth,
            (borderWidth) => {
                callbackThis.borderWidth = borderWidth;
                $(callbackThis.id).css("border-width", borderWidth + "px");
            }
        );      
        let borderStyleInput = new MenuDropDownInput(
            "button-border-style-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Border Style",            
            this.borderStyle,
            {
                "Solid" : "solid",
                "Dotted" : "dotted",
                "Dashed" : "dashed",
                "Double" : "double",
                "Groove" : "groove",
                "Ridge" : "ridge",
                "Inset" : "inset",
                "Outset" : "outset"
            },
            (borderStyle) => {
                callbackThis.borderStyle = borderStyle;
                $(callbackThis.id).css("border-style", borderStyle);
            }
        );
        let borderColor = new MenuColorInput(
            "button-border-color-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Border Color",
            this.borderColor,
            (borderColor)=>{
                callbackThis.borderColor = borderColor;
                $(callbackThis.id).css("border-color", callbackThis.borderColor);
            }
        );
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "box";
        state["borderRadius"] = this.borderRadius;
        state["borderWidth"] = this.borderWidth;
        state["borderColor"] = this.borderColor;
        state["borderStyle"] = this.borderStyle;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.borderRadius = state["borderRadius"];
        this.borderWidth = state["borderWidth"];
        this.borderColor = state["borderColor"];
        this.borderStyle = state["borderStyle"];
        this.backgroundColor = state["backgroundColor"];

        $(this.id).css("border-radius", this.borderRadius + "px");
        $(this.id).css("border-width", this.borderWidth + "px");
        $(this.id).css("border-color", this.borderColor);
        $(this.id).css("border-style", this.borderStyle);
        $(this.id).css("background-color", "transparent");
    }
}
