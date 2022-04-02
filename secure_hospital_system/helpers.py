from .models import *

def getRoleBasedMenus(user_id):
    user =  SHSUser.objects.select_related().filter(user = user_id)

    role = user[0].role_id
    role_name =''
    if role is not None:
        role_name = role.role_name
    menuList = Menu_Mapping.objects.filter(role_id = role.role_id)
    context = {
        'role_name' : role_name,
        'menuList' : menuList,
    }
    return context


def twofaEnabled(user):
    return hasattr(user, 'userotp')
