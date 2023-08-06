'use strict';

// Frontend URL's
const DEV_FRONTEND_URL = 'www.artemisardesignerdev.com';
const LIVE_FRONTEND_URL  = 'www.artemisardesigner.com';

// Server URL's
const DEV_SERVER_URL = "https://artemisarbackenddev.com:8080";
const LIVE_SERVER_URL = "https://artemisarbackend.com:8080";

// Server endpoints
const EP_APP_GET = "/get_app?";
const EP_APP_UPDATE = "/update_app?";
const EP_CREATE_ACCOUNT =  "/create_account?";
const EP_LOGIN_ACCOUNT = "/login?";
const EP_ACTIVATE_ACCOUNT = "/activate_account?";
const EP_VALIDATE_ACCOUNT = "/validate_account?";
const EP_LOGOUT_ACCOUNT = "/logout_account?";

// Setup server URL
function getServerURL() {
    if (window.location.href.indexOf(DEV_FRONTEND_URL) != -1) {
        return DEV_SERVER_URL;
    } else {
        return LIVE_SERVER_URL;
    }
}

// Helper to update app
function updateApps(in_username, in_token, in_JSONUpdate) {
    
    // Get server URL
    const SERVER_URL = getServerURL();

    // Stringify update
    let contentText = JSON.stringify(in_JSONUpdate);

    // Store app cache
    let URL = SERVER_URL + EP_APP_UPDATE;

    // Create body
    let body = {
        "username": in_username,
        "token": in_token,
        "content": contentText
    };
    
    // Create XMLHttp Request
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            console.log(xmlHttp.responseText);
    }
    xmlHttp.open("POST", URL, true); // true for asynchronous 
    xmlHttp.setRequestHeader("Content-Type", "application/json");

    // Send request
    xmlHttp.send(JSON.stringify(body));
}

// Helper to load app
function getApps(in_username, in_token, in_callback) {
    
    // Get server URL
    const SERVER_URL = getServerURL();

    // Menu URL
    let URL = SERVER_URL + EP_APP_GET + "username=" + in_username + "&token=" + in_token;

    // Fetch menu info
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            
            // Parse response
            let response = JSON.parse(xmlHttp.responseText);

            // Call callback
            in_callback(response);               
        }
    };
    
    // Send request
    xmlHttp.open("GET", URL, true); 
    xmlHttp.send(null);
}

// Helper to create account
function createAccount(in_username, in_password, in_callback) {
    
    // Get server URL
    const SERVER_URL = getServerURL();

    // Menu URL
    let URL = SERVER_URL + EP_CREATE_ACCOUNT + "username=" + in_username + "&" + "password=" + in_password;

    // Fetch menu info
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            
            // Parse response
            let response = JSON.parse(xmlHttp.responseText);

            // Call callback
            in_callback(response);               
        }
    };
    
    // Send request
    xmlHttp.open("GET", URL, true); 
    xmlHttp.send(null);
}

// Helper to login to account
function loginAccount(in_username, in_password, in_callback) {
    
    // Get server URL
    const SERVER_URL = getServerURL();

    // Menu URL
    let URL = SERVER_URL + EP_LOGIN_ACCOUNT + "username=" + in_username + "&" + "password=" + in_password;
    console.log(URL);

    // Fetch menu info
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            
            // Parse response
            let response = JSON.parse(xmlHttp.responseText);

            // Call callback
            in_callback(response);               
        }
    };
    
    // Send request
    xmlHttp.open("GET", URL, true); 
    xmlHttp.send(null);
}

// Helper to login to account
function registerAccount(in_username, in_token, in_apiKey, in_callback) {
    
    // Get server URL
    const SERVER_URL = getServerURL();

    // Menu URL
    let URL = SERVER_URL + EP_ACTIVATE_ACCOUNT + "username=" + in_username + "&" + "token=" + in_token + "&productKey=" + in_apiKey;
    console.log(URL);

    // Fetch menu info
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            
            // Parse response
            let response = JSON.parse(xmlHttp.responseText);

            // Call callback
            in_callback(response);               
        }
    };
    
    // Send request
    xmlHttp.open("GET", URL, true); 
    xmlHttp.send(null);
}

// Helper to login to account
function validateAccount(in_username, in_token, in_callback) {

    // Get server URL
    const SERVER_URL = getServerURL();

    // Menu URL
    let URL = SERVER_URL + EP_VALIDATE_ACCOUNT + "username=" + in_username + "&" + "token=" + in_token;

    // Fetch menu info
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            
            // Parse response
            let response = JSON.parse(xmlHttp.responseText);

            // Call callback
            in_callback(response);               
        }
    };
    
    // Send request
    xmlHttp.open("GET", URL, true); 
    xmlHttp.send(null);
}

// Helper to logout from account
function logoutAccount(in_username, in_token, in_callback) {
    
    // Get server URL
    const SERVER_URL = getServerURL();

    // Menu URL
    let URL = SERVER_URL + EP_LOGOUT_ACCOUNT + "username=" + in_username + "&" + "token=" + in_token;

    // Fetch menu info
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            
            // Parse response
            let response = JSON.parse(xmlHttp.responseText);

            // Call callback
            in_callback(response);               
        }
    };
    
    // Send request
    xmlHttp.open("GET", URL, true); 
    xmlHttp.send(null);
}

// Export
export {logoutAccount, registerAccount, updateApps, getApps, createAccount, loginAccount, validateAccount};