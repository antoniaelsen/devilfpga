import argparse


def reverse_bits(byte):
    return int(format(byte, '08b')[::-1], 2)


def main():
    parser = argparse.ArgumentParser(
        description="Reverse a bitstream")
    parser.add_argument("input_file", help="Input binary file")
    parser.add_argument("output_file", help="Output binary file")

    args = parser.parse_args()

    try:
        with open(args.input_file, 'rb') as input_file:
            input_data = input_file.read()

        reversed_data = bytes(reverse_bits(byte) for byte in input_data)

        with open(args.output_file, 'wb') as output_file:
            output_file.write(reversed_data)

        print(f"Reversed {len(input_data)} bytes")
        print("Done")
    except FileNotFoundError:
        print(f"Couldn't open the file {args.input_file} for input")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
