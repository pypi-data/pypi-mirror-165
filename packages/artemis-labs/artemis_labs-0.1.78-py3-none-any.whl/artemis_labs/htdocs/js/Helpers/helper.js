'use strict';

function qsa(selector) {
    let elements = document.querySelectorAll(selector);
    return elements;
}

function qs(selector) {
    let element = document.querySelector(selector);
    return element;
}

function createElement(selector, id="", cls="") {
    let element = document.createElement(selector);
    element.id = id;
    element.className = cls;
    return element;
}

function download(content, fileName) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', fileName);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}