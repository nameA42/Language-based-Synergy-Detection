from utility import TextUtil
from enum import Enum

dedent = TextUtil.dedent

# SYNERGY_KEYWORD = "synergy"
# SYNERGY_KEYWORD_PLURAL = "synergies"
# SYNERGY_KEYWORD_CAPITALIZED = "Synergy"
# SYNERGY_KEYWORD_VERB = "synergize"

SYNERGY_KEYWORD = "combo"
SYNERGY_KEYWORD_PLURAL = "combos"
SYNERGY_KEYWORD_CAPITALIZED = "Combo"
SYNERGY_KEYWORD_VERB = "combo"

def get_sts_definitions():
    prompts = []
    responses = []
    prompts.append(dedent(
        """You are studying a new card game. In this game, the player have a deck of cards.
        The game is single player and is played in a number of turns. The game is played against one or more enemies.
        The player has some amount of HP. If player's HP reaches zero, the player loses.
        Each of the enemies also have some amount of HP. Any enemy with zero HP dies and would not affect the game anymore. If all the enemies die, the player wins the game.
        At the start of every turn, each enemy also shows an intention. This intention describes what action that enemy performs after the player ends his turn. Example enemy actions are "deal 5 damage" or "gain 5 block".
        There are four card piles in the game: draw pile, discard pile, exhaust pile, and your hand. Initially, the player starts the game by shuffling the deck of cards into the draw pile. The other piles are empty.
        Every turn, these actions are performed in this exact order:
        1. The player gains some amount of energy. Most of the time this amount is 3, but some items or cards in the game can change this amount.
        2. The player draws some number of cards from the draw pile into his hand. Most of the time this number is 5, but some items or cards in the game can change this amount.
        * If there are not enough cards in the draw pile, all the cards in the discard pile shuffle back into the draw pile. Then the remaining cards are drawn.
        3. The player plays as many cards as he wants, as long as he has enough energy to play them. Then he ends his turn.
        4. When the player ends his turn, all the remaining cards in his hand are moved to the discard pile. New cards will be drawn next turn.
        5. When the player ends his turn, the enemies perform their actions that was shown as their intention at the start of the turn.
        Any questoins so far?\n"""))
    responses.append(dedent(
        '''No questions so far! The rules of the card game are clear. The mechanics regarding the turn structure, energy management, card drawing, and enemy actions are all well understood.\n'''
    ))
    prompts.append(dedent(
        '''OK, I want to explain some terms from the game before asking questions.
        Card Type: Either Attack, Skill or Power. Power cards are played and then removed from that battle, but Attack or Skill cards move to discard pile if they are played. We also have Status or Curse cards which are unplayable and most of the time are the cards that disadvantage the player in some way.
        Block: Until next turn, prevents damage. For example, if the player gains 5 block, and the enemy deals 7 damage to him that turn, the player loses only 2 HP and all their block. It only lasts one turn, so if there are any remining blocks on the enemy or the player, the blocks are removed right before they perform their next set of actions.
        Vulnerable: Take 50% more damage from Attack damage. Note that this only applies to damage coming from an Attack type card or an enemy Attack action. The number of Vulnerable shows how many turns it will last.
        Weak: Deal 25% less damage with Attacks. Note that this only applies to damage coming from an Attack type card or an enemy Attack action. The number of Weak shows how many turns it will last.
        Strength: Adds additional damage to Attacks. Note that this only applies to damage coming from an Attack type card or an enemy Attack action.
        Exhaust: Remove card until end of combat.
        Wound: An unplayable card with no effects.
        Ethereal: If an Ethereal card is in player's hand at the end of turn, it is Exhasted.
        Dazed: An unplayable card which is also Ethereal.
        Innate: Start each combat with this card in your hand.
        Burn: An unplayable card. If the card is in player's hand at the end of his turn, the player will take 2 damage.
        X cost card: If a card's cost is X, it means that when the card is played, it will consume all the avaialble energy the player has. This number of energy consumed is X, and the effect of the card is often described in terms of X.
        When a card says "At the start of your turn ..." or "At the end of your turn ...", it means this effect will happen every single turn at the start of player's turn or at the end of player's turn.
        Any questoins so far?\n'''))
    responses.append(dedent(
        '''No questions at the moment. I'm ready to give feedback on specific card designs or mechanics you have in mind!\n'''
    ))
    return prompts, responses

class AskType(Enum):
        Legacy = -1,
        Negative_or_Positive = 0,
        NP_Bundle = 1,
def get_sts_ask(ask_type: AskType):
    if ask_type == AskType.Legacy:
        prompt = dedent(
            f'''Now, I want you to help me understand card {SYNERGY_KEYWORD} effects.
            Basically, a {SYNERGY_KEYWORD} effect is when two cards have some additional effect when played together when compared to playing them separately.
            For example, let's say there is a card A that says "deal 5 damage and apply 1 Vulnerable" and a card B that says "deal 4 damage". If a player plays card A, he deals 5 damage, and if card B is played in a separate scenairo, it applies 4 damage. This is 9 damage in total. But if the player first plays card A and then card B after (in the same turn), card A deals 5 damage and card B deals 6 damage (instead of 4, because the enemy is vulnerable). So, in general the player does 5 + 6 = 11 damage instead of 9. We call this a positive {SYNERGY_KEYWORD}, since this extra effect is advantaging the player.
            {SYNERGY_KEYWORD_CAPITALIZED} is dependant on the order of cards. For example, if the player plays card B first and then card A, card B does 4 damage, and card A does 5 damage and applies Vulnerable. That Vulnerable effect can be beneficial in combination with other cards played later, but the two cards B and A in this order don't have a {SYNERGY_KEYWORD}.
            For another example of cards that don't have {SYNERGY_KEYWORD}, let's say card C says "deal 15 damage and gain 1 Weak", and card D says "Gain 5 Block". Card C has it's own effect, dealing damage and applying Weak to the player himself, which can has interesting effects in the game. But, if we played card C and then D, there is no {SYNERGY_KEYWORD}, since there is no additional effect from this combination. Same for if play card D and then C, again there is no extra effect.
            Some cards also have a negative {SYNERGY_KEYWORD}. For example, if you play card C and then card B, card C deals 15 damage, and card B deals 25% less damage (3 instead of 4), so you do 15 + 3 = 18 damage, which is less than if you look at the cards in isolation (15 damage and 4 damage). Note that again, order matters. Playing B first and then C doesn't have any {SYNERGY_KEYWORD}, positive or negative.
            The {SYNERGY_KEYWORD_PLURAL} can be normal, strong, or weak. Weak simulations are when there is a lot of setup or some other situations needed for that {SYNERGY_KEYWORD}, or if the {SYNERGY_KEYWORD} itself is not that strong of an effect.
            Now, given two cards, I want you to first describe their {SYNERGY_KEYWORD}, if any. I want you to think about this effect carefully. Again, some cards might not have a {SYNERGY_KEYWORD} at all. When trying to understand the {SYNERGY_KEYWORD}, we want to think about the effect of the cards, played in the exact given order, either immediately or after waiting some number of turns. Let's also assume that you have enough energy to play them in the same turn if needed, but if you think there are some considerations from one card to another that can be seen as a {SYNERGY_KEYWORD}, I want you to describe it.
            Second, I want you to give this description, tell me if the {SYNERGY_KEYWORD} is positive or negative, and how strong it is. Let's say, something like card A and B is a normal {SYNERGY_KEYWORD}. If the {SYNERGY_KEYWORD} effect is stronger, we call it strong and if it's weaker, very situational, or requies a lot of setup, we call it weak.
            Finally, I want to give me a final number at the end of your response in a single line.
            0: no {SYNERGY_KEYWORD}
            1: normal positive {SYNERGY_KEYWORD}
            0.5: weak positive {SYNERGY_KEYWORD}
            2: strong positive {SYNERGY_KEYWORD}
            -1: normal negative {SYNERGY_KEYWORD}
            -0.5: weak negative {SYNERGY_KEYWORD}
            -2: strong negative {SYNERGY_KEYWORD}
            When I give you the card descriptions, I want these exact three things. Make sure to describe each part and to end your response by writing the final number in a single line.
            Any questions?\n''')
    elif ask_type in [AskType.Negative_or_Positive, AskType.NP_Bundle]:
        prompt = dedent(
            f'''Now, I want you to help me understand card {SYNERGY_KEYWORD} effects.
            A {SYNERGY_KEYWORD} effect is when two cards have some additional effect when played together when compared to playing them separately.
            Let's say we have two cards, card A and card B. Each card has its own positive and negative effects, and can be strong or weak in different situations.
            Now, suppose we play card A in some scenario S with some other cards. Suppose we play card B in scenario S with some other cards.
            Is there a possible scenario S in which playing card A, then card B, would give us additional advantages or disadvantages when compared to the effects of card A in scenario S and card B in scenario S?
            If in most scenarios, there is an extra advantagous effects of playing the cards together, we call this a positive {SYNERGY_KEYWORD}.
            If in most cases, there is a disadvantages additional effect when A and then B is played (compared to playing them separately), we call this a negative {SYNERGY_KEYWORD}.
            Note that:
            - When we say "play card A, then card B", this can mean playing B immediately after playing A, or after playing other cards in between, or even after passing a few turns in between.
            - When we talk about {SYNERGY_KEYWORD} between card A and card B, only consider {SYNERGY_KEYWORD} BETWEEN A AND B. For example, if card A has a lot of {SYNERGY_KEYWORD} with other cards, it doesn't matter, because playing card A with other cards would still give us those effects. We want to see what additional effects we get from A and B together.
            Now, given two cards, I want you to first describe their {SYNERGY_KEYWORD}, if any. I want you to think about this effect carefully. Again, some cards might not have a {SYNERGY_KEYWORD} at all. When trying to understand the {SYNERGY_KEYWORD}, we want to think about the effect of the cards, played in the exact given order, either immediately or after waiting some number of turns or playing some other cards. Let's also assume that you have enough energy to play them in the same turn if needed, but if you think there are some considerations from one card to another that can be seen as a {SYNERGY_KEYWORD}, I want you to describe it.
            Second, I want you to given this description, tell me if the {SYNERGY_KEYWORD} is positive or negative, or if there is no {SYNERGY_KEYWORD} at all.
            Finally, I want to give me a final number at the end of your response in a single line.
            0: no {SYNERGY_KEYWORD}
            1: positive {SYNERGY_KEYWORD}
            -1: negative {SYNERGY_KEYWORD}
            When I give you the card descriptions, I want these exact three things. Make sure to describe each part and to end your response by writing the final number in a single line.
            Any questions?\n''')
    else:
        raise Exception("Ask Type unrecognised")
    response = dedent(
        f'''I’m ready to analyze the {SYNERGY_KEYWORD_PLURAL} for you. Please provide the descriptions of card A and card B.\n'''
    )
    return prompt, response

def get_few_shot_examples(ask_type: AskType, shot_count=None):
    if ask_type == AskType.Legacy:
        assert shot_count is None, "number of few-shot examples is not supported for Legacy prompt"
        # responses generated with gpt-4o-mini, but in a conversation format and while giving human feedback
        prompts, responses = [], []
        prompts.append(dedent(
            f'''Ok, let's think!
            Card 1 (Attack Type) - Costs 4: "Costs 1 less energy for each time you lose HP in combat. Deal 18 damage."
            Card 2 (Attack Type) - Costs 2: "Deal 8 damage. Apply 2 Vulnerable."
            Describe the {SYNERGY_KEYWORD} between playing card 1, then card 2.\n'''))
        responses.append(dedent(
            f'''### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            1. **Order of Play:** Card 1 is played first, followed by Card 2.

            2. **Effects Breakdown:**
            - **First, Card 1 is played.** It deals its full 18 damage immediately. The energy cost can be reduced, assuming the player has lost HP, but that {SYNERGY_KEYWORD} is outside the effects between card 1 then 2.
            - **Next, Card 2 is played.** This card deals 8 damage and applies 2 Vulnerable to the enemy. However, since the damage from Card 2 applies *after* Card 1 has already dealt damage, the Vulnerable effect does not enhance Card 1’s damage at all.

            3. **{SYNERGY_KEYWORD_CAPITALIZED} Result:**
            - When played in this order, the total damage becomes **18 (from Card 1) + 8 (from Card 2) = 26 damage.**
            - If Card 2 were played first (which can be done if energy allows), it would deal only 8 damage and apply Vulnerable, but Card 1 would still only deal 18 damage afterward without any enhancement from the Vulnerable effect.

            4. **Conclusion on {SYNERGY_KEYWORD_CAPITALIZED}:**
            - The {SYNERGY_KEYWORD} here doesn't actually result in an increased damage output because Card 1's damage does not benefit from the Vulnerable effect that Card 2 applies afterward. Therefore, there is no positive {SYNERGY_KEYWORD} between these two cards in this order; they simply contribute separately to the total damage. They also don't have any non-damage related {SYNERGY_KEYWORD_PLURAL}.

            ### Synergy Strength:
            - Since there is **no additional effect** from the order of these cards, we can say they have **no {SYNERGY_KEYWORD}**.

            Final score:
            0\n'''
        ))
        prompts.append(dedent(
            '''Nice! Let's look at another example: What if I play card 2 first, and then card 1?\n'''
        ))
        responses.append(dedent(
            f'''### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            1. **Order of Play:** Card 2 is played first, followed by Card 1.

            2. **Effects Breakdown:**
            - **First, Card 2 is played.** It deals 8 damage, and then, applies 2 Vulnerable to the enemy. The application of Vulnerable means the enemy will take 50% more damage from Attack damage this turn and the next.
            - **Next, Card 1 is played.** This card will now deal its full 18 damage. However, since the enemy is Vulnerable and this card is an Attack Type card, the damage from Card 1 is increased by 50%. Thus, Card 1 will deal **18 + (18 * 0.5) = 27 damage**.

            3. **{SYNERGY_KEYWORD_CAPITALIZED} Result:**
            - When played in this order, the total damage becomes **8 (from Card 2) + 27 (from Card 1 with Vulnerable effect) = 35 damage.**
            - If played separately, Card 2 would deal the 8 damage and apply the vulnerable, but Card 1 would only deal its 18 damage, resulting in **18 + 8 = 26 damage** without any {SYNERGY_KEYWORD}.

            4. **Conclusion on {SYNERGY_KEYWORD_CAPITALIZED}:**
            - In this order, playing Card 2 first to apply Vulnerable before playing Card 1 significantly increases the total damage, demonstrating a clear positive {SYNERGY_KEYWORD}. The addition of the Vulnerable means that the damage from Card 1 is effectively enhanced.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Strength:
            - This combination leads to a higher damage output than playing them in isolation. However, the {SYNERGY_KEYWORD} is of normal strenght, since the advantage is not huge.

            Final score:
            1\n'''
        ))
        prompts.append(dedent(
            '''Great job! Let's now look at another example again: Card 3 (Skill Type) - Costs 0: "Lose 3 HP. Gain 2 Energy." what if I play card 1 then card 3?\n'''
        ))
        responses.append(dedent(
            f'''### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            1. **Order of Play:** Card 1 is played first, followed by Card 3.

            2. **Effects Breakdown:**
            - **First, Card 1 is played.** It deals its full 18 damage. The energy cost may be lessened depending on the player's HP lost prior to this turn but will not be affected by Card 3 yet.
            - **Next, Card 3 is played.** The player loses 3 HP and gains 2 energy. Losing HP means that for future turns, or even in subsequent effects in this current turn, it may reduce the energy cost of Card 1 if the player hasn’t already played it (but this is not applicable to this {SYNERGY_KEYWORD} analysis since Card 1 is already played).

            3. **{SYNERGY_KEYWORD_CAPITALIZED} Result:**
            - Playing Card 1 first results in **18 damage**. Then, playing Card 3 afterwards causes the player to lose HP and gain energy. However, this energy gained is not used in this instance since it occurs after Card 1 has already been played.
            - The interaction here does not result in additional damage or effects because the damage from Card 1 is already resolved before Card 3 is played.

            4. **Conclusion on {SYNERGY_KEYWORD_CAPITALIZED}:**
            - In this order, the cards do not demonstrate any {SYNERGY_KEYWORD} because playing Card 3 after Card 1 does not create any benefits or changes in damage output. The player expends energy but simply loses HP without enhancing the outcome of Card 1.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Strength:
            - There is no additional effect from playing these cards in this order, thus resulting in **no {SYNERGY_KEYWORD}**.

            Final score:
            0\n'''
        ))
        prompts.append(dedent(
            '''Nice! Another example: what if I play card 3 then card 1?\n'''
        ))
        responses.append(dedent(
            f'''### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            1. **Order of Play:** Card 3 is played first, followed by Card 1.

            2. **Effects Breakdown:**
            - **First, Card 3 is played.** The player loses 3 HP and gains 2 energy. This means that regardless of their current HP, they will now be at a lower HP, which could influence future card costs.
            - **Next, Card 1 is played.** Because the player lost HP from playing Card 3, the energy cost of Card 1 will be reduced. Assuming the player has lost at least 1 HP, the cost of Card 1 will now be 2 if they started with 3 energy or 1 if they started with 4 energy. The card will also deal 18 damage.

            3. **{SYNERGY_KEYWORD_CAPITALIZED} Result:**
            - Since Card 3 was played first, it allows Card 1's cost to be reduced by 1 (assuming the player has lost HP), and it will still execute its full 18 damage. The energy gained from Card 3 (2 energy) means the player can comfortably play Card 1 without an issue regarding energy cost.
            - The total damage done when played in this order is **18 damage** from Card 1, as the previous HP loss does not provide additional benefits for this particular execution.

            4. **Conclusion on {SYNERGY_KEYWORD_CAPITALIZED}:**
            - Although the damage produced remains constant compared to playing the two cards in isolation, the {SYNERGY_KEYWORD} lowers the total amount of energy spent here, and shows a major interaction between the two.
            - The {SYNERGY_KEYWORD} is positive because Card 3 facilitates playing Card 1 smoothly with potentially reduced cost.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Strength:
            - Since there is a major effect between the two, the {SYNERGY_KEYWORD} is a bit stronger than normal.

            Final score:
            2\n'''
        ))
        prompts.append(dedent(
            '''Great! I have another question: What if I play card 2 then card 3?\n'''
        ))
        responses.append(dedent(
            f'''### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            1. **Order of Play:** Card 2 is played first, followed by Card 3.

            2. **Effects Breakdown:**
            - **First, Card 2 is played.** The player deals 8 damage and applies 2 Vulnerable to the enemy.
            - **Next, Card 3 is played.** The player loses 3 HP and gains 2 energy. However, losing HP from Card 3 doesn't enhance or alter the outcome of the damage dealt by Card 2.

            3. **{SYNERGY_KEYWORD_CAPITALIZED} Result:**
            - When Card 2 is played, the total damage dealt is **8 damage**. After that, Card 3 is played but does not change the damage already dealt by Card 2. The vulnerability applied by Card 2 is relevant for future damage but does not interact with or enhance the initial damage from Card 2.
            - If these cards were played separately (Card 2 followed by Card 3), the results would be the same as in this sequence, totaling **8 (from Card 2) + 0 (from Card 3)**.

            4. **Conclusion on {SYNERGY_KEYWORD_CAPITALIZED}:**
            - In this specific order, Card 3 provides no additional benefit or enhancement to the damage output of Card 2. The two cards do not {SYNERGY_KEYWORD_VERB} positively or negatively; Card 2's impact is unaffected by what follows.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Strength:
            - Given that the two cards played in this order do not enhance each other at all, there is **no {SYNERGY_KEYWORD}** between Card 2 and Card 3.

            Final score:
            0\n'''
        ))
        prompts.append(dedent(
            f'''Interesting! Let's say we have:
            Card 4 (Skill Type) - Cost 1: Gain 7 Block. Exhaust a random card from your hand.
            What is the {SYNERGY_KEYWORD} effect of playing card 4, then card 2?\n'''
        ))
        responses.append(dedent(
            f'''### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            1. **Order of Play:** Card 4 is played first, followed by Card 2.

            2. **Effects Breakdown:**
            - **First, Card 4 is played.** The player gains 7 Block, which will absorb damage up to that amount until the end of the player's next turn. Additionally, one random card from the player's hand is exhausted (removed until the end of combat).
            - **Next, Card 2 is played.** This card deals 8 damage and applies 2 Vulnerable to the enemy.     

            3. **{SYNERGY_KEYWORD_CAPITALIZED} Result:**
            - When Card 4 is played first, the player now has 7 Block, which helps mitigate damage from any incoming attacks during the enemy's turn after they play Card 2.
            - The Block itself doesn't enhance the damage from Card 2. Applying Vulnerable means that the enemy will take 50% more damage from future attacks, which can be especially valuable if further Attack cards are played later during this turn or in subsequent turns.
            - However, in the immediate context of Card 4 followed by Card 2, the damage output is **8 (from Card 2)**, and there is no interaction between the cards.

            4. **Conclusion on {SYNERGY_KEYWORD_CAPITALIZED}:**
            - There is no {SYNERGY_KEYWORD} here. The Vulnerable effect can help future cards, but doesn't affect this scenario and compared to playing the cards in isolation and adding up their effects, there is no difference. There is a possibility that card 4 exhausting some other card can result in more Attack cards remaining and better use of Vulnerable in the future, but it is as likely to exhaust a skill card and make it harder to use the Vulnerable effect in the future. The Block doesn't create any interaction between the cards.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Strength:
            - No {SYNERGY_KEYWORD} exists.

            Final score:
            0\n'''
        ))
        prompts.append(dedent(
            f'''Nice! What if what about the {SYNERGY_KEYWORD} between card 4 and then card 1?\n'''
        ))
        responses.append(dedent(
            f'''### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            1. **Order of Play:** Card 4 is played first, followed by Card 1.

            2. **Effects Breakdown:**
            - **First, Card 4 is played.** The player gains 7 Block and exhausts a random card from their hand. The Block will absorb up to 7 damage until the player's next turn.
            - **Next, Card 1 is played.** Card 1 will deal 18 damage. The energy cost of Card 1 might be affected by how much HP the player has lost previously in combat, but with Card 4 being played first, the player has not lost any HP yet (only gained Block).

            3. **{SYNERGY_KEYWORD_CAPITALIZED} Result:**
            - Card 4 gives some Block and card 1 is dealing damage. In combination, the have the same exact effect.
            - The direct damage output from this combination remains **18 damage (from Card 1)**, and there is no enhancement of damage based on the previous play.
            - However, there is an extra effect: having that extra 7 Blocks makes it less likely to receive damage. As discussed before, we can imagine some number of turns have passed between playing the two cards. So, in that case, it would be more likely to have a higher cost for card 1, since card 4 can make it less likely to receive damage in that turn.

            4. **Conclusion on {SYNERGY_KEYWORD_CAPITALIZED}:**
            - There is a small possibility that card 4 prevents the player from receiving any damage in the turn it is played. While this is normally positive, there is a small extra negative effect that the player gets damage one less time before playing card 1, making card 1 slightly more expensive.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Strength:
            - The likelihood of this happening is very small. First, there should be incoming damage with an amount that playing card 4 is the difference between receiving any damage and not receiving any damage. Second, there should be a number of turns before playing the card 1. Third, card 1 should have a cost more than 0 for this effect to be important. Because this is very situational, the {SYNERGY_KEYWORD} is **weak**.

            Final score:
            -0.5\n'''
        ))
        prompts.append(dedent(
            f'''Nice! What if what about the {SYNERGY_KEYWORD} between card 4 and then another one of  card 4 again?\n'''
        ))
        responses.append(dedent(
            f'''### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            1. **Order of Play:** Card 4 is played first, followed by Card 4.

            2. **Effects Breakdown:**
            - **First, Card 4 is played.** The player gains 7 Block and exhausts a random card from their hand. The Block will absorb up to 7 damage until the player's next turn.
            - **Next, Card 1 is played.** The player gains an additional 7 Block and again exhausts a random card from their hand.

            3. **{SYNERGY_KEYWORD_CAPITALIZED} Result:**
            - Card 4 gives some Block and exhausing a card from player's hand. The total Block gained is **7 (from the first card 4) + 7 (from the second card 4) = 14 Block**.
            - Compared to playing the card 4 in isolation twice, there is no additional effect, because that also results in 7 Block each.

            4. **Conclusion on {SYNERGY_KEYWORD_CAPITALIZED}:**
            - There is no {SYNERGY_KEYWORD} between the two cards.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Strength:
            - Since there is no additional benefit or change in the effect of playing this card twice in combination vs in isolation, the cards do not have {SYNERGY_KEYWORD} in this case.

            Final score:
            0\n'''
        ))
        next_card_number = 5
    elif ask_type == AskType.Negative_or_Positive:
        assert shot_count is None, "number of few-shot examples is not supported for negative/positive prompt"
        # responses generated with gpt-4o, but in a conversation format and while giving human feedback
        # occasionally you see the word synergy without the use of synergy_keyword.
        # This is because these answers were generated using the "combo" keyword. Any use of word synergy is part of the response.
        prompts, responses = [], []
        prompts.append(dedent(
            f'''Ok, let's think!
            Card 1 (Attack Type) - Costs 4: "Costs 1 less energy for each time you lose HP in combat. Deal 18 damage."
            Card 2 (Attack Type) - Costs 2: "Deal 8 damage. Apply 2 Vulnerable."
            Describe the {SYNERGY_KEYWORD} between playing card 1, then card 2.\n'''))
        responses.append(dedent(
            f'''### Card Descriptions and Effects:
            - **Card 1:**  
            - Costs 4 energy initially but costs 1 less for each time you lose HP in combat.
            - Deals 18 damage.
            
            - **Card 2:**  
            - Costs 2 energy.
            - Deals 8 damage and applies 2 Vulnerable (causing the target to take 50% more damage from subsequent Attack cards for 2 turns).

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:

            1. **Order of Play - Card 1, then Card 2:**
            - **Playing Card 1 First:**
                - You deal 18 damage to the enemy.
                - The energy cost reduction mechanic of Card 1 does not directly affect Card 2 unless HP loss influences the sequence in some other conditional way.
            
            - **Playing Card 2 Next:**
                - After Card 1, Card 2 deals 8 damage and applies 2 turns of Vulnerable.
                - Vulnerable does not retroactively enhance Card 1's damage, as it should be applied *before* dealing maximum damage.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            - **{SYNERGY_KEYWORD_CAPITALIZED} Effectiveness:**
            - The ideal scenario would be to apply Vulnerable before dealing high damage to maximize impact, but here, Card 1 is played first, negating this potential synergy.
            - There is no inherent synergy gained by playing Card 1 before Card 2. The ordering does not yield any extra advantage or disadvantage compared to playing them separately, especially since Vulnerable enhances future damage, not past damage.

            ### Conclusion:
            Since playing Card 1 followed by Card 2 does not create an advantageous effect when considering the order of operations, and since no special disadvantage arises from this sequence beyond not maximizing potential damage output, there isn’t a notable {SYNERGY_KEYWORD} effect here.

            Final score:
            0\n'''
        ))
        prompts.append(dedent(
            '''Nice! Let's look at another example: What if I play card 2 first, and then card 1?\n'''
        ))
        responses.append(dedent(
            f'''### Card Descriptions and Effects:
            - **Card 2:**
            - Costs 2 energy.
            - Deals 8 damage and applies 2 Vulnerable (causing the target to take 50% more damage from subsequent Attack cards for 2 turns).

            - **Card 1:**
            - Costs 4 energy initially but costs 1 less for each time you lose HP in combat.
            - Deals 18 damage.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:

            1. **Order of Play - Card 2, then Card 1:**
            - **Playing Card 2 First:**
                - You deal 8 damage to the enemy and apply 2 turns of Vulnerable, increasing subsequent Attack damage by 50%.
            
            - **Playing Card 1 Next:**
                - Card 1 is now able to take advantage of the Vulnerable status applied by Card 2.
                - When Card 1 deals 18 damage, with the opponent being Vulnerable, it actually deals 27 damage (18 damage increased by 50%). This significantly increases the total damage output from the sequence of plays.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            - **{SYNERGY_KEYWORD_CAPITALIZED} Effectiveness:**
            - Playing Card 2 first and applying Vulnerable means that Card 1's damage is increased by 50% due to the Vulnerable status. This is the kind of synergy one looks for in setting up a sequence of plays.
            - The combined damage of these plays is effectively 35 damage (8 from Card 2 and 27 from Card 1 under vulnerability effects), compared to 26 damage (8 + 18) if Vulnerable were not in place when Card 1 was played.

            ### Conclusion:
            This sequence creates a positive synergy due to the effective use of Vulnerable status to amplify damage from Card 1, making it a positive {SYNERGY_KEYWORD}.

            Final score:
            1\n'''
        ))
        prompts.append(dedent(
            '''Great job! Let's now look at another example again: Card 3 (Skill Type) - Costs 0: "Lose 3 HP. Gain 2 Energy." what if I play card 1 then card 3?\n'''
        ))
        responses.append(dedent(
            f'''### Card Descriptions and Effects:
            - **Card 1:**
            - Costs 4 energy initially but costs 1 less for each time you lose HP in combat.
            - Deals 18 damage.

            - **Card 3:**
            - Costs 0 energy.
            - Causes you to lose 3 HP but grants 2 energy.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:

            1. **Order of Play - Card 1, then Card 3:**
            - **Playing Card 1 First:**
                - Initially costs 4 energy and deals 18 damage.
                - Your current HP loss from playing Card 1 is irrelevant before playing Card 3.

            - **Playing Card 3 Next:**
                - You lose 3 HP, which potentially activates the effect of reducing Card 1's cost if played in future turns.
                - Gain 2 additional energy. However, since Card 1 has already been played, the immediate scenario doesn’t directly benefit from the extra energy unless it allows you to play other cards. 

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            - **{SYNERGY_KEYWORD_CAPITALIZED} Effectiveness:**
            - The play order implies no immediate synergy because any potential benefit from Card 3's effect on Card 1 is realized only in future plays of Card 1, provided it's repeatedly drawn in combat.
            - Card 3 grants more resources (energy) and theoretically allows for more plays, but for the immediate sequence of Card 1 then Card 3, there are no direct efficiency gains or additional effects.

            ### Conclusion:
            Since the described order doesn't produce an immediate advantageous or disadvantageous effect, considering the given conditions, there is no {SYNERGY_KEYWORD} in the sequence where Card 1 is played before Card 3.

            Final score:
            0\n'''
        ))
        prompts.append(dedent(
            '''Nice! Another example: what if I play card 3 then card 1?\n'''
        ))
        responses.append(dedent(
            f'''### Card Descriptions and Effects:
            - **Card 3:**
            - Costs 0 energy.
            - Causes you to lose 3 HP and grants 2 energy.

            - **Card 1:**
            - Costs 4 energy initially but costs 1 less for each time you lose HP in combat.
            - Deals 18 damage.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:

            1. **Order of Play - Card 3, then Card 1:**
            - **Playing Card 3 First:**
                - You lose 3 HP, activating the cost reduction mechanic of Card 1.
                - You also gain 2 additional energy, increasing your resource pool for the current turn.
            
            - **Playing Card 1 Next:**
                - The cost of Card 1 is now reduced by 1 due to the HP loss from Card 3.
                - This lets you save 1 energy, which can be used to play additional cards during your turn.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            - **{SYNERGY_KEYWORD_CAPITALIZED} Effectiveness:**
            - Playing Card 3 first directly synergizes with Card 1 by reducing Card 1’s cost through the HP loss mechanic.
            - The extra energy provided is not part of the {SYNERGY_KEYWORD} effect, since it is not part of the interaction between the two cards.

            ### Conclusion:
            The play order of Card 3 followed by Card 1 results in a positive {SYNERGY_KEYWORD} due to the immediate cost reduction, which optimizes your energy usage and potentially broadens your strategic options for the rest of the turn.

            Final score:
            1\n'''
        ))
        prompts.append(dedent(
            '''Great! I have another question: What if I play card 2 then card 3?\n'''
        ))
        responses.append(dedent(
            f'''### Card Descriptions and Effects:
            - **Card 2:**
            - Costs 2 energy.
            - Deals 8 damage and applies 2 Vulnerable (causing the target to take 50% more damage from subsequent Attack cards for 2 turns).

            - **Card 3:**
            - Costs 0 energy.
            - Causes you to lose 3 HP and grants 2 energy.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:

            1. **Order of Play - Card 2, then Card 3:**
            - **Playing Card 2 First:**
                - You spend 4 energy to deal 8 damage and apply 2 Vulnerable to an enemy.
            
            - **Playing Card 3 Next:**
                - Since Card 2 has already used up most of your energy, the additional 2 energy from Card 3 would allow you to regain some resource availability for additional plays in the same turn.
                - The 3 HP loss from Card 3 does not directly interact with Card 2 because Vulnerable affects damage taken, not energy or HP mechanics.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            - **{SYNERGY_KEYWORD_CAPITALIZED} Effectiveness:**
            - Playing Card 2 after Card 3 allows for potential further plays due to the energy burst from Card 3. However, there is no direct synergy between the cards' effects themselves.
            - Card 3 provides additional energy but playing it after Card 2 just restores some energy spent, which is useful for continuing the turn with more plays but not a synergistic {SYNERGY_KEYWORD} specific to these two cards' interactions.

            ### Conclusion:
            The sequence offers no notable synergistic interaction beyond regaining energy to play more cards. While this order may allow for greater flexibility in a turn by reopening energy options, nothing about the cards’ effects inherently enhances or diminishes the other's utility.

            Final score:
            0\n'''
        ))
        prompts.append(dedent(
            f'''Interesting! Let's say we have:
            Card 4 (Skill Type) - Cost 1: Gain 7 Block. Exhaust a random card from your hand.
            What is the {SYNERGY_KEYWORD} effect of playing card 4, then card 2?\n'''
        ))
        responses.append(dedent(
            f'''### Card Descriptions and Effects:
            - **Card 4:**
            - Costs 1 energy.
            - Gains 7 Block.
            - Exhausts a random card from your hand.

            - **Card 2:**
            - Costs 2 energy.
            - Deals 8 damage and applies 2 Vulnerable.

            ### New {SYNERGY_KEYWORD_CAPITALIZED} Analysis:

            1. **Order of Play - Card 4, then Card 2:**
            - Playing Card 4 confers 7 Block and exhausts a random card. This can impact any card, but it’s important to note this does not specifically interact with Card 2’s mechanism or effects.
            - After playing Card 4, if Card 2 is still in hand, you can play Card 2 normally, dealing 8 damage and applying 2 Vulnerable.

            ### Conclusion:
            Given that the risk of losing a card to exhaustion from Card 4 is an inherent risk not specific to Card 2, the sequence doesn't introduce any unique advantages or disadvantages specifically related to Card 2 beyond the inherent exhausting mechanic. Thus, there is no direct {SYNERGY_KEYWORD} effect due to the specific ordering of these cards.

            Final score:
            0\n'''
        ))
        prompts.append(dedent(
            f'''Nice! What if what about the {SYNERGY_KEYWORD} between card 4 and then card 1?\n'''
        ))
        responses.append(dedent(
            f'''### Card Descriptions and Effects:
            - **Card 4:**
            - Costs 1 energy.
            - Gains 7 Block.
            - Exhausts a random card from your hand.

            - **Card 1:**
            - Costs 4 energy initially but costs 1 less for each time you lose HP in combat.
            - Deals 18 damage.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:

            1. **Order of Play - Card 4, then Card 1:**
            - **Playing Card 4 First:**
                - You gain 7 Block to protect against incoming damage, which is generally positive.       
                - A random card from your hand is exhausted. This is a risk inherent to Card 4 but doesn't specifically impact Card 1 more than any other card.

            - **Playing Card 1 Next:**
                - Gaining Block reduces the potential to take damage this turn, which could have reduced Card 1’s energy cost if the player would have taken HP loss.
                - Although gaining Block is beneficial for immediate protection, it indirectly reduces the possibility of taking advantage of Card 1’s cost reduction mechanic.

            ### Conclusion:
            Considering both the subtle negative synergy between gaining Block and potentially reducing Card 1's cost, the sequence can be considered a slight negative {SYNERGY_KEYWORD} due to the fact that playing Card 4 first may inadvertently result in a less optimal use of resources for playing Card 1.

            Final score:
            -1\n'''
        ))
        prompts.append(dedent(
            f'''Nice! What if what about the {SYNERGY_KEYWORD} between card 4 and then another one of card 4 again?\n'''
        ))
        responses.append(dedent(
            f'''### Card Descriptions and Effects:
            - **Card 4:**
            - Costs 1 energy.
            - Gains 7 Block.
            - Exhausts a random card from your hand.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:

            1. **Order of Play - Card 4, then another Card 4:**
            - **First Card 4:**
                - Provides 7 Block for protection.
                - Exhausts a random card from your hand as a part of its fundamental effect.

            - **Second Card 4:**
                - Adds another 7 Block, further boosting your defense.
                - Again exhausts a random card, removing another card from your hand.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            - **{SYNERGY_KEYWORD_CAPITALIZED} Effectiveness:**
            - The primary effect of playing two Card 4s is the accumulation of a substantial 14 Block.   
            - The repeated card exhaustion could limit your strategic options, but it's not specific to the combination itself.
            - There’s no direct synergy or additional interplay between the two instances of Card 4 beyond their individual effects stacking.

            ### Conclusion:
            The sequential play of two Card 4s results in stacking of Block, a straightforward cumulative effect that does not introduce new positive or negative synergy beyond the individual card effects. As such, there isn't a net new {SYNERGY_KEYWORD} effect present.

            Final score:
            0\n'''
        ))
        next_card_number = 5
    elif ask_type == AskType.NP_Bundle:
        # same as AskType.Negative_or_Positive, only bundled all cards together
        prompts, responses = [], []
        cards_needed = [2, 2, 3, 3, 3, 4, 4, 4]
        prompts.append(dedent(
            f'''Ok, let's think! I give you some card descriptions and ask you for your analysis on a few pairs. I want to separate the analysis for each case by a line containing only ---NEXT---.
            Cards:\n'''))
        cards_defs = [
            f'''Card 1 (Attack Type) - Cost 4: "Costs 1 less energy for each time you lose HP in combat. Deal 18 damage."\n''',
            f'''Card 2 (Attack Type) - Cost 2: "Deal 8 damage. Apply 2 Vulnerable."\n''',
            f'''Card 3 (Skill Type) - Cost 0: "Lose 3 HP. Gain 2 Energy."\n''',
            f'''Card 4 (Skill Type) - Cost 1: "Gain 7 Block. Exhaust a random card from your hand."\n''',
        ]
        cases = [
            f'''1. Analyze the {SYNERGY_KEYWORD} between playing card 1, then card 2.\n''',
            f'''2. What if I play card 2 first, and then card 1?\n''',
            f'''3. What if I play card 1 then card 3?\n''',
            f'''4. What if I play card 3 then card 1?\n''',
            f'''5. What if I play card 2 then card 3?\n''',
            f'''6. What if I play card 4 then card 2?\n''',
            f'''7. What if I play card 4 then card 1?\n''',
            f'''8. What if I play card 4 then another card 4 again?\n''',
        ]
        if shot_count is None:
            shot_count = len(cases)
        assert shot_count <= len(cases), f"only {len(cases)} examples available, requested {shot_count}-shot"
        # TODO 0 should still work, but the prompt should be slightly modified, or this prompt should be completely removed.
        # Also, I expect 0 to create formatting problems, since LLM doesn't keep to the requested format that way
        assert shot_count > 0, f"only positive example count is supported"
        assert max(cards_needed) == len(cards_defs), "number of card definitions doesn't match the maximum supported card count"
        assert len(cards_needed) == len(cases), "cards_needed doesn't match the info for every case"
        prompts[-1] += ''.join(cards_defs[:cards_needed[shot_count-1]])
        prompts[-1] += 'Cases:\n'
        prompts[-1] += ''.join(cases[:shot_count])
        case_responses = [dedent(
            f'''# Case 1
            ### Card Descriptions and Effects:
            - **Card 1:**  
            - Costs 4 energy initially but costs 1 less for each time you lose HP in combat.
            - Deals 18 damage.
            
            - **Card 2:**  
            - Costs 2 energy.
            - Deals 8 damage and applies 2 Vulnerable (causing the target to take 50% more damage from subsequent Attack cards for 2 turns).

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:

            1. **Order of Play - Card 1, then Card 2:**
            - **Playing Card 1 First:**
                - You deal 18 damage to the enemy.
                - The energy cost reduction mechanic of Card 1 does not directly affect Card 2 unless HP loss influences the sequence in some other conditional way.
            
            - **Playing Card 2 Next:**
                - After Card 1, Card 2 deals 8 damage and applies 2 turns of Vulnerable.
                - Vulnerable does not retroactively enhance Card 1's damage, as it should be applied *before* dealing maximum damage.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            - **{SYNERGY_KEYWORD_CAPITALIZED} Effectiveness:**
            - The ideal scenario would be to apply Vulnerable before dealing high damage to maximize impact, but here, Card 1 is played first, negating this potential synergy.
            - There is no inherent synergy gained by playing Card 1 before Card 2. The ordering does not yield any extra advantage or disadvantage compared to playing them separately, especially since Vulnerable enhances future damage, not past damage.

            ### Conclusion:
            Since playing Card 1 followed by Card 2 does not create an advantageous effect when considering the order of operations, and since no special disadvantage arises from this sequence beyond not maximizing potential damage output, there isn’t a notable {SYNERGY_KEYWORD} effect here.

            Final score:
            0\n'''),
            dedent(
            f'''---NEXT---
            # Case 2
            ### Card Descriptions and Effects:
            - **Card 2:**
            - Costs 2 energy.
            - Deals 8 damage and applies 2 Vulnerable (causing the target to take 50% more damage from subsequent Attack cards for 2 turns).

            - **Card 1:**
            - Costs 4 energy initially but costs 1 less for each time you lose HP in combat.
            - Deals 18 damage.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:

            1. **Order of Play - Card 2, then Card 1:**
            - **Playing Card 2 First:**
                - You deal 8 damage to the enemy and apply 2 turns of Vulnerable, increasing subsequent Attack damage by 50%.
            
            - **Playing Card 1 Next:**
                - Card 1 is now able to take advantage of the Vulnerable status applied by Card 2.
                - When Card 1 deals 18 damage, with the opponent being Vulnerable, it actually deals 27 damage (18 damage increased by 50%). This significantly increases the total damage output from the sequence of plays.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            - **{SYNERGY_KEYWORD_CAPITALIZED} Effectiveness:**
            - Playing Card 2 first and applying Vulnerable means that Card 1's damage is increased by 50% due to the Vulnerable status. This is the kind of synergy one looks for in setting up a sequence of plays.
            - The combined damage of these plays is effectively 35 damage (8 from Card 2 and 27 from Card 1 under vulnerability effects), compared to 26 damage (8 + 18) if Vulnerable were not in place when Card 1 was played.

            ### Conclusion:
            This sequence creates a positive synergy due to the effective use of Vulnerable status to amplify damage from Card 1, making it a positive {SYNERGY_KEYWORD}.

            Final score:
            1\n'''),
            dedent(
            f'''---NEXT---
            # Case 3
            ### Card Descriptions and Effects:
            - **Card 1:**
            - Costs 4 energy initially but costs 1 less for each time you lose HP in combat.
            - Deals 18 damage.

            - **Card 3:**
            - Costs 0 energy.
            - Causes you to lose 3 HP but grants 2 energy.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:

            1. **Order of Play - Card 1, then Card 3:**
            - **Playing Card 1 First:**
                - Initially costs 4 energy and deals 18 damage.
                - Your current HP loss from playing Card 1 is irrelevant before playing Card 3.

            - **Playing Card 3 Next:**
                - You lose 3 HP, which potentially activates the effect of reducing Card 1's cost if played in future turns.
                - Gain 2 additional energy. However, since Card 1 has already been played, the immediate scenario doesn’t directly benefit from the extra energy unless it allows you to play other cards. 

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            - **{SYNERGY_KEYWORD_CAPITALIZED} Effectiveness:**
            - The play order implies no immediate synergy because any potential benefit from Card 3's effect on Card 1 is realized only in future plays of Card 1, provided it's repeatedly drawn in combat.
            - Card 3 grants more resources (energy) and theoretically allows for more plays, but for the immediate sequence of Card 1 then Card 3, there are no direct efficiency gains or additional effects.

            ### Conclusion:
            Since the described order doesn't produce an immediate advantageous or disadvantageous effect, considering the given conditions, there is no {SYNERGY_KEYWORD} in the sequence where Card 1 is played before Card 3.

            Final score:
            0\n'''),
            dedent(
            f'''---NEXT---
            # Case 4
            ### Card Descriptions and Effects:
            - **Card 3:**
            - Costs 0 energy.
            - Causes you to lose 3 HP and grants 2 energy.

            - **Card 1:**
            - Costs 4 energy initially but costs 1 less for each time you lose HP in combat.
            - Deals 18 damage.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:

            1. **Order of Play - Card 3, then Card 1:**
            - **Playing Card 3 First:**
                - You lose 3 HP, activating the cost reduction mechanic of Card 1.
                - You also gain 2 additional energy, increasing your resource pool for the current turn.
            
            - **Playing Card 1 Next:**
                - The cost of Card 1 is now reduced by 1 due to the HP loss from Card 3.
                - This lets you save 1 energy, which can be used to play additional cards during your turn.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            - **{SYNERGY_KEYWORD_CAPITALIZED} Effectiveness:**
            - Playing Card 3 first directly synergizes with Card 1 by reducing Card 1’s cost through the HP loss mechanic.
            - The extra energy provided is not part of the {SYNERGY_KEYWORD} effect, since it is not part of the interaction between the two cards.

            ### Conclusion:
            The play order of Card 3 followed by Card 1 results in a positive {SYNERGY_KEYWORD} due to the immediate cost reduction, which optimizes your energy usage and potentially broadens your strategic options for the rest of the turn.

            Final score:
            1\n'''),
            dedent(
            f'''---NEXT---
            # Case 5
            ### Card Descriptions and Effects:
            - **Card 2:**
            - Costs 2 energy.
            - Deals 8 damage and applies 2 Vulnerable (causing the target to take 50% more damage from subsequent Attack cards for 2 turns).

            - **Card 3:**
            - Costs 0 energy.
            - Causes you to lose 3 HP and grants 2 energy.

            ### Analyzing the {SYNERGY_KEYWORD_CAPITALIZED}:

            1. **Order of Play - Card 2, then Card 3:**
            - **Playing Card 2 First:**
                - You spend 4 energy to deal 8 damage and apply 2 Vulnerable to an enemy.
            
            - **Playing Card 3 Next:**
                - Since Card 2 has already used up most of your energy, the additional 2 energy from Card 3 would allow you to regain some resource availability for additional plays in the same turn.
                - The 3 HP loss from Card 3 does not directly interact with Card 2 because Vulnerable affects damage taken, not energy or HP mechanics.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            - **{SYNERGY_KEYWORD_CAPITALIZED} Effectiveness:**
            - Playing Card 2 after Card 3 allows for potential further plays due to the energy burst from Card 3. However, there is no direct synergy between the cards' effects themselves.
            - Card 3 provides additional energy but playing it after Card 2 just restores some energy spent, which is useful for continuing the turn with more plays but not a synergistic {SYNERGY_KEYWORD} specific to these two cards' interactions.

            ### Conclusion:
            The sequence offers no notable synergistic interaction beyond regaining energy to play more cards. While this order may allow for greater flexibility in a turn by reopening energy options, nothing about the cards’ effects inherently enhances or diminishes the other's utility.

            Final score:
            0\n'''),
            dedent(
            f'''---NEXT---
            # Case 6
            ### Card Descriptions and Effects:
            - **Card 4:**
            - Costs 1 energy.
            - Gains 7 Block.
            - Exhausts a random card from your hand.

            - **Card 2:**
            - Costs 2 energy.
            - Deals 8 damage and applies 2 Vulnerable.

            ### New {SYNERGY_KEYWORD_CAPITALIZED} Analysis:

            1. **Order of Play - Card 4, then Card 2:**
            - Playing Card 4 confers 7 Block and exhausts a random card. This can impact any card, but it’s important to note this does not specifically interact with Card 2’s mechanism or effects.
            - After playing Card 4, if Card 2 is still in hand, you can play Card 2 normally, dealing 8 damage and applying 2 Vulnerable.

            ### Conclusion:
            Given that the risk of losing a card to exhaustion from Card 4 is an inherent risk not specific to Card 2, the sequence doesn't introduce any unique advantages or disadvantages specifically related to Card 2 beyond the inherent exhausting mechanic. Thus, there is no direct {SYNERGY_KEYWORD} effect due to the specific ordering of these cards.

            Final score:
            0\n'''),
            dedent(
            f'''---NEXT---
            # Case 7
            ### Card Descriptions and Effects:
            - **Card 4:**
            - Costs 1 energy.
            - Gains 7 Block.
            - Exhausts a random card from your hand.

            - **Card 1:**
            - Costs 4 energy initially but costs 1 less for each time you lose HP in combat.
            - Deals 18 damage.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:

            1. **Order of Play - Card 4, then Card 1:**
            - **Playing Card 4 First:**
                - You gain 7 Block to protect against incoming damage, which is generally positive.       
                - A random card from your hand is exhausted. This is a risk inherent to Card 4 but doesn't specifically impact Card 1 more than any other card.

            - **Playing Card 1 Next:**
                - Gaining Block reduces the potential to take damage this turn, which could have reduced Card 1’s energy cost if the player would have taken HP loss.
                - Although gaining Block is beneficial for immediate protection, it indirectly reduces the possibility of taking advantage of Card 1’s cost reduction mechanic.

            ### Conclusion:
            Considering both the subtle negative synergy between gaining Block and potentially reducing Card 1's cost, the sequence can be considered a slight negative {SYNERGY_KEYWORD} due to the fact that playing Card 4 first may inadvertently result in a less optimal use of resources for playing Card 1.

            Final score:
            -1\n'''),
            dedent(
            f'''---NEXT---
            # Case 8
            ### Card Descriptions and Effects:
            - **Card 4:**
            - Costs 1 energy.
            - Gains 7 Block.
            - Exhausts a random card from your hand.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:

            1. **Order of Play - Card 4, then another Card 4:**
            - **First Card 4:**
                - Provides 7 Block for protection.
                - Exhausts a random card from your hand as a part of its fundamental effect.

            - **Second Card 4:**
                - Adds another 7 Block, further boosting your defense.
                - Again exhausts a random card, removing another card from your hand.

            ### {SYNERGY_KEYWORD_CAPITALIZED} Analysis:
            - **{SYNERGY_KEYWORD_CAPITALIZED} Effectiveness:**
            - The primary effect of playing two Card 4s is the accumulation of a substantial 14 Block.   
            - The repeated card exhaustion could limit your strategic options, but it's not specific to the combination itself.
            - There’s no direct synergy or additional interplay between the two instances of Card 4 beyond their individual effects stacking.

            ### Conclusion:
            The sequential play of two Card 4s results in stacking of Block, a straightforward cumulative effect that does not introduce new positive or negative synergy beyond the individual card effects. As such, there isn't a net new {SYNERGY_KEYWORD} effect present.

            Final score:
            0\n''')]
        responses.append(''.join(case_responses[:shot_count]))
        next_card_number = cards_needed[shot_count-1] + 1
    else:
        raise Exception("Ask Type unrecognised")
    return prompts, responses, next_card_number

def get_sts_prompts(ask_type: AskType, shot_count=None):
    system_message = "You are a game designer who is an expert in understanding card design in card games such as magic the gathering or hearthstone. There is a new card game and we want to know your opinion on some of the card designs in this game."
    prompts, responses = get_sts_definitions()
    p, r = get_sts_ask(ask_type=ask_type)
    prompts.append(p)
    responses.append(r)
    ps, rs, next_card_number = get_few_shot_examples(ask_type=ask_type, shot_count=shot_count)
    prompts += ps
    responses += rs
    return system_message, prompts, responses, next_card_number

def get_single_card_ask(card1, card2, id1, id2, starting_card_number):
    card1_type = card1['Type']
    card1_cost = card1['Cost']
    card1_desc = card1['Description']
    card2_type = card2['Type']
    card2_cost = card2['Cost']
    card2_desc = card2['Description']
    if id1 == id2:
        # Nice job! Remember, we are only considering synergies between the two cards we're looking at. It doesn't matter if the cards provide some positive or negative effect to other future cards played.
        prompt = dedent(f'''Nice job! Let's say card {starting_card_number} is defined as:
        Card {starting_card_number} ({card1_type} Type) - Cost {card1_cost}: {card1_desc}
        Let's say we have at least two of this card in our deck.
        What is the {SYNERGY_KEYWORD} effect of playing card {starting_card_number}, then another one of card {starting_card_number} again?\n''')
    else:
        prompt = dedent(f'''Nice job! Let's say we have:
        Card {starting_card_number} ({card1_type} Type) - Cost {card1_cost}: {card1_desc}
        Card {starting_card_number + 1} ({card2_type} Type) - Cost {card2_cost}: {card2_desc}
        What is the {SYNERGY_KEYWORD} effect of playing card {starting_card_number}, then card {starting_card_number + 1}?\n''')
    return prompt, (id1, id2)

def get_multi_card_multi_ask(cards_x, cards_y, x_indices, y_indices, starting_card_number: int):
    card_def = {}
    prompts = []
    ids = []
    for card_x, x in zip(cards_x, x_indices):
        for card_y, y in zip(cards_y, y_indices):
            prompt = ""
            if card_def.get(x, None) is None or card_def.get(y, None) is None:
                prompt += "Let's say we have:\n"
                if card_def.get(x, None) is None:
                    prompt += f"Card {starting_card_number} ({card_x['Type']} Type) - Cost {card_x['Cost']}: {card_x['Description']}\n"
                    card_def[x] = starting_card_number
                    starting_card_number += 1
                if card_def.get(y, None) is None:
                    prompt += f"Card {starting_card_number} ({card_y['Type']} Type) - Cost {card_y['Cost']}: {card_y['Description']}\n"
                    card_def[y] = starting_card_number
                    starting_card_number += 1
            if x == y:
                prompt += f"What is the {SYNERGY_KEYWORD} effect of playing card {card_def[x]}, then another one of card {card_def[x]} again?\n"
            else:
                prompt += f"What is the {SYNERGY_KEYWORD} effect of playing card {card_def[x]}, then card {card_def[y]}?"
            prompts.append(prompt)
            ids.append((x, y))
    return prompts, ids

def get_multi_card_bundle_ask(cards_x, cards_y, x_indices, y_indices, starting_card_number: int):
    prompt = "Let's say we have:\nCards:\n"
    ids = []
    card_def = {}
    def add_to_prompt(card, ind, prompt, card_def, starting_card_number):
        if card_def.get(ind, None) is None:
            prompt += f'''Card {starting_card_number} ({card['Type']} Type) - Cost {card['Cost']}: "{card['Description']}"\n'''
            card_def[ind] = starting_card_number
            starting_card_number += 1
        return prompt, starting_card_number
    for card, ind in zip(cards_x, x_indices):
        prompt, starting_card_number = add_to_prompt(card, ind, prompt, card_def, starting_card_number)
    for card, ind in zip(cards_y, y_indices):
        prompt, starting_card_number = add_to_prompt(card, ind, prompt, card_def, starting_card_number)
    question_counter = 1
    prompt += "Cases:\n"
    for x in x_indices:
        for y in y_indices:
            if x == y:
                prompt += f"{question_counter}. What is the {SYNERGY_KEYWORD} effect of playing card {card_def[x]}, then another one of card {card_def[x]} again?\n"
            else:
                prompt += f"{question_counter}. What is the {SYNERGY_KEYWORD} effect of playing card {card_def[x]}, then card {card_def[y]}?\n"
            question_counter += 1
            ids.append((x, y))
    return prompt, ids