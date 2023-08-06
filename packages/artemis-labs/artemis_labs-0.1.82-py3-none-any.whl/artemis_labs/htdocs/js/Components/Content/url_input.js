'use strict';

class URLInput {

    constructor(elementId, parentSectionId, inputLabel, inputFile, urlChangedCallback) {

        // Store element id
        this.elementId = elementId;
        this.parentSectionId = parentSectionId;

        // Create container
        let divContainer = createElement("div", this.elementId, "mb-3");

        // Create input label
        let divContainerLabel = createElement("label", "", "form-label");
        $(divContainerLabel).text(inputLabel);
        $(divContainerLabel).attr("for", this.elementId + "-input-group");

        // Create input group
        let divContainerInputGroup = createElement("div", this.elementId + "-input-group", "input-group");

        // Create input
        let divContainerInput = createElement("input", this.elementId + "-input", "form-control");
        divContainerInput.setAttribute("type", "text");
        divContainerInput.setAttribute("value", inputFile);
        $(divContainerInput).attr("aria-describedby", this.elementId + "-input-group-addon");

        // Create addon
        let divContainerInputGroupAddon = createElement("div", this.elementId + "-input-group-append", "input-group-append");
        let divContainerInputGroupAddonButton = createElement("button", this.elementId + "-input-group-addon", "btn btn-outline-secondary");
        divContainerInputGroupAddonButton.setAttribute("type", "button");
        $(divContainerInputGroupAddonButton).css("max-width", "68px");
        $(divContainerInputGroupAddonButton).css("max-height", "33.5px");
        $(divContainerInputGroupAddonButton).text("Upload");
        divContainerInputGroupAddon.appendChild(divContainerInputGroupAddonButton);

        // Add to input group
        divContainerInputGroup.appendChild(divContainerInput);
        divContainerInputGroup.appendChild(divContainerInputGroupAddon);

        // Add label and input to container
        divContainer.appendChild(divContainerLabel);
        divContainer.appendChild(divContainerInputGroup);

        // Add div container to accordion body
        let sectionContentRow = qs("#" + parentSectionId + " .accordion-body");
        sectionContentRow.appendChild(divContainer);

        // Upload listener
        $(divContainerInputGroupAddonButton).click(() => {
            urlChangedCallback(divContainerInput.value);
            divContainerInput.value = "";
        });
    }
}
