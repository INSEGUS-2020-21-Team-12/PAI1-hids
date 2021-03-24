#!pip install cryptography
from cryptography.hazmat.primitives.asymmetric import rsa
import sys
import random

def rsadata():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048)
    private_euler_function = (private_key.private_numbers().p-1)*(private_key.private_numbers().q-1)
    public_n_modulo = (private_key.private_numbers().p)*(private_key.private_numbers().q)
    return private_key, private_euler_function, public_n_modulo

# Interpretar los bytes de un fichero como un integer
def filebytes_to_int(input_filename):
  with open(input_filename,'rb') as ifile:
        data = ifile.read()
  return int.from_bytes(data,byteorder=sys.byteorder)

def hmorph_rsa_hash(input_filename, private_euler_function):
  data_int = filebytes_to_int(input_filename)
  return data_int % private_euler_function

def pdp_request(input_filename, n, hmorph_rsa_hash):
  # Se excluyen los primeros y ultimos n/10, de forma arbitraria
  b = random.randint(1, n-1)
  expected_result = pow(b, hmorph_rsa_hash, n)
  return b, n, expected_result

def pdp_response(input_filename,b, n):
  # Se excluyen los primeros y ultimos n/10, de forma arbitraria
  file_intbytes = filebytes_to_int(input_filename)
  pdp_result = pow(b, file_intbytes, n)
  return pdp_result