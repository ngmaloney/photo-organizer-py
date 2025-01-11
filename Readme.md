# Photo Organizer

Photo Organizer is a Python project that helps you organize your photos by date, location, and other metadata.

## Features

- Organize photos by date
- Organize photos by location
- Support for various image formats
- Easy to use command-line interface

## Installation

To install the Photo Organizer, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/photo-organizer-py.git
cd photo-organizer-py
pip install -r requirements.txt
```

## Usage

To organize your photos, run the following command:

```bash
python main.py /src_path /dest_path
```

This will organize your photos into folders by date and location.

### Command-line Options

- `--dry-run`: Perform a dry run without making changes.
- `--convert`: Convert the file format during processing.
- `--debug`: Print debug information about files.

Example usage with options:

```bash
python main.py /src_path /dest_path --dry-run --convert --debug
```

## Contributing

Contributions are welcome! Please create an issue or submit a pull request if you have any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
