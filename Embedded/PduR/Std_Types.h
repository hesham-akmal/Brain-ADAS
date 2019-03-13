#ifndef STD_TYPES_H_
#define STD_TYPES_H_

typedef unsigned char uint8_t;
typedef unsigned short uint16_t;
typedef unsigned long uint32_t;

typedef uint8_t Std_ReturnType;

typedef char int8_t;
typedef short int16_t;
typedef long int32_t;

typedef float fp32_t;
typedef double fp64_t;

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
