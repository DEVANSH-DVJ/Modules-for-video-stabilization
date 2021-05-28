all:
	g++ src/objloader.cpp -lGL -lGLU -lglut -o bin/objloader;
	g++ src/objloader_1.cpp -lGL -lGLU -lglut -o bin/objloader_1;

clean:
	rm -f *~ bin/*
