# MEWMA (Multivariate Exponentially Weighted Moving Average)
MEWMA algo implemented in python. 
This algo is used in statistical process control to monitor a certain process quantity. It will detect abnormal data points in the monitoring char and raise alarm.

- mspc.py: 			Define a class for mspc(Multivariate Statistical Process Control) chart
- const_limit.py:	Child class of mspc.py. Define a mspc chart with upper/lower limits
- mewma.py:			Chile class of const_limit: Define a const_limit chart with monitoring function.
					The monitoring algo is called MEWMA (Multivariate Exponentially Weighted Moving Average)


Inside this algo, there is one function "update" which involves linear algebra operations that is computational intensive, thus developed an C extension to be called in python 
- update_py27.c: 	C extension for "update" function for py27
- make_py27.bat:	Compile update_py27.c into python module	

- update_py35.c:	C extension for "update" function for py35
- make_py35.bat:	Compile update_py35.c into python module	
