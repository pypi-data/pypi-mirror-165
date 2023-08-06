# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaeb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'yaeb',
    'version': '0.3.0',
    'description': 'A simple typed event bus written in pure python',
    'long_description': "\n# Yet another event bus - yaeb for short\n\nA simple typed event bus written in pure python\n\n\n## Installation\n\nInstall yaeb with pip\n\n```bash\n  pip install yaeb\n```\n    \n## Usage/Examples\n\n```python\nfrom logging import info\n\nfrom yaeb.bus import EventBus, NonPersistentEventHandlerRegistry\nfrom yaeb.interface import Event, EventBusInterface, EventHandler\n\n\nclass UserCreated(Event):\n    user_id: int\n\n    def __init__(self, user_id: int) -> None:\n        self.user_id = user_id\n\n\nclass UserCreatedHandler(EventHandler[UserCreated]):\n    def handle_event(self, event: UserCreated, bus: EventBusInterface) -> None:\n        info('User with id=%d was created!', event.user_id)\n\n\nif __name__ == '__main__':\n    bus = EventBus(event_handler_registry=NonPersistentEventHandlerRegistry())\n    bus.register(event_type=UserCreated, event_handler=UserCreatedHandler())\n\n    bus.emit(UserCreated(user_id=1))  # prints log message with created user id\n\n```\n\n\n## Roadmap\n\n- [x] Add coroutines support\n- [ ] Add some kind of multithreading support. Though it can be implemented by handlers themselves 🤔\n\n",
    'author': 'Daniil Fedyaev',
    'author_email': 'wintercitizen@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/WinterCitizen/yaeb',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
