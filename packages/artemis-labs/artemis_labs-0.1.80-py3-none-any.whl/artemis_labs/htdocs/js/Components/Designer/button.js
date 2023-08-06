'use strict';






// Menu Node Context
class Button extends Component {

    // Constructor
    constructor(componentIndex) {

        // Call parent constructor
        super(componentIndex);

        // Next page callback
        this.nextPageCallback = null;

        // Set button features
        this.buttonText = "Press Me";
        this.fontSize = 1.0;
        this.fontUnit = "rem";
        this.nextPage = "None";
        this.textAlignment = "center";
        this.fontWeight = "normal";
        this.buttonStyle = "btn-primary";

        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-button");
        $(containerDiv).attr("data-type", "component");

        let button = createElement("button", "", "component-element-button btn " + this.buttonStyle);
        $(button).css("font-weight", this.fontWeight);
        button.innerHTML = this.buttonText;
        containerDiv.appendChild(button);
        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Setup size
        $(this.id).css('width', (10 * 8) + 'px');
        $(this.id).css('height', (4 * 8) + 'px');

         // Setup min size
         super.minWidth = 8 * 8;
         super.minHeight = 4 * 8;
         
        // Setup click callback
        super.setupClickCallback();
    }

    // Update content
    updateValue(value) {
        this.buttonText = value;
        qs(this.id + " .component-element-button").innerHTML = value;
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
                "Content", 
                "section-" + this.componentIndex + "-2"           
            )
        );

         this.menuSections.push(
            new MenuSection(
                "Style", 
                "section-" + this.componentIndex + "-5"           
            )
        );
        this.menuSections.push(
            new MenuSection(
                "Typography", 
                "section-" + this.componentIndex + "-4"           
            )
        );

        // Advanced sections
        this.menuSections.push(
            new MenuSection(
                "Connection", 
                "section-" + this.componentIndex + "-6",
                "#component-advanced-tab-body"    
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

        // Create content inputs
        let buttonNameInput = new MenuTextInputElement(
            "button-content-" + this.componentIndex + "-2",
            "section-" + this.componentIndex + "-2",
            "Text Content",
            this.buttonText,
            (newText) => {
                callbackThis.buttonText = newText;
                $(callbackThis.id + " button").text(newText);
            }
        );
        
        // Create alignment elements
        let alignmentInput = new MenuAlignElement(
            "button-alignment-content-" + callbackThis.componentIndex + "-1",
            "section-" + callbackThis.componentIndex + "-2",
            "Button Text Alignment",
            this.textAlignment,
            (value) => {
                callbackThis.textAlignment = value;
                $(qs(callbackThis.id + " button")).css("text-align", value);
            }
        );


        // Create typography elements
        let fontSizeInput = new MenuNumberInputElement(
            "button-font-size-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-4",
            "Button Font Size",
            callbackThis.fontSize,
            "rem",
            (fontSize) => {
                callbackThis.fontSize = fontSize;
                console.log(qs(callbackThis.id + " button"));
                console.log(callbackThis.fontSize + callbackThis.fontUnit);
                $(callbackThis.id + " button").css("font-size", callbackThis.fontSize + callbackThis.fontUnit);
            },
            (fontUnit) => {
                callbackThis.fontUnit = fontUnit;
                $(callbackThis.id + " button").css("font-size", callbackThis.fontSize + callbackThis.fontUnit);
            }
        );

         // Create font weight input
         let fontWeightInput = new MenuDropDownInput(
            "button-text-weight-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-4",
            "Text Weight",            
            this.fontWeight,
            {
                "Normal" : "normal",
                "Semibold " : "600",
                "Bold" : "bold"
            },
            (newFontWeight) => {
                callbackThis.fontWeight = newFontWeight;
                $(callbackThis.id + " button").css("font-weight", newFontWeight);
            }
        );

         // Create style input
         let buttonStyleInput = new MenuDropDownInput(
            "button-style-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-5",
            "Button Style",            
            this.buttonStyle,
            {
                "Primary" : "btn-primary",
                "Secondary" : "btn-secondary",
                "Success" : "btn-success",
                "Danger" : "btn-danger",
                "Warning " : "btn-warning",
                "Info" : "btn-info",
                "Light" : "btn-light",
                "Dark" : "btn-dark"
            },
            (buttonStyleClass) => {
                callbackThis.buttonStyle = buttonStyleClass;
                $(callbackThis.id + " button").removeClass();
                $(callbackThis.id + " button").addClass("component-element-button btn " + buttonStyleClass);
            }
        );

        // Create next page element
        let pages = qsa(".page-item span");
        let pageMap = {};
        pageMap['None'] = "None";
        for (let i = 0; i < pages.length; i++) {
            let pageName = $(pages[i]).text();
            pageMap[pageName] = pageName;
        }
        let nextPageInput = new MenuDropDownInput(
            "button-next-page-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-6",
            "Connect To Page",            
            this.nextPage,
            pageMap,
            (nextPage) => {
                callbackThis.nextPage = nextPage;
            }
        );
      
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "button";
        state["buttonText"] = this.buttonText;
        state["fontUnit"] = this.fontUnit;
        state["fontSize"] = this.fontSize;
        state["nextPage"] = this.nextPage;
        state["textAlignment"] = this.textAlignment;
        state["fontWeight"] = this.fontWeight;
        state["buttonStyle"] = this.buttonStyle;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.buttonText = state["buttonText"];
        this.fontUnit = state["fontUnit"];
        this.fontSize = state["fontSize"];
        this.nextPage = state["nextPage"];
        this.textAlignment = state["textAlignment"];
        this.fontWeight = state["fontWeight"];
        this.buttonStyle = state["buttonStyle"];

        if(this.fontWeight == undefined) {
            this.fontWeight = "normal";
        }
        if(this.buttonStyle == undefined) {
            this.buttonStyle = "btn-primary";
        }

        $(this.id + " button").text(this.buttonText);
        qs(this.id + " button").innerHTML = this.buttonText;
        $(this.id + " button").css("font-size", this.fontSize + this.fontUnit);
        $(qs(this.id + " button")).css("text-align", this.textAlignment);
        $(this.id + " button").css("font-weight", this.fontWeight);  
        $(this.id + " button").removeClass();
        $(this.id + " button").addClass("component-element-button btn " + this.buttonStyle);
    }

    // Bind next page
    bindNextPageCallback(callback) {
        this.nextPageCallback = callback;
    }
}
