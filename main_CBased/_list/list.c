/* list.c — функції для підтримки операцій зі списком */
#include <stdio.h>
#include <stdlib.h>
#include "list.h"

#define PET_NAME_LEN 30

typedef struct item
{
    char petname[PET_NAME_LEN]; /* ім’я домашнього улюбленця */
    char petkind[PET_NAME_LEN]; /* вид домашнього улюбленця */
} Item;                       /* визначення типу елемента списку */

typedef struct node
{
    Item item;               /* елемент списку */
    struct node * next;      /* вказівник на наступний вузол */
} Node;

typedef Node* List;         /* визначення типу списку */

/* прототип локальної функції */
static void CopyToNode(Item item, Node * pnode);

/* функції інтерфейсу */
/* встановлює список у порожній стан */
void InitializeList(List * plist) {*plist = NULL;}

/* повертає true, якщо список порожній */
_Bool ListIsEmpty(const List * plist) {return *plist == NULL ?  1 : 0;}

/* повертає true, якщо список заповнений */
_Bool ListIsFull(const List * plist)
{
    Node * pt;
    _Bool full;

    pt = (Node *) malloc(sizeof(Node));

    full = pt == NULL ? 1 : 0;

    free(pt);

    return full;
}

/* повертає кількість вузлів */
unsigned int ListItemCount(const List * plist)
{
    unsigned int count = 0;
    Node * pnode = *plist;    /* встановлення на початок списку */

    while (pnode != NULL)
    {
        ++count;
        pnode = pnode->next;  /* перехід до наступного вузла */
    }

    return count; 
}

/* створює вузол для зберігання елемента і додає його в кінець */
/* списку, вказаного змінною plist (повільна реалізація) */
_Bool AddItem(Item item, List * plist)
{
    Node * pnew;
    Node * scan = *plist;

    pnew = (Node*)malloc(sizeof(Node));

    if (pnew == NULL) return 0;        /* вихід із функції в разі помилки */

    CopyToNode(item, pnew);
    pnew->next = NULL;
    if (scan == NULL)          /* список порожній, тому розмістити */
        *plist = pnew;         /* pnew на початок списку            */
    else
    {
        while (scan->next != NULL)
            scan = scan->next;  /* пошук кінця списку       */
        scan->next = pnew;      /* додавання pnew в кінець  */
    }

    return 1;
}

/* проходить кожен вузол і виконує функцію, вказану pfun */
void Traverse  (const List * plist, void (* pfun)(Item item) )
{
    Node * pnode = *plist;    /* встановлення на початок списку */

    while (pnode != NULL)
    {
        (*pfun)(pnode->item); /* застосування функції до елемента */
        pnode = pnode->next;  /* перехід до наступного елемента */
    }
}

/* звільняє пам’ять, виділену за допомогою malloc() */
/* встановлює покажчик списку в NULL                */
void EmptyTheList(List * plist)
{
    Node * psave;

    while (*plist != NULL)
    {
        psave = (*plist)->next; /* збереження адреси наступного вузла */
        free(*plist);           /* звільнення поточного вузла          */
        *plist = psave;         /* перехід до наступного вузла         */
    }
}

/* визначення локальної функції */
/* копіює елемент у вузол       */
static void CopyToNode(Item item, Node * pnode) {pnode->item = item; } /* копіювання структури */
