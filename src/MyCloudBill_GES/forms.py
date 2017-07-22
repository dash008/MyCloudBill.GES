
from django.contrib.auth.models import User, Group
from django import forms
from MyCloudBill_GES.models import Solicitud, UserProfile, Busqueda, Factura, Distribucion, NuevosRecursos, Negociacion, Empresa
from datetime import datetime
#from datetimewidget.widgets import DateTimeWidget
from django.contrib.admin import widgets
from django.forms import extras


class  SolicitudForm(forms.ModelForm):	
    # Opciones
    backupimagenes_choices= (('Si','Si'),('No','No'))
    sistemaoperativo_choices = (('AIX Version 5.3','AIX Version 5.3'), ('CentOS release 4.2','CentOS release 4.2'), ('CentOS release 4.4','CentOS release 4.4'), ('CentOS release 4.8','CentOS release 4.8'), ('CentOS release 5.2','CentOS release 5.2'), ('Fedora Core release 3','Fedora Core release 3'), ('HP-UV Version 11.23','HP-UV Version 11.23'), ('Microsoft Windows Server 2003 enterprise',' Microsoft Windows Server 2003 enterprise'), ('Microsoft Windows Server 2003 estandar','Microsoft Windows Server 2003 estandar'), ('Microsoft Windows Server 2003 R2 enterprise','Microsoft Windows Server 2003 R2 enterprise'), ('Microsoft Windows Server 2003 R2 estandar','Microsoft Windows Server 2003 R2 estandar'), ('Microsoft Windows Server 2008 enterprise',' Microsoft Windows Server 2008 enterprise'), ('Microsoft Windows Server 2008 estandar','Microsoft Windows Server 2008 estandar'), ('Red Hat Enterprise Linux 4.5','Red Hat Enterprise Linux 4.5'), ('Red Hat Enterprise Linux 5',' Red Hat Enterprise Linux 5'), ('Red Hat Enterprise Linux AS release 4',' Red Hat Enterprise Linux AS release 4'), ('Red Hat Enterprise Linux Server release 5','Red Hat Enterprise Linux Server release 5'), ('Red Hat Enterprise Linux Server release 5.3','Red Hat Enterprise Linux Server release 5.3'), ('Red Hat Linux 2.6.9','Red Hat Linux 2.6.9'), ('Red Hat Linux 4','Red Hat Linux 4'), ('OS/400 V5R4M0','OS/400 V5R4M0'), ('OS/400 V5R3M0','OS/400 V5R3M0'), ('OS/400 V6R1M0','OS/400 V6R1M0'), ('Red Hat Enterprise Linux Server release 5.5','Red Hat Enterprise Linux Server release 5.5'), ('Vmware ESXI 4.1','Vmware ESXI 4.1'), ('Vmware ESX 4.1','Vmware ESX 4.1'), ('Microsoft Windows Server 2008 R2 enterprise','Microsoft Windows Server 2008 R2 enterprise'), ('Microsoft Windows Server 2008 R2 estandar','Microsoft Windows Server 2008 R2 estandar'), ('Red Hat Linux Enterprise 5 64 Bits','Red Hat Linux Enterprise 5 64 Bits'), ('Red Hat Entreprise 6.0  x86-64','Red Hat Entreprise 6.0  x86-64'), ('OS/400 V5R2M0','OS/400 V5R2M0'), ('Fedora Core release 5','Fedora Core release 5'), ('System i OS/i5 V6R1M0','System i OS/i5 V6R1M0'), ('Red Hat Enterprise Linux Server release 6.1','Red Hat Enterprise Linux Server release 6.1'), ('Red Hat Linux Enterprise 6.2 64 Bits ','Red Hat Linux Enterprise 6.2 64 Bits '), ('Intel Xeon (TM)','Intel Xeon (TM)'), ('VMWARE ESXI 5.1','VMWARE ESXI 5.1'), ('VMWARE ESXI 4.0','VMWARE ESXI 4.0'), ('SUSE Linux Enterprise Server 11 (x86_64)','SUSE Linux Enterprise Server 11 (x86_64)'), ('Novell Access Manager - Access Gateway Appliance 3.1.3 (i586)','Novell Access Manager - Access Gateway Appliance 3.1.3 (i586)'), ('Red Hat Enterprise Linux Server release 6.2','Red Hat Enterprise Linux Server release 6.2'), ('Red Hat Enterprise Linux AS release 4','Red Hat Enterprise Linux AS release 4'), ('Red Hat Enterprise Linux Server release 5.1','Red Hat Enterprise Linux Server release 5.1'), ('Red Hat Enterprise Linux Server release 6.3 ','Red Hat Enterprise Linux Server release 6.3 '), ('Red Hat Enterprise Linux Server release 5.7 ','Red Hat Enterprise Linux Server release 5.7 '), ('Red Hat Enterprise Linux Server release 5.5','Red Hat Enterprise Linux Server release 5.5'), ('SUSE Linux Enterprise Server 11 SP1','SUSE Linux Enterprise Server 11 SP1'), ('CentOS release 5.5','CentOS release 5.5'), ('Back Tack 5 ','Back Tack 5 '), ('VMWARE ESXI 5.0','VMWARE ESXI 5.0'), ('Red Hat Enterprise Linux Server release 6.4','Red Hat Enterprise Linux Server release 6.4'), ('Microsoft Windows Server 2012','Microsoft Windows Server 2012'), ('Red Hat Enterprise Linux Server release 6.5','Red Hat Enterprise Linux Server release 6.5'), ('Windows Server 2012 R2','Windows Server 2012 R2'), ('AIX 6.1.6.3 TL06','AIX 6.1.6.3 TL06'), ('RED HAT LINUX ENTERPRISE 5.6 X86_64','RED HAT LINUX ENTERPRISE 5.6 X86_64'), ('AIX 5.3.12.1 TL08','AIX 5.3.12.1 TL08'))
    plataforma_choices = (('Windows','Windows'),('Linux','Linux'),('Aix','Aix'),('i5/OS','i5/OS'))
    basededatos_choices = (('Oracle','Oracle'),('SQL Server','SQL Server'),('SYBASE','SYBASE'),('iSeries DB2','iSeries DB2'))
    procesador_choices = (('Intel Xeon E5450','Intel Xeon E5450'),('POWER 4','POWER 4'),('POWER 5 PLUS','POWER 5 PLUS'), ('POWER 6','POWER 6'), ('E5420','E5420'), ('E6305','E6305'), ('POWER PC','POWER PC'), ('Intel Xeon E7330','Intel Xeon E7330'), ('Intel Xeon E7350','Intel Xeon E7350'), ('Intel Xeon E7320','Intel Xeon E7320'), ('Intel Xeon E5440','Intel Xeon E5440'), ('Processor 2352','Processor 2352'), ('Intel Xeon MP','Intel Xeon MP'), ('Intel Xeon E5405','Intel Xeon E5405'), ('Intel Xeon 5160','Intel Xeon 5160'), ('Intel Xeon E5540','Intel Xeon E5540'), ('Intel xeon L5530','Intel xeon L5530'), ('Intel Xeon W3503','Intel Xeon W3503'), ('Intel Xeon E5520 ','Intel Xeon E5520 '), ('Intel Xeon Quad Core','Intel Xeon Quad Core'), ('Intel Pentium IV Xeon','Intel Pentium IV Xeon'), ('Intel Pentium IV','Intel Pentium IV'), ('Intel Xeon E5335','Intel Xeon E5335'), ('Montecito','Montecito'), ('AMD Opteron (tm) Processor ','AMD Opteron (tm) Processor '), ('Intel Core Duo','Intel Core Duo'), ('Intel Pentium D','Intel Pentium D'), ('Intel Xeon Core 2','Intel Xeon Core 2'), ('CPW-POWERPC','CPW-POWERPC'), ('POWER 7 - TIPO 8351','POWER 7 - TIPO 8351'), ('E7540','E7540'), ('Intel Xeon E5620','Intel Xeon E5620'), (' Intel Xeon E5650',' Intel Xeon E5650'), ('POWER 7','POWER 7'), ('Intel(R) Xeon (R) E5430 ','Intel(R) Xeon (R) E5430 '), (' Intel(R) Xeon(R) CPU E5504 ',' Intel(R) Xeon(R) CPU E5504 '), ('XEON DUAL-CORE 5160','XEON DUAL-CORE 5160'), ('Intel(R) Pentium(R) III Xeon ','Intel(R) Pentium(R) III Xeon '), ('Intel ® Xeon ™','Intel ® Xeon ™'), ('Intel Xeon E7540','Intel Xeon E7540'), ('Intel Xeon E5649','Intel Xeon E5649'), ('Intel Xeon E5530','Intel Xeon E5530'), ('INTEL XEON E5-2407','INTEL XEON E5-2407'), ('INTEL XEON E5-2690','INTEL XEON E5-2690'), ('INTEL XEON E5-2630 V2','INTEL XEON E5-2630 V2'))
    memoria_choices = (('1 GB','1 GB'), ('1.2 GB','1.2 GB'), ('1.5. GB','1.5. GB'), ('1.95 GB','1.95 GB'), ('2 GB','2 GB'), ('2.5. GB','2.5. GB'), ('3 GB','3 GB'), ('3.5 GB','3.5 GB'), ('4 GB','4 GB'), ('4.5 GB','4.5 GB'), ('4.9 GB','4.9 GB'), ('5 GB','5 GB'), ('5.5 GB','5.5 GB'), ('6 GB','6 GB'), ('6.5 GB','6.5 GB'), ('7 GB','7 GB'), ('7.4 GB','7.4 GB'), ('7.52 GB','7.52 GB'), ('7.65 GB','7.65 GB'), ('8 GB','8 GB'), ('9 GB','9 GB'), ('9.8 GB','9.8 GB'), ('10 GB','10 GB'), ('11 GB','11 GB'), ('12 GB','12 GB'), ('13 GB','13 GB'), ('13.12 GB','13.12 GB'), ('14 GB','14 GB'), ('15 GB','15 GB'), ('16 GB','16 GB'), ('17 GB','17 GB'), ('18 GB','18 GB'), ('19 GB','19 GB'), ('20 GB','20 GB'), ('21 GB','21 GB'), ('21.5 GB','21.5 GB'), ('22 GB','22 GB'), ('23 GB','23 GB'), ('24 GB','24 GB'), ('25 GB','25 GB'), ('26 GB','26 GB'), ('27 GB','27 GB'), ('28 GB','28 GB'), ('29 GB','29 GB'), ('30 GB','30 GB'), ('30.75 GB','30.75 GB'), ('31 GB','31 GB'), ('32 GB','32 GB'), ('34 GB','34 GB'), ('40 GB','40 GB'), ('58 GB','58 GB'), ('60GB','60GB'), ('64 GB','64 GB'), ('75 GB','75 GB'), ('96 GB','96 GB'), ('98 GB','98 GB'), ('128 GB','128 GB'), ('4 GB','4 GB'), ('8 GB','8 GB'), ('12 GB','12 GB'), ('16 GB','16 GB'), ('20 GB','20 GB'), ('24 GB','24 GB'), ('28 GB','28 GB'), ('32 GB','32 GB'), ('36 GB','36 GB'), ('40 GB','40 GB'), ('44 GB','44 GB'), ('48 GB','48 GB'), ('52 GB','52 GB'), ('56 GB','56 GB'), ('60 GB','60 GB'), ('64 GB','64 GB'), ('68 GB','68 GB'), ('72 GB','72 GB'), ('76 GB','76 GB'), ('80 GB','80 GB'), ('84 GB','84 GB'), ('88 GB','88 GB'), ('92 GB','92 GB'), ('96 GB','96 GB'), ('100 GB','100 GB'), ('104 GB','104 GB'), ('108 GB','108 GB'), ('112 GB','112 GB'), ('116 GB','116 GB'), ('120 GB','120 GB'), ('124 GB','124 GB'), ('128 GB','128 GB'), ('132 GB','132 GB'), ('136 GB','136 GB'), ('140 GB','140 GB'), ('144 GB','144 GB'), ('148 GB','148 GB'), ('152 GB','152 GB'), ('156 GB','156 GB'), ('160 GB','160 GB'), ('164 GB','164 GB'), ('168 GB','168 GB'), ('172 GB','172 GB'), ('176 GB','176 GB'), ('180 GB','180 GB'), ('184 GB','184 GB'), ('188 GB','188 GB'), ('192 GB','192 GB'), ('196 GB','196 GB'), ('200 GB','200 GB'), ('204 GB','204 GB'), ('208 GB','208 GB'), ('212 GB','212 GB'), ('216 GB','216 GB'), ('220 GB','220 GB'), ('224 GB','224 GB'), ('228 GB','228 GB'), ('232 GB','232 GB'), ('236 GB','236 GB'), ('240 GB','240 GB'), ('244 GB','244 GB'), ('248 GB','248 GB'), ('252 GB','252 GB'), ('256 GB','256 GB'), ('260 GB','260 GB'), ('264 GB','264 GB'), ('268 GB','268 GB'), ('272 GB','272 GB'), ('276 GB','276 GB'), ('280 GB','280 GB'), ('284 GB','284 GB'), ('288 GB','288 GB'), ('292 GB','292 GB'), ('296 GB','296 GB'), ('300 GB','300 GB'), ('304 GB','304 GB'), ('308 GB','308 GB'), ('312 GB','312 GB'), ('316 GB','316 GB'), ('320 GB','320 GB'), ('324 GB','324 GB'), ('328 GB','328 GB'), ('332 GB','332 GB'), ('336 GB','336 GB'), ('340 GB','340 GB'), ('344 GB','344 GB'), ('348 GB','348 GB'), ('352 GB','352 GB'), ('356 GB','356 GB'), ('360 GB','360 GB'), ('364 GB','364 GB'), ('368 GB','368 GB'), ('372 GB','372 GB'), ('376 GB','376 GB'), ('380 GB','380 GB'), ('384 GB','384 GB'), ('388 GB','388 GB'), ('392 GB','392 GB'), ('396 GB','396 GB'), ('400 GB','400 GB'), ('404 GB','404 GB'), ('408 GB','408 GB'), ('412 GB','412 GB'), ('416 GB','416 GB'), ('420 GB','420 GB'), ('424 GB','424 GB'), ('428 GB','428 GB'), ('432 GB','432 GB'), ('436 GB','436 GB'), ('440 GB','440 GB'), ('444 GB','444 GB'), ('448 GB','448 GB'), ('452 GB','452 GB'), ('456 GB','456 GB'), ('460 GB','460 GB'), ('464 GB','464 GB'), ('468 GB','468 GB'), ('472 GB','472 GB'), ('476 GB','476 GB'), ('480 GB','480 GB'), ('484 GB','484 GB'), ('488 GB','488 GB'), ('492 GB','492 GB'), ('496 GB','496 GB'), ('500 GB','500 GB'), ('504 GB','504 GB'), ('508 GB','508 GB'), ('512 GB','512 GB'), ('516 GB','516 GB'), ('520 GB','520 GB'), ('524 GB','524 GB'), ('528 GB','528 GB'), ('532 GB','532 GB'), ('536 GB','536 GB'), ('540 GB','540 GB'), ('544 GB','544 GB'), ('548 GB','548 GB'), ('552 GB','552 GB'), ('556 GB','556 GB'), ('560 GB','560 GB'), ('564 GB','564 GB'), ('568 GB','568 GB'), ('572 GB','572 GB'), ('576 GB','576 GB'), ('580 GB','580 GB'), ('584 GB','584 GB'), ('588 GB','588 GB'), ('592 GB','592 GB'), ('596 GB','596 GB'), ('600 GB','600 GB'), ('604 GB','604 GB'), ('608 GB','608 GB'), ('612 GB','612 GB'), ('616 GB','616 GB'), ('620 GB','620 GB'), ('624 GB','624 GB'), ('628 GB','628 GB'), ('632 GB','632 GB'), ('636 GB','636 GB'), ('640 GB','640 GB'), ('644 GB','644 GB'), ('648 GB','648 GB'), ('652 GB','652 GB'), ('656 GB','656 GB'), ('660 GB','660 GB'), ('664 GB','664 GB'), ('668 GB','668 GB'), ('672 GB','672 GB'), ('676 GB','676 GB'), ('680 GB','680 GB'), ('684 GB','684 GB'), ('688 GB','688 GB'), ('692 GB','692 GB'), ('696 GB','696 GB'), ('700 GB','700 GB'), ('704 GB','704 GB'), ('708 GB','708 GB'), ('712 GB','712 GB'), ('716 GB','716 GB'), ('720 GB','720 GB'), ('724 GB','724 GB'), ('728 GB','728 GB'), ('732 GB','732 GB'), ('736 GB','736 GB'), ('740 GB','740 GB'), ('744 GB','744 GB'), ('748 GB','748 GB'), ('752 GB','752 GB'), ('756 GB','756 GB'), ('760 GB','760 GB'), ('764 GB','764 GB'), ('768 GB','768 GB'), ('772 GB','772 GB'), ('776 GB','776 GB'), ('780 GB','780 GB'), ('784 GB','784 GB'), ('788 GB','788 GB'), ('792 GB','792 GB'), ('796 GB','796 GB'), ('800 GB','800 GB'), ('804 GB','804 GB'), ('808 GB','808 GB'), ('812 GB','812 GB'), ('816 GB','816 GB'), ('820 GB','820 GB'), ('824 GB','824 GB'), ('828 GB','828 GB'), ('832 GB','832 GB'), ('836 GB','836 GB'), ('840 GB','840 GB'), ('844 GB','844 GB'), ('848 GB','848 GB'), ('852 GB','852 GB'), ('856 GB','856 GB'), ('860 GB','860 GB'), ('864 GB','864 GB'), ('868 GB','868 GB'), ('872 GB','872 GB'), ('876 GB','876 GB'), ('880 GB','880 GB'), ('884 GB','884 GB'), ('888 GB','888 GB'), ('892 GB','892 GB'), ('896 GB','896 GB'), ('900 GB','900 GB'), ('904 GB','904 GB'), ('908 GB','908 GB'), ('912 GB','912 GB'), ('916 GB','916 GB'), ('920 GB','920 GB'), ('924 GB','924 GB'), ('928 GB','928 GB'), ('932 GB','932 GB'), ('936 GB','936 GB'), ('940 GB','940 GB'), ('944 GB','944 GB'), ('948 GB','948 GB'), ('952 GB','952 GB'), ('956 GB','956 GB'), ('960 GB','960 GB'), ('964 GB','964 GB'), ('968 GB','968 GB'), ('972 GB','972 GB'), ('976 GB','976 GB'), ('980 GB','980 GB'), ('984 GB','984 GB'), ('988 GB','988 GB'), ('992 GB','992 GB'), ('996 GB','996 GB'), ('1000 GB','1000 GB'), ('1004 GB','1004 GB'), ('1008 GB','1008 GB'), ('1012 GB','1012 GB'), ('1016 GB','1016 GB'), ('1020 GB','1020 GB'), ('1024 GB','1024 GB'))
    procesamiento_choices = (('1.8 Ghz','1.8 Ghz'), ('2.0 Ghz','2.0 Ghz'), ('2.1 Ghz','2.1 Ghz'), ('2.2 Ghz','2.2 Ghz'), ('2.3 Ghz','2.3 Ghz'), ('2.4 Ghz','2.4 Ghz'), ('3.0 Ghz','3.0 Ghz'), ('1100 CPW','1100 CPW'), ('5500 CPW','5500 CPW'), ('2.5 Ghz','2.5 Ghz'), ('2.9 Ghz','2.9 Ghz'), ('2.8 Ghz','2.8 Ghz'), ('2.13 Ghz','2.13 Ghz'), ('4.7 Ghz','4.7 Ghz'), ('2.66 Ghz','2.66 Ghz'), ('2.27 Ghz','2.27 Ghz'), ('2.93 Ghz','2.93 Ghz'), ('2.83 Ghz','2.83 Ghz'), ('2.26 Ghz','2.26 Ghz'), ('2.66 Ghz','2.66 Ghz'), ('2.6Ghz','2.6Ghz'), ('3.20Ghz','3.20Ghz'), ('4.20GHz','4.20GHz'), ('3,4 GHz','3,4 GHz'), ('3.10 Ghz','3.10 Ghz'), ('3.2 Ghz','3.2 Ghz'))
    estado_choices = (('EnAprobacionArq','En aprobacion Arquitecto'),('EnAprobacion','En aprobacion Jefe Infraestructura'),('EnValoracion','En Valoracion'),('Aprobado','Aprobado'),('Disponible','Disponible'),('Uso','Uso'),('Liberado','Liberado'),('Contabilizado','Contabilizado'),('ParaPago','ParaPago'),('Finalizado','Finalizado'))
    almacenamiento_choices = (('1 GB','1 GB'),('1.2 GB','1.2 GB'),('1.5. GB','1.5. GB'),('1.95 GB','1.95 GB'),('2 GB','2 GB'),('2.5. GB','2.5. GB'),('3 GB','3 GB'),('3.5 GB','3.5 GB'),('4 GB','4 GB'),('4.5 GB','4.5 GB'),('4.9 GB','4.9 GB'),('5 GB','5 GB'),('5.5 GB','5.5 GB'),('6 GB','6 GB'),('6.5 GB','6.5 GB'),('7 GB','7 GB'),('7.4 GB','7.4 GB'),('7.52 GB','7.52 GB'),('7.65 GB','7.65 GB'),('8 GB','8 GB'),('9 GB','9 GB'),('9.8 GB','9.8 GB'),('10 GB','10 GB'),('11 GB','11 GB'),('12 GB','12 GB'),('13 GB','13 GB'),('13.12 GB','13.12 GB'),('14 GB','14 GB'),('15 GB','15 GB'),('16 GB','16 GB'),('17 GB','17 GB'),('18 GB','18 GB'),('19 GB','19 GB'),('20 GB','20 GB'),('21 GB','21 GB'),('21.5 GB','21.5 GB'),('22 GB','22 GB'),('23 GB','23 GB'),('24 GB','24 GB'),('25 GB','25 GB'),('26 GB','26 GB'),('27 GB','27 GB'),('28 GB','28 GB'),('29 GB','29 GB'),('30 GB','30 GB'),('30.75 GB','30.75 GB'),('31 GB','31 GB'),('32 GB','32 GB'),('34 GB','34 GB'),('40 GB','40 GB'),('58 GB','58 GB'),('60GB','60GB'),('64 GB','64 GB'),('75 GB','75 GB'),('96 GB','96 GB'),('98 GB','98 GB'),('128 GB','128 GB'),('4 GB','4 GB'),('8 GB','8 GB'),('12 GB','12 GB'),('16 GB','16 GB'),('20 GB','20 GB'),('24 GB','24 GB'),('28 GB','28 GB'),('32 GB','32 GB'),('36 GB','36 GB'),('40 GB','40 GB'),('44 GB','44 GB'),('48 GB','48 GB'),('52 GB','52 GB'),('56 GB','56 GB'),('60 GB','60 GB'),('64 GB','64 GB'),('68 GB','68 GB'),('72 GB','72 GB'),('76 GB','76 GB'),('80 GB','80 GB'),('84 GB','84 GB'),('88 GB','88 GB'),('92 GB','92 GB'),('96 GB','96 GB'),('100 GB','100 GB'),('104 GB','104 GB'),('108 GB','108 GB'),('112 GB','112 GB'),('116 GB','116 GB'),('120 GB','120 GB'),('124 GB','124 GB'),('128 GB','128 GB'),('132 GB','132 GB'),('136 GB','136 GB'),('140 GB','140 GB'),('144 GB','144 GB'),('148 GB','148 GB'),('152 GB','152 GB'),('156 GB','156 GB'),('160 GB','160 GB'),('164 GB','164 GB'),('168 GB','168 GB'),('172 GB','172 GB'),('176 GB','176 GB'),('180 GB','180 GB'),('184 GB','184 GB'),('188 GB','188 GB'),('192 GB','192 GB'),('196 GB','196 GB'),('200 GB','200 GB'),('204 GB','204 GB'),('208 GB','208 GB'),('212 GB','212 GB'),('216 GB','216 GB'),('220 GB','220 GB'),('224 GB','224 GB'),('228 GB','228 GB'),('232 GB','232 GB'),('236 GB','236 GB'),('240 GB','240 GB'),('244 GB','244 GB'),('248 GB','248 GB'),('252 GB','252 GB'),('256 GB','256 GB'),('260 GB','260 GB'),('264 GB','264 GB'),('268 GB','268 GB'),('272 GB','272 GB'),('276 GB','276 GB'),('280 GB','280 GB'),('284 GB','284 GB'),('288 GB','288 GB'),('292 GB','292 GB'),('296 GB','296 GB'),('300 GB','300 GB'),('304 GB','304 GB'),('308 GB','308 GB'),('312 GB','312 GB'),('316 GB','316 GB'),('320 GB','320 GB'),('324 GB','324 GB'),('328 GB','328 GB'),('332 GB','332 GB'),('336 GB','336 GB'),('340 GB','340 GB'),('344 GB','344 GB'),('348 GB','348 GB'),('352 GB','352 GB'),('356 GB','356 GB'),('360 GB','360 GB'),('364 GB','364 GB'),('368 GB','368 GB'),('372 GB','372 GB'),('376 GB','376 GB'),('380 GB','380 GB'),('384 GB','384 GB'),('388 GB','388 GB'),('392 GB','392 GB'),('396 GB','396 GB'),('400 GB','400 GB'),('404 GB','404 GB'),('408 GB','408 GB'),('412 GB','412 GB'),('416 GB','416 GB'),('420 GB','420 GB'),('424 GB','424 GB'),('428 GB','428 GB'),('432 GB','432 GB'),('436 GB','436 GB'),('440 GB','440 GB'),('444 GB','444 GB'),('448 GB','448 GB'),('452 GB','452 GB'),('456 GB','456 GB'),('460 GB','460 GB'),('464 GB','464 GB'),('468 GB','468 GB'),('472 GB','472 GB'),('476 GB','476 GB'),('480 GB','480 GB'),('484 GB','484 GB'),('488 GB','488 GB'),('492 GB','492 GB'),('496 GB','496 GB'),('500 GB','500 GB'),('504 GB','504 GB'),('508 GB','508 GB'),('512 GB','512 GB'),('516 GB','516 GB'),('520 GB','520 GB'),('524 GB','524 GB'),('528 GB','528 GB'),('532 GB','532 GB'),('536 GB','536 GB'),('540 GB','540 GB'),('544 GB','544 GB'),('548 GB','548 GB'),('552 GB','552 GB'),('556 GB','556 GB'),('560 GB','560 GB'),('564 GB','564 GB'),('568 GB','568 GB'),('572 GB','572 GB'),('576 GB','576 GB'),('580 GB','580 GB'),('584 GB','584 GB'),('588 GB','588 GB'),('592 GB','592 GB'),('596 GB','596 GB'),('600 GB','600 GB'),('604 GB','604 GB'),('608 GB','608 GB'),('612 GB','612 GB'),('616 GB','616 GB'),('620 GB','620 GB'),('624 GB','624 GB'),('628 GB','628 GB'),('632 GB','632 GB'),('636 GB','636 GB'),('640 GB','640 GB'),('644 GB','644 GB'),('648 GB','648 GB'),('652 GB','652 GB'),('656 GB','656 GB'),('660 GB','660 GB'),('664 GB','664 GB'),('668 GB','668 GB'),('672 GB','672 GB'),('676 GB','676 GB'),('680 GB','680 GB'),('684 GB','684 GB'),('688 GB','688 GB'),('692 GB','692 GB'),('696 GB','696 GB'),('700 GB','700 GB'),('704 GB','704 GB'),('708 GB','708 GB'),('712 GB','712 GB'),('716 GB','716 GB'),('720 GB','720 GB'),('724 GB','724 GB'),('728 GB','728 GB'),('732 GB','732 GB'),('736 GB','736 GB'),('740 GB','740 GB'),('744 GB','744 GB'),('748 GB','748 GB'),('752 GB','752 GB'),('756 GB','756 GB'),('760 GB','760 GB'),('764 GB','764 GB'),('768 GB','768 GB'),('772 GB','772 GB'),('776 GB','776 GB'),('780 GB','780 GB'),('784 GB','784 GB'),('788 GB','788 GB'),('792 GB','792 GB'),('796 GB','796 GB'),('800 GB','800 GB'),('804 GB','804 GB'),('808 GB','808 GB'),('812 GB','812 GB'),('816 GB','816 GB'),('820 GB','820 GB'),('824 GB','824 GB'),('828 GB','828 GB'),('832 GB','832 GB'),('836 GB','836 GB'),('840 GB','840 GB'),('844 GB','844 GB'),('848 GB','848 GB'),('852 GB','852 GB'),('856 GB','856 GB'),('860 GB','860 GB'),('864 GB','864 GB'),('868 GB','868 GB'),('872 GB','872 GB'),('876 GB','876 GB'),('880 GB','880 GB'),('884 GB','884 GB'),('888 GB','888 GB'),('892 GB','892 GB'),('896 GB','896 GB'),('900 GB','900 GB'),('904 GB','904 GB'),('908 GB','908 GB'),('912 GB','912 GB'),('916 GB','916 GB'),('920 GB','920 GB'),('924 GB','924 GB'),('928 GB','928 GB'),('932 GB','932 GB'),('936 GB','936 GB'),('940 GB','940 GB'),('944 GB','944 GB'),('948 GB','948 GB'),('952 GB','952 GB'),('956 GB','956 GB'),('960 GB','960 GB'),('964 GB','964 GB'),('968 GB','968 GB'),('972 GB','972 GB'),('976 GB','976 GB'),('980 GB','980 GB'),('984 GB','984 GB'),('988 GB','988 GB'),('992 GB','992 GB'),('996 GB','996 GB'),('1000 GB','1000 GB'),('1004 GB','1004 GB'),('1008 GB','1008 GB'),('1012 GB','1012 GB'),('1016 GB','1016 GB'),('1020 GB','1020 GB'),('1024 GB','1024 GB'))

    # Campos

    plataforma = forms.ChoiceField(choices = plataforma_choices, label = 'Plataforma')
    sistemaoperativo = forms.ChoiceField(choices = sistemaoperativo_choices, label='Sistema Operativo')
    basededatos = forms.ChoiceField(choices = basededatos_choices, label = 'Base de Datos')
    procesador = forms.ChoiceField(choices = procesador_choices, label = 'Procesador')
    procesamiento = forms.ChoiceField(choices = procesamiento_choices,label='Velocidad Procesador')
    numeroprocesadores = forms.IntegerField(label ='Numero de procesadores', max_value = 8, min_value = 1, initial = 1)
    memoria = forms.ChoiceField(choices= memoria_choices, label ='Memoria RAM en GB')
    almacenamiento = forms.ChoiceField(choices= almacenamiento_choices,label = 'Almacenamiento en GB')
    backupimagenes = forms.ChoiceField(choices = backupimagenes_choices, label = 'Backup de Imagenes')
    tiempodeuso = forms.IntegerField( label = 'Tiempo de uso del recurso en meses',max_value=36,min_value=1)
    cantidaddeusuarios = forms.IntegerField(label='Cantidad de usuarios que dispondran del recurso',max_value=15000,min_value=1)
    justificacion = forms.CharField(widget=forms.Textarea,label= 'Justificacion',required = True,initial="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum")
    estado = forms.ChoiceField(label = 'Estado', required = False)

    class Meta:
        model = Solicitud
        fields=('plataforma','sistemaoperativo','basededatos','procesador','procesamiento','numeroprocesadores','memoria','almacenamiento','backupimagenes','estado','tiempodeuso','cantidaddeusuarios','justificacion')

    def __init__(self, *args, **kwargs):
            my_group = kwargs.pop('group')  # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole
            super(SolicitudForm, self).__init__(*args, **kwargs)
            # If the user does not belong to a certain group, remove the field
            if my_group == "['ArqSoluciones']":
                self.fields['estado']= forms.ChoiceField(choices = (('EnAprobacionArq','En aprobacion Arquitecto'),('EnAprobacion','En aprobacion Jefe de Infraestructura'),('Liberado','Liberado')) , label = 'Estado', required = False)
            elif my_group =="['JefeInfraestructura']":
                self.fields['estado']= forms.ChoiceField(choices = (('EnValoracion','En proceso de Valoracion'),('Contabilizado','Contabilizado')), label = 'Estado', required = False)
            elif my_group =="['JefeTI']":
                self.fields['estado']= forms.ChoiceField(choices = (('Aprobado','Aprobado'),('ParaPago','Para pago')), label = 'Estado', required = False)
            elif my_group =="['LiderInfraestructura']":
                self.fields['estado']= forms.ChoiceField(choices = (('Disponible','Disponible'),('Finalizado','Finalizado')), label = 'Estado', required = False)


class SearchForm(forms.ModelForm):
    search_query = forms.CharField(label="", max_length=100,  required = False,widget=forms.TextInput(attrs={'placeholder': 'Nro. Solicitud'}))
    class Meta:
        model = Busqueda
        fields =('search_query',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
            model = User
            fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):	
    rol_choices = (('CoordinadorSI','Coordinador SI'),('ArqSoluciones','Arq de Soluciones'),('JefeInfraestructura','Jefe De Infraestructura'),('JefeTI','Jefe TI'),('LiderInfraestructura','Lider de Infraestructura'))
    empresa_choices = ((1,'Financiero'),(2,'Sugiro'),(3,'vivienda'),(4,'MP'),(5,'EPS'),(6,'EME'),(7,'Homecare'),(8,'Seguros'),(9,'Solidaridad'),(10,'Vida en plenitud'),(11,'Centro Vacacional'),(12,'Agencia de viajes'),(13,'Gremial'))
    rol = forms.ChoiceField(choices =rol_choices, label = 'Rol')
    queryset = Empresa.objects.all()
    empresa = forms.ModelChoiceField(queryset, label = 'Empresa')

    class Meta:
            model = UserProfile
            fields = ('rol','empresa',)

class FacturaForm(forms.ModelForm):
    estado_choices = (('prefactura','Prefactura'),('facturadef','Factura Definitiva'))
    tiempodeservicio = forms.IntegerField(label = 'Tiempo de Servicio en Meses',max_value=36,min_value=1)
    cargototal = forms.IntegerField(label = 'Cargo Total a 24 Meses')
    cargoinicial = forms.IntegerField(label = 'Cargo inicial unica vez')
    cargomeslineabase = forms.FloatField(label = 'Cargo Mes Linea Base a 23 Meses')
    cargomescra = forms.FloatField(label = 'Cargo Mes CRA')
    cargomesnuevos = forms.IntegerField(label = 'Cargo Mes Nuevos (Servicos/Recursos)')
    estado = forms.ChoiceField(label = 'Estado de la Factura',choices = estado_choices)

    class Meta:
        model = Factura
        fields = ('tiempodeservicio','cargototal','cargoinicial','cargomeslineabase','cargomescra','cargomesnuevos','estado')

class DistribucionForm(forms.ModelForm):
    financiero = forms.IntegerField( label = '',max_value=80000,min_value=0,initial = 0)
    sugiro= forms.IntegerField( label = '',max_value=80000,min_value=0,initial = 0)
    vivienda = forms.IntegerField( label = '',max_value=80000,min_value=0,initial = 0)
    mp = forms.IntegerField( label = '',max_value=80000,min_value=0,initial = 0)
    eps = forms.IntegerField( label = '',max_value=80000,min_value=0,initial = 0)
    eme = forms.IntegerField( label = '',max_value=80000,min_value=0,initial = 0)
    homecare = forms.IntegerField( label = '',max_value=80000,min_value=0,initial = 0)
    seguros = forms.IntegerField( label = '',max_value=80000,min_value=0,initial = 0)
    solidaridad = forms.IntegerField( label = '',max_value=80000,min_value=0,initial = 0)
    vida_en_plenitud = forms.IntegerField( label = '',max_value=80000,min_value=0,initial = 0)
    centro_vacacional = forms.IntegerField( label = '',max_value=80000,min_value=0,initial = 0)
    agencia_viajes = forms.IntegerField( label = '',max_value=80000,min_value=0,initial = 0)
    gremial	 = forms.IntegerField( label = '',max_value=80000,min_value=0,initial = 0)
    id_solicitud = forms.CharField(widget = forms.HiddenInput(), required = False)


    class Meta:
        model = Distribucion
        fields = ('financiero','sugiro' ,'vivienda' ,'mp' ,'eps' ,'eme' ,'homecare' ,'seguros' ,'solidaridad' ,'vida_en_plenitud' ,'centro_vacacional' ,'agencia_viajes' ,'gremial','id_solicitud')

class NuevosRecursosForm(forms.ModelForm):
    recurso_choices = (('networking_LAN_SAN','Networking LAN y SAN'),('portal_aprovisionamiento_dinamico','Portal de aprovisionamiento dinamico'))
    id_solicitud = forms.CharField(widget = forms.HiddenInput(), required = False)
    nuevo_recurso = forms.ChoiceField(label='Nuevo recurso a adicionar',choices = recurso_choices )
    tiempo_de_uso = forms.IntegerField(label='Tiempo de uso en meses',max_value=24)

    class Meta:
        model = NuevosRecursos
        fields = ('id_solicitud','nuevo_recurso','tiempo_de_uso')

class NegociacionForm(forms.ModelForm):

    proovedor = forms.CharField(max_length = 30, label = "Proovedor")
    tiempo_de_servicio = forms.IntegerField(label="Tiempo de Servicio en meses")
    cargototal = forms.IntegerField(label = "Cargo Total")
    cargoinicial = forms.IntegerField(label = "Cargo Inicial")
    cargomeslineabase = forms.IntegerField(label = "Cargo Mes Linea Base")
    dob = forms.DateField(widget = widgets.AdminDateWidget)

    class Meta:
        model = Negociacion
        fields = ('date','fecha_negociacion','proovedor','tiempo_de_servicio','cargototal','cargoinicial','cargomeslineabase',)
        dateTimeOptions = {
                'format': 'dd/mm/yyyy HH:ii P',
                'autoclose': True,
                'showMeridian' : True}
        #widgets = {
            #Usar bootstrap 3
        #    'date': DateTimeWidget(attrs={'id': 'date'},bootstrap_version=3,usel10n=False,options = dateTimeOptions )}

class LineaBaseForm(forms.ModelForm):
    periodo_facturado = forms.CharField(label = "Periodo facturado")
    tiempodeuso = forms.IntegerField(label = "Tiempo en meses")
    cargototal = forms.IntegerField(label = "Cargo Total")
    cargoinicial = forms.IntegerField(label = "Cargo Inicial")
    cargomeslineabase = forms.IntegerField(label = "Cargo Mes Linea Base")

