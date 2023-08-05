import json
import websocket


class Messages():
    op_codes = {
            "loopback": 0,
            "get_mplab_path": 1,
            "open_notebook": 2,
            "open_link": 3,
            "file_upload": 11,
            "text_box": 12,
            "dropdown": 13,
            "open_explorer": 14,
            "messagebox": 18
        }

    # msg_schema = {"msg_id": "int", "parameters": ["string"]}
    def encode(self, op_code: str, args: list):
        message = {
            'msg_id': self.op_codes.get(op_code, 'loopback'),
            'parameters': args}
        return json.dumps(message)


class Client():
    def __init__(self, parent, recv_handler=None):
        self.client = websocket.WebSocket(
                            on_error = self.error,
                            on_close = self.close)
        self.client.connect("ws://127.0.0.1:1302/")

    def error(self, error_code):
        print("error code: {}".format(error_code))
        print(self.client.errorString())

    def close(self):
        print("close - exiting")
        self.client.close()

    def send_message(self, op_code, args: list):
        msg = Messages()
        message = msg.encode(op_code, args)
        self.client.send(message)


if __name__ == '__main__':
    # Server must be running before this application starts sending
    # requests
    pass
