#include<GL/gl.h>
#include<GL/glut.h>
#include<stdio.h>
#include<vector>
using namespace std;

//globals
struct point{
	float x,y,z;
};

GLuint elephant;
float elephantrot, elephanttrans;
char ch='1';
vector<point> vertices;

//other functions and main
//wavefront .obj loader code begins
void loadObj(char *fname)
{
    FILE *fp;
    int read;
    GLfloat x, y, z;
    char ch;
    elephant=glGenLists(1);
    fp=fopen(fname,"r");
    if (!fp)
    {
        printf("can't open file %s\n", fname);
        exit(1);
    }
    glPointSize(2.0);
    glNewList(elephant, GL_COMPILE);
    {
        glPushMatrix();
        //glBegin(GL_POINTS);
        while(!(feof(fp)))
        {
            read=fscanf(fp,"%c %f %f %f",&ch,&x,&y,&z);
            if(read==4&&ch=='v')
            {
            	vertices.push_back({x,y,z});
                //glVertex3f(x,y,z);
            }
        }
        fclose(fp);
        fp=fopen(fname,"r");
        int q1,q2,q3,q4,q5,q6;
        glBegin(GL_TRIANGLES);
        while(!(feof(fp)))
        {
            read=fscanf(fp,"%c %d//%d %d//%d %d//%d",&ch,&q1,&q2,&q3,&q4,&q5,&q6);
            if(read==7&&ch=='f')
            {
            	glVertex3f(vertices[q1].x,vertices[q1].y,vertices[q1].z);
            	glVertex3f(vertices[q3].x,vertices[q3].y,vertices[q3].z);
            	glVertex3f(vertices[q5].x,vertices[q5].y,vertices[q5].z);
                //glVertex3f(x,y,z);
            }
        }
        //glBegin(GL_POINTS);

        glEnd();
    }
    glPopMatrix();
    glEndList();
    fclose(fp);
}
//wavefront .obj loader code ends here
void reshape(int w,int h)
{
    glViewport(0,0,w,h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective (60, (GLfloat)w / (GLfloat)h, 0.1, 1000.0);
    //glOrtho(-25,25,-2,2,0.1,100);
    glMatrixMode(GL_MODELVIEW);
}
void drawElephant()
{
    glPushMatrix();
    glTranslatef(elephanttrans,-40.00,-105);
    glColor3f(1.0,0.23,0.27);
    glScalef(0.1,0.1,0.1);
    glRotatef(elephantrot,0,1,0);
    glCallList(elephant);
    glPopMatrix();
    elephantrot=elephantrot+0.5;
    if(elephantrot>360)elephantrot=elephantrot-360;
    //elephanttrans=elephanttrans+0.1;

}
void display(void)
{
    glClearColor (0.0,0.0,0.0,1.0);
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();
    drawElephant();
    glutSwapBuffers(); //swap the buffers
}
int main(int argc,char **argv)
{
	vertices.push_back({0,0,0});
    glutInit(&argc,argv);
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH);
    glutInitWindowSize(800,450);
    glutInitWindowPosition(20,20);
    glutCreateWindow("ObjLoader");
    glutReshapeFunc(reshape);
    glutDisplayFunc(display);
    glutIdleFunc(display);
    loadObj("data/Elephant.obj");//replace elepham.obj withp orsche.obj or radar.obj or any other .obj to display it
    glutMainLoop();
    return 0;
}
