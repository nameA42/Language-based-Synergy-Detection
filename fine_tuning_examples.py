from utility import TextUtil
from sts_prompts import SYNERGY_KEYWORD, SYNERGY_KEYWORD_CAPITALIZED, SYNERGY_KEYWORD_PLURAL, SYNERGY_KEYWORD_VERB

examples = [
    {
        "Question": TextUtil.dedent(f"""Let's say we have:
        Cards:
        Card 5 (Power Type) - Cost 1: "Whenever you draw a Status card, draw 1 card."
        Card 6 (Attack Type) - Cost 1: "Deal 3 damage to a random enemy 3 times."
        Card 7 (Power Type) - Cost 0: "At the start of your turn, lose 1 HP and draw 1 card."
        Card 8 (Attack Type) - Cost 0: "Can only be played if every card in your hand is an Attack. Deal 14 damage."
        Card 9 (Attack Type) - Cost 2: "Exhaust all cards in your hand. Deal 7 damage for each Exhausted card. Exhaust."      
        Card 10 (Skill Type) - Cost 1: "This turn, your next Attack is played twice."
        Card 11 (Skill Type) - Cost 1: "Add 2 Wounds to your hand. Gain 15 Block."
        Cases:
        1. What is the {SYNERGY_KEYWORD} effect of playing card 5, then card 9?
        2. What is the {SYNERGY_KEYWORD} effect of playing card 5, then card 10?
        3. What is the {SYNERGY_KEYWORD} effect of playing card 5, then card 8?
        4. What is the {SYNERGY_KEYWORD} effect of playing card 5, then card 11?
        5. What is the {SYNERGY_KEYWORD} effect of playing card 6, then card 9?
        6. What is the {SYNERGY_KEYWORD} effect of playing card 6, then card 10?
        7. What is the {SYNERGY_KEYWORD} effect of playing card 6, then card 8?
        8. What is the {SYNERGY_KEYWORD} effect of playing card 6, then card 11?
        9. What is the {SYNERGY_KEYWORD} effect of playing card 7, then card 9?
        10. What is the {SYNERGY_KEYWORD} effect of playing card 7, then card 10?
        11. What is the {SYNERGY_KEYWORD} effect of playing card 7, then card 8?
        12. What is the {SYNERGY_KEYWORD} effect of playing card 7, then card 11?
        13. What is the {SYNERGY_KEYWORD} effect of playing card 8, then card 9?
        14. What is the {SYNERGY_KEYWORD} effect of playing card 8, then card 10?
        15. What is the {SYNERGY_KEYWORD} effect of playing card 8, then another one of card 8 again?
        16. What is the {SYNERGY_KEYWORD} effect of playing card 8, then card 11?"""),
        "Answer": TextUtil.dedent(
            f"""# Case 1
            ### Card Descriptions:
            - **Card 5:**
            - Type: Power
            - Cost: 1
            - Whenever you draw a Status card, draw 1 card.

            - **Card 9:**
            - Type: Attack
            - Cost: 2
            - Exhaust all cards in your hand. Deal 7 damage for each Exhausted card. Exhaust.

            ### Order of Events
            - **Playing Card 5 First:**
            - This card sets up a mechanism that allows you to draw additional cards when Status cards are drawn later.

            - **Playing Card 9 Next:**
            - You exhaust all cards in your hand. Card 5 would still be active.
            - You deal damage based on the number of cards you just exhausted. If you have drawn additional cards via Card 5 before playing Card 9, those will also be exhausted and counted towards the damage calculation.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - Card 5 can result in drawing additional cards. Having more cards in your hand when Card 9 is played enhances its effect.
            - Card 9 exhasts all the cards in your hand, including any Status cards. The means that there will be fewer Status cards in your deck, reducing the continued effectiveness of Card 5 on later turns, because Card 5 effect is permanent.

            ### Conclusion:
            While this {SYNERGY_KEYWORD} has both a negative and positive effect, the positive effect is immediate which makes it more valuable.

            Final score:
            1
            ---NEXT---
            # Case 2
            ### Card Descriptions:
            - **Card 5:**
            - Type: Power
            - Cost: 1
            - Whenever you draw a Status card, draw 1 card.

            - **Card 10:**
            - Type: Skill
            - Cost: 1
            - This turn, your next Attack is played twice.

            ### Order of Events
            - **Playing Card 5 First:**
            - You gain the ability to draw an additional card if you draw Status cards from this point on.

            - **Playing Card 10 Next:**
            - The next Attack card you play this turn will be played twice. If you have drawn additional cards via Card 5 before playing Card 10, there may be more Attack cards in your hand that you could play and have it be played twice because of Card 10.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - The effectiveness of Card 10 is very sensitive to what Attack card is played after Card 10 that turn. Having Card 5 in play potentially leads to more draws, giving you more options for cards to play.

            ### Conclusion:
            There is small positive indirect {SYNERGY_KEYWORD} between the two cards, since playing Card 5 can result in having more options for what Attack is played twice through Card 10's effect.

            Final score:
            1
            ---NEXT---
            # Case 3
            ### Card Descriptions:
            - **Card 5:**
            - Type: Power
            - Cost: 1
            - Whenever you draw a Status card, draw 1 card.

            - **Card 8:**
            - Type: Attack
            - Cost: 0
            - Can only be played if every card in your hand is an Attack. Deal 14 damage.

            ### Order of Events
            - **Playing Card 5 First:**
            - Sets an ongoing effect to draw additional cards if Status cards are drawn.

            - **Playing Card 8 Next:**
            - Card 8's conditions require that all cards in your hand must be Attacks. Since Card 5 is in play, it makes drawing a Status card more obstructive to Card 8's requirement, since any Status card drawn will trigger Card 5's effect, drawing an additional card which can be a non-Attack card.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - Playing Card 5 first can create a scenario where Card 8 cannot be played.
            - As such, there’s a disadvantage from the combination, since the inclusion of Card 5 may block the play of Card 8.

            ### Conclusion:
            The sequence produces a negative effect, as Card 5 inadvertently prevents Card 8 from being played.

            Final score:
            -1
            ---NEXT---
            # Case 4
            ### Card Descriptions:
            - **Card 5:**
            - Type: Power
            - Cost: 1
            - Whenever you draw a Status card, draw 1 card.

            - **Card 11:**
            - Type: Skill
            - Cost: 1
            - Add 2 Wounds to your hand. Gain 15 Block.

            ### Order of Events
            - **Playing Card 5 First:**
            - You gain the effect of drawing an additional card when any Status card is drawn.

            - **Playing Card 11 Next:**
            - You add 2 Wounds to your hand, which are Status cards, and gain 15 Block.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - By playing Card 11, you add Status cards to your hand that will end up in your deck and can be drawn later.
            - Since Card 5 has a permanent effect, whenever one of these Wound cards are drawn, you will draw  an additional card which would not have happened without Card 5 or 11 being played.

            ### Conclusion:
            Playing these cards leads to a positive {SYNERGY_KEYWORD}, as drawing Wounds allows you to trigger Card 5’s ability to draw more cards.

            Final score:
            1
            ---NEXT---
            # Case 5
            ### Card Descriptions:
            - **Card 6:**
            - Type: Attack
            - Cost: 1
            - Deal 3 damage to a random enemy 3 times.

            - **Card 9:**
            - Type: Attack
            - Cost: 2
            - Exhaust all cards in your hand. Deal 7 damage for each Exhausted card. Exhaust.

            ### Order of Events
            - **Playing Card 6 First:**
            - You deal 3 damage 3 times applied to a random enemies each time, possibly hitting the same enemy more than once.

            - **Playing Card 9 Next:**
            - You exhaust all the cards in your hand, dealing damage based on how many cards were exhausted.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - When playing Card 9, Card 6 may or may not be in your hand. However, the effect of Card 6 has no unique impact on the effect of Card 9.

            ### Conclusion:
            There is no positive or negative {SYNERGY_KEYWORD} between Card 6 and Card 9.

            Final score:
            0
            ---NEXT---
            # Case 6
            ### Card Descriptions:
            - **Card 6:**
            - Type: Attack
            - Cost: 1
            - Deal 3 damage to a random enemy 3 times.

            - **Card 10:**
            - Type: Skill
            - Cost: 1
            - This turn, your next Attack is played twice.

            ### Order of Events
            - **Playing Card 6 First:**
            - You deal 3 damage 3 times applied to a random enemies each time, possibly hitting the same enemy more than once.

            - **Playing Card 10 Next:**
            - By playing Card 10, the next Attack card you play this turn is played twice. If you play an Attack card this turn, this can enhance your turn but does not apply retroactively.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - Card 10 does not benefit from Card 6 since Card 6 resolves its effects before Card 10 is played.   

            ### Conclusion:
            No positive or negative {SYNERGY_KEYWORD} emerges from this sequence; these card do not interact when played in this order.

            Final score:
            0
            ---NEXT---
            # Case 7
            ### Card Descriptions:
            - **Card 6:**
            - Type: Attack
            - Cost: 1
            - Deal 3 damage to a random enemy 3 times.

            - **Card 8:**
            - Type: Attack
            - Cost: 0
            - Can only be played if every card in your hand is an Attack. Deal 14 damage.

            ### Order of Events
            - **Playing Card 6 First:**
            - You deal 3 damage 3 times applied to a random enemies each time, possibly hitting the same enemy more than once.

            - **Playing Card 8 Next:**
            - Card 8 can be played if all cards in your hand are Attack cards. Playing Card 6 does not impact this condition in any way.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - There is no effect on the ability to play Card 8 from playing Card 6.

            ### Conclusion:
            This sequence results in a no {SYNERGY_KEYWORD} since Card 6 wouldn't disqualify Card 8 from being played.

            Final score:
            0
            ---NEXT---
            # Case 8
            ### Card Descriptions:
            - **Card 6:**
            - Type: Attack
            - Cost: 1
            - Deal 3 damage to a random enemy 3 times.

            - **Card 11:**
            - Type: Skill
            - Cost: 1
            - Add 2 Wounds to your hand. Gain 15 Block.

            ### Order of Events
            - **Playing Card 6 First:**
            - You deal 3 damage 3 times applied to a random enemies each time, possibly hitting the same enemy more than once.

            - **Playing Card 11 Next:**
            - You add Wounds to your hand and gain Block. This is not impacted by Card 6’s output.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - There is no direct {SYNERGY_KEYWORD} between the two cards as played since the damage effect of Card 6 cannot be improved by playing Card 11 afterwards.
            - Playing Card 6 also does not influence the effect of Card 11 in any way.

            ### Conclusion:
            Overall, while Card 6 has its own benefit, it doesn’t create any meaningful {SYNERGY_KEYWORD} or advantage for Card 11. Thus, there is no direct {SYNERGY_KEYWORD} between them.

            Final score:
            0
            ---NEXT---
            # Case 9
            ### Card Descriptions:
            - **Card 7:**
            - Type: Power
            - Cost: 0
            - At the start of your turn, lose 1 HP and draw 1 card.

            - **Card 9:**
            - Type: Attack
            - Cost: 2
            - Exhaust all cards in your hand. Deal 7 damage for each Exhausted card. Exhaust.

            ### Order of Events
            - **Playing Card 7 First:**
            - From your next turn onward, at the start of each turn you will lose 1 HP and draw a card.

            - **Playing Card 9 Next:**
            - You exhaust all cards in your hand and deal damage based on the number of cards exhausted.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - The energy or HP loss is not relevant in terms of any benefits gained from Card 9 directly.
            - However, the additional card drawn can enhance the effect of Card 9 since Card 9's effect is proportional to the number of cards in your hand.

            ### Conclusion:
            Playing these two cards in this order leads to a positive {SYNERGY_KEYWORD} since Card 9's effect is enhanced when there are more cards in your hand.

            Final score:
            1
            ---NEXT---
            # Case 10
            ### Card Descriptions:
            - **Card 7:**
            - Type: Power
            - Cost: 0
            - At the start of your turn, lose 1 HP and draw 1 card.

            - **Card 10:**
            - Type: Skill
            - Cost: 1
            - This turn, your next Attack is played twice.

            ### Order of Events
            - **Playing Card 7 First:**
            - From your next turn onward, at the start of each turn you will lose 1 HP and draw a card.

            - **Playing Card 10 Next:**
            - This card is played to set your next Attack this turn to be played twice for whatever cards exist in hand or drawn (if it's an Attack card).

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - Having Card 7 in play leads to more cards drawn on future turns, but not this turn.
            - If Card 10 is played on a future turn, there will be more cards in your hand, some of which can be Attack cards. Because of this, there can be more options to choose from for Card 10 to affect.

            ### Conclusion:
            There is a positive {SYNERGY_KEYWORD} effect when these cards are played in this particular order since Card 7's effect can result in having more options for what Attack is played twice.

            Final score:
            1
            ---NEXT---
            # Case 11
            ### Card Descriptions:
            - **Card 7:**
            - Type: Power
            - Cost: 0
            - At the start of your turn, lose 1 HP and draw 1 card.

            - **Card 8:**
            - Type: Attack
            - Cost: 0
            - Can only be played if every card in your hand is an Attack. Deal 14 damage.

            ### Order of Events
            - **Playing Card 7 First:**
            - From your next turn onward, at the start of each turn you will lose 1 HP and draw a card.

            - **Playing Card 8 Next:**
            - If drawing more Cards leads to having non-Attack cards, you can potentially be prevented from playing Card 8 since it relies on the condition of not holding any cards not labeled as Attack cards.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - If you hold non-Attack cards, it blocks Card 8. This results in a potential detriment if Card 7 causes you to draw such a card.

            ### Conclusion:
            There is a negative {SYNERGY_KEYWORD} since the ability to play Card 8 hinges on what cards you have in your hand . Playing Card 7 creates the possibility of drawing a non-Attack card—hence creating a negative {SYNERGY_KEYWORD}.

            Final score:
            -1
            ---NEXT---
            # Case 12
            ### Card Descriptions:
            - **Card 7:**
            - Type: Power
            - Cost: 0
            - At the start of your turn, lose 1 HP and draw 1 card.

            - **Card 11:**
            - Type: Skill
            - Cost: 1
            - Add 2 Wounds to your hand. Gain 15 Block.

            ### Order of Events
            - **Playing Card 7 First:**
            - From your next turn onward, at the start of each turn you will lose 1 HP and draw a card.

            - **Playing Card 11 Next:**
            - You add 2 Wounds (Status cards) to your hand and gain 15 Block.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - The negative effect of adding Wounds from Card 11 directly hinders the positive effect of drawing an additional card each turn gained from Card 7, since the drawn cards now can be Wounds.
            - The positive effect of drawing an additional card each turn gained from Card 7 directly counteracts the negative effect of having your deck diluted with Wounds from card 1.

            ### Conclusion:
            Given this {SYNERGY_KEYWORD} has both a positive and negative side and these sides are relatively balanced, we can consider this as having no significant {SYNERGY_KEYWORD}.

            Final score:
            0
            ---NEXT---
            # Case 13
            ### Card Descriptions:
            - **Card 8:**
            - Type: Attack
            - Cost: 0
            - Can only be played if every card in your hand is an Attack. Deal 14 damage.

            - **Card 9:**
            - Type: Attack
            - Cost: 2
            - Exhaust all cards in your hand. Deal 7 damage for each Exhausted card. Exhaust.

            ### Order of Events
            - **Playing Card 8 First:**
            - This card is played, assuming that there are no non-Attack cards in your hand, dealing 14 damage.

            - **Playing Card 9 Next:**
            - When this card is played, all cards in your hand are exhausted and damage proportional to the number of cards exhausted is dealt to an enemy.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - By playing Card 8, you deal 14 damage to an enemy.
            - Card 9 does not gain or lose effectiveness as a result of playing Card 8.

            ### Conclusion:
            Card 8 serves as a solid Attack, following it with Card 9 has no additional positive or negative {SYNERGY_KEYWORD}.

            Final score:
            0
            ---NEXT---
            # Case 14
            ### Card Descriptions:
            - **Card 8:**
            - Type: Attack
            - Cost: 0
            - Can only be played if every card in your hand is an Attack. Deal 14 damage.

            - **Card 10:**
            - Type: Skill
            - Cost: 1
            - This turn, your next Attack is played twice.

            ### Order of Events
            - **Playing Card 8 First:**
            - This card would deal 14 damage since it gets played first.

            - **Playing Card 10 Next:**
            - Playing Card 10 sets you up to play your next Attack this turn twice.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - You have to consider that playing Card 10 after Card 8 doesn’t retroactively allow Card 8 to be played again and benefit.
            - Playing Card 8 does not influence future attacks played with Card 10.

            ### Conclusion:
            As both cards operate independently, the effects do not generate a {SYNERGY_KEYWORD} leading to a specific outcome.

            Final score:
            0
            ---NEXT---
            # Case 15
            ### Card Descriptions:
            - **Card 8:**
            - Type: Attack
            - Cost: 0
            - Can only be played if every card in your hand is an Attack. Deal 14 damage.

            ### Order of Events
            - **Playing Card 8 First:**
            - Assuming the conditions are met, you can play this card, dealing 14 damage.

            - **Playing Card 8 Next:**
            - Assuming the conditions are met again when another one of this card is played, you can deal 14 damage again.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - Given that these cards do not enhance each other's effect or make the requirement for playing Card 8 more or less likely, there is no {SYNERGY_KEYWORD} between the two cards.

            ### Conclusion:
            There is no positive or negative {SYNERGY_KEYWORD} between the two cards.

            Final score:
            0
            ---NEXT---
            # Case 16
            ### Card Descriptions:
            - **Card 8:**
            - Type: Attack
            - Cost: 0
            - Can only be played if every card in your hand is an Attack. Deal 14 damage.

            - **Card 11:**
            - Type: Skill
            - Cost: 1
            - Add 2 Wounds to your hand. Gain 15 Block.

            ### Order of Events
            - **Playing Card 8 First:**
            - Assuming all cards are Attack cards, deal 14 damage.

            - **Playing Card 11 Next:**
            - Add Status cards (Wounds) to your hand which disrupts the potential to play another card from Card 8 if applicable.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - Playing Card 11 after Card 8 would reduce your capability to play Card 8 in the future.
            - However, for the purposes of the {SYNERGY_KEYWORD} between these cards in this order, playing Card 8 would have no effect on playing Card 11, and the future plays of Card 8 are irrelevant.

            ### Conclusion:
            Since Card 11 would not retroactively stop you from playing Card 8, there is no {SYNERGY_KEYWORD}.

            Final score:
            0""")
    },
    {
        "Question": TextUtil.dedent(f"""Let's say we have:
        Cards:
        Card 5 (Skill Type) - Cost 1: "Gain 5 Block. Upgrade a card in your hand for the rest of combat."
        Card 6 (Skill Type) - Cost 1: "Ethereal. Gain 10 Block."
        Card 7 (Skill Type) - Cost 1: "Add 2 Wounds to your hand. Gain 15 Block."
        Card 8 (Power Type) - Cost 3: "Block is not removed at the start of your turn."
        Card 9 (Attack Type) - Cost 1: "Deal damage equal to your current Block."
        Card 10 (Skill Type) - Cost 2: "Double your current Block."
        Card 11 (Power Type) - Cost 1: "At the end of your turn, gain 3 Block."
        Cases:
        1. What is the {SYNERGY_KEYWORD} effect of playing card 5, then card 9?
        2. What is the {SYNERGY_KEYWORD} effect of playing card 5, then card 10?
        3. What is the {SYNERGY_KEYWORD} effect of playing card 5, then card 11?
        4. What is the {SYNERGY_KEYWORD} effect of playing card 5, then card 8?
        5. What is the {SYNERGY_KEYWORD} effect of playing card 6, then card 9?
        6. What is the {SYNERGY_KEYWORD} effect of playing card 6, then card 10?
        7. What is the {SYNERGY_KEYWORD} effect of playing card 6, then card 11?
        8. What is the {SYNERGY_KEYWORD} effect of playing card 6, then card 8?
        9. What is the {SYNERGY_KEYWORD} effect of playing card 7, then card 9?
        10. What is the {SYNERGY_KEYWORD} effect of playing card 7, then card 10?
        11. What is the {SYNERGY_KEYWORD} effect of playing card 7, then card 11?
        12. What is the {SYNERGY_KEYWORD} effect of playing card 7, then card 8?
        13. What is the {SYNERGY_KEYWORD} effect of playing card 8, then card 9?
        14. What is the {SYNERGY_KEYWORD} effect of playing card 8, then card 10?
        15. What is the {SYNERGY_KEYWORD} effect of playing card 8, then card 11?
        16. What is the {SYNERGY_KEYWORD} effect of playing card 8, then another one of card 8 again?"""),
        "Answer": TextUtil.dedent(f"""
            # Case 1
            ### Card Descriptions:
            - **Card 5:** 
            - Type: Skill
            - Cost: 1
            - Gain 5 Block. Upgrade a card in your hand for the rest of combat.

            - **Card 9:** 
            - Type: Attack
            - Cost: 1
            - Deal damage equal to your current Block.

            ### Order of Events
            - **Playing Card 5 First:** 
            - You gain 5 Block.

            - **Playing Card 9 Next:** 
            - Deals damage equal to your current Block (5), resulting in 5 damage.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - The damage from Card 9 is reliant on the Block provided by Card 5. Without Card 5, Card 9 would deal no damage.
            
            ### Conclusion:
            This sequence demonstrates a positive {SYNERGY_KEYWORD}, as Card 5 increases the functionality of Card 9 by enabling it to deal damage.

            Final score:
            1
            ---NEXT---
            # Case 2
            ### Card Descriptions:
            - **Card 5:** 
            - Type: Skill
            - Cost: 1
            - Gain 5 Block. Upgrade a card in your hand for the rest of combat.

            - **Card 10:** 
            - Type: Skill
            - Cost: 2
            - Double your current Block.

            ### Order of Events
            - **Playing Card 5 First:**
            - You gain 5 Block.
            
            - **Playing Card 10 Next:**
            - Doubles the Block from 5 to 10 Block.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - This showcases a very effective {SYNERGY_KEYWORD}. The initial Block from Card 5 enhances the benefit from Card 10 by providing a solid base to double.

            ### Conclusion:
            A strong {SYNERGY_KEYWORD} from the combination is clearly evident in the increased Block value.

            Final score:
            1
            ---NEXT---
            # Case 3
            ### Card Descriptions:
            - **Card 5:** 
            - Type: Skill
            - Cost: 1
            - Gain 5 Block. Upgrade a card in your hand for the rest of combat.

            - **Card 11:** 
            - Type: Power
            - Cost: 1
            - At the end of your turn, gain 3 Block.

            ### Order of Events
            - **Playing Card 5 First:**
            - You gain 5 Block.

            - **Playing Card 11 Next:**
            - At the end of your turn, gain an additional 3 Block, for a total of 8 Block.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - While both cards contribute positively to Block totals, the interaction remains relatively standard and lacks further productive {SYNERGY_KEYWORD} beyond their individual effects.

            ### Conclusion:
            The total Block is increased but does not yield extraordinary outcomes due to lack of deeper interaction between both cards.

            Final score:
            0
            ---NEXT---
            # Case 4
            ### Card Descriptions:
            - **Card 5:** 
            - Type: Skill
            - Cost: 1
            - Gain 5 Block. Upgrade a card in your hand for the rest of combat.

            - **Card 8:** 
            - Type: Power
            - Cost: 3
            - Block is not removed at the start of your turn.

            ### Order of Events
            - **Playing Card 5 First:**
            - You gain 5 Block.

            - **Playing Card 8 Next:**
            - This means your Block will persist into the next turn.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - The ability to carry Over the Block ensures solid defensive capabilities going into future rounds, establishing beneficial resilience.

            ### Conclusion:
            This sequence reflects positive {SYNERGY_KEYWORD} for long-term block buildup.

            Final score:
            1
            ---NEXT---
            # Case 5
            ### Card Descriptions:
            - **Card 6:** 
            - Type: Skill
            - Cost: 1
            - Ethereal. Gain 10 Block.

            - **Card 9:** 
            - Type: Attack
            - Cost: 1
            - Deal damage equal to your current Block.

            ### Order of Events
            - **Playing Card 6 First:**
            - You gain 10 Block.
            
            - **Playing Card 9 Next:**
            - This deals damage equal to the current Block (10), resulting in 10 damage.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - The damage from Card 9 directly corresponds to the Block gained from Card 6, demonstrating clear {SYNERGY_KEYWORD} by maximizing damage output based on accrued Block.

            ### Conclusion:
            This interaction is positive {SYNERGY_KEYWORD} as it utilizes the Block gain to initiate potential damage.

            Final score:
            1
            ---NEXT---
            # Case 6
            ### Card Descriptions:
            - **Card 6:** 
            - Type: Skill
            - Cost: 1
            - Ethereal. Gain 10 Block.

            - **Card 10:** 
            - Type: Skill
            - Cost: 2
            - Double your current Block.

            ### Order of Events
            - **Playing Card 6 First:** 
            - You gain 10 Block.

            - **Playing Card 10 Next:**
            - Doubles that Block to 20.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - This sequence demonstrates excellent {SYNERGY_KEYWORD}, doubling your current Block to amplify defensive capabilities significantly.

            ### Conclusion:
            The strong {SYNERGY_KEYWORD} results in a high degree of effectiveness through maximizing Block application.

            Final score:
            1
            ---NEXT---
            # Case 7
            ### Card Descriptions:
            - **Card 6:** 
            - Type: Skill
            - Cost: 1
            - Ethereal. Gain 10 Block.

            - **Card 11:** 
            - Type: Power
            - Cost: 1
            - At the end of your turn, gain 3 Block.

            ### Order of Events
            - **Playing Card 6 First:**
            - You gain 10 Block.

            - **Playing Card 11 Next:**
            - This adds an extra 3 Block at the end of the turn, resulting in 13 Block.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - Though the total Block is respectable, the effect of Card 11 does not derive additional {SYNERGY_KEYWORD} from Card 6 directly.

            ### Conclusion:
            The combination boosts total Block, but lacks deeper interaction between the plays.

            Final score:
            0
            ---NEXT---
            # Case 8
            ### Card Descriptions:
            - **Card 6:** 
            - Type: Skill
            - Cost: 1
            - Ethereal. Gain 10 Block.

            - **Card 8:** 
            - Type: Power
            - Cost: 3
            - Block is not removed at the start of your turn.

            ### Order of Events
            - **Playing Card 6 First:**
            - You gain 10 Block.

            - **Playing Card 8 Next:**
            - Ensures that Block is retained for the next turn.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - Retaining 10 Block for next turn creates a strategic advantage for future plays, demonstrating a good {SYNERGY_KEYWORD}.

            ### Conclusion:
            This sequence is effective due to the combination of immediate and future Block retention.

            Final score:
            1
            ---NEXT---
            # Case 9
            ### Card Descriptions:
            - **Card 7:** 
            - Type: Skill
            - Cost: 1
            - Add 2 Wounds to your hand. Gain 15 Block.

            - **Card 9:** 
            - Type: Attack
            - Cost: 1
            - Deal damage equal to your current Block.

            ### Order of Events
            - **Playing Card 7 First:**
            - You gain 15 Block and add 2 Wounds to your hand.

            - **Playing Card 9 Next:**
            - Deals damage equal to your current Block (15), resulting in 15 damage.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - The damage is effectively realized due to the Block gained from Card 7. The Wounds added don't contribute to this interaction.

            ### Conclusion:
            This pair has a positive {SYNERGY_KEYWORD} with respect to damage scaling based on Block.

            Final score:
            1
            ---NEXT---
            # Case 10
            ### Card Descriptions:
            - **Card 7:** 
            - Type: Skill
            - Cost: 1
            - Add 2 Wounds to your hand. Gain 15 Block.

            - **Card 10:** 
            - Type: Skill
            - Cost: 2
            - Double your current Block.

            ### Order of Events
            - **Playing Card 7 First:**
            - You gain 15 Block and add 2 Wounds to your hand.

            - **Playing Card 10 Next:**
            - Doubles the Block to 30.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - Doubling the initial Block gained from Card 7 signifies a robust outcome with benefits extracted from both cards effectively.

            ### Conclusion:
            The combination clearly exhibits positive {SYNERGY_KEYWORD} by leveraging Block enhancement.

            Final score:
            1
            ---NEXT---
            # Case 11
            ### Card Descriptions:
            - **Card 7:** 
            - Type: Skill
            - Cost: 1
            - Add 2 Wounds to your hand. Gain 15 Block.

            - **Card 11:** 
            - Type: Power
            - Cost: 1
            - At the end of your turn, gain 3 Block.

            ### Order of Events
            - **Playing Card 7 First:**
            - You gain 15 Block and 2 Wounds.

            - **Playing Card 11 Next:**
            - Provides an extra 3 Block at the turn's end, totaling 18 Block.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - Although the total Block is beneficial, the wounds do not enhance the effects positively.

            ### Conclusion:
            The interaction produces a straightforward Block gain without significant intra-card {SYNERGY_KEYWORD}.

            Final score:
            0
            ---NEXT---
            # Case 12
            ### Card Descriptions:
            - **Card 7:** 
            - Type: Skill
            - Cost: 1
            - Add 2 Wounds to your hand. Gain 15 Block.


            - **Card 8:** 
            - Type: Power
            - Cost: 3
            - Block is not removed at the start of your turn.

            ### Order of Events
            - **Playing Card 7 First:**
            - You gain 15 Block and add 2 Wounds.

            - **Playing Card 8 Next:**
            - Ensures that the 15 Block stays through the next turn.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - This strategic pairing provides strong defensive strategies for future turns, indicating higher efficacy.

            ### Conclusion:
            This sequence demonstrates positive {SYNERGY_KEYWORD} through Block retention in subsequent turns.

            Final score:
            1
            ---NEXT---
            # Case 13
            ### Card Descriptions:
            - **Card 8:** 
            - Type: Power
            - Cost: 3
            - Block is not removed at the start of your turn.

            - **Card 9:** 
            - Type: Attack
            - Cost: 1
            - Deal damage equal to your current Block.

            ### Order of Events
            - **Playing Card 8 First:**
            - Block is retained for the next turn.
            
            - **Playing Card 9 Next:**
            - Deals damage equal to the current Block.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - It showcases good use of Block retention for damage, as any block gained inbetween makes card 9 stronger because of card 8 being played.

            ### Conclusion:
            This results in a positive {SYNERGY_KEYWORD} as the damage can grow a lot.

            Final score:
            1
            ---NEXT---
            # Case 14
            ### Card Descriptions:
            - **Card 8:** 
            - Type: Power
            - Cost: 3
            - Block is not removed at the start of your turn.

            - **Card 10:** 
            - Type: Skill
            - Cost: 2
            - Double your current Block.

            ### Order of Events
            - **Playing Card 8 First:**
            - Retains Block for the next round.

            - **Playing Card 10 Next:**
            - Doubles the Block amount.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - The pairing is extremely effective, ensuring the retained Block is subsequently maximized.

            ### Conclusion:
            This sequence exhibits strong positive {SYNERGY_KEYWORD} through effective interaction between cards.

            Final score:
            1
            ---NEXT---
            # Case 15
            ### Card Descriptions:
            - **Card 8:** 
            - Type: Power
            - Cost: 3
            - Block is not removed at the start of your turn.

            - **Card 11:** 
            - Type: Power
            - Cost: 1
            - At the end of your turn, gain 3 Block.

            ### Order of Events
            - **Playing Card 8 First:**
            - Retains Block into the next turn.

            - **Playing Card 11 Next:**
            - Adds additional 3 Block at the end.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - The effective production of Block results in a steady buildup of block that can be cached in when you take damage.

            ### Conclusion:
            This interaction produces a strong {SYNERGY_KEYWORD} through heightened Block totals.

            Final score:
            1
            ---NEXT---
            # Case 16
            ### Card Descriptions:
            - **Card 8:** 
            - Type: Power
            - Cost: 3
            - Block is not removed at the start of your turn.

            ### Order of Events
            - **Playing Card 8 First:** 
            - You maintain Block from previous plays.

            - **Playing Another Card 8 Next:** 
            - Does nothing since the block is already maintined

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:
            - While card 8 is a good card in its own right, it has no extra effect when played with another card 8.
            
            ### Conclusion:
            The engagement demonstrates no {SYNERGY_KEYWORD} through playing the second card 8 because the effect cannot compound.

            Final score:
            0""")
    },
]

if __name__ == "__main__":
    from llm_connector import OpenAIChat
    from sts_prompts import get_sts_prompts, get_single_card_ask, AskType
    import json
    import time

    system_prompt, prompts, responses, next_card_number = get_sts_prompts(ask_type=AskType.NP_Bundle_Revised)
    chat = OpenAIChat(OpenAIChat.OpenAIModel.GPT_4O_mini, chat_format=False, system_message=system_prompt)
    for prompt, response in zip(prompts, responses):
        chat.inject(prompt, response)
    output_filename = f"finetune_dataset{int(time.time())}"
    with open(f'{output_filename}.jsonl', 'w') as outfile:
        for example in examples:
            example_chat = chat.copy()
            example_chat.inject(example["Question"], example["Answer"])
            json_requset = example_chat.as_fine_tuning_example()
            json.dump(json_requset, outfile)
            outfile.write('\n')
