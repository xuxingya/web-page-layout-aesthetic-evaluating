all:
	g++ -fPIC -shared extern.cpp -I/usr/include/ -L/usr/lib64 -lopencv_core -lopencv_highgui -lopencv_imgproc -o ../libs/blank.so	

test: main.cpp
	g++ main.cpp -L/usr/lib64 -lopencv_core -lopencv_highgui -lopencv_imgproc -o test

clean:
	rm test
