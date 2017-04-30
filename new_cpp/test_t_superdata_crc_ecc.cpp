#include <stdio.h>
#include <string.h>
#include <iostream>

#include "hex_print.h"
#include "Crc16.h"
#include "Ecc.h"
#include "test_data.h"
#include "paperbak.h"

using namespace std;

#define EPOCH_DIFF 11644473600LL
#define TEST_TIME 1483228800LL

int main(int argc, char const *argv[]) {
  t_superdata block;
  block.addr = 0xFFFFFFFF;
  block.datasize = 90;
  block.pagesize = 1;
  block.origsize = 90;
  block.mode = 1;
  block.attributes = 0x80;
  block.page = 1;
  block.filecrc = 31055;
  memset(block.name, 0, 64); // on python there will be all zeros if empty
  block.name[0] = 'R';
  block.name[1] = 'E';
  block.name[2] = 'A';
  block.name[3] = 'D';
  block.name[4] = 'M';
  block.name[5] = 'E';
  block.name[6] = '.';
  block.name[7] = 't';
  block.name[8] = 'x';
  block.name[9] = 't';

  // set time
  long long ll = (TEST_TIME + EPOCH_DIFF) * 10000000LL;
  block.modified.dwLowDateTime = (unsigned int)ll;
  block.modified.dwHighDateTime = ll >> 32;

  t_superdata *blockptr = &block;
  cout << "address: " << block.addr << endl;
  cout << "datasize: " << block.datasize << endl;
  cout << "pagesize: " << block.pagesize << endl;
  cout << "origsize: " << block.origsize << endl;
  cout << "mode: " << +block.mode << endl;
  cout << "attributes: " << +block.attributes << endl;
  cout << "page: " << block.page << endl;
  cout << "filecrc: " << block.filecrc << endl;
  cout << "modified (unixtimestamp): " << TEST_TIME << endl;
  cout << "name: " << block.name << endl;

  unsigned char * blockcharptr = (unsigned char *)blockptr;
  cout << "###BLOCK:" << endl;
  for (int i = 0; i < NDATA+sizeof(DWORD); i++){
    cout << HexToString(blockcharptr[i]) << ", " << endl;
  }

  // Add CRC.
  blockptr->crc=(ushort)(Crc16((unsigned char *)blockptr,NDATA+sizeof(DWORD))^0x55AA);
  // Add error correction code.
  Encode8((unsigned char *)blockptr,blockptr->ecc,127);

  cout << "CRC: " << block.crc << endl;
  cout << "###ECC:" << endl;
  unsigned char *pft = (unsigned char *)&block.ecc;
  for (int i = 0; i < 32; i++){
    cout << HexToString(pft[i]) << ", "  << endl;
  }
  return 0;
}
