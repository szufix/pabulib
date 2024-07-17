# Update the parsing function to handle different types of BibTeX entries, including 'inproceedings'
import re
import bibtexparser

# Function to format author names
def format_authors(authors):
    authors = authors.replace('\n', ' ').split(' and ')

    formatted_authors = []
    for author in authors:
        names = author.split()
        # Assumes the last name is the surname, and all preceding names are first/middle names
        # This might need adjustment for names with different structures
        if len(names) > 1:
            formatted_name = '. '.join(name[0] for name in names[1:]) + '. ' + names[0]
        else:
            formatted_name = names[0]  # Handle case of single-name authors
        formatted_authors.append(formatted_name)
    return ' '.join(formatted_authors)


def updated_bib_to_html():

    library = bibtexparser.parse_file("bib.bib")

    sorted_entries = sorted(library.entries, key=lambda x: x['year'], reverse=True)

    html_entries = []

    for i in range(len(sorted_entries)):
        fields = sorted_entries[i]

        # Build HTML string with improved logic
        html_entry = f'<li>\n'
        html_entry += f'{format_authors(fields["author"])}'
        html_entry += f' ({fields["year"]}),'
        html_entry += f' {fields["title"]}'

        html_entry += '\n</li>\n\n'

        html_entries.append(html_entry)

    html_code = ''.join(html_entries)
    return html_code


# Convert the BibTeX file to HTML with the updated function
updated_html_code = updated_bib_to_html()
print(updated_html_code)  # Display the first part of the updated HTML code for brevity

