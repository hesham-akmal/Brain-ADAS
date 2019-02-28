#include "Can_Cfg.h"
#include "Can.h"
#include "ComStack_Types.h"
#include "Det.h"
#include "Std_Types.h"
#include "Modules.h"


#if (CAN_DEV_ERROR_DETECT == STD_ON)
/** @req 4.0.3/CAN027 */
#define VALIDATE(_exp,_api,_err ) \
        if( !(_exp) ) { \
          Det_ReportError(MODULE_ID_CAN,0,_api,_err); \
          return E_NOT_OK; \
        }
#define VALIDATE_NO_RV(_exp,_api,_err ) \
        if( !(_exp) ) { \
          Det_ReportError(MODULE_ID_CAN,0,_api,_err); \
          return; \
        }
#define DET_REPORTERROR(_x,_y,_z,_q) Det_ReportError(_x, _y, _z, _q)
#else
/** @req 4.0.3/CAN424 */
#define VALIDATE(_exp,_api,_err )
#define VALIDATE_NO_RV(_exp,_api,_err )
#define DET_REPORTERROR(_x,_y,_z,_q)
#endif

/* Type for holding information about each CAN controller */
typedef struct {
	CanIf_ControllerModeType 		state;					// Controller state (see R4.1.3 fig. 7-2)
	uint32							lock_cnt;				// Nr of interrupt locks
	const Can_ControllerConfigType* cfgCtrlPtr;     		// Pointer to controller configuration
	Can_Arc_StatisticsType 			stats;					// Statistics
	PduIdType 						swPduHandle; 			// PDU handle
} Can_UnitType;

/****************************************************************************/
/*	 				 		Private typedefs 								*/
/****************************************************************************/

typedef enum {
    CAN_UNINIT = 0,
    CAN_READY
} Can_DriverStateType;

// Mapping between HRH and Controller//HOH
typedef struct Can_Arc_ObjectHOHMapStruct
{
  CanControllerIdType CanControllerRef;    // Reference to controller
  const Can_HardwareObjectType* CanHOHRef;       // Reference to HOH.
} Can_Arc_ObjectHOHMapType;

/* Type for holding global information used by the driver */
typedef struct {
    Can_DriverStateType     initRun;            				// True if Can_Init() have been run
    const Can_ConfigType *  config;             				// Pointer to CAN configuration
    uint32                  configuredMask;     				// Bitmask for configured CAN HW units
    uint8   				channelMap[CAN_CONTROLLER_CNT];		// Maps controller id to configuration id

    // This is a map that maps the HTH:s with the controller and Hoh. It is built
    // during Can_Init and is used to make things faster during a transmit.
    Can_Arc_ObjectHOHMapType CanHTHMap[NUM_OF_HTHS];
} Can_GlobalType;

// Global config
Can_GlobalType Can_Global =
{
    .initRun = CAN_UNINIT,
};

#define GET_CALLBACKS()                 	(Can_Global.config->CanConfigSet->CanCallbacks)

/**
 * Initialize software and hardware configurations for all attached CAN controllers
 *
 * @param Config			----- CAN driver configuration
 */
void Can_Init(const Can_ConfigType *Config) {
	/* Locals */
	Can_UnitType *unitPtr;
	uint8 ctrlId, configId;
	const Can_ControllerConfigType *cfgCtrlPtr;

	/** @req 4.1.3/SWS_Can_00259: Check that the CAN module has not been initialized yet */
	VALIDATE_NO_RV((Can_Global.initRun == CAN_UNINIT),
			CAN_INIT_SERVICE_ID, CAN_E_TRANSITION);
	/** @req 4.1.3/SWS_Can_00175: Check that the configuration parameter is non-null */
	VALIDATE_NO_RV((Config != NULL ),
			CAN_INIT_SERVICE_ID, CAN_E_PARAM_POINTER);

	/* Save configuration */
	Can_Global.config = Config;
	Can_Global.initRun = CAN_READY;

	for (configId = 0; configId < CAN_CTRL_CONFIG_CNT; configId++) {
		cfgCtrlPtr = GET_CONTROLLER_CONFIG(configId);
		ctrlId = cfgCtrlPtr->CanControllerId;

		/* Initialize CAN unit structure to default values */
		unitPtr = GET_CAN_UNIT_PTR(ctrlId);
		unitPtr->state = CANIF_CS_STOPPED;
		unitPtr->lock_cnt = 0;
		unitPtr->cfgCtrlPtr = cfgCtrlPtr;
		memset(&unitPtr->stats, 0, sizeof(Can_Arc_StatisticsType));
		unitPtr->swPduHandle = 0;

		/* Map controller id to configuration id */
		Can_Global.channelMap[ctrlId] = configId;

		/* Record that this controller has been configured */
		Can_Global.configuredMask |= (1 << ctrlId);

		/* Loop through all HOH:s (HW Object Handles, which are
         * either HTH or HRH (for transmission and reception))
		 * and map them into the HTHMap. These handles are used
		 * as an interface between CanInterface and CanDriver. */
		const Can_HardwareObjectType* hoh;
		hoh = cfgCtrlPtr->Can_Arc_Hoh;
		hoh--;
		do {
			hoh++;
			if (hoh->CanObjectType == CAN_OBJECT_TYPE_TRANSMIT) {
				Can_Global.CanHTHMap[hoh->CanObjectId].CanControllerRef = cfgCtrlPtr->CanControllerId;
				Can_Global.CanHTHMap[hoh->CanObjectId].CanHOHRef = hoh;
			}
		} while (!hoh->Can_Arc_EOL);

		/* Initialize the CAN controller HW */
		Can_InitController(ctrlId, cfgCtrlPtr);
	}
}

/**
 * Read several consecutive CAN-board registers
 *
 * The registers on MCP2515 have been arranged to optimize sequential reading
 * and writing of data. This is used in this function, where a number of consecutive
 * registers are looped through (e.g. RXB0SIDH, RXB0SIDL, RXB0EID8, RXB0EID0)
 *
 * @param address			----- the first CAN-board register to read
 * @param values			----- array of rx-buffers to store the received values in
 * @param dlc				----- number of consecutive registers to read
 */
static void Can_ReadController_Regs(const Spi_DataType address,
								    Spi_DataType *values,
									const uint8 dlc)
{
	/* Read instruction in MCP2515-language (00000011) */
	Spi_DataType cmdbuf = MCP2515_READ;

	/* Check that the data length does not exceed what is allowed in one CAN frame */
	VALIDATE_NO_RV(dlc <= CAN_MAX_CHAR_IN_MESSAGE,
			CAN_MAINFUNCTION_READ_SERVICE_ID, CAN_E_PARAM_DLC);

	/* Setup external buffers for SPI read operation (see p.65 in mcp2515_can.pdf for details) */
	Spi_SetupEB(SPI_CH_CMD,  &cmdbuf,  NULL,   sizeof(cmdbuf));			// Tell the CAN controller that this is a read operation
	Spi_SetupEB(SPI_CH_ADDR, &address, NULL,   sizeof(address));		// Read-from register address (A7-A0)
	Spi_SetupEB(SPI_CH_DATA, NULL, 	   values, dlc);					// Place the response in an array of values

	/* Transmit the SPI sequence to read data (up to 8 bytes) from the CAN controller
	 * (which increments its register address by itself) */
	Spi_SyncTransmit(SPI_SEQ_READ);
}

/**
 * Read a byte from one of the Rx-registers of the CAN controllers (MCP2515)
 *
 * The Read instruction is sent to to the MCP2515 followed by the
 * 8-bit address of the Rx-register. Then, the data stored in that register
 * will be shifted out on the SO pin and arrives through SPI to MCU's rx-buffer.
 *
 * @param address			----- CAN boards Rx-register address
 * @param mask				----- mask describing interesting bits in this register
 * 								  (MCP2515_NO_MASK preserves all bits)
 * @return rxbuf			----- pointer to MCU-local rx-buffer
 */
static Spi_DataType Can_ReadController_Reg(const Spi_DataType address,
										   const Spi_DataType mask)
{
    Spi_DataType rxbuf;

    /* Read only one register */
    Can_ReadController_Regs(address, &rxbuf, 1);

    /* Mask out non-interesting bits and return */
	return rxbuf & mask;
}

/**
 * Find the first non-busy Tx-buffer on the CAN board and return its address
 *
 * MCP2515 has 3 transfer buffers, controlled by TXBnCTRL-registers,
 * located at 0x30H, 0x40H and 0x50H (see p.18 in mcp2515_can.pdf)
 *
 * TXBnCTRL: - | ABTF | MLOA | TXERR | TXREQ | - | TXP1 | TXP0
 * 		bit 6   (ABTF) 	 	Message aborted flag bit
 * 		bit 5   (MLOA) 	 	Message lost arbitration bit
 * 		bit 4   (TXERR)  	Transmission error detected bit
 * 		bit 3   (TXREQ)  	Message Transmit request bit, pending (1) or not (0)
 * 		bit 1-0 (TXPn)  	Transmit buffer priority bits (11 - highest priority)
 *
 * @param[in]
 */
static Can_ReturnType Can_GetController_TxBuf(Spi_DataType *txbuf_addr)
{
	/* Locals */
    uint8 i;
    Spi_DataType ctrl_val;
    const Spi_DataType ctrl_regs[MCP2515_NR_TXBUFFERS] = {MCP2515_TXB0CTRL,			// Available Tx-buffers
											 	    	  MCP2515_TXB1CTRL,
														  MCP2515_TXB2CTRL};

	/* Find the first non-busy TX-Buffer */
	for (i=0; i < MCP2515_NR_TXBUFFERS; i++) {
		/* Get TXBn control status bits */
		ctrl_val = Can_ReadController_Reg(ctrl_regs[i], MCP2515_TXBnCTRL_TXREQ);

		/* If no transmission is currently pending from this buffer, return it */
		if (ctrl_val == 0) {
			*txbuf_addr = ctrl_regs[i] + 1;			// Tx-buffer follows its control register

			return CAN_OK;
		}
	}

	return CAN_BUSY;
}

/**
 * Set up SPI and write one byte of data to a register on the CAN board
 *
 * @param address			----- register address on the CAN board
 * @param value				----- data
 */
static void Can_WriteController_Reg(const Spi_DataType address,
									const Spi_DataType value)
{
	Can_WriteController_Regs(address, &value, 1);
}

/**
 * Set up SPI buffers and write several consecutive registers on the CAN board
 *
 * The write operation on MCP2515 works in such a way that sequential
 * registers are being written to on each rising edge of SCK, as long
 * as CS is held low (see p. 63 in mcp2515_can.pdf)
 *
 * This is typically used for transmitting several data bytes (up to 8) in
 * one CAN frame. Then the first register is given by TXBnD0.
 *
 * @param address			----- register address on the CAN board
 * @param values			----- data bytes
 * @param dlc				----- number of data bytes
 */
static void Can_WriteController_Regs(const Spi_DataType address,
									 const Spi_DataType *values,
									 const uint8 dlc)
{
	/* Write instruction (00000010), see p.64 in mcp2515_can.pdf */
	Spi_DataType cmdbuf = MCP2515_WRITE;

	/* Set up external buffers for each SPI channel in a write sequence */
	Spi_SetupEB(SPI_CH_CMD,  &cmdbuf,  NULL, sizeof(cmdbuf));		// Write instruction
	Spi_SetupEB(SPI_CH_ADDR, &address, NULL, sizeof(address));		// Tx-register address
    Spi_SetupEB(SPI_CH_DATA, values,   NULL, dlc);					// Data that will be written

    /* Transmit the SPI sequence */
    Spi_SyncTransmit(SPI_SEQ_WRITE);
}

/**
 * Set or clear individual bits in specific status and control registers
 *
 * Example of how mask and data bytes are used:
 *          Mask type:    00101000
 *          Data type:    00001000
 *          Pre-Reg data: xxxxxxxx
 *          New-Reg data: xx0x1xxx
 *
 * @param address			----- register address
 * @param mask 				----- mask byte determines which bits in the register that will change
 * @param data				----- data byte contains new bit values
 */
static void Can_WriteController_BitModify(const Spi_DataType address,
										  const Spi_DataType mask,
										  const Spi_DataType data)
{
	Spi_DataType cmdbuf = MCP2515_BITMOD;
	Spi_DataType valbuf[2] = {mask, data};

	/* Set up external buffers for SPI for status bit modification */
	Spi_SetupEB( SPI_CH_CMD,  &cmdbuf,  NULL, sizeof(cmdbuf));			// Bit modify instruction
	Spi_SetupEB( SPI_CH_ADDR, &address, NULL, sizeof(address));			// Register address
	Spi_SetupEB( SPI_CH_DATA, valbuf,   NULL, sizeof(valbuf));			// Mask and new bit values

	/* Initiate SPI transmission */
    Spi_SyncTransmit(SPI_SEQ_WRITE);
}

/**
 * Write message standard identifier to the CAN board
 *
 * Typically a message id is written to 4 registers, SIDH, SIDL, EID8 and EID0.
 * Unless extended ids are used, only the first two registers are set.
 *
 * Currently only standard ids are used (not extended or remote frames).
 *
 * @param mcp_addr			----- SIDH register address (the other registers are written consecutively)
 * @param can_id			----- message id
 */
static void Can_WriteController_MsgID(const Spi_DataType mcp_addr, const uint32 can_id)
{
	/* Standard id, divided into SIDH/SIDL/EID8/EID0-registers */
	Spi_DataType sidData[4];

	/* Set up values for the different id-registers */
	sidData[0] = (Spi_DataType)(can_id >> 3 ); 		// standard id, high bits (SIDH)
	sidData[1] = (Spi_DataType)(can_id << 5 ); 		// standard id, low bits (SIDL)
	sidData[2] = (Spi_DataType)0;					// default values in EID8
	sidData[3] = (Spi_DataType)0;					// default values in EID0

	/* Write id to the CAN board */
	Can_WriteController_Regs(mcp_addr, sidData, sizeof(sidData));
}


/**
 * Send a message to the CAN controller
 *
 * Design choice: if all 3 Tx-buffers are full, the message is dropped
 * 				  (to avoid building up buffer queues)
 *
 * @param pduInfo			----- PDU (protocol data unit) for this CAN message, incl. data, data length, and id
 * @return rv				----- return status
 */
static Std_ReturnType Can_SendMessage(Can_PduType *pduInfo) {
	Can_ReturnType rv;
	Spi_DataType txbuf;

	/* Find a free tx-buffer, returning an error status if no one was found */
	rv = Can_GetController_TxBuf(&txbuf);
	if (rv == CAN_BUSY) {
		return E_NOT_OK;
	}

	/* Write data bytes to the data register(s) */
	Can_WriteController_Regs(txbuf + MCP2515_D0_OFFSET, pduInfo->sdu, pduInfo->length);

	/* Write the message id */
	Can_WriteController_MsgID(txbuf + MCP2515_SIDH_OFFSET, pduInfo->id);

	/* Write the data length (in bytes) */
	Can_WriteController_Reg(txbuf + MCP2515_DLC_OFFSET, pduInfo->length);

	/* Set control status to transmission pending */
	Can_WriteController_BitModify(txbuf + MCP2515_CTRL_OFFSET,
			MCP2515_TXBnCTRL_TXREQ, MCP2515_TXBnCTRL_TXREQ);

	return E_OK;
}

/**
 * Write data stored in a PDU-structure on the CAN bus
 *
 * Currently, HTH (hardware transmit handle) object is not used in this
 * implementation (TODO)
 *
 * @param hth 				----- hardware transmit handle (HTH)
 * @param pduInfo  			----- PDU (protocol data unit) for this CAN message, incl. data, data length, and id
 * @return 					----- result status
 */
Can_ReturnType Can_Write(Can_HwHandleType hth, Can_PduType *pduInfo) {
	/* Locals */
	Std_ReturnType rv;
	uint8 i;

	/* Check that CAN driver has been initialized */
	VALIDATE((Can_Global.initRun == CAN_READY), CAN_WRITE_SERVICE_ID, CAN_E_UNINIT);
	/* Check that there is a valid PDU object */
	VALIDATE((pduInfo != NULL), CAN_WRITE_SERVICE_ID, CAN_E_PARAM_POINTER);
	/* Check that data length does not exceed max data length in one frame */
	VALIDATE((pduInfo->length <= 8), CAN_WRITE_SERVICE_ID, CAN_E_PARAM_DLC);

	/* Send the data in PDU */
	rv = Can_SendMessage(pduInfo);

	/* Return the result */
	return (rv == E_OK) ? CAN_OK : CAN_NOT_OK;
}

/**
 * Trigger RxIndication-callback function in the CanIf layer
 *
 * Find a HOH object for message reception. Then find and set
 * an event notifying upper layers that a certain type of message
 * has been received. Finally, trigger message handling in CanIf.

 * @param pduInfo			----- PDU info, incl. data, data length and id
 * @param ctrlId			----- CAN controller id
 */
static void Can_TriggerCanIf(Can_PduType *pduInfo, uint8 ctrlId) {
	/* Get HOH pointer and message id table for the CAN controller */


	const Can_ControllerConfigType *cfgCtrlPtr = GET_CONTROLLER_CONFIG(Can_Global.channelMap[ctrlId]);
	const Can_HardwareObjectType *hohObj = cfgCtrlPtr->Can_Arc_Hoh;
	const Can_IdTableType *msgIdTable = cfgCtrlPtr->CanMsgIdTable;
	uint32 i;

	--hohObj;
	do {
		++hohObj;
		if (hohObj->CanObjectType == CAN_OBJECT_TYPE_RECEIVE) {
			if (GET_CALLBACKS()->RxIndication != NULL ) {
				/* Find and set an appropriate event to notify upper layers that a CAN-message has arrived */
				for (i=0; i<CAN_MESSAGE_TYPE_CNT; i++) {
					if (msgIdTable[i].msgId == pduInfo->id) {
#if 0
					  printf("trigger event %d %d\r\n",
						 pduInfo->id,
						 pduInfo->sdu[0]);
#endif
						SetEvent(msgIdTable[i].taskId, msgIdTable[i].eventMask);
						break;
					}
				}

				/* Trigger a method in CanIf to forward the fetched data */
#if 0
				printf("trig %d len %d %d %p: ",
				       pduInfo->id,
				       pduInfo->length,
				       pduInfo->sdu[0],
				       pduInfo->sdu
				       );
#endif

#if 0
				for (int i = 0; i < pduInfo->length; i++) {
				  printf(" %d", pduInfo->sdu[i]);
				}
				printf("\r\n");
#endif
#if 0
				printf("trigger callback %d %d\r\n",
				       pduInfo->id,
				       pduInfo->sdu[0]);
#endif
				GET_CALLBACKS()->RxIndication(hohObj->CanObjectId, pduInfo->id, pduInfo->length, pduInfo->sdu);
#if 0
				printf("trigger callback done %d %d\r\n",
				       pduInfo->id,
				       pduInfo->sdu[0]);
#endif
				//printf("callback 2\r\n");
			}
		}
	} while (!hohObj->Can_Arc_EOL);
}


/**
 * Read data in Rx-buffers, when CAN processing is driven by polling
 */
void Can_MainFunction_Read(void) {
	/* Locals */
	Spi_DataType stat;
	Can_PduType pduInfo, pduInfo2;
	int i;

	const Spi_DataType rxBufRegs[MCP2515_NR_BUFFERS] = {MCP2515_RXBUF_0,					// Rx-buffer registers
													    MCP2515_RXBUF_1};
	const Spi_DataType rxStatBits[MCP2515_NR_BUFFERS] = {MCP2515_CANINT_RX0I,				// Rx-buffer interrupt status bits
													     MCP2515_CANINT_RX1I};

	/** @req 4.0.3/CAN181 Check that the module has been initialized  */
	VALIDATE_NO_RV((Can_Global.initRun == CAN_READY), CAN_MAINFUNCTION_READ_SERVICE_ID, CAN_E_UNINIT);

	int xx = bcm2835_ReadGpioPin(&GPEDS0, GPIO_CAN_IRQ);

	/* If CAN communication is defined to be interrupt-driven and
	 * no event has been detected on the CAN interrupt pin, exit */
	if (CAN_INTERRUPT && (xx == 0x0)) {
	  return;
	}

	/* In the interrupt mode, don't forget to clear the interrupt pin, when done reading */
	if (CAN_INTERRUPT) {
		bcm2835_ClearEventDetectPin(GPIO_CAN_IRQ);
	}

	/* Read interrupt status bits to see if any Rx-buffer is non-empty */
	stat = Can_ReadController_Reg(MCP2515_CANINTF, CAN_NO_MASK);


	/* If there is data in any register, read it and clear the interrupt status bit,
	 * so that new data can be written into the Rx-buffer */
	for (i=0; i < MCP2515_NR_BUFFERS; i++) {
		if (stat & rxStatBits[i]) {													// RXBUF_i contains data

			/* Set event reception events and forward the CAN message upwards */
			Can_TriggerCanIf(&pduInfo, 0);

#if 0
			Can_WriteController_BitModify(MCP2515_CANINTF, rxStatBits[i], 0);		// Clear interrupt status
#endif

		}
	}

}

