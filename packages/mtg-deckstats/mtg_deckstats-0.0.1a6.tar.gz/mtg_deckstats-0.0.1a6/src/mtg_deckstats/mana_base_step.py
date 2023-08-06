#!/usr/bin/env python
# -*- coding: utf-8 -*-


# def mana_base(deck):

#     T1_LANDS = [
#         'Badlands', 'Bayou', 'Plateau', 'Savannah', 'Scrubland', 'Taiga',
#         'Tropical Island', 'Tundra', 'Underground Sea', 'Volcanic Island',
#     ]
#     T1_LANDS_SCORE = [0, 0, 1, 3, 6, 10]

#     T2_LANDS = [
#         'Arid Mesa', 'Bloodstained Mire', 'Flooded Strand', 'Marsh Flats',
#         'Misty Rainforest', 'Polluted Delta', 'Scalding Tarn',
#         'Verdant Catacombs', 'Windswept Heath', 'Wooded Foothills',
#     ]
#     T2_LANDS_SCORE = [0, 4, 7, 9, 10, 10]

#     T3_LANDS = [
#         'Blood Crypt', 'Breeding Pool', 'Godless Shrine',
#         'Hallowed Fountain', 'Overgrown Tomb', 'Sacred Foundry',
#         'Steam Vents', 'Stomping Ground', 'Temple Garden', 'Watery Grave',
#     ]
#     T3_LANDS_SCORE = [0, 0, 1, 3, 6, 10]

#     cards = deck.get('cards', [])
#     color_identities = (set(card.color_identity) for card in cards)
#     color_identity = reduce(lambda x,y:x|y, color_identities)

#     lands = [card for card in cards if 'Land' in card.type_line]
#     number_of_lands = count_cards(lands)

#     utility_lands = [
#         land for land in lands
#         if not(set(land.produced_mana) & color_identity)
#     ]
#     number_of_utility_lands = count_cards(utility_lands)

#     t1_target = T1_LANDS_SCORE[len(color_identity)]
#     t1_lands = [land for land in lands if land.name in T1_LANDS]
#     t1_score = count_cards(t1_lands) / t1_target if t1_target > 0 else 1.0

#     t2_target = T2_LANDS_SCORE[len(color_identity)]
#     t2_lands = [land for land in lands if land.name in T2_LANDS]
#     t2_score = count_cards(t2_lands) / t2_target if t2_target > 0 else 1.0

#     t3_target = T3_LANDS_SCORE[len(color_identity)]
#     t3_lands = [land for land in lands if land.name in T3_LANDS]
#     t3_score = count_cards(t3_lands) / t3_target if t3_target > 0 else 1.0

#     mana_base_power = t1_score * t2_score * t3_score

#     return {
#         'mana_base::color_identity': color_identity,

#         'mana_base::lands#': number_of_lands,
#         'mana_base::lands': lands,

#         'mana_base::utility_lands#': number_of_utility_lands,
#         'mana_base::utility_lands': utility_lands,

#         'mana_base::tier1_lands': t1_lands,
#         'mana_base::tier1_lands_score':
#             f'{count_cards(t1_lands)}/{T1_LANDS_SCORE[len(color_identity)]}',
#         'mana_base::tier1_lands_score#': t1_score,

#         'mana_base::tier2_lands': t2_lands,
#         'mana_base::tier2_lands_score':
#             f'{count_cards(t2_lands)}/{T2_LANDS_SCORE[len(color_identity)]}',
#         'mana_base::tier2_lands_score#': t2_score,

#         'mana_base::tier3_lands': t3_lands,
#         'mana_base::tier3_lands_score':
#             f'{count_cards(t3_lands)}/{T3_LANDS_SCORE[len(color_identity)]}',
#         'mana_base::tier3_lands_score#': t3_score,

#         'mana_base::power': mana_base_power,
#     }
