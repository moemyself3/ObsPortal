# ObsPortal - Observatory Portal ✨

ObsPortal is a self contained observatory control and management system.
The client is a web-based UI using Django. The control system implements 
[ASCOMInitiative/alpyca](https://github.com/ASCOMInitiative/alpyca) a Python
client for [ASCOM Alpaca API](https://ascom-standards.org/Developer/Alpaca.htm).

## Planned Features

- [x] Register and manage devices
- [ ] Dashboard
- [ ] Manual control of devices
- [ ] Automated Routines
- [ ] Scheduler
- [ ] Image Viewer
- [ ] More...

## Known Issues

### During Installation

We use [ASCOMInitiative/alpyca](https://github.com/ASCOMInitiative/alpyca)
 which relies on the [al45stair/netifaces](https://github.com/al45tair/netifaces)
 for network calls using alpaca's discovery feature. During install netifaces
will attempt to build wheels which depend on C++14. Unless your environment
already has it, you will experience an error.

## Considerations

#### Django's Development Server

As per Django [Documentation](https://docs.djangoproject.com/en/4.1/ref/django-admin/#django-admin-runserver)
> DO NOT USE THIS SERVER IN A PRODUCTION SETTING. It has not gone through security audits or performance tests. (And that’s how it’s gonna stay. We’re in the business of making web frameworks, not web servers, so improving this server to be able to handle a production environment is outside the scope of Django.)

[How to deploy Django](https://docs.djangoproject.com/en/4.1/howto/deployment/)


#### Authentication

Based on the previous section you should consider safe network practices.
This project is currently planned to be used in a sterile environment with no access to internet.
(Plans to include roles and authentication may come soon.)
