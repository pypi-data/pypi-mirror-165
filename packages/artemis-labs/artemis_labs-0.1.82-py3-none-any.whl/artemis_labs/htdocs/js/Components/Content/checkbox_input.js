'use strict';

class MenuCheckboxElement {

    constructor(elementId, parentSectionId, inputLabel, inputChecked, checkboxChangedCallback) {

        // Store element id
        this.elementId = elementId;
        this.parentSectionId = parentSectionId;

        // Create container
        let divContainer = createElement("div", this.elementId, "mb-3");

        // Checkbox form
        let divCheckboxForm = createElement("div", "", "form-check");
        divContainer.appendChild(divCheckboxForm);

        // Create input label
        let divContainerLabel = createElement("label", "", "form-check-label");
        $(divContainerLabel).text(inputLabel);
        $(divContainerLabel).attr("for", this.elementId + "-input");

        // Create input
        let divContainerInput = createElement("input", this.elementId + "-input", "form-check-input");
        $(divContainerInput).attr("type", "checkbox");
        $(divContainerInput).attr("value", "");
        $(divContainerInput).prop("checked", inputChecked);

        // Add label and input to checkbox form
        divCheckboxForm.appendChild(divContainerLabel);
        divCheckboxForm.appendChild(divContainerInput);
        
        // Add div container to accordion body
        let sectionContentRow = qs("#" + parentSectionId + " .accordion-body");
        sectionContentRow.appendChild(divContainer);

        // Text changed callback
        if (checkboxChangedCallback) {
            divContainerInput.addEventListener("change", (event) => {
                checkboxChangedCallback(event.target.checked);
            });
        }
    }
}

