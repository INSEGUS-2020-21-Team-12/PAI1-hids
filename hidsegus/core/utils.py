import mmap
import sys
import ntpath
def filebytes_to_int(filepath):
    """An RSA-based homomorphic hash function
    
    Parameters
    ----------
        filepath : str
            The path to the file we want to calculate the homomorphic hash to"""
    #print('[filebytes_to_int] Loding file into memory...')
    with open(filepath,'rb') as ifile:
        with mmap.mmap(ifile.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            data = mmap_obj.read()
    
    #print(f'CPU execution time: {getrusage(RUSAGE_SELF).ru_utime}')
    #print(f'Memory size (unshared): {getrusage(RUSAGE_SELF).ru_idrss}')
    #print(f'Memory size (shared): {getrusage(RUSAGE_SELF).ru_ixrss}')


    #print('[filebytes_to_int] Converting bytes to int...')
    file_int = int.from_bytes(data,byteorder=sys.byteorder)
    #print(f'CPU execution time: {getrusage(RUSAGE_SELF).ru_utime}')
    #print(f'Memory size (unshared): {getrusage(RUSAGE_SELF).ru_idrss}')
    #print(f'Memory size (shared): {getrusage(RUSAGE_SELF).ru_ixrss}')
    return file_int

def filename(filepath):
    head, tail = ntpath.split(filepath)
    return tail or ntpath.basename(head)

def generate_jsonfilename(filepath, file_prefix):
    head, tail = ntpath.split(filepath)
    res = f'{file_prefix}{str(0).zfill(2)}_{tail}.json'
    if ntpath.exists(res): 
        for n in range(100):
            res = f"{file_prefix}{str(n).zfill(2)}_{tail}.json"
            if not ntpath.exists(res):
                break

    return res

def dir_or_json(filepath):
    return npath.isdir(filepath) or filepath.endswith('.json')

def hmorph_rsa_hash(filepath, euler_function):
    """An RSA-based homomorphic hash function
    Parameters
    ----------
        filepath : str
            The path to the file we want to calculate the homomorphic hash to
        private_euler_function : int
            The euler function corresponding to (p-1)*(q-1) so p,q are secure primes for RSA
    Returns
    -------
        int
            A private homomorphic hash used to generate PDP requests for a file"""
    
    data_int = filebytes_to_int(filepath)
    return data_int % euler_function