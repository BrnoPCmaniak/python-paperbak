#include <stdio.h>
#include <iostream>

#include "Crc16.h"
#include "test_data.h"

using namespace std;

unsigned char DATA[90] = TEST_DATA;

int main(int argc, char const *argv[]) {
  cout << "CRC of test data is: " << Crc16(&DATA[0], 90) << endl;
  return 0;
}
