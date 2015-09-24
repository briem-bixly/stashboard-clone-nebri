from nebriosmodels import NebriOSModel, NebriOSField, NebriOSReference


class Service(NebriOSModel):
    name = NebriOSField(required=True)
    description = NebriOSField()
    date_added = NebriOSField(required=True)

    def current_status(self):
        try:
            statuses = ServiceStatus.filter(service=self)
            statuses.sort(key=lambda x: x.date_added, reverse=True)
            return statuses[0].status
        except:
            return None

    def get_json(self):
        return {'name': self.name,
                'description': self.description,
                # make sure to make your dates JSON serializable
                'date_added': self.date_added.isoformat(),
                'current_status': self.current_status()}


class ServiceStatus(NebriOSModel):
    service = NebriOSReference(Service, required=True)
    status_string = NebriOSField(required=True, default='up')
    running = NebriOSField(required=True, default=True)
    description = NebriOSField()
    date_added = NebriOSField(required=True)
    alerted = NebriOSField(required=True, default=False)

    def get_json(self):
        return {'status': self.status_string,
                'description': self.description,
                'running': self.running,
                # make sure your dates are JSON serializable
                'date_added': self.date_added.isoformat()}
