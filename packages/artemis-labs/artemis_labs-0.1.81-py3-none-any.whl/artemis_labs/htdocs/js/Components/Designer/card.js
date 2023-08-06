'use strict';

// Menu Node Context
class Card extends Component {

    // Constructor
    constructor(componentIndex) {

        // Call parent constructor
        super(componentIndex);

        // Setup box features
        this.borderRadius = 8;
        this.borderWidth = 1;
        this.borderColor = "#eeeeee";
        this.borderStyle = "solid";
        this.backgroundColor = "#fefefe";
        this.headerTextColor = "#000000";
        this.headerColor = "#fefefe";
        this.boxShadow = true;
        this.cardTitle = "Card Title";
        this.cardTitleAlignment = "center";
        this.cardHeaderEnabled = true;
        this.cardHeaderBorderEnabled = true;
        this.elementName = "card";

        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-card");
        $(containerDiv).css("display", 'flex');
        $(containerDiv).css("align-items", 'start');
        $(containerDiv).attr("data-type", "component");
        if (this.boxShadow) {
            $(containerDiv).css("box-shadow", "rgba(99, 99, 99, 0.2) 0px 2px 8px 0px");
        }
        $(containerDiv).css("border-color", this.borderColor);
        if (this.backgroundColor != "#fefefe") {
            $(containerDiv).css("background-color", this.backgroundColor);
        }
        $(containerDiv).css("border-radius", this.borderRadius);

        // Create header section
        let headerDiv = createElement("div", "", "card-header");
        $(headerDiv).css("display", 'flex');
        $(headerDiv).css("align-items", 'center');
        $(headerDiv).css("justify-content", 'center');
        $(headerDiv).css('width', '100%');
        $(headerDiv).css('padding-top', '12px');
        $(headerDiv).css('padding-bottom', '12px');
        $(headerDiv).css("padding-left", '18px');
        $(headerDiv).css("padding-right", '18px');
        $(headerDiv).css('border-bottom-width', '1px');
        $(headerDiv).css('border-bottom-color', 'var(--light-grey)');
        $(headerDiv).css('border-bottom-style', 'solid');
        if (this.headerColor != "#fefefe") {
            $(headerDiv).css("background-color", this.headerColor);
        }
        $(headerDiv).css("border-top-left-radius", this.borderRadius);
        $(headerDiv).css("border-top-right-radius", this.borderRadius);

        $(containerDiv).append(headerDiv);

        // Create title
        let titleDiv = createElement("h5", "", "card-title");
        $(titleDiv).text(this.cardTitle);
        $(titleDiv).css('word-break', 'break-all');
        $(titleDiv).css("position", "relative");
        $(titleDiv).css("top", "0px");
        $(titleDiv).css("left", "0px");
        $(titleDiv).css("color", this.headerTextColor);
        $(headerDiv).append(titleDiv);
            
        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Setup size
        $(this.id).css("width", (20 * 8) + "px");
        $(this.id).css("height", (12 * 8) + 'px');

        // Update select type
        this.selectType = "border";

        // Set constraints
        super.minWidth = 2 * 8;
        super.minHeight = 6 * 8;

        // Setup click callback
        super.setupClickCallback();
    }

    // Update content
    updateValue(value) {
        this.cardTitle = value;
        qs(this.id + " .card-title").textContent = value;
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
                "Card Header", 
                "section-" + this.componentIndex + "-2"       
            )
        );
        this.menuSections.push(
            new MenuSection(
                "Style", 
                "section-" + this.componentIndex + "-3"           
            )
        );
        this.menuSections.push(
            new MenuSection(
                "Background", 
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


        let titleInput = new MenuTextInputElement(
            "title-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Card Title",
            callbackThis.cardTitle,
            (val) => {
                callbackThis.cardTitle = val;
                $(callbackThis.id + " h5").text(callbackThis.cardTitle);
            }
        );

        // Create alignment elements
        let alignmentInput = new MenuAlignElement(
            "card-title-alignment-content-" + callbackThis.componentIndex + "-1",
            "section-" + callbackThis.componentIndex + "-2",
            "Card Title Alignment",
            this.cardTitleAlignment,
            (value) => {
                callbackThis.cardTitleAlignment = value;
                $(qs(callbackThis.id + " > div")).css("justify-content", callbackThis.cardTitleAlignment);
            }
        );

        let cardHeaderEnabled = new MenuCheckboxElement(
            "card-header-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Card Header",
            callbackThis.cardHeaderEnabled,
            (checkboxValue)=>{
                callbackThis.cardHeaderEnabled = checkboxValue;
                if (checkboxValue) {
                    $(callbackThis.id + " > div").css("display", "flex");
                } else {
                    $(callbackThis.id + " > div").css("display", "none");
                }   
            }
        );

        let cardHeaderBorderEnabled = new MenuCheckboxElement(
            "card-header-border-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Card Header Border",
            callbackThis.cardHeaderBorderEnabled,
            (checkboxValue)=>{
                callbackThis.cardHeaderBorderEnabled = checkboxValue;
                if (checkboxValue) {
                    $(callbackThis.id + " > div").css("border-bottom-width", "1px");
                } else {
                    $(callbackThis.id + " > div").css("border-bottom-width", "0px");
                }   
            }
        );

        let cardHeaderColor = new MenuColorInput(
            "header-bg-color-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Header Background Color",
            this.headerColor,
            (headerColor)=>{
                console.log('here');
                callbackThis.headerColor = headerColor;
                $(callbackThis.id + ' > div').css("background-color", callbackThis.headerColor);
            }
        );

        let cardHeaderTextColor = new MenuColorInput(
            "header-text-color-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Header Text Color",
            this.headerTextColor,
            (headerTextColor)=>{
                callbackThis.headerTextColor = headerTextColor;
                $(callbackThis.id + ' > div > h5').css("color", callbackThis.headerTextColor);
            }
        );

        // Create style inputs
        let showBoxShadow = new MenuCheckboxElement(
            "card-box-shadow-background-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
            "Box Shadow",
            this.boxShadow,
            (checkboxValue)=>{
                callbackThis.boxShadow = checkboxValue;
                if (checkboxValue) {
                    $(callbackThis.id).css("box-shadow", "rgba(99, 99, 99, 0.2) 0px 2px 8px 0px");
                } else {
                    $(callbackThis.id).css("box-shadow", "none");
                }   
            }
        );
        let borderRadiusInput = new MenuTextInputElement(
            "button-border-radius-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
            "Border Radius (px)",
            this.borderRadius,
            (borderRadius) => {
                callbackThis.borderRadius = borderRadius;
                $(callbackThis.id).css("border-radius", borderRadius + "px");
                $(callbackThis.id + " > div").css("border-top-left-radius", borderRadius + "px");
                $(callbackThis.id + " > div").css("border-top-right-radius ", borderRadius + "px");
            }
        );
        let borderWidthInput = new MenuTextInputElement(
            "button-border-width-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
            "Border Width",
            this.borderWidth,
            (borderWidth) => {
                callbackThis.borderWidth = borderWidth;
                $(callbackThis.id).css("border-width", borderWidth + "px");
            }
        );      
        let borderStyleInput = new MenuDropDownInput(
            "button-border-style-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
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
            "section-" + this.componentIndex + "-3",
            "Border Color",
            this.borderColor,
            (borderColor)=>{
                callbackThis.borderColor = borderColor;
                $(callbackThis.id).css("border-color", callbackThis.borderColor);
            }
        );

        let bgColor = new MenuColorInput(
            "button-bg-color-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-4",
            "Background Color",
            this.backgroundColor,
            (backgroundColor)=>{
                callbackThis.backgroundColor = backgroundColor;
                $(callbackThis.id).css("background-color", callbackThis.backgroundColor);
            }
        );
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "card";
        state['cardTitle'] = this.cardTitle;
        state["borderRadius"] = this.borderRadius;
        state["borderWidth"] = this.borderWidth;
        state["borderColor"] = this.borderColor;
        state["borderStyle"] = this.borderStyle;
        state["backgroundColor"] = this.backgroundColor;
        state["boxShadow"] = this.boxShadow;
        state["cardTitleAlignment"] = this.cardTitleAlignment;
        state["cardHeaderEnabled"] = this.cardHeaderEnabled;
        state["cardHeaderBorderEnabled"] = this.cardHeaderBorderEnabled;
        state["headerColor"] = this.headerColor;
        state["headerTextColor"] = this.headerTextColor;
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
        this.boxShadow = state["boxShadow"];
        this.cardTitle = state["cardTitle"];
        this.cardTitleAlignment = state["cardTitleAlignment"];
        this.cardHeaderEnabled = state["cardHeaderEnabled"];
        this.cardHeaderBorderEnabled = state["cardHeaderBorderEnabled"];
        this.headerColor = state["headerColor"];
        this.headerTextColor = state["headerTextColor"];

        if (this.headerColor == undefined) {
            this.headerColor = "#fefefe";
        }
        if (this.headerTextColor == undefined) {
            this.headerTextColor = "#000000";
        }
        if (this.backgroundColor == undefined) {
            this.backgroundColor = "#fefefe";
        }
        if (this.cardHeaderEnabled == undefined) {
            this.cardHeaderEnabled = true;
        }
        if (this.cardTitle == undefined) {
            this.cardTitle = "Card Title";
        }
        if(this.boxShadow == undefined) {
            this.boxShadow = true;
        }
        if(this.cardTitleAlignment == undefined) {
            this.cardTitleAlignment = "center";
        }
        if(this.cardHeaderBorderEnabled == undefined) {
            this.cardHeaderBorderEnabled = true;
        }


        if (this.cardHeaderBorderEnabled) {
            $(this.id + " > div").css("border-bottom-width", "1px");
        } else {
            $(this.id + " > div").css("border-bottom-width", "0px");
        }

        if (this.cardHeaderEnabled) {
            $(this.id + " > div").css("display", "flex");
        } else {
            $(this.id + " > div").css("display", "none");
        }
        $(this.id + " > div").css("justify-content", this.cardTitleAlignment);
        $(this.id + ' .card-title').text(this.cardTitle);
        $(this.id).css("border-radius", this.borderRadius + "px");
        $(this.id + " > div").css("border-top-left-radius", this.borderRadius + "px");
        $(this.id + " > div").css("border-top-right-radius ", this.borderRadius + "px");
        $(this.id).css("border-width", this.borderWidth + "px");
        $(this.id).css("border-color", this.borderColor);
        $(this.id).css("border-style", this.borderStyle);
        if (this.backgroundColor != "#fefefe") {
            console.log(this.backgroundColor);
            $(this.id).css("background-color", this.backgroundColor);
        }
        if (this.headerColor != "#fefefe") {
            $(this.id + " > div").css("background-color", this.headerColor);
        }
        $(this.id + " > div > h5").css("color", this.headerTextColor);
        if (this.boxShadow) {
            $(this.id).css("box-shadow", "rgba(99, 99, 99, 0.2) 0px 2px 8px 0px");
        }
    }
}
