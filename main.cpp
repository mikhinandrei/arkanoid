#include <iostream>
#include <cstdlib>

using namespace std;

struct Node{
    Node *left = NULL;
    Node *right = NULL;
    int value;
};

class Binary_tree{
public:
    bool find(int);
    void add(int);
    bool remove(int);
    void out(Node*);
    Node *head = nullptr;

private:
    void insert(Node*, int);
    Node* find_with_parent(int, Node*&);
    Node* find_left(Node*);
};

int main() {
    char answer, choose;
    int n;

    setlocale(LC_ALL,"Russian");

    Binary_tree tree;
    cout << "Хотите что-нибудь сделать с деревом? (y - да, остальное - нет):  ";
    cin >> answer;
    while (answer == 'y'){
        cout << "1-вставить, 2-удалить, 3-найти, 4-вывод: ";
        cin >> choose;
        switch (choose) {
            case '1':
                cin >> n;
                tree.add(n);
                break;
            case '2':
                cin >> n;
                tree.remove(n);
                break;
            case '3':
                cin >> n;
                if(tree.find(n)){
                    cout << "Found!!!\n";
                }
                else{
                    cout << "Not found (\n";
                }
                break;
            case '4':
                tree.out(tree.head);
                break;
            default:
                cout << "Error";
                break;
        }
        cout << "Хотите продолжить? (д - да, остальное - нет): ";
        cin >> answer;
    }
    return 0;
}

void Binary_tree::add(int val){
    if (!(head)){
        Node *p;
        head = p;
        delete(p);
        head->value = val;
        head->right = nullptr;
    }
    else{
        insert(head, val);
    }
}

void Binary_tree::insert(Node *node, int val){
    if (val < node->value){
        if (node->left == nullptr) {
            node->left = new Node;
            node->left->value = val;
        }
        else{
            insert(node->left, val);
        }
    }
    else{
        if (node->right == nullptr){
            node->right = new Node;
            node->right->value = val;
        }
        else{
            insert(node->right, val);
        }
    }
}

bool Binary_tree::remove(int val){
    Node *current = nullptr;
    Node *parent;

    current = find_with_parent(val, *&parent);

    if (current == nullptr){
        return false;
    }
    //Если у удаляемого нет ребёнка справа, то его левый ребёнок идёт вверх
    if(current->right == nullptr){
        if (parent == nullptr){
            head = current->left;
        }
        else{
            if (parent->value > current->value) {
                parent->left = current->left;
            }
            else {
                parent->right = current->left;
            }
        }
        return true;
    }
    //Есть правый ребёнок без левого ребёнка
    if (current->right->left == nullptr){
        current->right->left = current->left;
        if (parent == nullptr){
            head = current->right;
        }
        else{
            if (parent->value > current->value) {
                parent->left = current->right;
            }
            else {
                parent->right = current->right;
            }
        }
        return true;
    }
    else {
        Node* leftmost = find_left(current->right);
        if (parent == nullptr){
            head->left = leftmost;
        }
        else{
            current->value = leftmost->value;
            Node *parent_leftmost;
            leftmost = find_with_parent(val, *&parent_leftmost);
            parent_leftmost->left = nullptr;
        }
    }
}

Node* Binary_tree::find_with_parent(int val, Node*& parent) {
    Node* current = head;

    while(current != nullptr){
        if (val < current->value){
            parent = current;
            current = current->left;
        }
        else{
            if (val > current->value){
                parent = current;
                current = current->right;
            }
            else{
                break;
            }
        }
    }
    return current;
}

bool Binary_tree::find(int val){
    Node *current = head;
    while ((current->value != val) && (current != nullptr)){
        cout << current->value << " -> ";
        if (val < current->value){
            current = current->left;
        }
        else{
            current = current->right;
        }
    }
    if (current == nullptr){
        return false;
    }
    cout << current->value << endl;
    return true;
};

void Binary_tree::out(Node* node){
    if (node){
        cout << node->value << " ";
    }
    if (node->left){
        out(node->left);
    }
    if (node->right){
        out(node->right);
    }
};

Node* Binary_tree::find_left(Node *node){
    if (node->left){
        return find_left(node->left);
    }
    else {
        return node;
    }
};
