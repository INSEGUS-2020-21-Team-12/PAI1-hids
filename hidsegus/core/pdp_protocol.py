# Provable Data Protection Protocol
import random
#from resource import *
from cryptography.hazmat.primitives.asymmetric import rsa
from hidsegus.core import utils

def rsa_hash(filepath, key_bitsize=2048):
  """Calculates the homomorphic hash of a file generating first a secure RSA private key
  
  Parameters
  ----------
      filepath : str
          The path to the file we want to calculate the homomorphic hash to
      key_bitsize : int
          The size of the private RSA-key (default=2048)
  Returns
  -------
      file_hmorph_hash : int
          A private homomorphic hash used to generate PDP requests for a file
      n_modulo : int
          N module for a PDP challenge"""
  if key_bitsize is None: key_bitsize = 2048

  private_key = rsa.generate_private_key(public_exponent=65537,key_size=key_bitsize)
      
  p_prime = private_key.private_numbers().p
  q_prime = private_key.private_numbers().q
      
  n_modulo = private_key.public_key().public_numbers().n
  euler_function = (p_prime -1)*(q_prime -1)

  hmorph_hash = utils.hmorph_rsa_hash(filepath, euler_function)
  return hmorph_hash, n_modulo


def request(n_modulo):
  """Calculates expected result of a PDP challenge based on a randomly generated b_token
  
  Parameters
  ----------
      n_modulo : int
          N module for the PDP challenge
      hmorph_hash : int
          A private homomorphic hash used compute easily a PDP challenge
  Returns
  -------
      b_token : int
          A randomly generated token for the PDP challenge
      n_modulo : int
          N module for the PDP challenge
      expected_result : int
          Expected result for the PDP challenge calculated with the hmorph_hash"""
  b_token = random.randint(1, n_modulo-1)
  return b_token, n_modulo

def response(filepath, b_token, n_modulo):
  """Calculates a PDP challenge for a file based on a random B token and a N module operation
  
  Parameters
  ----------
      filepath : str
          The path to the file we want to calculate the homomorphic hash to
      b_token : int
          A randomly generated token for the PDP challenge
      n_modulo : int
          N module for the PDP challenge
  Returns
  -------
      pdp_result : int
          The result of computing the PDP challenge"""
  # Se excluyen los primeros y ultimos n/10, de forma arbitraria
  file_intbytes = utils.filebytes_to_int(filepath)
  print('[pdp_response] pow(b, file_intbytes, n)...')
  pdp_result = pow(b_token, file_intbytes, n_modulo)
#   print(f'CPU execution time: {getrusage(RUSAGE_SELF).ru_utime}')
#   print(f'Memory size (unshared): {getrusage(RUSAGE_SELF).ru_idrss}')
#   print(f'Memory size (shared): {getrusage(RUSAGE_SELF).ru_ixrss}')
  return pdp_result

def verification(b_token, hmorph_hash, n_modulo):
    pdp_expected_result = pow(b_token, hmorph_hash, n_modulo)
    return pdp_expected_result


def pdp_test(input_filename):
    print(f'Testing PDP-Protocol for file: {input_filename}')
    
    file_hmorph_hash, public_n_modulo = rsa_hash(input_filename)

    pdp_request_b, pdp_request_n = request(public_n_modulo)
    pdp_expected_result = verification(pdp_request_b, file_hmorph_hash, public_n_modulo)

    print(f'Expected result: {pdp_expected_result}')

    print(f'Calculating response result... (This might take a while)')
    pdp_response_result = response(input_filename, pdp_request_b, pdp_request_n)
    
    print(f'Result: {pdp_response_result}')
    print(f'Are they equal?: {pdp_response_result == pdp_expected_result}')

if __name__ == '__main__':
    pdp_test('sampledir/PAI-1-integridad.pdf')


