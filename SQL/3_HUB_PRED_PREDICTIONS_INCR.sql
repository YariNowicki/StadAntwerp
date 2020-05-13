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


-- HUB_TGT

	INSERT INTO "DEMO_DV_FL"."HUB_PREDICTIONS"(
		 "PREDICTIONS_HKEY"
		,"LOAD_DATE"
		,"LOAD_CYCLE_ID"
		,"DATUM_BK"
		,"TIJD_BK"
	)
	SELECT
		  "STG_SRC"."PREDICTIONS_HKEY" AS "PREDICTIONS_HKEY"
		, "STG_SRC"."LOAD_DATE" AS "LOAD_DATE"
		, "STG_SRC"."LOAD_CYCLE_ID" AS "LOAD_CYCLE_ID"
		, "STG_SRC"."DATUM_BK" AS "DATUM_BK"
		, "STG_SRC"."TIJD_BK" AS "TIJD_BK"
	FROM "PRED_STG"."PREDICTIONS" "STG_SRC"
	LEFT OUTER JOIN "DEMO_DV_FL"."HUB_PREDICTIONS" "HUB_SRC" ON  "STG_SRC"."PREDICTIONS_HKEY" = "HUB_SRC"."PREDICTIONS_HKEY"
	WHERE  "STG_SRC"."RECORD_TYPE" = 'S' AND "STG_SRC"."JRN_FLAG" != 'D' AND "HUB_SRC"."PREDICTIONS_HKEY" is NULL
	;



 
 
