#!/usr/bin/env python3

import argparse
import os
import re
import subprocess
import sys

def eprint(*args, **kwargs): print(*args, file=sys.stderr, **kwargs)

def check_steghide() -> bool:
    """Checks if steghide is installed and accessible."""
    try:
        subprocess.run(['steghide', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        eprint("Error: steghide does not appear to be installed or is not in your PATH.")
        eprint("Please install steghide to use this tool.")
        return False

def embed_message(cover_file: str, embed_file: str, output_file: str|None, passphrase: str) -> bool:
    """
    Embeds a file embed_file into the file cover_file using steghide.
    """
    if not os.path.exists(cover_file):
        eprint(f"Error: Cover file '{cover_file}' not found.")
        return False
    if not os.path.exists(embed_file):
        eprint(f"Error: File to embed '{embed_file}' not found.")
        return False

    if output_file is None:
        output_file = cover_file

    command = [
        'steghide', 'embed',
        '-cf', cover_file,
        '-ef', embed_file,
        '-sf', output_file,
        '-p', passphrase,
        '-f'
    ]

    try:
        print(f"Embedding '{embed_file}' into '{cover_file}' to create '{output_file}'...")
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        print(f"Successfully embedded message. Output saved to '{output_file}'.")
        return True
    except subprocess.CalledProcessError as e:
        eprint(f"Error during embedding with steghide:")
        if e.stdout:
            eprint(e.stdout)
        if e.stderr:
            eprint(e.stderr)
        return False
    except Exception as e:
        eprint(f"An unexpected error occurred: {e}")
        return False

def extract_message(stego_file: str, output_file: str|None, passphrase: str) -> bool:
    """
    Extracts a hidden file from stego_file using steghide.
    """
    if not os.path.exists(stego_file):
        eprint(f"Error: Stego file '{stego_file}' not found.")
        return False


    command = [
        'steghide', 'extract',
        '-sf', stego_file,
        '-p', passphrase,
        '-f'
    ]
    if output_file is not None:
        command.extend(['-xf', output_file])

    try:
        print(f"Extracting message from '{stego_file}'...")
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        
        stdout_match = re.search(r'wrote extracted data to "(.*)"\.', process.stdout)
        stderr_match = re.search(r'wrote extracted data to "(.*)"\.', process.stderr)
        if stdout_match:
            output_file = stdout_match.group(1)
        elif stderr_match:
            output_file = stderr_match.group(1)
            
        if output_file is not None and os.path.exists(output_file):
            if os.path.getsize(output_file) > 0:
                print(f"Successfully extracted message to '{output_file}'.")
                return True
            else:
                eprint(f"Warning: Extraction complete, but the output file '{output_file}' is empty.")
                eprint("This might indicate an incorrect passphrase or no embedded data.")
                os.remove(output_file)
                return False
        else:
            eprint(f"Error: Extraction failed. Output file '{output_file}' was not created.")
            eprint("This could be due to an incorrect passphrase or no hidden data in the file.")
            return False
    except subprocess.CalledProcessError as e:
        eprint(f"Error during extraction:")
        if e.stdout:
            eprint(e.stdout)
        if e.stderr:
            eprint(e.stderr)
        if output_file is not None and os.path.exists(output_file) and os.path.getsize(output_file) == 0:
            os.remove(output_file)
        return False
    except Exception as e:
        eprint(f"An unexpected error occurred: {e}")
        return False

def main():
    if not check_steghide():
        return

    parser = argparse.ArgumentParser(description="A Python tool to hide messages in images or audio files using steghide.")
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    embed_parser = subparsers.add_parser('embed', help='Embed a message into a cover file.')
    embed_parser.add_argument('-c', '--cover', required=True, help='Path to the cover image/audio file (e.g., image.bmp, audio.wav).')
    embed_parser.add_argument('-e', '--embed', required=True, help='Path to the file containing the message to embed (e.g., message.txt).')
    embed_parser.add_argument('-p', '--passphrase', required=True, help='Passphrase to protect the hidden message.')
    embed_parser.add_argument('-o', '--output', required=False, help='Path for the output stego image/audio file (e.g., output.bmp).')

    extract_parser = subparsers.add_parser('extract', help='Extract a hidden message from a stego file.')
    extract_parser.add_argument('-s', '--stego', required=True, help='Path to the stego image/audio file (e.g., output.bmp).')
    extract_parser.add_argument('-p', '--passphrase', required=True, help='Passphrase used during embedding.')
    extract_parser.add_argument('-o', '--output', required=False, help='Path to save the extracted message (e.g., extracted_message.bmp).')

    args = parser.parse_args()

    if args.command == 'embed':
        embed_message(args.cover, args.embed, args.output, args.passphrase)
    elif args.command == 'extract':
        extract_message(args.stego, args.output, args.passphrase)

if __name__ == '__main__':
    main()
