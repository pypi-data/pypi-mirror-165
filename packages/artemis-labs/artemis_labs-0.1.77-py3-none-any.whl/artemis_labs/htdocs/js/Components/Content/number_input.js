'use strict';

class MenuNumberInputElement {

    constructor(elementId, parentSectionId, inputLabel, inputNumberValue, inputTypeValue, fontSizeChangedCallback, fontSizeUnitChangedCallback) {

        // Store element id
        this.elementId = elementId;
        this.parentSectionId = parentSectionId;

        // Create container
        let divContainer = createElement("div", this.elementId, "mb-3");

        // Create label for input group
        let label = createElement("label", "", "form-label");
        label.setAttribute("for", "number-input-group");
        label.innerHTML = inputLabel;
        divContainer.appendChild(label);

        // Create input group
        let inputGroupDiv = createElement("div", "number-input-group", "input-group");
        divContainer.appendChild(inputGroupDiv);

        // Create text input
        let input = createElement("input", "", "form-control");
        input.setAttribute("type", "number");
        input.setAttribute("name", "number");
        input.setAttribute("value", inputNumberValue);
        inputGroupDiv.appendChild(input);

        // Create input type selector
        let selectType = createElement("select", "", "form-select small-arrow number-input-select");
        selectType.setAttribute("name", "unit");
        inputGroupDiv.appendChild(selectType);

        // Add options to input type selector
        let option1 = createElement("option", "", "");
        option1.setAttribute("value", "px");
        option1.innerHTML = "px";

        let option2 = createElement("option", "", "");
        option2.setAttribute("value", "em");
        option2.innerHTML = "em";

        let option3 = createElement("option", "", "");
        option3.setAttribute("value", "rem");
        option3.innerHTML = "rem";
        
        // Append options to input type selector
        selectType.appendChild(option1);
        selectType.appendChild(option2);
        selectType.appendChild(option3);

        // Set selected value
        selectType.value = inputTypeValue;

        // Add div container to accordion body
        let sectionContentRow = qs("#" + parentSectionId + " .accordion-body");
        sectionContentRow.appendChild(divContainer);

        // Text changed callback
        if (fontSizeChangedCallback) {
            input.addEventListener("input", (event) => {
                fontSizeChangedCallback(event.target.value);
            });
        }
        if (fontSizeUnitChangedCallback) {
            selectType.addEventListener("change", (event) => {
                fontSizeUnitChangedCallback(event.target.value);
            });
        }
    }
}
