from decimal import Decimal
from django.shortcuts import render
import concurrent.futures
import time
from math import prod
rates = [ (535,1.2,1,0.9,0.8,0.97,0.86), (978,1.06,1,0.76,0.8,0.97,0.85)]

def home(request):
        start = time.perf_counter()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            p1 = executor.submit(c1_run_routine,rates)
            p2 = executor.submit(c2_run_routine,rates)
        end = time.perf_counter()
        print(Decimal(end - start))

        start = time.perf_counter()
        c1_routine(rates)
        c2_routine(rates)
        end = time.perf_counter()
        print(Decimal(end - start))

        return render(request, 'myapp2/base3.html')


def c1_routine(rates):
    try:
        for item in rates:
            prem = prod(item)
            print(prem)
            time.sleep(1)
    except Exception as e:
        print(e)

def c2_routine(rates):
    try:
        for item in rates:
            prem = prod(item)
            print(prem)
            time.sleep(1)
    except Exception as e:
        print(e)


