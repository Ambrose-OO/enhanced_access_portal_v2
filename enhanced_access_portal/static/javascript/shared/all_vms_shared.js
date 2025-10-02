
// Setting up variables for later use




// Sub-functions

function search_all_vms(){
    if (search_button.innerHTML == "Search"){

        if (vm_search.value == ""){
            prompt_user(
                "Error: Cannot run a search query",
                "Error handling the search query. As nothing has been entered into the 'Search VMs' entry box. Please try again."
            );
        }else{
            search_query = vm_search.value;
            search_button.innerHTML = "Close search";
            prompt_user(
                "Success: Search query",
                "Search query went through sucessfully."
            );
        }
        
    }else{
        search_button.innerHTML = "Search";
        search_query = "";
    }
    
}