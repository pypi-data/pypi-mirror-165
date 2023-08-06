'use strict';

class MenuSwitchInputElement {

    constructor(elementId, parentSectionId, inputLabel, inputState, switchChangedCallback, readOnly=false) {

        // Store element id
        this.elementId = elementId;
        this.parentSectionId = parentSectionId;
        this.switchState = inputState;

        // Create container
        let divContainer = createElement("div", this.elementId, "mb-3"); 
        $(divContainer).css("height", "28px");       
        $(divContainer).css("display", "flex");       
        $(divContainer).css("flex-direction", "row");       
        $(divContainer).css("align-items", "center");       

        // Create input div
        let inputDiv = createElement("div", "", "form-check form-switch");
        divContainer.appendChild(inputDiv);
        $(inputDiv).css("box-sizing", "border-box");
        $(inputDiv).css("padding", "0px");

        // Create input
        let input = createElement("input", "", "form-check-input");
        inputDiv.appendChild(input);
        $(input).css("margin", "0px");
        $(input).css("width", "44px");
        $(input).css("height", "22px");
        $(input).attr("type", "checkbox");
        $(input).attr("role", "switch");
        if(this.switchState) {
            console.log('checked');
            $(input).prop("checked", "true");
        }
       
        // Create input label
        let divContainerLabel = createElement("label", "", "form-check-label");
        inputDiv.appendChild(divContainerLabel);
        $(divContainerLabel).text(inputLabel);
        $(divContainerLabel).attr("for", this.elementId + "-input");
        $(divContainerLabel).css("margin-left", "8px");

             
        // Add div container to accordion body
        let sectionContentRow = qs("#" + parentSectionId + " .accordion-body");
        console.log(sectionContentRow);
        sectionContentRow.appendChild(divContainer);

        // Text changed callback
        let callbackThis = this;
        if (switchChangedCallback) {
            input.addEventListener("input", (event) => {
                callbackThis.switchState = !callbackThis.switchState;
                switchChangedCallback(callbackThis.switchState);
            });
        }
    }
}
