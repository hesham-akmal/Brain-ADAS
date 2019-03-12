/** incomplete COM stack types file used as a test to PDUR module */

#ifndef COMSTACK_TYPES_H_
#define COMSTACK_TYPES_H_

#include "Std_Types.h"
#include "types.h"

typedef uint16_t PduIdType;
typedef uint16_t PduLengthType;
typedef uint8 IcomConfigIdType;

typedef enum {
    ICOM_SWITCH_E_OK=0,
    ICOM_SWITCH_E_FAILED=1
}IcomSwitch_ErrorType;



typedef struct {
	uint8_t *SduDataPtr;			  // payload
	PduLengthType SduLength;	// length of SDU
} PduInfoType;

typedef enum {
	TP_DATACONF,
	TP_DATARETRY,
	TP_CONFPENDING,
	TP_NORETRY,
} TpDataStateType;

typedef struct {
	TpDataStateType TpDataState;
	PduLengthType   TxTpDataCnt;
} RetryInfoType;

typedef enum {
	BUFREQ_OK=0,
	BUFREQ_NOT_OK,
	BUFREQ_BUSY,
	BUFREQ_OVFL
} BufReq_ReturnType;

typedef enum {
    TP_STMIN=0,
    TP_BS,
    TP_BC
}TPParameterType;



#endif //COMSTACK_TYPES_H_
