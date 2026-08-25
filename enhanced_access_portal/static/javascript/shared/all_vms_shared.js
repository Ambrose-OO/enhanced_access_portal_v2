
// Setting up variables for later use




// Sub-functions

function search_all_vms_call_handler(search_query){
    fetch(
        all_vms_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams(
                {
                }
            )
        }
    )
    .then(response => response.json())
    .then(data => {

        if (data.status == "success"){

            // Generating vm entries for VM searching

            all_vms_display_content.innerHTML = ""; // Clearing elements for the all vms section

            // Display available VM details
            for (const vm of data.vms){
                
                // Checking if the searched query matches with the given vm name.
                // If it does, then we will display the vm
                if (substring_match(search_query, vm_name) == true){
                    // Generating the vm element visual listing
                    generate_vm_element_returns = generate_vm_element(
                        vm.vm_name,
                        vm.vm_status,
                        vm.vm_ip
                    );
                    vm_add_button = generate_vm_element_returns[0];
                    vm_add_button.remove();
                    vms_content = generate_vm_element_returns[1];
                    vm_title = generate_vm_element_returns[2];
                    vm_name = generate_vm_element_returns[3];

                    //vm_title.innerHTML = vm_counter + " . " + vm_title.innerHTML;
                    vm_title.style.textAlign = "center";

                    // Generating vm entries for VM searching - Rendering the div 
                    all_vms_display_content.appendChild(vms_content);

                    let divider = document.createElement("div");
                    divider.className = "content_divider";
                    divider.style.marginTop = "1%";
                    divider.style.marginBottom = "1%";
                    
                    all_vms_display_content.appendChild(divider);
                    
                }
                
            }

            // Feedback relay to the user
            search_button.innerHTML = "Close search";
            prompt_user(
                "Success: Search query",
                "Search query went through sucessfully."
            );
                
        }else{
            prompt_user(
                "Error: Server error handling the search query",
                "Error handling the search query. Please try again."
            );
            search_button.innerHTML == "Search"
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
        prompt_user(
            "Error: Server error handling the search query",
            "Error handling the search query. Please try again."
        );
        search_button.innerHTML == "Search"

    });
}


function search_all_vms(){
    if (search_button.innerHTML == "Search"){

        if (vm_search.value == ""){
            prompt_user(
                "Error: Cannot run a search query",
                "Error handling the search query. As nothing has been entered into the 'Search VMs' entry box. Please try again."
            );
        }else{
            search_button.innerHTML = "Indexing..."
            search_query = vm_search.value;

            search_all_vms_call_handler(search_query);
        }
        
    }else if(search_button.innerHTML == "Close search"){
        search_button.innerHTML = "Search";
        search_query = "";
        search_all_vms_call_handler(search_query);
    }
    
}



