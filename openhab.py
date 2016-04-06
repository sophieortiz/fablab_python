self.openhab_host = localhost
self.openhab_port = localport


def post_command(self, key, value):
    """ Post a command to OpenHAB - key is item, value is command """
    url = 'http://%s:%s/rest/items/%s'%(self.openhab_host,
                                self.openhab_port, key)
    req = requests.post(url, data=value,
                            headers=self.basic_header())
    if req.status_code != requests.codes.ok:
        req.raise_for_status()



def put_status(self, key, value):
    """ Put a status update to OpenHAB  key is item, value is state """
    url = 'http://%s:%s/rest/items/%s/state'%(self.openhab_host,
                                self.openhab_port, key)
    req = requests.put(url, data=value, headers=self.basic_header())
    if req.status_code != requests.codes.ok:
        req.raise_for_status()     

def get_status(self, name):
    """ Request updates for any item in group NAME from OpenHAB.
     Long-polling will not respond until item updates.
    """
    # When an item in Group NAME changes we will get all items in the group 
    # and need to determine which has changed
    url = 'http://%s:%s/rest/items/%s'%(self.openhab_host,
                                    self.openhab_port, name)
    payload = {'type': 'json'}
    try:
        req = requests.get(url, params=payload,
                            headers=self.polling_header())
        if req.status_code != requests.codes.ok:
            req.raise_for_status()
        # Try to parse JSON response
        # At top level, there is type, name, state, link and members array
        members = req.json()["members"]
        for member in members:
            # Each member has a type, name, state and link
            name = member["name"]
            state = member["state"]
            do_publish = True
            # Pub unless we had key before and it hasn't changed
            if name in self.prev_state_dict:
                if self.prev_state_dict[name] == state:
                    do_publish = False
            self.prev_state_dict[name] = state
            if do_publish:
                self.publish(name, state)

def basic_header(self):
    """ Header for OpenHAB REST request - standard """
    self.auth = base64.encodestring('%s:%s'
                       %(self.username, self.password)
                       ).replace('\n', '')
    return {
            "Authorization" : "Basic %s" %self.auth,
            "Content-type": "text/plain"}


