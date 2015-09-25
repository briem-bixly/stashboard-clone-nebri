class stashboard_trigger_up(NebriOS):
    listens_to = ['running']
    
    def check(self):
        return self.running == True and \
               self.kind == 'servicestatus' and \
               self.alerted == False
    
    def action(self):
        message = "%s service has come back online with status %s" % (self.service.name, self.status_string)
        send_email("example@example.com", message)
