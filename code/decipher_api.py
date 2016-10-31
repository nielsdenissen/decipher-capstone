import json
import logging
from tornado import ioloop, web


class DecipherHandler(web.RequestHandler):
    """
    Web request handler for the deciphering of text.
    """

    def data_received(self, chunk):
        pass

    async def get(self):
        """
        Assumes one argument (text).
        Deciphers this text and returns the result.

        :return: json with result and original text.
        """
        # Parse the arguments
        input_text = self.get_argument(name="text")
        print("Received input text: {0}".format(input_text))

        output_text = input_text

        self.finish(json.dumps({'input_text': input_text, 'output_text': output_text}))


def make_app():
    """
    Creates the application object with the endpoints for root and database queries.

    :return: tornado application object
    """
    routes = [
        (r"/decipher", DecipherHandler)
    ]
    return web.Application(routes, debug=True)


def init(port):
    """
    Initialize and start the decipher app.

    :param port: port to run app on
    :return: -
    """
    # Disable the default loggers for tornado:
    logging.getLogger('tornado.access').addHandler(logging.NullHandler())
    logging.getLogger('tornado.application').addHandler(logging.NullHandler())
    logging.getLogger('tornado.general').addHandler(logging.NullHandler())

    # Start the tornado application and broadcast over the specified port:
    app = make_app()

    # Create instance of the asynchronous loop
    mainloop = ioloop.IOLoop.instance()

    # Start the tornado app
    print("Run the application on port {0}".format(port))
    app.listen(port=port, address="0.0.0.0")
    mainloop.start()
