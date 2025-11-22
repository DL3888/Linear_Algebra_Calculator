class Matrix: 
    def __init__(self, data: list[list[float]]):
        if not data or not data[0]:
            raise ValueError("Matrix cannot be empty")
        self.rows = len(data)
        self.cols = len(data[0])
        for row in data:
            if len(row) != self.cols:
                raise ValueError("All rows must have the same number of columns")
        self.data = [[float(x) for x in row] for row in data]

    def __str__(self):
        return '\n'.join(' '.join(f"{x:.2f}" for x in row) for row in self.data)
    
    def __add__(self, other):
        # Add twp matrices (only possible for the same dimensions)
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions to add")
        
        result = [[self.data[i][j] + other.data[i][j] for j in range(self.cols)] for i in range(self.rows)]
        
        return Matrix(result)
    
    def __mul__(self, other):
        # Multiply two matrices (only possible if the number of columns in the first equals the number of rows in the second)
        if self.cols != other.rows:
            raise ValueError("Number of columns in the first matrix must equal number of rows in the second matrix")
        
        result = [[0.0 for _ in range(other.cols)] for _ in range(self.rows)]
        
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result[i][j] += self.data[i][k] * other.data[k][j]
        
        return Matrix(result)
    
    def transpose(self):
        # Transpose the matrix
        result = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(result)
    
    def det(self):
        # Calculate the determinant (only for square matrices)
        if self.rows != self.cols:
            raise ValueError("Determinant can only be calculated for square matrices")
        
        #if its a small matrix, calculate directly
        if self.rows == 1:
            return self.data[0][0]
        
        if self.rows == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        
        # if larger matrix, use Laplace expansion
        determinant = 0.0
        for c in range(self.cols):
            minor = Matrix([row[:c] + row[c+1:] for row in self.data[1:]])
            determinant += ((-1) ** c) * self.data[0][c] * minor.det()
        
        return determinant
    
    def inverse(self):
        # Calculate the inverse (only for square matrices with non-zero determinant)
        if self.rows != self.cols:
            raise ValueError("Inverse can only be calculated for square matrices")
        
        det = self.det()
        if det == 0:
            raise ValueError("Matrix is singular and cannot be inverted")
        
        # Create the matrix of minors
        minors = [[0.0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                minor = Matrix([row[:j] + row[j+1:] for k, row in enumerate(self.data) if k != i])
                minors[i][j] = minor.det()
        
        # Create the matrix of cofactors
        cofactors = [[((-1) ** (i + j)) * minors[i][j] for j in range(self.cols)] for i in range(self.rows)]
        
        # Transpose the cofactor matrix to get the adjugate
        adjugate = Matrix(cofactors).transpose()
        
        # Divide each element by the determinant to get the inverse
        inverse_data = [[adjugate.data[i][j] / det for j in range(adjugate.cols)] for i in range(adjugate.rows)]
        
        return Matrix(inverse_data)
    
    
    

