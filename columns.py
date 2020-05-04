class Columns:
    display = ['postcode', 'jaar', 'fiets_naar_werk_school', 'naam', 'shape_area', 'shape_length']
    enq = ['bibliotheek_bezocht', 'boek_gelezen', 'museum_bezocht', 'park_bezocht',
           'restaurant_of_cafe_bezocht', 'televisie_gekeken',
           'voorstelling_bezocht', 'sport_beoefend']
    opp = ['opp_sportterreinen', 'opp_gebruiksgroen_en_pleinen', 'opp_speelterreinen']
    plaatsen = ['plaatsen_buurtparkings','plaatsen_fietsenstallingen','plaatsen_velo_stations']
    so = ['al_so_binnen_a', 'al_so_buiten_a']
    basis = ['al_basis_binnen_a', 'al_basis_buiten_a']
    stroom = ['al_a_stroom', 'al_b_stroom']
    vertraging = ['al_so_geen_vertraging', 'al_so_vertraging', 'al_so_meer_vertraging']
    secundair = ['theorestisch_geschoolden']
    dichtheid = ['dichtheid']
    belastingplichtigen = ['belastingplichtigen']
    belasting = ['gemiddeld_netto_belastbaar_inkomen_per_persoon', 'opbrengst_aanvullende_personenbelasting_per_belast']
    werk = ['werkenden']
    total_columns = ['postcode',
                    'werkenden',
                    'belastingplichtigen',
                    'gemiddeld_netto_belastbaar_inkomen_per_persoon',
                    'opbrengst_aanvullende_personenbelasting_per_belast',
                    'dichtheid',
                    'bibliotheek_bezocht',
                    'boek_gelezen',
                    'museum_bezocht',
                    'park_bezocht',
                    'restaurant_of_cafe_bezocht',
                    'televisie_gekeken',
                    'voorstelling_bezocht',
                    'sport_beoefend',
                    'regelmatig_de_fiets_naar_werk_school',
                    'theorestisch_geschoolden',
                    'al_basis_binnen_a',
                    'al_so_binnen_a',
                    'al_a_stroom',
                    'al_so_geen_vertraging',
                    'plaatsen_buurtparkings',
                    'plaatsen_fietsenstallingen',
                    'plaatsen_velo_stations',
                    'opp_sportterreinen',
                    'opp_gebruiksgroen_en_pleinen',
                    'opp_speelterreinen']
    input_columns = ['postcode','werkenden','belastingplichtigen',
                       'gemiddeld_netto_belastbaar_inkomen_per_persoon',
                       'opbrengst_aanvullende_personenbelasting_per_belast',
                       'dichtheid', 'bibliotheek_bezocht', 'boek_gelezen', 'museum_bezocht',
                       'park_bezocht', 'restaurant_of_cafe_bezocht', 'televisie_gekeken',
                       'voorstelling_bezocht', 'sport_beoefend', 'theorestisch_geschoolden', 'al_basis_binnen_a','al_so_binnen_a',
                       'al_a_stroom','al_so_geen_vertraging','plaatsen_buurtparkings',
                       'plaatsen_fietsenstallingen', 'plaatsen_velo_stations','opp_sportterreinen',
                       'opp_gebruiksgroen_en_pleinen', 'opp_speelterreinen']
    min_max_columns_input = ["choose-postcode",
                             "werk-slider-0",
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
                             "basis-slider-0",
                             "so-slider-0",
                             "stroom-slider-0",
                             "vertraging-slider-0",
                             "plaatsen-input-0",
                             "plaatsen-input-1",
                             "plaatsen-input-2",
                             "opp-slider-0",
                             "opp-slider-1",
                             "opp-slider-2"]