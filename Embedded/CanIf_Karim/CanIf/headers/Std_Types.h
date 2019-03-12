// #ifndef STD_TYPES_H
// #define STD_TYPES_H

// #ifndef NULL
// #define NULL 0
// #endif

#include "types.h"

typedef struct
{
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



#define STD_GET_VERSION (_major, _minor, _patch)(_major * 10000 + _minor * 100 + _patch)

/* Create Std_VersionInfoType */

#define STD_GET_VERSION_INFO(_vi, _module)                      \
	if (_vi != NULL)                                            \
	{                                                           \
		((_vi)->vendorID = _module##_VENDOR_ID);                \
		((_vi)->moduleID = _module##_MODULE_ID);                \
		((_vi)->sw_major_version = _module##_SW_MAJOR_VERSION); \
		((_vi)->sw_minor_version = _module##_SW_MINOR_VERSION); \
		((_vi)->sw_patch_version = _module##_SW_PATCH_VERSION); \
		((_vi)->ar_major_version = _module##_AR_MAJOR_VERSION); \
		((_vi)->ar_minor_version = _module##_AR_MINOR_VERSION); \
		((_vi)->ar_patch_version = _module##_AR_PATCH_VERSION); \
	}

#ifndef MIN
#define MIN(_x, _y) (((_x) < (_y)) ? (_x) : (_y))
#endif
#ifndef MAX
#define MAX(_x, _y) (((_x) > (_y)) ? (_x) : (_y))
#endif

typedef uint8 Std_ReturnType;

#define E_OK (Std_ReturnType)0
#define E_NOT_OK (Std_ReturnType)1

#define E_NO_DTC_AVAILABLE (Std_ReturnType)2
#define E_SESSION_NOT_ALLOWED (Std_ReturnType)4
#define E_PROTOCOL_NOT_ALLOWED (Std_ReturnType)5
#define E_REQUEST_NOT_ACCEPTED (Std_ReturnType)8
#define E_REQUEST_ENV_NOK (Std_ReturnType)9
#ifndef E_PENDING
#define E_PENDING (Std_ReturnType)10
#endif
#define E_COMPARE_KEY_FAILED (Std_ReturnType)11
#define E_FORCE_RCRRP (Std_ReturnType)12

#define STD_HIGH 0x01
#define STD_LOW 0x00

#define STD_ACTIVE 0x01
#define STD_IDLE 0x00

#define STD_ON 0x01
#define STD_OFF 0x00


/** @} */