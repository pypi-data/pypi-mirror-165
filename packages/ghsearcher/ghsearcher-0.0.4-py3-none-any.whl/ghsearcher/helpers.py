"""
Helper functions/classes for ghdorker
"""
from datetime import datetime, date
from time import sleep
import json
import logging

logger = logging.getLogger("debug")

class Limit():
  """A class for handling single endpoint limits

  Parameters:
  limit (int): Max number of requests
  remaining (int): Number of remaining allowable calls
  reset (datetime): When the limit resets
  used (int): Number of calls used so far
  resource (str): Name of the endpoint
  """
  def __init__(self, limit, remaining, reset, used, resource):
    self.limit = limit
    self.remaining = remaining
    self.reset = reset
    self.used = used
    self.resource = resource

  def step(self):
    """Iterate the counters"""
    self.remaining = self.remaining -1
    self.used = self.used + 1

  def __str__(self) -> str:
    return f"""\n
            limit: {self.limit}
            remaining: {self.remaining}
            reset: {self.reset}
            used: {self.used}
            resource: {self.resource}"""


class RateLimiter:
  """A class for ensuring rate limits are not exceeded

  Parameters:
  client (GHApi): A GHApi instance
  """
  def __init__(self, client):
    self.client = client
    self.initialize_limits()


  def get_rate_limits(self, endpoint: str) -> str:
    """Get the currently set rate limits for an endpoint"""
    rate_limit = getattr(self, endpoint)
    return str(rate_limit)


  def initialize_limits(self):
    """Populate limits from GitHub

    This will auto populate the class with limits objects
    based on the endpoints in GitHub. This way it can get
    real limits based off your currently used limits.s"""
    limits = self.client.rate_limit.get()
    for key, value in limits["resources"].items():
      setattr(self, key, Limit(**value))


  def check_safety(self, endpoint: str):
    """Checks the safety of making a call to github

    Return:
    There is no return value but it will pause for a short period to
    prevent overusing the endpoints."""
    rate_limit = getattr(self, endpoint)
    curr_time = datetime.now().timestamp()

    if curr_time < rate_limit.reset:
      sleep(((rate_limit.reset - curr_time) / rate_limit.remaining)+1)
    else:
      self.initialize_limits()

    rate_limit.step()


def output_json_file(file, data):
  """Helper function to output data to JSON file

  Parameters:
  file_path: File Path and Name
  data: JSON Serializable Data

  Returns:
  None
  """
  with open(f"{file}-{date.today()}.json", "+w") as f:
    json.dump(data, f)


def paginator(operation, per_page=30, page=1, **kwargs):
  """Helper function for paginating requests

  Parameters:
  operation (GHapi Function): The fuction you would like to paginate requests from
  per_page (int): Number of results per page (some endpoints have a 30 max)
  page (int): Page to start on
  kwargs: any other arguments you would like to pass to the funtion (eg. q=Query)

  Returns:
  Attribute Dict: A list of dictionary objects containing the results returned
  """
  out_of_items = False
  while not out_of_items:
    result = operation(**kwargs, per_page=per_page, page=page)
    if len(result['items']) != 0:
      yield result
      page += 1
    else: out_of_items = True
