"""
    
    Test the the round-off error of floating point operations.
    
    lbuchart@eoas.ubc.ca
    January 4, 2026   
    
"""
#%%
import numpy as np

def test_roundoff1():
    input = 0.33333333333333333
    machine = np.round(1.0/3.0, 15)
    assert machine == input, f"Expected {input}, got {machine}, difference: {abs(input - machine)}"

def test_roundoff2():
    input = 3.141592653589793
    machine = np.round(np.pi, 15)
    assert machine == input, f"Expected {input}, got {machine}, difference: {abs(input - machine)}"
    
def test_roundoff3():
    input = 2.718281828459045
    machine = np.round(np.e, 15)
    assert machine == input, f"Expected {input}, got {machine}, difference: {abs(input - machine)}"

def test_roundoff4():
    input = 1.4142135623730951
    machine = np.round(np.sqrt(2), 15)
    assert machine == input, f"Expected {input}, got {machine}, difference: {abs(input - machine)}"
    
def test_roundoff5():
    input = 0.6931471805599453
    machine = np.round(np.log(2), 15)
    assert machine == input, f"Expected {input}, got {machine}, difference: {abs(input - machine)}"
    
def test_roundoff6():
    input = 0.3010299956639812
    machine = np.round(np.log10(2), 15)
    assert machine == input, f"Expected {input}, got {machine}, difference: {abs(input - machine)}"

#%%
test_roundoff1() 

#%%
test_roundoff2()

#%%
test_roundoff3()

#%%
test_roundoff4()

#%%
test_roundoff5()

#%%
test_roundoff6()
print("All tests completed.")
    
# %%
