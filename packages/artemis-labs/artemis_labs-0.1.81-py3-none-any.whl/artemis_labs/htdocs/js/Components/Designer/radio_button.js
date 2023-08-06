'use strict';


// Menu Node Context
class RadioButton extends Component {
    constructor(componentIndex) {

        // Call parent constructor
        super(componentIndex);

        // Radio button name and group
        this.label = "Radio Button";
        this.group = "Group 1";
        this.alignment = "left";
        this.textColor = "#000000";

        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-radio-button form-check");
        $(containerDiv).attr("data-type", "component");
        
        // Create radio button
        let radio = createElement("input", this.id.substring(1), "component-element-radio-button form-check-input");
        $(radio).attr("type", "radio");
        $(radio).attr("name", "radio-button");
        $(radio).attr("value", "radio-button");

        // Create label for radio button
        let label = createElement("label", this.id.substring(1), "component-element-radio-button-label form-check-label");
        $(label).attr("for", "radio-button");
        $(label).text(this.label);

        // Add radio button and label to container and append to DOM
        containerDiv.appendChild(radio);
        containerDiv.appendChild(label);
        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Setup size
        $(this.id).css('width', (16 * 8) + 'px');
        $(this.id).css('height', (4 * 8) + 'px');

        // Setup size
        super.minWidth = 4 * 8;
        super.minHeight = 3 * 8;
        super.maxHeight = 3 * 8;

        // Setup click callback
        super.setupClickCallback();
    }

    // Update content
    updateValue(value) {
        const checked = value == 'true';
        $(this.id + " input").prop("checked", checked);
    }

    // Get value
    getValue() {
        if ($(this.id + " input").prop("checked")) {
            return true;
        }
        return false;
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
                "section-" + this.componentIndex + "-3"           
            )
        );

        this.menuSections.push(
            new MenuSection(
                "Colors", 
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

        // Create content inputs
        let labelInput = new MenuTextInputElement(
            "radio-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Label",
            callbackThis.label,
            (newText) => {
                callbackThis.label = newText;
                $(callbackThis.id + " label").text(newText);
            }
        );

        // Create group name
        let groupInput = new MenuTextInputElement(
            "radio-content-" + this.componentIndex + "-2",
            "section-" + this.componentIndex + "-2",
            "Radio Button Group",
            callbackThis.group,
            (newText) => {
                callbackThis.group = newText;
            }
        );

        // Create alignment inputs
        let alignmentInput = new MenuAlignElement(
            "radio-alignment-content-" + callbackThis.componentIndex + "-1",
            "section-" + callbackThis.componentIndex + "-3",
            "Alignment",
            this.alignment,
            (value) => {
                callbackThis.alignment = value;
                $(qs(callbackThis.id + " input").parentElement).css("justify-content", value);
            }
        );

        // Create menu color input
        let textColorInput = new MenuColorInput(
            "radio-text-color-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-4",
            "Text Color",
            this.textColor,
            (textColor)=>{
                callbackThis.textColor = textColor;
                $(callbackThis.id).css("color", callbackThis.textColor);
            }
        );
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "radio button";
        state["label"] = this.label;
        state["group"] = this.group;
        state["alignment"] = this.alignment;
        state["textColor"] = this.textColor;
        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.label = state["label"];
        this.textColor = state["textColor"];
        this.group = state["group"];
        this.alignment = state["alignment"];

        $(this.id + " label").text(this.label);
        $(qs(this.id + " input").parentElement).css("justify-content", this.alignment);
        $(this.id + " input").css("color", this.textColor);
        $(this.id).css("color", this.textColor);
        $(this.id + " input").attr("name", this.group);
    }
}
