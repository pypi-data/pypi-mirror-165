'use strict';


// Menu Node Context
class Video extends Component {
    constructor(componentIndex, disabled=true) {

        // Call parent constructor
        super(componentIndex);

        // Setup features
        this.videoURL = "";

        // Create DOM element container 
        let containerDiv = createElement("div", this.id.substring(1), "component-video");
        $(containerDiv).attr("data-type", "component");

        // Create HTML for video
        let video = createElement("video", "", "component-element-video");
        video.controls = true;
        containerDiv.appendChild(video);
        if(disabled) {
            $(video).attr("disabled", "true");
            $(video).css("pointer-events", "none");
        }

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

    updateValue(state) {
        this.videoURL = state;
        console.log(this.videoURL);
        if (this.videoURL != "") {
            $(this.id + " video").attr("src", this.videoURL);
        }
    }

    getValue() {
        return this.videoURL;
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
 
        let videoURLNameElement = new MenuTextElement(
            "image-url-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Video URL:",
            this.videoURL
        );

     
        let videoUrlInput = new URLInput(
            "url-input-" + this.componentIndex + "-1",
            "section-" + this.componentIndex + "-2",
            "Upload a Video",
            this.videoURL,
            (videoURL) => {
                callbackThis.videoURL = videoURL;
                videoURLNameElement.setText(videoURL);                
                $(callbackThis.id + " video").attr("src", videoURL);
            }
        );
    }

    // Get state
    getState() {
        let state = super.getState();
        state["type"] = "video";
        state['videoURL'] = this.videoURL;
        return state;
    }

    // Load state
    loadState(state) {        
        super.loadState(state);
        this.videoURL = state['videoURL'];

        if(this.videoURL == undefined) {
            this.videoURL = "";
        }

        if (this.videoURL != "") {
            $(this.id + " video").attr("src", this.videoURL);
        }
    }
}
