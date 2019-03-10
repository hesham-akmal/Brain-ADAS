#include "types.h"
#include "ComStack_Types.h"

typedef enum Can_ReturnType
{
	CAN_OK,		/* Successful operation */
	CAN_NOT_OK, /* Error occurred or wakeup event occurred during sleep transition */
	CAN_BUSY	/* Transmit request not processed because no transmit object was available*/
} Can_ReturnType;

typedef enum Can_StateTransitionType
{
	CAN_T_STOP, /* Cannot request mode CAN_UNINIT */
	CAN_T_START,
	CAN_T_SLEEP,
	CAN_T_WAKEUP
} Can_StateTransitionType;

typedef struct Can_PduType
{
	PduIdType swPduHandle;
	uint8 length;
	Can_IdType id;
	uint8 *sdu;
} Can_PduType;

typedef uint16 Can_HwHandleType;
typedef uint32 Can_IdType;

Can_ReturnType Can_SetControllerMode(uint8 Controller, Can_StateTransitionType Transition);

Can_ReturnType Can_Write(Can_HwHandleType Hth, const Can_PduType *PduInfo)