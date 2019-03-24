#ifndef STD_TYPES_H_
#define STD_TYPES_H_

#include "stdbool.h"

typedef unsigned char uint8_t;
typedef unsigned short uint16_t;
typedef unsigned long uint32_t;

typedef uint8_t Std_ReturnType;

typedef unsigned char uint8;
typedef unsigned short uint16;
typedef unsigned long uint32;

typedef uint8 Std_ReturnType;

typedef char int8_t;
typedef short int16_t;
typedef long int32_t;

typedef char int8;
typedef short int16;
typedef long int32;

typedef float fp32_t;
typedef double fp64_t;

typedef struct {
    /* Recheck */
    uint16 vendorID;
    uint16 moduleID;
    uint8 instanceID;

    uint8 sw_major_version; /* Vendor numbers */
    uint8 sw_minor_version; /* Vendor numbers */
    uint8 sw_patch_version; /* Vendor numbers */

    uint8 ar_major_version; /* Autosar spec. numbers */
    uint8 ar_minor_version; /* Autosar spec. numbers */
    uint8 ar_patch_version; /* Autosar spec. numbers */
} Std_VersionInfoType;



#ifndef NULL
#define NULL 0
#endif

#ifndef TRUE
#define TRUE	(1U)
#endif

#ifndef FALSE
#define FALSE	(0U)
#endif

#define STD_HIGH		0x01
#define STD_LOW			0x00

#define STD_ACTIVE	0x01
#define STD_IDLE		0x00

#define STD_ON			0x01
#define STD_OFF			0x00

#define E_OK 				(Std_ReturnType)0
#define E_NOT_OK 		(Std_ReturnType)1

#endif
