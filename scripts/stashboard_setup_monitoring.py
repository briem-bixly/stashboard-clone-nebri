from stashboardmodels import Service


class stashboard_setup_monitoring(NebriOS):
    listens_to = ['stashboard_setup_monitoring']
    
    def check(self):
        return self.stashboard_setup_monitoring == True
        
    def action(self):
        all_services = Service.filter()
        for service in all_services:
            if service.is_url():
                service.do_monitor = True
                service.save()
