import os
import sys

def process_file(src_file, dest_file):
    with open(src_file, 'r') as f:
        lines = f.readlines()

    with open(dest_file, 'w') as f:
        for line in lines:
            # Split the line by space and then join using a tab
            f.write('\t'.join(line.split()) + '\n')

def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py source_directory destination_directory")
        sys.exit(1)

    src_dir = sys.argv[1]
    dest_dir = sys.argv[2]

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            process_file(src_file, dest_file)

    print(f"Processed files saved in {dest_dir}")

if __name__ == "__main__":
    main()
