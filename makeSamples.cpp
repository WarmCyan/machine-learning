#include <iostream>
#include <cmath>
#include <cstdlib>
#include <fstream>

using namespace std;

int main()
{

	ofstream fileStream;
	fileStream.open("data.txt", ios::out | ios::app);
	


	//cout << "topology: 2 4 1" << endl;
	for (int i = 2000; i >= 0; --i)
	{
		int n1 = (int)(2.0 * rand() / double(RAND_MAX));
		int n2 = (int)(2.0 * rand() / double(RAND_MAX));
		int t = n1 ^ n2;
		//cout << "in: " << n1 << ".0 " << n2 << ".0 " << endl;
		//cout << "out: " << t << ".0" << endl;
		//cout << n1 << ".0," << n2 << ".0" << endl;
		//cout << t << ".0" << endl;
		fileStream << n1 << ".0," << n2 << ".0," << t << ".0" << endl; // in1,in2,out
		//fileStream << t << ".0" << endl;
	}

	fileStream.close();
}
