
// Setting up variables for later use




// Sub-functions

function search_all_vms_call_handler(
    search_query, 
    query_debug_id, 
    silence_feedback = false,
    polling_loop = false
){

    console.log(query_debug_id + " Client: Point A");
    
    return fetch(
        all_vms_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams(
                {
                    debug_id: query_debug_id
                }
            )
        }
    )
    .then(response => response.json())
    .then(data => {

        console.log(query_debug_id + " Client: Point E");

        if (data.status == "success"){

            // Generating vm entries for VM searching
            const all_vms_display_content = document.getElementById("all_vms_display_content");
            all_vms_display_content.innerHTML = ""; // Clearing elements for the all vms section
            
            console.log(query_debug_id + " Client: Point F");

            // Display available VM details
            for (const vm of data.vms){
                
                // Checking if the searched query matches with the given vm name.
                // If it does, then we will display the vm
                if (substring_match(search_query, vm.vm_name) == true){
                    
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

            console.log(query_debug_id + " Client: Point G");

            // Feedback relay to the user
            if (silence_feedback == false){
                prompt_user(
                    "Success: Search query",
                    "Search query went through sucessfully."
                );
            }
       
            console.log(query_debug_id + " Client: Point H");
        
        }else{
            prompt_user(data.header_message, data.message);
            if (!polling_loop) {
                search_button.innerHTML = "Search"
            }
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
        prompt_user(data.header_message, data.message);
        if (!polling_loop) {
            search_button.innerHTML = "Search"
        }
    });
}


function search_all_vms(){

    // Function call when the vm search button is clicked

    const query_debug_id = generate_debug_id() + "_button_click";
    console.log(query_debug_id + " Client: Point 1");

    const search_button = document.getElementById("search_button");
    
    if (search_button.innerHTML.trim() == "Search"){

        console.log(query_debug_id + " Client: Point 2");

        if (vm_search.value == ""){
            prompt_user(
                "Error: Cannot run a search query",
                "Error handling the search query. As nothing has been entered into the 'Search VMs' entry box. Please try again."
            );
        }else{
            console.log(query_debug_id + " Client: Point 3");
            search_button.innerHTML = "Indexing..."
            search_query = vm_search.value;

            search_all_vms_call_handler(search_query, query_debug_id);
            search_button.innerHTML = "Close search";
            console.log(query_debug_id + " Client: Point 3.2");
        }
        
    }else if(search_button.innerHTML.trim() == "Close search"){
        console.log(query_debug_id + " Client: Point 4");

        search_button.innerHTML = "Indexing..."
        search_query = "";

        search_all_vms_call_handler(search_query, query_debug_id);
        search_button.innerHTML = "Search"
        console.log(query_debug_id + " Client: Point 4.2");

    }
    
}


function update_all_vms(){

    search_query = "";

    if(search_button.innerHTML.trim() == "Close search"){
        search_query = vm_search.value;
    }

    const query_debug_id = generate_debug_id();
    console.log(query_debug_id + " Client: Point 1");

    search_all_vms_call_handler(search_query, query_debug_id, true, true)
        .finally(() => {
            // Once the first request has been handled, wait one second before doing the next call
            setTimeout(update_all_vms, BASE_POLL_TIME);
        });
}

update_all_vms();
