'use strict';

class MenuTextInputElement {

    constructor(elementId, parentSectionId, inputLabel, inputValue, textChangedCallback, readOnly=false) {

        // Store element id
        this.elementId = elementId;
        this.parentSectionId = parentSectionId;

        // Create container
        let divContainer = createElement("div", this.elementId, "mb-3");

        // Create input label
        let divContainerLabel = createElement("label", "", "form-label");
        $(divContainerLabel).text(inputLabel);
        $(divContainerLabel).attr("for", this.elementId + "-input");

        // Create input
        let divContainerInput = createElement("input", this.elementId + "-input", "form-control");
        $(divContainerInput).attr("type", "text");
        $(divContainerInput).attr("value", inputValue);
        if(readOnly) {
            $(divContainerInput).prop("readonly", true);
        }

        // Add label and input to container
        divContainer.appendChild(divContainerLabel);
        divContainer.appendChild(divContainerInput);
       
        // Add div container to accordion body
        let sectionContentRow = qs("#" + parentSectionId + " .accordion-body");
        sectionContentRow.appendChild(divContainer);

        // Text changed callback
        if (textChangedCallback) {
            divContainerInput.addEventListener("input", (event) => {
                textChangedCallback(event.target.value);
            });
        }
    }
}

