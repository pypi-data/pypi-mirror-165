'use strict';

// Helper to update app
function getURLArg(index) {
    let urlDecoded = decodeURI(window.location.search);
    let urlArg = urlDecoded.substring(1);
    let urlArgs = urlArg.split("&");
    return urlArgs[index].substring(urlArgs[index].indexOf("=") + 1).trim();
}
    
// Export
export {getURLArg};