
import os
import csv


def import_params(path):
    print(path)
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        meta = {}
        projects = {}
        votes = {}
        section = ""
        header = []
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if str(row[0]).strip().lower() in ["meta", "projects", "votes"]:
                section = str(row[0]).strip().lower()
                header = next(reader)
            elif section == "meta":
                meta[row[0]] = row[1].strip()

    return int(meta['num_votes']), int(meta['num_projects'])


if __name__ == "__main__":

    # Replace this with your directory path
    directory = 'pabulib_877'

    # Iterate over all files in the directory
    with open('pabulib_params.csv', 'w', newline='', encoding="utf-8") as csvfile:
        csvfile.write(f"num_candidates;num_voters;filename\n")
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                num_voters, num_candidates = import_params(filepath)

                csvfile.write(f"{num_candidates};{num_voters};{filename}\n")

