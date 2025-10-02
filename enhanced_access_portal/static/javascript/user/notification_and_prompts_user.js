
// Setting up variables for later use




// Sub-functions

/**
 * Processes the result of a confirmation prompt made to a user
 * @param function_to_call {string The name of the function to call}
 * @param function_args {list A list of arguments to pass to the function call}
 */
function continue_confirmation_prompt(function_to_call, function_args){
    reveal_notification_or_prompt("none");
    if (function_to_call == "ADMIN_USER_PROMPT_rename_project"){
        ADMIN_USER_PROMPT_rename_project();
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
}