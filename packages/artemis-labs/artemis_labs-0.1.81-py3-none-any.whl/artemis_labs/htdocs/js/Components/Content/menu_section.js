'use strict';


class MenuSection {

    constructor(sectionName, sectionId, tabId = "#component-content-tab-body") {

        // Store section name
        this.sectionName = sectionName;
        this.sectionId = sectionId;

        // Set number of option inputs to 0
        this.optionInputCount = 0;

        // Create accordion
        let accordionItem = createElement("div", "", "accordion-item");

        // Create accordion header
        let accordionItemHeader = createElement("h2", sectionId + "-header", "accordion-header");
        let accordionButton = createElement("button", "", "accordion-button collapsed");
        $(accordionButton).attr("type", "button");
        $(accordionButton).attr("data-bs-toggle", "collapse");
        $(accordionButton).attr("data-bs-target", "#" + sectionId);
        $(accordionButton).attr("aria-expanded", "false");
        $(accordionButton).attr("aria-controls", sectionId);
        let accordionSpan = createElement("span", "", "accordion-span");
        accordionSpan.innerHTML = sectionName;
        accordionButton.appendChild(accordionSpan);
        accordionItemHeader.appendChild(accordionButton);
        accordionItem.appendChild(accordionItemHeader);

        // Create accordion body
        let accordionItemBody = createElement("div", sectionId, "accordion-collapse collapse");
        $(accordionItemBody).attr("aria-labelledby", sectionId + "-header");
        $(accordionItemBody).attr("id", sectionId);
        accordionItem.appendChild(accordionItemBody);

        // Create accordion body div
        let accordionItemBodyDiv = createElement("div", "", "accordion-body");
        accordionItemBody.appendChild(accordionItemBodyDiv);
        accordionItem.appendChild(accordionItemBody);

        // Add accordion to tab
        qs("#right-panel " + tabId + " #accordion-component-container").appendChild(accordionItem);
    }

    remove() {
        qs("#" + this.sectionId).parentElement.remove();
    }
}

// Export
export {MenuSection};