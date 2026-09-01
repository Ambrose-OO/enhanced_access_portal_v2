
// Setting up variables for later use




// Sub-functions

function navigate_to_group_creation(){ 

    // Creating a project identifier
    const group_name = document.getElementById("group_name_entry");
    group_name.placeholder = "Group name";


    // Navigating to the section within the project section area
    group_creation.style.display = "flex";
    group_display.style.display = "none";
    group_content.style.display = "none";
    available_group_vms_display.style.display = "none";

}


function group_panel_navigation(panel){

    previous_group_section = panel; 

    // Navigating to the section within the group section area

    // Hiding all the panels in the group section
    group_creation.style.display = "none";
    group_display.style.display = "none";
    group_content.style.display = "none";
    available_group_vms_display.style.display = "none";

    // Working on which one to reval and how
    if (panel == "group_creation"){
        group_creation.style.display = "flex";
    } 
    else if (panel == "group_content"){
        group_content.style.display = "grid";
    }
    else if (panel = "group_display"){
        group_display.style.display = "";
    }
  
}


function group_creation_cancellation(){
    
    group_creation.style.display = "none";
    group_display.style.display = "none";
    group_content.style.display = "none";

    if (previous_group_section == "group_content"){
        group_content.style.display = "grid";
    }else if (previous_group_section == "group_display"){
        group_content.style.display = "flex";
    }else if (previous_group_section == "group_creation"){
        group_content.style.display = "flex";
    }
}


function toggle_add_group_vm_button_innertext(default_state){
    if (default_state == true){
        add_group_vm_button.innerHTML = "Add VM";
    }else{
        add_group_vm_button.innerHTML = "Go back to group detail";
    }
}
function reveal_group_display_available_vms_subfunction(state){
    if (state == true){
        update_available_group_vms_content(false)
        available_group_vms_display.style.display = "block";
        group_display.style.display = "none";

        toggle_add_group_vm_button_innertext(false);
    }else if (state == false){
        available_group_vms_display.style.display = "none";
        group_display.style.display = "block";
        
        toggle_add_group_vm_button_innertext(true);
    }
}
function reveal_group_display_available_vms(state)
{

    if (state){
        reveal_group_display_available_vms_subfunction(state);
    }
    else if (available_group_vms_display.style.display == "block"){
        reveal_group_display_available_vms_subfunction(false);
    } else {
        reveal_group_display_available_vms_subfunction(true);
    }

}


function reset_group_creation_section(){
    group_creation_loading_text.innerHTML = "Creating group"; // Resetting text

    group_detail.style.display = "block";
    group_creation_loading.style.display = "none";  
}


function update_group_display_with_group_data(group_listing_data, group_metadata_data){
    // Display virtual machines
    const group_display_vms_content = document.getElementById("group_display_vms_content");
    group_display_vms_content.innerHTML = ""; // Clearing all the elements under the div content container

    for (const group of group_listing_data){
        if (group["group_root"] == false & group["group_name"] == selected_group_name){
            const vms_content = document.createElement("div");
            vms_content.className = "vms_content";


            const vm_title = document.createElement("p");
            vm_title.className = "roboto_font project_entry_p2"
            vm_title.innerHTML = "Virtual machine: " + group.vm_name + " | Status: " + group.vm_status + " | " + group.vm_ip;
            vms_content.appendChild(vm_title);

    
            const vm_connect_button = document.createElement("button");
            vm_connect_button.type = "button";
            vm_connect_button.className = "alternate_connect_button";
            //vm_connect_button.onclick = () => navigate_to_project_display(project);
            //VM doesn't have actual connect functionality as this is a demo
            vm_connect_button.innerHTML = "Connect";
            vms_content.appendChild(vm_connect_button);

            const vm_remove_button = document.createElement("button");
            vm_remove_button.type = "button";
            vm_remove_button.className = "alternate_connect_button";
            
            let group_vm_removal_args = [vms_content, vm_remove_button, group.vm_id];
            vm_remove_button.onclick = () => confirmation_prompt_user(
                "VM group removal confirmation",
                "Clicking confirm will mean you will completely remove the vm from the group entry. Are you sure?",
                "ADMIN_USER_PROMPT_remove_vm_from_group",
                group_vm_removal_args
            );
            
        
            vm_remove_button.innerHTML = "Remove";
            vms_content.appendChild(vm_remove_button);


            // Rendering the div we created into "group_display_vms_content"
            group_display_vms_content.appendChild(vms_content);
        }   
    }
    
}


function navigate_to_group_display(group_listing_data, group_metadata_data, inputted_selected_group_name) {
    // Updating knowledge on which project has been selected by changing
    // the selected_project_id variable

    selected_group_name = inputted_selected_group_name; 

    // Hide all toggle buttons
    lower_button_toggle(false, false, false, false, true, false, true);

    // Navigates and provides data
    group_content.style.display = "none";
    group_display.style.display = "flex";
    previous_group_section = "group_display";

    // Updating displays for virtual machines
    update_group_display_with_group_data(group_listing_data, group_metadata_data);
}


function generate_groups_content_with_group_data(group_detail_data){
    group_content.innerHTML = ""; // Clearing all the elements under the div content container

    // Display project details
    const group_listing_data = group_detail_data.listings;
    const group_metadata_data = group_detail_data.meta_data;
    
    let group_dictionary = {};

    // Collecting data for individual groups
    for (const group of group_listing_data){
        if (group.group_root == false){
            if (group_dictionary[group.group_name]){
                group_dictionary[group.group_name]["count"] += 1;
                if (group.vm_status == "Online"){
                    group_dictionary[group.group_name]["online_count"] += 1;
                }
            }else{
                group_dictionary[group.group_name] = {}
                group_dictionary[group.group_name]["count"] = 0;
                group_dictionary[group.group_name]["online_count"] = 0;
            }
        }else{
            if (!group_dictionary[group.group_name]){
                group_dictionary[group.group_name] = {}
                group_dictionary[group.group_name]["count"] = 0;
                group_dictionary[group.group_name]["online_count"] = 0;
            }
        }
    }
    
    // Displaying groups
    for (const group of group_listing_data){
        // Checking for the group root records which act as a representation of a group
        if (group.group_root == true){
            
            const group_entry_div = document.createElement("div");
            group_entry_div.className = "rounded_container project_entry";
            group_entry_div.id = "project_entry";

            // <p> class elements
            const group_title = document.createElement("p");
            group_title.className = "roboto_font project_entry_p1";
            group_title.innerHTML = "Group name: " + group.group_name;
            group_entry_div.appendChild(group_title);

            const group_id = document.createElement("p");
            group_id.className = "roboto_font project_entry_p2";
            group_id.innerHTML = "Id: " + group.group_id;
            group_entry_div.appendChild(group_id);

            const group_details = document.createElement("p");
            group_details.className = "roboto_font";
            group_details.innerHTML = "VMs (" + group_dictionary[group.group_name]["count"] + ") VMs online (" + group_dictionary[group.group_name]["online_count"] + ")";
            group_entry_div.appendChild(group_details);
            
            // <button> class elements
            const open_group_button = document.createElement("button");
            open_group_button.type = "button";
            open_group_button.className = "alternate_connect_button";
            open_group_button.onclick = () => navigate_to_group_display(group_listing_data, group_metadata_data, group.group_name);
            open_group_button.innerHTML = "Open";
            open_group_button.style.marginRight = "3%";
            group_entry_div.appendChild(open_group_button);


            const delete_group_button = document.createElement("button");
            delete_group_button.type = "button";
            delete_group_button.className = "alternate_connect_button"

            let delete_group_args = [group_entry_div, delete_group_button, group.group_id];
            delete_group_button.onclick = () => confirmation_prompt_user(
                "Group deletion confirmation",
                "Clicking confirm will mean you will completely delete the group entry. There is no recovery of this data. Are you sure?",
                "ADMIN_USER_PROMPT_delete_group",
                delete_group_args
            );
            
            delete_group_button.innerHTML = "Delete";
            group_entry_div.appendChild(delete_group_button);
            
            group_content.appendChild(group_entry_div);
        }
    }
}



function update_groups_content() {
    const group_content = document.getElementById("group_content");

    const timeout_controller = new AbortController();
    const timeout_id = setTimeout(() => timeout_controller.abort(), 10000); // network timeout, kept shorter than BASE_POLL_TIME on purpose
                     
    return fetch(
        group_list_request_url,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams({}),
            signal: timeout_controller.signal
        }
    )
    .then(response => response.json())
    .then(data => {

        if (data.status == "success"){
        
            generate_groups_content_with_group_data(data.groups)

        }else{
            //console.log(data.message);
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
    })
    .finally(() => {
        clearTimeout(timeout_id);
        // Reschedule from inside every call (not just the first) so the loop is actually self-sustaining
        setTimeout(update_groups_content, BASE_POLL_TIME);
    });

}
update_groups_content() 



function update_available_group_vms_content() {
    if (group_name_target == ""){
        return;
    }
    
    // Fetching available group vms

    const timeout_controller = new AbortController();
    const timeout_id = setTimeout(() => timeout_controller.abort(), 10000); // network timeout, kept shorter than BASE_POLL_TIME on purpose

    return fetch(
        available_vms_for_group_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams(
                {
                    group_name_target: selected_group_name
                }
            ),
            signal: timeout_controller.signal
        }
    )
    .then(response => response.json())
    .then(data => {

        if (data.status == "success"){
            
            group_available_vms_content.innerHTML = ""; // Clearing all the elements under the div content container
            vm_counter = 0;

            // Display available VM details
            for (const vm of data.vms){
                vm_counter += 1;

                // Generating vm entries for available vms for selection in a group
                generate_vm_element_returns = generate_vm_element(
                    vm.vm_name,
                    vm.vm_status,
                    vm.vm_ip
                );
                vm_add_button = generate_vm_element_returns[0];
                vms_content = generate_vm_element_returns[1];
                
                vm_add_button.onclick = () => ADMIN_USER_PROMPT_add_vm_to_group(vms_content, vm_add_button, vm.vm_id);

                // Generating vm entries for available vms for selection in a group - Rendering the div we created into "group_available_vms_content"
                group_available_vms_content.appendChild(vms_content);

            }

        }else{
            console.log("Error updating available group vms content");
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
    })
    .finally(() => {
        clearTimeout(timeout_id);
        // Reschedule from inside every call (not just the first) so the loop is actually self-sustaining
        setTimeout(update_available_group_vms_content, BASE_POLL_TIME);
    });

}
update_available_group_vms_content() 
 


// Functions

function ADMIN_USER_PROMPT_create_group_attempt(project_identifier_code){
    // Hiding the group creation form and revealing group loading icon
    
   
    const group_name_entry = document.getElementById("group_name_entry");

    group_detail.style.display = "none";
    group_creation_loading.style.display = "block";
    
    // Post request to create group
    setTimeout(function() {
                                       
        fetch(
            create_group_request_url, 
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
                },
                body: new URLSearchParams(
                    {
                        group_name: group_name_entry.value
                    }
                )
            }
        )
        .then(response => response.json())
        .then(data => {

            if (data.status == "success"){
                
                group_creation_loading_text.innerHTML = "Group created!";
                
                generate_groups_content_with_group_data(data.groups);

                setTimeout(function() {
                    group_creation_cancellation(); // Moving user back to main project display section
                    reset_group_creation_section();
                }, 3000);

            }else{

                const group_creation_loading_text = document.getElementById("group_creation_loading_text");
                group_creation_loading_text.innerHTML = "Group failed to create";
                
                prompt_user(data.header_message, data.message);

                setTimeout(function() {
                    reset_group_creation_section();
                }, 3000);

            }
                                                                        
        })
        .catch(error => {
            console.error("Error:", error);
        });

    }, 1000);
}


function ADMIN_USER_PROMPT_add_vm_to_group(vms_content, vm_add_button, vm_id_to_add) {
    if (selected_group_name == ""){
        //console.log("no selected group"); 
        return;
    }

    vm_add_button.innerHTML = "Adding vm...";

    fetch(
        add_vm_to_group_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams(
                {
                    vm_id: vm_id_to_add,
                    group_name: selected_group_name
                }
            )
        }
    )
    .then(response => response.json())
    .then(data => {
        
        if (data.status == "success"){
                
            prompt_user(data.header_message, data.message);

            // Updating group information currently being displayed to the user
            const group_listing_data = data.groups.listings;
            const group_metadata_data = data.groups.meta_data;

            update_group_display_with_group_data(group_listing_data, group_metadata_data);

        }else{

            prompt_user(data.header_message, data.message);

            // If the VM has failed to be added, give a failed prompt
            // then return back to normal

            vm_add_button.innerHTML = "Failed.";
            setTimeout(function() {
                vm_add_button.innerHTML = "Add VM";
            }, 3000);
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
    });
}


function ADMIN_USER_PROMPT_remove_vm_from_group(arg_list){
    
    //console.log("-----------------");
    //console.log("Removing group VM");
    
    let vms_content = arg_list[0];
    let vm_remove_button = arg_list[1];
    let vm_id_to_remove = arg_list[2];
                    
    vm_remove_button.innerHTML = "Removing...";
    
    fetch(
        remove_group_vm_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams(
                {
                    vm_id: vm_id_to_remove,
                    group_name: selected_group_name
                }
            )
        }
    )
    .then(response => response.json())
    .then(data => {

        if (data.status == "success"){
            
            prompt_user(data.header_message, data.message);

            // Updating group information currently being displayed to the user
            const group_listing_data = data.groups.listings;
            const group_metadata_data = data.groups.meta_data;

            update_group_display_with_group_data(group_listing_data, group_metadata_data);
    
        }else{

            prompt_user(data.header_message, data.message);
            
            // If the VM has failed to be added, give a failed prompt
            // then return back to normal

            vm_remove_button.innerHTML = "Failed.";
            setTimeout(function() {
                vm_remove_button.innerHTML = "Remove";
            }, 3000);
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
    });
}


function ADMIN_USER_PROMPT_delete_group(arg_list){

    //console.log("--------------");
    //console.log("Deleting group");
    
    let group_entry_div = arg_list[0];
    let delete_group_button = arg_list[1];
    let group_id_to_delete = arg_list[2];

    delete_group_button.innerHTML = "Removing..."

    fetch(
        delete_group_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams(
                {
                    group_id: group_id_to_delete
                }
            )
        }
    )
    .then(response => response.json())
    .then(data => {
        
        if (data.status == "success"){
            

            generate_groups_content_with_group_data(data.groups);
            console.log("group data generation after group deletion");

            prompt_user(data.header_message, data.message);
           
        }else{
            // If the VM has failed to be deleted, give a failed prompt
            // then return back to normal
            prompt_user(data.header_message, data.message);

            delete_group_button.innerHTML = "Failed.";
            setTimeout(function() {
                delete_group_button.innerHTML = "Delete";
            }, 3000);
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
    });

}