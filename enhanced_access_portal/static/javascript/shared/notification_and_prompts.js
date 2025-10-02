
// Setting up variables for later use

const notification_window = document.getElementById("notification_window");
const prompt_window = document.getElementById("prompt_window");
const confirmation_prompt_window = document.getElementById("confirmation_prompt_window");

const confirmation_prompt_button = document.getElementById("confirmation_prompt_button");


// Sub-functions

/*
* Reveals a notification or prompt window
* @param reveal_type {string a "notification" or "prompt" window you want revealed. Hides the other}
*/
function reveal_notification_or_prompt(reveal_type){

    if (reveal_type == "notification"){
        notification_window.style.display = "flex";
        prompt_window.style.display = "none";
        confirmation_prompt_window.style.display = "none";
    }else if (reveal_type == "prompt"){
        notification_window.style.display = "none";
        prompt_window.style.display = "flex";
        confirmation_prompt_window.style.display = "none";
    }else if (reveal_type == "confirmation_prompt"){
        notification_window.style.display = "none";
        prompt_window.style.display = "none";
        confirmation_prompt_window.style.display = "flex";
    }else if (reveal_type == "none"){
        notification_window.style.display = "none";
        prompt_window.style.display = "none";
        confirmation_prompt_window.style.display = "none";
    }else{
        error("Wrong input");
    }
}
//reveal_notification_or_prompt("none");


/**
 * Reveals a notification to the user
 * @param notification_message {string The message to reveal}
 * @param loading_icon {bool Whether to show the loading icon}
 */
function notify_user(notification_message, loading_icon){

    reveal_notification_or_prompt("notification");

    const notification_message_p = document.getElementById("notification_message");
    notification_message_p.innerHTML = notification_message;

    const notification_loading_icon = document.getElementById("notification_loading_icon");

    if (loading_icon){
        if (loading_icon == true){
            notification_loading_icon.style.display = "block";
        }else{
            notification_loading_icon.style.display = "none";
        }
    }else{
        notification_loading_icon.style.display = "none";
    }

}


/**
 * Reveals a prompt to the user
 * @param prompt_header {string The header message}
 * @param prompt_message {string The prompt message}
 */
function prompt_user(prompt_header, prompt_message){

    reveal_notification_or_prompt("prompt");

    const prompt_header_p = document.getElementById("prompt_header");
    prompt_header_p.innerHTML = prompt_header;

    const prompt_message_p = document.getElementById("prompt_message");
    prompt_message_p.innerHTML = prompt_message;

}


/**
 * Processes the result of a confirmation prompt made to a user
 * @param function_to_call {string The name of the function to call}
 * @param function_args {list A list of arguments to pass to the function call}
 */
function continue_confirmation_prompt(function_to_call, function_args){
    reveal_notification_or_prompt("none");
    if (function_to_call == "ADMIN_PROMPT_delete_project"){
        ADMIN_PROMPT_delete_project(function_args);
    }
    if (function_to_call == "ADMIN_PROMPT_rename_project"){
        ADMIN_PROMPT_rename_project();
    }
    if (function_to_call == "ADMIN_USER_PROMPT_remove_vm_from_group"){
        ADMIN_USER_PROMPT_remove_vm_from_group(function_args);
    }
    if (function_to_call == "ADMIN_USER_PROMPT_delete_group"){
        ADMIN_USER_PROMPT_delete_group(function_args);
    }
    if (function_to_call == "ADMIN_USER_PROMPT_remove_vm"){
        ADMIN_USER_PROMPT_remove_vm(function_args);
    }
    if (function_to_call == "ADMIN_PROMPT_remove_member_from_project"){
        ADMIN_PROMPT_remove_member_from_project(function_args);
    }
}

/**
 * Reveals a confirmation prompt to the user
 * @param prompt_header {string The header message}
 * @param prompt_message {string The prompt message}
 * @param function_to_call {string The name of the function to call}
 * @param function_args {list A list of arguments to pass to the function call}
 */
function confirmation_prompt_user(prompt_header, prompt_message, function_to_call, function_args){

    reveal_notification_or_prompt("confirmation_prompt");

    const confirmation_prompt_header_p = document.getElementById("confirmation_prompt_header");
    confirmation_prompt_header.innerHTML = prompt_header;

    const confirmation_prompt_message_p = document.getElementById("confirmation_prompt_message");
    confirmation_prompt_message.innerHTML = prompt_message;

    confirmation_prompt_button.onclick = () => continue_confirmation_prompt(function_to_call, function_args);
    
}


/**
 * Hides a prompt pop up
 */
function prompt_continue_button(){
    reveal_notification_or_prompt("none");
}