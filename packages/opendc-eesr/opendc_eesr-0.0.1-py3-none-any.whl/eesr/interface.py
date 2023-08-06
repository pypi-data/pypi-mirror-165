from eesr.reporting import run_basic_validation, html_builder
from eesr.analysis import GridAnalysis, preprocess
import json
import logging
from pandas import Timestamp
from weasyprint import HTML
import fitz

logger = logging.getLogger(__name__)


def setup_logging():
    pass


def read_data(data_path):
    with open(data_path, "r") as read_file:
        return json.load(read_file)


def generate_standard_profile(
    data_path, profile_name, graph_data, path="std_report.html", generate_domain=False
):
    data = read_data(data_path)
    builder = html_builder.HTMLBuilder(data, profile_name)

    run_basic_validation(data, builder.profile)

    if generate_domain:
        builder.generate_domain()
    builder.generate_metrics()
    builder.generates_graph(graph_data)
    builder.generate_meta()
    builder.add_logo()

    return builder.write_html(path=path)


def generate_compact_profile(data_path, profile_name, path="compact_report.html", generate_domain=False):
    data = read_data(data_path)
    builder = html_builder.HTMLBuilder(data, profile_name, template="compact")

    run_basic_validation(data, builder.profile)

    if generate_domain:
        builder.generate_domain()
    builder.generate_metrics()
    builder.generate_meta()

    return builder.write_html(path=path)


def to_pdf(report, out=None):
    if out is None:
        out = report.replace('.html', '.pdf')
    HTML(report).write_pdf(out)

    return out

#Based on solution: https://stackoverflow.com/a/55480474
def to_image(report, out=None):
    pdf = to_pdf(report)

    if out is None:
        out = pdf.replace('.pdf', '.png')
        
    doc = fitz.open(pdf)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=300)
    pix.save(out)

    return out

    
# Analysis Methods
def opendc_grid_analysis(
    dc_path, key_path, start: Timestamp, country, out, tz="Europe/Amsterdam", caching=True, green_ratio=None, PUE=1.59
):
    df_dc = preprocess(dc_path, start, tz, PUE=PUE)

    analysis = GridAnalysis(df_dc, key_path, country, caching=caching, green_ratio=green_ratio)
    df = analysis.analyze(out, "OpenDC Simulator (Solvinity)", "https://opendc.org/")

    return df


if __name__ == "__main__":
    pass