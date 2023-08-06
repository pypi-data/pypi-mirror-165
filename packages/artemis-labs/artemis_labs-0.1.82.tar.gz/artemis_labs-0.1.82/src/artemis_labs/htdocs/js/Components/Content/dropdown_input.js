'use strict';

class MenuDropDownInput {

    constructor(elementId, parentSectionId, inputLabel, inputValue, inputOptions, selectionChangedCallback) {

        // Store element id
        this.elementId = elementId;
        this.parentSectionId = parentSectionId;

        // Create container
        let divContainer = createElement("div", this.elementId, "mb-3");

        // Create label for container
        let label = createElement("label", "", "form-label");
        label.setAttribute("for", "dropdown-input");
        label.innerHTML = inputLabel;
        divContainer.appendChild(label); 

        // Create input
        let inputSelect = createElement("select", "dropdown-input", "form-select");
        let inputOptionNames = Object.keys(inputOptions);
        for(let i = 0; i < inputOptionNames.length; i++) {
            let inputOption = inputOptionNames[i];
            let inputOptionValue = inputOptions[inputOption];
            let option = createElement("option", "", "");
            option.setAttribute("value", inputOptionValue);
            option.innerHTML = inputOption;
            inputSelect.appendChild(option);
        }
        $(inputSelect).val(inputValue);
        divContainer.appendChild(inputSelect);

        // Add div container to accordion body
        let sectionContentRow = qs("#" + parentSectionId + " .accordion-body");
        sectionContentRow.appendChild(divContainer);

        // Text changed callback
        if (selectionChangedCallback) {
            $(inputSelect).change((event) => {
                selectionChangedCallback(event.target.value);
            });
        }
    }
}

