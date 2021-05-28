OPENGLLIB= -lGL
GLULIB= -lGLU
GLUTLIB = -lglut
LIBS=$(OPENGLLIB) $(GLULIB) $(GLUTLIB)

BINDIR=./bin

SRCDIR=./src

SHADERCPP=./src/shader_util.cpp
SHADEROBJ=$(OBJECTFILES)/shader_util.o

BIN1=$(BINDIR)/objloader
BIN2=$(BINDIR)/objloader_1

SRCS1=$(SRCDIR)/objloader.cpp
SRCS2=$(SRCDIR)/objloader_1.cpp

all: $(BIN1) $(BIN2)

$(BIN1): $(SRCS1)
	g++ $(SRCS1) $(LIBS) -o $(BIN1).o;

$(BIN2): $(SRCS2)
	g++ $(SRCS2) $(LIBS) -o $(BIN2).o;

clean:
	rm -f *~ $(BINDIR)/*.o
