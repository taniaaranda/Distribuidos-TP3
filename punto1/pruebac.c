#include <stdio.h>

int main(int argc, char *argv[])
{
	// Si esta primera linea se comenta se producira un error...
	//printf("Content-type: text/html%c%c", 10, 10);
    printf("Content-type: text/html\n\n");
	printf("<HTML><BODY>\n");
	printf("<font color = blue>\n");
	printf("<h1 style=\"TEXT-ALIGN: center\">Hey, ahora si</h1>\n");

	printf("</font>\n");
	printf("Esto no es un error\n");
	printf("</BODY></HTML>\n");
    return 0;
}
