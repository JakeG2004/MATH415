#include <stdio.h>
#include <stdlib.h>

struct Node
{
    int data;
    struct Node* next;
};

typedef struct Node* NodePtr;
typedef struct Node Node;

void Enqueue(int data, NodePtr* head)
{
    //make new node
    NodePtr newNode = (NodePtr)malloc(sizeof(Node));
    if(newNode == NULL)
    {
        printf("Failed to alloc node\n");
        exit(-1);
    }

    //fill node data
    newNode -> data = data;
    newNode -> next = NULL;

    //handle empty queue
    if((*head) == NULL)
    {
        (*head) = newNode;
        return;
    }

    NodePtr p = *head;

    //traverse to end of queue
    while(p -> next != NULL)
    {
        p = p -> next;
    }

    //insert
    p -> next = newNode;
}

void Dequeue(NodePtr* head)
{
    if(*head == NULL)
    {
        printf("Trying to pop from empty stack\n");
        exit(-1);
    }

    //grab value from head
    int retVal = (*head) -> data;

    NodePtr p = *head;

    //reassign head
    *head = (*head) -> next;

    //break link and free
    p -> next = NULL;
    free(p);
}

void PrintQueue(NodePtr head)
{
    while(head != NULL)
    {
        printf("%i\n", head -> data);
        head = head -> next;
    }
}

void EraseQueue(NodePtr* head)
{
    NodePtr p = *head;
    NodePtr n = *head;

    while(p != NULL)
    {
        //get next node
        p = p -> next;

        //break chain and free
        n -> next = NULL;
        free(n);

        //increment
        n = p;
    }

    *head = NULL;
}