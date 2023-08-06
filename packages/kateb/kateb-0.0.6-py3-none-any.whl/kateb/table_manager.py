class TableManager:
    def __init__(self):
        self.table = [
            [None]
            ]
        self.current_row = 0
        self.current_column = 0


    def is_available(self, row, column):
        if len(self.table) <= row:
            return False
        elif len(self.table[row]) <= column:
            return False
        else:
            return True
    

    def is_occupied(self, row, column):
        if not self.is_available(row=row, column=column):
            return False
        elif self.table[row][column] is None:
            return False
        else:
            return True
    

    def create_row(self, row):
        while (row > len(self.table)-1):
            self.table.append([None])


    def create_cell(self, row, column):
        self.create_row(row=row)
        while (column > len(self.table[row])-1):
            self.table[row].append(None)


    def write_cell(self, row, column, content):
        self.create_cell(row=row, column=column)
        self.table[row][column] = content


    def handle_colspan(self, row, column, content, colspan):
        for i in range(colspan):
            self.write_cell(row=row, column=column+i, content=content)


    def write_multiple_cells(self, row, column, content, colspan, rowspan):
        for i in range(rowspan):
            self.handle_colspan(row=row+i, column=column, content=content, colspan=colspan)

    
    def write_in_row(self, content, colspan=1, rowspan=1):
        while self.is_occupied(self.current_row, self.current_column):
            self.current_column += 1

        self.write_multiple_cells(
            row=self.current_row,
            column=self.current_column,
            content=content,
            colspan=colspan,
            rowspan=rowspan,
            )

        self.current_column += (colspan)


    def next_row(self):
        self.current_row += 1
        self.current_column = 0


    def show(self):
        for row in self.table:
            for cell in row:
                print(cell, end='\t')
            print('\n')
    
    