'use strict';

class MultipleInputElement {

    constructor(parentSectionId, onChangeCallback, options) {

        // Store element id
        this.parentSectionId = parentSectionId;

        // Initalize option input count
        this.optionInputCount = 0;

        // Set on change callback
        this.onChangeCallback = onChangeCallback;

        // Add new option button
        this.addNewOptionButton();

        // Add option items
        for (let i = 0; i < options.length; i++) {
            this.addOptionItem(options[i]);
        }
    }

    addOptionItem(inputValue) {

        // Callback
        let callbackThis = this;

        // Increment option input count
        this.optionInputCount++;

        // Create container
        let divContainer = createElement("div", this.elementId, "mb-3 option");

        // Create label for container
        let label = createElement("label", "", "form-label");
        label.setAttribute("for", "input-model");
        label.innerHTML = "Option " + this.optionInputCount;
        divContainer.appendChild(label);

         // Create input container and input group for container
        let inputDiv = createElement("div", "", "input");
        let inputGroupDiv = createElement("div", "", "input-group");
        inputDiv.appendChild(inputGroupDiv);
        divContainer.appendChild(inputGroupDiv);

        // Create inputs for input group
        let optionInput = createElement("input", "", "form-control");
        optionInput.setAttribute("type", "text");
        optionInput.setAttribute("name", "text");
        optionInput.setAttribute("value", inputValue);
        inputGroupDiv.appendChild(optionInput);

        // Monitor change
        $(optionInput).on("input", (event) => {
            callbackThis.onChangeCallback(callbackThis.getOptions());
        });
        
        // Add delete button
        let divDelete = createElement("div", "", "col-12");
        let buttonDelete = createElement("button", "", "btn btn-sm btn-outline-light text-danger");
        $(buttonDelete).css('max-width', '76.11px');
        $(buttonDelete).css('max-height', '27.38px');
        let buttonDeleteIcon = createElement("i", "", "fa-light fa-trash");
        $(buttonDeleteIcon).css("padding-right", "6px");
        let buttonDeleteText = createElement("span", "", "");
        buttonDeleteText.innerHTML = "Remove";
        buttonDelete.appendChild(buttonDeleteIcon);
        buttonDelete.appendChild(buttonDeleteText);
        divDelete.appendChild(buttonDelete);
        inputGroupDiv.appendChild(divDelete);

        // Remove button callback
        buttonDelete.addEventListener("click", (event) => {
           
            // Remove option group
            let optionGroup = buttonDelete.parentElement.parentElement.parentElement;
            optionGroup.remove();

            // Decrement option counter
            callbackThis.optionInputCount--;

            // Update option id's and text
            let options = qsa("#" + callbackThis.parentSectionId + " .option");
            for (let i = 0; i < options.length; i++) {
                options[i].setAttribute("id", "option-" + (i + 1));
                options[i].querySelector("label").innerHTML = "Option " + (i + 1);
            }

            // Call change callback
            callbackThis.onChangeCallback(callbackThis.getOptions());
        });

        // Add option before button
        let addOptionBtn = qs("#" + this.parentSectionId + " #add-option-btn");
        addOptionBtn.parentNode.insertBefore(divContainer, addOptionBtn);
    }

    addNewOptionButton() {

        // Callback
        let callbackThis = this;
        
        // Create row for new option
        let divContainer = createElement("div", this.elementId, "mb-3");
        divContainer.setAttribute("data-key", "addChild");

        // Create button for new option
        let divInput = createElement("div", "", "col-sm-12 input");
        let divDivInput = createElement("div", "", "");
        let buttonAdd = createElement("button", "add-option-btn", "btn btn-sm btn-primary");
        $(buttonAdd).css('max-width', '94.02px');
        $(buttonAdd).css('max-height', '27.38px');
        let buttonAddIcon = createElement("i", "", "fa-light fa-plus");
        $(buttonAddIcon).css("padding-right", "6px");
        let buttonAddText = createElement("span", "", "");
        buttonAddText.innerHTML = "Add option";

        buttonAdd.appendChild(buttonAddIcon);
        buttonAdd.appendChild(buttonAddText);
        divDivInput.appendChild(buttonAdd);
        divInput.appendChild(divDivInput);
        divContainer.appendChild(divInput);

        // Add div container to accordion body
        let sectionContentRow = qs("#" + this.parentSectionId + " .accordion-body");
        sectionContentRow.appendChild(divContainer);

        // Set callback to create new option
        buttonAdd.addEventListener("click", (event) => {
            callbackThis.addOptionItem("");
            callbackThis.onChangeCallback(callbackThis.getOptions());
        });
    }

    getOptions() {
        let optionItems = [];
        let options = qsa("#" + this.parentSectionId + " .option input");

        console.log("#" + this.parentSectionId + " .option input");
        for (let i = 0; i < options.length; i++) {
            optionItems.push(options[i].value);
        }
        return optionItems;
    }
    
}
