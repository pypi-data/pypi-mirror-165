'use strict';

class MenuNumberWheel {

    constructor(elementId, parentSectionId, inputLabel, inputValue, inputMin, inputMax, inputStep,  numberChangedCallback) {

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
        let input = createElement("input", this.elementId + "-input", "component-element-number-wheel form-control");
        $(input).attr("type", 'number');
        $(input).attr("name", "input");
        $(input).attr('step', inputStep);
        $(input).attr('min', inputMin);
        $(input).attr('max', inputMax);
        $(input).val(inputValue);

        // Add label and input to container
        divContainer.appendChild(divContainerLabel);
        divContainer.appendChild(input);
       
        // Add div container to accordion body
        let sectionContentRow = qs("#" + parentSectionId + " .accordion-body");
        sectionContentRow.appendChild(divContainer);

        // Text changed callback
        if (numberChangedCallback) {
            input.addEventListener("input", (event) => {
                numberChangedCallback(event.target.value);
            });
        }
    }
}
