def generate_pascal_triangle_formatted(n):
    """
    Generate and format Pascal's Triangle up to the n-th row.

    Parameters:
    n (int): Number of rows in Pascal's Triangle

    Returns:
    str: Formatted Pascal's Triangle as a string
    """
    triangle = []

    for row_num in range(n):
        row = [1 for _ in range(row_num + 1)]
        for i in range(1, row_num):
            row[i] = triangle[row_num - 1][i - 1] + triangle[row_num - 1][i]
        triangle.append(row)

    # Formatting the triangle
    formatted_triangle = ""
    max_width = len(" ".join(map(str, triangle[-1])))
    
    for row in triangle:
        formatted_row = " ".join(map(str, row))
        formatted_triangle += f"{formatted_row.center(max_width)}\n"

    return formatted_triangle

# Example usage
n = 10
formatted_pascals_triangle = generate_pascal_triangle_formatted(n)
print(formatted_pascals_triangle)
