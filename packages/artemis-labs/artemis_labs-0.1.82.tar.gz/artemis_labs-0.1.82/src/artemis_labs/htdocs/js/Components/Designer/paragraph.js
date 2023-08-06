'use strict';

// Menu Node Context
class Paragraph extends Component {
    constructor(componentIndex) {

        // Call parent constructor
        super(componentIndex);

        // Set paragraph text
        this.paragraphText = "Sample Text";
        this.fontSize = 1.0;
        this.paragraphAlignment = "center";
        this.fontUnit = "rem";
        this.textColor = "#000000";
        this.fontWeight = "normal";

        // Create DOM element container
        let containerDiv = createElement("div", this.id.substring(1), "component-paragraph");
        $(containerDiv).attr("data-type", "component");

        // Create paragraph with sample text
        let paragraph = createElement("p", "", "component-element-paragraph");
        paragraph.innerHTML = this.paragraphText;
        $(paragraph).css("font-weight", this.fontWeight);
        $(paragraph).css("align-items", this.paragraphAlignment);
        $(paragraph).css("text-align", this.paragraphAlignment);


        // Add paragraph to container and append to DOM
        containerDiv.appendChild(paragraph);
        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Setup size
        $(this.id).css('width', (16 * 8) + 'px');
        $(this.id).css('height', (8 * 8) + 'px');

        // Min size
        super.minHeight = 1 * 8;
        super.minWidth = 1 * 8;
        
        // Setup click callback
        super.setupClickCallback();
    }

    // Update content
    updateValue(value) {
        this.paragraphText = value;
        $(this.id + " p").text(this.paragraphText);
    }

    // Get value
    getValue() {
        return this.paragraphText;
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
        let paragraphTextArea = new MenuTextAreaElement(
            "paragraph-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-1",
            "Paragraph Text",
            callbackThis.paragraphText,
            (newText) => {
                callbackThis.paragraphText = newText;
                $(callbackThis.id + " p").html(newText.replaceAll("\n","<br>"));
            }
        );

        // Create alignment elements
        let alignmentInput = new MenuAlignElement(
            "paragraph-alignment-content-" + callbackThis.componentIndex + "-1",
            "section-" + callbackThis.componentIndex + "-2",
            "Horizontal Alignment",
            this.paragraphAlignment,
            (value) => {
                callbackThis.paragraphAlignment = value;
                $(qs(callbackThis.id + " p")).css("align-items", value);
                $(qs(callbackThis.id + " p")).css("text-align", value);
            }
        );

        // Create typography elements
        let fontSizeInput = new MenuNumberInputElement(
            "paragraph-font-size-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
            "Paragraph Font Size",
            callbackThis.fontSize,
            "rem",
            (fontSize) => {
                callbackThis.fontSize = fontSize;
                $(callbackThis.id + " p").css("font-size", callbackThis.fontSize + callbackThis.fontUnit);
            },
            (fontUnit) => {
                callbackThis.fontUnit = fontUnit;
                $(callbackThis.id + " p").css("font-size", callbackThis.fontSize + callbackThis.fontUnit);
            }
        );

        // Create menu color input
        let textColorInput = new MenuColorInput(
            "paragraph-text-color-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-4",
            "Text Color",
            this.textColor,
            (textColor)=>{
                callbackThis.textColor = textColor;
                $(callbackThis.id + " p").css("color", callbackThis.textColor);
            }
        );

        // Create font weight input
        let textWeightInput = new MenuDropDownInput(
            "paragraph-text-weight-content-" + this.componentIndex + "-1",
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
                $(callbackThis.id + " p").css("font-weight", newFontWeight);
            }
        );
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "paragraph";
        state["paragraphText"] = this.paragraphText;
        state["fontSize"] = this.fontSize;
        state["paragraphAlignment"] = this.paragraphAlignment;
        state["fontUnit"] = this.fontUnit;
        state["textColor"] = this.textColor;
        state["fontWeight"] = this.fontWeight;

        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.paragraphText = state["paragraphText"];
        this.fontSize = state["fontSize"];
        this.paragraphAlignment = state["paragraphAlignment"];
        this.fontUnit = state["fontUnit"];
        this.textColor = state["textColor"];
        this.fontWeight = state["fontWeight"];
       

        $(this.id + " p").css("color", this.textColor);
        $(this.id + " p").css("font-size", this.fontSize + this.fontUnit);
        $(qs(this.id + " p")).css("text-align", this.paragraphAlignment);
        $(qs(this.id + " p")).css("align-items", this.paragraphAlignment);
        $(this.id + " p").text(this.paragraphText);
        $(this.id + " p").css("font-weight", this.fontWeight);  
    }
}
