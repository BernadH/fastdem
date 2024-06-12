# fastdem
fastq demultiplexer
## A Python program for demultiplexing fastq files.

### The script reads the pairs of barcodes from a file in the format *barcode1+barcode2*, reads the compressed multiplexed .fastq.gz file and extracts the sequences of each group into a barcode1+barcode2.hits.fastq.gz file.

**WARNING: The program under development and does not work just yet, please be patient.**


Usage: main.py [-h] -i INPUT -b BARCODES [-o OUTDIR] [-t THREADS] [-v] [-s]

-i, --input: Input file to search patterns on.

-b, --barcodes: File containing patterns to be searched for.

-o, --outdir: Output directory (default: current directory).

-t, --threads: Maximum number of threads to use (default: maximum available).

-v, --version: Display current version and exit.

-s, --silent: Turn off verbose mode. (TO DO)
