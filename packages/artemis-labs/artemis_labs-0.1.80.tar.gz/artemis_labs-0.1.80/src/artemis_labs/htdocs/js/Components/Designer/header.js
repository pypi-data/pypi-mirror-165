'use strict';







// Menu Node Context
class Header extends Component {
    constructor(componentIndex) {

        // Call parent constructor
        super(componentIndex);

        // Set heading text
        this.headingText = "Sample Text";
        this.fontSize = 1.0;
        this.headingAlignment = "center";
        this.fontUnit = "rem";
        this.textColor = "#000000";
        this.fontWeight = "normal";

        // Create DOM element container
        let containerDiv = createElement("div", this.id.substring(1), "component-header");
        $(containerDiv).attr("data-type", "component");

        // Create header with sample text
        let header = createElement("h1", "", "component-element-header");
        header.innerHTML = this.headingText;
        $(header).css("font-weight", this.fontWeight);
        $(header).css("align-items", this.headingAlignment);
        $(header).css("text-align", this.headingAlignment);

        // Add header to container and append to DOM
        containerDiv.appendChild(header);
        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Setup size
        $(this.id).css('width', (10 * 8) + 'px');
        $(this.id).css('height', (4 * 8) + 'px');
          
        // Min size
        super.minHeight = 1 * 8;
        super.minWidth = 1 * 8;

        // Setup click callback
        super.setupClickCallback();
    }

     // Update content
    updateValue(value) {
        this.headingText = value;
        $(this.id + " h1").text(value);
    }

    // Get value
    getValue() {
        return $(this.id + " h1").text();
    }

    // Add editable content
    addEditableContent() {

        // Callback
        let callbackThis = this;

        // Create menu sections
        this.menuSections.push(
            new MenuSection(
                "General", 
                "section-" + this.componentIndex + "-0"           
            )
        );

        this.menuSections.push(
            new MenuSection(
                "Content", 
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
                "Typography", 
                "section-" + this.componentIndex + "-3"           
            )
        );

        this.menuSections.push(
            new MenuSection(
                "Colors", 
                "section-" + this.componentIndex + "-4"           
            )
        );

        // Create general elements
        let elementNameInput = new MenuTextInputElement(
            "element-name-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-0",
            "Component Name",
            this.elementName,
            (elementName) => {
                callbackThis.elementName = elementName;
            }
        );

        // Create content elements
        let headerTextInput = new MenuTextInputElement(
            "header-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-1",
            "Header Text",
            callbackThis.headingText,
            (newText) => {
                callbackThis.headingText = newText;
                $(callbackThis.id + " h1").text(newText);
            }
        );

        // Create alignment elements
        let alignmentInput = new MenuAlignElement(
            "header-alignment-content-" + callbackThis.componentIndex + "-1",
            "section-" + callbackThis.componentIndex + "-2",
            "Horizontal Alignment",
            this.headingAlignment,
            (value) => {
                callbackThis.headingAlignment = value;
                $(qs(callbackThis.id + " h1")).css("align-items", value);
                $(qs(callbackThis.id + " h1")).css("text-align", value);
            }
        );

        // Create typography elements
        let fontSizeInput = new MenuNumberInputElement(
            "header-font-size-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
            "Header Font Size",
            callbackThis.fontSize,
            "rem",
            (fontSize) => {
                callbackThis.fontSize = fontSize;
                $(callbackThis.id + " h1").css("font-size", callbackThis.fontSize + callbackThis.fontUnit);
            },
            (fontUnit) => {
                callbackThis.fontUnit = fontUnit;
                $(callbackThis.id + " h1").css("font-size", callbackThis.fontSize + callbackThis.fontUnit);
            }
        );

        // Create menu color input
        let textColorInput = new MenuColorInput(
            "header-text-color-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-4",
            "Text Color",
            this.textColor,
            (textColor)=>{
                callbackThis.textColor = textColor;
                $(callbackThis.id + " h1").css("color", callbackThis.textColor);
            }
        );

        // Create font weight input
        let textWeightInput = new MenuDropDownInput(
            "header-text-weight-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
            "Text Weight",            
            this.fontWeight,
            {
                "Normal" : "normal",
                "Semibold " : "600",
                "Bold" : "bold"
            },
            (newFontWeight) => {
                callbackThis.fontWeight = newFontWeight;
                $(callbackThis.id + " h1").css("font-weight", newFontWeight);
            }
        );
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "heading";
        state["headingText"] = this.headingText;
        state["fontSize"] = this.fontSize;
        state["headingAlignment"] = this.headingAlignment;
        state["fontUnit"] = this.fontUnit;
        state["textColor"] = this.textColor;
        state["fontWeight"] = this.fontWeight;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.headingText = state["headingText"];
        this.fontSize = state["fontSize"];
        this.headingAlignment = state["headingAlignment"];
        this.fontUnit = state["fontUnit"];
        this.textColor = state["textColor"];
        this.fontWeight = state["fontWeight"];


        $(this.id + " h1").css("color", this.textColor);
        $(this.id + " h1").css("font-size", this.fontSize + this.fontUnit);
        $(qs(this.id + " h1")).css("align-items", this.headingAlignment);
        $(qs(this.id + " h1")).css("text-align", this.headingAlignment);
        $(this.id + " h1").text(this.headingText);
        $(this.id + " h1").css("font-weight", this.fontWeight);  
    }
}
