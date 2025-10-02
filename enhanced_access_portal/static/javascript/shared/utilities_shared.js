
// Setting up variables for later use




// Sub-functions

function update_name_email_display() {
    const name_display = document.getElementById("name_display");
    const email_display = document.getElementById("email_display");
                   
    fetch(
        email_name_request_url, 
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

            name_display.innerHTML = data.name;
            email_display.innerHTML = data.email; 

        }else{
            //console.log(data.message);
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
update_name_email_display() // On program launch, fetch the user/admins name/email display


function reset_section_button_background()
{      
    projects_button.style = "margin-top: 5px;";
    groups_button.style = "margin-top: 5px;";
    all_vms_button.style = "margin-top: 5px;";
    statistics_button.style = "margin-top: 5px;";
}


function toggle_lower_button_panel(toggle){
    const lower_button_panel = document.getElementById("lower_button_panel");
    const grey_divider = document.getElementById("grey_divider");

    if (toggle == true){
        lower_button_panel.style.display = "flex";
        grey_divider.style.marginTop = "1%";
    }else{
        lower_button_panel.style.display = "none";
        grey_divider.style.marginTop = "5%";
    }
}

function generate_vm_element(
    vm_name,
    vm_status,
    vm_ip
){

    const vms_content = document.createElement("div");
    vms_content.className = "vms_content";


    const vm_title = document.createElement("p");
    vm_title.className = "roboto_font project_entry_p2";
    vm_title.innerHTML = "Virtual machine: " + vm_name + " | Status: " + vm_status + " | " + vm_ip;
    vms_content.appendChild(vm_title);

            
    const vm_add_button = document.createElement("button");
    vm_add_button.type = "button";
    vm_add_button.className = "alternate_connect_button";

    vm_add_button.onclick = () => ADMIN_USER_PROMPT_add_vm(vms_content, vm_add_button, vm.vm_id);
                    
    vm_add_button.innerHTML = "Add VM";
    vms_content.appendChild(vm_add_button);

    return [vm_add_button, vms_content, vm_title, vm_name];
}


// Functions

function USER_ADMIN_PROMPT_logout_attempt() {

    section_reveal('logging_out_section');
    
    console.log("logout attempt");

    setTimeout(function() {
                                       
        fetch(
            logout_request_url, 
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
                window.location.href = "/login_page/";
            }else{
                //console.log("error logging out");
            }
                                                                        
        })
        .catch(error => {
            //console.error("Error:", error);
        });

    }, 1000);

}