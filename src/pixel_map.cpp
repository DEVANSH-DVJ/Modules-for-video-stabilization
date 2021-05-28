#include <GL/gl.h>
#include <GL/glut.h>

#include <iostream>
#include <unistd.h>
#include <vector>

using namespace std;

struct point {
  float x, y, z;
};
struct pointd {
  GLdouble x, y, z;
};

GLdouble coords[] = {0.5, 0.5, 1.0}; // current 3d coords

GLdouble model_view[16];
GLdouble projection[16];
GLint viewport[4];

GLuint elephant;
float elephantrot, elephanttrans = 0.0;
char ch = '1';
vector<point> vertices;

int width = 500;
int height = 500;

vector<vector<pointd>>
    img2obj_map(height, vector<pointd>(width, {10000000, 10000000, 10000000}));
vector<vector<pointd>> img2img_map(height, vector<pointd>(width, {-2, -2, 2}));

// wavefront .obj loader code begins
void loadObj(char *fname) {
  FILE *fp;
  int read;
  GLfloat x, y, z;
  char ch;
  elephant = glGenLists(1);
  fp = fopen(fname, "r");
  if (!fp) {
    printf("can't open file %s\n", fname);
    exit(1);
  }
  glPointSize(2.0);
  glNewList(elephant, GL_COMPILE);

  glPushMatrix();
  while (!(feof(fp))) {
    read = fscanf(fp, "%c %f %f %f", &ch, &x, &y, &z);
    if (read == 4 && ch == 'v') {

      vertices.push_back({x, y, z});
    }
  }
  fclose(fp);
  fp = fopen(fname, "r");
  int q1, q2, q2_, q3, q4, q4_, q5, q6, q6_;
  glBegin(GL_TRIANGLES);
  while (!(feof(fp))) {
    read = fscanf(fp, "%c %d/%d/%d %d/%d/%d %d/%d/%d", &ch, &q1, &q2, &q2_, &q3,
                  &q4, &q4_, &q5, &q6, &q6_);
    if (read == 10 && ch == 'f') {
      glColor3f((vertices[q1].x + 1) / 2, (vertices[q1].y + 1) / 2,
                (vertices[q1].z + 1) / 2);
      glVertex3f(vertices[q1].x, vertices[q1].y, vertices[q1].z);
      glColor3f((vertices[q2].x + 1) / 2, (vertices[q2].y + 1) / 2,
                (vertices[q2].z + 1) / 2);
      glVertex3f(vertices[q3].x, vertices[q3].y, vertices[q3].z);
      glColor3f((vertices[q3].x + 1) / 2, (vertices[q3].y + 1) / 2,
                (vertices[q3].z + 1) / 2);
      glVertex3f(vertices[q5].x, vertices[q5].y, vertices[q5].z);
    }
  }

  glEnd();

  glPopMatrix();
  glEndList();

  fclose(fp);
}
// wavefront .obj loader code ends here

void reshape(int w, int h) {
  glViewport(0, 0, w, h);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();

  gluPerspective(60, 1, 2.0, 50.0);
  glMatrixMode(GL_MODELVIEW);
}

void drawElephant() {
  glPushMatrix();

  glTranslatef(elephanttrans, 0.00, -8.0);
  glColor3f(1.0, 0.23, 0.27);
  glRotatef(45, 1, 1, 0);

  glCallList(elephant);

  glGetDoublev(GL_MODELVIEW_MATRIX, model_view);

  glGetDoublev(GL_PROJECTION_MATRIX, projection);

  glGetIntegerv(GL_VIEWPORT, viewport);

  glPopMatrix();
}

void drawElephant1() {
  glPushMatrix();

  glTranslatef(elephanttrans, 0.00, -8.0);
  glColor3f(1.0, 0.23, 0.27);

  glCallList(elephant);

  glGetDoublev(GL_MODELVIEW_MATRIX, model_view);

  glGetDoublev(GL_PROJECTION_MATRIX, projection);

  glGetIntegerv(GL_VIEWPORT, viewport);

  glPopMatrix();
}

void img2obj() {
  GLfloat z__;
  GLdouble x1, y1, z1;

  for (int i = 0; i < height; ++i) {
    for (int j = 0; j < width; ++j) {
      glReadPixels(i, j, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &z__);

      gluUnProject(i, j, z__, model_view, projection, viewport, &x1, &y1, &z1);

      img2obj_map[i][j] = {x1, y1, z1};
    }
  }
  cout << img2obj_map[264][268].x << " " << img2obj_map[264][268].y << " "
       << img2obj_map[264][268].z << "\n";
}

void img2img() {
  vector<vector<GLdouble>> depths(height, vector<GLdouble>(width, 2));
  GLdouble x_, y_, z_;
  for (int i = 0; i < height; ++i) {
    for (int j = 0; j < width; ++j) {
      if (img2obj_map[i][j].z != 10000000) {
        gluProject(img2obj_map[i][j].x, img2obj_map[i][j].y,
                   img2obj_map[i][j].z, model_view, projection, viewport, &x_,
                   &y_, &z_);
        if (z_ < depths[i][j]) {
          depths[i][j] = z_;
          img2img_map[i][j].x = x_;
          img2img_map[i][j].y = y_;
          img2img_map[i][j].z = z_;
        }
      }
    }
  }
  cout << img2img_map[264][268].x << " " << img2img_map[264][268].y << "\n";
}

void display(void) {
  glClearColor(0.0, 0.0, 0.0, 1.0);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glLoadIdentity();
  drawElephant();
  glFlush();
  img2obj();

  sleep(2);

  glClearColor(0.0, 0.0, 0.0, 1.0);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glLoadIdentity();
  drawElephant1();
  glFlush();
  img2img();

  sleep(3);
}

int main(int argc, char **argv) {
  vertices.push_back({0, 0, 0});

  glutInit(&argc, argv);

  glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH);

  glutInitWindowSize(width, height);
  glutInitWindowPosition(20, 20);

  glutCreateWindow("ObjLoader");

  glutReshapeFunc(reshape);
  glutDisplayFunc(display);
  glutIdleFunc(display);

  glEnable(GL_DEPTH_TEST);

  loadObj("data/Cube.obj");

  glutMainLoop();

  return 0;
}
