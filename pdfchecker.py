import argparse
import urllib.request
from collections import Counter
from dataclasses import dataclass
from multiprocessing.pool import ThreadPool
from typing import List
from pathlib import Path

import PyPDF2 as pypdf
from tabulate import tabulate


@dataclass
class LinkInfo:
    page_no: int
    url: str
    code: str
    error_details: str

    def __repr__(self) -> str:
        return (
            f"On page {self.page_no} for URL {self.url} got error: {self.error_details}"
        )

    @property
    def error_summary(self):
        return [self.page_no, self.url, self.error_details]


def get_links_from_page(indexstart, indexend, pdf) -> List[List]:
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
            code = urllib.request.urlopen(raw_url, timeout=5).getcode()
        except urllib.error.HTTPError as e:
            code = "error"
            error_details = repr(e)
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
    print(f"File {pdf_path}, found: {dict(counter)}")
    errors = [r.error_summary for r in link_results if r.code == "error"]
    print(
        tabulate(
            errors,
            headers=["Page Number", "URL", "Details"],
            tablefmt="orgtbl",
        )
    )
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check all URL embedded in your PDF')
    parser.add_argument('-p', '--pdf_path', help='Path to PDF file', required=False)
    args = parser.parse_args()
    if args.pdf_path is not None:
        pdf_paths = [args.pdf_path]
    else:
        ROOT = Path(__file__).parent.parent
        pdf_paths = [str(f) for f in ROOT.rglob("*.pdf")]

    errors = {}
    for pdf_path in pdf_paths:
        error_report = check_urls_in_pdf(pdf_path)
        errors[pdf_path] = len(error_report)
    if sum(list(errors.values())) > 0:
        raise ValueError(f"Found unavailable links!: {errors}")