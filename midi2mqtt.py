import mido
import paho.mqtt.client as mqtt

MIDI_DEVICE_NAME = "<your midi device name>"   # or partial match, e.g. "Launchkey"
MQTT_BROKER_HOST = "<ip of MQTT broker>"
MQTT_BROKER_PORT = 1883
MQTT_USERNAME = "<your mqtt user>"
MQTT_PASSWORD = "<your mqtt password>"
client_id = "HASS" # default for Home Assistant MQTT 
client = mqtt.Client(client_id=client_id)

MQTT_TOPIC_PREFIX = "midi2mqtt"

def main():
    # 1) Find and open the MIDI input
    input_name = None
    for name in mido.get_input_names():
        if MIDI_DEVICE_NAME in name:
            input_name = name
            break
    
    if not input_name:
        print(f"Error: Could not find MIDI device containing '{MIDI_DEVICE_NAME}'")
        print("Available devices:")
        for name in mido.get_input_names():
            print(" ", name)
        return

    print(f"Using MIDI input: {input_name}")
    midi_in = mido.open_input(input_name)

    # 2) Connect to MQTT
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    client.loop_start()
    print(f"Connected to MQTT broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")

    # 3) Listen forever
    print("Listening for MIDI messages... Press Ctrl+C to exit.")
    try:
        for msg in midi_in:
            # For example, msg.type == 'note_on', 'note_off', 'control_change', etc.
            if msg.type in ('note_on', 'note_off'):
                topic = f"{MQTT_TOPIC_PREFIX}/note/{msg.note}"
                # We can publish velocity or 1 for 'on', 0 for 'off'
                payload = msg.velocity if msg.type == 'note_on' else 0
                client.publish(topic, payload)
                print(f"Published to {topic}: {payload}")

            elif msg.type == 'control_change':
                topic = f"{MQTT_TOPIC_PREFIX}/cc/{msg.control}"
                payload = msg.value
                client.publish(topic, payload)
                print(f"Published to {topic}: {payload}")
                
            # You can expand this to handle pitchwheel, aftertouch, etc.
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == '__main__':
    main()
