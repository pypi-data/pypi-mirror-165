'use strict';





// Menu Node Context
class Checkbox extends Component{
    constructor(componentIndex, readonly=true) {

        // Call parent constructor
        super(componentIndex);

        // Checkbox label
        this.checkboxLabel = "Checkbox";
        this.alignment = "left";
        this.textColor = "#000000";

        // Create DOM element container 
        let containerDiv = createElement("div", this.id.substring(1), "form-check component-checkbox");
        $(containerDiv).attr("data-type", "component");

        // Create checkbox
        let checkBox = createElement("input", "", "form-check-input");
        $(checkBox).attr("type", "checkbox");
        $(checkBox).attr("name", "checkbox");
        $(checkBox).attr("value", "Checkbox");

        // Create checkbox label
        let label = createElement("label", "", "form-check-label");
        $(label).attr("for", "checkbox");
        $(label).text(this.checkboxLabel);

        // Prevent checkbox from interacting
        if (readonly) {
            $(checkBox).click((e) => {
                e.stopPropagation();
                return false;
            });

            $(this.id + " input").on('mousedown', function(e) {
                e.preventDefault();
                this.blur();
                window.focus();
            });
        }

        // Append checkbox and label to container, and add to DOM
        containerDiv.appendChild(checkBox);
        containerDiv.appendChild(label);
        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Setup size
        $(this.id).css('width', (16 * 8) + 'px');
        $(this.id).css('height', (4 * 8) + 'px');

        // Setup min size
        super.minWidth = 8 * 8;
        super.minHeight = 4 * 8;
        super.maxHeight = 4 * 8;

        // Setup click callback
        super.setupClickCallback();       
    }

    // Get value
    getValue() {
        return $(this.id + " input").prop("checked");
    }

    // Update content
    updateValue(value) {
        const checked = value == 'true';
        $(this.id + " input").prop("checked", checked);
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
        let textContent = new MenuTextInputElement(
            "text-content-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Text Content",
            this.checkboxLabel,
            (newText) => {
                callbackThis.checkboxLabel = newText;
                $(callbackThis.id + " label").text(newText);
            }
        );

        // Create alignment inputs
        let alignmentInput = new MenuAlignElement(
            "checkbox-alignment-content-" + callbackThis.componentIndex + "-1",
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
            "checkbox-text-color-content-" + this.componentIndex + "-1",
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
        state["type"] = "checkbox";
        state["checkboxLabel"] = this.checkboxLabel;
        state["alignment"] = this.alignment;
        state["textColor"] = this.textColor;

        return state;
    }

    // Load state
    loadState(state) {
        super.loadState(state);
        this.checkboxLabel = state["checkboxLabel"];
        this.alignment = state["alignment"];
        this.textColor = state["textColor"];
       
        $(this.id + " label").text(this.checkboxLabel);
        $(qs(this.id + " input").parentElement).css("justify-content", this.alignment);
        $(this.id + " input").css("color", this.textColor);
    }
}
