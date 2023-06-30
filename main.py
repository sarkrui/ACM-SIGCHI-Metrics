import csv
from seleniumbase import BaseCase
import pandas as pd

def sort_csv_by_citation_count(filename):
    # read the data from the csv file
    data = pd.read_csv(filename)

    # convert the "Citation count" column to integers for sorting
    data["Citation count"] = data["Citation count"].apply(lambda x: int(x.replace(',', '')) if isinstance(x, str) and x.replace(',', '').isdigit() else 0)

    # sort the data by "Citation count" in descending order
    sorted_data = data.sort_values(by="Citation count", ascending=False)

    # write the sorted data back to the csv file
    sorted_data.to_csv(filename, index=False)

def render_csv_to_markdown_table(filename, output_filename):
    # read the data from the csv file
    data = pd.read_csv(filename)

    # convert the DataFrame to markdown
    markdown_table = data.to_markdown(index=False)

    # write the markdown table to the output file
    with open(output_filename, 'w') as f:
        f.write(markdown_table)

class RecorderTest(BaseCase):
    def test_recording(self):
        # list of urls for the conferences
        conferences = [
        "https://dl.acm.org/conference/ubicomp",
        "https://dl.acm.org/conference/uist",
        "https://dl.acm.org/conference/iui",
        "https://dl.acm.org/conference/idc",
        "https://dl.acm.org/conference/c-n-c",
        "https://dl.acm.org/conference/tei",
        "https://dl.acm.org/conference/dis",
        "https://dl.acm.org/conference/chi",
        "https://dl.acm.org/conference/chi-play",
        "https://dl.acm.org/conference/chinese-chi",
        "https://dl.acm.org/conference/MobileHCI",
        "https://dl.acm.org/conference/ICMI",
        "https://dl.acm.org/conference/HRI",
        "https://dl.acm.org/conference/cscw"
        ]

        # headers for the csv file
        headers = ["Conference Name", "Conference Url", "Publication Years","Publication count",
                   "Available for Download","Citation count","Downloads (cumulative)",
                   "Downloads (6 weeks)","Downloads (12 months)","Average Citation per Article",
                   "Average Downloads per Article"]

        # open csv file to store metrics
        with open('acm_metrics.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)

            # write header
            writer.writeheader()

            # iterate over each conference
            for conference in conferences:
                self.open(conference)

                # Fetch the conference name from the specified div element
                conference_name = self.get_text('p.banner__text')

                # find all metric blocks
                metrics_elements = self.find_elements('div.bibliometrics__block')

                metrics = {}
                # iterate over each metric block and get its text (inner content)
                for metric_element in metrics_elements:
                    metric_text = metric_element.text
                    # print(metric_text)
                    
                    lines = metric_text.split('\n')
                    metric = lines[0]
                    value = ' '.join(lines[1:])

                    # Check if the metric is in headers before adding it to the metrics dictionary
                    if metric in headers:
                        metrics[metric] = value
                    else:
                        print(f"Dropped.")

                # write data to csv
                writer.writerow({"Conference Name": conference_name, "Conference Url": conference, **metrics})


if __name__ == "__main__":
    BaseCase.main(__name__, __file__,"--block-images","--headless2")
    sort_csv_by_citation_count('acm_metrics.csv')
    render_csv_to_markdown_table('acm_metrics.csv', 'README.md')
