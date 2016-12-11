import os
import json
import logging
from tornado import ioloop, web

from . import decipher, translator


class HtmlHandler(web.RequestHandler):
    """
    Web request handler for the root directory. Returns the index.html page.
    """

    def data_received(self, chunk):
        pass

    def get(self):
        """
        Returns the index.html page.

        :return: index.html
        """
        print("New frontend page opened")
        return self.render("static/index.html")


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
        language = self.get_argument(name="language")
        return_cipher = self.get_argument(name="cipher", default=False) == 'on'
        return_original = self.get_argument(name="original", default=False) == 'on'

        print("Received input text: {0}".format(input_text))

        # Using the decipher class, decipher the text received
        cipher = decipher.calc_cipher(text=input_text, language=language)
        output_text = translator.decipher_text(text=input_text, cipher=cipher)

        result_dict = {'output_text': output_text}
        if return_cipher:
            result_dict['cipher'] = cipher
        if return_original:
            result_dict['input_text'] = input_text

        self.finish(json.dumps(result_dict))


def make_app():
    """
    Creates the application object with the endpoints for root and database queries.

    :return: tornado application object
    """
    routes = [
        (r"/", HtmlHandler),
        (r"/decipher", DecipherHandler)
    ]
    return web.Application(routes,
                           static_path=os.path.join(os.path.dirname(__file__), "static"),
                           debug=True)


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
