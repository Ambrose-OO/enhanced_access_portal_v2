
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


// Functions

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
            
    console.log("-----------");
    console.log("Removing VM");
    
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


