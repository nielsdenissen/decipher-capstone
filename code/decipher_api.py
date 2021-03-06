import os
import json
import logging
from tornado import ioloop, web

from code.decipher.solver import Solver
from code import translator


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
        logging.info("New frontend page opened")
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

        if language == 'detect':
            cipher = None
            perc_correct = -1

            for l in ('en', 'nl', 'de'):
                cipher_new, perc_correct_new = self.application.solvers[l].solve(msg_enc=input_text)
                if perc_correct_new > perc_correct:
                    perc_correct = perc_correct_new
                    cipher = cipher_new
        else:
            # Using the decipher class, decipher the text received
            try:
                solver = self.application.solvers[language]
            except KeyError:
                solver = Solver(language=language)
            cipher, perc_correct = solver.solve(msg_enc=input_text)

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
    # Start the tornado application and broadcast over the specified port:
    app = make_app()
    app.solvers = dict()

    to_preload = ('en', 'nl', 'de')

    logging.info("Start preloading languages: {}".format(to_preload))
    count = 1
    for l in to_preload:
        logging.info("- loading ({}/{}): {}".format(count, len(to_preload), l))
        app.solvers[l] = Solver(language=l, logger=root_logger)
        count += 1

    # Create instance of the asynchronous loop
    mainloop = ioloop.IOLoop.instance()

    # Start the tornado app
    logging.info("Run the application on port {0}".format(port))
    app.listen(port=port, address="0.0.0.0")
    mainloop.start()


if __name__ == '__main__':
    # Disable the default loggers for tornado:
    logging.getLogger('tornado.access').addHandler(logging.NullHandler())
    logging.getLogger('tornado.application').addHandler(logging.NullHandler())
    logging.getLogger('tornado.general').addHandler(logging.NullHandler())

    log_formatter = logging.Formatter("%(asctime)s %(threadName)s %(levelname)s %(message)s")
    root_logger = logging.getLogger()

    root_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

    logging.info("--- Initialize the application. ---")
    init(8080)
