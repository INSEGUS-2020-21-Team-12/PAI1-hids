"""HIDSEGUS: A Host Intrusion Detection Systems made in python by INSEGUS ST 12 2020-21"""
import cmd2, functools
import argparse
import sys
import time
from hidsegus.core import pdp_json, utils, hids_runner

class HIDSegus(cmd2.Cmd):
    """HIDSEGUS: A Host Intrusion Detection Systems made in python by INSEGUS ST 12 2020-21"""
    
    prompt = 'HIDSEGUS >'
    PDP_PROTOCOL = '(PDP) Proof of Data Possesion'
    HIDS = '(HIDS) Host Intrusion Detection System'
    OTHER = 'Other'
    def __init__(self):
        """Initialize the base class as well as this one"""
        #shortcuts = dict(cmd2.DEFAULT_SHORTCUTS)
        #super().__init__(multiline_commands=[], terminators=[], shortcuts={})
        super().__init__()
        self.debug = True
        self.default_category = 'Built-in Commands'
        self.hidden_commands.extend(['alias','macro','shortcuts','edit','shell','history','py', 'run_pyscript', 'run_script'])
    
    # auto-complete
    complete_rsahash = cmd2.Cmd.path_complete
    complete_request = cmd2.Cmd.path_complete
    complete_proof = cmd2.Cmd.path_complete
    complete_verify = cmd2.Cmd.path_complete

    # ----- rsahash_parser for do_rsahash()
    rsahash_parser = arg_parser = argparse.ArgumentParser()
    rsahash_parser.add_argument('-k', '--keysize', type=int, help='key size in bits of the RSA private key')
    rsahash_parser.add_argument('-o', '--output', help='Output file path for the resulting .json')
    rsahash_parser.add_argument('filepath', type=str, help='file path to be hashed')
    
    @cmd2.with_category(PDP_PROTOCOL)
    @cmd2.with_argparser(rsahash_parser)
    def do_rsahash(self, args):
        """Generate a homomorphic hash of a file and store it as a .json"""
        # rsahash sampledir/PAI-1-integridad.pdf
        started_time = time.process_time()
        filepath = args.filepath
        keysize = args.keysize
        output = args.output

        self.stdout.write("\n")
        json_output = pdp_json.rsa_hash(filepath, output, keysize)
        self.stdout.write(f"Homomorphic hash generated for '{filepath}'.\n")
        self.stdout.write(f"Keep the '{json_output}' JSON-file private.\n")
        self.stdout.write("\n")
        elapsed_time = time.process_time() - started_time
        self.stdout.write(f"Executed in {elapsed_time:9.3f}s.\n")
        self.stdout.write(f"Generate a challenge with: \n   > request {json_output}\n")
        self.stdout.write("\n")

    # ----- request_parser for do_request()
    request_parser = arg_parser = argparse.ArgumentParser()
    request_parser.add_argument('-o', '--output', help='Output file path for the resulting .json')
    request_parser.add_argument('jsonfile', type=str, help='JSON file where the homomorphic hash is stored')

    @cmd2.with_category(PDP_PROTOCOL)
    @cmd2.with_argparser(request_parser)
    def do_request(self, args):
        """Generate a challenge to the server for a Proof of Data Possesion"""
        started_time = time.process_time()
        jsonfile = args.jsonfile
        output = args.output

        self.stdout.write("\n")
        json_output, filepath =  pdp_json.request(jsonfile, output)
        self.stdout.write(f"PDP request generated for file '{filepath}'.\n")
        self.stdout.write(f"Resquest file generated as '{json_output}'.\n")
        self.stdout.write("\n")
        elapsed_time = time.process_time() - started_time
        self.stdout.write(f"Executed in {elapsed_time:9.3f}s.\n")
        self.stdout.write(f"Solve the challenge with command: \n   > proof {json_output}\n")
        self.stdout.write("\n")

    # ----- request_parser for do_proof()
    proof_parser = arg_parser = argparse.ArgumentParser()
    proof_parser.add_argument('-o', '--output', help='Output file path for the resulting .json')
    proof_parser.add_argument('jsonfile', type=str, help='JSON file from a pdp_request')
    
    @cmd2.with_category(PDP_PROTOCOL)
    @cmd2.with_argparser(proof_parser)
    def do_proof(self, args):
        """Solve a challenge for a Proof of Data Possesion verification"""
        started_time = time.process_time()
        jsonfile = args.jsonfile
        output = args.output
        
        self.stdout.write("\n")
        self.stdout.write('Calculating pow(b, file_intbytes, n)\n')
        self.stdout.write('Please be patient...\n')
        json_output, filepath =  pdp_json.response(jsonfile, output)
        self.stdout.write(f"PDP response generated as '{json_output}'.\n")
        self.stdout.write("\n")
        elapsed_time = time.process_time() - started_time
        self.stdout.write(f"Executed in {elapsed_time:9.3f}s.\n")
        self.stdout.write(f"Verify the result: \n   > verify {json_output} {utils.filename(filepath)}.json\n")
        self.stdout.write("\n")

    # ----- verify_parser for do_verify()
    verify_parser = arg_parser = argparse.ArgumentParser()
    verify_parser.add_argument('json_pdp_response', type=str, help='JSON file from a pdp_response')
    verify_parser.add_argument('json_hashfile', type=str, help='JSON file where the homomorphic hash is stored')

    @cmd2.with_category(PDP_PROTOCOL)
    @cmd2.with_argparser(verify_parser)
    def do_verify(self, args):
        """Check the result of the Proof of Data Possesion challenge"""
        started_time = time.process_time()
        json_pdp_response = args.json_pdp_response
        json_hashfile = args.json_hashfile

        self.stdout.write("\n")
        proof_succeded, filepath = pdp_json.verification(json_pdp_response, json_hashfile)
        if proof_succeded:
            self.stdout.write(f"The result of the Proof of Data challenge was correct.\n")
            self.stdout.write(f"The server confirmed the integrity of the file '{filepath}'.\n")
        else:
            self.perror(f"The result of the challenge was not correct.\n")
            self.perror(f"The file '{filepath}' might be corrupted.\n")
        elapsed_time = time.process_time() - started_time
        self.stdout.write(f"Executed in {elapsed_time:9.3f}s.\n")
        self.stdout.write("\n")

    @cmd2.with_category(HIDS)
    def do_start(self, args):
        """Start the HIDS system"""
        hids_runner.run()


def run():
    cli = HIDSegus()
    sys.exit(cli.cmdloop())