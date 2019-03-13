#include "stdio.h"
#include "../headers/Can.h"
//
//const CanHardwareObjectType CanHardwareObjectConfig_Controller_A[] = {
//	{
//		.CanObjectId =				0,
//	},
//	{
//		.CanObjectId =				1,
//	},
//};

Can_ReturnType Can_SetControllerMode(uint8 Controller,Can_StateTransitionType Transition)
{
    return CAN_OK;
}
//
//Std_ReturnType Can_GetControllerErrorState( uint8 ControllerId, Can_ErrorStateType* ErrorStatePtr )
//{
//    printf("\nCan_GetControllerErrorState done");
//    return E_OK;
//}


//Std_ReturnType Can_SetBaudrate( uint8 Controller, uint16 BaudRateConfigID )
//{
//    printf("\nCan_SetBaudrate done");
//    return E_OK;
//}

Can_ReturnType Can_Write( Can_HwHandleType Hth, const Can_PduType* PduInfo )
{
    printf("\nCan_Write done and data is : %s",PduInfo->sdu);
    return CAN_OK;
}
//
//Std_ReturnType Can_SetIcomConfiguration( uint8 Controller, IcomConfigIdType ConfigurationId )
//{
//    printf("\nCan_SetIcomConfiguration done ");
//    return E_OK;
//}
