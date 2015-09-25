from nebriosmodels import NebriOSModel, NebriOSField, NebriOSReference
import requests


class Service(NebriOSModel):
    name = NebriOSField(required=True)
    description = NebriOSField()
    date_added = NebriOSField(required=True)

    def current_status(self):
        try:
            statuses = ServiceStatus.filter(service=self)
            statuses.sort(key=lambda x: x.date_added)
            return statuses[0].status
        except:
            return None

    def get_last_4_days(self):
        try:
            to_return = []
            today = datetime.now().replace(hour=23, minute=59, second=59)
            check_date_end = today - timedelta(days=1)
            check_date_start = check_date_end.replace(hour=0, minute=0, second=0)
            for _ in range(4):
                statuses = ServiceStatus.filter(service=self, date_added__gte=check_date_start, date_added__lte=check_date_end)
                found_down = False
                found_up = False
                message = 'up'
                if len(statuses) == 0:
                    to_return.append({
                        'date': check_date_start.date().isoformat(),
                        'message': 'no data'
                    })
                else:
                    for s in statuses:
                        if s.running == True:
                            found_up = True
                        else:
                            found_down = True
                    if found_up and found_down:
                        message = 'warning'
                    if not found_up and found_down:
                        message = 'down'
                    to_return.append({
                        'date': check_date_start.date().isoformat(),
                        'message': message
                    })
                check_date_end = check_date_start - timedelta(seconds=1)
                check_date_start = check_date_start - timedelta(days=1)
            return to_return
        except Exception as e:
            return str(e)

    def get_json(self):
        return {'name': self.name,
                'description': self.description,
                # make sure to make your dates JSON serializable
                'date_added': self.date_added.isoformat(),
                'current_status': self.current_status()}

    def is_url(self):
        try:
            requests.get(self.name)
            return True
        except:
            return False


class ServiceStatus(NebriOSModel):
    service = NebriOSReference(Service, required=True)
    status_string = NebriOSField(required=True, default='up')
    running = NebriOSField(required=True, default=False)
    description = NebriOSField()
    date_added = NebriOSField(required=True)
    alerted = NebriOSField(required=True, default=False)

    def get_json(self):
        return {'status': self.status_string,
                'description': self.description,
                'running': self.running,
                # make sure your dates are JSON serializable
                'date_added': self.date_added.isoformat()}
