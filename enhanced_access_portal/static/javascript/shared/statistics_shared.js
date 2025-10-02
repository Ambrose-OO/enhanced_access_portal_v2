
// Setting up variables for later use




// Sub-functions

function update_statistics() { 
            
    fetch(
        statistics_request_url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie('csrftoken') //https://www.geeksforgeeks.org/python/csrf-token-in-django/
            },
            body: new URLSearchParams(
                {}
            )
        }
    )
    .then(response => response.json())
    .then(data => {
        
        if (data.status == "success"){
            
            statistics_data = data.statistics; 

            // Resource stats - p elements
            const vm_total_p = document.getElementById("vm_total_p");
            const vms_online_p = document.getElementById("vms_online_p");
            const vms_offline_p = document.getElementById("vms_offline_p");

            const unassigned_project_vms_p = document.getElementById("unassigned_project_vms_p");
            const assigned_project_vms_p = document.getElementById("assigned_project_vms_p");

            const version_number_p = document.getElementById("version_number_p");

            // Resource stats - data insertion 
            vm_total_p.innerHTML = "Total number of VMs: " + statistics_data.vm_total;
            vms_online_p.innerHTML = "VMs online: " + statistics_data.vms_online; 
            vms_offline_p.innerHTML = "VMs offline: " + statistics_data.vms_offline;

            unassigned_project_vms_p.innerHTML = "Unassigned project VMs: " + statistics_data.unassigned_project_vms;
            assigned_project_vms_p.innerHTML = "Assigned project VMs: " + statistics_data.assigned_project_vms;
            
            version_number_p.innerHTML = "Version number: " + statistics_data.version_number;
            
            // Usage - p elements
            const user_total_p = document.getElementById("user_total_p");
            const admins_total_p = document.getElementById("admins_total_p");
            const system_users_total_p = document.getElementById("system_users_total_p");

            const project_total_p = document.getElementById("project_total_p");
            const group_total_p = document.getElementById("group_total_p");

            // Usage - p elements
            user_total_p.innerHTML = "Total number of users: " + statistics_data.user_total;
            admins_total_p.innerHTML = "Total number of admins: " + statistics_data.admins_total; 
            system_users_total_p.innerHTML = "Overal number of system users: " + statistics_data.system_users_total;

            project_total_p.innerHTML = "Total number of projects: " + statistics_data.project_total;
            group_total_p.innerHTML = "Total number of groups: " + statistics_data.group_total;
        
        }else{
            console.log(data.message);
        }
                                                                    
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
update_statistics();
setInterval(update_statistics, 1000); // Updating available vm content every second