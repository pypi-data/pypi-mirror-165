from pathlib import Path
from hashcopy import HashCopier

with Path('hashcopy.c').open('rb') as inputfp, Path('output.c').open('wb') as outputfp:
    with HashCopier(inputfp.fileno(), outputfp.fileno()) as hasher:
        while (bytes_copied := hasher.update()) > 0:
            print(f'hashed {bytes_copied} bytes')
        print(f'hash result = {hasher.finalize().hex()}')
