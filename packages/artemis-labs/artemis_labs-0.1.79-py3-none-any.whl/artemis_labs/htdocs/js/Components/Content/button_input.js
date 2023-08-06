'use strict';

class MenuButtonElement {

    constructor(elementId, parentSectionId, buttonLabel, buttonPressedCallback) {

        // Store element id
        this.elementId = elementId;
        this.parentSectionId = parentSectionId;

        // Create container
        let divContainer = createElement("div", this.elementId, "mb-3");

        // Button form
        let buttonAdd = createElement("button", "add-option-btn", "btn btn-sm btn-outline-light text-danger");
        divContainer.appendChild(buttonAdd);
        let buttonAddIcon = createElement("i", "", "fa-light fa-trash");
        $(buttonAddIcon).css('padding-right', '6px');
        buttonAdd.appendChild(buttonAddIcon);
        let buttonAddText = createElement("span", "", "");
        buttonAdd.appendChild(buttonAddText);
        buttonAddText.innerHTML = buttonLabel;

        // Add to DOm
        let sectionContentRow = qs("#" + parentSectionId + " .accordion-body");
        sectionContentRow.appendChild(divContainer);

        // Button pressed callback
        if (buttonPressedCallback) {
            $(buttonAdd).click(() => {
                buttonPressedCallback();
            });
        }
    }
}

// Export
export {MenuButtonElement};