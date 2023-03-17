import xml.etree.ElementTree as ET
import pandas as pd
import uuid
import datetime

def readFile(batchNo,txnNo,amtType,amount):
    tree = ET.parse("XMLFile123\FPS_Template.xml")
    ns = {"fps": "urn:hkicl:fps:xsd:fps.envelope.01",
          "ah": "urn:iso:std:iso:20022:tech:xsd:head.001.001.01",
          "doc": "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.06",
          "": "http://www.w3.org/2000/09/xmldsig#"}

    ET.register_namespace("fps", ns["fps"])
    ET.register_namespace("ah", ns["ah"])
    ET.register_namespace("doc", ns["doc"])
    ET.register_namespace("", ns[""])
    root = tree.getroot()

    fileElement = root.find(".//fps:FpsPylds", ns)  # File Level Element
    fiToFiElement = root.find(".//doc:FIToFICstmrCdtTrf", ns)
    NbOfMsgs = root.find(".//fps:NbOfMsgs", ns)
    NbOfMsgs.text = str(batchNo)

    for i in range(batchNo - 1):
        btchElement = root.find(".//fps:BizData", ns)  # Batch Level Element
        fileElement.append(btchElement)
    for j in range(txnNo - 1):
        txnElement = root.find(".//doc:CdtTrfTxInf", ns)  # CdtTrfTxInf Level Element
        fiToFiElement.append(txnElement)

    if amtType == 1:
        for txn in root.findall('.//doc:CdtTrfTxInf', ns):
            txn.find('.//doc:IntrBkSttlmAmt', ns).text = str(amount)
            txn.find('.//doc:InstdAmt', ns).text = str(amount)

    elif amtType == 2:
        for txn in root.findall('.//doc:CdtTrfTxInf', ns):
            txn.find('.//doc:IntrBkSttlmAmt', ns).text = str(amount / (txnNo * batchNo))
            txn.find('.//doc:InstdAmt', ns).text = str(amount / (txnNo * batchNo))

    else:
        raise ValueError("Invalid Input")

    # NbOfTxs
    NbOfTxs = root.find(".//doc:NbOfTxs", ns)
    NbOfTxs.text = str(txnNo)

    tree.write("XMLFile123\SampleFile1.xml", xml_declaration=True, encoding='utf-8')
    print("File 1 generated sucessfully..")



def writeFile():
    tree = ET.parse("XMLFile123\SampleFile1.xml")
    ns = {"fps": "urn:hkicl:fps:xsd:fps.envelope.01",
          "ah": "urn:iso:std:iso:20022:tech:xsd:head.001.001.01",
          "doc": "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.06",
          "": "http://www.w3.org/2000/09/xmldsig#"}

    ET.register_namespace("fps", ns["fps"])
    ET.register_namespace("ah", ns["ah"])
    ET.register_namespace("doc", ns["doc"])
    ET.register_namespace("", ns[""])

    root = tree.getroot()
    df = pd.read_csv("XMLFile123\Account.csv")
    Acc_no = df['ACC_NO']
    Acc_name = df['ACCOUNTNAME']

    now = datetime.datetime.now()
    c_date = (now.strftime("%y%m%d%H%M%S"))  # Current Date and Time
    uid = uuid.uuid4().hex[:15].upper()  # Generate UUID

    for element in root.findall('.//fps:BtchId', ns):
        btchId = 'BTCH' + c_date + uid  # BtchId
        element.text = str(btchId)

    for element in root.findall('.//fps:BizData', ns):
        bizMsgIdr = 'BZMSG' + c_date + uid  # BizMsgIdr
        element.find(".//ah:BizMsgIdr", ns).text = str(bizMsgIdr)

    for element in root.findall('.//doc:GrpHdr', ns):
        c_date = (now.strftime("%y%m%d%H%M%S"))  # Current Date and Time
        uid = uuid.uuid4().hex[:15].upper()  # Generate UUID

        msgId = 'MSG' + c_date + '' + uid  # MsgId
        element.find(".//doc:MsgId", ns).text = str(msgId)

    count = 0
    for element in root.findall('.//doc:CdtTrfTxInf', ns):
        c_date = (now.strftime("%y%m%d%H%M%S"))  # Current Date and Time
        uid = uuid.uuid4().hex[:15].upper()  # Generate UUID

        endToEndId = 'E2E' + c_date + '' + uid  # EndToEndId
        element.find(".//doc:EndToEndId", ns).text = str(endToEndId)

        txID = 'TXID' + c_date + uid  # TXID
        element.find('.//doc:TxId', ns).text = str(txID)

        clrSysRef = 'CLRREF' + c_date + uid  # ClrSysRef
        element.find('.//doc:ClrSysRef', ns).text = str(clrSysRef)

        # Id and Name from CSV File
        Id = element.find(".//doc:CdtrAcct/doc:Id/doc:Othr/doc:Id", ns)
        Nm = element.find(".//doc:Cdtr/doc:Nm", ns)
        if (count < len(df)):
            Id.text = str(Acc_no[count])
            Nm.text = str(Acc_name[count])
            count = count + 1

        else:
            df = df.reset_index(drop=True)
            count = 0
            Id.text = str(Acc_no[count])
            Nm.text = str(Acc_name[count])
            count = count + 1

    for element in root.findall('.//fps:BizData', ns):
        c_date = (now.strftime("%Y-%m-%dT%H:%M:%S:%f")[:-3] + 'Z')
        c_date_1 = (now.strftime("%Y-%m-%dT%H:%M:%S:%f")[:-3])
        element.find(".//ah:CreDt", ns).text = str(c_date)
        element_1.find(".//doc:CreDtTm", ns).text = str(c_date_1)

    for element_1 in root.findall('.//doc:CdtTrfTxInf', ns):
        c_date_2 = (now.strftime("%Y-%m-%dT%H:%M:%S"))
        element_1.find(".//doc:CdtDtTm", ns).text = str(c_date_2)

    tree.write("XMLFile123\SampleFileMain.xml", xml_declaration=True, encoding='utf-8')
    print("File 2 generated sucessfully..")

