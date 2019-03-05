# a quick and dirty way to store user values
import general
import json

# the cvar key is the cvar we use to store any data in
CVAR_KEY = "ca_CharEditModel"


class UserValues(object):
    """
	User Values are ephemeral values that can be read and changed at run time, but may not always store
	"""

    def __init__(self, cvar_key=CVAR_KEY, init_funcs=[]):
        super(UserValues, self).__init__()
        self.cvar_key = cvar_key
        self.bootstrap(init_funcs)

    def bootstrap(self, init_funcs):
        try:
            # if it fails to get all it's because it's not json or something is wrong reset it
            self.get_all()
        except ValueError:
            # set some basic initialized json data
            general.set_cvar(self.cvar_key, json.dumps({"initialized": True}))
            for func in init_funcs:
                func()

    def get(self, key):
        values = json.loads(general.get_cvar(self.cvar_key))
        try:
            return values[key]
        except KeyError:
            return None

    def set(self, key, value):
        user_values = self.get_all()
        user_values[key] = value
        return general.set_cvar(self.cvar_key, json.dumps(user_values))

    def delete(self, key):
        user_values = self.get_all()
        del user_values[key]
        return general.set_cvar(self.cvar_key, json.dumps(user_values))

    def get_all(self):
        return json.loads(general.get_cvar(self.cvar_key))
