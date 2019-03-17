
#define PDUR_CANIF_SUPPORT STD_ON
#define PDUR_CANTP_SUPPORT STD_ON
#define PDUR_COM_SUPPORT STD_ON
#define PDUR_DCM_SUPPORT STD_ON

/** Zero cost operation */
#define PDUR_ZERO_COST_OPERATION STD_OFF

/** If zero cost operation support is active */
#if PDUR_ZERO_COST_OPERATION == STD_ON

#if PDUR_CANIF_SUPPORT == STD_ON
#define PduR_CanIfRxIndication Com_RxIndication
#define PduR_CanIfTxConfirmation Com_TxConfirmation
#else
#define PduR_CanIfRxIndication(...)
#define PduR_CanIfTxConfirmation(...)
#endif

#if PDUR_COM_SUPPORT == STD_ON
#define PduR_ComTransmit CanIf_Transmit
#else
#define PduR_ComTransmit(...) (E_OK)
#endif

#endif // PDUR_ZERO_COST_OPERATION
