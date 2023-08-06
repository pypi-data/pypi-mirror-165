'use strict';

// Menu Node Context
class Component {
    constructor(componentIndex) {

        // Store component index
        this.componentIndex = componentIndex;

        // Save component index and id
        this.id = "#component-" + componentIndex;

        // Component Name
        this.elementName = "Default";

        // Component Position
        this.componentPosition = {
            "top" : 0,
            "left" : 0
        };

        // Initialize menu section (area on right side)
        // to null
        this.menuSections = [];       

        // Special type
        this.selectType = "default";

        // Size constraints
        this.minWidth = -1;
        this.minHeight = -1;
        this.maxWidth = -1;
        this.maxHeight = -1;

        // Grouped property
        this.grouped = false;
    }
    
    setGrouped() {
        this.grouped = true;
    }
    unsetGrouped() {
        this.grouped = false;
    }
    isGrouped() {
        return this.grouped;
    }

    getComponentIndex() {
        return this.componentIndex;
    }
    
    setupClickCallback() {

        // Init click callback
        this.clickCallback = null;

        // Add click listener
        let callbackThis = this;
        $(this.id).click((e)=> {

            /* Special Handler For Bordered Elements */
            if(callbackThis.selectType == "border" && e.target !== e.currentTarget) return;

            // Call callback if it exists
            if(callbackThis.clickCallback != null) {
                callbackThis.clickCallback(this);
            }
        });

        // Right click menu setup
        qs(this.id).addEventListener('contextmenu',function(event){
            
            // Prevent default
            event.preventDefault();

            // Call callback
            if(callbackThis.rightClickCallback != null) {
                callbackThis.rightClickCallback(event);
            }           
        },true);

        // Mouse down callback
        qs(this.id).addEventListener('mousedown',function(event){
            if (callbackThis.mouseDownCallback != null) {
                callbackThis.mouseDownCallback(event);
            }
        });

        // Next page callback
        $(this.id + " button").click(() => {
            if(callbackThis.nextPage != "None" && callbackThis.nextPageCallback != null) {
                callbackThis.nextPageCallback(callbackThis.nextPage);
            }
        });
    }
    
    bindSelectbox(selectbox) {
        this.selectbox = selectbox;
    }
    
    bindClickCallback(callback) {
        this.clickCallback = callback;
    }

    bindRightClickCallback(callback) {
        this.rightClickCallback = callback;
    }

    bindMouseDownCallback(callback) {
        this.mouseDownCallback = callback;
    }

    updatePosition() {
        // Get drag area position
        let dragAreaPosition = $("#drag-area").offset();

        // Get absolute position
        let absolutePositionLeft = this.componentPosition.left + dragAreaPosition.left;
        let absolutePositionTop = this.componentPosition.top + dragAreaPosition.top;

        // Position component
        $(this.id).css('left', absolutePositionLeft);
        $(this.id).css('top', absolutePositionTop);
    }

    position(positionRelativeToDragArea) {

        // Get drag area position
        let dragAreaPosition = $("#drag-area").offset();

        // Get absolute position
        let absolutePositionX = positionRelativeToDragArea.x + dragAreaPosition.left;
        let absolutePositionY = positionRelativeToDragArea.y + dragAreaPosition.top;

        // Store component position
        this.componentPosition.top = positionRelativeToDragArea.y;
        this.componentPosition.left = positionRelativeToDragArea.x;

        // Position component
        $(this.id).css('left', absolutePositionX);
        $(this.id).css('top', absolutePositionY);
    }

    move(x, y) {

        // Update component position
        this.componentPosition.left += x;
        this.componentPosition.top += y;

       // Get drag area position
       let dragAreaPosition = $("#drag-area").offset();
       if(this.componentPosition.left % 8 != 0) {
            let error = this.componentPosition.left % 8;
            if(8 - error < error) {
                this.componentPosition.left += (8 - error);
            } else {
                this.componentPosition.left -= error;
            }
       }
       if(this.componentPosition.top % 8 != 0) {
            let error = this.componentPosition.top % 8;
            if(8 - error < error) {
                this.componentPosition.top += (8 - error);
            } else {
                this.componentPosition.top -= error;
            }
        }

        // Get absolute position
        let absolutePositionX = this.componentPosition.left + dragAreaPosition.left;
        let absolutePositionY = this.componentPosition.top + dragAreaPosition.top;
        
        // Translate component
        $(this.id).css('left', absolutePositionX + "px");
        $(this.id).css('top', absolutePositionY + "px");
    }

    canResizeHorizontally() {
        if (this.minWidth != this.maxWidth || (this.minWidth == -1 && this.maxWidth == -1)) {
            return true;
        }
        return false;
    }

    canResizeVertically() {
        if (this.minHeight != this.maxHeight || (this.minHeight == -1 && this.maxHeight == -1)) {
            return true;
        }
        return false;
    }

    setWidth(width) {
        if (width % 8 != 0) console.log('Set width error!');
        $(this.id).css('width', width + 'px');
    }

    setHeight(height) {
        if (height % 8 != 0) console.log('Set height error!');
        $(this.id).css('height', height + 'px');
    }
    
    expandRight(expansion) {
        let oldWidth = parseInt($(this.id).css('width'));
        if (this.maxWidth != -1 && oldWidth + expansion > this.maxWidth) return false;
        $(this.id).css('width', (oldWidth + expansion) + 'px');
        return true;
    }

    expandDown(expansion) {
        let oldHeight = parseInt($(this.id).css('height'));
        if (this.maxHeight != -1 && oldHeight + expansion > this.maxHeight) return false;
        $(this.id).css('height', (oldHeight + expansion) + 'px'); 
        return true;
    }

    contractRight(contraction) {
        let oldWidth = parseInt($(this.id).css('width'));
        if (this.minWidth != -1 && oldWidth - contraction < this.minWidth) return false;
        $(this.id).css('width', (oldWidth - contraction) + 'px'); 
        return true;
    }

    contractLeft(contraction) {
        let oldWidth = parseInt($(this.id).css('width'));
        if (this.minWidth != -1 && oldWidth - contraction < this.minWidth) return false;
        $(this.id).css('width', (oldWidth - contraction) + 'px'); 
        let oldLeft = parseInt($(this.id).css('left'));
        $(this.id).css('left', (oldLeft + contraction) + 'px');
        return true;
    }

    expandLeft(contraction) {
        let oldWidth = parseInt($(this.id).css('width'));
        if (this.maxWidth != -1 && oldWidth + contraction > this.maxWidth) return false;
        $(this.id).css('width', (oldWidth + contraction) + 'px'); 
        let oldLeft = parseInt($(this.id).css('left'));
        $(this.id).css('left', (oldLeft - contraction) + 'px');
        return true;
    }

    contractDown(contraction) {
        let oldHeight = parseInt($(this.id).css('height'));
        if (this.minHeight != -1 && oldHeight - contraction < this.minHeight) return false;
        $(this.id).css('height', (oldHeight - contraction) + 'px'); 

        return true;
    }

    expandUp(expansion) {
        let oldHeight = parseInt($(this.id).css('height'));
        if (this.maxHeight != -1 && oldHeight + expansion > this.maxHeight) return false;

        $(this.id).css('height', (oldHeight + expansion) + 'px'); 
        let oldTop = parseInt($(this.id).css('top'));
        $(this.id).css('top', (oldTop - expansion) + 'px');
        return true;
    }

    contractUp(contraction) {
        let oldHeight = parseInt($(this.id).css('height'));
        if (this.minHeight != -1 && oldHeight - contraction < this.minHeight) return false;

        $(this.id).css('height', (oldHeight - contraction) + 'px'); 
        let oldTop = parseInt($(this.id).css('top'));
        $(this.id).css('top', (oldTop + contraction) + 'px');
        return true;
    }

    getId() {
        return this.id;
    }

    addEditableContent() {
    }

    removeEditableContent() {
        for(let i = 0; i < this.menuSections.length; i++) {
            this.menuSections[i].remove();
        }
        this.menuSections = [];
    }

    getState() {

        // Get drag area pos
        let dragAreaPosition = $("#drag-area").offset();
        this.componentPosition.top = $(this.id).offset().top - dragAreaPosition.top;
        this.componentPosition.left = $(this.id).offset().left - dragAreaPosition.left;
        
        // Export state
        let state = {
            "top" : this.componentPosition.top,
            "left" : this.componentPosition.left,
            "width" : parseInt($(this.id).css('width')),
            "height" : parseInt($(this.id).css('height')),
            "id" : this.id,
            "index" : this.componentIndex,
            "zIndex" : parseInt($(this.id).css('z-index')),
            "name" : this.elementName
        };
        return state;
    }

    getValue() {
        return "unsupported";
    }

    updateValue(update) {
        return;
    }

    getElementName() {
        return this.elementName;
    }

    remove() {
        this.removeEditableContent();
        $(this.id).remove();
    }

    getZIndex() {
        return parseInt($(this.id).css('z-index'));
    }

    setZIndex(zIndex) {
        $(this.id).css('z-index', zIndex);
    }

    loadState(data) {

        // Check if editor
        let editor = qs("#drag-area") != null;

        // Store component position
        this.componentPosition.top = parseInt(data["top"]);
        this.componentPosition.left = parseInt(data["left"]);

        // Get absolute position of component
        let absolutePositionLeft;
        let absolutePositionTop;
        if (editor) {
            let dragAreaPosition = $("#drag-area").offset();
            absolutePositionLeft = this.componentPosition.left + dragAreaPosition.left;
            absolutePositionTop = this.componentPosition.top + dragAreaPosition.top;
        } else {
            absolutePositionLeft = this.componentPosition.left;
            absolutePositionTop = this.componentPosition.top;
        }

        $(this.id).css('left', absolutePositionLeft);
        $(this.id).css('top', absolutePositionTop);
        $(this.id).css('width', data["width"] + 'px');
        $(this.id).css('height', data["height"] + 'px');
        $(this.id).css('z-index', data["zIndex"]);
        this.elementName = data["name"];
        $(this.id).attr('component-name', this.elementName);
    }

    getLeft() {
        return $(this.id).offset().left;
    }
    getRight() {
        return $(this.id).offset().left + parseInt($(this.id).css('width'));
    }
    getTop() {
        return $(this.id).offset().top;
    }
    getBottom() {
        return $(this.id).offset().top + parseInt($(this.id).css('height'));
    }
    getWidth() {
        return parseInt($(this.id).css('width'));
    }
    getHeight() {
        return parseInt($(this.id).css('height'));
    }
    
}
