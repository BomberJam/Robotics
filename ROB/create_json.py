import pypot.dynamixel
import json

if __name__ == '__main__':

    with open('ergo.json', 'w') as f:
        rob = pypot.dynamixel.autodetect_robot()
        config = rob.to_config()

        json.dump(config, f, indent=2)

        rob.close()