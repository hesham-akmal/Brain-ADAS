#include "ComStack_Types.h"
#include "Can_GeneralTypes.h"


Can_ReturnType Can_SetControllerMode(uint8 Controller, Can_StateTransitionType Transition);

Can_ReturnType Can_Write(Can_HwHandleType Hth, const Can_PduType *PduInfo);

