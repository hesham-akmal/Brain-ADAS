#include "ComStack_Types.h"
#include "Can_GeneralTypes.h"


#define     CAN_INF_HARDWARE_OBJECT_REF_0 &CanHardwareObjectConfig_Controller_A[0]
#define     CAN_INF_HARDWARE_OBJECT_REF_1 &CanHardwareObjectConfig_Controller_A[1]

extern const CanHardwareObject CanHardwareObjectConfig_Controller_A[];

Std_ReturnType Can_SetBaudrate(uint8 Controller, uint16 BaudRateConfigID);
Can_ReturnType Can_SetControllerMode(uint8 Controller, Can_StateTransitionType Transition);
Can_ReturnType Can_Write(Can_HwHandleType Hth, const Can_PduType *PduInfo);
