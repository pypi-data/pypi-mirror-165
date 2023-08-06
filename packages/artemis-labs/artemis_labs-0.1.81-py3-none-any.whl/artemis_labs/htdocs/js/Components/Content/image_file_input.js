'use strict';

class ImageFileInput {

    constructor(elementId, parentSectionId, inputLabel, inputFile, imageUploadedCallback) {

        // Store element id
        this.elementId = elementId;
        this.parentSectionId = parentSectionId;

        // Values
        this.chosenImageName = "";
        this.chosenImageData = "";

        // Create container
        let divContainer = createElement("div", this.elementId, "mb-3");

        // Create input label
        let divContainerLabel = createElement("label", "", "form-label");
        $(divContainerLabel).text(inputLabel);
        $(divContainerLabel).attr("for", this.elementId + "-input");

        // Create input
        let divContainerInput = createElement("input", this.elementId + "-input", "form-control");
        divContainerInput.setAttribute("type", "file");
        divContainerInput.setAttribute("accept", "image/png, image/gif, image/jpeg, image/jpg");
        divContainerInput.setAttribute("value", inputFile);

        // Add label and input to container
        divContainer.appendChild(divContainerLabel);
        divContainer.appendChild(divContainerInput);

        // Add upload image button
        let buttonAdd = createElement("button", "add-option-btn", "btn btn-sm btn-primary");
        $(buttonAdd).css("margin-top", "12px");
        let buttonAddIcon = createElement("i", "", "fa-light fa-plus");
        buttonAdd.appendChild(buttonAddIcon);
        $(buttonAddIcon).css("padding-right", "6px");
        let buttonAddText = createElement("span", "", "");
        buttonAdd.appendChild(buttonAddText);
        buttonAddText.innerHTML = "Upload Image";
        $(buttonAdd).prop('disabled', 'true');

        // Add button to container
        divContainer.appendChild(buttonAdd);
        
        // Add div container to accordion body
        let sectionContentRow = qs("#" + parentSectionId + " .accordion-body");
        sectionContentRow.appendChild(divContainer);

        // Call callback and reset input when image is uploaded
        $(buttonAdd).click(function () {
            if(callbackThis.chosenImageData == "") return;
            imageUploadedCallback(callbackThis.chosenImageName, callbackThis.chosenImageData);
            $(buttonAdd).prop('disabled', 'true');
            callbackThis.chosenImageName = "";
            callbackThis.chosenImageData = "";
            $(divContainerInput).val(null);
        });

        // File uploaded callback
        let callbackThis = this;
        divContainerInput.addEventListener("change", function() {
            const reader = new FileReader();
            reader.addEventListener("load", () => {
                callbackThis.chosenImageName = this.files[0];
                callbackThis.chosenImageData = reader.result;
                $('#' + callbackThis.elementId + ' button').removeAttr('disabled');
            });
            reader.readAsDataURL(this.files[0]);
        });
    }
}

// Export
export {ImageFileInput};