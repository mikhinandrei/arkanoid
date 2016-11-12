#include <iostream>

using namespace std;

struct find_parent_function_return{
    Node* parent;
    char direction;
};

class Node{
    public:
    Node(int);
    Node *left;
    Node *right;
    int value;
};

class Binary_tree{
    public:
    int find(int);
    void add(int);
    bool contains(int);
    bool remove(Node*, int);
    void out();
    Node *head;

    private:
    void insert(Node*, int);
    find_parent_function_return find_parent(Node*);
    Node* find_left(Node*);
};

int main() {
    char answer, choose;
    int n;

    Binary_tree tree;
    cout << "?????? ???-?????? ???????? ? ???????? (? - ??, ????????? - ???): ";
    cin >> answer;
    while (answer == '?'){
        cout << "1-????????, 2-???????, 3-?????, 4-?????: ";
        cin >> choose;
        switch (choose) {
            case '1':
                cin >> n;
                tree.add(n);
                break;
            case '2':
                cin >> n;
                tree.remove(tree.head, n);
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
                tree.out();
                break;
            default:
                cout << "Error";
                break;
        }
        cout << "?????? ??????????? (? - ??, ????????? - ???): ";
        cin >> answer;
    }
    return 0;
}

Node::Node(int val){
    value = val;
}

void Binary_tree::add(int val){
    if (head == NULL){
        head->value = val;
    }
    else{
        insert(head, val);
    }
}

void Binary_tree::insert(Node *node, int val){
    if (val < node->value){
        if (node->left == NULL) {
            node->left = new Node(val);
        }
        else{
            insert(node->left, val);
        }
    }
    else{
        if (node->right == NULL){
            node->right = new Node(val);
        }
        else{
            insert(node->right, val);
        }
    }
}

bool Binary_tree::remove(Node *node, int val){
    if (node == NULL){
        return false;
    }
    if (val > node->value){
        remove(node->right, val);
    }
    else{
        if (val < node->value){
            remove(node->left, val);
        }
        else {  // val == node->value
            find_parent_function_return found = find_parent(node);
            Node *n;
            switch (found.direction){
                case 'l':
                    n = found.parent->left;
                    break;
                case 'r':
                    n = found.parent->right;
                    break;
            }
            if ((node->left == NULL) && (node->right == NULL)){
                delete(node);
                n = NULL;
                return true;
            }
            if (node->left == NULL){
                n = node->right;
                delete(node);
                return true;
            }
            if (node->right == NULL){
                n = node->left;
                delete(node);
                return true;
            }
            if (node->right->left == NULL){
                node->value = node->right->value;
                node->right = node->right->right;
                return true;
            }
            else{
                Node *node1 = find_left(node->right);
                node->value = node1->value;
                find_parent_function_return found = find_parent(node1);
                found.parent->left = NULL;
            }
        }
    }
}