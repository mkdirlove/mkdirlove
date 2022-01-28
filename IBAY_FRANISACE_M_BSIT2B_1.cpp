#include <iostream>
#include <queue>
using namespace std;

// Print the queue
void displayQueue(queue<int> Ibay)
{
	queue<int> Ace = Ibay;
	while (!Ace.empty()) {
		cout << ' ' << Ace.front();
		Ace.pop();
	}
	cout << "";
}

// Driver Code
int main()
{
	// Initialize the queue
	queue<int> Francis;

	// Push elements in the queue
	Francis.push(10);
	Francis.push(20);
	Francis.push(30);

	// Display all elements inside the queue
	cout << "Elements of Queue are: ";
	displayQueue(Francis);

	// Display elements in front
	cout << "\nElement at front is: " << Francis.front();

	// Display element in rear
	cout << "\nElement at back is: " << Francis.back();

	// Display elements after pop operation
	cout << "\nQueue after pop operation: ";
	Francis.pop();

	// Display all elements
	displayQueue(Francis);

	// Check if queue is empty or not
	if(!Francis.empty()){
		cout << "\nQueue is not empty";
	} else{
		cout << "\nQueue is empty";
	}

	// Dispaly the size of the queue
	cout << "\nSize of the Queue is: " << Francis.size();

	return 0;
}
