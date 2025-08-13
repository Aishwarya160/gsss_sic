

Employee_name = input("Enter the employee name:")
Employee_id =  int(input("Enter the employee id:"))
Basic_monthly_salary =  int(input("Enter the basic monthly salary :"))
Special_allowances =  int(input("Enter the special allowances:"))
Bonus_percentage = float(input("enter the bonus percentage"))
Gross_monthly_salary = Basic_monthly_salary + Special_allowances
Annual_gross_salary = (Gross_monthly_salary * 12) + Bonus_percentage

print("The Gross monthly salary is", Gross_monthly_salary)
print("The Annual gross salary is", Annual_gross_salary)