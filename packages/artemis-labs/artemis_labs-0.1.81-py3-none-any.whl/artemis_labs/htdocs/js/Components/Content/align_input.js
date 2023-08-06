'use strict';

class MenuAlignElement {

    constructor(elementId, parentSectionId, inputLabel, selectedElement, selectionChangedCallback) {

        // Store element id
        this.elementId = elementId;
        this.parentSectionId = parentSectionId;
        this.selectedElement = selectedElement;

        // Create container
        let divContainer = createElement("div", this.elementId, "mb-3");

        // Create button group label
        let divContainerLabel = createElement("label", "", "form-label");
        $(divContainerLabel).text(inputLabel);
        $(divContainerLabel).css("margin-right", "12px");
        $(divContainerLabel).attr("for", "alignment-group");
        divContainer.appendChild(divContainerLabel);

        // Create button group
        let divButtonGroup = createElement("div", "alignment-group", "btn-group");
        $(divButtonGroup).attr("role", "toolbar");
        $(divButtonGroup).attr("aria-label", "Alignment");
        $(divButtonGroup).css("max-height", "35.5px");
        $(divButtonGroup).css("max-width", "180px");
        divContainer.appendChild(divButtonGroup);

        // First button
        let button1Input = createElement("input", "", "btn-check");
        button1Input.setAttribute("type", "radio");
        button1Input.setAttribute("value", "default");
        button1Input.setAttribute("id", "rb-25text-align0");
        button1Input.setAttribute("autocomplete", "off");
        button1Input.setAttribute("name", "text-align");
        divButtonGroup.appendChild(button1Input);

        let button1Label = createElement("label", "", "btn btn-outline-primary");
        button1Label.setAttribute("for", "rb-25text-align0");
        button1Label.setAttribute("title", "None");
        divButtonGroup.appendChild(button1Label);

        let button1LabelIcon = createElement("i", "", "la la-times");
        button1Label.appendChild(button1LabelIcon);

        // Second button
        let button2Input = createElement("input", "", "btn-check");
        button2Input.setAttribute("type", "radio");
        button2Input.setAttribute("value", "start");
        button2Input.setAttribute("name", "text-align");
        button2Input.setAttribute("id", "rb-25text-align1");
        button2Input.setAttribute("autocomplete", "off");
        divButtonGroup.appendChild(button2Input);

        let button2Label = createElement("label", "", "btn btn-outline-primary");
        button2Label.setAttribute("for", "rb-25text-align1");
        button2Label.setAttribute("title", "Left");
        divButtonGroup.appendChild(button2Label);

        let button2LabelIcon = createElement("i", "", "la la-align-left");
        button2Label.appendChild(button2LabelIcon);

        // Third button
        let button3Input = createElement("input", "", "btn-check");
        button3Input.setAttribute("type", "radio");
        button3Input.setAttribute("value", "center");
        button3Input.setAttribute("name", "text-align");
        button3Input.setAttribute("id", "rb-25text-align2");
        button3Input.setAttribute("autocomplete", "off");
        button3Input.setAttribute("checked", "checked");
        divButtonGroup.appendChild(button3Input);

        let button3Label = createElement("label", "", "btn btn-outline-primary");
        button3Label.setAttribute("for", "rb-25text-align2");
        button3Label.setAttribute("title", "Center");
        divButtonGroup.appendChild(button3Label);

        let button3LabelIcon = createElement("i", "", "la la-align-center");
        button3Label.appendChild(button3LabelIcon);

        // Fourth button
        let button4Input = createElement("input", "", "btn-check");
        button4Input.setAttribute("type", "radio");
        button4Input.setAttribute("value", "end");
        button4Input.setAttribute("name", "text-align");
        button4Input.setAttribute("id", "rb-25text-align3");
        button4Input.setAttribute("autocomplete", "off");
        divButtonGroup.appendChild(button4Input);

        let button4Label = createElement("label", "", "btn btn-outline-primary");
        button4Label.setAttribute("for", "rb-25text-align3");
        button4Label.setAttribute("title", "Right");
        divButtonGroup.appendChild(button4Label);

        let button4LabelIcon = createElement("i", "", "la la-align-right");
        button4Label.appendChild(button4LabelIcon);

        // Fifth button
        let button5Input = createElement("input", "", "btn-check");
        button5Input.setAttribute("type", "radio");
        button5Input.setAttribute("value", "space-evenly");
        button5Input.setAttribute("name", "text-align");
        button5Input.setAttribute("id", "rb-25text-align4");
        button5Input.setAttribute("autocomplete", "off");
        divButtonGroup.appendChild(button5Input);

        let button5Label = createElement("label", "", "btn btn-outline-primary");
        button5Label.setAttribute("for", "rb-25text-align4");
        button5Label.setAttribute("title", "Justify");
        divButtonGroup.appendChild(button5Label);

        let button5LabelIcon = createElement("i", "", "la la-align-justify");
        button5Label.appendChild(button5LabelIcon);
      
        // Add div container to accordion body
        let sectionContentRow = qs("#" + parentSectionId + " .accordion-body");
        sectionContentRow.appendChild(divContainer);

        // Choose selected element
        if (selectedElement == "default") {
            button1Input.setAttribute("checked", "checked");
        }
        else if (selectedElement == "start") {
            button2Input.setAttribute("checked", "checked");
        }
        else if (selectedElement == "center") {
            button3Input.setAttribute("checked", "checked");
        }
        else if (selectedElement == "end") {
            button4Input.setAttribute("checked", "checked");
        }
        else if (selectedElement == "space-evenly") {
            button5Input.setAttribute("checked", "checked");
        }
      
        // Event handlers for changing selection
        button1Input.addEventListener("click", (event) => {
            selectionChangedCallback(event.target.value);
        });
        button2Input.addEventListener("click", (event) => {
            selectionChangedCallback(event.target.value);
        });
        button3Input.addEventListener("click", (event) => {
            selectionChangedCallback(event.target.value);
        });
        button4Input.addEventListener("click", (event) => {
            selectionChangedCallback(event.target.value);
        });
        button5Input.addEventListener("click", (event) => {
            selectionChangedCallback(event.target.value);
        });
    }
}
