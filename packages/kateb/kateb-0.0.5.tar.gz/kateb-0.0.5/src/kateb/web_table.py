from bs4 import BeautifulSoup
from .table_manager import TableManager

def clean_cell_content(text):
    black_list = ['\n', '\t', '\r']
    for ch in black_list:
        text = text.replace(ch, '')
    text = text.strip()
    return text

class WebTableExtractor():
    def __init__(self, html, extract_links=False):
        if isinstance(html, BeautifulSoup):
            self.soup = html
        else:
            self.soup = BeautifulSoup(html, 'html.parser')
        self.tables = []
        self.table = TableManager()
        self.table_link = extract_links

        self.parse_page()


    def search_tables(self, drop_subtables=False):
        tables = self.soup.find_all('table')
        if drop_subtables:
            subtables = []
            for t in tables:
                subtables.extend(t.find_all('table'))
            tables = [x for x in tables if x not in subtables]
        self.html_tables = tables


    def read_cell(self, html_cell):
        content = html_cell.get_text()
        content = clean_cell_content(content)

        if content == '':
            cell_input = html_cell.find('input')
            if cell_input is not None:
                content = cell_input.get('value')

        attributes = html_cell.attrs
        colspan = 1
        if 'colspan' in attributes:
            if attributes['colspan'].isnumeric():
                colspan = int(attributes['colspan'])
        
        rowspan = 1
        if 'rowspan' in attributes:
            if attributes['rowspan'].isnumeric():
                rowspan = int(attributes['rowspan'])
        
        return (content, colspan, rowspan)


    def extract_link(self, html_cell):
        try:
            link = html_cell.find('a')['href']
            return link
        except (ValueError, TypeError):
            return None


    def parse_cell(self, html_cell):
        content, colspan, rowspan = self.read_cell(html_cell)
        self.table.write_in_row(content=content, colspan=colspan, rowspan=rowspan)
        if self.table_link is True:
            link = self.extract_link(html_cell)
            self.table.write_in_row(link)


    def parse_row(self, html_row):
        html_cells = html_row.find_all(['th', 'td'])
        for html_cell in html_cells:
            self.parse_cell(html_cell=html_cell)


    def parse_table(self, html_table):
        html_rows = html_table.find_all('tr')
        for html_row in html_rows:
            self.parse_row(html_row)
            self.table.next_row()

    
    def parse_page(self, drop_subtables=False):
        self.search_tables(drop_subtables)
        for html_table in self.html_tables:
            self.table = TableManager()
            self.parse_table(html_table)
            self.tables.append(self.table.table)

