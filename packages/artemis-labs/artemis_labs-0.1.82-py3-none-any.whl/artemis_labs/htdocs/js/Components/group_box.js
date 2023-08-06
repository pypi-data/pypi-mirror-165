'use strict';
import { qs, qsa, createElement } from "../Helpers/helper.js";

class GroupBox {
    constructor() {

        // Store ID and padding
        this.id = "#group-box";
        this.padding = 10;

        // Group positions
        this.groupStart = { "left" : 0, "top" : 0 };
        this.groupEnd = { "left" : 0, "top" : 0 };

        // Create DOM elememt
        let groupBox = createElement("div", "group-box", "hidden");
        qs("#artemis-builder").appendChild(groupBox);
    }

    isSelected() {
        return $(this.id).hasClass("selected");
    }
    getExtents() {
        return qs(this.id).getBoundingClientRect();
    }

    hide() {
        $(this.id).addClass("hidden");
        $(this.id).css("width", "0");
        $(this.id).css("height", "0");
        $(this.id).css("left", "0");
        $(this.id).css("top", "0");
    }
    show() {
        $(this.id).removeClass("hidden");
    }

    setGroupStart(in_groupStart) {
        in_groupStart["left"] = parseInt(in_groupStart.left);
        in_groupStart["top"] = parseInt(in_groupStart.top);
        this.groupStart = in_groupStart;
        this.updateGroupBox();
    }
    setGroupEnd(in_groupEnd) {
        in_groupEnd["left"] = parseInt(in_groupEnd.left);
        in_groupEnd["top"] = parseInt(in_groupEnd.top);
        this.groupEnd = in_groupEnd;
        this.updateGroupBox();
    }

    updateGroupBox() {
        let lowerLeft = Math.min(this.groupStart.left, this.groupEnd.left);
        let lowerTop = Math.min(this.groupStart.top, this.groupEnd.top);

        let width = Math.abs(this.groupStart.left - this.groupEnd.left);
        let height = Math.abs(this.groupStart.top - this.groupEnd.top);

        $(this.id).css("left", lowerLeft + "px");
        $(this.id).css("top", lowerTop + "px");
        $(this.id).css("width", width + "px");
        $(this.id).css("height", height + "px");
    }
   
    getTopLeftCorner() {
        return { "left" : parseInt($(this.id).css("left")), "top" : parseInt($(this.id).css("top")) };
    }

    getBottomRightCorner() {
        let groupTopLeftCorner = this.getTopLeftCorner();
        let groupSize = this.getSize();
        return { "left" : parseInt(groupTopLeftCorner.left) + parseInt(groupSize.width), "top" : parseInt(groupTopLeftCorner.top) + parseInt(groupSize.height) };
    }
  
    getSize() {
        return { "width" : $(this.id).css("width"), "height" : $(this.id).css("height") };
    }
    getId() {
        return this.id;
    }
}

// Export
export {GroupBox};