#include "PduR_Cfg.h"
#include "Can_Texas_TivaC.h"
#include "CanIf.h"
#include "Can.h"
//
//
//
//CanIfCtrlCfg canIfCtrlCfg[] = {
//    {
//        .canIfCtrlId = CANIF_INF_CAN_DRIVER_0_CONTROLER_0,
//        .canIfCtrlWakeupSupport = false,
//        //        .canIfCtrlCanCtrlRef = NULL, ///Symbolic name reference to CanController
//        .canIfCtrlCanCtrlRef = 0, ///Symbolic name reference to CanController
//    },
//};
//
//CanIfHrhCfg canIfHrhCfg[] = {
//    {
//        /* ----------- Configuration Parameters ----------- */
//        .canIfHrhSoftwareFilter = false,
//        .canIfHrhCanCtrlIdRef = &canIfCtrlCfg[0],
//        .canIfHrhIdSymRef = CAN_INF_HARDWARE_OBJECT_REF_0,
//        //        .CanIfHrhRangeCfg = NULL,
//        .canIfHrhRangeCfg = 0,
//
//    },
//};
//
//CanIfHthCfg canIfHthCfg[] = {
//    {
//        /* ----------- Configuration Parameters ----------- */
//        .canIfHthCanCtrlIdRef = &canIfCtrlCfg[0],
//        .canIfHthIdSymRef = CAN_INF_HARDWARE_OBJECT_REF_1, ///CanHardwareObject
//
//        /* ------------- Included Containers ------------- */
//    },
//};
//
////const CanIfRxPduCanIdRangeType CanIfRxPduCanIdRange =
////{
/////* ----------- Configuration Parameters ----------- */
////    .CanIfRxPduCanIdRangeLowerCanId = ,
////    .CanIfRxPduCanIdRangeUpperCanId = ,
////
/////* ------------- Included Containers ------------- */
////};
//
//#if (CANIF_INF_CAN_TRCV_SUPPORT == STD_ON)
//const CanIfTrcvCfg canIfTrcvCfg[] = {
//    {
//        .CanIfTrcvId = CANIF_INF_CAN_TRCV_DRIVER_0_TRANSCEIVER_0,
//        .CanIfTrcvWakeupSupport = false,
//        //        .CanIfTrcvCanTrcvRef = NULL, ///Symbolic name reference to CanTrcvChannel
//        .CanIfTrcvCanTrcvRef = 0, ///Symbolic name reference to CanTrcvChannel
//    },
//};
//#endif
//
//const CanIfBufferCfg canIfBufferCfg[] = {
//    {
//        .canIfBufferSize = 0,
//        .canIfBufferHthRef = &canIfHthCfg[0],
//    },
//};
//
//const CanIfInitHohCfg canIfInitHohCfg[] = {
//    {
//        .canIfHrhCfg = &canIfHrhCfg[0],
//        .canIfHrhCfg = &canIfHthCfg[0],
//    },
//};
//
//const CanIfRxPduCfg canIfRxPduCfg[] = {
//    {
//        /* ----------- Configuration Parameters ----------- */
//        .canIfRxPduCanId = CANIF_INF_RX_PDU_0_CAN_ID,
//        .canIfRxPduCanIdMask = 0x7FF, ///STANDARD_CAN;
//        .canIfRxPduCanIdType = STANDARD_CAN,
//        .canIfRxPduDlc = 7, //0 .. 64
//        .CanIfRxPduId = CANIF_INF_RX_PDU_0,
//        .canIfRxPduReadData = false,
//        .canIfRxPduReadNotifyStatus = false,
//        .canIfRxPduUserRxIndicationName = PduR_CanIfRxIndication,
//        .canIfRxPduUserRxIndicationUL = PDUR,
//        .canIfRxPduHrhIdRef = &canIfHrhCfg[0],
////        .canIfRxPduRef = &Pdus[0],
//        .canIfRxPduRef = 0,
//    },
//};
//
//CanIfTxPduCfg canIfTxPduCfg[] = {
//    {
//        /* ----------- Configuration Parameters ----------- */
//        .canIfTxPduCanId = CANIF_INF_TX_PDU_0_CAN_ID,
//        .canIfTxPduCanIdMask = 0x7FF, ///STANDARD_CAN
//        .canIfTxPduCanIdType = STANDARD_CAN,
//        .canIfTxPduId = CANIF_INF_TX_PDU_0,
//        .canIfTxPduPnFilterPdu = false,
//        .canIfTxPduReadNotifyStatus = false,
//        .canIfTxPduTriggerTransmit = true,
//        .canIfTxPduType = STATIC,
////        .canIfTxPduUserTriggerTransmitName = PduR_CanIfTriggerTransmit,
//        .canIfTxPduUserTxConfirmationName = PduR_CanIfTxConfirmation,
////        .CanIfTxPduUserTxConfirmationUL = PDUR,
//        .canIfTxPduBufferRef = &canIfBufferCfg[0],
////        .canIfTxPduRef = &Pdus[1],
//        .canIfTxPduRef = 0,
//    },
//};
//
//#if (CANIF_INF_CAN_TRCV_SUPPORT == STD_ON)
//const CanIfTrcvDrvCfg canIfTrcvDrvCfg[] = {
//    {
//        .canIfTrcvCfg = canIfTrcvCfg,
//    },
//};
//#endif
//
//const CanIfPublicCfg canIfPublicCfg = {
//    /* ----------- Configuration Parameters ----------- */
//    .canIfMetaDataSupport = false,
//    .canIfPublicCancelTransmitSupport = false,
//    .canIfPublicCddHeaderFile = 0,
//    .canIfPublicHandleTypeEnum = UINT16,
//    .canIfPublicIcomSupport = CANIF_PUBLIC_ICOM_SUPPORT,
//    .canIfPublicMultipleDrvSupport = false,
//    .canIfPublicPnSupport = CANIF_PUBLIC_PN_SUPPORT,
//    .canIfPublicReadRxPduDataApi = CANIF_PUBLIC_READRXPDU_DATA_API,
//    .canIfPublicReadRxPduNotifyStatusApi = CANIF_PUBLIC_READRXPDU_NOTIFY_STATUS_API,
//    .canIfPublicReadTxPduNotifyStatusApi = CANIF_PUBLIC_READTXPDU_NOTIFY_STATUS_API,
//    .canIfPublicSetDynamicTxIdApi = CANIF_PUBLIC_SETDYNAMICTXID_API,
//    .canIfPublicTxBuffering = false,
//    .canIfPublicTxConfirmPollingSupport = CANIF_INF_PUBLIC_TX_CONFIRMATION_POLLING_SUPPORT,
//    .canIfPublicWakeupCheckValidByNM = false,
//    .canIfPublicWakeupCheckValidSupport = CANIF_PUBLIC_WAKEUP_CHECK_VALIDATION_SUPPORT,
//    .canIfSetBaudrateApi = CANIF_SET_BAUDRATE_API,
//    .canIfTriggerTransmitSupport = false,
//    .canIfTxOfflineActiveSupport = false,
//    .canIfWakeupSupport = CANIF_INF_WAKEUP_SUPPORT,
//};
//
//const CanIfPrivateCfg canIfPrivateCfg = {
//    /* ----------- Configuration Parameters ----------- */
//    .CanIfFixedBuffer = false,
//    .CanIfPrivateDlcCheck = CANIF_INF_PRIVATE_DATA_LENGTH_CHECK,
//    .canIfPrivateSoftwareFilterType = BINARY,
//};
////
////const CanIfDispatchCfgType CanIfDispatchCfg = {
////    /* ----------- Configuration Parameters ----------- */
////    .CanIfDispatchUserCheckTrcvWakeFlagIndicationName = CanSM_CheckTransceiverWakeFlagIndication,
////    .CanIfDispatchUserCheckTrcvWakeFlagIndicationUL = CAN_SM,
////    .CanIfDispatchUserClearTrcvWufFlagIndicationName = CanSM_ClearTrcvWufFlagIndication,
////    .CanIfDispatchUserClearTrcvWufFlagIndicationUL = CAN_SM,
////    .CanIfDispatchUserConfirmPnAvailabilityName = CanSM_ConfirmPnAvailability,
////    .CanIfDispatchUserConfirmPnAvailabilityUL = CAN_SM,
////    .CanIfDispatchUserCtrlBusOffName = CanSM_ControllerBusOff,
////    .CanIfDispatchUserCtrlBusOffUL = CAN_SM,
////    .CanIfDispatchUserCtrlModeIndicationName = CanSM_ControllerModeIndication,
////    .CanIfDispatchUserCtrlModeIndicationUL = CAN_SM,
////    .CanIfDispatchUserTrcvModeIndicationName = CanSM_TransceiverModeIndication,
////    .CanIfDispatchUserTrcvModeIndicationUL = CAN_SM,
////    .CanIfDispatchUserValidateWakeupEventName = EcuM_CheckValidation,
////    .CanIfDispatchUserValidateWakeupEventUL = ECUM,
////
////    /* ------------- Included Containers ------------- */
////};
//
//
//const CanIfCtrlDrvCfg canIfCtrlDrvCfg[] = {
//    {
//        /* ----------- Configuration Parameters ----------- */
//        .canIfCtrlDrvInitHohConfigRef = canIfInitHohCfg[0],
//        //        .canIfCtrlDrvNameRef = NULL, ///Reference to CanGeneral
//        .canIfCtrlDrvNameRef = 0, ///Reference to CanGeneral
//        .canIfCtrlCfg = canIfCtrlCfg,
//    },
//};
//
//
//const CanIfInitCfg canIfInitCfg = {
//    /* ----------- Configuration Parameters ----------- */
//    //    .canIfInitCfgSet = NULL,
//    .canIfInitCfgSet = 0,
//    .canIfMaxBufferSize = 0,
//    .canIfMaxRxPduCfg = CANIF_INF_RX_CNT,
//    .canIfMaxTxPduCfg = CANIF_INF_TX_CNT,
//
//    /* ------------- Included Containers ------------- */
//    .canIfBufferCfg = canIfBufferCfg,
//    .canIfInitHohCfg = canIfInitHohCfg,
//    .canIfRxPduCfg = canIfRxPduCfg,
//    .canIfTxPduCfg = canIfTxPduCfg,
//
//};
//
//const CanIf_ConfigType CanIf_Config = {
//    .canIfPrivateCfg = &canIfPrivateCfg,
//    .canIfPublicCfg = &canIfPublicCfg,
//    .canIfInitCfg = &canIfInitCfg,
//    //    .canIfDispatchCfg = &canIfDispatchCfg,
//    .canIfCtrlDrvCfg = canIfCtrlDrvCfg,
//#if (CANIF_INF_CAN_TRCV_SUPPORT == STD_ON)
//    .canIfTrcvDrvCfg = canIfTrcvDrvCfg,
//#endif
//};
