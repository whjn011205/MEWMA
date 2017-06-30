rm *.pyc
rm *.pyd
rm *.o
C:\msys64\mingw64\bin\gcc.exe -static -DMS_WIN64 -mdll -O -Wall -ID:\Anaconda3\envs\py27\lib\site-packages\numpy\core\include -ID:\Anaconda3\envs\py27\include  -IC:\lib64\GSL\include -c sample27.c -o sample.o

C:\msys64\mingw64\bin\gcc.exe -static -DMS_WIN64 -shared -s sample.o -LD:\Anaconda3\envs\py27\libs -LC:\lib64\GSL\lib -lpython27  -lgsl -lgslcblas -o sample.pyd