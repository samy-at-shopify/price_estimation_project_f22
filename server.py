# standard library dependencies
import json
import time
import pickle
import logging
from sys import argv
from random import uniform
from pprint import pformat
from typing import Mapping, Any, Tuple
from http.server import BaseHTTPRequestHandler, HTTPServer


class PriceSuggestor:
  def __init__(self, path_to_serialized_assets: str):
    try:
      self.__load(path_to_serialized_assets)
    except NotImplementedError:
      print(f"Still in development; using fake data generator for now...\n")

  def __load(self, filepath: str):
    raise NotImplementedError
    with open(filepath, "rb") as handle:
      self.__assets = pickle.load(handle, protocol=pickle.HIGHEST_PROTOCOL)

  def __get_n_most_similar_products_prices(self, product_of_interest: Mapping[str,Any], n: int = 30):
    return [ uniform(100,150) for _ in range(n) ]

  def __get_suggested_price(self, product_of_interest: Mapping[str,Any]) -> Mapping[str,float]:
    return {
      "suggested_price": 123.45,
      "range_around_suggested_price": 0.97,
    }

  def suggest(self,
              product_of_interest: Mapping[str,Any],
              number_of_most_similar_products: int = 30):
    time.sleep(3)
    response = {
      "similar_product_prices": self.__get_n_most_similar_products_prices(
        product_of_interest,
        number_of_most_similar_products
      ),
      **self.__get_suggested_price(
        product_of_interest
      )
    }
    return json.dumps(response)

class RequestHandler(BaseHTTPRequestHandler):
  def __init__(self, request, client_address, server):
    self.price_suggestor = PriceSuggestor("fake")
    super().__init__(request, client_address, server)

  def _set_response(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()

  def do_GET(self):
    message = f"Received GET request\nPath: {self.path}\nHeaders: {self.headers.as_string()}\n"
    logging.info(message)
    self._set_response()
    self.wfile.write(json.dumps({"message": message}).encode("utf-8"))

  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    POST_data = self.rfile.read(content_length)
    logging.info(f"Received POST request\nPath: {self.path}\nHeaders: {self.headers.as_string()}\nBody: {pformat(POST_data.decode('utf-8'))}\n")
    self._set_response()
    POST_parameters = {
      "product_of_interest": {
        "is fake?": True,
         "features": {
          "feature 1": "foo",
          "feature 2": "bar"
        }
      },
      "number_of_most_similar_products": 30
    }
    suggestion = self.price_suggestor.suggest(
      POST_parameters["product_of_interest"],
      POST_parameters["number_of_most_similar_products"]
    )
    self.wfile.write(suggestion.encode("utf-8"))

def run(server_ip_address: str = "127.0.0.1", server_port: int = 8080):
  logging.basicConfig(level=logging.INFO)
  logging.info(f"Starting server at {server_ip_address}:{server_port} ...\n")
  server = HTTPServer(
    (server_ip_address, server_port),
    RequestHandler
  )
  logging.info(f"Server is running at {server_ip_address}:{server_port}\n")
  print_help_message(server_ip_address=server_ip_address, server_port=server_port)
  logging.info("(Use Control+C to shut down the server)")
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    logging.info("Stopping server...\n")
  server.server_close()

def print_help_message(server_ip_address: str = "127.0.0.1", server_port: int = 8080):
  message = f"Use the following commands to test the server (while it is running):\n\t"
  GET_command = f"For a GET request, use:\n\tcurl --location --request GET '{server_ip_address}:{server_port}'"
  POST_command = "For a POST request, use:\n\t" + \
  "curl --location --request POST '127.0.0.1:8080' --header 'Content-Type: application/json' --data-raw '{" + \
  '"foo": "bar"' + "}'"
  print(f"\n{message}\n{GET_command}\n\n{POST_command}\n\n")

if __name__ == "__main__":
  if len(argv) == 1:
    run()
  if len(argv) == 2:
    run(server_ip_address=argv[1])
  elif len(argv) == 3:
    run(server_ip_address=argv[1], server_port=int(argv[2]))
  else:
    print(f"\nInvalid input.")
    print(f"Launch the server by using the following command:")
    print(f"\tpython <path-to-server.py> <server-ip-address> <port>")
    print(f"e.g.:\tpython server.py 127.0.0.1 8080\n")
