# Lex词法分析器Python版本实验说明



## 环境依赖
* Python 2.7(没有在3.5的情况下测试)
* networkx >= 1.11
* matplotlib >= 1.52
* Cheetah >= 2.4.4

其中networkx是Python的图论包，用于构建nfa与dfa。
</br>Cheetah是模板引擎，用于生成自动化代码
</br>然后matplotlib可以图形化图，更加直观
</br>麻烦助教安装一下了

## 实验目标
为了完成一个近似Lex的pyLex！！！

## 报告叙述思路
主要分为四个部分，第一部分会演示一下Lex的用法并表达一下膜拜之情；之后是自己pyLex的用法；第三部分会详细解释从re到dfa的转换过程；最后是讲解如何读取配置文件，如何生成代码，如何匹配等问题
</br>整个实验花费了有近一周的时间，从最初的懵逼到对于Lex的敬佩。。。我还是最后再抒情吧

## Lex词法分析器用法
### .l文件的组织结构
参考自[维基百科](https://zh.wikipedia.org/wiki/Lex)和[相关教程](https://www.ibm.com/support/knowledgecenter/zh/ssw_aix_71/com.ibm.aix.cmds3/lex.htm)
</br>lex 规范文件是.l结尾的文件，lex读取、分析，之后生成一份**可以被编译成可执行程序**的c代码。

>输入文件文件包含三部分：定义、规则和用户子例程。每部分必须用仅含定界符 %%（双百分号）的行和其他部分分开。格式是：

>定义</br>
%%</br>
规则</br>
%%</br>
用户子例程</br>

通常来说，我们在定义中引用库，第二部分定义正则与匹配成功后的操作，第三部分作为launcher，即为main函数，因为lex不会帮你写main。例如下面的[.l文件](../gaint/t.l)

    %{           
    #include <stdio.h>

    extern char *yytext;
    extern FILE *yyin;
    int sem_count = 0;

    %}
    %option noyywrap
    %%
    [1-9]+[0-9]*		printf("INTEGER[%s]",yytext);
    [0-9]*\.[0-9]*		{printf("DOUBLE[%s]",yytext);}


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
</br>
第一部分和第三部分会原封不动加入生成的代码中，我们可以看见在第一部分中引入了stdio的库为了后面的printf，定义了yytext，而在第三部分则是一个main，用于启动文件。
</br>关键的第二部分，我们给出了int和double的正则匹配，并定义了匹配成功的动作，yytext是约定好了的变量名，代表匹配成功的字符，我们相当于输出类型[变量]。之后运行：

    lex t.l

我用的是Linux-Fedora，Windows下是flex，key
