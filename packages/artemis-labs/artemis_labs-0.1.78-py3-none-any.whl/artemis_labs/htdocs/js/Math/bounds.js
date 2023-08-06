'use strict';

function testIntersection(point, box) {
    if(point.x < box.left || point.x > box.right || point.y < box.top || point.y > box.bottom) {
        return false;
    }
    return true;
}

function testBoxIntersection(boxA, boxB) {
    if(boxA.left > boxB.right || boxA.right < boxB.left || boxA.top > boxB.bottom || boxA.bottom < boxB.top) {
        return false;
    }
    return true;
}

function getElementBounds(elementSelector) {
    return {
        "left" : parseInt($(elementSelector).css("left")),
        "top" : parseInt($(elementSelector).css("top")),
        "right" : parseInt($(elementSelector).css("left")) + parseInt($(elementSelector).css("width")),
        "bottom" : parseInt($(elementSelector).css("top")) + parseInt($(elementSelector).css("height"))
    };
}
