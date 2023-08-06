import logging

def login(instance, user, password):
  base_url = f'https://{instance}.alationcloud.com'
  logging.debug(f'using base url: {base_url}')
  logging.debug(f'user: {user}')
  
