'use strict';

class MenuColorInput {

    async useEyeDropper(eyeDropper) {
        try {
          const selectedColor = await eyeDropper.open();
          const colorHashCode = selectedColor['sRGBHex'];
          $("#" + this.elementId + "-input").val(colorHashCode);
          this.colorChangedCallback(colorHashCode);
        } catch (err) {
          console.log('eye dropper cancelled')
        }
      }

    constructor(elementId, parentSectionId, inputLabel, inputValue, colorChangedCallback) {

        // Store element id
        this.elementId = elementId;
        this.parentSectionId = parentSectionId;

        // Bind callback
        this.colorChangedCallback = colorChangedCallback;

        // Create container
        let divContainer = createElement("div", this.elementId, "mb-3");

        // Create input label
        let divContainerLabel = createElement("label", "", "form-label");
        $(divContainerLabel).text(inputLabel);
        $(divContainerLabel).attr("for", this.elementId + "-input");

        // Create button group
        let buttonGroup = createElement("div", "", "btn-group");
        $(buttonGroup).css('width', '100%');
        $(buttonGroup).css('display', 'flex');
        $(buttonGroup).css('justify-content', 'start');
        $(buttonGroup).css('align-items', 'center');

        // Create input
        let divContainerInput = createElement("input", this.elementId + "-input", "form-control form-control-color");
        divContainerInput.setAttribute("type", "color");
        divContainerInput.setAttribute("pattern", "#[a-f0-9]{6}");
        divContainerInput.setAttribute("value", inputValue);
        $(divContainerInput).css("margin-right", "10px");

        // Create match button
        let matchButton = createElement("button", this.elementId + "-match", "btn btn-secondary");
        $(matchButton).css('width', '28px');
        $(matchButton).css('max-width', '28px');
        $(matchButton).css('max-height', '28px');
        $(matchButton).css('height', '28px');
        $(matchButton).css('border-radius', '4px');
        $(matchButton).css('display', 'flex');
        $(matchButton).css('align-items', 'center');
        $(matchButton).css('justify-content', 'center');
        $(matchButton).css('background-color', '#000000');
        $(matchButton).attr("type", "clone-button");

        let matchButtonIcon = createElement("i", "", "fa fa-eyedropper");
        $(matchButtonIcon).css('font-size', '1em');
        $(matchButton).append(matchButtonIcon);
        
        // Add label and input to container
        divContainer.appendChild(divContainerLabel);
        buttonGroup.appendChild(divContainerInput);
        buttonGroup.appendChild(matchButton);
        divContainer.appendChild(buttonGroup);
        
        // Add div container to accordion body
        let sectionContentRow = qs("#" + parentSectionId + " .accordion-body");
        sectionContentRow.appendChild(divContainer);

        // Text changed callback
        if (colorChangedCallback) {
            divContainerInput.addEventListener("input", (event) => {
                colorChangedCallback(event.target.value);
            });
        }

        // Clonining button click
        let clickCounter = 0;
        matchButton.addEventListener("click", (event) => {
            this.useEyeDropper(new EyeDropper());
        });
    }
}
