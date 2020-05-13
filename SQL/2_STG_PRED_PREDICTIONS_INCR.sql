/*
    ___  ___  ______  |  
   / _ \/ _ \|  ____| |  agile    
  / / \ \/ \ \ |__    |  automation
 / /  /\ \  \ \ __|   |  factory   
/_/  /_/\_\  \_\      | 

Vaultspeed version: 4.1.14.0, generation date: 2020/05/12 12:48:20
DV_NAME: DEMO_ANTWERP_CITY_DATA_VAULT - Release: 2.2 predictions schema(2.2) - Comment: Predictions schema - Release date: 2020/05/12 12:44:25, 
BV release: init(1) - Comment: initial release - Release date: 2020/05/12 10:45:49, 
SRC_NAME: PRED - Release: PRED(2) - Comment: Update schema parameters - Release date: 2020/05/12 12:30:07
 */


-- STG_TGT

	TRUNCATE TABLE "PRED_STG"."PREDICTIONS";

	INSERT INTO "PRED_STG"."PREDICTIONS"(
		 "PREDICTIONS_HKEY"
		,"POSTZONES_HKEY"
		,"LNK_PREDICTIONS_POSTZONES_HKEY"
		,"LOAD_DATE"
		,"LOAD_CYCLE_ID"
		,"JRN_FLAG"
		,"RECORD_TYPE"
		,"DATUM"
		,"TIJD"
		,"POSTCODE"
		,"DATUM_BK"
		,"TIJD_BK"
		,"POSTCODE_FK_POSTCODE_BK"
		,"WERKENDEN"
		,"BELASTINGSPLICHTIGEN"
		,"GEMIDDELD_NETTO_BELASTBAAR_INKOMEN_PER_PERSOON"
		,"DICHTHEID"
		,"BIBLIOTHEEK_BEZOCHT"
		,"BOEK_GELEZEN"
		,"PARK_BEZOCHT"
		,"RESTAURANT_OF_CAFE_BEZOCHT"
		,"TELEVISIE_GEKEKEN"
		,"VOORSTELLING_BEZOCHT"
		,"SPORT_BEOEFEND"
		,"THEORETISCH_GESCHOOLDEN"
		,"AL_SO_GEEN_VERTRAGING"
		,"SCHOOL_BINNEN_ANTWERPEN"
		,"PLAATSEN_BUURTPARKINGS"
		,"PLAATSEN_FIETSENSTALLINGEN"
		,"PLAATSEN_VELO_STATIONS"
		,"OPP_SPORTTERREINEN"
		,"OPP_GEBRUIKSGROEN_EN_PLEINEN"
		,"OPP_SPEELTERREINEN"
		,"FIETS_PERCENTAGE"
	)
	SELECT
		 UPPER(MD5_HEX( "EXT_SRC"."DATUM_BK" || '#' ||  "EXT_SRC"."TIJD_BK" || '#')) AS "PREDICTIONS_HKEY"
		,UPPER(MD5_HEX( "EXT_SRC"."POSTCODE_FK_POSTCODE_BK" || '#')) AS "POSTZONES_HKEY"
		,UPPER(MD5_HEX( "EXT_SRC"."DATUM_BK" || '#' ||  "EXT_SRC"."TIJD_BK" || '#' ||
			"EXT_SRC"."POSTCODE_FK_POSTCODE_BK" || '#')) AS "LNK_PREDICTIONS_POSTZONES_HKEY"
		, "EXT_SRC"."LOAD_DATE" AS "LOAD_DATE"
		, "EXT_SRC"."LOAD_CYCLE_ID" AS "LOAD_CYCLE_ID"
		, "EXT_SRC"."JRN_FLAG" AS "JRN_FLAG"
		, "EXT_SRC"."RECORD_TYPE" AS "RECORD_TYPE"
		, "EXT_SRC"."DATUM" AS "DATUM"
		, "EXT_SRC"."TIJD" AS "TIJD"
		, "EXT_SRC"."POSTCODE" AS "POSTCODE"
		, "EXT_SRC"."DATUM_BK" AS "DATUM_BK"
		, "EXT_SRC"."TIJD_BK" AS "TIJD_BK"
		, "EXT_SRC"."POSTCODE_FK_POSTCODE_BK" AS "POSTCODE_FK_POSTCODE_BK"
		, "EXT_SRC"."WERKENDEN" AS "WERKENDEN"
		, "EXT_SRC"."BELASTINGSPLICHTIGEN" AS "BELASTINGSPLICHTIGEN"
		, "EXT_SRC"."GEMIDDELD_NETTO_BELASTBAAR_INKOMEN_PER_PERSOON" AS "GEMIDDELD_NETTO_BELASTBAAR_INKOMEN_PER_PERSOON"
		, "EXT_SRC"."DICHTHEID" AS "DICHTHEID"
		, "EXT_SRC"."BIBLIOTHEEK_BEZOCHT" AS "BIBLIOTHEEK_BEZOCHT"
		, "EXT_SRC"."BOEK_GELEZEN" AS "BOEK_GELEZEN"
		, "EXT_SRC"."PARK_BEZOCHT" AS "PARK_BEZOCHT"
		, "EXT_SRC"."RESTAURANT_OF_CAFE_BEZOCHT" AS "RESTAURANT_OF_CAFE_BEZOCHT"
		, "EXT_SRC"."TELEVISIE_GEKEKEN" AS "TELEVISIE_GEKEKEN"
		, "EXT_SRC"."VOORSTELLING_BEZOCHT" AS "VOORSTELLING_BEZOCHT"
		, "EXT_SRC"."SPORT_BEOEFEND" AS "SPORT_BEOEFEND"
		, "EXT_SRC"."THEORETISCH_GESCHOOLDEN" AS "THEORETISCH_GESCHOOLDEN"
		, "EXT_SRC"."AL_SO_GEEN_VERTRAGING" AS "AL_SO_GEEN_VERTRAGING"
		, "EXT_SRC"."SCHOOL_BINNEN_ANTWERPEN" AS "SCHOOL_BINNEN_ANTWERPEN"
		, "EXT_SRC"."PLAATSEN_BUURTPARKINGS" AS "PLAATSEN_BUURTPARKINGS"
		, "EXT_SRC"."PLAATSEN_FIETSENSTALLINGEN" AS "PLAATSEN_FIETSENSTALLINGEN"
		, "EXT_SRC"."PLAATSEN_VELO_STATIONS" AS "PLAATSEN_VELO_STATIONS"
		, "EXT_SRC"."OPP_SPORTTERREINEN" AS "OPP_SPORTTERREINEN"
		, "EXT_SRC"."OPP_GEBRUIKSGROEN_EN_PLEINEN" AS "OPP_GEBRUIKSGROEN_EN_PLEINEN"
		, "EXT_SRC"."OPP_SPEELTERREINEN" AS "OPP_SPEELTERREINEN"
		, "EXT_SRC"."FIETS_PERCENTAGE" AS "FIETS_PERCENTAGE"
	FROM "PRED_EXT"."PREDICTIONS" "EXT_SRC"
	INNER JOIN "PRED_MTD"."MTD_EXCEPTION_RECORDS" "MEX_SRC" ON  "MEX_SRC"."RECORD_TYPE" = 'U'
	;



 
 