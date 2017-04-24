#include "paperbak.h"
#include <stdio.h>
#include <iostream>
using namespace std;

#define EPOCH_DIFF 11644473600LL
#define TEST_TIME 1483228800LL

struct HexCharStruct
{
  unsigned char c;
  HexCharStruct(unsigned char _c) : c(_c) { }
};

inline std::ostream& operator<<(std::ostream& o, const HexCharStruct& hs)
{
  return (o << std::hex << (int)hs.c);
}

inline HexCharStruct hex(unsigned char _c)
{
  return HexCharStruct(_c);
}

int main(int argc, char const *argv[]) {
  long long ll = (TEST_TIME + EPOCH_DIFF) * 10000000LL;
  FILETIME ft;
  ft.dwLowDateTime = (unsigned int)ll;
  ft.dwHighDateTime = ll >> 32;
  cout << "size of unsigned int " << sizeof(unsigned int) << endl;
  cout << "size of unsigned long " << sizeof(unsigned long) << endl;
  cout << "FILETIME:" << endl;
  cout << "LOW: " << ft.dwLowDateTime << endl;
  cout << "HIGH: " << ft.dwHighDateTime << endl;
  unsigned char *pft = (unsigned char *)&ft;
  for (int i = 0; i < 8; i++) {
    cout << i << " " << hex(pft[i]) << endl;
  };
  return 0;
}
