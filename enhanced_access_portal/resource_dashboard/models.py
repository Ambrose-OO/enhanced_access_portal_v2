from django.db import models
from datetime import date
from login_page.models import User

# Create your models here.
class Projects(models.Model):
  #Don't need a project_id field as django adds id fields by default. 
  #On foreign keys, it identifies the the keys origin database name then ID. 
  #For example user_id for the "Users" model
  
  entity_type = models.CharField(max_length = 255, default = "-")
  entity_id = models.CharField(max_length = 255, default = "-")
  owner_id = models.ForeignKey(User, on_delete=models.CASCADE, default = 0) 
  project_name = models.CharField(max_length = 255, default = "-")
  project_identifier_code = models.CharField(max_length = 255, default = "-")

class VMs(models.Model):
    #Don't need a vms_id field as django adds id fields by default. 

    #TODO: finish this
    vm_name = models.CharField(max_length = 255, default = "undefined_vm_name")
    vm_online = models.CharField(max_length = 255, default = "offline")
    vm_ip = models.CharField(max_length = 255, default = "0.0.0.0") 
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, default = None, null = True, blank = True)
    # If the user entry is deleted and their foreign key resides in an entry for a VMs then the Vms entry 
    # is deleted too
    
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, default = None, null = True, blank = True) 
    # If the user entry is deleted and their foreign key resides in an entry for a VMs then the Vms entry 
    # is deleted too

class VM_Group(models.Model):
    #Don't need a group_id field as django adds id fields by default. 

    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, default = 0) 
    # If the user entry is deleted and their foreign key resides in an entry for a VM_Group then the VM_Groupe entry 
    # is deleted too

    vm_id = models.ForeignKey(VMs, on_delete=models.CASCADE, default = 0)
    # If the vm_entry is deleted and their foreign key resides in an entry for a VM_Group then the VM_Group entry 
    # is deleted too

    vm_group_name = models.CharField(max_length = 255, default = "-") 
    created_date = models.DateField(default = date.today) # https://www.geeksforgeeks.org/datefield-django-models/
