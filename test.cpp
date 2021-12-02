
#include <stdio.h>
int main()
{

    int a[5] = {10, 20, 30, 40, 50}, b[4] = {60, 70, 80, 90}, c[9], i;

    for (i = 0; i < 5; i++)
    {
        printf("a=%d", a[i]);
    }
    printf("\n");
    for (i = 0; i < 4; i++)
    {
        printf("b=%d", b[i]);
    }
    printf("\n");
    for (i = 0; i < 5; i++)
    {
        c[i] = a[i];
    }
    for (i = 0; i < 5; i++)
        ;
    {
        printf("c=%d", c[i]);
    }
    for (i = 0; i < 4; i++)
    {
        c[i] = b[i];
    }
    for (i = 0; i < 4; i++)
    {
        printf("c=%d", c[i]);
    }

    return 0;
}
