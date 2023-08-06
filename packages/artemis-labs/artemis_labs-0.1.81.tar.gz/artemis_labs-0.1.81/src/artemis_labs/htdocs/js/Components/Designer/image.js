'use strict';





// Menu Node Context
class Image extends Component {
    constructor(componentIndex) {

        // Call parent constructor
        super(componentIndex);

        // Setup features
        this.imageURL = "";
        this.imageTiling = "no-repeat";
        this.imageFit = "contain";
        this.imagePosition = "center";
        this.borderRadius = 0;
        this.borderWidth = 1;
        this.borderColor = "#dee2e6";
        this.borderStyle = "dashed";
        this.showImageInDesigner = true;

        // Create DOM element container 
        let containerDiv = createElement("div", this.id.substring(1), "component-image");
        $(containerDiv).attr("data-type", "component");
        $(containerDiv).css("background-repeat", this.imageTiling);
        $(containerDiv).css("background-size", this.imageFit);
        $(containerDiv).css("background-position", this.imagePosition);
        $(containerDiv).css("border-width", this.borderWidth + "px");
        $(containerDiv).css("border-style", this.borderStyle);
        $(containerDiv).css("border-color", this.borderColor);

        // Create DOM element
        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Setup size
        $(this.id).css('width', (16 * 8) + 'px');
        $(this.id).css('height', (16 * 8) + 'px');

        // Min size
        super.minHeight = 3 * 8;
        super.minWidth = 3 * 8;

        // Init click callback
        this.clickCallback = null;

        // Setup click callback
        super.setupClickCallback();
    }

    // Update content
    updateValue(value) {
        this.imageURL = value;
        if (this.imageURL != "") {
            $(this.id).css("background-image", "url(" + this.imageURL + ")");
            $(this.id).css("border-width", "0px");
        } else {
            $(this.id).css("border-width", "1px");
        }
    }

    // Get value
    getValue() {
        return this.imageURL;
    }

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
                "Content", 
                "section-" + this.componentIndex + "-2"           
            )
        );
        
 
        let imageURLNameElement = new MenuTextElement(
            "image-url-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Image URL:",
            this.imageURL
        );

     
        let urlInput = new URLInput(
            "file-input-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Upload an Image",
            this.imageURL,
            (imageURL) => {
                callbackThis.imageURL = imageURL;
                imageURLNameElement.setText(imageURL);                
                if (callbackThis.showImageInDesigner) {
                    $(callbackThis.id).css("background-image", "url(" + callbackThis.imageURL + ")");
                    $(callbackThis.id).css("border-width", "0px");                
                }                
            }
        );

        let showImageInDesignerInput = new MenuCheckboxElement(
            "img-show-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Show image is designer",
            this.showImageInDesigner,
            (checkboxValue)=>{                
                if (checkboxValue) {
                    callbackThis.showImageInDesigner = true;
                    $(callbackThis.id).css("background-image", "url(" + callbackThis.imageURL + ")");
                    $(callbackThis.id).css("border-width", "0px");
                } else {
                    callbackThis.showImageInDesigner = false;
                    $(callbackThis.id).css("background-image", "none");
                    $(callbackThis.id).css("border-width", "1px");               
                 }   
            }
        );


        this.menuSections.push(
            new MenuSection(
                "Style", 
                "section-" + this.componentIndex + "-3"           
            )
        );

        let imageFitInput = new MenuDropDownInput(
            "image-fit-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
            "Image Fit",            
            this.imageFit,
            {
                "Original Size" : "auto",
                "Contain" : "contain",
                "Cover" : "cover"
            },
            (imageFit) => {
                $(callbackThis.id).css("border-width", "0px");
                callbackThis.imageFit = imageFit;
                $(callbackThis.id).css("background-size", imageFit);
            }
        );

        let imageTilingInput = new MenuDropDownInput(
            "image-tiling-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
            "Image Tiling",            
            this.imageTiling,
            {
                "Repeat XY" : "repeat",
                "Repeat X" : "repeat-x",
                "Repeat Y" : "repeat-y", 
                "No Repeat" : "no-repeat", 
                "Space" : "space"
            },
            (imageTiling) => {
                callbackThis.imageTiling = imageTiling;
                $(callbackThis.id).css("background-repeat", imageTiling);
            }
        );

        let imagePositionInput = new MenuDropDownInput(
            "image-position-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-3",
            "Image Position",            
            this.imagePosition,
            {
                "Center" : "center",
                "Left" : "left",
                "Right" : "right",
                "Top" : "top",
                "Bottom" : "bottom",
                "Center" : "center"
            },
            (imagePosition) => {
                callbackThis.imagePosition = imagePosition;
                $(callbackThis.id).css("background-position", imagePosition);
            }
        );

        this.menuSections.push(
            new MenuSection(
                "Border", 
                "section-" + this.componentIndex + "-4"           
            )
        );

         // Create style inputs
         let borderRadiusInput = new MenuTextInputElement(
            "image-border-radius-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-4",
            "Border Radius (px)",
            callbackThis.borderRadius,
            (borderRadius) => {
                console.log('here');
                callbackThis.borderRadius = borderRadius;
                $(callbackThis.id).css("border-radius", borderRadius + "px");
            }
        );
        let borderWidthInput = new MenuTextInputElement(
            "image-border-width-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-4",
            "Border Width",
            callbackThis.borderWidth,
            (borderWidth) => {
                callbackThis.borderWidth = borderWidth;
                $(callbackThis.id).css("border-width", borderWidth + "px");
            }
        );      
        let borderStyleInput = new MenuDropDownInput(
            "image-border-style-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-4",
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
            "section-" + this.componentIndex + "-4",
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
        state["type"] = "image";
        state['imageURL'] = this.imageURL;
        state['imageTiling'] = this.imageTiling;
        state['imageFit'] = this.imageFit;
        state['imagePosition'] = this.imagePosition;
        state["borderRadius"] = parseInt(this.borderRadius);
        state["borderWidth"] = this.borderWidth;
        state["borderColor"] = this.borderColor;
        state["borderStyle"] = this.borderStyle;
        state["showImageInDesigner"] = this.showImageInDesigner;
        return state;
    }

    // Load state
    loadState(state) {        
        super.loadState(state);
        this.imageURL = state['imageURL'];
        this.imageTiling = state['imageTiling'];
        this.imageFit = state['imageFit'];
        this.imagePosition = state['imagePosition'];
        this.borderRadius = state["borderRadius"];
        this.borderWidth = state["borderWidth"];
        this.borderColor = state["borderColor"];
        this.borderStyle = state["borderStyle"];
        this.showImageInDesigner = state["showImageInDesigner"];

        if(this.imageTiling == undefined) {
            this.imageTiling = "no-repeat";
        }

        if(this.imageFit == undefined) {
            this.imageFit = "contain";
        }

        if(this.imageURL == undefined) {
            this.imageURL = "";
        }

        if(this.imagePosition == undefined) {
            this.imagePosition = "center";
        }

        if (this.borderRadius == undefined) {
            this.borderRadius = "0";
        }

        if (this.borderWidth == undefined) {
            this.borderWidth = "1";
        }

        if (this.borderColor == undefined) {
            this.borderColor = "#dee2e6";
        }

        if (this.borderStyle == undefined) {
            this.borderStyle = "dashed";
        }

        if (this.showImageInDesigner == undefined) {
            this.showImageInDesigner = true;
        }

        $(this.id).css("border-width", this.borderWidth + "px");
        $(this.id).css("border-color", this.borderColor);
        $(this.id).css("border-style", this.borderStyle);
        $(this.id).css("border-radius", this.borderRadius + "px");
        $(this.id + " img").css("border-radius", this.borderRadius + "px");
        $(this.id).css("background-position", this.imagePosition);
        $(this.id).css("background-repeat", this.imageTiling);
        $(this.id).css("background-size", this.imageFit);
        if (this.imageURL != "" && this.showImageInDesigner) {
            $(this.id).css("background-image", "url(" + this.imageURL + ")");
            $(this.id).css("border-width", "0px");
        } else {
            $(this.id).css("border-width", "1px");
        }
    }
}
