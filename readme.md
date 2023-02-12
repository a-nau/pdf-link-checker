# PDF Link Checker

Github Action to automatically check all links in a PDF for availability to find dead or broken links.


## Usage

Install the package using `pip`
```shell
pip install pdflinkchecker
```
and use it as a CLI tool
```shell
pdflinkchecker .                          # to search for and check all pdfs in the current directory recursively
pdflinkchecker path/to/pdf                # to check a specific file
pdflinkchecker path/to/pdf1 path/to/pdf2  # to check multiple specific files
```

To use the Github Action, create a `pdf_link_checker.yml` in `.github/workflows`:

```yaml
on: [push]

jobs:
  check_pdf_links:
    runs-on: ubuntu-latest
    name: Check PDF Links
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: PDF Link Checker
        uses: a-nau/pdf-link-checker@v0.1.3
        with:  # if all PDFs should be checked, just remove this part
          paths: 'root.pdf'  # adjust to file path
```

To run within Docker

```shell
docker build -t pdf_link_checker .
docker run -it --rm --mount type=bind,source=${PWD},target=/data/ --name pdf_link_checker pdf_link_checker /data/.
```

## Credits

I started from [pdf-link-checker](https://github.com/mattbriggs/pdf-link-checker)
by [Matt Briggs](https://github.com/mattbriggs). Especially `get_links_from_page` is still heavily borrowed from the
original.

This work is licensed under the [MIT](LICENSE) license.
