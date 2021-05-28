# OpenGL Libraries
OPENGLLIB= -lGL
GLULIB= -lGLU
GLUTLIB = -lglut

LIBS=$(OPENGLLIB) $(GLULIB) $(GLUTLIB)

# Binary output files
BINDIR=./bin

BIN1=$(BINDIR)/objloader
BIN2=$(BINDIR)/objloader_1

# C++ Source files
SRCDIR=./src

SRCS1=$(SRCDIR)/objloader.cpp
SRCS2=$(SRCDIR)/objloader_1.cpp

# MAKE Commands
all: $(BIN1) $(BIN2)

$(BIN1): $(SRCS1)
	g++ $(SRCS1) $(LIBS) -o $(BIN1).o;

$(BIN2): $(SRCS2)
	g++ $(SRCS2) $(LIBS) -o $(BIN2).o;

clean:
	rm -f *~ $(BINDIR)/*.o
