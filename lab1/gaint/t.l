%{           
#include <stdio.h> 

extern char *yytext;
extern FILE *yyin;
int sem_count = 0;

%}
%option noyywrap
%%
[0-9]*\.[0-9]*		{printf("DOUBLE[%s]",yytext);}
[1-9]+[0-9]*		printf("INTEGER[%s]",yytext);
[a-zA-Z][a-zA-Z0-9]*    {printf("WORD[%s] ", yytext);}
[a-zA-Z0-9//.-]+        printf("FILENAME ");

%%
//上面为规则定义部分，以下为函数定义部分
int main(int avgs, char *avgr[])
{
    yyin = fopen(avgr[1], "r");
    if (!yyin)
    {
        return 0;
    }
    yylex();
    printf("sem_count : %d/n\n", sem_count);
    fclose(yyin);

    return 1;
}


