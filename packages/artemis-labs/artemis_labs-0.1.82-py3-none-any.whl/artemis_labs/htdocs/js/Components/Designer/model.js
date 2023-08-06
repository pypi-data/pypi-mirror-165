'use strict';




// Menu Node Context
class Model extends Component {

    // Constructor
    constructor(componentIndex) {

        // Call parent constructor
        super(componentIndex);

        // Create DOM element
        let containerDiv = createElement("div", this.id.substring(1), "component-model");
        $(containerDiv).attr("data-type", "component");

        qs("#artemis-builder").appendChild(containerDiv);        
        
        // Setup size
        $(this.id).css("width", '100%');
        $(this.id).css("height", '100%');

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
    }

    // Get state
    getState() {
        let state = super.getState();
        return state;
    }

    // Load state
    loadState(state) {
        let componentBox = qs("#" + this.id.substring(1));
        if (componentBox.firstChild != undefined) {
            componentBox.firstChild.remove();
        }
        let modelViewer = createElement("model-viewer", this.id.substring(1) + "-model-viewer", "component-element-model-viewer");
        $(modelViewer).attr("src", state.data);
        $(modelViewer).attr("camera-controls", "");
        $(modelViewer).attr("touch-action", "pan-y");
        $(modelViewer).attr("environment-image", "legacy");
        $(modelViewer).attr('oncontextmenu', 'return false;');
        $(modelViewer).css('height', '100%');
        $(modelViewer).css('width', '100%');
        $(modelViewer).css('min-height', '256px');
        $(modelViewer).css('min-width', '256px');

        componentBox.appendChild(modelViewer);
    }
}
