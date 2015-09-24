import requests

class stashboard_check_site_status(NebriOS):
    listens_to = ['do_monitor']

    def check(self):
        return self.do_monitor == True and \
               self.is_url() == True

    def action(self):
        try:
            response = requests.get(self.name, timeout=240, allow_redirects=True)
            if 200 <= response.status_code < 300:
                self.running = True
                self.status_string = 'up'
            else:
                self.running = False
                self.status_string = 'down'
        except:
            # either we reached our timeout, or the url isn't appropriate
            self.running = False
            self.status_string = 'down'
        # for debouncing purposes
        self.do_monitor = False
