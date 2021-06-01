#include <GL/gl.h>
#include <GL/glut.h>

#include <iostream>
#include <unistd.h>
#include <vector>
#include <string.h>

using namespace std;

// globals
struct point {
  float x, y, z;
};

struct point2 {
  float x, y;
};

GLuint elephant;
float elephantrot, elephanttrans;
char ch = '1';
vector<point> vertices;

// other functions and main
// wavefront .obj loader code begins
void loadObj(char *fname) {
  elephant = glGenLists(1);

  std::vector<unsigned int> vertexIndices, uvIndices, normalIndices;
  std::vector<point> vertices;
  std::vector<point2> uvs;
  std::vector<point> normals;

  FILE *file = fopen(fname, "r");
  if (file == NULL) {
    printf("Incorrect path");
    getchar();
    return;
  }

  glPointSize(2.0);
  glNewList(elephant, GL_COMPILE);
  glPushMatrix();

  while (1) {

    char lineHeader[128];
    // read the first word of the line
    int res = fscanf(file, "%s", lineHeader);
    if (res == EOF)
      break; // EOF = End Of File. Quit the loop.

    // else : parse lineHeader

    if (strcmp(lineHeader, "v") == 0) {
      point vertex;
      fscanf(file, "%f %f %f\n", &vertex.x, &vertex.y, &vertex.z);
      vertices.push_back(vertex);
    } else if (strcmp(lineHeader, "vt") == 0) {
      point2 uv;
      fscanf(file, "%f %f\n", &uv.x, &uv.y);
      // uv.y = -uv.y; // Invert V coordinate since we will only use DDS
      // texture, which are inverted. Remove if you want to use TGA or BMP
      // loaders.
      uvs.push_back(uv);
    } else if (strcmp(lineHeader, "vn") == 0) {
      point normal;
      fscanf(file, "%f %f %f\n", &normal.x, &normal.y, &normal.z);
      normals.push_back(normal);
    } else if (strcmp(lineHeader, "f") == 0) {
      std::string vertex1, vertex2, vertex3;
      unsigned int vertexIndex[3], uvIndex[3], normalIndex[3];
      int matches = fscanf(file, "%d/%d/%d %d/%d/%d %d/%d/%d\n",
                           &vertexIndex[0], &uvIndex[0], &normalIndex[0],
                           &vertexIndex[1], &uvIndex[1], &normalIndex[1],
                           &vertexIndex[2], &uvIndex[2], &normalIndex[2]);
      if (matches != 9) {
        printf("File can't be read by our simple parser :-( Try exporting with "
               "other options\n");
        fclose(file);
        return;
      }

      glBindTexture(GL_TEXTURE_2D, 1);
      glBegin(GL_TRIANGLES);

      glTexCoord2f(uvs[uvIndex[0] - 1].x, uvs[uvIndex[0] - 1].y);
      glNormal3f(normals[normalIndex[0] - 1].x, normals[normalIndex[0] - 1].y,
                 normals[normalIndex[0] - 1].z);
      glVertex3f(vertices[vertexIndex[0] - 1].x, vertices[vertexIndex[0] - 1].y,
                 vertices[vertexIndex[0] - 1].z);

      glTexCoord2f(uvs[uvIndex[1] - 1].x, uvs[uvIndex[1] - 1].y);
      glNormal3f(normals[normalIndex[1] - 1].x, normals[normalIndex[1] - 1].y,
                 normals[normalIndex[1] - 1].z);
      glVertex3f(vertices[vertexIndex[1] - 1].x, vertices[vertexIndex[1] - 1].y,
                 vertices[vertexIndex[1] - 1].z);

      glTexCoord2f(uvs[uvIndex[2] - 1].x, uvs[uvIndex[2] - 1].y);
      glNormal3f(normals[normalIndex[2] - 1].x, normals[normalIndex[2] - 1].y,
                 normals[normalIndex[2] - 1].z);
      glVertex3f(vertices[vertexIndex[2] - 1].x, vertices[vertexIndex[2] - 1].y,
                 vertices[vertexIndex[2] - 1].z);

      glEnd();
    } else {
      // Probably a comment, eat up the rest of the line
      char stupidBuffer[1000];
      fgets(stupidBuffer, 1000, file);
    }
  }

  glPopMatrix();
  glEndList();
  fclose(file);
  return;
}

GLuint LoadTexture(GLuint tex, const char *filename, int width, int height) {
  // bmp 24 bit
  unsigned char *data;
  unsigned char R, G, B;
  FILE *file;

  // open .bmp
  file = fopen(filename, "rb");

  if (file == NULL)
    return 0;
  // get memory for data
  data = (unsigned char *)malloc(width * height * 3);
  // data skip offset
  fseek(file, 128, 0);
  // read file to data
  fread(data, width * height * 3, 1, file);
  // close file
  fclose(file);

  // transpose R,G,B values
  int index;
  for (int i = 0; i < width * height; ++i) {
    index = i * 3;
    B = data[index];
    G = data[index + 1];
    R = data[index + 2];
    data[index] = R;
    data[index + 1] = G;
    data[index + 2] = B;
  }

  // create a texture
  glGenTextures(1, &tex);
  glBindTexture(GL_TEXTURE_2D, tex);
  gluBuild2DMipmaps(GL_TEXTURE_2D, 3, width, height, GL_RGB, GL_UNSIGNED_BYTE,
                    data);

  // texture filtering
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
  glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL);
  // glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);

  // free memory
  free(data);
  return 0;
}

// wavefront .obj loader code ends here
void reshape(int w, int h) {
  glViewport(0, 0, w, h);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluPerspective(60, (GLfloat)w / (GLfloat)h, 0.1, 1000.0);
  // glOrtho(-25,25,-2,2,0.1,100);
  glMatrixMode(GL_MODELVIEW);
}

void drawElephant() {
  glPushMatrix();
  glTranslatef(elephanttrans, 0, -4);
  glRotatef(elephantrot, 0, 1, 0);

  glCallList(elephant);
  glPopMatrix();

  elephantrot = elephantrot + 0.5;
  if (elephantrot > 360)
    elephantrot = elephantrot - 360;
  usleep(2000);
}

void display(void) {
  glClearColor(0.0, 0.0, 0.0, 1.0);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glLoadIdentity();
  drawElephant();
  glutSwapBuffers(); // swap the buffers
}

int main(int argc, char **argv) {
  vertices.push_back({0, 0, 0});
  glutInit(&argc, argv);
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
  glutInitWindowSize(800, 450);
  glutInitWindowPosition(20, 20);
  glutCreateWindow("ObjLoader");
  glutReshapeFunc(reshape);
  glutDisplayFunc(display);
  glutIdleFunc(display);
  glEnable(GL_TEXTURE_2D);
  LoadTexture(1, "data/uvtemplate.bmp", 512, 512);
  loadObj("data/Cube.obj");

  glutMainLoop();
  return 0;
}
