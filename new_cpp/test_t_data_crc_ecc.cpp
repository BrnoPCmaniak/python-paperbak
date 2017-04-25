#include <stdio.h>
#include <iostream>

#include "hex_print.h"
#include "Crc16.h"
#include "Ecc.h"
#include "test_data.h"
#include "paperbak.h"

using namespace std;

int main(int argc, char const *argv[]) {
  t_data block = {15, TEST_DATA};
  t_data *blockptr = &block;
  cout << "address: " << block.addr << endl;

  unsigned char * blockcharptr = (unsigned char *)blockptr;
  cout << "BLOCK" << endl;
  for (int i = 0; i < NDATA+sizeof(DWORD); i++){
    cout << i << " " << HexToString(blockcharptr[i]) << endl;
  }

  // Add CRC.
  blockptr->crc=(ushort)(Crc16((unsigned char *)blockptr,NDATA+sizeof(DWORD))^0x55AA);
  // Add error correction code.
  Encode8((unsigned char *)blockptr,blockptr->ecc,127);

  cout << "CRC: " << block.crc << endl;
  cout << "ECC:" << endl;
  unsigned char *pft = (unsigned char *)&block.ecc;
  for (int i = 0; i < 32; i++){
    cout << i << " " << HexToString(pft[i]) << endl;
  }
  return 0;
}
