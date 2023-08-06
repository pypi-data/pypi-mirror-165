(function($) {
    'use strict';    

    // Editor
    let editor;
    let editor_language = 'python';

    // Archive
    let archive = [];
    let archiveMode = false;
    let archiveIndex = 0;
    let inputsDict = {};
    let inputCounter = 0;

    // Components
    let componentCounter = 0;
    let componentX = 0;
    let componentY = 0;

    // Next card
    let newCard = false;
    let newCardLine = -1;
    let newCardName = '';
    let newCardColor = '';
    let newCardFontColor = '';    

    // Same card
    let sameCard = false;
    
    // MD converter
    let converter;

    // Range
    var Range = ace.require('ace/range').Range // get reference to ace/range

    // Grouping
    let groupStart = -1;
    let groupEnd = -1;
    let groupedLines = null;

    // Component states
    let defaultComponentStates = {
        "card" : {
            "top": "0px",
            "left": "0px",
            "width": 400,
            "height": 80,
            "id": "",
            "index": 12,
            "zIndex": 1,
            "name": "card",
            "type": "card",
            "cardTitle": "Title",
            "borderRadius": 1,
            "borderWidth": 1,
            "borderColor": "#eeeeee",
            "borderStyle": "solid",
            "backgroundColor": "#fefefe",
            "boxShadow": true,
            "cardTitleAlignment": "left",
            "cardHeaderEnabled": false,
            "cardHeaderBorderEnabled": true,
            "headerColor": "#fefefe",
            "headerTextColor": "#000000"
        },
        "heading" : {
            "top": componentY,
            "left": componentX + 15,
            "width": 800,
            "height": 20,
            "id": "",
            "index": 26,
            "zIndex": 1,
            "name": "Default",
            "type": "heading",
            "headingText": "",
            "fontSize": 1,
            "headingAlignment": "start",
            "fontUnit": "rem",
            "textColor": "#ffffff",
            "backgroundColor": "#ffffff",
            "fontWeight": "600"
        },
        "table" : {
            "top": 336,
            "left": 384,
            "width": 320,
            "height": 128,
            "id": "#component-8",
            "index": 8,
            "zIndex": 5,
            "name": "Default",
            "type": "table",
            "headerHighlighted": false,
            "striped": true,
            "bordered": true,
            "hoverableRows": true,
            "numberOfDummyRows": 1
        },
        "image": {
            "top": 128,
            "left": 184,
            "width": 128,
            "height": 128,
            "id": "",
            "index": 26,
            "zIndex": 14,
            "name": "image",
            "type": "image",
            "imageURL": "",
            "imageTiling": "no-repeat",
            "imageFit": "contain",
            "imagePosition": "left",
            "borderRadius": 0,
            "borderWidth": 1,
            "borderColor": "#dee2e6",
            "borderStyle": "dashed",
            "showImageInDesigner": true
        },
        "model" : {
            'src' : ''
        }
    };

    // Socket
    let ws;

    // Exit
    let exit = false;
    let restarting = false;

    // Helper
    function listOfListsToDict(lists) {
        let dict = {};
        for (let i = 0; i < lists.length; i++) {
            let list = lists[i];
            dict[list[0]] = list[1];
        }
        return dict;
    }

    // Clear window
    function clearWindow() {
        let outputList = qs("#outputs-list");
        if(outputList) {
            for (let i = outputList.children.length; i >= 0; i--) {
                if (outputList.children[i] == undefined) continue;
                outputList.removeChild(outputList.children[i]);
            }
        }
    }

    // Create via socket  
    function createSocket(){
        console.log("Creating socket");
        ws = new WebSocket("ws://127.0.0.1:5678/");
        ws.onmessage = processSocketMessage;
        ws.onclose = function(e) {
            clearWindow();
            if (!restarting) window.close();
            console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
            setTimeout(function() {
                createSocket();
            }, 100);
            setTimeout(function() {
                if (restarting) {
                    window.close();
                }
            }, 3000);
        };
    }

    // Select card
    function selectCard(card) {

        // Unselect other card
        let selectedCard = qs('.card-selected');
        if (selectedCard != null) {          
            selectedCard.classList.remove('card-selected');
        }

        // Select card
        $(card).addClass('card-selected');

        // Group lines belonging to card
        let cardStartLine = parseInt($(card).attr('line-start'));
        let cardEndLine = parseInt($(card).attr('line-end'));

        groupLines(cardStartLine, cardEndLine);
    }
    function unselectCard(card) {
         let selectedCard = qs('.card-selected');
         if (selectedCard != null) {
            selectedCard.classList.remove('card-selected');
         }
        ungroupLines();
    }


    // Highlihgt lines
    function ungroupLines(startLine, endLine) {
        if (groupedLines != null) {
            editor.session.removeMarker(groupedLines);
            groupedLines = null;
        }
    }

    function groupLines(startLine, endLine) {

        // Cache grouping
        groupStart = startLine;
        groupEnd = endLine;

        // Ungroup lines
        ungroupLines();

        // Group lines
        if (startLine != endLine) {
            groupedLines = editor.session.addMarker(
                new Range(startLine - 1, 0, endLine - 1, 0), "ace_active-line grouped", "fullLine"
            );
        } else {
            let targetLineToGroup = editor.session.getLine(startLine - 1);
            groupedLines = editor.session.addMarker(
                new Range(startLine - 1, 0, startLine - 1, targetLineToGroup.length), "ace_active-line grouped", "fullLine"
            );
        }
    }

    // DOM Helpers
    function createInputCard(inputCardTitle, inputCardLineStart, inputCardLineEnd, inputCardComponentDOM) {
        
        // Create input card
        let inputCardDOM = createOutputComponentDOM("card", "", "#outputs-list", true);
        if (newCard) {
            inputCardLineStart = newCardLine;
        }
        setupOutputComponentDOMCard(inputCardDOM);

        // Check for click
        $(inputCardDOM).click(function() {
            let lineStart = parseInt($(inputCardDOM).attr('line-start'));
            let lineEnd = parseInt($(inputCardDOM).attr('line-end'));
            editor.gotoLine(lineStart);
            selectCard(inputCardDOM);
        });

        // Create card header
        let cardHeaderDOM = createElement("div", "card-header", "card-header-bar");
        inputCardDOM.appendChild(cardHeaderDOM);

        // Create card header contents 
        let variableNameCardHeaderDOM = createElement("span", "", "card-header-element");
        $(variableNameCardHeaderDOM).html(inputCardTitle);

        let endTab = createElement("div", "", "card-header-end-tab");
        let lineCardHeaderDOM = createElement("span", "", "card-header-element-bold");
        $(lineCardHeaderDOM).html(inputCardLineStart + "-" + inputCardLineEnd);

        // Setup minimize button
        let minimizeCardHeaderDOM = createElement("i", "", "fa-light fa-square-minus toggle-btn");
        $(minimizeCardHeaderDOM).click(()=>{
            let parentCard = minimizeCardHeaderDOM.parentElement.parentElement.parentElement;
            if ($(parentCard).attr("minimized") == "true") {
                let originalHeight = $(parentCard).attr('original-height');
                $(parentCard).css("height", originalHeight + 'px');
                $(parentCard).attr("minimized", "false");
                $(minimizeCardHeaderDOM).removeClass("fa-square-plus");
                $(minimizeCardHeaderDOM).addClass("fa-square-minus");
                $(minimizeCardHeaderDOM).css("color", "red");
            } else {
                $(parentCard).attr('minimized', 'true');
                $(parentCard).attr('original-height', $(parentCard).height() + 12);
                $(parentCard).css("height", "30px");
                $(minimizeCardHeaderDOM).removeClass("fa-square-minus");
                $(minimizeCardHeaderDOM).addClass("fa-square-plus");
                $(minimizeCardHeaderDOM).css("color", "green");
            }
        });

         // Setup minimize double click
         $("#" + inputCardDOM.id).dblclick(()=>{
            let parentCard = minimizeCardHeaderDOM.parentElement.parentElement.parentElement;
            if ($(parentCard).attr("minimized") == "true") {
                let originalHeight = $(parentCard).attr('original-height');
                $(parentCard).css("height", originalHeight + 'px');
                $(parentCard).attr("minimized", "false");
                $(minimizeCardHeaderDOM).removeClass("fa-square-plus");
                $(minimizeCardHeaderDOM).addClass("fa-square-minus");
                $(minimizeCardHeaderDOM).css("color", "red");
            } else {
                $(parentCard).attr('minimized', 'true');
                $(parentCard).attr('original-height', $(parentCard).height() + 12);
                $(parentCard).css("height", "30px");
                $(minimizeCardHeaderDOM).removeClass("fa-square-minus");
                $(minimizeCardHeaderDOM).addClass("fa-square-plus");
                $(minimizeCardHeaderDOM).css("color", "green");
            }
        });

        // Add elements to header
        endTab.appendChild(minimizeCardHeaderDOM);
        endTab.appendChild(variableNameCardHeaderDOM);

        cardHeaderDOM.appendChild(endTab);
        cardHeaderDOM.appendChild(lineCardHeaderDOM);

        // Add card component to card
        let previewDOM = createElement("div", inputCardDOM.id + "-preview", "card-body-preview");
        previewDOM.appendChild(inputCardComponentDOM);
        inputCardDOM.appendChild(previewDOM);

        // Hovering
        let hoveredInputCard = qs('.output-card-hover');
        if(hoveredInputCard) {
            hoveredInputCard.classList.remove('output-card-hover');
        }


        return inputCardDOM;
    }

    /* Create Input DOM Elements */
    function createInputText() {
        let input = createElement('input', '', 'form-control');
        input.setAttribute('type', 'text');
        input.setAttribute('placeholder', 'Input');
        input.setAttribute('aria-label', 'Input');

        // Set read only if archive mode
        if (archiveMode) {
            $(input).attr('readonly', true);
        }

        // Set value if archive mode
        if (archiveMode) {
            input.value = inputsDict[inputCounter++];
            $(input).attr('input-value', input.value);
        }
        return input;
    }


    /* Create Component Type Specific Input Cards */
    function createInputTextCard(inputCardTitle, inputCardLineStart, inputCardLineEnd) {
        
        // Adjust line start
        if (newCard) inputCardLineStart = newCardLine;
        
        // Create input text
        let inputElement = createInputText();

        // Check for previous card
        let previousCard = qs('.component-card[line-end=\'' + (inputCardLineStart - 1) + '\'] .card-body-preview');

        // Search for just any previous card if we have same card
        if ((previousCard == null || previousCard == undefined) && sameCard) {
            previousCard = qs('.component-card:last-of-type');
            sameCard = false;
        }

        // Check for previous output
        if (previousCard) {

            // Add input
            previousCard.appendChild(inputElement);

            // Add submit button if not in archive mode
            if (!archiveMode) {
                previousCard.appendChild(createInputSubmitButton());
            }
            $(previousCard.parentElement).attr('line-end', inputCardLineEnd);
            let lineCardHeaderDOM = qs("#" + previousCard.parentElement.id + " .card-header-element-bold");
            if ($(previousCard.parentElement).attr('line-start') != $(previousCard.parentElement).attr('line-end')) {
                $(lineCardHeaderDOM).html($(previousCard.parentElement).attr('line-start') + " - " + $(previousCard.parentElement).attr('line-end'));
            } 

            // Group lines
            let lineStart = parseInt($(previousCard.parentElement).attr('line-start'));
            editor.gotoLine(lineStart);
            selectCard(previousCard.parentElement);


            qs("#outputs-list").scrollTop = $("#outputs-list").height();

             // Restore input values
             let cardInputs = previousCard.querySelectorAll(" input");
             for (let i = 0; i < cardInputs.length - 1; i++) {
                 cardInputs[i].value = $(cardInputs[i]).attr("input-value");
             }
            return null;
        }

        // Create new input card
        let inputCard = createInputCard("Interface Card", inputCardLineStart, inputCardLineEnd, inputElement);
        if (archiveMode) {
            inputCard.querySelector("input").setAttribute('readonly', 'true');
        }
        $(inputCard).attr('line-start', inputCardLineStart);
        $(inputCard).attr('line-end', inputCardLineEnd);   
        editor.gotoLine(inputCardLineStart);
        
        if (!archiveMode) {
            let previewDOM = inputCard.querySelector('.card-body-preview');
            previewDOM.appendChild(createInputSubmitButton());
        }
        qs("#outputs-list").appendChild(inputCard);
        qs("#outputs-list").scrollTop = 10000;

        // Select card
        selectCard(inputCard);

        // Customizations
        if (inputCard) {

            // Store and Apply customizations
            if (newCardColor != '') {
                $(inputCard).css('background-color', newCardColor + " !important");
            }
            if (newCardFontColor != '') {
                $(inputCard).attr('custom-font-color', newCardFontColor);
                let elementTypes = ['span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'thead', 'td'];
                for (let i = 0; i < elementTypes.length; i++) {
                    let elements = qsa('#' + inputCard.id + " " + elementTypes[i]);
                    for (let j = 0; j < elements.length; j++) {
                        $(elements[j]).css('color', newCardFontColor + " !important");
                    }
                }
            }
            newCardFontColor = '';
            newCardColor = '';
            newCard = false;
        }

    }

    /* Create Input Submit Button */
    function createInputSubmitButton() {
        let submitButton = createElement('button', 'submit-btn', 'btn btn-primary');
        submitButton.innerHTML = 'Submit';
        return submitButton;
    }

    // Update input
    function createInput(lineStart, lineEnd, name, comment){

        // Go to line
        editor.gotoLine(parseInt(lineStart));

        // Create card
        createInputTextCard(name, lineStart, lineEnd);

    }

    function hideInput() {
        $("#submit-btn").remove();
    }

    // Outputs
    function createOutputComponentDOM(in_componentType, outputValue, parentElementSelector, startTop=false) {

        // Store component type
        let componentType = in_componentType;

        // Convert type
        if(componentType == "table") {
            outputValue = JSON.parse(outputValue);
        } else if (componentType == "graph") {
            componentType = "image";            
        }

        // Create output element
        let component = createComponentFromType(componentType, componentCounter);        
        let componentState = defaultComponentStates[componentType];

        // Modify component state
        if (componentType == "model") {
            componentState['data'] = outputValue['data'];
        }

        // Set id and load
        componentState['id'] = "#component" + componentCounter++
        component.loadState(componentState);

        
        // Customize CSS
        $(component.getId()).css("position", "static");
        $(component.getId()).css("width", "95%");
        if(componentType == "card") {
            $(component.getId()).css("height", "auto");
            $(component.getId()).css("min-height", "30px");
            $(component.getId()).css("overflow", "hidden");
        } else if (in_componentType == "graph") {
            let aspectRatio = 100 * parseFloat(outputValue['height']) / parseFloat(outputValue['width']);
            if (outputValue['max-width'] != undefined) {
                $(component.getId()).css("max-width", outputValue['max-width']);
            }
            outputValue = outputValue['data'];
            $(component.getId()).css("width", "100%");
            $(component.getId()).css("padding-top", aspectRatio + '%');
            $(component.getId()).css("background-size", '100% 100%');
        } else if (in_componentType == "model") {
            $(component.getId()).css("width", "100%");
        }
        componentY += 10;

        // Move to output section
        let oldOutput = qs(component.getId());
        oldOutput.remove();
        qs(parentElementSelector).appendChild(oldOutput);
        let outputsList = qs(parentElementSelector).parentElement;
        $(outputsList).scrollTop(10000);

        // Update with value
        component.updateValue(outputValue);

        // Make final udpates
        if(componentType == "table") {
            component.removeHeader();
            let numberOfRows = qsa(component.getId() + " tbody tr").length;
            let height = Math.min(40 * numberOfRows + 10, 40);
            $(component.getId() + " table").css("height", height + "px");
            $(component.getId()).css("height", "auto");
            if ($(component.getId()).height() > 160) {
                $(component.getId()).css("height", "160px");
            }
        } else if (componentType == "image") {
            $(component.getId()).css('background-color', 'rgb(254, 254, 254)');
        }

        // Zoom when right click
        if (componentType == "card") {


            $(component.getId()).on('contextmenu', function(e) {

                // Ensure zoom doesnt exist
                if (qs("#zoom") != null) return;

                // Get DOM and aspect
                let componentDOM = qs(component.getId() + " .card-body-preview");
                let componentDOMAspectRatio = $(componentDOM).width() / $(componentDOM).height();

                // Clone DOM
                let copyCard = componentDOM.cloneNode(true);

                // Create Zoom Menu
                let zoomMenu = createElement('div', 'zoom', '');
                $(zoomMenu).css("position", "fixed !important");
                $(zoomMenu).css("width", $(componentDOM).width() + "px");
                $(zoomMenu).css("height", "auto");
                $(zoomMenu).css("z-index", "100000");
                $(zoomMenu).css("padding-bottom", "10px");

                // Create zoom menu title bar
                let zoomMenuTitleBar = createElement('div', '', 'zoom-menu-title-bar');

                // Create x icon
                let xIcon = createElement('i', '', 'fas fa-times zoom-menu-x-icon');
                $(xIcon).click(()=>{
                    $(zoomMenu).remove();
                });

                // Create title 
                let zoomMenuTitleBarText = createElement('span', '', 'zoom-menu-title-bar-text');
                zoomMenuTitleBarText.innerHTML = "Preview Window";

                // Add elements to title bar
                zoomMenuTitleBar.appendChild(xIcon);
                zoomMenuTitleBar.appendChild(zoomMenuTitleBarText);

                // Add title bar to zoom menu
                $(zoomMenu).append(zoomMenuTitleBar);

                // Update clone
                $(copyCard).attr('id', 'zoom-card');
                $(copyCard).css('margin', 'auto');

                // Make draggable
                $(zoomMenu).draggable(
                    {
                        "handle": ".zoom-menu-title-bar",
                    }
                );

                // Add DOM to Zoom
                zoomMenu.appendChild(copyCard);
                qs("body").appendChild(zoomMenu);
                $(zoomMenu).css("top", ($(document).height() / 2 - $(zoomMenu).height() / 2) + "px");
                $(zoomMenu).css("left", ($(document).width() / 2 - $(zoomMenu).width() / 2) + "px");

                // Custom
                if ($(copyCard).attr('type') == 'table') {
                    $('#zoom-card .component-table').css("margin-top", "10px");
                    $('#zoom-card .component-table').css("height", "calc(100% - 10px)");
                }              
            });
        }
    
        return qs(component.getId());
    }

    function setupOutputComponentDOMCard(component) {
        $("#" + component.id).css("margin-top", "10px");
        $("#" + component.id).css("padding", "10px");
        $("#" + component.id).css("display", "flex");
        $("#" + component.id).css("flex-direction", "column");
    }

    function setupOutputComponentDOMHeading(component, name) {
        let heading  = qs("#" + component.id + " h1");
        heading.innerHTML = name;
    }

    function createOutputComponent(outputLineStart, outputLineEnd, outputName, outputValue, outputComment, outputComponentType) {

        // Reset pos
        if(componentX == -1 && componentY == -1) {
            componentX = $("#outputs h3").offset().left;
            componentY = $("#outputs h3").offset().top + 30;
        }

        // Destroy old card if it exists
        if (qs("div[name='" + outputName + "']")) {
            qs("div[name='" + outputName + "']").remove();
        }
        
        // Set line
        editor.gotoLine(outputLineEnd);

        // Create card or merge
        let outputCard;
        let previewDOM;

        // Check card belonging to previous line
        let previousElement = qs(".component-card[line-end='" + (outputLineStart - 1) + "']");

        // Search for just any previous card if we have same card
        if ((previousElement == null || previousElement == undefined) && sameCard) {
            previousElement = qs('.component-card:last-of-type');
            sameCard = false;
        }

        // Create card
        if (previousElement != null) {
            outputCard = previousElement;
            previewDOM = qs("#" + outputCard.id + " .card-body-preview");
            $(outputCard).attr('line-end', outputLineEnd);
            let lineCardHeaderDOM = qs("#" + outputCard.id + " .card-header-element-bold");
            if ($(outputCard).attr('line-start') != $(outputCard).attr('line-end')) {
                $(lineCardHeaderDOM).html($(outputCard).attr('line-start') + " - " + $(outputCard).attr('line-end'));
            } 
        } else {

            // Create new card
            outputCard = createOutputComponentDOM("card", "", "#outputs-list", true);
            if (newCard) outputLineStart = newCardLine;
            $(outputCard).attr('line-start', outputLineStart);
            $(outputCard).attr('line-end', outputLineEnd);
            $(outputCard).attr('name', outputName);
            $(outputCard).attr('type', outputComponentType);

             // Link card to line
            setupOutputComponentDOMCard(outputCard);
            $(outputCard).click(()=>{
                let lineStart =  parseInt($(outputCard).attr('line-start'));
                editor.gotoLine(lineStart);
                selectCard(outputCard);
            });
            $(outputCard).mouseenter(()=>{
                $(outputCard).addClass("output-card-hover");
            });
            $(outputCard).mouseleave(()=>{
                $(outputCard).removeClass("output-card-hover");
            });

            // Get line
            let lineEditorDOM = qsa(".ace_line")[outputLineStart - 1];
            $(lineEditorDOM).css("pointer-events", "default");
            $(lineEditorDOM).click((e)=> {
                e.preventDefault();
            });

           // Create card header
           let cardHeaderDOM = createElement("div", outputCard.id + "-card-header", "card-header-bar");
           qs("#" + outputCard.id).appendChild(cardHeaderDOM);

           // Create end tab
           let endTab = createElement("div", "", "card-header-end-tab");
           cardHeaderDOM.appendChild(endTab);

           // Create card header contents             
           let variableNameCardHeaderDOM = createElement("span", "", "card-header-element");
           let cardName = "Interface Card";
           if (newCard) {
                cardName = newCardName;
                newCardName = '';
           }
           $(variableNameCardHeaderDOM).html(cardName);

           // Setup minimize button
           let minimizeCardHeaderDOM = createElement("i", "", "fa-light fa-square-minus toggle-btn");
           $(minimizeCardHeaderDOM).click(()=>{
               let selectCardLineStart = parseInt($(outputCard).attr('line-start'));
               let selectCardLineEnd = parseInt($(outputCard).attr('line-end'));
               editor.session.foldAll(selectCardLineStart, selectCardLineEnd);

               let parentCard = minimizeCardHeaderDOM.parentElement.parentElement.parentElement;
                if ($(parentCard).attr("minimized") == "true") {
                   let originalHeight = $(parentCard).attr('original-height');
                   $(parentCard).css("height", originalHeight + 'px');
                   $(parentCard).attr("minimized", "false");
                   $(minimizeCardHeaderDOM).removeClass("fa-square-plus");
                   $(minimizeCardHeaderDOM).addClass("fa-square-minus");
                   $(minimizeCardHeaderDOM).css("color", "red");
                } else {
                   $(parentCard).attr('minimized', 'true');
                   $(parentCard).attr('original-height', $(parentCard).height() + 12);
                   $(parentCard).css("height", "30px");
                   $(minimizeCardHeaderDOM).removeClass("fa-square-minus");
                   $(minimizeCardHeaderDOM).addClass("fa-square-plus");
                   $(minimizeCardHeaderDOM).css("color", "green");
                }
            });

            // Setup minimize double click
            $("#" + outputCard.id).dblclick(()=>{
                let parentCard = minimizeCardHeaderDOM.parentElement.parentElement.parentElement;
                if ($(parentCard).attr("minimized") == "true") {
                   let originalHeight = $(parentCard).attr('original-height');
                   $(parentCard).css("height", originalHeight + 'px');
                   $(parentCard).attr("minimized", "false");
                   $(minimizeCardHeaderDOM).removeClass("fa-square-plus");
                   $(minimizeCardHeaderDOM).addClass("fa-square-minus");
                   $(minimizeCardHeaderDOM).css("color", "red");
                } else {
                   $(parentCard).attr('minimized', 'true');
                   $(parentCard).attr('original-height', $(parentCard).height() + 12);
                   $(parentCard).css("height", "30px");
                   $(minimizeCardHeaderDOM).removeClass("fa-square-minus");
                   $(minimizeCardHeaderDOM).addClass("fa-square-plus");
                   $(minimizeCardHeaderDOM).css("color", "green");
                }
            });

           // Add elements to header
           endTab.appendChild(minimizeCardHeaderDOM);
           endTab.appendChild(variableNameCardHeaderDOM);
           
           // Create line number
           let lineCardHeaderDOM = createElement("span", "", "card-header-element-bold");
           if (componentCounter > 1) {
                if (outputLineStart != outputLineEnd) {
                        $(lineCardHeaderDOM).html(outputLineStart + " - " + outputLineEnd);
                } else {
                        $(lineCardHeaderDOM).html(outputLineStart);
                }
            }
           cardHeaderDOM.appendChild(lineCardHeaderDOM);

            // Create card body
           previewDOM = createElement("div", outputCard.id + "-preview", "card-body-preview");
           $(outputCard).append(previewDOM);
        }

        // Select card
        selectCard(outputCard);

        // Mark lines
        let lineStart = parseInt($(outputCard).attr('line-start'));
        editor.gotoLine(lineStart);
        
        // Create card body
        if (outputComponentType == "markdown") {

            // Set name
            $(outputCard).attr('name', outputComponentType + "-" + outputLineStart);

            // Create temp wrapper
            let tempWrapper = createElement('div', '', '');
            tempWrapper.innerHTML += converter.makeHtml(outputValue);
            
            // Transfer from temp wrapper to preview DOM
            for (let i = 0; i < tempWrapper.children.length; i++) {
                let childCopy = tempWrapper.children[i].cloneNode(true);
                previewDOM.appendChild(childCopy);
            }

            // Highlight code elements
            let codeElements = qsa("#" + outputCard.id + "-preview code");
            for (let i = 0; i < codeElements.length; i++) {
                if (!$(codeElements[i]).attr("highlighted")) {
                    let codeContent = codeElements[i].innerHTML;
                    codeElements[i].innerHTML = hljs.highlight(codeContent, {language: 'python'}).value;
                    codeElements[i].innerHTML = codeElements[i].innerHTML.replaceAll('&amp;amp;lt;', '&lt;').replaceAll('&amp;amp;gt;', '&gt;');
                    codeElements[i].innerHTML = codeElements[i].innerHTML.replaceAll('&amp;lt;', '&lt;').replaceAll('&amp;gt;', '&gt;');
                    $(codeElements[i]).attr("highlighted", "true");
                    if (codeElements[i].parentElement.tagName == "PRE") {
                        codeElements[i].parentElement.className = "hljs language-python";
                    }
                }
            }

            
            // Make tables bootstrap
            let tables = qsa("#" + outputCard.id + "-preview table");
            for (let i = 0; i < tables.length; i++) {

                // Place table in wrapper
                let tableWrapper = createElement("div", "", "table-wrapper");
                tables[i].parentElement.insertBefore(tableWrapper, tables[i]);
                tableWrapper.appendChild(tables[i]);

                // Make table boostrap
                tables[i].className = "table table-light table-striped table-bordered";                
            }

            // Make thead bootstrap
            let theads = qsa("#" + outputCard.id + "-preview thead");
            for (let i = 0; i < theads.length; i++) {
                theads[i].className = "thead-light";
            }

            // Separate latex equations
            let paragraphs = qsa("#" + outputCard.id + "-preview p");
            for (let i = 0; i < paragraphs.length; i++) {

                // Skip if no latex
                if (paragraphs[i].innerHTML.indexOf("$$") == -1) {
                    continue;
                }

                // Split into chunks
                let paragraph = paragraphs[i];
                let chunks = paragraph.innerHTML.split("$$");

                // Put into cleaned bucket
                let cleanedBucket = []

                // Split into buckets
                for (let j = 0; j < chunks.length; j++) {
                    if (j % 2 == 0) {
                        cleanedBucket.push(chunks[j]);
                    } else {
                        cleanedBucket.push("<div style=\"display: inline-block;\">" + '$$' + chunks[j] + '$$' + "</div>");
                    }
                }

                // new mega-paragraph
                let mainParapraph = createElement("p", "", "");

                // Create paragraphs for each bucket and insert after original paragraph
                for (let j = 0; j < cleanedBucket.length; j++) {
                    if (cleanedBucket[j].length > 0) {
                        mainParapraph.innerHTML += cleanedBucket[j];                        
                    }
                }

                // Replace paragraph with new mega-paragraph
                paragraph.parentElement.replaceChild(mainParapraph, paragraph);

                // Update
                paragraphs = qsa("#" + outputCard.id + "-preview .latex-equation p");
                

                // Remove text indent
                let latexEquations = qsa("#" + outputCard.id + "-preview .latex-equation");
                for (let j = 0; j < latexEquations.length; j++) {
                    let latexParagraphs = latexEquations[j].shadowRoot.querySelectorAll("p");
                    for (let k = 0; k < latexParagraphs.length; k++) {
                        $(latexParagraphs[k]).css("text-indent", "0px");
                    }
                }

            }
            
            // Typeset
            MathJax.typeset();

            // Scan for local links
            let links = qsa("#" + outputCard.id + "-preview a");
            for (let i = 0; i < links.length; i++) {
                let link = links[i];
                if (link.href.indexOf("www.") == -1 && link.href.indexOf("http") == -1) {
                    $(link).click((e)=>{
                        let openFileMessage = {};
                        openFileMessage["type"] = "open-file";
                        let outerHTML = link.outerHTML;
                        outerHTML = outerHTML.substring(9);
                        outerHTML = outerHTML.substring(0, outerHTML.indexOf("\">"));
                        if (outerHTML.indexOf("\" rel=") != -1) {
                            outerHTML = outerHTML.substring(0, outerHTML.indexOf("\" rel="));
                        }
                        
                        openFileMessage["content"] = outerHTML;
                        sendSocket(JSON.stringify(openFileMessage));
                        e.preventDefault();
                    });
                }
            }

            // Link linked code to editor
            let code_lines = qsa("#" + outputCard.id + "-preview .hljs-comment");
            for (let i = 0; i < code_lines.length; i++) {
                if (code_lines[i].innerHTML.indexOf("[linked code:") != -1) {
                    let lines_range = code_lines[i].innerHTML.split(":")[1].trim();
                    lines_range = lines_range.substring(6);
                    lines_range = lines_range.substring(0, lines_range.length - 1).trim();
                    let line_range_start = parseInt(lines_range.split("-")[0]);
                    let line_range_end = parseInt(lines_range.split("-")[1]);
                    $(code_lines[i].parentElement.parentElement).click((e)=>{

                        // Go to line
                        editor.gotoLine(line_range_start);
                        groupLines(line_range_start, line_range_end);
                        e.stopPropagation();
                    });
                }
            }

            // Auto-adjust height
            $("#" + outputCard.id + " .component-element-header").css("height", "auto");
            $("#" + outputCard.id + " .component-element-header").css("user-select", "none");
            $("#" + outputCard.id + " .component-header").css("height", "auto");
            $("#" + outputCard.id + " .component-element").css("user-select", "none");
            $("#" + outputCard.id).css("height", "auto");
        } else {
            let valueDOM = createOutputComponentDOM(outputComponentType, outputValue, "#" + outputCard.id + "-preview");
            if (outputComponentType == "heading") {
                $("#" + outputCard.id + " h1").css("user-select", "none");
            }
        }
        componentY += 30;

        // Restore input values
        let cardInputs = qsa("#" + outputCard.id + " input");
        for (let i = 0; i < cardInputs.length; i++) {
            cardInputs[i].value = $(cardInputs[i]).attr("input-value");
        }

        // Apply customizations
        if ($(outputCard).attr('custom-font-color') != undefined) {
            let fontColor = $(outputCard).attr('custom-font-color');
            let elementTypes = ['span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'thead', 'td'];
            for (let i = 0; i < elementTypes.length; i++) {
                let elements = qsa('#' + outputCard.id + " " + elementTypes[i]);
                for (let j = 0; j < elements.length; j++) {
                    $(elements[j]).css('color', fontColor + " !important");
                }
            }
        }

        // Customizations
        if (newCard) {

            // Store and Apply customizations
            if (newCardColor != '') {
                $(outputCard).css('background-color', newCardColor + " !important");
            }
            if (newCardFontColor != '') {
                $(outputCard).attr('custom-font-color', newCardFontColor);
                let elementTypes = ['span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'thead', 'td'];
                for (let i = 0; i < elementTypes.length; i++) {
                    let elements = qsa('#' + outputCard.id + " " + elementTypes[i]);
                    for (let j = 0; j < elements.length; j++) {
                        $(elements[j]).css('color', newCardFontColor + " !important");
                    }
                }
            }
            newCardFontColor = '';
            newCardColor = '';
            newCard = false;
        }

        // Update scroll
        let outputsList = qs("#outputs-list");
        $(outputsList).scrollTop(10000);
    }

    function createSubmitCallback() {
        $("#submit-btn").mousedown(function() {

            // Pipe contents home
            let input = $(this.previousSibling).val();
            let reply = {};
            reply["type"] = "submit";
            reply["content"] = input;
            sendSocket(JSON.stringify(reply));

            // Unselect
            $(this.previousSibling).prop("disabled", true);
            $(this.previousSibling).attr('input-value', input);

            // Unbind submit
            $("#submit-btn").unbind("click");
        });
    }

    // Process socket message
    function processSocketMessage(event) {

        // Parse message
        let message;
        if (!archiveMode) {
            message = JSON.parse(event.data);
        } else {
            message = event;
        }

        if(message.type == "heartbeat") return;
        if (message.type != 'ping' && message.type != 'heartbeat') {

            if (!archiveMode) {
                archive.push(message);
            }

            if (message.type == "create" && message.element == 'input') {
                let lineStart = message.line_start;
                let lineEnd = message.line_end;
                let name = message.name;
                let comment = message.comment;
                createInput(lineStart, lineEnd, name, comment);
                createSubmitCallback();
            } else if (message.type == "quit") {
                window.close();
            } else if (message.type == "hide" && message.element == "input") {
                hideInput();
            } else if (message.type == "wait-for-next" || message.type == "wait-for-submit") {
                if (message['line-number'] != "-1") {
                    editor.gotoLine(message['line-number']);
                }
                if (!archiveMode) {
                    archive.push(message);
                }
            } else if (message.type == "create" && message.element == "output") {

                // Handle card
                if (message.componentType == "card") {
                    let newCardDict = listOfListsToDict(message.value)
                    newCard = true;
                    newCardLine = message.line_start;
                    if (newCardDict['title'] != undefined) {
                        newCardName = newCardDict['title'];
                    }
                    if (newCardDict['bg-color'] != undefined) {
                        newCardColor = newCardDict['bg-color'];
                    }
                    if (newCardDict['text-color'] != undefined) {
                        newCardFontColor =  newCardDict['text-color'];
                    }
                    return;
                }
                if (message.componentType == 'samecard') {
                    sameCard = true;
                    return;
                }

                // Switch to MD
                if (message.componentType == "markdown" && message['value']['data'] != undefined) {
                    message['value'] = message['value']['data'];
                    message['name'] = '';
                }

                // Create output
                let outputLineStart = parseInt(message.line_start);
                let outputLineEnd = parseInt(message.line_end);
                let outputValue = message.value;
                let outputName = message.name;
                let outputComment = message.comment;
                let outputComponentType = message.componentType;
                createOutputComponent(outputLineStart, outputLineEnd, outputName, outputValue, outputComment, outputComponentType);
                let outputsList = qs("#outputs-list");
                $(outputsList).scrollTop(100000);
            } else if (message.type == "callback" && message.name == "submit-btn") {
                
            } else if (message.type == "init") {
                restarting = false;
                editor.setValue(message.state.replaceAll("&lt;", "<").replaceAll("&gt;", ">").replaceAll("$$", ""));                
                editor.gotoLine(1);
                setTimeout(() => {
                    editor.session.foldAll();
                    let startRow = -1;
                    for (let i = 0; i < editor.session.getLength(); i++) {
                        let line = editor.session.getLine(i);
                        if (line.includes("'''") || line.includes("\"\"\"")) {
                            if (startRow == -1) {
                                startRow = i;                    
                            } else {
                                editor.session.foldAll(startRow, i);
                                startRow = -1;
                            }
                        } 
                    }
                    /*
                    editor.session.setAnnotations([{
                        row: 3,
                        column: 0,
                        text: "Error Message", // Or the Json reply from the parser 
                        type: "error" // also "warning" and "information"
                    }]);
                    */
                }, 10);
            }
        }
    }

    // Send via socket
    function sendSocket(outMessage){

        // Send socket
        if (!archiveMode) {
            try {       
                if(exit && (ws.readyState == ws.CLOSED || ws.readyState == ws.CLOSING)) {
                    window.close();
                }   
                if (outMessage.indexOf('ping') == -1) {
                    archive.push(JSON.parse(outMessage));
                }
                ws.send(outMessage);
            } catch (error) {
                console.log("[Error sending message to server]", error)
            }
        }
    }

    // Update cards
    function updateCards(){

        // Get tags from tag bar
        let tagsDOM = qs("#tag-bar tags");
        let tags = [];
        for (let i = 0; i < tagsDOM.children.length; i++) {
            let tagTitle = $(tagsDOM.children[i]).attr('title');
            if (tagTitle != undefined) {
                tags.push(tagTitle.toLowerCase());
            }
        }
        
        // Filter if all is not a tag
        if (tags.includes("all")) {
            return;
        }
    }

    // Setup tab list
    function setupTabs() {
        var input = document.querySelector('input[name=tags]');
        $(input).change(()=> {
            updateCards();
        });
        new Tagify(input)
    }

    // Create editor
    function createEditor() {
        // Create editor
        editor = ace.edit("editor");


        editor.setOptions({
            autoScrollEditorIntoView: true,
            copyWithEmptySelection: true,
        });
        editor.setTheme("ace/theme/twilight");
        editor.session.setFoldStyle("markbeginend");
        editor.session.setMode("ace/mode/python");
        editor.setReadOnly(true);  // false to make it editable
        let code = "";
        editor.setValue(code);
        editor.gotoLine(1);
        document.getElementById('editor').style.fontSize='12px';
        editor.resize();
        editor.setOptions({
            fontSize: "12pt",
            useWorker: false
        });

        editor.on('changeSelection',  (e) => {
            let selectionStart = editor.selection.cursor.row;
            let cards = qsa('.component-card');
            for (let i = 0; i < cards.length; i++) {
                let card = cards[i];
                let cardStart = parseInt(card.getAttribute('line-start'));
                let cardEnd = parseInt(card.getAttribute('line-end'));
                if (cardStart == cardEnd) {
                    if (cardStart == (selectionStart + 1)) {
                        selectCard(card);
                        return;
                    }
                } else {
                    if (cardStart <= selectionStart + 1 && selectionStart < cardEnd) {
                        card.parentElement.scrollTop = card.offsetTop -  140;
                        selectCard(card);
                        return;
                    }
                }            
            }
            unselectCard();
        });
    }

    // Remove zoom if exists
    function removeZoomIfExists(evt) {
        let zoom = qs("#zoom");
        if (zoom != null) {
            let zoomExtents = getElementBounds("#zoom");
            let cursorPos = {"x" : evt.clientX, "y" : evt.clientY};
            if (!testIntersection(cursorPos, zoomExtents)) {
                qs("#zoom").remove();
            }
        }
    }

    // Setup drag
    function setupDrag() {
        let drag =  false;
        let border = $("#display-canvas").width();
        $("#drag").css('left', $("#right-pane").offset().left);
        $("#drag").mousedown(function(e) {
            drag = true;
            $("#drag").css('left', e.pageX);
        });
        $(document).mouseup(function(e) {
            drag = false;
        });
        $(document).mousemove((e)=>{
            if (drag) {
                $("#display-canvas").css('width', e.pageX - $("#display-canvas").offset().left);
                $("#drag").css('left', e.pageX);
                e.stopPropagation();
                e.preventDefault();
            }
        });
    }

    // Play archive
    function playArchive(fastForward=false) {
        if (!fastForward) {
            while(archiveIndex < archive.length && archive[archiveIndex].type != "wait-for-next" && archive[archiveIndex].type != "wait-for-input") {
                processSocketMessage(archive[archiveIndex]);
                archiveIndex++;
            }
        } else {
            while(archiveIndex < archive.length) {
                processSocketMessage(archive[archiveIndex]);
                archiveIndex++;
            }
        }
    }


    // Main Entry Point
    $(function() {

        // Extract input dict
        if (archiveMode) {
            inputsDict = archive[archive.length - 1];
            archive.splice(-1);
        }

        // Create editor
        createEditor();

        // Setup drag
        setupDrag();

        // Setup tabs
        setupTabs();

        // Zoom responder
        $(document).dblclick((evt)=>{
            removeZoomIfExists(evt);
        });

        // Initialize component spot
        componentX = -1;
        componentY = -1;

        // Initialize next button
        $("#next-btn").click(function() {

            if (!archiveMode) {
                let reply = {};
                reply["type"] = "next";
                sendSocket(JSON.stringify(reply));
            } else {
                archiveIndex++;
                playArchive();
            }
        });

        $("#fast-forward-btn").click(function() {
            if (archiveMode) {
                playArchive(true);
            } else {
                let reply = {};
                reply["type"] = "fast-forward";
                sendSocket(JSON.stringify(reply));
            }
        });
        
        $("#reload-btn").click(function() {
            if (archiveMode) {
                $("#outputs-list").empty();
                archiveIndex = 0;
                componentCounter = 0;
                inputCounter = 0;
                playArchive();
            } else {
                let reply = {};
                reply["type"] = "reload";
                restarting = true;
                sendSocket(JSON.stringify(reply));
            }
        });

        $("#archive-btn").click(function() {
            let reply = {};
            let inputs = qsa(".component-card input");
            let inputsDict = {};
            for (let i = 0; i < inputs.length; i++) {                
                inputsDict[i] = inputs[i].value;
            }
            archive.push(inputsDict);
            reply["type"] = "archive";
            reply["archive"] = archive;
            sendSocket(JSON.stringify(reply))
        });

        $("#exit-btn").click(function() {
            if (archiveMode) window.close();
            exit = true
            let reply = {};
            reply["type"] = "exit";
            sendSocket(JSON.stringify(reply));
        });

        // Remove archive in archive mode
        if(archiveMode) {
            $("#archive-btn").remove();
        }

        // Create MD converter
        converter = new showdown.Converter(
            {
                literalMidWordUnderscores : false,
                literalMidWordAsterisks : true,
                tables : true,
                strikethrough: true,
                emoji : true,
                underline: true,
                simpleLineBreaks: true,
                openLinksInNewWindow : true,
                tasklists : true,
                smartIndentationFix : true,
                simpleLineBreaks : true
            }
        );


        // Setup socket
        console.log("Version 1.14");
        if (!archiveMode) {
            createSocket();
            setInterval(()=>{
                let pingMessage = {'type': 'ping', 'data' : 'ping'};
                sendSocket(JSON.stringify(pingMessage));
            }, 20);
        }

        // Play mode
        if (archiveMode) {
            playArchive();
        }
    });

  })(jQuery);
  