import tkinter as tk
from tkinter import messagebox

class SimpleSudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("450x550")
        self.root.configure(bg='#f0f0f0')
        
        self.entries = []
        self.setup_interface()
    
    def setup_interface(self):
       
        title_label = tk.Label(self.root, text="Sudoku Solver", 
                              font=("Arial", 16, "bold"), 
                              bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=10)
        
       
        instruction = tk.Label(self.root, text="Enter numbers 1-9 (use 0 or leave blank for empty cells)", 
                              font=("Arial", 9), bg='#f0f0f0', fg='#666666')
        instruction.pack(pady=5)
        
       
        grid_frame = tk.Frame(self.root, bg='#333333', padx=3, pady=3)
        grid_frame.pack(pady=15)
        
        self.create_grid(grid_frame)
        
       
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        
        solve_btn = tk.Button(button_frame, text="Solve", 
                             font=("Arial", 12, "bold"),
                             bg='#4CAF50', fg='white',
                             width=10, height=1,
                             command=self.solve)
        solve_btn.pack(side=tk.LEFT, padx=10)
        
        
        clear_btn = tk.Button(button_frame, text="Clear", 
                             font=("Arial", 12, "bold"),
                             bg='#f44336', fg='white',
                             width=10, height=1,
                             command=self.clear)
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        
        self.status_label = tk.Label(self.root, text="Ready to solve", 
                                    font=("Arial", 10), bg='#f0f0f0', fg='#333333')
        self.status_label.pack(pady=10)
    
    def create_grid(self, parent):
        for row in range(9):
            row_entries = []
            for col in range(9):
               
                border_width = 1
                padx = (1, 3) if col % 3 == 2 and col != 8 else (1, 1)
                pady = (1, 3) if row % 3 == 2 and row != 8 else (1, 1)
                
                entry = tk.Entry(parent, width=2, font=("Arial", 18, "bold"),
                                justify="center", relief="solid", 
                                borderwidth=border_width,
                                bg='white', fg='#333333')
                entry.grid(row=row, column=col, padx=padx, pady=pady, ipadx=8, ipady=8)
               
                entry.bind('<Key>', self.validate_input)
                
                row_entries.append(entry)
            self.entries.append(row_entries)
    
    def validate_input(self, event):
        """Only allow numbers 1-9 or backspace"""
        if event.keysym in ['BackSpace', 'Delete']:
            return True
            
        if event.char and event.char.isdigit():
            num = int(event.char)
            if 1 <= num <= 9:
                
                if event.widget.get():
                    event.widget.delete(0, tk.END)
                return True
        
        return False
    
    def get_grid(self):
        """Get current grid values"""
        grid = []
        for row in range(9):
            current_row = []
            for col in range(9):
                val = self.entries[row][col].get()
                if val == "":
                    current_row.append(0)
                else:
                    current_row.append(int(val))
            grid.append(current_row)
        return grid
    
    def display_solution(self, solution):
        """Display the solved puzzle"""
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                if solution[row][col] != 0:
                    self.entries[row][col].insert(0, str(solution[row][col]))
    
    def is_valid_sudoku(self, board, row, col, num):
        """Check if placing num at board[row][col] is valid"""
       
        for x in range(9):
            if board[row][x] == num:
                return False
        
        
        for x in range(9):
            if board[x][col] == num:
                return False
        
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        
        return True
    
    def solve_sudoku(self, board):
        """Solve using backtracking algorithm"""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:  # Empty cell
                    for num in range(1, 10):
                        if self.is_valid_sudoku(board, row, col, num):
                            board[row][col] = num
                            
                            if self.solve_sudoku(board):
                                return True
                            
                            board[row][col] = 0  
                    return False
        return True
    
    def solve(self):
        """Solve the Sudoku puzzle"""
        self.status_label.config(text="Solving...")
        
        
        board = self.get_grid()
        
        
        board_copy = [row[:] for row in board]
        
       
        if self.solve_sudoku(board_copy):
            self.display_solution(board_copy)
            self.status_label.config(text="Solved!")
            messagebox.showinfo("Success", "Sudoku solved successfully!")
        else:
            self.status_label.config(text="No solution found")
            messagebox.showerror("Error", "No solution exists for this puzzle!")
    
    def clear(self):
        """Clear the entire grid"""
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
        self.status_label.config(text="Grid cleared")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleSudokuSolver(root)
    root.mainloop()