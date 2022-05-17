-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- 主機： db
-- 產生時間： 2022 年 05 月 17 日 05:23
-- 伺服器版本： 8.0.28
-- PHP 版本： 8.0.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫: `work_order`
--
CREATE DATABASE IF NOT EXISTS `work_order` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `work_order`;

-- --------------------------------------------------------

--
-- 資料表結構 `central_data`
--

CREATE TABLE `central_data` (
  `product` char(50) DEFAULT NULL,
  `material` char(50) DEFAULT NULL,
  `process` char(50) DEFAULT NULL,
  `plate` char(50) DEFAULT NULL,
  `plate_thickness` char(50) DEFAULT NULL,
  `others` char(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 傾印資料表的資料 `central_data`
--

INSERT INTO `central_data` (`product`, `material`, `process`, `plate`, `plate_thickness`, `others`) VALUES
('', '', '', '', '', ''),
('舞台背板', 'PP', '亮面冷錶', '合成板', '5mm', '150直鐵腳架'),
('接待背板', 'PVC', '霧面冷錶', '豪卡板', '1cm', '180直鐵腳架'),
('展示背板', '燈片', '亮+正面雙面膠', '黑色合成板', '1.5cm', '150斜鐵腳架'),
('攤位背板', '弱黏PVC', '地板膠', '瓦楞板', '2cm', '180斜鐵腳架'),
('媒體背板', '弱黏導氣PVC', '地板膠', '黑色瓦楞板', '1mm', '橫桿'),
('報到處板', '單透布300D', '特殊加工', '發泡板', '2mm', '貼條'),
('講台背板', '雙透布150D', '厚磅紙板', '', '', '機台切型'),
('桌前背板', '油畫布600D', '', '', '', '易拉展'),
('議程背板', '油畫布900D', '', '', '', 'X展架'),
('人型立牌', '半透PVC', '', '', '', '紙腳架'),
('橫幅背板', '全透PVC', '', '', '', '組合框租用'),
('三角桌牌', '單向透視', '', '', '', 'TRUSS'),
('桌上立牌', '膠膜', '', '', '', '燈光'),
('指引牌', '帆布', '', '', '', '吊工'),
('箭頭', '壓克力', '', '', '', '鷹架搭設'),
('名牌', '保麗龍', '', '', '', '木桿'),
('桌次表', '全透PET', '', '', '', '結構'),
('摸彩箱', '', '', '', '', '特殊加工'),
('手舉牌', '', '', '', '', '其他'),
('易拉展', '', '', '', '', ''),
('X展架', '', '', '', '', ''),
('MIC牌', '', '', '', '', ''),
('海報', '', '', '', '', ''),
('簽名綢', '', '', '', '', ''),
('掛軸', '', '', '', '', ''),
('旗幟', '', '', '', '', ''),
('帆布', '', '', '', '', ''),
('關東旗', '', '', '', '', ''),
('地貼', '', '', '', '', ''),
('窗貼', '', '', '', '', ''),
('道具', '', '', '', '', ''),
('包裝', '', '', '', '', ''),
('外發', '', '', '', '', ''),
('進場', '', '', '', '', ''),
('撤場', '', '', '', '', ''),
('垃圾處理', '', '', '', '', ''),
('其他', '', '', '', '', '');

-- --------------------------------------------------------

--
-- 資料表結構 `client`
--

CREATE TABLE `client` (
  `name` char(50) NOT NULL,
  `full_name` char(50) DEFAULT NULL,
  `phone` char(50) DEFAULT NULL,
  `address` char(50) DEFAULT NULL,
  `taxID` char(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 傾印資料表的資料 `client`
--

INSERT INTO `client` (`name`, `full_name`, `phone`, `address`, `taxID`) VALUES
('', '', '', '', ''),
('6636', '陸陸參拾陸有限公司', '66368606', '10694台北市忠孝東路四段320號10樓', '27541768'),
('228基金會', '財團法人二二八事件紀念基金會', '23326228', '10066台北市南海路54號', '97971614'),
('228共生', '社團法人台灣共生青年協會', '無', '10351台北市大同區長安西路84號4樓之一', '85202463'),
('KING', '誠全整合行銷有限公司', '0938616260', '10049台北市中正區北平東路30-2號4樓', '83231490'),
('Eric', '', '0935888727', '', ''),
('AAMA', '財團法人台北市創業者共創平台基金會', '', '10058台北市中正區八德路一段1號2樓', '77793991'),
('九天馬', '九天馬整合行銷有限公司', '27207070', '11061台北市忠孝東路五段412號6樓', '84909060'),
('中央社', '財團法人中央通訊社', '25051180', '10485台北市松江路209號', '97991169'),
('可樂旅遊', '康福旅行社(股)公司', '25112556', '10457台北市中山區南京東路二段90號17樓', '04315397'),
('心連結書佾', '眾好行銷有限公司', '0933092714', '231新北市新店區如意街13巷3弄3號6樓', '50776098'),
('加密實驗', '加密實驗股份有限公司', '0988189451', '10061台北市中正區信義路二段253號', '5077293'),
('台灣原色', '台灣原色創意行銷有限公司', '0937549598', '33052桃園市大有路489號7樓之一', '28728713'),
('石盤公關', '石盤公關顧問有限公司', '27082678', '10682台北市大安區信義路四段96號5樓之2', '12939918'),
('禾睿', '禾睿整合行銷有限公司', '', '10491台北市中山區建國北路一段78巷36號1樓', '24324824'),
('亞洲黃龍', '亞洲黃隆有限公司', '27906028', '11470台北市內湖區南京東路六段346號12樓之一', '80132215'),
('林思宏醫師', '財團法人台北市林思宏X5醫師慈善基金會', '27036988', '106台北市大安區復興南路二段210巷9號', '77603660'),
('采月廣告', '采月設計有限公司', '86478840', '22172新北市汐止區茄苳路240號', '24496570'),
('冠銘廣告', '冠銘廣告企業社', '23250209', '10695台北市光復南路420巷26號', '81615718'),
('美味生活', '美味生活股份有限公司', '0981307638', '10487台北市南京東路三段89巷27弄19號1樓', '21931519'),
('時代基金會', '財團法人時代基金會', '25112678', '10449台北市中山北路二段96號後棟9樓', '76942403'),
('Lingumi', 'Lingumi', '', '10449台北市中山區中山北路二段96號後棟9樓', '82947905'),
('區塊鏈', '台灣區塊鏈愛好者協會', '0905935509', '115台北市南港區經貿二路2號', '76312926'),
('國泰人壽', '國泰人壽保險(股)公司', '27551399', '10687台北市仁愛路四段296號18樓', '03374707'),
('陳椿樺', '', '', '', ''),
('麥點公關', '麥點創意行銷有限公司', '', '10478台北市中山區合江街105巷21號', '27555544'),
('富邦金控', '台北富邦商業銀行股份有限公司', '66027527', '105台北市松山區敦化南路一段108號6樓', '03750168'),
('台灣人壽', '台灣人壽保險(股)公司', '', '11568台北市南港區經貿二陸188號7樓', '03557017'),
('聯廣', '格威傳媒股份有限公司', '26278806', '1692台北市大安區忠孝東路四段285號3樓', '1133055'),
('富越', '富越空間計畫公司有限公司', '', '23147新北市新店區新店路129號2樓', '84139350'),
('華碩雲端', '華碩雲端股份有限公司', '28987477', '25159新北市淡水區中正東路二段177號4樓', '70538068'),
('傳揚行銷', '傳揚行銷廣告(股)公司', '25021929', '10489台北市南京東路三段26號11樓', '89963035'),
('新巨企業', '新巨企業(股)公司', '', '23141新北市新店區民權路50號10樓', '20970807'),
('新綠', '新綠主義(股)公司', '77294877', '22055新北市板橋區縣民大道一段285號3樓', '28498923'),
('宏綠', '宏綠景觀(股)公司', '22720552', '22055新北市板橋區明德街2巷8號', '53705055'),
('源子設計', '源子創作館', '', '10667台北市大安區大安路二段142巷5號1樓', '10340534'),
('遠雄人壽', '遠雄人壽保險事業(股)公司', '', '11073台北市信義區松高路1號26樓', '84703052'),
('數位時代', '巨思文化(股)有限公司', '', '10694台北市光復南路二102號9樓', '16780474'),
('尚凡', '尚凡國際創新科技股份有限公司', '23650103', '106台北市大安區羅斯福路三段37號12樓', '80283629'),
('內湖扶輪社', '台北內湖扶輪社', '', '104台北市中山區松江路328號8樓之6', ''),
('創新扶輪社', '社團法人台日國際扶輪親善會', '', '23141新北市新店區民權路100號13樓', '25281631'),
('國際扶輪社', '社團法人國際扶輪3482地區', '', '', '42521538'),
('雲端扶輪社', '台北雲端扶輪社', '25238638', '104台北市中山區松江路328號8樓之6', '38583949'),
('憾聲音響', '撼聲影音有限公司', '', '23512新北市中和區立德街138號4樓', '23618744'),
('彥儒', '默默的有限公司', '0928160214', '', '83448245'),
('鴻榮', '參拾參創意行銷有限公司', '', '10352台北市大同區承德路二段1巷8號1樓', '54055163'),
('宣彩印刷', '宣彩印刷有限公司', '28421106', '23585新北市中和區建康路', '50856851'),
('試富社會', '試附社會企業有限公司', '23912288', '10652台北市忠孝東路三段96號4樓之一', '52932476'),
('繁葵', '繁葵實業股份有限公司', '0911068081', '231新北市新店區寶橋路235巷2號7樓', '97404268'),
('無設Ivan', '無設制作設計有限公司', '', '24155新北市三重區仁愛街178號3樓', '83566018'),
('燈光小尤', '意象聲動創設實業社', '', '24254新北市新莊區復興路二段130號2樓', '41381355'),
('林彥岑', '台灣數位媒體應用暨行銷協會', '77180056', '10683台北市大安區敦化南路2段2號3樓-1', '42543218'),
('優越廣告', '優越廣告(股)公司', '', '10478台北市中山區合江街105巷21號1樓', '80694833'),
('薔薇杉婚禮', '薔薇杉婚禮設計有限公司', '', '11680台北市文山區景隆街1巷7號1樓', '55800603'),
('芝山綠園', '社團法人台北市野鳥學會芝山岩管理處', '', '111台北市士林區雨聲街120號', '29207509'),
('波賽頓', '波賽頓科技有限公司', '77515558', '22246新北市深坑區北深路一段181號3樓', '24723723'),
('永達保險', '永達保險經紀人(股)公司', '25212019', '10448台北市中山區中山北路二段79號4樓', '12684149'),
('黑森林', '黑森林知識文化產業(股)公司', '27952230', '11490台北市內湖區民權東路6段216號', '54363289'),
('心心相印', '心心相印(股)公司', '', '22068新北市板橋區中山路二段403-6號9樓', '83666430'),
('資廚', '資廚管理顧問(股)公司', '27130120', '106465台北市大安區仁愛路三段136號15樓 1501室', '53750585'),
('龍骨王', '龍骨王股份有限公司', '77236027', '11577台北市南港區八德路四段768巷1弄20號B1樓A02室', '54158175');

-- --------------------------------------------------------

--
-- 資料表結構 `employee`
--

CREATE TABLE `employee` (
  `name` char(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 傾印資料表的資料 `employee`
--

INSERT INTO `employee` (`name`) VALUES
(''),
('羅浩強'),
('羅韋杰'),
('鄭志豪'),
('盧俊達');

-- --------------------------------------------------------

--
-- 資料表結構 `pack_transport`
--

CREATE TABLE `pack_transport` (
  `pack` char(50) DEFAULT NULL,
  `transport` char(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 傾印資料表的資料 `pack_transport`
--

INSERT INTO `pack_transport` (`pack`, `transport`) VALUES
('', ''),
('廢版', '自送'),
('紙箱', '派車'),
('離形紙', '快遞'),
('瓦楞紙版', '自取');

-- --------------------------------------------------------

--
-- 資料表結構 `save_basic_data`
--

CREATE TABLE `save_basic_data` (
  `worknum` char(50) NOT NULL,
  `case_name` char(50) DEFAULT NULL,
  `company_name` char(50) DEFAULT NULL,
  `phone` char(50) DEFAULT NULL,
  `client_name` char(50) DEFAULT NULL,
  `worktime` char(50) DEFAULT NULL,
  `cleanuptime` char(50) DEFAULT NULL,
  `workaddress` char(50) DEFAULT NULL,
  `pack` char(50) DEFAULT NULL,
  `transport` char(50) DEFAULT NULL,
  `cemployee1` char(50) DEFAULT NULL,
  `cemployee2` char(50) DEFAULT NULL,
  `cemployee3` char(50) DEFAULT NULL,
  `cemployee4` char(50) DEFAULT NULL,
  `cemployee5` char(50) DEFAULT NULL,
  `crossbar_width` char(50) DEFAULT NULL,
  `crossbar_amount` char(50) DEFAULT NULL,
  `crossbar_remark` char(50) DEFAULT NULL,
  `150shelter` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `180shelter` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `iron_Shelter_amount` char(50) DEFAULT NULL,
  `iron_Shelter_remark` char(50) DEFAULT NULL,
  `paper_Shelter_height` char(50) DEFAULT NULL,
  `paper_Shelter_amount` char(50) DEFAULT NULL,
  `paper_Shelter_remark` char(50) DEFAULT NULL,
  `stand_style` char(50) DEFAULT NULL,
  `stand_amount` char(50) DEFAULT NULL,
  `stand_remark` char(50) DEFAULT NULL,
  `rent1` char(50) DEFAULT NULL,
  `rent2` char(50) DEFAULT NULL,
  `remark` char(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 傾印資料表的資料 `save_basic_data`
--

INSERT INTO `save_basic_data` (`worknum`, `case_name`, `company_name`, `phone`, `client_name`, `worktime`, `cleanuptime`, `workaddress`, `pack`, `transport`, `cemployee1`, `cemployee2`, `cemployee3`, `cemployee4`, `cemployee5`, `crossbar_width`, `crossbar_amount`, `crossbar_remark`, `150shelter`, `180shelter`, `iron_Shelter_amount`, `iron_Shelter_remark`, `paper_Shelter_height`, `paper_Shelter_amount`, `paper_Shelter_remark`, `stand_style`, `stand_amount`, `stand_remark`, `rent1`, `rent2`, `remark`) VALUES
('22-05-001', '光合派對', '33', '77294877', '品妤', '', '', '', '0', '1', '0', '0', '0', '0', '0', '', '', '', 'False', 'False', '', '', '', '', '', '', '', '', '', '', ''),
('22-05-002', '嘉利康拍照道具', '9', '25112556', '雅筠', '', '', '', '0', '0', '0', '0', '0', '0', '0', '', '', '', 'False', 'False', '', '', '', '', '', '', '', '', '', '', ''),
('22-05-003', '荷蘭banner', '25', '', 'Steven', '5/10 10:00', '', '松菸文創603', '0', '0', '1', '2', '0', '0', '0', '', '', '', 'False', 'True', '6', '', '', '', '', '', '', '', '', '', '');

-- --------------------------------------------------------

--
-- 資料表結構 `save_central_data`
--

CREATE TABLE `save_central_data` (
  `worknum` char(50) NOT NULL,
  `comboBox_product_1` char(50) DEFAULT NULL,
  `comboBox_product_2` char(50) DEFAULT NULL,
  `comboBox_product_3` char(50) DEFAULT NULL,
  `comboBox_product_4` char(50) DEFAULT NULL,
  `comboBox_product_5` char(50) DEFAULT NULL,
  `comboBox_product_6` char(50) DEFAULT NULL,
  `comboBox_product_7` char(50) DEFAULT NULL,
  `comboBox_product_8` char(50) DEFAULT NULL,
  `comboBox_product_9` char(50) DEFAULT NULL,
  `comboBox_product_10` char(50) DEFAULT NULL,
  `comboBox_product_11` char(50) DEFAULT NULL,
  `comboBox_product_12` char(50) DEFAULT NULL,
  `comboBox_product_13` char(50) DEFAULT NULL,
  `comboBox_product_14` char(50) DEFAULT NULL,
  `comboBox_product_15` char(50) DEFAULT NULL,
  `lineEdit_width_1` char(50) DEFAULT NULL,
  `lineEdit_width_2` char(50) DEFAULT NULL,
  `lineEdit_width_3` char(50) DEFAULT NULL,
  `lineEdit_width_4` char(50) DEFAULT NULL,
  `lineEdit_width_5` char(50) DEFAULT NULL,
  `lineEdit_width_6` char(50) DEFAULT NULL,
  `lineEdit_width_7` char(50) DEFAULT NULL,
  `lineEdit_width_8` char(50) DEFAULT NULL,
  `lineEdit_width_9` char(50) DEFAULT NULL,
  `lineEdit_width_10` char(50) DEFAULT NULL,
  `lineEdit_width_11` char(50) DEFAULT NULL,
  `lineEdit_width_12` char(50) DEFAULT NULL,
  `lineEdit_width_13` char(50) DEFAULT NULL,
  `lineEdit_width_14` char(50) DEFAULT NULL,
  `lineEdit_width_15` char(50) DEFAULT NULL,
  `lineEdit_height_1` char(50) DEFAULT NULL,
  `lineEdit_height_2` char(50) DEFAULT NULL,
  `lineEdit_height_3` char(50) DEFAULT NULL,
  `lineEdit_height_4` char(50) DEFAULT NULL,
  `lineEdit_height_5` char(50) DEFAULT NULL,
  `lineEdit_height_6` char(50) DEFAULT NULL,
  `lineEdit_height_7` char(50) DEFAULT NULL,
  `lineEdit_height_8` char(50) DEFAULT NULL,
  `lineEdit_height_9` char(50) DEFAULT NULL,
  `lineEdit_height_10` char(50) DEFAULT NULL,
  `lineEdit_height_11` char(50) DEFAULT NULL,
  `lineEdit_height_12` char(50) DEFAULT NULL,
  `lineEdit_height_13` char(50) DEFAULT NULL,
  `lineEdit_height_14` char(50) DEFAULT NULL,
  `lineEdit_height_15` char(50) DEFAULT NULL,
  `lineEdit_amount_1` char(50) DEFAULT NULL,
  `lineEdit_amount_2` char(50) DEFAULT NULL,
  `lineEdit_amount_3` char(50) DEFAULT NULL,
  `lineEdit_amount_4` char(50) DEFAULT NULL,
  `lineEdit_amount_5` char(50) DEFAULT NULL,
  `lineEdit_amount_6` char(50) DEFAULT NULL,
  `lineEdit_amount_7` char(50) DEFAULT NULL,
  `lineEdit_amount_8` char(50) DEFAULT NULL,
  `lineEdit_amount_9` char(50) DEFAULT NULL,
  `lineEdit_amount_10` char(50) DEFAULT NULL,
  `lineEdit_amount_11` char(50) DEFAULT NULL,
  `lineEdit_amount_12` char(50) DEFAULT NULL,
  `lineEdit_amount_13` char(50) DEFAULT NULL,
  `lineEdit_amount_14` char(50) DEFAULT NULL,
  `lineEdit_amount_15` char(50) DEFAULT NULL,
  `comboBox_material_1` char(50) DEFAULT NULL,
  `comboBox_material_2` char(50) DEFAULT NULL,
  `comboBox_material_3` char(50) DEFAULT NULL,
  `comboBox_material_4` char(50) DEFAULT NULL,
  `comboBox_material_5` char(50) DEFAULT NULL,
  `comboBox_material_6` char(50) DEFAULT NULL,
  `comboBox_material_7` char(50) DEFAULT NULL,
  `comboBox_material_8` char(50) DEFAULT NULL,
  `comboBox_material_9` char(50) DEFAULT NULL,
  `comboBox_material_10` char(50) DEFAULT NULL,
  `comboBox_material_11` char(50) DEFAULT NULL,
  `comboBox_material_12` char(50) DEFAULT NULL,
  `comboBox_material_13` char(50) DEFAULT NULL,
  `comboBox_material_14` char(50) DEFAULT NULL,
  `comboBox_material_15` char(50) DEFAULT NULL,
  `comboBox_process_1` char(50) DEFAULT NULL,
  `comboBox_process_2` char(50) DEFAULT NULL,
  `comboBox_process_3` char(50) DEFAULT NULL,
  `comboBox_process_4` char(50) DEFAULT NULL,
  `comboBox_process_5` char(50) DEFAULT NULL,
  `comboBox_process_6` char(50) DEFAULT NULL,
  `comboBox_process_7` char(50) DEFAULT NULL,
  `comboBox_process_8` char(50) DEFAULT NULL,
  `comboBox_process_9` char(50) DEFAULT NULL,
  `comboBox_process_10` char(50) DEFAULT NULL,
  `comboBox_process_11` char(50) DEFAULT NULL,
  `comboBox_process_12` char(50) DEFAULT NULL,
  `comboBox_process_13` char(50) DEFAULT NULL,
  `comboBox_process_14` char(50) DEFAULT NULL,
  `comboBox_process_15` char(50) DEFAULT NULL,
  `comboBox_plate_1` char(50) DEFAULT NULL,
  `comboBox_plate_2` char(50) DEFAULT NULL,
  `comboBox_plate_3` char(50) DEFAULT NULL,
  `comboBox_plate_4` char(50) DEFAULT NULL,
  `comboBox_plate_5` char(50) DEFAULT NULL,
  `comboBox_plate_6` char(50) DEFAULT NULL,
  `comboBox_plate_7` char(50) DEFAULT NULL,
  `comboBox_plate_8` char(50) DEFAULT NULL,
  `comboBox_plate_9` char(50) DEFAULT NULL,
  `comboBox_plate_10` char(50) DEFAULT NULL,
  `comboBox_plate_11` char(50) DEFAULT NULL,
  `comboBox_plate_12` char(50) DEFAULT NULL,
  `comboBox_plate_13` char(50) DEFAULT NULL,
  `comboBox_plate_14` char(50) DEFAULT NULL,
  `comboBox_plate_15` char(50) DEFAULT NULL,
  `comboBox_thicknes_1` char(50) DEFAULT NULL,
  `comboBox_thicknes_2` char(50) DEFAULT NULL,
  `comboBox_thicknes_3` char(50) DEFAULT NULL,
  `comboBox_thicknes_4` char(50) DEFAULT NULL,
  `comboBox_thicknes_5` char(50) DEFAULT NULL,
  `comboBox_thicknes_6` char(50) DEFAULT NULL,
  `comboBox_thicknes_7` char(50) DEFAULT NULL,
  `comboBox_thicknes_8` char(50) DEFAULT NULL,
  `comboBox_thicknes_9` char(50) DEFAULT NULL,
  `comboBox_thicknes_10` char(50) DEFAULT NULL,
  `comboBox_thicknes_11` char(50) DEFAULT NULL,
  `comboBox_thicknes_12` char(50) DEFAULT NULL,
  `comboBox_thicknes_13` char(50) DEFAULT NULL,
  `comboBox_thicknes_14` char(50) DEFAULT NULL,
  `comboBox_thicknes_15` char(50) DEFAULT NULL,
  `comboBox_others_1` char(50) DEFAULT NULL,
  `comboBox_others_2` char(50) DEFAULT NULL,
  `comboBox_others_3` char(50) DEFAULT NULL,
  `comboBox_others_4` char(50) DEFAULT NULL,
  `comboBox_others_5` char(50) DEFAULT NULL,
  `comboBox_others_6` char(50) DEFAULT NULL,
  `comboBox_others_7` char(50) DEFAULT NULL,
  `comboBox_others_8` char(50) DEFAULT NULL,
  `comboBox_others_9` char(50) DEFAULT NULL,
  `comboBox_others_10` char(50) DEFAULT NULL,
  `comboBox_others_11` char(50) DEFAULT NULL,
  `comboBox_others_12` char(50) DEFAULT NULL,
  `comboBox_others_13` char(50) DEFAULT NULL,
  `comboBox_others_14` char(50) DEFAULT NULL,
  `comboBox_others_15` char(50) DEFAULT NULL,
  `lineEdit_others_amount_1` char(50) DEFAULT NULL,
  `lineEdit_others_amount_2` char(50) DEFAULT NULL,
  `lineEdit_others_amount_3` char(50) DEFAULT NULL,
  `lineEdit_others_amount_4` char(50) DEFAULT NULL,
  `lineEdit_others_amount_5` char(50) DEFAULT NULL,
  `lineEdit_others_amount_6` char(50) DEFAULT NULL,
  `lineEdit_others_amount_7` char(50) DEFAULT NULL,
  `lineEdit_others_amount_8` char(50) DEFAULT NULL,
  `lineEdit_others_amount_9` char(50) DEFAULT NULL,
  `lineEdit_others_amount_10` char(50) DEFAULT NULL,
  `lineEdit_others_amount_11` char(50) DEFAULT NULL,
  `lineEdit_others_amount_12` char(50) DEFAULT NULL,
  `lineEdit_others_amount_13` char(50) DEFAULT NULL,
  `lineEdit_others_amount_14` char(50) DEFAULT NULL,
  `lineEdit_others_amount_15` char(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 傾印資料表的資料 `save_central_data`
--

INSERT INTO `save_central_data` (`worknum`, `comboBox_product_1`, `comboBox_product_2`, `comboBox_product_3`, `comboBox_product_4`, `comboBox_product_5`, `comboBox_product_6`, `comboBox_product_7`, `comboBox_product_8`, `comboBox_product_9`, `comboBox_product_10`, `comboBox_product_11`, `comboBox_product_12`, `comboBox_product_13`, `comboBox_product_14`, `comboBox_product_15`, `lineEdit_width_1`, `lineEdit_width_2`, `lineEdit_width_3`, `lineEdit_width_4`, `lineEdit_width_5`, `lineEdit_width_6`, `lineEdit_width_7`, `lineEdit_width_8`, `lineEdit_width_9`, `lineEdit_width_10`, `lineEdit_width_11`, `lineEdit_width_12`, `lineEdit_width_13`, `lineEdit_width_14`, `lineEdit_width_15`, `lineEdit_height_1`, `lineEdit_height_2`, `lineEdit_height_3`, `lineEdit_height_4`, `lineEdit_height_5`, `lineEdit_height_6`, `lineEdit_height_7`, `lineEdit_height_8`, `lineEdit_height_9`, `lineEdit_height_10`, `lineEdit_height_11`, `lineEdit_height_12`, `lineEdit_height_13`, `lineEdit_height_14`, `lineEdit_height_15`, `lineEdit_amount_1`, `lineEdit_amount_2`, `lineEdit_amount_3`, `lineEdit_amount_4`, `lineEdit_amount_5`, `lineEdit_amount_6`, `lineEdit_amount_7`, `lineEdit_amount_8`, `lineEdit_amount_9`, `lineEdit_amount_10`, `lineEdit_amount_11`, `lineEdit_amount_12`, `lineEdit_amount_13`, `lineEdit_amount_14`, `lineEdit_amount_15`, `comboBox_material_1`, `comboBox_material_2`, `comboBox_material_3`, `comboBox_material_4`, `comboBox_material_5`, `comboBox_material_6`, `comboBox_material_7`, `comboBox_material_8`, `comboBox_material_9`, `comboBox_material_10`, `comboBox_material_11`, `comboBox_material_12`, `comboBox_material_13`, `comboBox_material_14`, `comboBox_material_15`, `comboBox_process_1`, `comboBox_process_2`, `comboBox_process_3`, `comboBox_process_4`, `comboBox_process_5`, `comboBox_process_6`, `comboBox_process_7`, `comboBox_process_8`, `comboBox_process_9`, `comboBox_process_10`, `comboBox_process_11`, `comboBox_process_12`, `comboBox_process_13`, `comboBox_process_14`, `comboBox_process_15`, `comboBox_plate_1`, `comboBox_plate_2`, `comboBox_plate_3`, `comboBox_plate_4`, `comboBox_plate_5`, `comboBox_plate_6`, `comboBox_plate_7`, `comboBox_plate_8`, `comboBox_plate_9`, `comboBox_plate_10`, `comboBox_plate_11`, `comboBox_plate_12`, `comboBox_plate_13`, `comboBox_plate_14`, `comboBox_plate_15`, `comboBox_thicknes_1`, `comboBox_thicknes_2`, `comboBox_thicknes_3`, `comboBox_thicknes_4`, `comboBox_thicknes_5`, `comboBox_thicknes_6`, `comboBox_thicknes_7`, `comboBox_thicknes_8`, `comboBox_thicknes_9`, `comboBox_thicknes_10`, `comboBox_thicknes_11`, `comboBox_thicknes_12`, `comboBox_thicknes_13`, `comboBox_thicknes_14`, `comboBox_thicknes_15`, `comboBox_others_1`, `comboBox_others_2`, `comboBox_others_3`, `comboBox_others_4`, `comboBox_others_5`, `comboBox_others_6`, `comboBox_others_7`, `comboBox_others_8`, `comboBox_others_9`, `comboBox_others_10`, `comboBox_others_11`, `comboBox_others_12`, `comboBox_others_13`, `comboBox_others_14`, `comboBox_others_15`, `lineEdit_others_amount_1`, `lineEdit_others_amount_2`, `lineEdit_others_amount_3`, `lineEdit_others_amount_4`, `lineEdit_others_amount_5`, `lineEdit_others_amount_6`, `lineEdit_others_amount_7`, `lineEdit_others_amount_8`, `lineEdit_others_amount_9`, `lineEdit_others_amount_10`, `lineEdit_others_amount_11`, `lineEdit_others_amount_12`, `lineEdit_others_amount_13`, `lineEdit_others_amount_14`, `lineEdit_others_amount_15`) VALUES
('22-05-001', '4', '4', '4', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '42', '42', '21', '', '', '', '', '', '', '', '', '', '', '', '', '59', '30', '30', '', '', '', '', '', '', '', '', '', '', '', '', '42', '8', '26', '', '', '', '', '', '', '', '', '', '', '', '', '2', '2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
('22-05-002', '37', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '60', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '20', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '6', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '4', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '7', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
('22-05-003', '1', '22', '34', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '150', '32', '', '', '', '', '', '', '', '', '', '', '', '', '', '120', '6', '', '', '', '', '', '', '', '', '', '', '', '', '', '3', '3', '', '', '', '', '', '', '', '', '', '', '', '', '', '2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '6', '', '', '', '', '', '', '', '', '', '', '', '', '', '');

-- --------------------------------------------------------

--
-- 資料表結構 `save_price_data`
--

CREATE TABLE `save_price_data` (
  `worknum` char(50) NOT NULL,
  `lineEdit_CBM_1` char(50) DEFAULT NULL,
  `lineEdit_CBM_2` char(50) DEFAULT NULL,
  `lineEdit_CBM_3` char(50) DEFAULT NULL,
  `lineEdit_CBM_4` char(50) DEFAULT NULL,
  `lineEdit_CBM_5` char(50) DEFAULT NULL,
  `lineEdit_CBM_6` char(50) DEFAULT NULL,
  `lineEdit_CBM_7` char(50) DEFAULT NULL,
  `lineEdit_CBM_8` char(50) DEFAULT NULL,
  `lineEdit_CBM_9` char(50) DEFAULT NULL,
  `lineEdit_CBM_10` char(50) DEFAULT NULL,
  `lineEdit_CBM_11` char(50) DEFAULT NULL,
  `lineEdit_CBM_12` char(50) DEFAULT NULL,
  `lineEdit_CBM_13` char(50) DEFAULT NULL,
  `lineEdit_CBM_14` char(50) DEFAULT NULL,
  `lineEdit_CBM_15` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_1` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_2` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_3` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_4` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_5` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_6` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_7` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_8` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_9` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_10` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_11` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_12` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_13` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_14` char(50) DEFAULT NULL,
  `lineEdit_CBMprice_15` char(50) DEFAULT NULL,
  `lineEdit_single_price_1` char(50) DEFAULT NULL,
  `lineEdit_single_price_2` char(50) DEFAULT NULL,
  `lineEdit_single_price_3` char(50) DEFAULT NULL,
  `lineEdit_single_price_4` char(50) DEFAULT NULL,
  `lineEdit_single_price_5` char(50) DEFAULT NULL,
  `lineEdit_single_price_6` char(50) DEFAULT NULL,
  `lineEdit_single_price_7` char(50) DEFAULT NULL,
  `lineEdit_single_price_8` char(50) DEFAULT NULL,
  `lineEdit_single_price_9` char(50) DEFAULT NULL,
  `lineEdit_single_price_10` char(50) DEFAULT NULL,
  `lineEdit_single_price_11` char(50) DEFAULT NULL,
  `lineEdit_single_price_12` char(50) DEFAULT NULL,
  `lineEdit_single_price_13` char(50) DEFAULT NULL,
  `lineEdit_single_price_14` char(50) DEFAULT NULL,
  `lineEdit_single_price_15` char(50) DEFAULT NULL,
  `lineEdit_single_price_16` char(50) DEFAULT NULL,
  `lineEdit_single_price_17` char(50) DEFAULT NULL,
  `lineEdit_single_price_18` char(50) DEFAULT NULL,
  `lineEdit_single_price_19` char(50) DEFAULT NULL,
  `lineEdit_single_price_20` char(50) DEFAULT NULL,
  `lineEdit_single_price_21` char(50) DEFAULT NULL,
  `lineEdit_single_price_22` char(50) DEFAULT NULL,
  `lineEdit_single_price_23` char(50) DEFAULT NULL,
  `lineEdit_single_price_24` char(50) DEFAULT NULL,
  `lineEdit_single_price_25` char(50) DEFAULT NULL,
  `lineEdit_single_price_26` char(50) DEFAULT NULL,
  `lineEdit_single_price_27` char(50) DEFAULT NULL,
  `lineEdit_single_price_28` char(50) DEFAULT NULL,
  `lineEdit_single_price_29` char(50) DEFAULT NULL,
  `lineEdit_single_price_30` char(50) DEFAULT NULL,
  `lineEdit_tmpprice` char(50) DEFAULT NULL,
  `lineEdit_tax` char(50) DEFAULT NULL,
  `lineEdit_final_price` char(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 傾印資料表的資料 `save_price_data`
--

INSERT INTO `save_price_data` (`worknum`, `lineEdit_CBM_1`, `lineEdit_CBM_2`, `lineEdit_CBM_3`, `lineEdit_CBM_4`, `lineEdit_CBM_5`, `lineEdit_CBM_6`, `lineEdit_CBM_7`, `lineEdit_CBM_8`, `lineEdit_CBM_9`, `lineEdit_CBM_10`, `lineEdit_CBM_11`, `lineEdit_CBM_12`, `lineEdit_CBM_13`, `lineEdit_CBM_14`, `lineEdit_CBM_15`, `lineEdit_CBMprice_1`, `lineEdit_CBMprice_2`, `lineEdit_CBMprice_3`, `lineEdit_CBMprice_4`, `lineEdit_CBMprice_5`, `lineEdit_CBMprice_6`, `lineEdit_CBMprice_7`, `lineEdit_CBMprice_8`, `lineEdit_CBMprice_9`, `lineEdit_CBMprice_10`, `lineEdit_CBMprice_11`, `lineEdit_CBMprice_12`, `lineEdit_CBMprice_13`, `lineEdit_CBMprice_14`, `lineEdit_CBMprice_15`, `lineEdit_single_price_1`, `lineEdit_single_price_2`, `lineEdit_single_price_3`, `lineEdit_single_price_4`, `lineEdit_single_price_5`, `lineEdit_single_price_6`, `lineEdit_single_price_7`, `lineEdit_single_price_8`, `lineEdit_single_price_9`, `lineEdit_single_price_10`, `lineEdit_single_price_11`, `lineEdit_single_price_12`, `lineEdit_single_price_13`, `lineEdit_single_price_14`, `lineEdit_single_price_15`, `lineEdit_single_price_16`, `lineEdit_single_price_17`, `lineEdit_single_price_18`, `lineEdit_single_price_19`, `lineEdit_single_price_20`, `lineEdit_single_price_21`, `lineEdit_single_price_22`, `lineEdit_single_price_23`, `lineEdit_single_price_24`, `lineEdit_single_price_25`, `lineEdit_single_price_26`, `lineEdit_single_price_27`, `lineEdit_single_price_28`, `lineEdit_single_price_29`, `lineEdit_single_price_30`, `lineEdit_tmpprice`, `lineEdit_tax`, `lineEdit_final_price`) VALUES
('22-05-001', '3', '2', '1', '', '', '', '', '', '', '', '', '', '', '', '', '50', '50', '50', '', '', '', '', '', '', '', '', '', '', '', '', '6300', '800', '1300', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
('22-05-002', '2', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '100', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '400', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '400', '20', '420'),
('22-05-003', '20', '1', '', '', '', '', '', '', '', '', '', '', '', '', '', '50', '40', '', '', '', '', '', '', '', '', '', '', '', '', '', '3000', '120', '', '', '', '', '', '', '', '', '', '', '', '', '', '1800', '', '1000', '', '', '', '', '', '', '', '', '', '', '', '', '5920', '296', '6216');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `save_basic_data`
--
ALTER TABLE `save_basic_data`
  ADD PRIMARY KEY (`worknum`);

--
-- 資料表索引 `save_central_data`
--
ALTER TABLE `save_central_data`
  ADD PRIMARY KEY (`worknum`);

--
-- 資料表索引 `save_price_data`
--
ALTER TABLE `save_price_data`
  ADD PRIMARY KEY (`worknum`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
