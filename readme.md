# PDF Link Checker

Github Action to automatically check all links in a PDF for availability to find dead or broken links.
Code is partially based on [pdf-link-checker](https://github.com/mattbriggs/pdf-link-checker)
by [Matt Briggs](https://github.com/mattbriggs).


## Usage

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
        uses: a-nau/pdf-link-checker@v0.1.0
        with:  # if all PDFs should be checked, just remove this part
          pdf_filepath: 'root.pdf'  # adjust to file path
```

To run within Docker

```shell
docker build -t pdf_link_checker .
docker run -it --rm --mount type=bind,source=${PWD},target=/data/ --name pdf_link_checker pdf_link_checker
```

and to run locally with `Python 3.9`

```shell
pip install PyPDF2==2.12.* tabulate
python pdfchecker.py --pdf_path FILE_PATH
```

## Credits

I started from [pdf-link-checker](https://github.com/mattbriggs/pdf-link-checker)
by [Matt Briggs](https://github.com/mattbriggs). Especially `get_links_from_page` is still heavily borrowed from the
original.

This work is licensed under the [MIT](LICENSE) license.
