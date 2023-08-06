# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hue2mqtt', 'hue2mqtt.mqtt']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'aiohue>=2.5.1,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'gmqtt>=0.6.10,<0.7.0',
 'pydantic>=1.9.2,<2.0.0']

extras_require = \
{':python_version <= "3.10"': ['tomli>=2.0.1,<3.0.0']}

entry_points = \
{'console_scripts': ['hue2mqtt = hue2mqtt.app:app']}

setup_kwargs = {
    'name': 'hue2mqtt',
    'version': '0.4.0',
    'description': 'Python Hue to MQTT Bridge',
    'long_description': '# Hue2MQTT\n\nPython Hue to MQTT Bridge\n\n## What and Why?\n\nHue2MQTT lets you control your Hue setup using MQTT and publishes the current state in real-time.\n\n- Python 3.8+ with type hints and asyncio\n- Uses the excellent [aiohue](https://github.com/home-assistant-libs/aiohue) library to communicate with Hue.\n- Control your lights using MQTT\n- Receive live events (i.e button pushes, motion sensors) in real-time.\n- No polling your Hue Bridge for changes\n- IPv6 Support\n\n## Configuration\n\nHue2MQTT is configured using `hue2mqtt.toml`.\n\n```toml\n# Hue2MQTT Default Config File\n\n[mqtt]\nhost = "::1"\nport = 1883\nenable_tls = false\nforce_protocol_version_3_1 = true\n\nenable_auth = false\nusername = ""\npassword = ""\n\ntopic_prefix = "hue2mqtt"\n\n[hue]\nip = "192.0.2.2"  # or IPv6: "[2001:db0::1]"\nusername = "some secret here"\n```\n\nIf you do not know the username for your bridge, find it using `hue2mqtt --discover`.\n\n## Running Hue2MQTT\n\nUsually, it is as simple as running `hue2mqtt`.\n\n```\nUsage: hue2mqtt [OPTIONS]\n\n  Main function for Hue2MQTT.\n\nOptions:\n  -v, --verbose\n  -c, --config-file PATH\n  --discover\n  --help                  Show this message and exit.\n```\n\n## Bridge Status\n\nThe status of Hue2MQTT is published to `hue2mqtt/status` as a JSON object:\n\n```json\n{"online": true, "bridge": {"name": "Philips Hue", "mac_address": "ec:b5:fa:ab:cd:ef", "api_version": "1.45.0"}}\n```\n\nIf `online` is `false`, then all other information published by the bridge should be assumed to be inaccurate.\n\nThe `bridge` object contains information about the Hue Bridge, if available.\n\n## Getting information about Hue\n\nInformation about the state of Hue is published to MQTT as retained messages. Messages are re-published when the state changes.\n\n### Lights\n\nInformation about lights is published to `hue2mqtt/light/{{UNIQUEID}}` where `UNIQUEID` is the Zigbee MAC of the light.\n\ne.g `hue2mqtt/light/00:17:88:01:ab:cd:ef:01-02`\n\n```json\n{"id": 1, "name": "Lounge Lamp", "uniqueid": "00:17:88:01:ab:cd:ef:01-02", "state": {"on": false, "alert": "none", "bri": 153, "ct": 497, "effect": "none", "hue": 7170, "sat": 225, "xy": [0, 0], "transitiontime": null, "reachable": true, "color_mode": null, "mode": "homeautomation"}, "manufacturername": "Signify Netherlands B.V.", "modelid": "LCT012", "productname": "Hue color candle", "type": "Extended color light", "swversion": "1.50.2_r30933"}\n\n```\n\n### Groups\n\nA group represents a group of lights, referred to as Rooms and Zones in the Hue app.\n\nInformation about lights is published to `hue2mqtt/group/{{GROUPID}}` where `GROUPID` is an integer.\n\n```json\nhue2mqtt/group/3 {"id": 3, "name": "Lounge", "lights": [24, 21, 20, 3, 5], "sensors": [], "type": "Room", "state": {"all_on": false, "any_on": false}, "group_class": "Living room", "action": {"on": false, "alert": "none", "bri": 153, "ct": 497, "effect": "none", "hue": 7170, "sat": 225, "xy": [0, 0], "transitiontime": null, "reachable": null, "color_mode": null, "mode": null}}\n```\n\n### Sensors\n\nSensors represent other objects in the Hue ecosystem, such as switches and motion sensors. There are also a number of "virtual" sensors that the Hue Hub uses to represent calculated values (e.g `daylight`), but these are ignored by Hue2MQTT.\n\nInformation about sensors is published to `hue2mqtt/sensor/{{UNIQUEID}}` where `UNIQUEID` is the Zigbee MAC of the device.\n\ne.g `hue2mqtt/sensor/00:17:88:01:ab:cd:ef:01-02`\n\n**Switch**\n\n```json\n{"id": 10, "name": "Lounge switch", "type": "ZLLSwitch", "modelid": "RWL021", "manufacturername": "Signify Netherlands B.V.", "productname": "Hue dimmer switch", "uniqueid": "00:17:88:01:ab:cd:ef:01-02", "swversion": "6.1.1.28573", "state": {"lastupdated": "2021-07-10T11:37:58", "buttonevent": 4002}, "capabilities": {"certified": true, "primary": true, "inputs": [{"repeatintervals": [800], "events": [{"buttonevent": 1000, "eventtype": "initial_press"}, {"buttonevent": 1001, "eventtype": "repeat"}, {"buttonevent": 1002, "eventtype": "short_release"}, {"buttonevent": 1003, "eventtype": "long_release"}]}, {"repeatintervals": [800], "events": [{"buttonevent": 2000, "eventtype": "initial_press"}, {"buttonevent": 2001, "eventtype": "repeat"}, {"buttonevent": 2002, "eventtype": "short_release"}, {"buttonevent": 2003, "eventtype": "long_release"}]}, {"repeatintervals": [800], "events": [{"buttonevent": 3000, "eventtype": "initial_press"}, {"buttonevent": 3001, "eventtype": "repeat"}, {"buttonevent": 3002, "eventtype": "short_release"}, {"buttonevent": 3003, "eventtype": "long_release"}]}, {"repeatintervals": [800], "events": [{"buttonevent": 4000, "eventtype": "initial_press"}, {"buttonevent": 4001, "eventtype": "repeat"}, {"buttonevent": 4002, "eventtype": "short_release"}, {"buttonevent": 4003, "eventtype": "long_release"}]}]}}\n```\n\n**Light Sensor**\n\n```json\n{"id": 5, "name": "Hue ambient light sensor 1", "type": "ZLLLightLevel", "modelid": "SML001", "manufacturername": "Signify Netherlands B.V.", "productname": "Hue ambient light sensor", "uniqueid": "00:17:88:01:04:b7:b5:20-02-0400", "swversion": "6.1.1.27575", "state": {"lastupdated": "2021-07-10T12:28:17", "dark": true, "daylight": false, "lightlevel": 14606}, "capabilities": {"certified": true, "primary": false}}\n```\n\n## Controlling Hue\n\nLights and Groups can be controlled by publishing objects to the `hue2mqtt/light/{{UNIQUEID}}/set` or `hue2mqtt/group/{{GROUPID}}/set` topics.\n\nThe object should be a JSON object containing the state values that you wish to change.\n\n```json\n{"on": "true"}\n```\n\n## Docker\n\nIncluded is a basic Dockerfile and docker-compose example. \n\n## Contributions\n\nThis project is released under the MIT Licence. For more information, please see LICENSE.\n\nThe CONTRIBUTORS file can be generated by executing CONTRIBUTORS.gen. This generated file contains a list of people who have contributed to Hue2MQTT.\n\n',
    'author': 'Dan Trickey',
    'author_email': 'contact@trickey.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trickeydan/hue2mqtt-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
