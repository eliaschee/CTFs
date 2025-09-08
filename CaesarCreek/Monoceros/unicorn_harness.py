import argparse
from unicorn import *
from unicorn.x86_const import *  
from capstone import *
import unicorn_loader 

def hook_strlen(uc):
    print("strlen()")
    return

def unicorn_hook_instruction(uc, address, size, user_data):
    # http://www.capstone-engine.org/
    if address == 0x555555554831 or address == 0x555555554879:
        hook_strlen(uc)
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('context_dir', type=str, help="Directory containing process context")
    parser.add_argument('-d', '--debug', default=False, action="store_true", help="Dump trace info")
    args = parser.parse_args()

    print("Loading context from {}".format(args.context_dir))
    uc = unicorn_loader.AflUnicornEngine(args.context_dir, enable_trace=args.debug, debug_print=False)       

    uc.hook_add(UC_HOOK_CODE, unicorn_hook_instruction)

    START_ADDRESS = 0x555555554958
    END_ADDRESS   = 0x555555554978
    print("Starting emulation from 0x{0:016x} to 0x{1:016x}".format(START_ADDRESS, END_ADDRESS))
    uc.emu_start(START_ADDRESS, END_ADDRESS, timeout=0, count=0)

    print("Finished Emulation")    
        
if __name__ == "__main__":
    main()
