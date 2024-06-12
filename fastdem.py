import argparse
import threading
import gzip
from queue import Queue

def process_group(group, output_queue, max_threads, args):
  """
  Processes a group and writes extracted lines to a compressed file.

  Args:
    group: The group to search for.
    output_queue: Queue to store output lines for writing.
    max_threads: The maximum number of threads to use. If not specified, it will be
    determined automatically.
  """
  with gzip.open(f"{args[3].outdir}/{group}.hits.gz", "wt") as out_file, \
       gzip.open(args[3].input, "rb") as f:
      line_counter = -1
      for line in f:
        line_counter += 1
        if line_counter % 4 == 0 and line.decode().startswith("@"):
          line = line.decode()
          if group in line:
            for _ in range(3):
              next_line = next(f).decode()
              output_queue.put(next_line)
        else:
          next(f)

def main():
  """
  Parses command-line arguments and runs the program.
  """
  parser = argparse.ArgumentParser(description="Fastq Demultiplexer.")
  parser.add_argument("-i", "--input", type=str, required=True, help="Input file to" +
                      "search patterns on.")
  parser.add_argument("-b", "--barcodes", type=str, required=True, help="File" +
                      "containing patterns to be searched for.")
  parser.add_argument("-o", "--outdir", type=str, default=".", help="Output directory" +
                      "(default: current directory).")
  parser.add_argument("-t", "--threads", type=int, default=None, help="Maximum number" +
                      "of threads to use (default: maximum available).")
  parser.add_argument("-v", "--version", action="version", version="%(prog)s a-0.0",
                      help="Display program version and exit.")
  parser.add_argument("-s", "--silent", action="store_true", help="Turn off verbose" +
                      "mode.(to be done)")
  args = parser.parse_args()

  if args.help or len(vars(args)) == 0:
    parser.print_help()
    return

# Get user input for maximum threads (if not provided, determine automatically)
  max_threads = args.threads
  if max_threads is None:
    import multiprocessing
    max_threads = multiprocessing.cpu_count()
  else:
    max_threads = int(max_threads)

  # Create queues and threads
  output_queue = Queue()

  def worker(output_queue):
    """
    Worker thread that processes lines from the queue and writes them to output files.
    """
    while True:
      line = output_queue.get()
      if line is None:
        break
      group = line.split(" ")[0] # Assuming the first word is the group
      with gzip.open(f"{args.outdir}/{group}.hits.gz", "at") as out_file:
        out_file.write(line)
  
  threads = []
  for _ in range(max_threads):
    worker_thread = threading.Thread(target=worker, args=(output_queue,))
    worker_thread.start()
    threads.append(worker_thread)

  # Read groups and process them in threads
  groups = []
  with open(args.barcodes, "r") as f:
   for line in f:
      groups.append(line.strip())

  for group in groups:
    thread = threading.Thread(target=process_group,
                              args=(group,
                                    output_queue,
                                    max_threads,
                                    args))
    thread.start()

# Signal threads to finish and wait for them
  for _ in range(max_threads):
   output_queue.put(None)

  for thread in threads:
   thread.join()

#Process barcodes and write output files
  process_group(group, output_queue, max_threads, args)

# Code to process the input file, groups, and output files based on the arguments
if __name__ == "__main__":
  main()
