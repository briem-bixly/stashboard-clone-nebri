from stashboardmodels import Service, ServiceStatus
import logging

logging.basicConfig(filename='stashboard.log', level=logging.DEBUG)


def get_info(service=None):
    logging.debug('get info')
    if service is None:
        # get info for all services
        return_data = []
        services = Service.filter()
        for service in services:
            statuses = ServiceStatus.filter(service=service)
            data = {'service': service.get_json(), 'statuses': []}
            for s in statuses:
                data['statuses'].append(s.get_json())
            return_data.append(data)
        logging.debug(return_data)
        return return_data
    else:
        service = Service.get(name=service)
        statuses = ServiceStatus.filter(service=service)
        return_data = {'service': service.get_json(), 'statuses': []}
        for s in statuses:
            return_data['service']['statuses'].append(s.get_json())
        return return_data


def set_status(data):
    logging.debug('enter set status')
    try:
        service = Service.get(name=data['service'])
        logging.debug(service)
        try:
            status = ServiceStatus(
                service=service,
                date_added=datetime.now(),
                description=data.get('description', ''),
                status=data['status']
            )
        except:
            status = ServiceStatus(
                service=service,
                date_added=datetime.now(),
                description=data.description,
                status=data.status
            )
        status.save()
        return 'Successfully Created'
    except Exception as e:
        logging.debug(str(e))
        return str(e)


def create_service(data):
    logging.debug('enter create service')
    logging.debug(type(data))
    try:
        try:
            service = Service(
                name=data['name'],
                description=data.get('description', ''),
                date_added=datetime.now()
            )
        except:
            service = Service(
                name=data.name,
                description=data.description,
                date_added=datetime.now()
            )
        service.save()
        logging.debug(service)
        return 'Successfully Created'
    except Exception as e:
        logging.debug(str(e))
        return str(e)
