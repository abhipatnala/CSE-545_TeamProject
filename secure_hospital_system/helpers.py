from .models import *

def getRoleBasedMenus(user_id):
    user =  SHSUser.objects.select_related().filter(user = user_id)

    role = user[0].role_id
    role_name =''
    if role is not None:
        role_name = role.role_name
    menuList = Menu_Mapping.objects.filter(role_id = role.role_id)
    # import ipdb; ipdb.set_trace()
    context = {
        'role_name' : role_name,
        'menuList' : menuList,
    }
    return context

