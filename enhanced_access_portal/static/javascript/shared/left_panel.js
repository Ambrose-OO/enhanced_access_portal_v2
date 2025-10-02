
// Setting up variables for later use

const left_panel = document.getElementById("left_panel");


// Sub-functions

/*
* Left panel toggle
*/
function toggle_left_panel(){
    if (left_panel.style.display == "block"){
        left_panel.style.display = "none";
    }else{
        left_panel.style.display = "block";
    }
}


function section_reveal(name) { 
    if (section_lock == false){
        // Reseting selcted vm 
        selected_project_id = "";

        // Hiding add vm and user buttons
        lower_button_toggle(false, false, false, false, false, false, false);

        // Section buttons
        
        reset_section_button_background();

        // Hiding all the sections
        const right_content = document.getElementById("right_content");
        for (const child of right_content.children){
            child.style.display = "none";
        }

        // Revealing section of interest
        const section_element = document.getElementById(name);
        section_element.style.display = "flex";


        if (name == "projects_section"){

            // Handling bottom panel buttons
            toggle_lower_button_panel(true);
            lower_button_toggle(false, false, false, true, false, false, false);

            reset_project_navigation_to_project_content();
            
            // Adjusting project button colour background to indicate its selected
            projects_button.style = "background-color: #FFFFFF; margin-top: 5px;";

        } else if (name == "groups_section"){

            // Handling bottom panel buttons
            toggle_lower_button_panel(true);
            lower_button_toggle(false, false, true, false, false, false, false);
            
            group_panel_navigation("group_content");

            // Adjusting project button colour background to indicate its selected
            groups_button.style = "background-color: #FFFFFF; margin-top: 5px;";
            
            // Resetting a button state
            toggle_add_group_vm_button_innertext(true);

        } else if (name == "all_vms_section"){

            // Handling bottom panel buttons
            toggle_lower_button_panel(false);
            lower_button_toggle(false, false, false, false, false, false, false);

            // Adjusting project button colour background to indicate its selected
            all_vms_button.style = "background-color: #FFFFFF; margin-top: 5px;";

        } else if (name == "statistics_section"){
            
            // Handling bottom panel buttons
            toggle_lower_button_panel(false);
            lower_button_toggle(false, false, false, false, false, false, false);

            // Adjusting project button colour background to indicate its selected
            statistics_button.style = "background-color: #FFFFFF; margin-top: 5px;";

        } else if (name == "logging_out_section"){

            // Handling bottom panel buttons
            toggle_lower_button_panel(false);
            lower_button_toggle(false, false, false, false, false, false, false);

            section_lock = true;

        } else {
            toggle_lower_button_panel(false);
            lower_button_toggle(false, false, false, false, false, false, false);
        }
    }
}
section_reveal("projects_section");
// Doing this so on runtime for the dashboard we navigate to the correct area 