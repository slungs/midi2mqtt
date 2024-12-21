# midi2mqtt
A simple script for sending midi inputs as MQTT events.

# Usage

Edit the configuration files with your ip, password etc.

Make sure you have Python installed.

Install dependencies:
`pip install mido python-rtmidi paho-mqtt`

Copy the script.

Go to the directory of the script and run `python midi2mqtt.py`. 

If configured correctly, you should see events in your MQTT broker on the `midi2mqtt` topic when pressing a key on the midi controller.


Video example:
https://github.com/user-attachments/assets/db4ea870-5b02-4d9a-adb1-434844715083

