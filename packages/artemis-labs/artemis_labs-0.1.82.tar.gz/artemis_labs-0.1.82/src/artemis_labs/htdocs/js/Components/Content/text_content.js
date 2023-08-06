'use strict';

class MenuTextElement {

    constructor(elementId, parentSectionId, textLabel, textValue) {

        // Store element id
        this.elementId = elementId;
        this.parentSectionId = parentSectionId;

        // Create container
        let divContainer = createElement("div", this.elementId, "mb-3");

        // Text label
        let divContainerLabel = createElement("label", "", "form-check-label");
        $(divContainerLabel).text(textLabel);
        $(divContainerLabel).attr("for", this.elementId + "-span");

        // Create text value
        let divContainerTextValue = createElement("span", this.elementId + "-span", "");
        $(divContainerTextValue).css('display', 'block');
        divContainerTextValue.innerHTML = textValue;

        // Add label and input to checkbox form
        divContainer.appendChild(divContainerLabel);
        divContainer.appendChild(divContainerTextValue);

        // Add div container to accordion body
        let sectionContentRow = qs("#" + parentSectionId + " .accordion-body");
        sectionContentRow.appendChild(divContainer);
    }

    setText(value) {
        qs("#" + this.elementId + "-span").innerHTML = value;
    }

    getText() {
        return qs("#" + this.elementId + "-span").innerHTML;
    }
}
