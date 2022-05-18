#include <stdio.h>

int main() {
    char *s = NULL;
    size_t len = 0;
    getline(&s, &len, stdin);
    printf("%s", s);
    return 0;
}
