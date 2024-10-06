import re

class SparseMatrix:
    def _init_(self, file_path=None, rows=0, cols=0):  # Fixed constructor
        self.rows = rows
        self.cols = cols
        self.data = {}
        if file_path:
            self.load_from_file(file_path)
    
    def load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
                # Get dimensions of the matrix
                first_line = lines[0].strip()
                second_line = lines[1].strip()
                self.rows = int(first_line.split('=')[1])
                self.cols = int(second_line.split('=')[1])
                
                # Process each line to extract matrix elements
                for line in lines[2:]:
                    line = line.strip()
                    if not line:  # Ignore blank lines
                        continue
                    match = re.match(r'\((\d+),\s*(\d+),\s*(-?\d+)\)', line)
                    if not match:
                        raise ValueError("The input file format is incorrect")
                    row, col, value = map(int, match.groups())
                    self.set_element(row, col, value)
        except Exception as e:
            raise ValueError(f"An error occurred while reading the matrix file: {str(e)}")
    
    def get_element(self, row, col):
        return self.data.get((row, col), 0)
    
    def set_element(self, row, col, value):
        if value != 0:
            self.data[(row, col)] = value
        elif (row, col) in self.data:
            del self.data[(row, col)]  # Remove entry if the value is zero to maintain sparsity
    
    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Both matrices must have the same dimensions for addition")
        
        result = SparseMatrix(rows=self.rows, cols=self.cols)
        
        # Combine elements from both matrices
        for (row, col), value in self.data.items():
            result.set_element(row, col, value + other.get_element(row, col))
        
        for (row, col), value in other.data.items():
            if (row, col) not in self.data:
                result.set_element(row, col, value)
        
        return result
    
    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Both matrices must have the same dimensions for subtraction")
        
        result = SparseMatrix(rows=self.rows, cols=self.cols)
        
        # Compute difference of elements from both matrices
        for (row, col), value in self.data.items():
            result.set_element(row, col, value - other.get_element(row, col))
        
        for (row, col), value in other.data.items():
            if (row, col) not in self.data:
                result.set_element(row, col, -value)
        
        return result
    
    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrix multiplication cannot be performed; the columns of the first must match the rows of the second")
        
        result = SparseMatrix(rows=self.rows, cols=other.cols)
        
        # Perform multiplication using the dot product
        for (row1, col1), value1 in self.data.items():
            for col2 in range(other.cols):
                value2 = other.get_element(col1, col2)
                if value2 != 0:
                    result.set_element(row1, col2, result.get_element(row1, col2) + value1 * value2)
        
        return result


def main():
    # Load two sparse matrices from specified files
    matrix1 = SparseMatrix(file_path='DSA/small_input_01.txt')
    matrix2 = SparseMatrix(file_path='DSA/small_input_02.txt')
    
    # Prompt user for the desired operation
    operation = input("Select operation: add, subtract, multiply: ").strip().lower()
    
    if operation == 'add':
        result = matrix1.add(matrix2)
    elif operation == 'subtract':
        result = matrix1.subtract(matrix2)
    elif operation == 'multiply':
        result = matrix1.multiply(matrix2)
    else:
        print("Operation not recognized")
        return
    
    # Display the resulting matrix in sparse format
    for (row, col), value in result.data.items():
        print(f"({row}, {col}, {value})")


if _name_ == "_main_":  # Fixed main block
    main()
