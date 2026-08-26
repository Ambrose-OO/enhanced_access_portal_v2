
// Setting up variables for later use

let project_identifier = ""; // Variable used to pass a project identifer code when creating a project


// Sub-functions

function generate_project_identifier_string() {
    const alphabet = 'abcdefghijklmnopqrstuvwxyz';
    let result = '';

    for (let i = 0; i < 8; i++) {
        // Pick random index
        const randomIndex = Math.floor(Math.random() * alphabet.length);
        let char = alphabet[randomIndex];

        // 50% chance to uppercase
        if (Math.random() < 0.5) {
        char = char.toUpperCase();
        }

        result += char;
    }
    project_identifier = result; 
    return result;
}


function toggle_add_user_to_project_button_innertext(default_state){
    if (default_state == true){
        add_user_button.innerHTML = "Add user";
    }else{
        add_user_button.innerHTML = "Go back to project detail";
    }
}


function navigate_to_project_creation(){ 

    // Creating a project identifier
    const project_identifier = generate_project_identifier_string();

    const project_name = document.getElementById("project_name_entry");
    project_name.placeholder = "Project " + project_identifier;

    const project_identifier_label = document.getElementById("project_identifier_label");
    project_identifier_label.innerHTML = "Project identifier: " + project_identifier;
    
    // Navigating to the section within the project section area
    

    project_creation.style.display = "flex";
    project_display.style.display = "none";
    project_content.style.display = "none";
    available_vms_display.style.display = "none";
}


function project_creation_cancellation(full_cancel){

    if (full_cancel == true){
        project_creation.style.display = "none";
        project_display.style.display = "none";
        project_content.style.display = "none";
        
        // Resetting the project creation page section
        project_detail.style.display = "block";
        project_creation_loading.style.display = "none";

        if (previous_project_section == "project_content"){
            project_content.style.display = "grid";
        }else if (previous_project_section == "project_display"){
            project_display.style.display = "flex";
        }else if (previous_project_section == "project_creation"){
            project_creation.style.display = "flex";
        }
    }else{
       
        // Resetting the project creation page section
        project_detail.style.display = "block";
        project_creation_loading.style.display = "none";
    
    }
   
}


function update_available_project_users() { 
    if (selected_project_id != ""){
         // Display users
        const project_available_users_content = document.getElementById("project_available_users_content");
        
        fetch(
            available_users_request_url, 
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
                },
                body: new URLSearchParams(
                    {
                        project_id: selected_project_id
                    }
                )
            }
        )
        .then(response => response.json())
        .then(data => {
            
            if (data.status == "success"){
                
                project_available_users_content.innerHTML = ""; // Clearing the content views
                //console.log("got available user data");
                for (const user of data.available_users_details){

                    const user_content = document.createElement("div");
                    user_content.className = "vms_content";

                    const member_title = document.createElement("p");
                    member_title.className = "roboto_font project_entry_p2";
                    member_title.innerHTML = user.firstname + " | " + user.emailaddress + " | Type: " + user.type; 
                    user_content.appendChild(member_title);
                                
                    const user_add_button = document.createElement("button");
                    user_add_button.type = "button";
                    user_add_button.className = "alternate_connect_button";

                    user_add_button.onclick = () => ADMIN_PROMPT_add_user(user_content, user_add_button, user.user_id);
                    
                    user_add_button.innerHTML = "Add user";
                    user_content.appendChild(user_add_button);

                    // Rendering the div we created into "project_available_users_content"
                    project_available_users_content.appendChild(user_content);
                }
                
            }else{
                //console.log(data.message);
            }
                                                                        
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }
}
//setInterval(update_available_project_users, 3000); // Updating available vm content every 3 seconds


// Functions

function ADMIN_PROMPT_create_project_attempt(project_identifier_code){

    const query_debug_id = generate_debug_id() + "_button_click";
    console.log(query_debug_id + " Client: Point A - Create project attempt");

    // Hiding the project creation form and revealing project loading icon

    const project_detail = document.getElementById("project_detail");
    
    const project_name_entry = document.getElementById("project_name_entry");

    project_detail.style.display = "none";
    project_creation_loading.style.display = "block";
    
    // Post request to create project
    console.log(query_debug_id + " Client: Point B - Create project attempt");
    setTimeout(function() {
                                       
        fetch(
            create_project_request_url, 
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
                },
                body: new URLSearchParams(
                    {
                        project_name: project_name_entry.value,
                        project_identifier: project_identifier,
                        debug_id: query_debug_id
                    }
                )
            }
        )
        .then(response => response.json())
        .then(data => {
            console.log(query_debug_id + " Client: Point F - Create project attempt");

            if (data.status == "success"){
                console.log(query_debug_id + " Client: Point F.1.1 - Create project attempt");
  
                const project_detail = document.getElementById("project_detail");

                const register_loading_text = document.getElementById("register_loading_text");
                register_loading_text.innerHTML = "Project created!";
            
                setTimeout(function() {
                    
                    project_creation_cancellation(true); // Moving user back to main project display section
                    register_loading_text.innerHTML = "Creating project"; // Resetting text

                }, 3000);

                console.log(query_debug_id + " Client: Point F.1.2 - Create project attempt");

            }else{
                
                console.log(query_debug_id + " Client: Point F.2.1 - Create project attempt");

                if (data.header_message == "Error: Invalid project name"){
                     console.log(query_debug_id + " Client: Point F.2.2 - Create project attempt");
                    prompt_user(data.header_message, data.message);
                    project_creation_cancellation(false); // Resettingt he project creation screen
                }else{
                    console.log(query_debug_id + " Client: Point F.2.3 - Create project attempt");
                    const register_loading_text = document.getElementById("register_loading_text");
                    register_loading_text.innerHTML = "Project failed to create";

                    prompt_user(data.header_message, data.message);

                    setTimeout(function() {
                        project_creation_cancellation(true); // Moving user back to main project display section
                        register_loading_text.innerHTML = "Creating project"; // Resetting text
                    }, 3000);

                     console.log(query_debug_id + " Client: Point F.2.4 - Create project attempt");
                }
            }
                                                                        
        })
        .catch(error => {
            console.error("Error:", error);
            prompt_user("Error: Unknown error", "Root cause not known.");
            console.log(query_debug_id + " Client: Point F.2.5 - Create project attempt");
        });

    }, 1000);
}


function ADMIN_PROMPT_delete_project(arg_list){

    //console.log("-----------");
    //console.log("Deleting VM");
                    
    let delete_project_button = arg_list[1];
    let project_id_to_delete = arg_list[2];

    delete_project_button.innerHTML = "Removing..."

    fetch(
        delete_project_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams(
                {
                    project_id: project_id_to_delete
                }
            )
        }
    )
    .then(response => response.json())
    .then(data => {
        
        if (data.status == "success"){
            
            prompt_user(data.header_message, data.message);
            delete_project_button.innerHTML = "Success!"
            update_projects_content()
          
        }else{
            // If the VM has failed to be deleted, give a failed prompt
            // then return back to normal
            //console.log(data.message);
            prompt_user(data.header_message, data.message);

            delete_project_button.innerHTML = "Failed.";
            setTimeout(function() {
                delete_project_button.innerHTML = "Delete";
            }, 3000);
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
    });

}


function ADMIN_PROMPT_add_user(user_content, user_add_button, user_id_to_add) {
    // Checking if a project is selected, if not, return and do nothing
    if (selected_project_id == ""){
        //console.log("no selected project"); 
        return;
    }   

    //console.log("add user to project");
                    
    user_add_button.innerHTML = "Adding...";

    fetch(
        add_users_to_project_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams(
                {
                    user_id: user_id_to_add,
                    project_id: selected_project_id
                }
            )
        }
    )
    .then(response => response.json())
    .then(data => {
        
        if (data.status == "success"){
            
            prompt_user(data.header_message, data.message);

            // Updating available user data
            update_available_project_users();
            
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

            user_add_button.innerHTML = "Failed.";
            setTimeout(function() {
                user_add_button.innerHTML = "Add User";
            }, 3000);
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
    });
}


function ADMIN_PROMPT_remove_member_from_project(arg_list) {
            
    let member_content = arg_list[0];
    let member_remove_button = arg_list[1];
    let member_id_to_remove = arg_list[2];
    let project_id_to_remove_from = arg_list[3];
    
    if (project_id_to_remove_from == ""){
        //console.log("no selected project"); 
        return;
    }
     
    member_remove_button.innerHTML = "Removing...";

    fetch(
        remove_user_from_project_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams(
                {
                    user_id: member_id_to_remove,
                    project_id: project_id_to_remove_from
                }
            )
        }
    )
    .then(response => response.json())
    .then(data => {
        
        if (data.status == "success"){
            
            prompt_user(data.header_message, data.message);

            // Updating available user data
            update_available_project_users();
            
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

            member_remove_button.innerHTML = "Failed.";
            setTimeout(function() {
                member_remove_button.innerHTML = "Add User";
            }, 3000);
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
    });
}