
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