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


-- LNK_TGT

	INSERT INTO "DEMO_DV_FL"."LNK_PREDICTIONS_POSTZONES"(
		 "LNK_PREDICTIONS_POSTZONES_HKEY"
		,"LOAD_DATE"
		,"LOAD_CYCLE_ID"
		,"POSTZONES_HKEY"
		,"PREDICTIONS_HKEY"
	)
	SELECT
		  "STG_SRC"."LNK_PREDICTIONS_POSTZONES_HKEY" AS "LNK_PREDICTIONS_POSTZONES_HKEY"
		, "STG_SRC"."LOAD_DATE" AS "LOAD_DATE"
		, "STG_SRC"."LOAD_CYCLE_ID" AS "LOAD_CYCLE_ID"
		, "STG_SRC"."POSTZONES_HKEY" AS "POSTZONES_HKEY"
		, "STG_SRC"."PREDICTIONS_HKEY" AS "PREDICTIONS_HKEY"
	FROM "PRED_STG"."PREDICTIONS" "STG_SRC"
	LEFT OUTER JOIN "DEMO_DV_FL"."LNK_PREDICTIONS_POSTZONES" "LNK_SRC" ON  "STG_SRC"."LNK_PREDICTIONS_POSTZONES_HKEY" = "LNK_SRC"."LNK_PREDICTIONS_POSTZONES_HKEY"
	WHERE  "LNK_SRC"."LNK_PREDICTIONS_POSTZONES_HKEY" IS NULL AND "STG_SRC"."JRN_FLAG" != 'D'
	;



 
 
