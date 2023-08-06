from eesr.reporting import run_basic_validation, html_builder
from eesr.analysis import GridAnalysis, process
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
    data_path, profile_name, graph_data, generate_domain=False
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

    builder.write_html()


def generate_compact_profile(data_path, profile_name, generate_domain=False):
    data = read_data(data_path)
    builder = html_builder.HTMLBuilder(data, profile_name, template="compact")

    run_basic_validation(data, builder.profile)

    if generate_domain:
        builder.generate_domain()
    builder.generate_metrics()
    builder.generate_meta()

    builder.write_html()


def to_pdf(report, out):
    HTML(report, base_url=".").write_pdf(out)

#Based on solution: https://stackoverflow.com/a/55480474
def to_image(report, out):
    doc = fitz.open(report)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=300)
    pix.save(out)

# Analysis Methods
def opendc_grid_analysis(
    dc_path, key_path, start: Timestamp, country, out, tz="Europe/Amsterdam"
):
    df_dc = process(dc_path, start, tz)

    analysis = GridAnalysis(df_dc, key_path, country)
    df = analysis.analyze(out, "OpenDC Simulator", "https://opendc.org/")

    return df


if __name__ == "__main__":
    pass
