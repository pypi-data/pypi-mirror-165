(function($) {
    /**
     * Thai language package
     * Translated by @figgaro
     */
    FormValidation.I18n = $.extend(true, FormValidation.I18n, {
        'th_TH': {
            base64: {
                'default': 'กรุณาระบุ base 64 encoded ให้ถูกต้อง'
            },
            between: {
                'default': 'กรุณาระบุค่าระหว่าง %s และ %s',
                notInclusive: 'กรุณาระบุค่าระหว่าง %s และ %s เท่านั้น'
            },
            bic: {
                'default': 'กรุณาระบุหมายเลข BIC ให้ถูกต้อง'
            },
            callback: {
                'default': 'กรุณาระบุค่าให้ถูก'
            },
            choice: {
                'default': 'กรุณาระบุค่าให้ถูกต้อง',
                less: 'โปรดเลือกตัวเลือก %s ที่ต่ำสุด',
                more: 'โปรดเลือกตัวเลือก %s ที่สูงสุด',
                between: 'กรุณาเลือก %s - %s ที่มีอยู่'
            },
            color: {
                'default': 'กรุณาระบุค่าสี color ให้ถูกต้อง'
            },
            creditCard: {
                'default': 'กรุณาระบุเลขที่บัตรเครดิตให้ถูกต้อง'
            },
            cusip: {
                'default': 'กรุณาระบุหมายเลข CUSIP ให้ถูกต้อง'
            },
            cvv: {
                'default': 'กรุณาระบุ CVV ให้ถูกต้อง'
            },
            date: {
                'default': 'กรุณาระบุวันที่ให้ถูกต้อง',
                min: 'ไม่สามารถระบุวันที่ได้ก่อน %s',
                max: 'ไม่สามารถระบุวันที่ได้หลังจาก %s',
                range: 'โปรดระบุวันที่ระหว่าง %s - %s'
            },
            different: {
                'default': 'กรุณาระบุค่าอื่นที่แตกต่าง'
            },
            digits: {
                'default': 'กรุณาระบุตัวเลขเท่านั้น'
            },
            ean: {
                'default': 'กรุณาระบุหมายเลข EAN ให้ถูกต้อง'
            },
            ein: {
                'default': 'กรุณาระบุหมายเลข EIN ให้ถูกต้อง'
            },
            emailAddress: {
                'default': 'กรุณาระบุอีเมล์ให้ถูกต้อง'
            },
            file: {
                'default': 'กรุณาเลือกไฟล์'
            },
            greaterThan: {
                'default': 'กรุณาระบุค่ามากกว่าหรือเท่ากับ %s',
                notInclusive: 'กรุณาระบุค่ามากกว่า %s'
            },
            grid: {
                'default': 'กรุณาระบุหมายลข GRId ให้ถูกต้อง'
            },
            hex: {
                'default': 'กรุณาระบุเลขฐานสิบหกให้ถูกต้อง'
            },
            iban: {
                'default': 'กรุณาระบุหมายเลข IBAN ให้ถูกต้อง',
                country: 'กรุณาระบุหมายเลข IBAN ใน %s',
                countries: {
                    AD: 'อันดอร์รา',
                    AE: 'สหรัฐอาหรับเอมิเรตส์',
                    AL: 'แอลเบเนีย',
                    AO: 'แองโกลา',
                    AT: 'ออสเตรีย',
                    AZ: 'อาเซอร์ไบจาน',
                    BA: 'บอสเนียและเฮอร์เซโก',
                    BE: 'ประเทศเบลเยียม',
                    BF: 'บูร์กินาฟาโซ',
                    BG: 'บัลแกเรีย',
                    BH: 'บาห์เรน',
                    BI: 'บุรุนดี',
                    BJ: 'เบนิน',
                    BR: 'บราซิล',
                    CH: 'สวิตเซอร์แลนด์',
                    CI: 'ไอวอรี่โคสต์',
                    CM: 'แคเมอรูน',
                    CR: 'คอสตาริกา',
                    CV: 'เคปเวิร์ด',
                    CY: 'ไซปรัส',
                    CZ: 'สาธารณรัฐเชค',
                    DE: 'เยอรมนี',
                    DK: 'เดนมาร์ก',
                    DO: 'สาธารณรัฐโดมินิกัน',
                    DZ: 'แอลจีเรีย',
                    EE: 'เอสโตเนีย',
                    ES: 'สเปน',
                    FI: 'ฟินแลนด์',
                    FO: 'หมู่เกาะแฟโร',
                    FR: 'ฝรั่งเศส',
                    GB: 'สหราชอาณาจักร',
                    GE: 'จอร์เจีย',
                    GI: 'ยิบรอลตา',
                    GL: 'กรีนแลนด์',
                    GR: 'กรีซ',
                    GT: 'กัวเตมาลา',
                    HR: 'โครเอเชีย',
                    HU: 'ฮังการี',
                    IE: 'ไอร์แลนด์',
                    IL: 'อิสราเอล',
                    IR: 'อิหร่าน',
                    IS: 'ไอซ์',
                    IT: 'อิตาลี',
                    JO: 'จอร์แดน',
                    KW: 'คูเวต',
                    KZ: 'คาซัคสถาน',
                    LB: 'เลบานอน',
                    LI: 'Liechtenstein',
                    LT: 'ลิทัวเนีย',
                    LU: 'ลักเซมเบิร์ก',
                    LV: 'ลัตเวีย',
                    MC: 'โมนาโก',
                    MD: 'มอลโดวา',
                    ME: 'มอนเตเนโก',
                    MG: 'มาดากัสการ์',
                    MK: 'มาซิโดเนีย',
                    ML: 'มาลี',
                    MR: 'มอริเตเนีย',
                    MT: 'มอลตา',
                    MU: 'มอริเชียส',
                    MZ: 'โมซัมบิก',
                    NL: 'เนเธอร์แลนด์',
                    NO: 'นอร์เวย์',
                    PK: 'ปากีสถาน',
                    PL: 'โปแลนด์',
                    PS: 'ปาเลสไตน์',
                    PT: 'โปรตุเกส',
                    QA: 'กาตาร์',
                    RO: 'โรมาเนีย',
                    RS: 'เซอร์เบีย',
                    SA: 'ซาอุดิอารเบีย',
                    SE: 'สวีเดน',
                    SI: 'สโลวีเนีย',
                    SK: 'สโลวาเกีย',
                    SM: 'ซานมาริโน',
                    SN: 'เซเนกัล',
                    TL: 'ติมอร์ตะวันออก',
                    TN: 'ตูนิเซีย',
                    TR: 'ตุรกี',
                    VG: 'หมู่เกาะบริติชเวอร์จิน',
                    XK: 'สาธารณรัฐโคโซโว'
                }
            },
            id: {
                'default': 'โปรดระบุเลขบัตรประจำตัวประชาชนให้ถูกต้อง',
                country: 'โปรดระบุเลขบัตรประจำตัวประชาชนใน %s ให้ถูกต้อง',
                countries: {
                    BA: 'บอสเนียและเฮอร์เซโก',
                    BG: 'บัลแกเรีย',
                    BR: 'บราซิล',
                    CH: 'วิตเซอร์แลนด์',
                    CL: 'ชิลี',
                    CN: 'จีน',
                    CZ: 'สาธารณรัฐเชค',
                    DK: 'เดนมาร์ก',
                    EE: 'เอสโตเนีย',
                    ES: 'สเปน',
                    FI: 'ฟินแลนด์',
                    HR: 'โครเอเชีย',
                    IE: 'ไอร์แลนด์',
                    IS: 'ไอซ์',
                    LT: 'ลิทัวเนีย',
                    LV: 'ลัตเวีย',
                    ME: 'มอนเตเนโก',
                    MK: 'มาซิโดเนีย',
                    NL: 'เนเธอร์แลนด์',
                    PL: 'โปแลนด์',
                    RO: 'โรมาเนีย',
                    RS: 'เซอร์เบีย',
                    SE: 'สวีเดน',
                    SI: 'สโลวีเนีย',
                    SK: 'สโลวาเกีย',
                    SM: 'ซานมาริโน',
                    TH: 'ไทย',
                    TR: 'ตุรกี',
                    ZA: 'แอฟริกาใต้'
                }
            },
            identical: {
                'default': 'โปรดระบุค่าให้ตรง'
            },
            imei: {
                'default': 'โปรดระบุหมายเลข IMEI ให้ถูกต้อง'
            },
            imo: {
                'default': 'โปรดระบุหมายเลข IMO ให้ถูกต้อง'
            },
            integer: {
                'default': 'โปรดระบุตัวเลขให้ถูกต้อง'
            },
            ip: {
                'default': 'โปรดระบุ IP address ให้ถูกต้อง',
                ipv4: 'โปรดระบุ IPv4 address ให้ถูกต้อง',
                ipv6: 'โปรดระบุ IPv6 address ให้ถูกต้อง'
            },
            isbn: {
                'default': 'โปรดระบุหมายเลข ISBN ให้ถูกต้อง'
            },
            isin: {
                'default': 'โปรดระบุหมายเลข ISIN ให้ถูกต้อง'
            },
            ismn: {
                'default': 'โปรดระบุหมายเลข ISMN ให้ถูกต้อง'
            },
            issn: {
                'default': 'โปรดระบุหมายเลข ISSN ให้ถูกต้อง'
            },
            lessThan: {
                'default': 'โปรดระบุค่าน้อยกว่าหรือเท่ากับ %s',
                notInclusive: 'โปรดระบุค่าน้อยกว่า %s'
            },
            mac: {
                'default': 'โปรดระบุหมายเลข MAC address ให้ถูกต้อง'
            },
            meid: {
                'default': 'โปรดระบุหมายเลข MEID ให้ถูกต้อง'
            },
            notEmpty: {
                'default': 'โปรดระบุค่า'
            },
            numeric: {
                'default': 'โปรดระบุเลขหน่วยหรือจำนวนทศนิยม ให้ถูกต้อง'
            },
            phone: {
                'default': 'โปรดระบุหมายเลขโทรศัพท์ให้ถูกต้อง',
                country: 'โปรดระบุหมายเลขโทรศัพท์ใน %s ให้ถูกต้อง',
                countries: {
                    AE: 'สหรัฐอาหรับเอมิเรตส์',
                    BG: 'บัลแกเรีย',
                    BR: 'บราซิล',
                    CN: 'จีน',
                    CZ: 'สาธารณรัฐเชค',
                    DE: 'เยอรมนี',
                    DK: 'เดนมาร์ก',
                    ES: 'สเปน',
                    FR: 'ฝรั่งเศส',
                    GB: 'สหราชอาณาจักร',
                    IN: 'อินเดีย',
                    MA: 'โมร็อกโก',
                    NL: 'เนเธอร์แลนด์',
                    PK: 'ปากีสถาน',
                    RO: 'โรมาเนีย',
                    RU: 'รัสเซีย',
                    SK: 'สโลวาเกีย',
                    TH: 'ไทย',
                    US: 'สหรัฐอเมริกา',
                    VE: 'เวเนซูเอลา'
                }
            },
            promise: {
                'default': 'กรุณาระบุค่าให้ถูก'
            },
            regexp: {
                'default': 'โปรดระบุค่าให้ตรงกับรูปแบบที่กำหนด'
            },
            remote: {
                'default': 'โปรดระบุค่าให้ถูกต้อง'
            },
            rtn: {
                'default': 'โปรดระบุหมายเลข RTN ให้ถูกต้อง'
            },
            sedol: {
                'default': 'โปรดระบุหมายเลข SEDOL ให้ถูกต้อง'
            },
            siren: {
                'default': 'โปรดระบุหมายเลข SIREN ให้ถูกต้อง'
            },
            siret: {
                'default': 'โปรดระบุหมายเลข SIRET ให้ถูกต้อง'
            },
            step: {
                'default': 'โปรดระบุลำดับของ %s'
            },
            stringCase: {
                'default': 'โปรดระบุตัวอักษรพิมพ์เล็กเท่านั้น',
                upper: 'โปรดระบุตัวอักษรพิมพ์ใหญ่เท่านั้น'
            },
            stringLength: {
                'default': 'ค่าที่ระบุยังไม่ครบตามจำนวนที่กำหนด',
                less: 'โปรดระบุค่าตัวอักษรน้อยกว่า %s ตัว',
                more: 'โปรดระบุค่าตัวอักษรมากกว่า %s ตัว',
                between: 'โปรดระบุค่าตัวอักษรระหว่าง %s ถึง %s ตัวอักษร'
            },
            uri: {
                'default': 'โปรดระบุค่า URI ให้ถูกต้อง'
            },
            uuid: {
                'default': 'โปรดระบุหมายเลข UUID ให้ถูกต้อง',
                version: 'โปรดระบุหมายเลข UUID ในเวอร์ชั่น %s'
            },
            vat: {
                'default': 'โปรดระบุจำนวนภาษีมูลค่าเพิ่ม',
                country: 'โปรดระบุจำนวนภาษีมูลค่าเพิ่มใน %s',
                countries: {
                    AT: 'ออสเตรีย',
                    BE: 'เบลเยี่ยม',
                    BG: 'บัลแกเรีย',
                    BR: 'บราซิล',
                    CH: 'วิตเซอร์แลนด์',
                    CY: 'ไซปรัส',
                    CZ: 'สาธารณรัฐเชค',
                    DE: 'เยอรมัน',
                    DK: 'เดนมาร์ก',
                    EE: 'เอสโตเนีย',
                    ES: 'สเปน',
                    FI: 'ฟินแลนด์',
                    FR: 'ฝรั่งเศส',
                    GB: 'สหราชอาณาจักร',
                    GR: 'กรีซ',
                    EL: 'กรีซ',
                    HU: 'ฮังการี',
                    HR: 'โครเอเชีย',
                    IE: 'ไอร์แลนด์',
                    IS: 'ไอซ์',
                    IT: 'อิตาลี',
                    LT: 'ลิทัวเนีย',
                    LU: 'ลักเซมเบิร์ก',
                    LV: 'ลัตเวีย',
                    MT: 'มอลตา',
                    NL: 'เนเธอร์แลนด์',
                    NO: 'นอร์เวย์',
                    PL: 'โปแลนด์',
                    PT: 'โปรตุเกส',
                    RO: 'โรมาเนีย',
                    RU: 'รัสเซีย',
                    RS: 'เซอร์เบีย',
                    SE: 'สวีเดน',
                    SI: 'สโลวีเนีย',
                    SK: 'สโลวาเกีย',
                    VE: 'เวเนซูเอลา',
                    ZA: 'แอฟริกาใต้'
                }
            },
            vin: {
                'default': 'โปรดระบุหมายเลข VIN ให้ถูกต้อง'
            },
            zipCode: {
                'default': 'โปรดระบุรหัสไปรษณีย์ให้ถูกต้อง',
                country: 'โปรดระบุรหัสไปรษณีย์ให้ถูกต้องใน %s',
                countries: {
                    AT: 'ออสเตรีย',
                    BG: 'บัลแกเรีย',
                    BR: 'บราซิล',
                    CA: 'แคนาดา',
                    CH: 'วิตเซอร์แลนด์',
                    CZ: 'สาธารณรัฐเชค',
                    DE: 'เยอรมนี',
                    DK: 'เดนมาร์ก',
                    ES: 'สเปน',
                    FR: 'ฝรั่งเศส',
                    GB: 'สหราชอาณาจักร',
                    IE: 'ไอร์แลนด์',
                    IN: 'อินเดีย',
                    IT: 'อิตาลี',
                    MA: 'โมร็อกโก',
                    NL: 'เนเธอร์แลนด์',
                    PL: 'โปแลนด์',
                    PT: 'โปรตุเกส',
                    RO: 'โรมาเนีย',
                    RU: 'รัสเซีย',
                    SE: 'สวีเดน',
                    SG: 'สิงคโปร์',
                    SK: 'สโลวาเกีย',
                    US: 'สหรัฐอเมริกา'
                }
            }
        }
    });
}(jQuery));
