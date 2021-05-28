# OpenGL Libraries
OPENGLLIB= -lGL
GLULIB= -lGLU
GLUTLIB = -lglut

LIBS=$(OPENGLLIB) $(GLULIB) $(GLUTLIB)

# Binary output files
BINDIR=./bin

BIN1=$(BINDIR)/objloader
BIN2=$(BINDIR)/pixel_map
BIN3=$(BINDIR)/image_save

# C++ Source files
SRCDIR=./src

SRCS1=$(SRCDIR)/objloader.cpp
SRCS2=$(SRCDIR)/pixel_map.cpp
SRCS3=$(SRCDIR)/image_save.cpp

# MAKE Commands
all: $(BIN1) $(BIN2) $(BIN3)

$(BIN1): $(SRCS1)
	g++ $(SRCS1) $(LIBS) -o $(BIN1).o;

$(BIN2): $(SRCS2)
	g++ $(SRCS2) $(LIBS) -o $(BIN2).o;

$(BIN3): $(SRCS3)
	g++ $(SRCS3) $(LIBS) -o $(BIN3).o;

clean:
	rm -f *~ $(BINDIR)/*.o
