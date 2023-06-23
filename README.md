# Zpyder

A simple program to extract all the images from a website, recursively.

## Usage

```bash
> python3.11 -m venv env
> source env/bin/activate
> pip install -r requirements.txt
> chmod +x zpyder.py
> ./zpyder [-h] [-r] [-l LEVEL] [-p PATH] URL
```

## Options

* `-r`: Recursively downloads the images in a URL received as a parameter.
* `-l`: Indicates the maximum depth level of the recursive download. If not indicated, it will be 5.
* `-p`: Indicates the path where the downloaded files will be saved. If not specified, `./data/` will be used.

## Supported file extensions

* `.jpg/jpeg`
* `.png`
* `.gif`
* `.bmp`

## Example

To recursively download all the images from the website `https://example.com`, run the following command:

```bash
> ./zpyder -r https://example.com
```

This will download all the images in the website, including the images in subdirectories.

## Contributing

Contributions are welcome! Please open a pull request on GitHub.

## License

This project is licensed under the MIT License.
