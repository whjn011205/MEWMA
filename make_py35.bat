rm *.pyc
rm *.pyd
rm *.o
C:\msys64\mingw64\bin\gcc.exe -static -DMS_WIN64 -mdll -O -Wall -ID:\Anaconda3\Lib\site-packages\numpy\core\include -ID:\Anaconda3\include  -IC:\lib64\GSL\include -c update_py35.c -o update.o

C:\msys64\mingw64\bin\gcc.exe -static -DMS_WIN64 -shared -s update.o -LD:\Anaconda3\libs -LC:\lib64\GSL\lib -lpython35  -lgsl -lgslcblas -o update.pyd