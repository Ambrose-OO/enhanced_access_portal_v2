
// Setting up variables for later use




// Sub-functions

function toggle_add_vm_to_project_button_innertext(default_state){
    if (default_state == true){
        add_vm_button.innerHTML = "Add VM";
    }else{
        add_vm_button.innerHTML = "Go back to project detail";
    }
}


function navigate_to_project_display(project) {
    // Updating knowledge on which project has been selected by changing
    // the selected_project_id variable

    selected_project_id = project.project_id; 

    // Reveals "Add VM" and "Add user" buttons
    lower_button_toggle(true, true, false, false, false, true, false);

    // Navigates and provides data
    const project_content = document.getElementById("project_content");
    const project_display = document.getElementById("project_display");

    project_content.style.display = "none";
    project_display.style.display = "flex";
    previous_project_section = "project_display";

    // Updating displays for virtual machines and users 
    update_project_display_with_project_data(project);
}


function navigate_to_project_rename_display(project) {
    // Updating knowledge on which project has been selected by changing
    // the selected_project_id variable

    selected_project_id = project.project_id; 

    // Reveals "Add VM" and "Add user" buttons
    lower_button_toggle(false, false, false, false, false, true, false);

    // Navigates and provides data
    const project_content = document.getElementById("project_content");
    const project_rename_display = document.getElementById("project_rename_display");

    project_content.style.display = "none";
    project_rename_display.style.display = "flex";

    previous_project_section = "project_rename_display";
}




function reveal_project_display_available_users(state)
{
    if (state == true){
        available_vms_display.style.display = "none";

        project_display_users.style.display = "none";
        project_display_vms.style.display = "none";

        if (CORE_USER_TYPE == "ADMIN"){
            available_users_display.style.display = "block";
            toggle_add_user_to_project_button_innertext(false);
        } 

        toggle_add_vm_to_project_button_innertext(true);
    }else if (state == false){
        available_vms_display.style.display = "none";

        project_display_users.style.display = "block";
        project_display_vms.style.display = "block";
        
        if (CORE_USER_TYPE == "ADMIN"){
            available_users_display.style.display = "none";
            toggle_add_user_to_project_button_innertext(false);
        } 

        toggle_add_vm_to_project_button_innertext(false);
    }
    else if (available_users_display.style.display == "block"){
        available_vms_display.style.display = "none";

        project_display_users.style.display = "block";
        project_display_vms.style.display = "block";

        if (CORE_USER_TYPE == "ADMIN"){
            available_users_display.style.display = "none";
            toggle_add_user_to_project_button_innertext(true);
        }

        toggle_add_vm_to_project_button_innertext(true);
    } else {
        available_vms_display.style.display = "none";

        project_display_users.style.display = "none";
        project_display_vms.style.display = "none";

        if (CORE_USER_TYPE == "ADMIN"){
            available_users_display.style.display = "block";
            toggle_add_user_to_project_button_innertext(false);
        }

        toggle_add_vm_to_project_button_innertext(true);
    }
}
function reveal_project_display_available_vms(state)
{
    if (state == true){
        available_vms_display.style.display = "block";

        project_display_users.style.display = "none";
        project_display_vms.style.display = "none";
        
        if (CORE_USER_TYPE == "ADMIN"){
            available_users_display.style.display = "none";
            toggle_add_user_to_project_button_innertext(true);
        }

        toggle_add_vm_to_project_button_innertext(false);
    }else if (state == false){
        available_vms_display.style.display = "none";

        project_display_users.style.display = "block";
        project_display_vms.style.display = "block";
        
        if (CORE_USER_TYPE == "ADMIN"){
            available_users_display.style.display = "none";
            toggle_add_user_to_project_button_innertext(true);
        }

        toggle_add_vm_to_project_button_innertext(true);
    }
    else if (available_vms_display.style.display == "block"){
        available_vms_display.style.display = "none";

        project_display_users.style.display = "block";
        project_display_vms.style.display = "block";

        if (CORE_USER_TYPE == "ADMIN"){
            available_users_display.style.display = "none";
            toggle_add_user_to_project_button_innertext(true);
        }

        toggle_add_vm_to_project_button_innertext(true);
    } else {
        available_vms_display.style.display = "block";

        project_display_users.style.display = "none";
        project_display_vms.style.display = "none";

        if (CORE_USER_TYPE == "ADMIN"){
            available_users_display.style.display = "none";
            toggle_add_user_to_project_button_innertext(true);
        }
        
        toggle_add_vm_to_project_button_innertext(false);
    }
}


function reset_project_navigation_to_project_content(){

    previous_project_section = "project_content"; 

    // Hiding all the panels in the project section
    if (CORE_USER_TYPE == "ADMIN"){
        const project_creation = document.getElementById("project_creation");
        project_creation.style.display = "none";
    }

    project_display.style.display = "none";
    project_content.style.display = "grid";
    project_rename_display.style.display = "none";
    available_vms_display.style.display = "none";

}


function update_project_display_with_project_data(project){
    // Display virtual machines
    const project_display_vms_content = document.getElementById("project_display_vms_content");
    project_display_vms_content.innerHTML = ""; // Clearing all the elements under the div content container

    for (const vm of project.project_vms_details){
        const vms_content = document.createElement("div");
        vms_content.className = "vms_content";


        const vm_title = document.createElement("p");
        vm_title.className = "roboto_font project_entry_p2"
        vm_title.innerHTML = "Virtual machine: " + vm.vm_name + " | Status: " + vm.vm_status + " | " + vm.vm_ip;
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
        
        let remove_vm_args = [vms_content, vm_remove_button, vm.vm_id];
        vm_remove_button.onclick = () => confirmation_prompt_user(
            "Project VM removal confirmation",
            "Clicking confirm will mean you will remove the VM from the project. You will be able to add it back later if it's available. Are you sure?",
            "ADMIN_USER_PROMPT_remove_vm",
            remove_vm_args
        );

        vm_remove_button.innerHTML = "Remove";
        vms_content.appendChild(vm_remove_button);


        // Rendering the div we created into "project_display_vms_content"
        project_display_vms_content.appendChild(vms_content);
    }
    
    // Display project users
    const project_display_users_content = document.getElementById("project_display_users_content");
    project_display_users_content.innerHTML = ""; // Clearing all the elements under the div content container

    for (const member of project.project_member_details){
        const member_content = document.createElement("div");
        member_content.className = "member_content";


        const member_title = document.createElement("p");
        member_title.className = "roboto_font project_entry_p2";
        member_title.innerHTML = member.firstname + " | " + member.emailaddress + " | Type: " + member.type; 
        member_content.appendChild(member_title);
        
        const member_remove_button = document.createElement("button");
        member_remove_button.type = "button";
        member_remove_button.className = "alternate_connect_button";
        
        member_remove_button.onclick = () => ADMIN_PROMPT_remove_member_from_project(member_content, member_remove_button, member.user_id, project.project_id);
        
        let remove_member_args = [member_content, member_remove_button, member.user_id, project.project_id];
        member_remove_button.onclick = () => confirmation_prompt_user(
            "Member removal confirmation",
            "Clicking confirm will mean you will remove this member from the project. You can add them back later if they still exist in the system. Are you sure?",
            "ADMIN_PROMPT_remove_member_from_project",
            remove_member_args
        );
        
        member_remove_button.innerHTML = "Remove";
        member_content.appendChild(member_remove_button);


        // Rendering the div we created into "project_display_users_content"
        project_display_users_content.appendChild(member_content);
    }
}


function generate_projects_content_with_project_data(project_detail_data){
    const project_content = document.getElementById("project_content");

    project_content.innerHTML = ""; // Clearing all the elements under the div content container

    // Display project details

    for (const project of project_detail_data){
        //console.log(project.project_name);
        //console.log(project.entity_type);
        if (project.entity_type == "PROJECT"){
            const project_entry_div = document.createElement("div");
            project_entry_div.className = "rounded_container project_entry";
            project_entry_div.id = "project_entry";

            // <p> class elements
            const project_title = document.createElement("p");
            project_title.className = "roboto_font project_entry_p1";
            project_title.innerHTML = "Project name: " + project.project_name;
            project_entry_div.appendChild(project_title);

            const project_id = document.createElement("p");
            project_id.className = "roboto_font project_entry_p2";
            project_id.innerHTML = "Id: " + project.project_identifier_code;
            project_entry_div.appendChild(project_id);

            const project_details = document.createElement("p");
            project_details.className = "roboto_font";
            project_details.innerHTML = "VMs (" + project.project_available_vms + ") VMs online (" + project.project_vms_online + ") Users (" + project.project_users + ") Admins (" + project.project_admins + ")";
            project_entry_div.appendChild(project_details);
            
            // <button> class elements
            const open_project_button = document.createElement("button");
            open_project_button.type = "button";
            open_project_button.className = "alternate_connect_button";
            open_project_button.onclick = () => navigate_to_project_display(project);
            open_project_button.innerHTML = "Open";
            open_project_button.style.marginRight = "3%";
            project_entry_div.appendChild(open_project_button);

            if (CORE_USER_TYPE == "ADMIN"){
                const delete_project_button = document.createElement("button");
                delete_project_button.type = "button";
                delete_project_button.className = "alternate_connect_button"

                let delete_project_args = [project_entry_div, delete_project_button, project.project_id];
                delete_project_button.onclick = () => confirmation_prompt_user(
                    "Project deletion confirmation",
                    "Clicking confirm will mean you will completely delete the project entry. There is no recovery of this data. Are you sure?",
                    "ADMIN_PROMPT_delete_project",
                    delete_project_args
                );

                delete_project_button.innerHTML = "Delete";
                delete_project_button.style.marginRight = "3%";
                project_entry_div.appendChild(delete_project_button);
            }

            
            const rename_project_button = document.createElement("button");
            rename_project_button.type = "button";
            rename_project_button.className = "alternate_connect_button";
            rename_project_button.onclick = () => navigate_to_project_rename_display(project);
            rename_project_button.innerHTML = "Rename";
            rename_project_button.style.marginRight = "3%";
            project_entry_div.appendChild(rename_project_button);

            project_content.appendChild(project_entry_div);
        }
    }
}


function update_projects_content() {

    const query_debug_id = generate_debug_id();

    console.log(query_debug_id + " Client: Point A - Project listings");
                      
    return fetch(
        project_list_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams({
                debug_id: query_debug_id
            })
        }
    )
    .then(response => response.json())
    .then(data => {

        if (data.status == "success"){

            console.log(query_debug_id + " Client: Point C - Project listings");

            const project_detail_data = data.projects;
            generate_projects_content_with_project_data(project_detail_data);
           
            console.log(query_debug_id + " Client: Point D - Project listings");

        }else{
            console.log(query_debug_id + " Client: Point C.2-Fail on data retrieve - Project listings");
        }
                                                                    
    })
    .catch(error => {
        //console.error("Error:", error);
        console.log(query_debug_id + " Client: Point C.3-Server error - Project listings");
    });
}
update_projects_content()
    .finally(() => {
        // Once the first request has been handled, wait one second before doing the next call
        console.log(query_debug_id + " Client: Point E - Project listings");
        setTimeout(update_projects_content, BASE_POLL_TIME);
        console.log(query_debug_id + " Client: Point G - Project listings");
    });


function update_available_project_vms() { 
    // Display virtual machines
    const project_available_vms_content = document.getElementById("project_available_vms_content");
    
    fetch(
        available_vms_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams({})
        }
    )
    .then(response => response.json())
    .then(data => {
        
        if (data.status == "success"){
            
            project_available_vms_content.innerHTML = ""; // Clearing the content views
         
            for (const vm of data.vms){
                
                generate_vm_element_returns = generate_vm_element(
                    vm.vm_name,
                    vm.vm_status,
                    vm.vm_ip
                )
                vm_add_button = generate_vm_element_returns[0];
                vms_content = generate_vm_element_returns[1];


                vm_add_button.onclick = () => ADMIN_USER_PROMPT_add_vm(vms_content, vm_add_button, vm.vm_id);

                // Rendering the div we created into "project_available_vms_content"
                project_available_vms_content.appendChild(vms_content);
            }
            
        }else{
            //console.log(data.message);
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
//setInterval(update_available_project_vms, 3000); // Updating available vm content every 3 seconds


// Functions

function ADMIN_USER_PROMPT_rename_project(arg_list){

    //console.log("-----------");
    //console.log("Renaming VM");

    const rename_project_entry = document.getElementById("rename_project_entry");

    if (selected_project_id == ""){
        prompt_user(
            "Error: Rename project query failed", 
            "A project for renaming hasn't been selected."
        );
        return;
    }else if (rename_project_entry.value == ""){
        prompt_user(
            "Error: Rename project query failed", 
            "A project name to rename to hasn't been entered."
        );
        return;
    } else { 
        notify_user("Renaming project...", true);
    }
    
    fetch(
        rename_project_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams(
                {
                    project_id: selected_project_id,
                    new_project_name: rename_project_entry.value
                }
            )
        }
    )
    .then(response => response.json())
    .then(data => {
        
        if (data.status == "success"){
            
            prompt_user(data.header_message, data.message);
            update_projects_content();
            reset_project_navigation_to_project_content();

            lower_button_toggle(false, false, false, true, false, false, false);
        }else{
            // If the VM has failed to be renamed, give a failed prompt
            // then return back to normal
            prompt_user(data.header_message, data.message);
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
    });

}


function ADMIN_USER_PROMPT_add_vm(vms_content, vm_add_button, vm_id_to_add) {
    if (selected_project_id == ""){console.log("no selected vm"); return;}

    //console.log("add vm");
                    
    vm_add_button.innerHTML = "Adding vm...";

    fetch(
        add_vm_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams(
                {
                    vm_id: vm_id_to_add,
                    project_id: selected_project_id
                }
            )
        }
    )
    .then(response => response.json())
    .then(data => {
        
        if (data.status == "success"){
            
            prompt_user(data.header_message, data.message);

            // After successfully removing a VM, request an update on the latest
            // available vms
            update_available_project_vms();

            // Updating project information currently being displayed to the user
            const project_detail_data = data.projects;

            for (const project of project_detail_data){
                if (project.project_id == selected_project_id) { 
                    update_project_display_with_project_data(project);
                }
            }
            
        }else{
            // If the VM has failed to be added, give a failed prompt
            // then return back to normal
            prompt_user(data.header_message, data.message);

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


function ADMIN_USER_PROMPT_remove_vm(arg_list){
            
    //console.log("-----------");
    //console.log("Removing VM");
    
    let vms_content = arg_list[0];
    let vm_remove_button = arg_list[1];
    let vm_id_to_remove = arg_list[2];

    vm_remove_button.innerHTML = "Removing...";

    fetch(
        remove_vm_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams(
                {
                    vm_id: vm_id_to_remove
                }
            )
        }
    )
    .then(response => response.json())
    .then(data => {
        
        if (data.status == "success"){
            
            prompt_user(data.header_message, data.message);

            // Updating project information currently being displayed to the user
            const project_detail_data = data.projects;

            for (const project of project_detail_data){
                if (project.project_id == selected_project_id) { 
                    update_project_display_with_project_data(project);
                }
            }

        }else{
            // If the VM has failed to be added, give a failed prompt
            // then return back to normal
            prompt_user(data.header_message, data.message);

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


