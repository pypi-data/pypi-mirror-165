'use strict';
import {Component} from "../Components/Designer/component.js";

class DesignerPage {

    constructor(pageIndex) {

        // Store page index
        this.pageIndex = pageIndex;

        // Initialize state
        this.state = {};
        this.state['page-name'] = 'Blank Page';
        this.state['page-width'] = 792;
        this.state['page-height'] = 792;
        this.state['page-background-color'] = '#ECEDEF';

        // Z index bounds
        this.minZIndex = -1;
        this.maxZIndex = -1;

        // Initialize componet map
        this.componentMap = {};

        // Initialize componet count
        this.componentCount = 0;

        // Click callback
        this.clickCallback = null;
        this.deleteCallback = null;

        // Create page DOM element
        let pageItem = createElement("li", "page-" + pageIndex, "page-item");

        let pageTrashCan = createElement("i", "", "fa-light fa-trash-can page-icon");
        $(pageItem).append(pageTrashCan);

        let pageSpan = createElement("span", "", "page-label");
        $(pageSpan).text(this.state['page-name']);
        $(pageItem).append(pageSpan);
  
        let pageTree = qs("#page-tree-manager .page-tree");
        $(pageTree).append(pageItem);

        // Click callback
        let callbackThis = this;
        $(pageItem).click(function() {
            callbackThis.clickCallback(pageIndex);
        });

        // Delete page callback
        $(pageTrashCan).click(function(e) {
            e.preventDefault();
            if (qsa('.page-tree li').length > 1) {
                callbackThis.deleteCallback(pageIndex);
            }
        });

    }

    updateComponentPositions() {        
        let componentKeys = Object.keys(this.componentMap);
        for(let i = 0; i < componentKeys.length; i++) {
            let componentKey = componentKeys[i];
            let component = this.componentMap[componentKey];
            component.updatePosition();
        }
    }

    bindClickCallback(callbackClick) {
        this.clickCallback = callbackClick;
    }

    bindDeleteButtonCallback(callbackRightClick) {
        this.deleteCallback = callbackRightClick;
    }

    getPageIndex() {
        return this.pageIndex;
    }

    getComponentById(id) {
        return this.componentMap[id];
    }
    
    getComponentMap() {
        return this.componentMap;
    }

    getComponentCounter() {
        return this.componentCount;
    }

    getMinZIndex() {
        return this.minZIndex;
    }

    getMaxZIndex() {
        return this.maxZIndex;
    }

    addComponent(component, launcher=false) {
        this.componentMap[component.getId()] = component;
        this.componentCount = Math.max(this.componentCount, component.getComponentIndex() + 1);
        if (!launcher) {
            if (this.minZIndex == -1) {
                this.minZIndex = component.getZIndex();
            } else {
                this.minZIndex = Math.min(this.minZIndex, component.getZIndex());
            }
            if (this.maxZIndex == -1) {
                this.maxZIndex = component.getZIndex();
            } else {
                this.maxZIndex = Math.max(this.maxZIndex, component.getZIndex());
            }
        }
    }

    lowerZIndex(component) {

        // Get z index of components
        let componentZIndex = component.getZIndex();
    
        // Get components in bounds
        let components = qsa("div[data-type=component]");
                
        // Find next lowest element 
        let nextLowestZIndex = -1;
        let nextLowestElement = null;
        for(let i = 0; i < components.length; i++) {
            let el = components[i];
            if (el.id == component.getId()) continue;
            let elZIndex = parseInt($(el).css("z-index"));
            if(nextLowestElement == null && elZIndex < componentZIndex) {
                nextLowestElement = el;
                nextLowestZIndex = elZIndex;
            } else if (elZIndex > nextLowestZIndex && elZIndex < componentZIndex) {
                nextLowestElement = el;
                nextLowestZIndex = elZIndex;
            }
        }
        
        // If we found a next lowest element, swap z index
        if (nextLowestElement != null) {
            component.setZIndex(nextLowestZIndex);
            $(nextLowestElement).css("z-index", componentZIndex);
        }
    }

    raiseZIndex(component) {

      // Get z index of components
      let componentZIndex = component.getZIndex();

      // Get components in bounds
      let components = qsa("div[data-type=component]");
        
      // Find next highest element in bounds
      let nextHighestZIndex = -1;
      let nextHighestElement = null;
      for(let i = 0; i < components.length; i++) {
          let el = components[i];
          if (el.id == component.getId()) continue;
          let elZIndex = parseInt($(el).css("z-index"));
          if(nextHighestElement == null && elZIndex > componentZIndex) {
              nextHighestElement = el;
              nextHighestZIndex = elZIndex;
          } else if (elZIndex < nextHighestZIndex && elZIndex > componentZIndex) {
              nextHighestElement = el;
              nextHighestZIndex = elZIndex;
          }
      }
      
      // If we found a next lowest element, swap z index
      if (nextHighestElement != null) {
          component.setZIndex(nextHighestZIndex);
          $(nextHighestElement).css("z-index", componentZIndex);
      }
    }

    raiseAllZIndex(component) {

      // Get z index of components
      let componentZIndex = component.getZIndex();

      // Query all components
      let elements = qsa("div[data-type=component]");

      // Lower all higher components
      for(let i = 0; i < elements.length; i++) {
          let el = elements[i];
          let elZIndex = parseInt($(el).css("z-index"));
          if(elZIndex > componentZIndex) {
              $(el).css("z-index", elZIndex - 1);
          }
      }

      // Set to lowest z index
      component.setZIndex(this.maxZIndex);
    }
  
    lowerAllZIndex(component) {

        // Get z index of components
        let componentZIndex = component.getZIndex();

        // Query all components
        let elements = qsa("div[data-type=component]");

        // Raise all lower components
        for(let i = 0; i < elements.length; i++) {
            let el = elements[i];
            let elZIndex = parseInt($(el).css("z-index"));
            if(elZIndex < componentZIndex) {
                $(el).css("z-index", elZIndex + 1);
            }
        }

        // Set to lowest z index
        component.setZIndex(this.minZIndex);
    }

    raiseAllZIndexGroup(components) {

        // Tag group elements 
        for (let i = 0; i < components.length; i++) {
            components[i].setGrouped();
        }
  
        // Query all components
        let elements = qsa("div[data-type=component]");

        // Map number of elements higher
        let numberOfElementsHigher = {};
        for(let i = 0; i < components.length; i++) {
            numberOfElementsHigher[components[i].getId()] = 0;
        }
  
        // Track downgrades
        let downgradeMap = {};
        for(let i = 0; i < elements.length; i++) {
            downgradeMap[elements[i].id] = 0;
        }

        // Iterate through all elements
        for (let i = 0; i < elements.length; i++ ){ 
        
            // Get element
            let el = elements[i];
            let elZIndex = parseInt($(el).css("z-index"));

            // Skip same
            if (this.componentMap["#" + el.id].isGrouped()) continue;

            // Lower component for each group lower higher
            for(let j = 0; j < components.length; j++) {
                let componentZIndex = components[j].getZIndex();
                if(elZIndex > componentZIndex) {
                    downgradeMap[el.id]++;
                    numberOfElementsHigher[components[j].getId()]++;
                }
            }
        }

        // Downgrade
        for(let i = 0; i < elements.length; i++) {
            let el = elements[i];
            if (downgradeMap[el.id] > 0) {
                $(el).css("z-index", parseInt($(el).css("z-index")) - downgradeMap[el.id]);
            }
        }

        // Update group entries
        for(let i = 0; i < components.length; i++) {
            components[i].setZIndex(components[i].getZIndex() + numberOfElementsHigher[components[i].getId()]);
        }        
        
        // Untag group elements 
        for (let i = 0; i < components.length; i++) {
            components[i].unsetGrouped();
        }
    }

    lowerAllZIndexGroup(components) {

        // Tag group elements 
        for (let i = 0; i < components.length; i++) {
            components[i].setGrouped();
        }
  
        // Query all components
        let elements = qsa("div[data-type=component]");

        // Map number of elements lower
        let numberOfElementsLower = {};
        for(let i = 0; i < components.length; i++) {
            numberOfElementsLower[components[i].getId()] = 0;
        }
  
        // Track downgrades
        let upgradeMap = {};
        for(let i = 0; i < elements.length; i++) {
            upgradeMap[elements[i].id] = 0;
        }

        // Iterate through all elements
        for (let i = 0; i < elements.length; i++ ){ 
        
            // Get element
            let el = elements[i];
            let elZIndex = parseInt($(el).css("z-index"));

            // Skip same
            if (this.componentMap["#" + el.id].isGrouped()) continue;

            // Lower component for each group lower higher
            for(let j = 0; j < components.length; j++) {
                let componentZIndex = components[j].getZIndex();
                if(elZIndex < componentZIndex) {
                    upgradeMap[el.id]++;
                    numberOfElementsLower[components[j].getId()]++;
                }
            }
        }

        // Downgrade
        for(let i = 0; i < elements.length; i++) {
            let el = elements[i];
            if (upgradeMap[el.id] > 0) {
                $(el).css("z-index", parseInt($(el).css("z-index")) + upgradeMap[el.id]);
            }
        }

        // Update group entries
        for(let i = 0; i < components.length; i++) {
            components[i].setZIndex(components[i].getZIndex() - numberOfElementsLower[components[i].getId()]);
        }        
        
        // Untag group elements 
        for (let i = 0; i < components.length; i++) {
            components[i].unsetGrouped();
        }
    }

    setNewComponentToTop(component) {
        $(component.getId()).css("z-index", ++this.maxZIndex);
    }
    
    deleteComponent(componentId) {
        delete this.componentMap[componentId];
    }

    incrementComponentCounter() {
        this.componentCount++;
    }

    findGroupedElements(groupStart, groupEnd) {
        let groupedElements = [];
        let componentKeys = Object.keys(this.componentMap);
        for(let i = 0; i < componentKeys.length; i++) {
            let componentKey = componentKeys[i];
            let component = this.componentMap[componentKey];
            let componentPositionStart = {
                "left" : $(component.getId()).position().left,
                "top" : $(component.getId()).position().top
            };
            let componentPositionEnd = {
                "left" : $(component.getId()).position().left + $(component.getId()).width(),
                "top" : $(component.getId()).position().top + $(component.getId()).height()
            };
            
            let leftExtentsContained = (componentPositionStart.left <= groupStart.left && componentPositionEnd.left >= groupStart.left) || (componentPositionStart.left >= groupStart.left && componentPositionStart.left <= groupEnd.left);
            let topExtentsContained = (componentPositionStart.top <= groupStart.top && componentPositionEnd.top >= groupStart.top) || (componentPositionStart.top >= groupStart.top && componentPositionStart.top <= groupEnd.top);
            if(leftExtentsContained && topExtentsContained) {
                groupedElements.push(component);
            }
        }
        return groupedElements;
    }

    findTopLayerElementInGroup(groupStart, groupEnd) {

        let topLayerBoxElement = null;
        let topLayerBoxZIndex = -100000;

        let topLayerGroupElement = null;
        let topLayerZIndex = -1000000;
        let componentKeys = Object.keys(this.componentMap);

        // non-box pass
        for(let i = 0; i < componentKeys.length; i++) {       
            let componentKey = componentKeys[i];
            let component = this.componentMap[componentKey];

            if (!qs(component.getId()).classList.contains("component-box")) {
                let componentPositionStart = {
                    "left" : $(component.getId()).offset().left,
                    "top" : $(component.getId()).offset().top
                };
                let componentPositionEnd = {
                    "left" : $(component.getId()).offset().left + $(component.getId()).width(),
                    "top" : $(component.getId()).offset().top + $(component.getId()).height()
                };            

                let leftExtentsContained = (componentPositionStart.left <= groupStart.left && componentPositionEnd.left >= groupStart.left) || (componentPositionStart.left >= groupStart.left && componentPositionStart.left <= groupEnd.left);
                let topExtentsContained = (componentPositionStart.top <= groupStart.top && componentPositionEnd.top >= groupStart.top) || (componentPositionStart.top >= groupStart.top && componentPositionStart.top <= groupEnd.top);     
                if(leftExtentsContained && topExtentsContained) {
                    if (component.getZIndex() > topLayerZIndex) {
                        topLayerZIndex = component.getZIndex();
                        topLayerGroupElement = component;
                    }
                }
            } else {

                // border width
                let borderWidth = parseInt($(component.getId()).css("border-width"));

                // outer box extent
                let outerBoxExtent = {
                    "left" : $(component.getId()).offset().left - 4,
                    "top" : $(component.getId()).offset().top - 4,
                    "right" : $(component.getId()).offset().left + $(component.getId()).width() + borderWidth * 2 + 4,
                    "bottom" : $(component.getId()).offset().top + $(component.getId()).height() + borderWidth * 2 + 4
                };

                // inner box extent
                let innerBoxExtent = {
                    "left" : $(component.getId()).position().left + borderWidth + 4,
                    "top" : $(component.getId()).position().top + borderWidth + 4,
                    "right" : $(component.getId()).position().left + $(component.getId()).width() + borderWidth - 4,
                    "bottom" : $(component.getId()).position().top + $(component.getId()).height() + borderWidth - 4
                };

                // group extent
                let groupExtent = {
                    "left" : groupStart.left,
                    "top" : groupStart.top,
                    "right" : groupEnd.left,
                    "bottom" : groupEnd.top
                };

                // test boxes
                let groupInOuterBox = testBoxIntersection(outerBoxExtent, groupExtent);
                let groupInInnerBox = testBoxIntersection(innerBoxExtent, groupExtent);
                
                // Add box
                if(groupInOuterBox && !groupInInnerBox) {
                    topLayerZIndex = component.getZIndex();
                    topLayerGroupElement = component;
                }
            }
        }
        if (topLayerGroupElement != null) {
            return topLayerGroupElement;
        }

        // box pass
        return topLayerBoxElement;
    }

    getState() {
        let state = {};
        state['page-name'] = $("#page-name input").val();
        state['page-width'] = $("#page-width input").val();
        state['page-height'] = $("#page-height input").val();
        state['page-background-color'] = $("#page-background-color input").val();
        let componentIds = Object.keys(this.componentMap);
        for(let i = 0; i < componentIds.length; i++) {
            let componentKey = componentIds[i];
            let component = this.componentMap[componentKey];
            state[component.getId()] = component.getState();
        }
        return state;
    };

    getValue() {
        let value = {};
        let componentIds = Object.keys(this.componentMap);
        for(let i = 0; i < componentIds.length; i++) {
            let componentKey = componentIds[i];
            let component = this.componentMap[componentKey];
            value[component.getElementName()] = component.getValue();
        }
        return value;
    };

    activatePage() {
        $(".active-page").removeClass("active-page");
        $("#page-" + this.pageIndex + " span").addClass("active-page");
        $("#page-" + this.pageIndex + " i").addClass("active-page");
        if('page-name' in this.state) {
            $("#page-name input").val(this.state['page-name']);
            $("#page-width input").val(parseInt(this.state['page-width']));
            $("#page-height input").val(parseInt(this.state['page-height']));
            $("#page-background-color input").val(this.state['page-background-color']);
            $("#drag-area").css("background-color", this.state['page-background-color']);
        } else {
            $("#page-name input").val("Page " + this.pageIndex);
            $("#page-width input").val(800);
            $("#page-height input").val(800);
            $("#page-background-color input").val("#ECEDEF");
            $("#drag-area").css("background-color", "#ECEDEF");
        }
        
        $("#drag-area").width(this.state['page-width']);
        $("#drag-area").height(this.state['page-height']);
    }

    setState(state) {
        this.state = state;
        $("#page-" + this.pageIndex + " span").text(this.state['page-name']);
    }
    
    loadState() {
        return this.state;
    }

    getPageName() {
        return this.state['page-name'];
    }

    getPageWidth() {
        return this.state['page-width'];
    }

    getPageHeight() {
        return this.state['page-height'];
    }

    saveState() {
        this.state = this.getState();
    }

    remove() {
        let componentKeys = Object.keys(this.componentMap);
        for(let i = 0; i < componentKeys.length; i++) {
            let componentKey = componentKeys[i];
            let component = this.componentMap[componentKey];
            delete this.componentMap[componentKey];
            component.remove();
        }
    }

    checkAlignment(bounds, blackList) {

        // Get check componnet bounds
        let checkComponentLeft = bounds.left;
        let checkComponentRight = bounds.right;
        let checkComponentTop = bounds.top;
        let checkComponentBottom = bounds.bottom;
        let checkComponentWidth = checkComponentRight - checkComponentLeft;
        let checkComponentHeight = checkComponentBottom - checkComponentTop;
        let checkComponentMiddleHorizontal = checkComponentLeft + (checkComponentRight - checkComponentLeft) / 2;
        let checkComponentMiddleVertical = checkComponentTop + (checkComponentBottom - checkComponentTop) / 2;

        // Alignmnet
        let alignment = {};
        
        alignment['left'] = [];
        alignment['right'] = [];
        alignment['top'] = [];
        alignment['bottom'] = [];
        alignment['middleHorizontal'] = [];
        alignment['middleVertical'] = [];

        // Scan through components
        let componentKeys = Object.keys(this.componentMap);

        for(let i = 0; i < componentKeys.length; i++) {

            // Skip check component
            let component = this.componentMap[componentKeys[i]];
            let blMatch = false;
            for (let i = 0; i < blackList.length; i++) {
                if (component == blackList[i]) {
                    blMatch = true;
                    break;
                }
            }
            if (blMatch) continue;

            // Get component bounds
            let componentLeft = $(component.getId()).offset().left;
            let componentRight = $(component.getId()).offset().left + parseInt($(component.getId()).css('width'));
            let componentTop = $(component.getId()).offset().top;
            let componentBottom = $(component.getId()).offset().top + parseInt($(component.getId()).css('height'));
            let componentMiddleHorizontal = componentLeft + (componentRight - componentLeft) / 2;
            let componentMiddleVertical = componentTop + (componentBottom - componentTop) / 2;

            // Check alignment
            if (Math.abs(componentLeft - checkComponentLeft) < 1) {
                alignment['left'].push(component);
            }
            if (Math.abs(componentRight - checkComponentLeft) < 1) {
                alignment['left'].push(component);
            }

            if (Math.abs(componentLeft - checkComponentRight) < 1) {
                alignment['right'].push(component);
            }
            if (Math.abs(componentRight - checkComponentRight) < 1) {
                alignment['right'].push(component);
            }

            if (Math.abs(componentTop - checkComponentTop) < 1) {
                alignment['top'].push(component);
            }
            if (Math.abs(componentBottom - checkComponentTop) < 1) {
                alignment['top'].push(component);
            }

            if (Math.abs(componentTop - checkComponentBottom) < 1) {
                alignment['bottom'].push(component);
            }
            if (Math.abs(componentBottom - checkComponentBottom) < 1) {
                alignment['bottom'].push(component);
            }

            if (Math.abs(componentTop - checkComponentBottom) < 1) {
                alignment['bottom'].push(component);
            }
            if (Math.abs(componentBottom - checkComponentBottom) < 1) {
                alignment['bottom'].push(component);
            }

            if (Math.abs(componentMiddleHorizontal - checkComponentMiddleHorizontal) < 1) {
                alignment['middleHorizontal'].push(component);
            }

            if (Math.abs(componentMiddleVertical - checkComponentMiddleVertical) < 1) {
                alignment['middleVertical'].push(component);
            }   

        }


        // Compute alignment lines
        let alignmentLines = {};

        // Left alignment
        if (alignment['left'].length > 0) {
            
            let alignmentTop = checkComponentTop;
            let alignmentBottom = checkComponentTop + checkComponentHeight;
            
            for(let i = 0; i < alignment['left'].length; i++) {
                let component = alignment['left'][i];
                let componentTop = $(component.getId()).offset().top;
                let componentBottom = $(component.getId()).offset().top + $(component.getId()).height();
                if (componentTop < alignmentTop) {
                    alignmentTop = componentTop;
                }
                if (componentBottom > alignmentBottom) {
                    alignmentBottom = componentBottom;
                }
            }

            alignmentLines['left'] = {
                "left" : checkComponentLeft,
                "top" : alignmentTop,
                "bottom" : alignmentBottom
            };
        }

        if (alignment['right'].length > 0) {
            
            let alignmentTop = checkComponentTop;
            let alignmentBottom = checkComponentTop + checkComponentHeight;
            
            for(let i = 0; i < alignment['right'].length; i++) {
                let component = alignment['right'][i];
                let componentTop = $(component.getId()).offset().top;
                let componentBottom = $(component.getId()).offset().top + $(component.getId()).height();
                if (componentTop < alignmentTop) {
                    alignmentTop = componentTop;
                }
                if (componentBottom > alignmentBottom) {
                    alignmentBottom = componentBottom;
                }
            }

            alignmentLines['right'] = {
                "left" : checkComponentRight,
                "top" : alignmentTop,
                "bottom" : alignmentBottom
            };
        }

        if (alignment['top'].length > 0) {
            
            let alignmentLeft = checkComponentLeft;
            let alignmentRight = checkComponentLeft + checkComponentWidth;
            
            for(let i = 0; i < alignment['top'].length; i++) {
                let component = alignment['top'][i];
                let componentLeft = $(component.getId()).offset().left;
                let componentRight = $(component.getId()).offset().left + parseInt($(component.getId()).css('width'));
                if (componentLeft < alignmentLeft) {
                    alignmentLeft = componentLeft;
                }
                if (componentRight > alignmentRight) {
                    alignmentRight = componentRight;
                }
            }

            alignmentLines['top'] = {
                "top" : checkComponentTop,
                "left" : alignmentLeft,
                "right" : alignmentRight
            };
        }

        if (alignment['bottom'].length > 0) {
            
            let alignmentLeft = checkComponentLeft;
            let alignmentRight = checkComponentLeft + checkComponentWidth;
            
            for(let i = 0; i < alignment['bottom'].length; i++) {
                let component = alignment['bottom'][i];
                let componentLeft = $(component.getId()).offset().left;
                let componentRight = $(component.getId()).offset().left + parseInt($(component.getId()).css('width'));
                if (componentLeft < alignmentLeft) {
                    alignmentLeft = componentLeft;
                }
                if (componentRight > alignmentRight) {
                    alignmentRight = componentRight;
                }
            }

            alignmentLines['bottom'] = {
                "top" : checkComponentBottom,
                "left" : alignmentLeft,
                "right" : alignmentRight
            };
        }

        if (alignment['middleHorizontal'].length > 0) {

            let alignmentTop = checkComponentTop;
            let alignmentBottom = checkComponentTop + checkComponentHeight;

            for(let i = 0; i < alignment['middleHorizontal'].length; i++) {
                let component = alignment['middleHorizontal'][i];
                let componentTop = $(component.getId()).offset().top;
                let componentBottom = $(component.getId()).offset().top + $(component.getId()).height();
                if (componentTop < alignmentTop) {
                    alignmentTop = componentTop;
                }
                if (componentBottom > alignmentBottom) {
                    alignmentBottom = componentBottom;
                }
            }

            alignmentLines['middleHorizontal'] = {
                "left" : checkComponentMiddleHorizontal,
                "top" : alignmentTop,
                "bottom" : alignmentBottom
            };
        }

        if (alignment['middleVertical'].length > 0) {

            let alignmentLeft = checkComponentLeft;
            let alignmentRight = checkComponentLeft + checkComponentWidth;

            for(let i = 0; i < alignment['middleVertical'].length; i++) {
                let component = alignment['middleVertical'][i];
                let componentLeft = $(component.getId()).offset().left;
                let componentRight = $(component.getId()).offset().left + $(component.getId()).width();
                if (componentLeft < alignmentLeft) {
                    alignmentLeft = componentLeft;
                }
                if (componentRight > alignmentRight) {
                    alignmentRight = componentRight;
                }
            }   
            
            alignmentLines['middleVertical'] = {
                "top" : checkComponentMiddleVertical,
                "left" : alignmentLeft,
                "right" : alignmentRight
            };
        }

        return alignmentLines;
    }
}

// Export
export {DesignerPage};