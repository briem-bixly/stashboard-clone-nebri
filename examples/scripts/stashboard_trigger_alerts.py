class stashboard_trigger_alerts(NebriOS):
    listens_to = ['running']
    
    def check(self):
        return self.running is False and \
               self.kind == 'servicestatus' and \
               self.alerted is False
               
    def action(self):
        message = "%s service is down with status %s" % (self.service.name, self.status_string)
        send_email("example@example.com", message)
