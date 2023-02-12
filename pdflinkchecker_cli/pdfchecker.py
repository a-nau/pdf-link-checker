import argparse
import urllib.request
from collections import Counter
from dataclasses import dataclass
from multiprocessing.pool import ThreadPool
from pathlib import Path
from socket import timeout
from typing import List

import PyPDF2 as pypdf
from tabulate import tabulate

__all__ = ["check", "check_url", "check_urls_in_pdf", "get_links_from_page"]


@dataclass
class LinkInfo:
    page_no: int
    url: str
    code: str
    error_details: str

    @property
    def error_summary(self):
        return [self.page_no, self.url, self.error_details]


def get_links_from_page(
    indexstart: int, indexend: int, pdf: pypdf.PdfFileReader
) -> List[List]:
    """ PDF Link Check
        For more information see: https://github.com/mattbriggs/pdf-link-checker
        PDFLinkCheck.py checks the hyperlinks in an Portable Document Format (PDF)
        file.

        Release V1.1.1 2020.1.23
    """

    links = []
    for i in range(indexstart, indexend):
        page_obj = pdf.getPage(i)
        page_no = i + 1
        annots = page_obj.get("/Annots", [])
        for a in annots:
            u = a.getObject()
            uris = u.get("/A", [])
            raw_url = uris.get("/URI", None)
            if raw_url is not None:
                links.append([page_no, raw_url])
    return links


def check_url(page_no: int, raw_url: str) -> LinkInfo:
    error_details = None
    if raw_url.startswith("mailto:"):
        code = "mail"
    elif raw_url.startswith("tel:"):
        code = "tel"
    else:
        try:
            req = urllib.request.Request(raw_url)
            req.add_header(
                "User-Agent",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            )
            code = urllib.request.urlopen(req, timeout=5).getcode()
        except (urllib.error.HTTPError, timeout, urllib.error.URLError) as e:
            code = "error"
            error_details = repr(e)
        except Exception as e:
            code = "error"
            error_details = f"Unknown: {repr(e)}"
    return LinkInfo(page_no, raw_url, code, error_details)


def check_urls_in_pdf(pdf_path: str) -> List[LinkInfo]:
    pdf = pypdf.PdfFileReader(pdf_path)
    link_results = []
    links = get_links_from_page(0, pdf.numPages, pdf)
    with ThreadPool() as pool:
        result = pool.map_async(lambda x: check_url(*x), links)
        for result in result.get():
            link_results.append(result)
    counter = Counter([l.code for l in link_results])
    print(f"\nAnalyzed {pdf_path}, found the following types of links/http codes: {dict(counter)}")
    errors = [r.error_summary for r in link_results if r.code == "error"]
    if len(errors) > 0:
        print(
            tabulate(
                errors, headers=["Page Number", "URL", "Details"], tablefmt="orgtbl",
            )
        )
    return errors


def check():
    parser = argparse.ArgumentParser(description="Check all URLs embedded in your PDF.")
    parser.add_argument(
        "paths",
        type=str,
        nargs="+",
        help="Paths to directories or files that should be checked.",
    )
    args = parser.parse_args()

    pdf_paths = []
    for path in args.paths:
        path = Path(path)
        if path.is_dir():
            pdf_paths.extend([str(f) for f in path.rglob("*.pdf")])
        else:
            if path.suffix == ".pdf":
                pdf_paths.append(str(path))
            else:
                print(f"Specified file {path} is not a PDF. Skipping.")

    errors = {}
    for pdf_path in pdf_paths:
        error_report = check_urls_in_pdf(pdf_path)
        errors[pdf_path] = len(error_report)
    erroneous_pdfs = sum(list(errors.values())) > 0
    if erroneous_pdfs:
        return f"\n\nFound the following PDFs with unavailable links: {errors}"


if __name__ == "__main__":
    errors = check()
    if errors is not None:
        raise ValueError(errors.replace("\n", ""))
