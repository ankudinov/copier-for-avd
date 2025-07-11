from jinja2.ext import Extension

def mlag_groups(inventory):
    mlag_group_list = list()
    for device in inventory:
        if device['mlag_group'] and (device['mlag_group'] not in mlag_group_list):
            mlag_group_list.append(device['mlag_group'])
    return mlag_group_list

class MlagGroupsExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["mlag_groups"] = mlag_groups
