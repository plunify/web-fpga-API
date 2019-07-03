import plunifyutils
import hashlib
import os
import struct
import argparse
import sys
from shutil import copyfile
from Crypto.Cipher import AES
from Crypto import Random

def encryptFile(key, in_filename, out_filename=None):

    if not out_filename:
        out_filename = in_filename + '.enc'

    chunk_size = 1024 * 1024
    signature = b"[Encrypted by Plunify Pte Ltd. v1]"
    iv = Random.new().read( AES.block_size )
    cipher = AES.new( key, AES.MODE_CBC, iv )
    filesize = os.path.getsize(in_filename)

    in_file = open(in_filename, 'rb')
    signature_found = in_file.read( len(signature) )
    in_file.close()

    if signature_found == signature:
        print("{} has already been encrypted".format(os.path.abspath(in_filename)))
        copyfile(in_filename, out_filename)
        return

    in_file = open(in_filename, 'rb')
    out_file = open(out_filename, 'wb')

    out_file.write(signature)
    out_file.write(struct.pack('<Q', filesize))
    out_file.write(iv)

    while True:
        chunk = in_file.read(chunk_size)
        if len(chunk) == 0:
            break
        if len(chunk) % 16 != 0:
            chunk += b' ' * (16 - len(chunk) % 16)
        enc_chunk = cipher.encrypt(chunk)
        out_file.write(enc_chunk)

    in_file.close()
    out_file.close()


def decryptFile(key, in_filename, out_filename=None):

    if not out_filename:
        out_filename = in_filename + '.dec'

    chunk_size = 1024 * 1024
    signature = b"[Encrypted by Plunify Pte Ltd. v1]"
    
    in_file = open(in_filename, 'rb')
    signature_found = in_file.read( len(signature) )
    in_file.close()

    if signature_found != signature:
        print("{} has not been encrypted".format(os.path.abspath(in_filename)))
        copyfile(in_filename, out_filename)
        return

    in_file = open(in_filename, 'rb')
    out_file = open(out_filename, 'wb')

    signature_found = in_file.read( len(signature) )
    origsize = struct.unpack('<Q', in_file.read(struct.calcsize('Q')))[0]
    iv = in_file.read( AES.block_size )
    cipher = AES.new( key, AES.MODE_CBC, iv )

    while True:
        chunk = in_file.read(chunk_size)
        if len(chunk) == 0:
            break
        dec_chunk = cipher.decrypt(chunk)
        out_file.write(dec_chunk)
        
    out_file.truncate(origsize)
    in_file.close()
    out_file.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--credentials", metavar="credentials", help="Location of credential file. Default location is <home directory>/.plunify/credentials")
    parser.add_argument("-i", "--input", metavar="input", help="Input file to encrypt")
    parser.add_argument("-o", "--output", metavar="output", help="Ouput encrypted file")

    args = parser.parse_args()

    plunify_apiid, plunify_key, plunify_password = plunifyutils.readCredentialsFile(args.credentials)

    if not args.input or not args.output:
        print("Please specify input and output file to encrypt")
        sys.exit()

    in_filename = os.path.abspath(args.input)
    out_filename = os.path.abspath(args.output)

    if os.path.isdir(in_filename):
        print("Specified file for encryption {} is a directory".format(in_filename))
        sys.exit()

    if not os.path.exists(in_filename):
        print("Specified file for encryption {} does not exist".format(in_filename))
        sys.exit()

    print("Decrypting {}".format(in_filename))
    if sys.version_info[0] < 3:
        key = hashlib.md5(bytes(plunify_password)).hexdigest()
    else:
        key = hashlib.md5(bytes(plunify_password, "latin-1")).hexdigest()

    if in_filename == out_filename:
        tmp_filename = out_filename + ".plunify.tmp"
        decryptFile(key, in_filename, tmp_filename)
        copyfile(tmp_filename, in_filename)
        os.remove(tmp_filename)
    else:
        decryptFile(key, in_filename, out_filename)
    print("Done")


if __name__ == "__main__":
    main()
