#include <stdio.h>     /* printf(), fgets(), fileno() */
#include <stdlib.h>    /* getenv() */
#include <string.h>    /* strchr() */
#include <sys/file.h>  /* flock() & friends */
// Nombre del archivo con todo el texto del chat
#define chatfname "data/chat.txt"
// Cantidad maxima de caracteres de una linea
#define MAXLINE 500
int main(int argc, char *argv[])
{
  char *reqmet, *querystr, linein[MAXLINE];
  FILE *chatfile;
  int fd_chatfile;
  // Definicion del tipo de respuesta...
  printf("Content-type: text/plain%c%c", 10, 10);
  // Variable de ambiente con el Query_String para un GET
  querystr = getenv("QUERY_STRING");
  //  Abrir el archivo
  chatfile = fopen(chatfname, "a+");
  if (chatfile == NULL)
    printf("Error opening the file<br>\n");
  // Obtener el fd del archivo y bloquearlo
  fd_chatfile = fileno(chatfile);
  if (flock(fd_chatfile, LOCK_EX) != 0)
    printf("<p> Error on flock()</p>\n");
  while (linein == fgets(linein, MAXLINE, chatfile))
    printf("%s", linein);
  fprintf(chatfile, "%s\n", strchr(querystr, '=')+1);
  // Unlock and close file
  flock(fd_chatfile, LOCK_UN);
  fclose(chatfile);
  printf("%s\n", strchr(querystr, '=')+1);
}
