#include "Can_Cfg.h"
#include "Can_GeneralTypes.h"
#include "ComStack_Types.h"

/** @req 4.0.3/CAN039 */
typedef enum {
	CAN_OK,
	CAN_NOT_OK,
	CAN_BUSY
} Can_ReturnType;

 /* @req CAN429 */
typedef uint8 Can_HwHandleType;

/** @req 4.0.3/CAN416 */
// uint16: if only Standard IDs are used
// uint32: if also Extended IDs are used
typedef uint32 Can_IdType;

/** @req 4.0.3/CAN415 */
typedef struct Can_PduType_s {
	// private data for CanIf,just save and use for callback
	PduIdType   swPduHandle;
	// the CAN ID, 29 or 11-bit
	Can_IdType 	id;
	// Length, max 8 bytes
	uint8		length;
	// data ptr
	uint8 		*sdu;
} Can_PduType;

Can_ReturnType Can_Write(Can_HwHandleType hth, Can_PduType *pduInfo);

void Can_InitController(Can_ControllerConfigType *canx_config);
void Can_Init(const Can_ConfigType* Config);
void Can_MainFunction_Write(void);
void Can_MainFunction_Read(void);
Can_ReturnType Can_Write(Can_HwHandleType hth, Can_PduType *pduInfo);