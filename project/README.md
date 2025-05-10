# Steganography Tool for Linux (`steghide` wrapper)

This Python script uses the `steghide` Linux tool to hide files inside images or audio and to get them back out.

[Video Demo](./demo.mp4)

## Prerequisites

* **Linux:** This is for Linux systems. Tested on Debian 12.
* **Python 3:** The script needs Python 3.
* **`steghide`:** You have to install `steghide` yourself.

## Setup

1.  **Get the script:**
  Download or clone `steganography.py`.

2.  **Install `steghide`:**
  If you don't have it, install it. For example, on Debian/Ubuntu:
  ```bash
  sudo apt update
  sudo apt install steghide
  ```
  For other Linux distros, use their package manager.

3.  **Make it executable (optional):**
  ```bash
  chmod +x steganography.py
  ```

## How to Use

There are two main commands: `embed` (to hide a file) and `extract` (to get it back).

### Hiding a File (`embed`)

This puts your secret file into a cover file.

**Command:**

```bash
./steganography.py embed -c <cover_file> -e <file_to_hide> -p <password> [-o <output_name>]
```

* `-c <cover_file>`: The image/audio you're hiding stuff in (e.g., `picture.jpg`, `song.wav`).
* `-e <file_to_hide>`: The secret file you want to hide (e.g., `secret.txt`).
* `-p <password>`: Password to protect your hidden file. **Remember it\!**
* `-o <output_name>` (Optional): Name for the new file with the hidden stuff.
  * If you skip `-o`, the original `<cover_file>` will be overwritten. **Be careful\!**

**Example:**

```bash
# Make a secret file
echo "My secret message" > secret.txt

# Hide notes.txt in my_image.jpg, save as new_image.jpg
./steganography.py embed -c my_image.jpg -e secret.txt -p MyPassword123 -o new_image.jpg
```

### Getting a Hidden File Back (`extract`)

This pulls your secret file out of the stego file.

**Command:**

```bash
./steganography.py extract -s <stego_file> -p <password> [-o <extracted_file_name>]
```

* `-s <stego_file>`: The file that has your secret hidden in it (e.g., `new_image.jpg`).
* `-p <password>`: The password you used when hiding the file.
* `-o <extracted_file_name>` (Optional): What to name the extracted file.
  * If you skip `-o`, `steghide` tries to use the original name of the file you hid. The script will tell you what filename it used.

**Example:**

```bash
# Get the hidden file from new_image.jpg
./steganography.py extract -s new_image.jpg -p MyPassword123 -o my_extracted_notes.txt

# Check it
cat my_extracted_notes.txt
```

## Supported File Types

### Cover files

`steghide` (and this script) works only with these cover file types:

  * **Images:** JPEG (`.jpg`, `.jpeg`), BMP (`.bmp`)
  * **Audio:** WAV (`.wav`), AU (`.au`)

### Embedded files

You can hide any type of file inside cover files.
