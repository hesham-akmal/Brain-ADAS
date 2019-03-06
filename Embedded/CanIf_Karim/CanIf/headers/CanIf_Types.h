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

typedef enum
{
    BINARY,
    INDEX,
    LINEAR,
    TABLE
} CanIfPrivateSoftwareFilterType;

typedef enum
{
    UINT8,
    UINT16
} CanIfPublicHandleTypeEnum;

typedef enum
{
    EXTENDED,
    STANDARD
} CanIfHrhRangeRxPduRangeCanIdType;

typedef struct CanIfBufferCfg
{
    /* data */
} CanIfBufferCfg;

typedef struct CanIfRxPduCfg
{
    /* data */
} CanIfRxPduCfg;

typedef struct CanIfTxPduCfg
{

} CanIfTxPduCfg;







//-----------------------------------------------------------------
typedef struct CanIfHrhRangeCfg
{
    CanIfHrhRangeRxPduRangeCanIdType canIfHrhRangeRxPduRangeCanIdType;
    //BASEID + RANGEMASK = masked ID range in which all CAN Ids shall pass the software filtering
    uint32 CanIfHrhRangeBaseId;
    uint32 CanIfHrhRangeMask;
    //upper and lower bound of canIDs range
    uint32 CanIfHrhRangeRxPduLowerCanId;
    uint32 CanIfHrhRangeRxPduUpperCanId;
} CanIfHrhRangeCfg;
typedef struct CanIfHrhCfg
{
    //Reference to controller Id to which the HRH belongs to.
    const CanIfCtrlCfg *canIfHrhCanCtrlIdRef;

    //The parameter refers to a particular HRH object in the CanDrv configuration
    const CanHardwareObject *canIfHrhIdSymRef;

    //True: Software filtering is enabled False: Software filtering is enabled
    const bool canIfHrhSoftwareFilter;

    /*Defines the parameters required for configurating multiple CANID ranges for a given same HRH.*/
    const CanIfHrhRangeCfg *canIfHrhRangeCfg;

} CanIfHrhCfg;
typedef struct CanIfInitHohCfg
{
    //This container contains configuration parameters for each hardware receive object (HRH).
    const CanIfHrhCfg *canIfHrhCfg;
    //This container contains parameters related to each HTH.
    const CanIfHthCfg *canIfHthCfg;
} CanIfInitHohCfg;
typedef struct CanIfInitCfg
{
    /*Selects the CAN Interface specific configuration setup. This type of the
    external data structure shall contain the post build initialization data for
    the CAN Interface for all underlying CAN Dirvers.*/
    const uint8 *canIfInitCfgSet;
    // Maximum Total size of all Tx buffers
    const uint32 canIfMaxBufferSize;
    // Maximum number of Pdus.
    const uint32 canIfMaxRxPduCfg;
    // Maximum number of Pdus.
    const uint32 canIfMaxTxPduCfg;
    // this Container Contains The Txbuffer Configuration
    const CanIfBufferCfg *canIfBufferCfg;
    //This container contains the references to the configuration setup of each underlying CAN Driver.
    const CanIfInitHohCfg *canIfInitHohCfg;
    //This container contains the configuration (parameters) of each receive CAN L-PDU.
    const CanIfRxPduCfg *canIfRxPduCfg;
    //This container contains the configuration (parameters) of a transmit CAN L-PDU
    const CanIfTxPduCfg *canIfTxPduCfg;
} CanIfInitCfg;
typedef struct CanIfPrivateCfg
{
    //TRUE:  Minimum buffer element length is fixed to 8 Bytes.
    //FALSE: Buffer element length depends on the size of the referencing PDUs.
    bool CanIfFixedBuffer;
    //TRUE: Enabled
    //False : Disabled
    bool CanIfPrivateDlcCheck;
    //Selects the desired software filter mechanism for reception only.
    CanIfPrivateSoftwareFilterType canIfPrivateSoftwareFilterType;
} CanIfPrivateCfg;
typedef struct CanIfPublicCfg
{
    //Enable support for dynamic ID handling using L-SDU MetaData.
    bool canIfMetaDataSupport;

    //Enable or disable upper layer transmit cancel support
    bool canIfPublicCancelTransmitSupport;

    //Defines header files for callback functions which shall be included in case of CDDs
    uint8 *canIfPublicCddHeaderFile;

    //Switches the Default Error Tracer (Det) detection and notification ON or OFF
    bool canIfPublicDevErrorDetect;

    /*  This parameter is used to configure the Can_HwHandleType. The
        Can_HwHandleType represents the hardware object handles of a CAN
        hardware unit
    */
    CanIfPublicHandleTypeEnum canIfPublicHandleTypeEnum;

    //Selects support of Pretended Network features in CanIf. True: Enabled False: Disabled
    bool canIfPublicIcomSupport;

    //Selects support for multiple CAN Drivers.
    bool canIfPublicMultipleDrvSupport;

    //Selects support of Partial Network features in CanIf.
    bool canIfPublicPnSupport;

    //Enables-Disables the API CanIf_ReadRxPduData() for reading received L-SDU data.
    bool canIfPublicReadRxPduDataApi;

    //Enables and disables the API for reading the notification status of receive L-PDUs.
    bool canIfPublicReadRxPduNotifyStatusApi;

    //Enables and disables the API for reading the notification status of transmit L-PDUs.
    bool canIfPublicReadTxPduNotifyStatusApi;

    // Enables and diables the API for reconfiguation of the CAN Identifier for each transmit L-PDU
    bool canIfPublicSetDynamicTxIdApi;

    // Enables and diables the buffering of transmit L-Pdu within the CAN Interface Module
    bool canIfPublicTxBuffering;

    // Configuration parameter to enable/disable the API to poll for Tx Confirmation state
    bool canIfPublicTxConfirmPollingSupport;

    // Enables and disables the API for reading the version information about the CAN Interface.
    bool canIfPublicVersionInfoApi;

    /*  
        If enabled, only NM messages shall validate a detected wake-up event in CanIf. 
        If disabled, all received messages corresponding to a configured Rx PDU shall validate such a wake-up event.
    */
    bool canIfPublicWakeupCheckValidByNM

        //Selects support for wake up validation
        bool canIfPublicWakeupCheckValidSupport;

    // If this parameter is set to true the CanIf_SetBaudrate API shall be supported.
    bool canIfSetBaudrateApi;

    // Enables the CanIf_TriggerTransmit API at Pre-Compile-Time.
    bool canIfTriggerTransmitSupport;

    // Determines wether TxOffLineActive feature is supported by CanIf.
    bool canIfTxOfflineActiveSupport;

    /* 
        Enables the CanIf_CheckWakeup API at Pre-Compile-Time.
        this parameter defines if there shall be support for wake-up.
    */
    bool canIfWakeupSupport;

} CanIfPublicCfg;
typedef struct CanIf_ConfigType
{

    //This container contains the private configuration (parameters) of the CAN Interface.
    const CanIfPrivateCfg *canIfPrivateCfg;

    //This container contains the public configuration (parameters) of the CAN Interface.
    const CanIfPublicCfg *canIfPublicCfg;

    //This container contains the init parameters of the CAN Interface.
    const CanIfInitCfg *canIfInitCfg;

    /*
        Configuration parameters for all the underlying CAN
        Driver modules are aggregated under this container.
        For each CAN Driver module a seperate instance of
        this container has to be provided.
    */
    const CanIfCtrlDrvCfg *canIfCtrlDrvCfg;

    /*
        Callback functions provided by upper layer modules of the CanIf.
        The callback functions defined in this container are common to
        all configured CAN Driver / CAN Transceiver Driver modules.
    */
    const CanIfDispatchCfg *canIfDispatchCfg;

    /** List of CAN transceivers
        This container contains the configuration (parameters) of all addressed CAN transceivers
        by each underlying CAN Transceiver Driver module. For each CAN transceiver Driver
        a seperate instance of this container shall be provided.
    */
    const CanIfTrcvDrvCfg *canIfTrcvDrvCfg;

} CanIf_ConfigType;
