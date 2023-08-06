'use strict';
import { qs, qsa, createElement } from "../Helpers/helper.js";

// Menu Node Context
class DropBox {
    constructor() {
        let dropBox = createElement("div", "drop-box", "hidden");
        qs("#artemis-builder").appendChild(dropBox);
    }
    hide() {
        $("#drop-box").addClass("hidden");
    }
    show() {
        $("#drop-box").removeClass("hidden");
    }
    position(cursorPos, dragAreaExtents) {

        // Compute cursor pos relative to drag area
        let cursorPosRelDragArea = {};
        cursorPosRelDragArea['x'] = cursorPos['x'] - dragAreaExtents.left;
        cursorPosRelDragArea['y'] = cursorPos['y'] - dragAreaExtents.top;

        // Compute cursor pos offset from drag area
        cursorPosRelDragArea.x -= cursorPosRelDragArea.x % 8;
        cursorPosRelDragArea.y -= cursorPosRelDragArea.y % 8;

        // Compute final pos
        let dropBoxPosX = cursorPosRelDragArea.x + dragAreaExtents.left;
        let dropBoxPosY = cursorPosRelDragArea.y + dragAreaExtents.top;

        // Cap
        if((dropBoxPosX + $("#drop-box").width()) > qs("#drag-area").getBoundingClientRect().right - 5) {
            dropBoxPosX = qs("#drag-area").getBoundingClientRect().right - $("#drop-box").width();
        }
        if(dropBoxPosY < qs("#drag-area").getBoundingClientRect().top) {
            dropBoxPosY = qs("#drag-area").getBoundingClientRect().top;
        }
        if((dropBoxPosY + $("#drop-box").height()) > qs("#drag-area").getBoundingClientRect().bottom) {
            dropBoxPosY = qs("#drag-area").getBoundingClientRect().bottom - $("#drop-box").height;
        }

        // Place drop box
        $("#drop-box").css("left", dropBoxPosX);
        $("#drop-box").css("top", dropBoxPosY);
    }
    getPosition() {
        return { "x" : $("#drop-box").css("left"), "y" : $("#drop-box").css("top") };
    }
    getPlacementPosition() {
        
        // Get drop box position relative to drag area top left corner
        let dropBoxRelPositionX = parseInt(this.getPosition().x) - $("#drag-area").offset().left;
        let dropBoxRelPositionY = parseInt(this.getPosition().y) - $("#drag-area").offset().top;

        // Position
        return { "x" : dropBoxRelPositionX, "y" : dropBoxRelPositionY };
    }
}

// Export
export {DropBox};