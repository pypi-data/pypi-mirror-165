'use strict';
import { qs, qsa, createElement } from "../Helpers/helper.js";

// Menu Node Context
class PopupMenu {
    constructor(deleteButtonCallback) {

        // Create popup menu
        let popupMenu = createElement("div", "popup-menu", "hidden");
        qs("#artemis-builder").appendChild(popupMenu);

        // Create delete button
        let deleteButton = createElement("p", "delete-btn", "popup-menu-item");
        deleteButton.innerHTML = "Delete";
        popupMenu.appendChild(deleteButton);

        // Create copy button
        let copyButton = createElement("p", "copy-btn", "popup-menu-item");
        copyButton.innerHTML = "Copy";
        popupMenu.appendChild(copyButton);

        // Create copy button
        let pasteButton = createElement("p", "paste-btn", "popup-menu-item");
        pasteButton.innerHTML = "Paste";
        popupMenu.appendChild(pasteButton);

        // Create send to back button
        let sendToBack = createElement("p", "send-to-back-btn", "popup-menu-item");
        sendToBack.innerHTML = "Send To Back";
        popupMenu.appendChild(sendToBack);
          
        // Create send to back button
        let bringToFront = createElement("p", "bring-to-front-btn", "popup-menu-item");
        bringToFront.innerHTML = "Bring To Front";
        popupMenu.appendChild(bringToFront);

        // Create send back button
        let sendBack = createElement("p", "send-back-btn", "popup-menu-item");
        sendBack.innerHTML = "Send Back";
        popupMenu.appendChild(sendBack);

        // Create bring forward button
        let bringForward = createElement("p", "bring-forward-btn", "popup-menu-item");
        bringForward.innerHTML = "Bring Forward";
        popupMenu.appendChild(bringForward);

        // Store callback
        this.bindDeleteButtonCallback(deleteButtonCallback);

        // Listener for delete button
        let callbackThis = this;
        deleteButton.addEventListener("click", function() {
            callbackThis.deleteButtonCallback();
        });

        // Listener for copy button
        copyButton.addEventListener("click", function() {
            callbackThis.copyButtonCallback();
        });

        // Listener for paste button
        pasteButton.addEventListener("click", function() {
            callbackThis.pasteButtonCallback();
        });

        // Listener for send back
        sendBack.addEventListener("click", function() {
            callbackThis.sendBackCallback();            
        });

        // Listener for send to back
        sendToBack.addEventListener("click", function() {
            callbackThis.sendToBackCallback();
        });

        // Listener for bring forward
        bringForward.addEventListener("click", function() {
            callbackThis.bringForwardCallback();
        });

        // Listener for bring to front
        bringToFront.addEventListener("click", function() {
            callbackThis.bringToFrontCallback();
        });

    }

    bindBringToFrontCallback(callback) {
        this.bringToFrontCallback = callback;
    }

    bindSendToBackCallback(sendToBackCallback) {
        this.sendToBackCallback = sendToBackCallback;
    }

    bindDeleteButtonCallback(deleteButtonCallback) {
        this.deleteButtonCallback = deleteButtonCallback;
    }

    bindCopyButtonCallback(copyButtonCallback) {
        this.copyButtonCallback = copyButtonCallback;
    }

    bindPasteButtonCallback(pasteButtonCallback) {
        this.pasteButtonCallback = pasteButtonCallback;
    }

    bindSendBackCallback(sendBackCallback) {
        this.sendBackCallback = sendBackCallback;
    }

    bindBringForwardCallback(bringForwardCallback) {
        this.bringForwardCallback = bringForwardCallback;
    }

    hide() {
        $("#popup-menu").addClass("hidden");
    }

    show(numGroupedElements) {        
        if(numGroupedElements > 0) {
            $("#send-back-btn").addClass("popup-menu-item-disabled");
            $("#bring-forward-btn").addClass("popup-menu-item-disabled");
        } else {
            $("#send-back-btn").removeClass("popup-menu-item-disabled");
            $("#bring-forward-btn").removeClass("popup-menu-item-disabled");
        }
        $("#popup-menu").removeClass("hidden");
    }

    isVisible() {
        return !$("#popup-menu").hasClass("hidden");
    }

    position(cursorPos) {
        $("#popup-menu").css("left", cursorPos.x);
        $("#popup-menu").css("top", cursorPos.y);
    }

    getPosition() {
        return { "x" : $("#popup-menu").css("left"), "y" : $("#popup-menu").css("top") };
    }

    getExtents() {
        return qs("#popup-menu").getBoundingClientRect();
    }
}

// Export
export {PopupMenu};