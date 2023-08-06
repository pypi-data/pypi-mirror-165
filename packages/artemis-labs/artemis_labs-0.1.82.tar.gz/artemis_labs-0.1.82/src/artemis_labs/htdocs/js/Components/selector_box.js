'use strict';
import { qs, qsa, createElement } from "../Helpers/helper.js";

class SelectorBox {
    constructor() {

        // Callback
        let callbackThis = this;;

        // Store ID and padding
        this.id = "#selector-box";
        this.padding = 10;

        // On leave callback
        this.onLeaveCallback = null;

        // Mark not dragging
        this.dragging = false;

        // Mark not resizing
        this.resizing = false;
        this.resizingRight = false;
        this.resizingLeft = false;
        this.resizingDown = false;
        this.resizingUp = false;

        // Create DOM elememt
        let selectorBox = createElement("div", "selector-box", "hidden");
        qs("#artemis-builder").appendChild(selectorBox);

        // Expander callbacks
        this.callbackExpandLeft = null;
        this.callbackContractLeft = null;
        this.callbackExpandRight = null;
        this.callbackContractRight = null;
        this.callbackExpandDown = null;
        this.callbackContractDown = null;
        this.callbackContractUp = null;
        this.callbackExpandUp = null;

        // Sizing info
        this.horizontalResizing = true;
        this.verticalResizing = true;

        // End expansion on mouse release
        $(document).mouseup(function() {
            callbackThis.resizingRight = false;
            callbackThis.resizingLeft = false;
            callbackThis.resizingDown = false;
            callbackThis.resizingUp = false;
            callbackThis.resizing = false;
        });

        // Handle expansion
        $(document).mousemove(function(e) {


            if (callbackThis.resizing) {
                if(callbackThis.resizingRight) {
                    if(e.originalEvent.clientX >= ($("#selector-box").width() + parseInt($("#selector-box").offset().left + 8))) {  
                        
                        let gap = e.originalEvent.clientX - $("#selector-box").width() + parseInt($("#selector-box").offset().left);
                        let correction = gap % 8;

                        if (correction > 4) { 
                            gap = gap + (8 - correction);
                        } else {
                            gap = gap - correction;
                        }
                        if (gap < 8) {
                            gap = 0;
                        }    

                        if(callbackThis.callbackExpandRight != null) {
                            if(callbackThis.callbackExpandRight(gap)) {
                                $("#selector-box").width($("#selector-box").width() + gap);
                            }
                        }
                    }
                    if(e.originalEvent.clientX <= ($("#selector-box").width() + parseInt($("#selector-box").offset().left - 8))) {

                        let gap = $("#selector-box").width() + parseInt($("#selector-box").offset().left) - e.originalEvent.clientX;
                        let correction = gap % 8;
                       
                        if (correction > 4) { 
                            gap = gap + (8 - correction);
                        } else {
                            gap = gap - correction;
                        }
                        if (gap < 8) {
                            gap = 0;
                        }      

                        if(callbackThis.callbackContractRight != null) {
                            if(callbackThis.callbackContractRight(gap)) {
                                $("#selector-box").width($("#selector-box").width() - gap);
                            }
                        }
                    }   
                }
                if(callbackThis.resizingLeft) {
                    if(e.originalEvent.clientX >= (parseInt($("#selector-box").offset().left + 8))) {
                        let oldLeft = parseInt($("#selector-box").css("left"));
                        if(callbackThis.callbackContractLeft != null) {

                            let gap = e.originalEvent.clientX - parseInt($("#selector-box").offset().left);
                            let correction = gap % 8;
                            if (correction > 4) { 
                                gap = gap + (8 - correction);
                            } else {
                                gap = gap - correction;
                            }
                            if (gap < 8) {
                                gap = 0;
                            }      

                            if(callbackThis.callbackContractLeft(gap)){
                                $("#selector-box").css("left", oldLeft + gap);
                                $("#selector-box").width($("#selector-box").width() - gap);
                            }
                        }
                    }
                    if(e.originalEvent.clientX <= (parseInt($("#selector-box").offset().left - 8))) {
                        let oldLeft = parseInt($("#selector-box").css("left"));
                        if(callbackThis.callbackExpandLeft != null) {

                            let gap = parseInt($("#selector-box").offset().left) - e.originalEvent.clientX;
                            let correction = gap % 8;
                            if (correction > 4) { 
                                gap = gap + (8 - correction);
                            } else {
                                gap = gap - correction;
                            }
                            if (gap < 8) {
                                gap = 0;
                            }     

                            if(callbackThis.callbackExpandLeft(gap)){
                                $("#selector-box").css("left", oldLeft - gap);
                                $("#selector-box").width($("#selector-box").width() + gap);
                            }
                        }
                    }   
                }
                if(callbackThis.resizingDown) {
                    if(e.originalEvent.clientY >= ($("#selector-box").height() + parseInt($("#selector-box").offset().top + 8))) {   
                        
                        let gap = e.originalEvent.clientY - ($("#selector-box").height() + parseInt($("#selector-box").offset().top));
                        let correction = gap % 8;
                        if (correction > 4) { 
                            gap = gap + (8 - correction);
                        } else {
                            gap = gap - correction;
                        }
                        if (gap < 8) {
                            gap = 0;
                        }

                        if(callbackThis.callbackExpandDown != null) {
                            if(callbackThis.callbackExpandDown(gap)){
                                $("#selector-box").height($("#selector-box").height() + gap);
                            }
                        }
                    }
                    if(e.originalEvent.clientY <= ($("#selector-box").height() + parseInt($("#selector-box").offset().top - 8))) {    

                        let gap = ($("#selector-box").height() + parseInt($("#selector-box").offset().top)) - e.originalEvent.clientY;
                        let correction = gap % 8;
                        if (correction > 4) { 
                            gap = gap + (8 - correction);
                        } else {
                            gap = gap - correction;
                        }
                        if (gap < 8) {
                            gap = 0;
                        }      

                        if(callbackThis.callbackContractDown != null) {
                            if(callbackThis.callbackContractDown(gap)){
                                $("#selector-box").height($("#selector-box").height() - gap);
                            }
                        }
                    }   
                }
                if(callbackThis.resizingUp) {
                    if(e.originalEvent.clientY >= (parseInt($("#selector-box").offset().top + 8))) {
                        let gap = e.originalEvent.clientY - parseInt($("#selector-box").offset().top);
                        let correction = gap % 8;
                        if (correction > 4) { 
                            gap = gap + (8 - correction);
                        } else {
                            gap = gap - correction;
                        }
                        if (gap < 8) {
                            gap = 0;
                        }

                        let oldTop= parseInt($("#selector-box").css("top"));
                        if(callbackThis.callbackContractUp != null) {
                            if(callbackThis.callbackContractUp(gap)){
                                $("#selector-box").css("top", oldTop + gap);
                                $("#selector-box").height($("#selector-box").height() - gap);
                            }
                        }
                    }
                    if(e.originalEvent.clientY <= (parseInt($("#selector-box").offset().top - 8))) {

                        let gap = parseInt($("#selector-box").offset().top - e.originalEvent.clientY);
                        let correction = gap % 8;
                        if (correction > 4) { 
                            gap = gap + (8 - correction);
                        } else {
                            gap = gap - correction;
                        }
                        if (gap < 8) {
                            gap = 0;
                        }

                        let oldTop= parseInt($("#selector-box").css("top"));
                        if(callbackThis.callbackExpandUp != null) {
                            if(callbackThis.callbackExpandUp(gap)) {
                                $("#selector-box").css("top", oldTop - gap);
                                $("#selector-box").height($("#selector-box").height() + gap);
                            }
                        }
                    }   
                }
            }

            // check if cursor within 8px of right border of selector-box
            const grabMargin = 8;
            if(callbackThis.horizontalResizing && Math.abs(e.originalEvent.clientX - (($("#selector-box").width() + parseInt($("#selector-box").offset().left)))) < grabMargin &&
            e.originalEvent.clientY > parseInt($("#selector-box").offset().top) && e.originalEvent.clientY < (parseInt($("#selector-box").offset().top) + $("#selector-box").height())) {
                $('#selector-box').css('cursor', 'ew-resize'); // 'default' to revert
                callbackThis.resizingRight = true;
                callbackThis.resizingLeft = false;
                callbackThis.resizingDown = false;
                callbackThis.resizingUp = false;
                $(callbackThis.id).draggable( 'disable' )
            } 
            else if(callbackThis.horizontalResizing && Math.abs(e.originalEvent.clientX - (parseInt($("#selector-box").offset().left))) < grabMargin && 
            e.originalEvent.clientY > parseInt($("#selector-box").offset().top) && e.originalEvent.clientY < (parseInt($("#selector-box").offset().top) + $("#selector-box").height())) {
                $('#selector-box').css('cursor', 'ew-resize'); // 'default' to revert
                callbackThis.resizingLeft = true;
                callbackThis.resizingRight = false;
                callbackThis.resizingDown = false;
                callbackThis.resizingUp = false;

                $(callbackThis.id).draggable( 'disable' )
            } else if (callbackThis.verticalResizing && Math.abs(e.originalEvent.clientY - (($("#selector-box").height() + parseInt($("#selector-box").offset().top)))) < grabMargin && 
            e.originalEvent.clientX > parseInt($("#selector-box").offset().left) && e.originalEvent.clientX < (parseInt($("#selector-box").offset().left) + $("#selector-box").width())) {                
                $('#selector-box').css('cursor', 'ns-resize'); // 'default' to revert
                $(callbackThis.id).draggable( 'disable' );
                callbackThis.resizingDown = true;
                callbackThis.resizingLeft = false;
                callbackThis.resizingRight = false;
                callbackThis.resizingUp = false;

            } else if (callbackThis.verticalResizing && Math.abs(e.originalEvent.clientY - (parseInt($("#selector-box").offset().top))) < grabMargin && 
            e.originalEvent.clientX > parseInt($("#selector-box").offset().left) && e.originalEvent.clientX < (parseInt($("#selector-box").offset().left) + $("#selector-box").width())) {                
                $('#selector-box').css('cursor', 'ns-resize'); // 'default' to revert
                $(callbackThis.id).draggable( 'disable' );
                callbackThis.resizingUp = true;
                callbackThis.resizingLeft = false;
                callbackThis.resizingRight = false;
                callbackThis.resizingDown = false;
            } else if (!callbackThis.resizing) {
                    $('#selector-box').css('cursor', 'default');
                    this.resizingRight = false;
                    this.resizingLeft = false;
                    this.resizingDown = false;
                    this.resizingUp = false;
                    this.resizing = false;
                    $(callbackThis.id).draggable( 'enable' )
            }
        });

        // Expander button callbacks
        $("#selector-box").mousedown(function() {  
            if ($("#selector-box").css("cursor") == "ew-resize") {
                callbackThis.resizing = true;
            } else if ($("#selector-box").css("cursor") == "ns-resize") {
                callbackThis.resizing = true;
            }
        });

    }

    bindCallbackExpandUp(callback) {
        this.callbackExpandUp = callback;
    }
    bindCallbackContractUp(callback) {
        this.callbackContractUp = callback;
    }
    bindCallbackExpandLeft(callback) {
        this.callbackExpandLeft = callback;
    }
    bindCallbackContractLeft(callback) {
        this.callbackContractLeft = callback;
    }
    bindCallbackExpandRight(callback) {
        this.callbackExpandRight = callback;
    }
    bindCallbackExpandDown(callback) {
        this.callbackExpandDown = callback;
    }
    bindCallbackContractRight(callback) {
        this.callbackContractRight = callback;
    }
    bindCallbackContractDown(callback) {
        this.callbackContractDown = callback;
    }

    
    setWidth(width) {
        if (width % 8 != 0) console.log('Set width error!');
        $(this.id).css('width', width + 'px');
    }
    
    setHeight(height) {
        if (height % 8 != 0) console.log('Set height error!');
        $(this.id).css('height', height + 'px');
    }
    
    isResizing() {
        return this.resizing;
    }

    isSelected() {
        return $(this.id).hasClass("selected");
    }
    getExtents() {
        return qs("#selector-box").getBoundingClientRect();
    }

    hide() {
        $(this.id).addClass("hidden");
        $("#expand-right-button").addClass("hidden");
        $("#expand-down-button").addClass("hidden");
        this.resizingLeft = false;
        this.resizingRight = false;
        this.resizingDown = false;
        this.resizingUp = false;
    }
    show(horizontalResizing, verticalResizing) {

        // Store resizing
        this.horizontalResizing = horizontalResizing;
        this.verticalResizing = verticalResizing;

        // Unhide bounding selector box
        $(this.id).removeClass("hidden");
        
        // Unhide selectior box 
         $("#selector-box").addClass("selected");
         $("#expand-right-button").removeClass("hidden");
         $("#expand-down-button").removeClass("hidden");
    }

    positionButtons(){
        // Position expand right button
        let expandRightPosLeft = $(this.id).width();
        let expandRightPosTop = 0;
        $("#expand-right-button").css("left", expandRightPosLeft);
        $("#expand-right-button").css("top", expandRightPosTop);

        // Position expand down button
        let expandDownPosLeft = parseInt($(this.id).css("left")) + ($(this.id).width() / 2) - ($("#expand-down-button").width() / 2);
        let expandDownPosTop = parseInt($(this.id).css("top")) + $(this.id).height();
        $("#expand-down-button").css("left", expandDownPosLeft);
        $("#expand-down-button").css("top", expandDownPosTop);
    }

    position(componentPos, componentExtents) {

        // Place selector box
        $(this.id).css("left", componentPos.left);
        $(this.id).css("top", componentPos.top);

        // Size selector box
        $(this.id).css("width", componentExtents.width);
        $(this.id).css("height", componentExtents.height);

        // Position buttons
        this.positionButtons();
    }
    getPosition() {
        return { "x" : $(this.id).css("left"), "y" : $(this.id).css("top") };
    }
    getSize() {
        return { "width" : $(this.id).css("width"), "height" : $(this.id).css("height") };
    }
    bindDragCallback(callback) {
        //call on leaveCallback when draggable is dragged
        let callbackThis = this;
        $(this.id).draggable({
            drag: function( event, ui ) { callback(event, ui); },
            containment: "#snap-area",
            grid: [ 8, 8 ]
        });
    }
    bindOnLeaveCallback(callback) {
        this.onLeaveCallback = callback;
    }
    getId() {
        return this.id;
    }
}

// Export
export {SelectorBox};