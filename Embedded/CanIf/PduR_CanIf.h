void PduR_CanIfRxIndication(PduIdType CanRxPduId, const PduInfoType* PduInfoPtr);
void PduR_CanIfTxConfirmation(PduIdType CanTxPduId, Std_ReturnType result);
Std_ReturnType PduR_CanIfTriggerTransmit(PduIdType TxPduId, PduInfoType* PduInfoPtr);
