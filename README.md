# PDF Link Checker

Github Action and CLI tool to automatically check all links in a PDF for availability to find dead or broken links.

## Usage

Install the package using `pip`

```shell
pip install pdflinkchecker_cli
```

and use it as a CLI tool

```shell
pdflinkchecker .                          # to search for and check all pdfs in the current directory recursively
pdflinkchecker path/to/pdf                # to check a specific file
pdflinkchecker path/to/pdf1 path/to/pdf2  # to check multiple specific files
```

Exemplary output looks like this

```shell
Analyzed /data/dummy1.pdf, found the following types of links/http codes: {200: 13}

Analyzed /data/dummy2.pdf, found the following types of links/http codes: {'mail': 4, 'tel': 4, 200: 49, 'error': 3}
|   Page Number | URL                      | Details                                                             |
|---------------+--------------------------+---------------------------------------------------------------------|
|             1 | https://www.example1.com | <HTTPError 999: 'INKApi Error'>                                     |
|             1 | https://www.example2.com | URLError(timeout('_ssl.c:1112: The handshake operation timed out')) |
|             1 | https://www.example3.com | <HTTPError 403: 'Forbidden'>                                        |

```

To use the Github Action, create a `pdf_link_checker.yml` in `.github/workflows`:

```yaml
on: [ push ]

jobs:
  check_pdf_links:
    runs-on: ubuntu-latest
    name: Check PDF Links
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: PDF Link Checker
        uses: a-nau/pdf-link-checker@v0.2.0
        with:
          paths: '.'  # checks all PDFs, otherwise specify to file path(s)
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
