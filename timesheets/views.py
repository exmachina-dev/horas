from django.shortcuts import render

# Create your views here.
def home(request):
    cur_employee = None
    return render(request, 'timesheets/home.html', context)

def employees_list(request):
    employees = Empolyee.objects
    return render(request, 'timesheets/employees.html', context)
