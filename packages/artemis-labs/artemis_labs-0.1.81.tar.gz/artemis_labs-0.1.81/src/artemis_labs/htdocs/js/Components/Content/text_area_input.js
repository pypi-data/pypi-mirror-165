'use strict';

class MenuTextAreaElement {

    constructor(elementId, parentSectionId, textareaLabel, textareaValue, textChangedCallback, readOnly=false) {

        // Store element id
        this.elementId = elementId;
        this.parentSectionId = parentSectionId;

        // Create container
        let divContainer = createElement("div", this.elementId, "mb-3");

        // Create textarea label
        let divContainerLabel = createElement("label", "", "form-label");
        $(divContainerLabel).text(textareaLabel);
        $(divContainerLabel).attr("for", this.elementId + "-textarea");

        // Create textarea
        let divContainerTextarea = createElement("textarea", this.elementId + "-textarea", "form-control");
        $(divContainerTextarea).attr("type", "text");
        $(divContainerTextarea).attr("rows", 3);
        $(divContainerTextarea).text(textareaValue);

        if(readOnly) {
            $(divContainerTextarea).prop("readonly", true);
        }

        // Add label and textarea to container
        divContainer.appendChild(divContainerLabel);
        divContainer.appendChild(divContainerTextarea);
       
        // Add div container to accordion body
        let sectionContentRow = qs("#" + parentSectionId + " .accordion-body");
        sectionContentRow.appendChild(divContainer);

        // Text changed callback
        if (textChangedCallback) {
            divContainerTextarea.addEventListener("input", (event) => {
                textChangedCallback(event.target.value);
            });
        }
    }
}
