# print("Hello, World!")
# array = ["a", "b", "c"]
# print(array)

# print("\n=== สูตรคูณ แม่ 2-12 ===")
def print_multiplication_table(a, b):
    for table in range(a, b + 1):
        print(f"\nแม่ {table}:")
        for i in range(1, 13):
            if(i*table%2==0):
                result = table * i
                print(f"{table} x {i} = {result}")


students = [{'name': 'John', 'grade': 'A'}, 
            {'name': 'Jane', 'grade': 'B'}, 
            {'name': 'Doe', 'grade': 'C'},
            {'name': 'Smith', 'grade': 'A'},
            {'name': 'Emily', 'grade': 'B'}
            ]
# print("\n=== Students with grade A ===")
a = 0
for student in students:
    if student['grade'] == 'A':
        a += 1
        # print(student['name'])
# print(f"Total students with grade A: {a}")