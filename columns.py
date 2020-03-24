class Columns:
    enq = ['bibliotheek_bezocht', 'boek_gelezen', 'museum_bezocht', 'park_bezocht',
           'restaurant_of_cafe_bezocht', 'televisie_gekeken',
           'voorstelling_bezocht', 'sport_beoefend']
    opp = ['opp_sportterreinen', 'opp_gebruiksgroen_en_pleinen', 'opp_speelterreinen']
    plaatsen = ['plaatsen_buurtparkings','plaatsen_fietsenstallingen','plaatsen_velo_stations']
    kot = ['kotdichtheid']
    so = ['al_so_binnen_a', 'al_so_buiten_a']
    basis = ['al_basis_binnen_a', 'al_basis_buiten_a']
    stroom = ['al_a_stroom', 'al_b_stroom']
    vertraging = ['al_so_geen_vertraging', 'al_so_vertraging', 'al_so_meer_vertraging']
    secundair = ['al_aso', 'al_bso', 'al_kso', 'al_tso', 'al_deel_bso','al_buso']
    dichtheid = ['dichtheid']
    belastingplichtigen = ['belastingplichtigen']
    belasting = ['gemiddeld_netto_belastbaar_inkomen_per_persoon', 'opbrengst_aanvullende_personenbelasting_per_belast']
    werk = ['aantal_loontrekkenden', 'aantal_werkzoekende', 'aantal_zelfstandigen', 'inactieven']
    total_columns = ['aantal_loontrekkenden', 'aantal_werkzoekende', 'aantal_zelfstandigen',
               'inactieven', 'belastingplichtigen',
               'gemiddeld_netto_belastbaar_inkomen_per_persoon',
               'opbrengst_aanvullende_personenbelasting_per_belast',
               'dichtheid',
               'bibliotheek_bezocht', 'boek_gelezen', 'museum_bezocht', 'park_bezocht', 'restaurant_of_cafe_bezocht',
               'televisie_gekeken',
               'voorstelling_bezocht', 'sport_beoefend', 'al_aso', 'al_bso', 'al_kso', 'al_tso', 'al_deel_bso',
               'al_basis_binnen_a',
               'al_basis_buiten_a', 'al_buso', 'al_so_geen_vertraging', 'al_so_vertraging', 'al_so_meer_vertraging',
               'al_a_stroom',
               'al_b_stroom', 'al_so_binnen_a', 'al_so_buiten_a', 'aantal_koten', 'kotdichtheid',
               'plaatsen_buurtparkings', 'buurtparkings',
               'fietsenstallingen', 'plaatsen_fietsenstallingen', 'sportterreinen', 'speelterreinen',
               'opp_sportterreinen', 'opp_gebruiksgroen_en_pleinen',
               'opp_speelterreinen', 'plaatsen_velo_stations', 'velo_stations']
    input_columns = ['postcode', 'aantal_loontrekkenden', 'aantal_werkzoekende',
                       'aantal_zelfstandigen', 'inactieven', 'belastingplichtigen',
                       'gemiddeld_netto_belastbaar_inkomen_per_persoon',
                       'opbrengst_aanvullende_personenbelasting_per_belast',
                       'dichtheid', 'bibliotheek_bezocht', 'boek_gelezen', 'museum_bezocht',
                       'park_bezocht', 'restaurant_of_cafe_bezocht', 'televisie_gekeken',
                       'voorstelling_bezocht', 'sport_beoefend', 'al_aso', 'al_bso', 'al_kso',
                       'al_tso', 'al_deel_bso', 'al_basis_binnen_a', 'al_basis_buiten_a',
                       'al_buso', 'al_so_geen_vertraging', 'al_so_vertraging',
                       'al_so_meer_vertraging', 'al_a_stroom', 'al_b_stroom', 'al_so_binnen_a',
                       'al_so_buiten_a', 'kotdichtheid', 'plaatsen_buurtparkings',
                       'plaatsen_fietsenstallingen', 'opp_sportterreinen',
                       'opp_gebruiksgroen_en_pleinen', 'opp_speelterreinen',
                       'plaatsen_velo_stations']
    min_max_columns = ['aantal_loontrekkenden', 'aantal_werkzoekende',
                       'aantal_zelfstandigen', 'inactieven', 'belastingplichtigen',
                       'gemiddeld_netto_belastbaar_inkomen_per_persoon',
                       'opbrengst_aanvullende_personenbelasting_per_belast',
                       'dichtheid', 'bibliotheek_bezocht', 'boek_gelezen', 'museum_bezocht',
                       'park_bezocht', 'restaurant_of_cafe_bezocht', 'televisie_gekeken',
                       'voorstelling_bezocht', 'sport_beoefend', 'al_aso', 'al_bso', 'al_kso',
                       'al_tso', 'al_deel_bso', 'al_basis_binnen_a', 'al_basis_buiten_a',
                       'al_buso', 'al_so_geen_vertraging', 'al_so_vertraging',
                       'al_so_meer_vertraging', 'al_a_stroom', 'al_b_stroom', 'al_so_binnen_a',
                       'al_so_buiten_a', 'kotdichtheid', 'plaatsen_buurtparkings',
                       'plaatsen_fietsenstallingen', 'opp_sportterreinen',
                       'opp_gebruiksgroen_en_pleinen', 'opp_speelterreinen',
                       'plaatsen_velo_stations']

    min_max_columns_input = ["werk-slider-0",
                             "werk-slider-1",
                             "werk-slider-2",
                             "werk-slider-3",
                             "belast-slider-0",
                             "belast-input-0",
                             "belast-input-1",
                             "dichtheid-input-0",
                             "enq-slider-0",
                             "enq-slider-1",
                             "enq-slider-2",
                             "enq-slider-3",
                             "enq-slider-4",
                             "enq-slider-5",
                             "enq-slider-6",
                             "enq-slider-7",
                             "secundair-slider-0",
                             "secundair-slider-1",
                             "secundair-slider-2",
                             "secundair-slider-3",
                             "secundair-slider-4",
                             "basis-slider-0",
                             "basis-slider-1",
                             "secundair-slider-5",
                             "vertraging-slider-0",
                             "vertraging-slider-1",
                             "vertraging-slider-2",
                             "stroom-slider-0",
                             "stroom-slider-1",
                             "so-slider-0",
                             "so-slider-1",
                             "kotdichtheid-input-0",
                             "plaatsen-input-0",
                             "plaatsen-input-1",
                             "opp-slider-0",
                             "opp-slider-1",
                             "opp-slider-2",
                             "plaatsen-input-2"]