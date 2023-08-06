'use strict';




// Menu Node Context
class HorizontalRule extends Component  {
    constructor(componentIndex) {

        // Call parent constructor
        super(componentIndex);

        // Setup features
        this.borderStyle = "normal";

        // Create DOM element container
        let containerDiv = createElement("div", this.id.substring(1), "component-hr");
        $(containerDiv).attr("data-type", "component");

        // Create simulated hr element 
        let hr = createElement("hr", this.id.substring(1), "component-element-hr divider-horizontal");

        // Add to container and append to DOM
        containerDiv.appendChild(hr);
        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Set size
        $(this.id).css('width', (16 * 8) + 'px');
        $(this.id).css('height', (1 * 8) + 'px');

        // Set constraints
        super.minWidth = 2 * 8;
        super.minHeight = 1 * 8;
        super.maxHeight = 1 * 8;

        // Setup click callback
        super.setupClickCallback();

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

        this.menuSections.push(
            new MenuSection(
                "Style", 
                "section-" + this.componentIndex + "-2"           
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

        let borderStyleInput = new MenuDropDownInput(
            "hr-border-style-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Border Style",            
            this.borderStyle,
            {
                "Normal" : "normal",
                "Blurry" : "blurry"
            },
            (borderStyle) => {
                callbackThis.borderStyle = borderStyle;
                if(borderStyle != "normal") {
                    $(callbackThis.id + " > hr").attr('class', 'component-element-hr divider-horizontal-blurry');
                } else {
                    $(callbackThis.id + " > hr").attr('class', 'component-element-hr divider-horizontal');
                }
            }
        );
    }
    
    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "horizontal rule";
        state["borderStyle"] = this.borderStyle;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.borderStyle = state["borderStyle"];
        if(this.borderStyle != "normal") {
            $(this.id + " > hr").attr('class', 'component-element-hr divider-horizontal-blurry');
        } else {
            $(this.id + " > hr").attr('class', 'component-element-hr divider-horizontal');
        }
    }
}

