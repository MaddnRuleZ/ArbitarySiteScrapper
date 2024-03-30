from openpyxl import load_workbook
class ExcelUtils:
    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name


    # change single Cell, ex: (A10) A = Columb Row: 10
    def change_cell_content(self, row, columb, new_content):
        cell = str(row) + str(columb)

        # Load the Excel workbook
        workbook = load_workbook(self.file_path)

        # Get the sheet by name
        sheet = workbook[self.sheet_name]

        # Update the value of the specified cell
        sheet[cell] = new_content

        # Save the workbook
        workbook.save(self.file_path)


