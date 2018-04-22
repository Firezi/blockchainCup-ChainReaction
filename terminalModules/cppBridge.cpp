#include <Python.h>
#include <string>

using namespace std;

#include "Header.h"
__declspec(dllexport)
double __stdcall Add(char dir[], char name[], float price, float quantity, char time[], char sign[])
{
	Py_Initialize();
	pName = PyString_FromString();
	pModule = PyImport_Import("pushtrader.py");
	Py_Finalize();

}

