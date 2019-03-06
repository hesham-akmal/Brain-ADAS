#include "ComStack_Types.h"
#include "Can_GeneralTypes.h"

typedef enum
{
    CANIF_CS_UNINIT = 0, /* Default mode of each CAN controller after power on. */
    CANIF_CS_STOPPED,    /* CAN controller is halted and does not operate on the network */
    CANIF_CS_STARTED,    /* CAN controller is in full-operational mode.*/
    CANIF_CS_SLEEP       /* CAN controller is in SLEEP mode and can be woken up by an internal (SW) request or by a network event */
} CanIf_ControllerModeType;

typedef enum
{
    CANIF_NO_NOTIFICATION = 0, /* No transmit or receive event occurred for the requested L-PDU. */
    CANIF_TX_RX_NOTIFICATION   /* The requested Rx/Tx CAN L-PDU was successfully transmitted or received. */
} CanIf_NotifStatusType;

typedef enum
{
    CANIF_OFFLINE = 0,       /* Transmit and receive path of the corresponding channel are disabled */
    CANIF_TX_OFFLINE,        /* Transmit path of the corresponding channel is disabled. The receive path is enabled */
    CANIF_TX_OFFLINE_ACTIVE, /* Transmit path of the corresponding channel is in offline active mode. The receive path is disabled. CanIfTxOfflineActiveSupport = TRUE */
    CANIF_ONLINE             /* Transmit and receive path of the corresponding channel are enabled */
} CanIf_PduModeType;







typedef struct CanIf_ConfigType
{
    
    //pointer to private Configurations of CanIf
    const CanIfPrivateCfg *privateCfg;
    

//------------------------------------------

    /* Reference to the list of channel init configurations. */
    const CanIf_CtrlCfgType *ControllerConfig;

    /* Callout functions with respect to the upper layers. This callout
	 *  functions defined in this container are common to all
	 *  configured underlying CAN Drivers / CAN Transceiver Drivers */
    const CanIf_DispatchCfgType *DispatchConfig;

    /* This container contains the init parameters of the CAN Interface. */
    const CanIf_InitCfgType *InitConfig;

    /* Needed? */
    const Can_ControllerIdType *ChannelToControllerMap;

    const uint8 *ChannelDefaultConfIndex;


} CanIf_ConfigType;
