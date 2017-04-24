// WINDOWS

#if defined(_WIN64)
 typedef __int64 LONG_PTR;
#else
 typedef long LONG_PTR;
#endif

#if defined(_WIN64)
 typedef unsigned __int64 UINT_PTR;
#else
 typedef unsigned int UINT_PTR;
#endif

typedef UINT_PTR WPARAM;

#define MAXPATH 4096

typedef void * PVOID;
typedef unsigned int DWORD; // officialy long, but linux long have 8 instead of 4 bytes
typedef unsigned char BYTE;
typedef unsigned short WORD;
typedef long LONG;
typedef PVOID HANDLE;
typedef HANDLE HDC;
typedef HANDLE HFONT;
typedef HANDLE HBITMAP;
typedef HANDLE HWND;
typedef HANDLE HGLOBAL;
typedef HANDLE HINSTANCE;
typedef HANDLE HBRUSH;

typedef LONG_PTR LPARAM;


typedef struct _FILETIME {
  DWORD dwLowDateTime;
  DWORD dwHighDateTime;
} FILETIME, *PFILETIME;

typedef struct tagBITMAPINFOHEADER {
  DWORD biSize;
  LONG  biWidth;
  LONG  biHeight;
  WORD  biPlanes;
  WORD  biBitCount;
  DWORD biCompression;
  DWORD biSizeImage;
  LONG  biXPelsPerMeter;
  LONG  biYPelsPerMeter;
  DWORD biClrUsed;
  DWORD biClrImportant;
} BITMAPINFOHEADER, *PBITMAPINFOHEADER;

typedef struct tagRGBQUAD {
  BYTE rgbBlue;
  BYTE rgbGreen;
  BYTE rgbRed;
  BYTE rgbReserved;
} RGBQUAD;

typedef struct tagBITMAPINFO {
  BITMAPINFOHEADER bmiHeader;
  RGBQUAD          bmiColors[1];
} BITMAPINFO, *PBITMAPINFO;
