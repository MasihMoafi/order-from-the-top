## Games

### Chapter 1 — Ten Tales of Strategy

1. **Pick a Number (Authors vs. Reader & Steve Ballmer's Random-Number Interview Game)**
   - **Heading & First Line**: `"#1. PICK A NUMBER"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L364-L441)) — `"Believe it or not, we are going to ask you to play a game against us."`
   - **Players, Moves, Timing**: 2 players (chooser/authors vs. guesser/reader; also Microsoft CEO Steve Ballmer vs. job candidate). Chooser secretly picks an integer from 1 to 100; guesser makes up to 5 sequential guesses with `"Higher"` or `"Lower"` feedback. Sequential.
   - **Payoffs**: Guesser receives $100 (1st guess), $80 (2nd), $60 (3rd), $40 (4th), $20 (5th), or $0 (>5 guesses); chooser pays out that amount.
   - **Family**: `zero-sum mixing` / `other` (level-$k$ hide-and-seek).
   - **Best Move / Real People**: Against a random number, bisecting the remaining interval (`50, 25, 37, 42, 46...` — `"divide the set in two and conquer"`) is optimal. Real guessers follow bisection (`50, 25, 37, 42`) and then jump to `49`. Anticipating this, the authors hint at `49` and pick `48` (`"How many of you got 48 in five tries? Not many, we bet."`).
   - **THE RULE THAT CHANGES THE BEST MOVE**: Whether the number is chosen mechanically at random vs. by a strategic opponent who pays out the prize: `"When guessing a number picked at random, the number isn’t trying to hide."` vs. `"we’d rather keep the money than give it to you."`
   - **Catastrophic Loss?**: No.

2. **Winning by Losing: *Survivor* Final Three Immunity Challenge (plus "Trip to the Gym" Aside)**
   - **Heading & First Line**: `"#2. WINNING BY LOSING"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L443-L516)) — `"We admit it: we watched Survivor."` (Trip to the Gym aside at l. 496: `"Notice the 'Trip to the Gym' icon next to the text."`)
   - **Players, Moves, Timing**: 3 contestants (Richard Hatch, Rudy Boesch, Kelly Wiglesworth) plus a jury of ousted contestants. Moves: Hold onto the immunity idol on a pole or step down ("throw the game"); challenge winner chooses which of the other two advances to the final two; jury votes for the $1M winner. Sequential.
   - **Payoffs**: $1,000,000 to the final winner (`"This was a zero-sum game with a single prize of $1,000,000"`). Rudy beats either Richard or Kelly in a jury vote; if Richard wins immunity and eliminates ally Rudy, Rudy's friends punish Richard and vote for Kelly; if Kelly wins immunity, she eliminates Rudy and loses the jury vote to Richard.
   - **Family**: `other` (3-player sequential elimination / strategic losing) and `voting`.
   - **Best Move / Real People**: Richard's best move is to purposefully lose (`"throwing the game"`). Real people: After 2.5 hours, Richard stepped off the pole for a slice of orange; Kelly outlasted Rudy after 4 hours 11 minutes, eliminated Rudy, and Richard won the $1,000,000 jury vote with Rudy's support. (In the `"Trip to the Gym"` aside, l. 496–512: if Kelly might fall early, Richard could wait until one rival falls, unless Kelly reasons the same way).
   - **THE RULE THAT CHANGES THE BEST MOVE**: The jury vote by ousted contestants combined with Richard's alliance with Rudy: `"the ousted contestants vote to determine the final winner"` and `"Should Richard win the final competition and use his power to eliminate Rudy, it could look like a stab in the back."`
   - **Catastrophic Loss?**: Yes — elimination from the $1,000,000 contest (`"use his power to eliminate Rudy"`).

3. **The Hot Hand (NBA Defense Allocation, 1986 World Cup Maradona, LeBron James, Tennis Strokes)**
   - **Heading & First Line**: `"#3. THE HOT HAND"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L518-L585)) — `"Do athletes ever have a 'hot hand'?"`
   - **Players, Moves, Timing**: 2 players or 2 teams of $N$ players (Philadelphia 76ers/Andrew Toney vs. defense; Diego Maradona vs. West Germany in 1986 World Cup; LeBron James left-handed vs. right-handed drives; tennis player forehand vs. backhand). Moves: Offense allocates shots/passes or left/right/forehand/backhand; defense allocates guarding. Simultaneous / repeated.
   - **Payoffs**: Scoring rate / match victory (qualitative; statistical study of 76ers showed a shooter's individual hit rate actually fell right after making a basket).
   - **Family**: `zero-sum mixing`.
   - **Best Move / Real People**: Defense shifts extra coverage onto the "hot" star or stronger stroke; star passes to unguarded teammates (`"Maradona didn’t score a single goal in the final, yet Argentina won 3–2 because his unguarded teammates, Jorge Burruchaga and Jorge Valdano, scored"`).
   - **THE RULE THAT CHANGES THE BEST MOVE**: Improving the weaker stroke/hand forces the defense to guard it honestly, raising the payoff and frequency of the stronger stroke: `"As your two strokes become more equal, opponents can no longer exploit your weak backhand. This frees you up to use your preferred forehand even more often."`
   - **Catastrophic Loss?**: No.

4. **To Lead or Not to Lead (1983 America's Cup *Liberty* vs. *Australia II*, Economic Forecasters, Business Imitation)**
   - **Heading & First Line**: `"#4. TO LEAD OR NOT TO LEAD"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L587-L630)) — `"After the first four races in the 1983 America’s Cup finals, Dennis Conner’s Liberty led 3–1 in a best-of-seven series."`
   - **Players, Moves, Timing**: 2 boats (Dennis Conner's *Liberty* vs. John Bertrand's *Australia II*); or $N$ economic forecasters / firms (Dell vs. Gateway; P&G vs. upstarts). Moves: Trailing player chooses a tack/forecast/innovation; leader chooses whether to copy/cover (`"monkey see, monkey do"`) or go its own way. Sequential.
   - **Payoffs**: Winner-take-all race/series (*Liberty* led by 37 seconds at start of Race 5; *Australia II* tacked left, wind shifted 5 degrees, *Australia II* won by 1 minute 47 seconds and won the Cup).
   - **Family**: `other` (leader-follower sequential covering vs. risk-taking).
   - **Best Move / Real People**: In a 2-player winner-take-all contest, the leader should copy the trailer (`"When you are ahead, a monkey-see, monkey-do strategy preserves your lead"`). Dennis Conner failed to cover *Australia II* and lost. In economic forecasting, consensus leaders stay safe in the middle while newcomers bet on boom or doom.
   - **THE RULE THAT CHANGES THE BEST MOVE**:
     1. Winner-take-all vs. non-winner-take-all payoff structure: `"because, unlike in sports, the competition is usually not winner-take-all"` (in business, leaders wait to see if an upstart's innovation succeeds before copying).
     2. Two competitors vs. more than two competitors (fn l. 13902): `"This strategy no longer applies once there are more than two competitors."`
   - **Catastrophic Loss?**: Yes, for trailing forecasters who gamble on extreme predictions: `"Usually they are wrong and are never heard of again."`

5. **Here I Stand (Intransigent Bargaining: Martin Luther, Charles de Gaulle, Ferdinand de Lesseps)**
   - **Heading & First Line**: `"#5. HERE I STAND"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L632-L688)) — `"When the Catholic Church demanded that Martin Luther repudiate his attack on the authority of popes and councils, he refused to recant"`
   - **Players, Moves, Timing**: 2 or $N$ (Martin Luther vs. Catholic Church; Charles de Gaulle vs. Roosevelt/Churchill and EEC partners; Ferdinand de Lesseps vs. nature/investors in Suez and Panama). Moves: Commit to an unyielding position (`"Ich kann nicht anders"`) vs. compromise; counterpart concedes or breaks off. Sequential.
   - **Payoffs**: Division of political/bargaining surplus (e.g., de Gaulle vetoed British EEC entry in 1963 and 1968 and got his way).
   - **Family**: `bargaining` / `brinkmanship`.
   - **Best Move / Real People**: Credible inflexibility forces the other side into a take-it-or-leave-it choice; de Gaulle succeeded repeatedly, whereas de Lesseps refused to adapt to Panama's terrain and failed catastrophically.
   - **THE RULE THAT CHANGES THE BEST MOVE**: One-shot vs. repeated bargaining reputation: `"A compromise in the short term may prove a better strategy over the long haul"` because `"If you grab too big a share of the pie TODAY, people may decide not to bake anything with you TOMORROW."`
   - **Catastrophic Loss?**: Yes — `"The danger is that an inflexible person does not know when to compromise and may allow small losses to grow into major disasters"` (e.g., de Lesseps's ruin in the Panama Canal and EEC breakup risk).

6. **Thinning Strategically (ABC *Primetime* Bikini Diet Game, Bridgeport Bluefish Sequel, Odysseus, Xenophon, Cortés)**
   - **Heading & First Line**: `"#6. THINNING STRATEGICALLY"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L690-L781); also Ch. 6 [l. 5216](file:///home/masih/Work/tries/aos/book-full.txt#L5216-L5244) & Ch. 7 [l. 6153](file:///home/masih/Work/tries/aos/book-full.txt#L6153-L6190)) — `"Cindy Nacson-Schechter wanted to lose weight."`
   - **Players, Moves, Timing**: 2 selves (Present Self vs. Future Self) plus external enforcer (ABC *Primetime*, Ray's wife, Bridgeport Bluefish minor-league team); military parallels (Odysseus vs. Sirens, Xenophon vs. Persians, Hernán Cortés vs. Aztecs). Moves: Present self signs contract / burns ships / poses in bikini; future self diets (loses 15 lbs in 2 months) or overeats / fights or retreats. Sequential.
   - **Payoffs**: Lose 15 lbs -> bikini photos destroyed (in Ch. 6 game tree at l. 5347 `table not in text` and game table at l. 5379 `table not in text`, prose gives exact rankings 1–4 for Night Self and Morning Self: Night Self ranks `[No contract & Diet]=4, [Contract & Diet]=3, [No contract & No diet]=2, [Contract & No diet]=1`; Morning Self without contract prefers `No diet` over `Diet`, but with contract prefers `Diet [Lose 15 lbs]` over `No diet [National embarrassment]`). Real people: Cindy lost 17 lbs, Ray lost 22 lbs, Laurie lost 28 lbs; a 4th participant lost 13 lbs and was spared; in the Bridgeport Bluefish sequel (Ch. 7 l. 6168), 4 of 5 succeeded and the 5th threatened a lawsuit so ABC/team backed down.
   - **Family**: `other` (commitment / multi-self sequential game).
   - **Best Move / Real People**: Commit present self via an irrevocable penalty on future failure (`"burn his own ships"`).
   - **THE RULE THAT CHANGES THE BEST MOVE**: Whether the penalty contract is legally and socially enforceable without renegotiation: `"The woman wasn’t bluffing in her threat of a lawsuit, and so ABC and the team backed down"` (l. 6182), which destroys the commitment's credibility.
   - **Catastrophic Loss?**: Yes — in Cortés's parallel, `"The Spaniards now had no choice: they must either defeat the Aztecs or perish trying"` (l. 766); for Ray, `"he would lose the weight or his wife"` (l. 741).

7. **Buffett's Dilemma (Campaign Finance Reform, Capote's *In Cold Blood*, Aesop's Belling the Cat, Khrushchev's Heckler)**
   - **Heading & First Line**: `"#7. BUFFETT’S DILEMMA"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L783-L877)) — `"In an op-ed promoting campaign finance reform, the Oracle of Omaha, Warren Buffett, proposed a wildly creative strategic solution"`
   - **Players, Moves, Timing**: 2 political parties (Democrats and Republicans in Congress, plus Eccentric Billionaire E.B.); or 2 murder suspects (Dick Hickock and Perry Smith in *In Cold Blood*); or $N$ mice / Soviet citizens in Khrushchev's audience. Moves: Vote for vs. against campaign finance reform (or Confess vs. Remain silent; or Bell the cat / Speak out against Stalin vs. Keep silent). Simultaneous.
   - **Payoffs**: In Buffett's game, if the bill passes, E.B. pays $0; if defeated, E.B. donates $1 billion to whichever party delivered the most votes for passage. In *In Cold Blood*, confessing alone gets leniency while the silent partner faces the death penalty; both confessing leads to execution for both (fn l. 13916).
   - **Family**: `prisoners' dilemma`.
   - **Best Move / Real People**: Voting for the bill (or confessing in *In Cold Blood*, or staying silent in Belling the Cat / Stalin's terror) is the dominant strategy for each player. Real people: Dick and Perry both confessed and were executed; Congress never had to face E.B. because McCain-Feingold passed without it.
   - **THE RULE THAT CHANGES THE BEST MOVE**: Contingent $1 billion reward paid only if the bill fails to the party casting more votes for it: `"If the bill was defeated, this person—the E.B.—would donate $1 billion (yes, $1 billion) to the political party that had delivered the most votes in the bill’s favor."`
   - **Catastrophic Loss?**: Yes — execution in *In Cold Blood* (`"both were sentenced to death"`, fn l. 13916), losing a political party's viability if the rival gets $1 billion, or `"a broken nose or possibly his life"` for standing up to a tyrant (l. 868).

8. **Mix Your Plays (Takashi Hashiyama's Sotheby's vs. Christie's Rock-Paper-Scissors & Procurement Auction Alternative)**
   - **Heading & First Line**: `"#8. MIX YOUR PLAYS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L879-L958)) — `"Apparently Takashi Hashiyama has trouble making decisions."`
   - **Players, Moves, Timing**: 2 auction houses (Sotheby's and Christie's) plus seller Takashi Hashiyama. Moves: Rock, Paper, Scissors (simultaneous one-shot).
   - **Payoffs**: Winner auctions $18 million Maspro Denkoh art collection, earning ~$3 million commission (20% on first $800k, 12% above that) minus a small breakup fee to the loser.
   - **Family**: `zero-sum mixing` (and `auction` in the authors' redesign).
   - **Best Move / Real People**: Equilibrium is $1/3, 1/3, 1/3$ random mix; against an opponent following beginner psychology (`"When people don’t know what to do, they start with scissors"`), play Rock. Real people: Christie's consulted 11-year-old twins Alice and Flora and played Scissors; Sotheby's guessed Paper at random; Christie's won.
   - **THE RULE THAT CHANGES THE BEST MOVE**: Replacing RPS with a competitive procurement auction over the commission rate: `"Instead of letting the two contestants effectively agree to split the commission, he could have run his own auction. Ask each house carefully to state the lowest commission they would have taken in order to still turn a profit."`
   - **Catastrophic Loss?**: No.

9. **Never Give a Sucker an Even Bet (Sky Masterson & Nathan Detroit, Chicago Futures Speculators, Lindgren vs. Negreanu Poker)**
   - **Heading & First Line**: `"#9. NEVER GIVE A SUCKER AN EVEN BET"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L960-L1052)) — `"In Guys and Dolls, gambler Sky Masterson relates this valuable advice from his father"`
   - **Players, Moves, Timing**: 2 players (Nathan Detroit vs. Sky Masterson; informed trader vs. speculator on Chicago Board of Exchange; Erick Lindgren vs. Daniel Negreanu in televised poker). Moves: Offer/accept bet on whether Mindy's sold more strudel or cheesecake (or bow-tie color in fn l. 13920); or in poker, Negreanu raises $200k (putting $270k in pot with $200k behind), Lindgren moves all-in, Negreanu calls or folds within 90 seconds. Sequential.
   - **Payoffs**: Zero-sum bet ($1,000 in *Guys and Dolls*; $470k+ pot in poker).
   - **Family**: `signalling` / `zero-sum mixing` / `auction` (winner's curse).
   - **Best Move / Real People**: Refuse a private-information bet (`"Just remembering that the person offering the bet had an informational advantage was enough to suggest sitting on the sidelines"`). In poker, mix bluffs with strong hands so opponents cannot fold with certainty.
   - **THE RULE THAT CHANGES THE BEST MOVE**: Forcing the proposer to quote both sides and letting the uninformed party pick which side to take: `"let the less informed party pick which side of the bet to take"` (just as stock market makers must quote both buy and sell prices).
   - **Catastrophic Loss?**: Yes, in all-in tournament poker (`"Lindgren moves all in—wagering all he had... risk losing all his money"`).

10. **Game Theory Can Be Dangerous to Your Health (Jerusalem Taxi Bargaining)**
    - **Heading & First Line**: `"#10. GAME THEORY CAN BE DANGEROUS TO YOUR HEALTH"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L1054-L1162)) — `"Late one night, after a conference in Jerusalem, two American economists (actually, one of your authors and another economist) found a taxi"`
    - **Players, Moves, Timing**: 2 sides (economist passengers vs. Jerusalem taxi driver, with his new bride in the front seat). Moves: Bargain before ride vs. wait until arrival at hotel; driver demands 2,500 shekels ($2.75), Barry offers 2,200 shekels; driver accepts or locks doors and drives back to starting point. Sequential.
    - **Payoffs**: 2,500 vs. 2,200 shekels (~20 cents difference), plus driver's pride in front of his bride and 30 minutes of wasted driving/time.
    - **Family**: `bargaining`.
    - **Best Move / Real People**: Passengers waited until arrival so the trip was a sunk cost and offered 2,200; the insulted driver locked the doors, drove back at 80 mph to the origin, and threw them out; a second metered cab cost 2,200 shekels.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Exiting the cab *before* negotiating or accounting for the driver's audience/pride: `"If only he had begun to discuss the price after getting out of the taxi"` and `"Negotiate outside the bride’s earshot."`
    - **Catastrophic Loss?**: Near-catastrophic physical danger (`"turning off the headlights and driving at 80 miles per hour down narrow, winding streets"`).

11. **Case Study: Multiple Choice (Blind GMAT Question)**
    - **Heading & First Line**: `"CASE STUDY: MULTIPLE CHOICE"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L1164-L1228)) — `"We think almost everything in life is a game, even things that might not seem that way at first."`
    - **Players, Moves, Timing**: 2 players (GMAT test designer vs. test taker). Moves: Designer writes a geometry question and 5 choices `(a) 4π, (b) 8π, (c) 16, (d) 16π, (e) 32π sq. inches`; test taker picks one without seeing the question. Sequential.
    - **Payoffs**: Test taker wants a correct score; test maker wants right answers only from students who know the right formula ($\pi r^2$).
    - **Family**: `signalling` / `other` (strategic inference).
    - **Best Move / Real People**: Pick `(d) 16π sq. inches` (area of a circle of radius 4; if $r=2$ and the answer were $4\pi$, students using circumference $2\pi r$ would get it right for the wrong reason).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Test writer's constraint never to let a common mistake yield the right answer: `"It would be a terrible test question if the diameter were 4 and the right answer 4π. That would allow people who used the wrong formula, 2πr, to still get the right answer."`
    - **Catastrophic Loss?**: No.

---

### Chapter 2 — Games Solvable by Backward Reasoning

12. **It's Your Move, Charlie Brown (Lucy & the Football)**
    - **Heading & First Line**: `"IT’S YOUR MOVE, CHARLIE BROWN"` & `"Charlie Brown in Football and in Business"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L1242-L1372)) — `"In a recurring theme in the comic strip Peanuts, Lucy holds a football on the ground and invites Charlie Brown to run up and kick it."`
    - **Players, Moves, Timing**: 2 players (Charlie Brown, Lucy). Moves: Charlie accepts or declines; if Charlie runs up, Lucy lets him kick or pulls the ball away. Sequential.
    - **Payoffs**: Game tree at l. 1364 (`table not in text`); prose states Lucy's best outcome is Charlie falling flat on his back, and Charlie prefers declining over falling.
    - **Family**: `other` (sequential trust / backward induction).
    - **Best Move / Real People**: By backward induction, Charlie should reject Lucy's invitation; in the comic strip, Charlie accepts every year and falls.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Changing Lucy's payoff via a binding commitment or external penalty if she pulls the ball away.
    - **Catastrophic Loss?**: Physical fall/humiliation.

13. **Charlie Brown in Business (Charlie and Fredo in Freedonia / Trust Game)**
    - **Heading & First Line**: `"Charlie Brown in Football and in Business"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L1373-L1443)) — `"Imagine the following scenario. Charlie, now an adult, is vacationing in the newly reformed formerly Marxist country of Freedonia."`
    - **Players, Moves, Timing**: 2 players (Charlie, Fredo). Moves: Charlie invests $100,000 or does not invest; if he invests, the venture yields $500,000 and Fredo either honors the 50:50 split or absconds with all $500,000. Sequential.
    - **Payoffs**: Game tree at l. 1390 (`table not in text`), exact numbers in prose: Don't invest = ($0, $0); Invest & Honor = ($150,000 net profit to Charlie, $250,000 to Fredo); Invest & Abscond = (-$100,000 to Charlie, $500,000 to Fredo).
    - **Family**: `other` (sequential hold-up / trust game; sequential cousin of `prisoners' dilemma`).
    - **Best Move / Real People**: In a one-shot game under weak Freedonian law, Fredo absconds ($500k > $250k), so Charlie should not invest. In laboratory "trust game" experiments (fn 6, l. 13283), subjects show substantial trust and reciprocation.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Seizable U.S. assets, ongoing U.S. business, or a reputable intermediary: `"Perhaps he is engaged in many other enterprises that require financing from the United States or export goods to the United States"` so Charlie can attach assets or ruin his reputation.
    - **Catastrophic Loss?**: Yes — Charlie loses his entire $100,000 capital (`"leaves Charlie nursing a loss of $100,000"`).

14. **More Complex Trees: Presidential Line-Item Veto vs. Whole-Bill Veto**
    - **Heading & First Line**: `"More Complex Trees"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L1444-L1526)) — `"We turn to politics for an example of a slightly more complex game tree."`
    - **Players, Moves, Timing**: 2 players (Congress, President). Moves: Congress passes Package ($U$ = Urban renewal + $M$ = Antiballistic missile), $U$ alone, $M$ alone, or Nothing; President vetoes or signs (under standard rules, whole bill only; under line-item veto, can strike $U$ or $M$ separately). Sequential.
    - **Payoffs**: Preference table at l. 1467 and 2 trees at l. 1486 (`table not in text`), exact rankings in prose (4 = best, 1 = worst):
      - Congress: Only $U$ = 4, Both ($U+M$) = 3, Neither = 2, Only $M$ = 1.
      - President: Only $M$ = 4, Both ($U+M$) = 3, Neither = 2, Only $U$ = 1.
    - **Family**: `bargaining` / `voting` (sequential legislative game).
    - **Best Move / Real People**: Without line-item veto, Congress passes Package ($U+M$) and President signs -> payoff `(3, 3)`. With line-item veto, if Congress passes Package, President strikes $U$ and keeps Only $M$ -> `(1, 4)`; foreseeing this, Congress passes Nothing -> `(2, 2)`. Real-world evidence (fn 2, l. 13256): state governors with line-item vetoes do not achieve lower spending or deficits.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Granting the President a line-item veto: `"With the line-item veto, the outcome is that nothing passes; each side ends up with its second-worst outcome, ranked 2. Both are worse off than they were without the line-item veto!"`
    - **Catastrophic Loss?**: No.

15. **Strategies for "Survivors": The 21-Flags Game (Nim) & Trip to the Gym No. 1 (Hot-Potato 21-Flags)**
    - **Heading & First Line**: `"STRATEGIES FOR 'SURVIVORS'"` & `"TRIP TO THE GYM NO. 1"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L1528-L1610), Workout [l. 12978](file:///home/masih/Work/tries/aos/book-full.txt#L12978-L12994)) — `"CBS’s Survivor features many interesting games of strategy."`
    - **Players, Moves, Timing**: 2 tribes (Sook Jai and Chuay Gahn). Moves: Start with 21 flags; alternate removing 1, 2, or 3 flags per turn. In standard game, taking the last flag wins; in `"TRIP TO THE GYM NO. 1"` (l. 1606), `"instead of winning by taking the last flag, you win by forcing the other team to take the last flag"` (hot-potato / misère). Sequential.
    - **Payoffs**: Winning tribe gets immunity; losing tribe votes out one of its own members. Table of actual moves at l. 1595 (`table not in text`, partial moves in prose).
    - **Family**: `other` (finite sequential game of complete information / Nim).
    - **Best Move / Real People**: In standard 21-flags, first mover (Sook Jai) wins by taking 1 flag to leave 20, then always leaving multiples of 4 (`16, 12, 8, 4`). Real people: Sook Jai took 2 (leaving 19), later took 3 from 9 (leaving 6), and Chuay Gahn took 2 from 6 (leaving 4) and won. In Trip to the Gym No. 1 (hot potato), safe numbers left are `1, 5, 9, 13, 17, 21`, so starting at 21 is a losing position for the first mover!
    - **THE RULE THAT CHANGES THE BEST MOVE**:
      1. Winning by taking the last flag vs. forcing the opponent to take the last flag (`"instead of winning by taking the last flag, you win by forcing the other team to take the last flag"`, l. 1607, shifting target remainders from `4, 8, 12, 16, 20` to `1, 5, 9, 13, 17, 21`).
      2. Starting with 20 flags instead of 21 flags (fn l. 13928: `"Had the game started with 20 flags, a clean divisible-by-four number, Chuay Gahn should have been able to guarantee victory by moving second"`).
    - **Catastrophic Loss?**: Yes — `"The losing tribe had to vote out one of its own members"` (eliminated from $1M prize).

16. **Ultimatum Game, Reverse Ultimatum Game ("A Quick Trip to the Gym"), Dictator Game, Shame Dictator Game, and Testosterone Ultimatum Game**
    - **Heading & First Line**: `"Do People Actually Solve Games by Backward Reasoning?"`, `"A QUICK TRIP TO THE GYM: REVERSE ULTIMATUM GAME"`, `"IRRATIONALITY VERSUS OTHER-REGARDING RATIONALITY"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L1678-L1934)) — `"What seems to be the most damaging criticism comes from the ultimatum game."`
    - **Players, Moves, Timing**: 2 players (Proposer $A$, Responder $B$). Sequential.
      - *Standard Ultimatum*: Divide $100 (in whole dollars); $A$ makes a single offer, $B$ accepts or rejects (both get $0).
      - *Reverse Ultimatum (`"A QUICK TRIP TO THE GYM: REVERSE ULTIMATUM GAME"`, l. 1698)*: If $B$ rejects, $A$ can keep making strictly higher offers in $1 increments or stop (ending in $0, $0).
      - *Dictator Game (l. 1769)*: $A$ dictates split of $100; $B$ cannot reject.
      - *Dana-Cain-Dawes Silent-Exit Dictator Game (l. 1791)*: After $A$ divides $10, $A$ is offered $9 to exit silently so $B$ gets $0 and never learns a game occurred.
      - *Burnham Testosterone Ultimatum Game (l. 1913)*: $40 stake; proposer chooses only between `($25 to B, $15 to A)` or `($5 to B, $35 to A)`.
    - **Payoffs**: Dollar amounts as stated above.
    - **Family**: `bargaining`.
    - **Best Move / Real People**: Purely selfish backward induction predicts $A$ offers $1 in Standard Ultimatum, $0 in Dictator, and $B$ holds out for $99 in Reverse Ultimatum (since at 98:2 $A$ prefers 99:1 over $0). Real people: In Standard Ultimatum, average offer is 40–50% (mode 50:50), offers below 20% rejected ~50% of the time (Machiguenga of Peru averaged 26% with almost no rejections; two gift-giving cultures offered >50%). In Reverse Ultimatum, holding out for 99:1 fails because $A$ quits early. In Dictator, people give less than Ultimatum (and 10% less when proposer role is earned via trivia test); in Dana-Cain-Dawes, most take the silent $9; in Burnham's game, 6 of 26 rejected $5 and had 50% higher salivary testosterone.
    - **THE RULE THAT CHANGES THE BEST MOVE**:
      - Responder's veto right (Ultimatum vs. Dictator: `"any positive allocation must come purely from generosity, not from the fear of rejection"`).
      - Allowing Proposer to make repeated higher offers after a rejection (`"If B rejects A’s offer, then A gets to choose whether to make a more generous offer or to stop the game"`, l. 1702, flipping bargaining power to $B$).
      - Silent exit where Responder never knows of the game (`"the other person never finds out that you were playing this game"`, l. 1795).
    - **Catastrophic Loss?**: No (destruction of the whole prize upon rejection).

17. **Chess (Human vs. Computer: Kasparov vs. Fritz X3D, Hydra vs. Adams)**
    - **Heading & First Line**: `"VERY COMPLEX TREES"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L1936-L2041)) — `"When you have acquired a little experience with backward reasoning, the method looks pretty straightforward"`
    - **Players, Moves, Timing**: 2 players (White, Black). Alternating sequential moves (~$10^{120}$ possible game paths).
    - **Payoffs**: Win, Lose, Draw (2003 Kasparov vs. Fritz X3D: 1 win each, 2 draws; 2005 Hydra vs. Michael Adams: 5 wins, 1 draw).
    - **Family**: `other` (finite sequential zero-sum game).
    - **Best Move / Real People**: Prune tree using forward look-ahead plus positional evaluation function.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Threefold repetition draw rule: `"The rule that the game is a draw if the same position is repeated ensures that the game ends within a finite total number of moves."`
    - **Catastrophic Loss?**: Checkmate (loss of game).

18. **Case Study: The Tale of Tom Osborne and the '84 Orange Bowl**
    - **Heading & First Line**: `"CASE STUDY: THE TALE OF TOM OSBORNE AND THE ’84 ORANGE BOWL"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2043-L2120)) — `"In the 1984 Orange Bowl the undefeated Nebraska Cornhuskers and the once-beaten Miami Hurricanes faced off."`
    - **Players, Moves, Timing**: 2 football teams (Nebraska coached by Tom Osborne vs. Miami). Moves: Trailing 31–17 in 4th quarter, after scoring first touchdown (31–23), choose 1-point kick (~95% success) or 2-point conversion (~45% success); after scoring second touchdown, choose 1-point or 2-point conversion. Sequential.
    - **Payoffs**: #1 National Championship title (Nebraska wins #1 outright with a victory, or with a tie *if* they first tried to win and fell short; losing forfeits #1 to Miami).
    - **Family**: `other` (sequential risk-timing game).
    - **Best Move / Real People**: Go for 2 points after the *first* touchdown (if it succeeds -> 31–25, then a 1-point kick on the second TD wins 32–31; if it fails -> 31–23, go for 2 points on the second TD to tie 31–31 and still claim the championship). Real people: Osborne kicked 1 point on the first TD (31–24), then went for 2 points on the final TD (at 31–30), missed, and lost both game and title.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Taking the risky conversion on the first touchdown rather than the second so information arrives while a backup option remains: `"if you have to take some risks, it is often better to do so as quickly as possible."`
    - **Catastrophic Loss?**: Loss of national championship.

---

### Chapter 3 — Prisoners' Dilemmas and How to Resolve Them

19. **Four Opening Dilemmas: Gas Station Price War (Nexon vs. Lunaco), Centrist Campaign Platforms, New England Fisheries Collapse, *Catch-22* (Yossarian)**
    - **Heading & First Line**: `"MANY CONTEXTS, ONE CONCEPT"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2129-L2163)) — `"What do the following situations have in common?"`
    - **Players, Moves, Timing**: 2 players (Nexon vs. Lunaco; two presidential candidates) or $N$ players (New England fishermen; WWII soldiers like Yossarian in *Catch-22*). Moves: Keep price high vs. cut price; appeal to party base vs. move to center; limit catch vs. overfish; face combat risk vs. shirk duty. Simultaneous.
    - **Payoffs**: Qualitative (each player's dominant strategy leaves everyone worse off).
    - **Family**: `prisoners' dilemma` / `commons`.
    - **Best Move / Real People**: Defection is dominant in one-shot play.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Enforceable collective agreement or military/regulatory coercion (`"Catch-22"`).
    - **Catastrophic Loss?**: Yes — commercial extinction of New England fish species (`"Total catch hinges on the brink of commercial extinction"`) and death in combat for Yossarian (`"Yossarian doesn’t want to risk his life"`).

20. **Rainbow's End (RE) vs. B. B. Lean (BB) Mail-Order Shirt Pricing Game (and Chapters 3, 4, 6 & Workouts Variants)**
    - **Heading & First Line**: `"A Visual Representation"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2209-L2345)); `"Repetition"` ([l. 2751](file:///home/masih/Work/tries/aos/book-full.txt#L2751-L2875)); Ch. 4 `"SQUARING THE CIRCLE"` ([l. 3261](file:///home/masih/Work/tries/aos/book-full.txt#L3261-L3374)), `"TRIP TO THE GYM NO. 2"` ([l. 3284](file:///home/masih/Work/tries/aos/book-full.txt#L3284-L3353), Workout [l. 12996](file:///home/masih/Work/tries/aos/book-full.txt#L12996-L13033)), `"TRIP TO THE GYM NO. 3"` ([l. 3354](file:///home/masih/Work/tries/aos/book-full.txt#L3354-L3374), Workout [l. 13034](file:///home/masih/Work/tries/aos/book-full.txt#L13034-L13053)), `"APPENDICES TO CHAPTER 4"` ([l. 3743](file:///home/masih/Work/tries/aos/book-full.txt#L3743-L4021)); Ch. 6 `"THREATS AND PROMISES"` ([l. 5440](file:///home/masih/Work/tries/aos/book-full.txt#L5440-L5637)) — `"We will develop the method for displaying and solving the game using a business example."`
    - **Players, Moves, Timing**: 2 catalog firms (Rainbow's End [RE] and B. B. Lean [BB]). Simultaneous (or repeated annually, or sequential with pregame strategic commitments in Ch. 6).
    - **Payoffs**: Demand formula (l. 3832 & 13004): $Q_{\text{RE}} = 2800 - 100 P_{\text{RE}} + 80 P_{\text{BB}}$, unit cost = $20 (or $11.60 for RE in Trip to the Gym No. 3). Payoff tables at l. 2264, 3278, 3747, 3792, 5442, 5480, 5519, 13018, 13028, 13039, 13043 are images (`table not in text`), with exact numbers given in prose:
      - *Ch. 3 2x2 PD ($80 vs. $70)*: `($80, $80) = ($72,000, $72,000)` (1,200 shirts each; joint maximum); `($70, $80) = ($110,000, $24,000)` (2,200 vs. 400 shirts); `($80, $70) = ($24,000, $110,000)`; `($70, $70) = ($70,000, $70,000)` (1,400 shirts each).
      - *Ch. 4 5x5 ($42, $41, $40, $39, $38) & Continuous Price Equilibrium*: Best-response rule is $P_{\text{BB}} = 24 + 0.4 P_{\text{RE}}$. At `($42, $42)` profit is `$43,120` each; cutting from `$42` to `$41` against `$42..$38` raises profit (`$43,120 -> $43,260; $41,360 -> $41,580; $39,600 -> $39,900; $37,840 -> $38,220; $36,080 -> $36,540`); at `($40, $42)` profit is `$43,200` for `$40` and `$35,200` for `$42`; iterated elimination of dominated prices (`$42, $38`, then `$41, $39`) leaves unique Nash equilibrium `($40, $40)` with `$40,000` profit each.
      - *Trip to the Gym No. 3 (Asymmetric Cost, l. 3354 & 13034)*: When RE's unit cost falls from `$20` to `$11.60`, the new Nash equilibrium is `P_RE = $35` (profit `$54,756`) and `P_BB = $38` (profit `$32,400`).
      - *Ch. 6 Compellence / Deterrence ($80 vs. $40, l. 5440)*: `($80, $80) = ($72k, $72k)`, `($40, $80) = ($140k, $0)`, `($80, $40) = ($0, $140k)`, `($40, $40) = ($40k, $40k)`.
    - **Family**: `prisoners' dilemma` / `other` (Bertrand differentiated price competition).
    - **Best Move / Real People**: In one-shot play without commitments, `$70` dominates `$80` in the 2x2 game, and `($40, $40)` is the unique Nash equilibrium in the unrestricted game.
    - **THE RULE THAT CHANGES THE BEST MOVE**:
      1. Annual repetition with discount/interest rate below $2,000 / $38,000 = 5.26\%$: `"At an interest rate of 5 percent, cheating carries a penalty the value of which is larger than the short-run lure... the crucial threshold is 2/38 = 5.26 percent"` (l. 2777).
      2. Printing a `"meet the competition"` clause (`"We will meet any lower price charged by any competitor"`, l. 2979 & 5460) or `"beat the competition"` clause (`"(MINI) TRIP TO THE GYM NO. 4"`, l. 5485 & Workout l. 13054), which turns unilateral price-cutting from a `$140,000` gain into `$40,000` (or worse) and sustains `($80, $80)`.
    - **Catastrophic Loss?**: At `($80, $40)`, the `$80` firm loses its entire customer base (`$0` profit).

21. ***L.A. Confidential* Interrogation Dilemma (Exley vs. Fontaine, Coates, and Jones)**
    - **Heading & First Line**: `"MANY CONTEXTS, ONE CONCEPT"` & `"Some Preliminary Ideas for Resolving the Dilemma"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2164-L2189), [l. 2372](file:///home/masih/Work/tries/aos/book-full.txt#L2372-L2382), [l. 2698](file:///home/masih/Work/tries/aos/book-full.txt#L2698-L2705)) — `"In a scene from the movie L.A. Confidential, Sergeant Ed Exley promises Leroy Fontaine, one of three suspects held in isolated rooms"`
    - **Players, Moves, Timing**: 3 suspects (Leroy Fontaine, Sugar Ray Coates, Tyrone Jones) interrogated separately by Sgt. Ed Exley. Moves: Confess/snitch vs. Keep silent. Simultaneous.
    - **Payoffs**: First to confess gets a lighter sentence; silent partners take the fall; if all confess, all get heavy sentences.
    - **Family**: `prisoners' dilemma`.
    - **Best Move / Real People**: Confessing dominates inside the police payoff matrix unless external gang retaliation outweighs prison reduction.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Post-release retaliation by criminal associates: `"even if a prisoner gets a lighter sentence by confessing, when he emerges from jail, he may find friends of the other two waiting for him!"` (l. 2379).
    - **Catastrophic Loss?**: Yes — long prison sentence or gang retribution upon release.

22. **Baseball Plunking Dilemma: American League vs. National League (Designated Hitter Rule)**
    - **Heading & First Line**: `"Some Preliminary Ideas for Resolving the Dilemma"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2383-L2396)) — `"A striking example comes from baseball. Batters in the American League are hit by pitches 11 to 17 percent more often than batters in the National League."`
    - **Players, Moves, Timing**: 2 opposing pitchers/teams. Moves: Throw beanball (`"plunk"` opposing batter) vs. pitch cleanly. Sequential / repeated across innings.
    - **Payoffs**: Intimidation advantage vs. having your own pitcher or batters hit in retaliation (a National League pitcher's probability of being hit jumps by a factor of 4 after hitting an opposing batter in the previous half-inning).
    - **Family**: `prisoners' dilemma` (repeated with tit-for-tat deterrence).
    - **Best Move / Real People**: National League pitchers refrain from plunking 11–17% more often than American League pitchers.
    - **THE RULE THAT CHANGES THE BEST MOVE**: The Designated Hitter (DH) rule in the American League: `"In the American League, the pitchers don’t bat. Thus an American League pitcher who plunks a batter doesn’t have to fear direct retaliation."`
    - **Catastrophic Loss?**: Severe physical injury from a fastball (`"Imagine having to face Randy Johnson after hitting one of his teammates"`).

23. **Axelrod's Repeated Prisoners' Dilemma Computer Tournaments, Southampton's 60-Program Entry, and Blood Feuds**
    - **Heading & First Line**: `"TIT FOR TAT"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2398-L2494) & fn [l. 13986](file:///home/masih/Work/tries/aos/book-full.txt#L13986-L13997)) — `"In the early 1980s, University of Michigan political scientist Robert Axelrod invited game theorists from around the world to submit programs"`
    - **Players, Moves, Timing**: $N$ computer programs playing 2-player 150-round repeated PD matches in a round-robin tournament (and real-world feuds: Hatfields & McCoys, Grangerfords & Shepherdsons in *Huckleberry Finn*, Arab-Israeli conflict).
    - **Payoffs**: Standard repeated PD payoffs summed across all matches.
    - **Family**: `prisoners' dilemma` (repeated).
    - **Best Move / Real People**: Anatol Rapoport's `"tit for tat"` (start with Cooperate, then copy opponent's previous move) won both of Axelrod's original tournaments despite never beating any single opponent head-to-head. In the 2004 20th-anniversary tournament (fn l. 13986), a Southampton University team submitted 60 programs that recognized each other via a secret sequence of moves: 59 `"drones"` sacrificed themselves to 1 `"queen"` and defected against all outsiders, winning top spots.
    - **THE RULE THAT CHANGES THE BEST MOVE**:
      1. Cumulative points vs. head-to-head winner-take-all scoring: `"if Axelrod had scored each competition as a winner-take-all contest, tit for tat would have only losses and ties and therefore could never have finished in first place"` (l. 2442).
      2. Noise / errors / misperception: `"The slightest possibility of a mistake or a misperception results in a complete breakdown in the success of tit for tat"` (l. 2457; 50% of runs degenerate into endless feuds, making `"tit for two tats"` or `"forgiving tit for tat"` better).
      3. Allowing a single entrant to submit a cartel of 60 programs (fn l. 13986).
    - **Catastrophic Loss?**: In real-world blood feuds with noise (`"Grangerfords and the Shepherdsons"`), mutual slaughter.

24. **Cotton-Top Tamarin Monkeys Lever-Pulling Dilemma**
    - **Heading & First Line**: `"TIT FOR TAT"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2478-L2494)) — `"Here we might even learn something from monkeys. Cotton-top tamarin monkeys were placed in a game where they had to pull a lever"`
    - **Players, Moves, Timing**: 2 cotton-top tamarin monkeys. Moves: Pull lever (costly effort) to deliver food to partner vs. do not pull. Repeated.
    - **Payoffs**: Food reward to partner minus effort cost.
    - **Family**: `prisoners' dilemma` (repeated).
    - **Best Move / Real Behavior**: Monkeys sustained high cooperation using `"tit for two tats"` (tolerating up to 2 consecutive shirks before retaliating).
    - **THE RULE THAT CHANGES THE BEST MOVE**: More than two consecutive defections triggers retaliation (`"Before they retaliated, they tolerated up to two failures by their partner"`).
    - **Catastrophic Loss?**: No.

25. ***Friend or Foe* (Game Show Network One-Shot Prisoners' Dilemma)**
    - **Heading & First Line**: `"MORE RECENT EXPERIMENTS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2496-L2528)) — `"Indeed, the most striking demonstration of this was on the Game Show Network’s production of Friend or Foe."`
    - **Players, Moves, Timing**: 2 contestants who built a "trust fund" ($200 to $16,400 across 105 episodes). Moves: Simultaneously choose `"friend"` (Cooperate) or `"foe"` (Defect). One-shot simultaneous.
    - **Payoffs**: `(Friend, Friend)` = 50:50 split; `(Foe, Friend)` = 100% to Foe, $0 to Friend; `(Foe, Foe)` = $0 to both.
    - **Family**: `prisoners' dilemma` (weakly dominant strategy).
    - **Best Move / Real People**: `"Foe"` is dominant (`"gives at least as high a payoff as choosing friend, and possibly more"`). Real people: Nearly 50% chose `"friend"` (in Season 1, 53.7% of women and 47.5% of men; in Season 2 after 40 episodes aired, female-female pairs stayed at 55%, while in mixed pairs women dropped to 34.2% and men to 42.3%).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Airing the first 40 episodes publicly before Season 2 (`"in season 2, the results of the first 40 episodes had been aired"`, reducing cooperation in mixed-gender pairs).
    - **Catastrophic Loss?**: Yes — losing 100% of the prize ($0).

26. **Flood and Dresher's 100-Round Prisoners' Dilemma Experiment**
    - **Heading & First Line**: `"MORE RECENT EXPERIMENTS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2529-L2570)) — `"Almost immediately after they had thought up the game, Flood and Dresher recruited two of their colleagues to play the dilemma game a hundred times."`
    - **Players, Moves, Timing**: 2 RAND colleagues. Moves: Cooperate vs. Defect in each of 100 known rounds. Finitely repeated (100 rounds).
    - **Payoffs**: Asymmetric pennies/dollars PD matrix (exact numbers not in text).
    - **Family**: `prisoners' dilemma`.
    - **Best Move / Real People**: Backward induction from Round 100 dictates Defect in all 100 rounds. Real people: Both cooperated in 60 of the 100 rounds (cooperating continuously from Round 83 to Round 98 before defecting in Round 99).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Known fixed final round vs. small probability that the opponent is a `"reciprocator"` type: `"even a selfish player who knows that the other player holds a view that there is a small chance that he (the first player) may be a reciprocator will try to foster this impression and cooperate until very near the end of the game"` (l. 2563).
    - **Catastrophic Loss?**: No.

27. **Battalio's 27-Student Texas A&M Classroom Multiperson Dilemma**
    - **Heading & First Line**: `"MORE RECENT EXPERIMENTS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2571-L2601)) — `"Professor Raymond Battalio of Texas A&M University had his class of 27 students play the following game."`
    - **Players, Moves, Timing**: $N = 27$ students. Moves: Simultaneously write `1` (Cooperate / low output) or `2` (Defect / high output) on a slip of paper. Simultaneous.
    - **Payoffs**: Table at l. 2580 is an image (`table not in text`), exact numbers in prose: If all 27 write `1`, each gets `$1.08` (`$29.16` total); if 26 write `1` and 1 writes `2`, `1`-writers get `$1.04` and the `2`-writer gets `$1.54`; regardless of how many others write `1`, switching your own slip from `1` to `2` increases your own payout by `+46 cents` (`50 cents` higher column gap minus `4 cents` drop) while lowering each of the other 26 students' payouts by `4 cents` (a net class loss of `58 cents` per defector); if all 27 write `2`, each gets `$0.50`.
    - **Family**: `prisoners' dilemma` (multiperson).
    - **Best Move / Real People**: Writing `2` is strictly dominant (`+46 cents` in every contingency). Real students: Even after open classroom discussion and a vocal conspiracy to write `1`, only 4 of 27 students wrote `1` in the final binding round (total class payout `$15.82`, and the conspiracy organizer himself wrote `2`!).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Making individual choices public rather than secret ballots: `"if the students could detect who had reneged on the agreement to write 1, they could inflict social sanctions such as ostracism"` (l. 2627).
    - **Catastrophic Loss?**: No.

28. **Four-Player Public Goods Contribution Game & Altruistic Punishment Variant**
    - **Heading & First Line**: `"MORE RECENT EXPERIMENTS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2602-L2668)) — `"More recent laboratory experiments of multiperson dilemmas use a format called the contribution game."`
    - **Players, Moves, Timing**: 4 players ($A, B, C, D$; generalizable to $N$). Moves: Phase 1: Each receives $10 and chooses how much ($0–$10) to contribute to a common pool, which is doubled and split equally among all 4. Phase 2 (Punishment variant, l. 2637): After observing everyone's Phase 1 contribution, each player can pay `33 cents` per `$1` of fine inflicted on any other player. Simultaneous (1-stage) or Sequential (2-stage).
    - **Payoffs**: Every $1 contributed costs $1 and returns $0.50 to self (and $0.50 to each of the other 3). All contribute $0 -> $10 each; all contribute $10 -> $20 each.
    - **Family**: `prisoners' dilemma` / `commons`.
    - **Best Move / Real People**: In Phase 1 alone, contributing $0 (`"free rider"`) is dominant; in a 10-round experiment, contributions start at ~50% and decay to ~10%. In the 2-stage punishment game, punishing is dominated for a purely selfish player in the final stage, yet real subjects pay to punish free riders (activating the brain's dorsal striatum reward center), which raises Phase 1 contributions dramatically.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Adding the Phase 2 costly peer-punishment stage with observable contributions: `"when a second stage is added to the contribution game and players are given an opportunity to punish those who cheat on the implicit agreement to contribute maximally, this increases the contributions in the first phase of the game dramatically"` (l. 2648).
    - **Catastrophic Loss?**: No.

29. **Business Cartel Dilemmas: ADM & Ajinomoto Lysine Cartel, GE/Westinghouse/Allied-Chalmers Lunar-Cycle Turbine Cartel, FCC Spectrum Area-Code Bids, Pratt & Whitney vs. Rolls-Royce Fuel Guarantee, Ethyl/DuPont Most-Favored-Customer Clause**
    - **Heading & First Line**: `"DILEMMAS IN BUSINESS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2877-L3003)) — `"Let us begin with the dilemma of rival firms in an industry."`
    - **Players, Moves, Timing**: 2 or 3+ competing firms:
      - *Lysine (l. 2882)*: Archer Daniels Midland (ADM), Ajinomoto, and 3 Asian firms.
      - *Electrical Turbines (l. 2916)*: GE (60% share), Westinghouse (30%), Allied-Chalmers (10%) bidding on public utility contracts in the 1950s.
      - *FCC Spectrum Auctions (l. 2938)*: Telecom bidders in 1996–97 using the last 3 digits of multi-million-dollar bids to encode contested area codes.
      - *Jet Engines (l. 2948)*: Pratt & Whitney vs. Rolls-Royce bidding for Boeing 747 orders from Pan Am, BOAC, and Japan Airlines (P&W promised 8% better fuel efficiency or cash reimbursement, deterring Rolls-Royce from cutting price).
      - *Gasoline Antiknock Compound (l. 2960)*: Ethyl Corp. and DuPont using `"most-favored-customer"` clauses (promising every buyer the lowest price given to any customer).
    - **Payoffs**: Cartel monopoly profits vs. price-war profits (and prison sentences if caught by DOJ).
    - **Family**: `prisoners' dilemma` / `auction` / `signalling`.
    - **Best Move / Real People**: Firms used transparent rotation rules (days 1–17 of lunar month = GE, days 18–25 = Westinghouse, days 26–28 = Allied-Chalmers) or contractual penalty clauses (most-favored-customer / fuel-efficiency guarantee) to make secret price cuts detectable or expensive.
    - **THE RULE THAT CHANGES THE BEST MOVE**:
      - Making secret discounts public/automatic via a `"most-favored-customer"` clause (`"Now, cutting the price for one customer order requires cutting the price for all orders"`, l. 2966).
      - FTC/DOJ antitrust prohibition of those clauses or FBI infiltration (`"One of the participants in the conspiracy was an FBI informant"`, l. 2905).
    - **Catastrophic Loss?**: Yes — criminal conviction and prison for executives (`"some executives of the three firms went to jail"`, l. 2931).

30. **Tragedies of the Commons (Hardin's Grazing Commons, Global Warming, Ostrom's Community Governance)**
    - **Heading & First Line**: `"TRAGEDIES OF THE COMMONS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L3005-L3081) & fn [l. 14002](file:///home/masih/Work/tries/aos/book-full.txt#L14002-L14018)) — `"Among the examples at the start of this chapter, we mentioned problems like overfishing, in which each user gets the benefit of his extraction"`
    - **Players, Moves, Timing**: $N$ resource users (herders, fishermen, irrigators, nations emitting $\text{CO}_2$). Moves: Restrain use vs. overexploit. Repeated.
    - **Payoffs**: Individual extraction gain vs. collective depletion.
    - **Family**: `commons` / `prisoners' dilemma`.
    - **Best Move / Real People**: Without governance, overexploitation is dominant. Elinor Ostrom documented successful self-governing commons around the world.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Ostrom's five governance conditions (clear boundaries, clear extraction rules, automatic detection during normal routine, graduated sanctions, and user-designed rules) or private property rights (`"When land is private property, the invisible hand will shut the gate"`, fn l. 14004).
    - **Catastrophic Loss?**: Yes — total depletion/ruin of the common resource.

31. **Biological Dilemmas: Haldane's Kin Selection & Wilkinson's Costa Rican Vampire Bats**
    - **Heading & First Line**: `"NATURE RED IN TOOTH AND CLAW"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L3083-L3121)) — `"As you might expect, prisoners’ dilemmas arise in species other than humans."`
    - **Players, Moves, Timing**: Colony of ~12 vampire bats hunting individually at night (or kin in Haldane's calculation). Moves: Regurgitate blood to feed a starving colony-mate vs. refuse. Repeated.
    - **Payoffs**: A bat that fails to find blood for 3 consecutive nights faces death by starvation; a small blood donation saves its life. (Haldane: sacrifice life for $>2$ brothers [shared genes $1/2$] or $>8$ cousins [shared genes $1/8$]).
    - **Family**: `prisoners' dilemma` (reciprocal altruism).
    - **Best Move / Real Behavior**: Vampire bats share blood only when the recipient is near death AND only with recognized group members who have reciprocated in the past.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Individual recognition and memory within a small stable group: `"sharing occurred only among bats that already knew each other. And bats were much less likely to share blood with another bat that had previously refused to share blood when it had an excess"` (l. 3113).
    - **Catastrophic Loss?**: Yes — death by starvation (`"at risk of death"`).

32. **Case Study: The Early Bird Kills the Golden Goose (Galápagos Cactus Finches & Rousseau's Stag Hunt)**
    - **Heading & First Line**: `"CASE STUDY: THE EARLY BIRD KILLS THE GOLDEN GOOSE"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L3123-L3183)) — `"The Galápagos Islands are the home of Darwin’s finches."`
    - **Players, Moves, Timing**: $N$ cactus finches on Daphne Major (compared to $N$ hunters in Jean-Jacques Rousseau's Stag Hunt). Moves: Wait until 9:00 AM for cactus blossoms to open naturally (Cooperate/Stag) vs. pry open buds early and snip the stigma, sterilizing the flower so it produces no seeds or fruit (Defect/Hare). Simultaneous / evolutionary repeated.
    - **Payoffs**: If nobody snips stigmas, abundant seeds/fruit in the dry season; if few snip stigmas, territorial finches only ruin their own local dry-season food supply and lose out; if many snip stigmas (or territoriality breaks down), island-wide famine occurs and only early-prying birds get an extra sip of nectar before the entire population starves.
    - **Family**: `coordination (stag hunt, meeting)` (cousin to `prisoners' dilemma`).
    - **Best Move / Real Behavior**: Wait if others wait (and defend territories); pry early if the deviant strategy becomes widespread.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Breakdown of territorial boundaries or crossing the critical fraction of deviant birds: `"Because cactus finches are somewhat territorial, those practicing the deviant strategy bring ecological ruin mostly to themselves... Once the deviant strategy becomes pervasive, those finches that destroy the blossoms do best. Each gets one extra sip of nectar, while every bird gets the same dismal diet of seeds and fruits. It is the fittest strategy on a sinking ship"` (l. 3163–3173).
    - **Catastrophic Loss?**: Yes — extinction of the entire cactus finch population (`"eliminate the entire population"`).

---

### Chapter 4 — A Beautiful Equilibrium

33. **Big Game of Coordination: Fred and Barney's Stone Age Hunt (Stag, Bison, Rabbit / Assurance Game)**
    - **Heading & First Line**: `"BIG GAME OF COORDINATION"` & `"Which Equilibrium?"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L3207-L3259), [l. 3376](file:///home/masih/Work/tries/aos/book-full.txt#L3376-L3408)) — `"Fred and Barney are Stone Age rabbit hunters."`
    - **Players, Moves, Timing**: 2 players (Fred, Barney). Moves: Stag, Bison, or Rabbit (chosen in isolation in separate caves after forgetting their prior agreement). Simultaneous.
    - **Payoffs**: Tables at l. 3228 and l. 3380 (`table not in text`), exact numbers in prose: `(Stag, Stag) = (3, 3)`; `(Bison, Bison) = (3, 3)`; anyone choosing `Rabbit` gets `1` regardless of the other's choice; `(Stag, Bison)` or `(Bison, Stag) = (0, 0)`; lone `Stag` or `Bison` hunter against `Rabbit` gets `0` while `Rabbit` hunter gets `1`.
    - **Family**: `coordination (stag hunt, meeting)`.
    - **Best Move / Real People**: Three pure-strategy Nash equilibria: `(Stag, Stag)`, `(Bison, Bison)`, and `(Rabbit, Rabbit)`. Without assurance or a focal point on Stag vs. Bison, playing `Rabbit` is the safe choice.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Pre-play communication or a shared focal point providing assurance: `"Both would be better off if each could be confident that the other would go after the same big game... whether by direct communication or because of the existence of a focal point"` (l. 3399).
    - **Catastrophic Loss?**: Zero meat (`0`) for the family on a failed big-game hunt.

34. **Focal Point Coordination Games: Meeting in NYC (Schelling & ABC *Primetime*), Kreps's 9-Cities Partition, Naming a Positive Integer, Lost & Found, Keynes's Beauty Contest / Stock Market, and CEO Pay Escalation**
    - **Heading & First Line**: `"Which Equilibrium?"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L3409-L3588)) — `"We begin with one of Schelling’s classics. Suppose you are told to meet someone in New York City on a specific day"`
    - **Players, Moves, Timing**: 2 players (or $N$ players in Keynes's beauty contest and CEO pay). Simultaneous.
      - *NYC Meeting (l. 3409)*: Pick time and place in NYC without prior agreement. Schelling's students picked noon at the Grand Central Terminal information booth clock; in ABC *Primetime*'s 2006 experiment with 6 pairs, all 6 picked noon, 3 pairs went to the Empire State Building, 3 to Times Square, and all succeeded (women stood still holding signs while men ran around).
      - *Kreps's 9-Cities Game (l. 3452)*: Student A gets Boston, Student B gets San Francisco; partition 9 cities (`Atlanta, Chicago, Dallas, Denver, Houston, Los Angeles, New York, Philadelphia, Seattle`) into two non-overlapping lists. Complete non-overlapping partition wins a prize; any overlap or gap pays 0 ($2^9 = 512$ Nash equilibria). Over 80% of U.S. students succeeded by splitting East vs. West of the Mississippi River.
      - *Positive Integer Game (l. 3488)*: Both name any positive integer; match wins a prize, mismatch gets 0. Overwhelming choice: `1`.
      - *Keynes's Newspaper Beauty Contest & Stock Market (l. 3504)*: Pick the 6 prettiest of 100 photographs (or 1 redhead among 100); prize goes to the competitor whose picks are closest to the average preferences of all competitors.
      - *CEO Compensation Escalation (l. 3565)*: $N$ corporate boards each try to pay their CEO in the "top half" (above the industry average), driving pay up endlessly.
    - **Family**: `coordination (stag hunt, meeting)` (and `other` for CEO pay escalation).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Shared cultural/geographic background (`"Over 80 percent of pairs of American students succeeded in this task. Such coordination was much less likely when one or both students were non-U.S. residents"`, l. 3473).
    - **Catastrophic Loss?**: No.

35. **Battle of the Sexes (Movie Night *300* vs. *Pride and Prejudice*; Fred and Barney's Stag vs. Bison Hunt)**
    - **Heading & First Line**: `"BATTLES AND CHICKENS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L3589-L3650)) & Ch. 5 `"MIXING STRATEGIES IN MIXED-MOTIVES GAMES"` ([l. 4795](file:///home/masih/Work/tries/aos/book-full.txt#L4795-L4872)) — `"In the hunting game, the two players’ interests are perfectly aligned"`
    - **Players, Moves, Timing**: 2 players (Husband & Wife; or Fred & Barney). Moves: Stag vs. Bison (or *300* vs. *Pride and Prejudice*). Simultaneous (or repeated/sequential).
    - **Payoffs**: Tables at l. 3612 and l. 4806 (`table not in text`), exact numbers in prose: `(Stag, Stag) = (4 for Fred, 3 for Barney)`; `(Bison, Bison) = (3 for Fred, 4 for Barney)`; `(Stag, Bison)` or `(Bison, Stag) = (0, 0)`. (In Ch. 5 l. 4852 variant: Barney's payoffs are changed to `6` for Stag and `7` for Bison while Fred's remain `4` and `3`).
    - **Family**: `battle of the sexes`.
    - **Best Move / Real People**: Two pure Nash equilibria: `(Stag, Stag)` and `(Bison, Bison)`. There is also an inefficient, unstable mixed-strategy Nash equilibrium (Ch. 5 l. 4824) where Fred plays Stag with probability $x = 4/7$ and Barney plays Stag with probability $y = 3/7$, yielding expected payoff $12/7 = 1.71$ each and a $25/49$ chance of mismatch! (When Barney's payoffs change to 6 and 7, Barney's mix stays $y = 3/7$ while Fred's mix shifts to $x = 7/13$). Real subjects in labs fail to adjust their mix when the *other* player's payoffs change (l. 4869).
    - **THE RULE THAT CHANGES THE BEST MOVE**:
      1. Publicly observable correlating signal (correlated equilibrium): `"They can make an agreement that they both will go stag hunting if it is raining and bison hunting if it is dry. Then each will get an average payoff of 1/2 × 3 + 1/2 × 4 = 3.5"` (l. 4839).
      2. First-mover irreversible commitment by one partner (`"gain an advantage by seizing the initiative and making a rapid irreversible switch"`, l. 3628).
    - **Catastrophic Loss?**: Hungry family (`0` payoff) on mismatch.

36. **Chicken (Teenage Drivers in *Rebel Without a Cause* & Fred and Barney's North vs. South Rabbit Hunt)**
    - **Heading & First Line**: `"BATTLES AND CHICKENS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L3651-L3707)) & Ch. 6 `"CHANGING THE GAME"` ([l. 5246](file:///home/masih/Work/tries/aos/book-full.txt#L5246-L5284)) — `"The second classic game is called chicken."`
    - **Players, Moves, Timing**: 2 players (two teenage drivers racing toward each other or a cliff; or Fred & Barney choosing North vs. South rabbit grounds). Moves: Go Straight / North vs. Swerve / South. Simultaneous (or continuous time in Ch. 6).
    - **Payoffs**: Table at l. 3666 (`table not in text`), exact numbers in prose for Fred & Barney: `(South, South) = (1, 1)`; `(North, South) = (2, 1/2)` (South gets 1 rabbit minus 1/2 from envy); `(South, North) = (1/2, 2)`; `(North, North) = (0, 0)` (fight/crash). For teenage drivers, `(Straight, Straight)` = crash/hospital/death.
    - **Family**: `chicken`.
    - **Best Move / Real People**: Two pure Nash equilibria: `(North, South)` and `(South, North)`. To get the favored `2` outcome, one player must visibly commit to `Straight/North` before the other can.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Visibly disabling your ability to swerve *before* the opponent does: `"disconnect your steering wheel from the shaft and throw it out of the window in a manner that makes it very visible to the other driver. Then the other has no choice left except to swerve"` (l. 5263) — unless both throw their wheels out simultaneously!
    - **Catastrophic Loss?**: Yes — head-on collision, cliff crash, `"both may end up in the hospital, or worse"` (l. 5252).

37. **Case Study: Half Way (2-Player "Half the Other's Number" & $N$-Player "Half the Average" Beauty Contest, plus Dropped Cell-Phone Call)**
    - **Heading & First Line**: `"CASE STUDY: HALF WAY"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L4022-L4200) & fn [l. 14040](file:///home/masih/Work/tries/aos/book-full.txt#L14040-L14041)) — `"Abe and Bea are playing a game with the following rules: Each player is to pick a number between 0 and 100, inclusive."`
    - **Players, Moves, Timing**: 2 players (Abe and Bea) in the base game; $N$ players in the `"half the average"` classroom variant (l. 4155). Moves: Pick a number in $[0, 100]$. Player closest to half the other player's number (or half the group average) wins $100 (ties split $50 each). Simultaneous (and repeated across rounds).
    - **Payoffs**: $100 winner-take-all ($50 each on tie).
    - **Family**: `other` (iterated elimination of dominated strategies / $p$-beauty contest). (Also at l. 4189 in passing: **Dropped Mobile Phone Call**, 2 players, Call Back vs. Wait, 2 asymmetric equilibria like Chicken/Battle of the Sexes, solved by convention that the original caller calls back).
    - **Best Move / Real People**:
      - In the *2-player* game, `0` is a strictly dominant strategy (`0` is distance $X/2$ from $X/2$, whereas $X>0$ is distance $X$ from $0/2 = 0$), so `0` always wins or ties!
      - In the *$N$-player* game, `0` is *not* dominant (fn l. 14040: if two others pick `1` and `5`, the average with `0` is `2` and half the average is `1`, so picking `1` wins), though iterated elimination ($>50, >25, >12.5 \dots$) still leaves all-$0$ as the unique Nash equilibrium. Real people: On Round 1, most people pick `50` or `25` (only 2–3 steps of backward induction; authors pick `12.5` on Round 1 and `~0.78` on Round 2); after 2–3 repetitions, choices converge near `0`.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Changing from 2 players (`"closest to half the other’s number"`) to $N \ge 3$ players (`"closest to half the average number"`): `"Under these rules, it is no longer the case that 0 always wins"` (l. 4158), making the best move in early rounds depend on the population's depth of iterative reasoning (`12.5`).
    - **Catastrophic Loss?**: No.

---

### Chapter 5 — Choice and Chance

38. **Wit's End: *The Princess Bride* Poisoned Goblets (Westley vs. Vizzini)**
    - **Heading & First Line**: `"WIT’S END"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L4262-L4315) & fn [l. 14042](file:///home/masih/Work/tries/aos/book-full.txt#L14042-L14047)) — `"The Princess Bride is a brilliant whimsical comedy; among its many memorable scenes is the battle of wits"`
    - **Players, Moves, Timing**: 2 players (Westley in black mask vs. Vizzini). Moves: Westley secretly puts iocane poison in goblet in front of himself or in front of Vizzini (or both, in the movie); Vizzini chooses which goblet to drink from, and Westley drinks the other. Simultaneous.
    - **Payoffs**: Survival vs. death (`"one will die and the other will live"`).
    - **Family**: `zero-sum mixing` (and asymmetric capability in the movie).
    - **Best Move / Real Behavior**: In a symmetric 1-poisoned-cup game, randomize 50:50. In the movie, Vizzini tries infinite-regress deduction, distracts Westley to swap glasses, and drops dead because Westley had built up immunity to iocane powder and poisoned *both* glasses (fn l. 14042).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Westley's secret immunity to iocane poison allows him to poison both cups (fn l. 14042: `"Westley has spent the last few years building up an immunity to iocane powder and has put the poison in both glasses"`).
    - **Catastrophic Loss?**: Yes — death (`"falls over dead"`).

39. **Mixing It Up on the Soccer Field: Penalty Kicks (Palacios-Huerta Empirical Data & Comparative Statics Variants)**
    - **Heading & First Line**: `"MIXING IT UP ON THE SOCCER FIELD"`, `"Theory and Reality"`, `"Surprising Changes in Mixtures"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L4316-L4552), [l. 5005](file:///home/masih/Work/tries/aos/book-full.txt#L5005-L5093)) — `"The penalty kick in soccer is indeed the simplest and the best-known example of this dilemma."`
    - **Players, Moves, Timing**: 2 players (Kicker, Goalie). Moves: Left vs. Right (where Right = kicker's natural side). Simultaneous (11-meter kick reaches goal in ~0.3 seconds, so goalie must dive before seeing ball's trajectory).
    - **Payoffs**: Tables at l. 4371, 4417, 4500, 4544 and charts at l. 5023, 5061, 5075 are images (`table not in text`), with all numbers stated in prose from Ignacio Palacios-Huerta's dataset of 1,417 penalty kicks (1995–2000):
      - *Empirical Payoff Matrix (Scoring % for Kicker; Goalie gets $100\% - \text{score}$)*:
        - `(Left, Left)`: Kicker `58%`, Goalie `42%`
        - `(Left, Right)`: Kicker `95%`, Goalie `5%`
        - `(Right, Left)`: Kicker `93%`, Goalie `7%`
        - `(Right, Right)`: Kicker `70%`, Goalie `30%`
      - *Variant A (Dominant Pure Strategy, l. 4537)*: Kicker improves `(Left, Left)` from `58%` to `94%` (exceeding `93%` at `(Right, Left)`).
      - *Variant B (Goalie Improves Right Save, l. 5066)*: Kicker's success at `(Right, Right)` drops from `70%` to `60%`.
    - **Family**: `zero-sum mixing`.
    - **Best Move / Real People**:
      - In the empirical game, Kicker's equilibrium mix is `38.3% Left` ($23/60$), `61.7% Right` ($37/60$); Goalie's equilibrium mix is `41.7% Left` ($25/60$), `58.3% Right` ($35/60$); equilibrium scoring rate is `79.6%`.
      - Real professional players: Kickers chose Left `40.0%` and Right `60.0%`; Goalies chose Left `42.3%` and Right `57.7%` (remarkably close to Nash equilibrium!).
      - In *Variant A* (`(L,L) = 94%`), `Left` becomes a strictly dominant pure strategy for Kicker (`94% > 93%` and `95% > 70%`) and `(Left, Left)` is a pure Nash equilibrium (`94%`).
      - In *Variant B* (`(R,R)` drops from `70%` to `60%`), Goalie's equilibrium use of `Left` rises from `41.7%` to `50%` (using his newly improved `Right` side *less* often!), Kicker's `Left` rises from `38.3%` to `47.1%`, and Kicker's scoring rate drops from `79.6%` to `76.5%`.
    - **THE RULE THAT CHANGES THE BEST MOVE**:
      1. If Kicker's success rate when both choose Left rises above Kicker's success rate when Kicker goes Right and Goalie goes Left (`94% > 93%`), mixing disappears and pure `(Left, Left)` becomes the unique equilibrium (`"Now Left is a dominant strategy for the kicker, and the game has a pure-strategy Nash equilibrium"`, l. 4546).
      2. If Goalie improves his Right-side save (`70% -> 60%`), *Kicker* shifts toward Left (`38.3% -> 47.1%`) and *Goalie* dives Right *less* often (`58.3% -> 50%`): `"When the goalie improves his skill at saving penalties struck to the right, he uses that side less frequently!"` (l. 5072).
    - **Catastrophic Loss?**: Elimination in World Cup penalty shootouts (e.g., 2006 England vs. Portugal, l. 4621).

40. **Child's Play: World Rock Paper Scissors Championship (Andrew Bergel vs. Stan Long)**
    - **Heading & First Line**: `"CHILD’S PLAY"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L4554-L4624), [l. 4685](file:///home/masih/Work/tries/aos/book-full.txt#L4685-L4736)) — `"On October 23, 2005, Andrew Bergel of Toronto was crowned that year’s Rock Paper Scissors International World Champion"`
    - **Players, Moves, Timing**: 2 players (Andrew Bergel, Stan Long). Moves: Rock, Paper, Scissors (`prime, approach, delivery`). Simultaneous, repeated.
    - **Payoffs**: Table at l. 4586 (`table not in text`), exact numbers in prose: Win = `+1`, Tie = `0`, Loss = `-1`.
    - **Family**: `zero-sum mixing`.
    - **Best Move / Real People**: Game theory prescribes mixing $1/3, 1/3, 1/3$ (expected payoff `0`). Championship players use psychological gambits like `"Bureaucrat"` (`Paper, Paper, Paper`), `"Scissor Sandwich"` (`Paper, Scissors, Paper`), and `"Exclusion Strategy"` to exploit human negative serial correlation (too many reversals), though tournament records show little year-to-year consistency.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Using an external randomizer (such as the second hand on a wristwatch or odd/even birthdates, l. 4700) vs. human mental randomization (`"people tend to forget that heads is just as likely to be followed by heads as by tails; therefore they have too many reversals"`).
    - **Catastrophic Loss?**: No.

41. **Baseball Pitching (Fastball vs. Forkball), Grand Slam Tennis Serves, and Football Third-Down Play Calling**
    - **Heading & First Line**: `"HOW TO ACT RANDOMLY"` & `"Unique Situations"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L4660-L4786)) — `"Randomization does not mean alternating between the pure strategies."`
    - **Players, Moves, Timing**: 2 players/teams (Pitcher vs. Batter; Tennis Server vs. Receiver; Football Coach vs. Defense on 3rd-and-1; Battle Commander vs. Enemy with espionage). Simultaneous.
    - **Payoffs**: Batting average / point win % / first down vs. touchdown.
    - **Family**: `zero-sum mixing`.
    - **Best Move / Real People**: Randomize independently at the last moment using an espionage-proof device (e.g., wristwatch second hand: 1–24 = fastball [40%], 25–60 = forkball [60%]). Grand slam tennis servers show slight negative serial correlation (reversing too often), but too small for receivers to exploit.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Possibility of espionage or predictability in a one-shot battle: `"If you choose a definite course of action, and the enemy discovers what you are going to do, he will adapt his course of action to your maximum disadvantage. You want to surprise the enemy; the surest way to do so is to surprise yourself"` (l. 4760).
    - **Catastrophic Loss?**: Military defeat or coach getting fired (`"a similarly risky strategy in business can get you fired if it fails"`, l. 4886).

42. **Mixing in Business and Other Wars: Coke vs. Pepsi Promotions, Last-Minute Airline Tickets, Parking Meters, Random Drug Testing, IRS Audits, and WWII Dud Shells / Missile Decoys**
    - **Heading & First Line**: `"MIXING IN BUSINESS AND OTHER WARS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L4873-L4994)) — `"Our examples of the use of mixed strategies came from the sporting world."`
    - **Players, Moves, Timing**:
      - *Coke vs. Pepsi Coupons (l. 4889)*: 2 firms choosing in which weeks of a 52-week year to run price promotions.
      - *Parking Meter / Drug Testing / IRS Enforcement (l. 4937)*: Authority vs. Citizen/Employee. Meter fee = `$1/hr`; fine = `$25`; enforcement probability = `1/25` (`4%`).
      - *Air Defense vs. Decoys / WWII Dud Shells (l. 4973)*: Attacker mixes cheap decoy missiles or random dud shells with live warheads; Defender must intercept or defuse all of them.
    - **Family**: `zero-sum mixing`, `prisoners' dilemma` / `battle of the sexes` (for Coke & Pepsi), and `signalling` / `other` (inspection game).
    - **Best Move / Real People**: Coke and Pepsi resolved their promotional prisoners' dilemma by alternating 26 weeks each with zero overlap over 52 weeks (probability `< 1 in a quadrillion` under independent 50:50 mixing, l. 4915). In enforcement, set $\text{Fine} \times \text{Probability} \ge \text{Gain from cheating}$ ($25 \times 1/25 = $1). In WWII, firing dud shells randomly forced defenders to treat every unexploded shell as a delayed time bomb.
    - **THE RULE THAT CHANGES THE BEST MOVE**:
      - For Coke & Pepsi: ongoing relationship allowing coordinated turn-taking (`"each company to take a turn at having the lowest price"`, l. 4927) rather than independent mixing.
      - For enforcement: raising the fine lets the enforcer slash the inspection probability (`"When the fine is $25, a 1 in 25 risk of being caught is enough to keep you honest"`, l. 4949).
    - **Catastrophic Loss?**: In missile defense, failure to stop a real nuclear warhead among decoys (`"an air defense must be able to destroy nearly 100 percent of all incoming missiles"`, l. 4976).

43. **Case Study: Janken Step Game (Takashi vs. Yuichi in Tokyo Sushi Bar)**
    - **Heading & First Line**: `"CASE STUDY: JANKEN STEP GAME*"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L5095-L5171)) — `"The scene is a sushi bar in downtown Tokyo. Takashi and Yuichi are sitting at the bar drinking sake while waiting for their sushi."`
    - **Players, Moves, Timing**: 2 players (Takashi, Yuichi). Moves: Paper, Scissors, Rock. Simultaneous.
    - **Payoffs**: Table at l. 5119 is an image (`table not in text`), exact payoffs in steps ahead given in prose: Winning with Paper (5 fingers) = `+5` steps (loser `-5`); winning with Scissors (2 fingers) = `+2` steps (loser `-2`); winning with Rock (0 fingers) = `+1` step (loser `-1`); ties = `0` (replayed).
    - **Family**: `zero-sum mixing`.
    - **Best Move / Real People**: Indifference equations $-5p + q = 3p + q - 1 = -5p - 7q + 5$ yield the unique mixed-strategy Nash equilibrium: play **Paper $p = 1/8$**, **Scissors $q = 5/8$**, and **Rock $1 - p - q = 2/8$** (expected payoff = `0`).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Asymmetry in step rewards (`5` steps for Paper, `2` for Scissors, `1` for Rock instead of `1, 1, 1` in standard RPS) shifts the optimal mixture from `(1/3, 1/3, 1/3)` to `(1/8 Paper, 5/8 Scissors, 2/8 Rock)`: Scissors is played $5/8$ of the time to guard against the opponent's 5-step Paper payoff!
    - **Catastrophic Loss?**: No.

---

### Chapter 6 — Strategic Moves

44. **Deterrence and Compellence in Cold War Europe & "(Mini) Trip to the Gym No. 4" (NATO vs. USSR & RE vs. BB Beat-the-Competition)**
    - **Heading & First Line**: `"DETERRENCE AND COMPELLENCE"` & `"(MINI) TRIP TO THE GYM NO. 4"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L5475-L5525), Workout [l. 13054](file:///home/masih/Work/tries/aos/book-full.txt#L13054-L13082)) — `"Because threats come in two varieties, it is useful to have separate names to help keep them straight."`
    - **Players, Moves, Timing**:
      - *Cold War Europe (Workout l. 13054)*: 2 players (Soviet Union, United States). USSR chooses Invade Western Europe or Stay Out; US chooses Counterattack/Nuclear Retaliation or Do Nothing. Sequential.
      - *RE vs. BB Beat-the-Competition (l. 5485)*: RE commits to charge $80 if BB charges $80, but if BB cuts below $80, RE will *beat* BB's price by $5.
    - **Payoffs**: Trees at l. 13055 and l. 13077 (`table not in text`), exact numbers in prose (l. 13056–13075):
      - `(Don't Invade)`: USSR = `0`, US = `0`
      - `(Invade, Do Nothing)`: USSR = `+100`, US = `-100`
      - `(Invade, Counterattack)`: USSR = `-500`, US = `-200`
    - **Family**: `brinkmanship` / `other` (sequential deterrence game).
    - **Best Move / Real People**: Without a prior commitment, if USSR invades, US prefers `Do Nothing (-100)` over `Counterattack (-200)`, so USSR invades. With a credible automatic commitment to counterattack (e.g., tripwire troops in Berlin/Europe), USSR sees `-500 < 0` and does not invade, yielding `(0, 0)`.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Pre-committing to automatic retaliation before the invasion decision: `"Why would the United States want to take the trouble to commit in advance to a violent response in the case of a Soviet invasion, instead of maintaining the freedom of action to respond when the time came? Because if it waited until after the invasion, it would have to weigh the prospect of an all-out war against the marginal value of keeping Western Europe free"` (l. 13063).
    - **Catastrophic Loss?**: Yes — all-out nuclear war (`-500, -200`).

45. **Warnings and Assurances: Boeing vs. Airbus Superjumbo (A380)**
    - **Heading & First Line**: `"WARNINGS AND ASSURANCES"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L5526-L5599)) — `"All threats and promises have a common feature: the response rule commits you to taking actions that run counter to your inclinations"`
    - **Players, Moves, Timing**: 2 players (Boeing, Airbus). Moves: Develop vs. Don't Develop a superjumbo aircraft (600–800 seats). Sequential / simultaneous.
    - **Payoffs**: Market supports at most 1 profitable superjumbo; if both enter, both lose massive R&D investments.
    - **Family**: `chicken` / `duel or preemption`.
    - **Best Move / Real People**: Airbus committed first to the A380; once Airbus was in, Boeing's warning (`"if you build it, we won't, because the market is too small for two"`) became a simple factual statement, and Boeing stayed out (developing the mid-size 787 Dreamliner instead).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Whether the market can profitably support one firm vs. two firms, and who commits irreversibly first.
    - **Catastrophic Loss?**: Multi-billion-dollar R&D loss if both build a superjumbo.

46. **Waiting for a Threat or Promise: Professor Recommending Weak Student & Kidnapping Ransom**
    - **Heading & First Line**: `"OTHER PLAYERS’ STRATEGIC MOVES"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L5600-L5637)) — `"It is natural to think of the advantages you can get from strategic moves"`
    - **Players, Moves, Timing**: 2 players (Professor vs. Colleague at another university; or Kidnapper vs. Victim). Moves: Professor chooses whether to commit to candid letters or let Colleague move first by threatening never to trust the Professor again if a weak student turns out to be a dud. Sequential.
    - **Payoffs**: Qualitative (both gain if Colleague makes the threat first, solving the trust dilemma; in kidnapping, if Kidnapper commits first to release upon ransom, Victim pays).
    - **Family**: `other` (sequential commitment / timing of strategic moves).
    - **Best Move**: In a prisoners'/trust dilemma, let the other player make the threat/promise if you lack credibility yourself; in a conflict game (like Chicken or Kidnapping), preempt before the opponent can commit.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Who commits first (`"You may wait for a threat before taking any action"` in positive-sum trust games vs. seizing first-mover commitment in conflict games).
    - **Catastrophic Loss?**: Death of kidnap victim if kidnapper cannot credibly promise safe release.

47. **Brinkmanship: *L.A. Confidential* Russian Roulette (Bud White vs. Leroy Fontaine), Cuban Missile Crisis (Kennedy vs. Khrushchev), 1960s Civil Rights Movement (MLK vs. Bull Connor), and Labor Strikes**
    - **Heading & First Line**: `"BRINKMANSHIP"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L5759-L5923)) — `"In the book and movie L.A. Confidential, the 'good cop' Ed Exley is getting nowhere with his Prisoner’s Dilemma Stratagem"`
    - **Players, Moves, Timing**: 2 players:
      - *L.A. Confidential (l. 5759)*: Detective Bud White vs. suspect Leroy Fontaine. White loads 1 bullet in his 6-chamber `.38` revolver, spins cylinder, pulls trigger once at Fontaine's head (click = $1/6$ risk), next pull has $1/5$ risk, then $1/4, 1/3, 1/2, 1$. Fontaine confesses before the second pull.
      - *Cuban Missile Crisis (October 1962, l. 5839)*: JFK vs. Nikita Khrushchev. USSR places nuclear missiles in Cuba; US imposes naval `"quarantine"` (rather than immediate invasion or air strike), creating an escalating risk that a Soviet ship refuses to stop or a local commander fires (as actually happened when a Soviet commander in Cuba shot down a U-2 plane without Moscow's authorization, l. 5908). Khrushchev removes the missiles in exchange for a public no-invasion pledge and a private US promise to remove obsolete missiles from Turkey.
      - *1960s Civil Rights Protests (l. 5915)*: Martin Luther King Jr. vs. Segregationist Authorities. Peaceful marches created a risk of violent escalation by followers on both sides, compelling federal civil rights legislation.
    - **Payoffs**: Compliance vs. concession vs. mutual catastrophe (nuclear war costing hundreds of millions of lives; death of suspect; race war).
    - **Family**: `brinkmanship` (`"chicken in real time"`).
    - **Best Move / Real People**: When a pure threat of immediate catastrophe is too costly to be credible (`"Why would the United States risk losing 100 million lives right away if it actually invaded Cuba?"`), replace certainty with a *gradually escalating probability* of mutual disaster (`"brinkmanship is a controlled loss of control"`, l. 6493).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Scaling down a massive, incredible threat into a small, controllable risk of falling over the brink: `"threaten to expose both yourself and the other party to the risk (not the certainty) of a shared disaster"` (l. 5816).
    - **Catastrophic Loss?**: Yes — global nuclear war, death in Russian roulette, or civil war.

48. **Case Study: Two Wrongs Keep Things Right (Parent vs. Child Discipline & Sovereign Debt Default)**
    - **Heading & First Line**: `"CASE STUDY: TWO WRONGS KEEP THINGS RIGHT"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L5924-L5980)) — `"Parents often face a difficult problem in punishing their children for bad behavior"`
    - **Players, Moves, Timing**: 2 players (Parent vs. Child; or Bank Lender vs. Sovereign Borrower). Moves: Child obeys or misbehaves; Parent punishes or forgives (after the act is done, punishing hurts both parent and child). Repeated.
    - **Payoffs**: Qualitative (punishing is costly to both parent and child in a single round, so in a one-shot game the child knows the parent prefers to forgive).
    - **Family**: `other` (repeated deterrence / reputation game).
    - **Best Move / Real People**: Link today's forgiveness to tomorrow's behavior: if the parent lets the child off once, the child *knows* a second transgression will force the parent to punish to salvage parental credibility (`"If the parent fails to punish the child in accordance with the stated threat, the two reach a new behavioral expectation: the parent loses all credibility... Precisely to avoid this unhappy outcome, the parent can be expected to carry out the threatened punishment if the child misbehaves a second time"`, l. 5960).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Tying future credibility to carrying out the punishment on the next violation (`"if the parent ever lets the child off the hook, both should expect that the child will behave worse next time"`, forcing the parent to punish).
    - **Catastrophic Loss?**: Sovereign debt cut-off or total loss of parental authority.

---

### Chapter 7 — Making Strategies Credible

49. **In God We Trust? (Garden of Eden Deterrence: God vs. Adam, Eve, and the Serpent)**
    - **Heading & First Line**: `"IN GOD WE TRUST?"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L5990-L6050)) — `"Early in Genesis, God explains to Adam the punishment for eating from the tree of knowledge of good and evil"`
    - **Players, Moves, Timing**: 4 players (God, Adam, Eve, Serpent). Moves: God threatens `"in the day that thou eatest thereof thou shalt surely die"`; Serpent tells Eve `"Ye shall not surely die"`; Eve and Adam eat the forbidden fruit; God expels them from Eden instead of killing them that day (Adam lives to 930). Sequential.
    - **Payoffs**: Obedience in Eden vs. knowledge of good and evil vs. death/expulsion.
    - **Family**: `brinkmanship` / `other` (credibility of oversized deterrence threat).
    - **Best Move / Real Behavior**: Because killing Adam and Eve would ruin God's own creation plan, the Serpent deduces the threat is not credible (`"Ye shall not surely die"`), Eve eats first (testing whether she dies before offering it to Adam), and God scales down the punishment to expulsion and mortality.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Whether carrying out the threatened punishment destroys the threatener's own objective: `"If carrying out the threat hurts your own interest too severely, the target of the threat will know that, come the day, you will back down"` (l. 6034).
    - **Catastrophic Loss?**: Expulsion from Eden and human mortality (or destruction of humanity if carried out).

50. **The Eightfold Path to Credibility: Mini-Games & Historical Instances**
    - **Heading & First Line**: `"THE EIGHTFOLD PATH TO CREDIBILITY"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L6051-L6730)) — `"In most situations, mere verbal promises should not be trusted."`
    - **Distinct Game Instances Inside This Section**:
      - **50a. Deposit-Refund Bottle Recycling & Auto Emissions Tampering** (l. 6102; Government vs. Drivers/Consumers; `commons`/`other`; 5-cent deposit works for bottles, whereas a large fine for tampering with a car's pollution control device would merely induce owners of old cars to abandon them on city streets!).
      - **50b. Polaroid vs. Kodak Instant Camera War** (l. 6204; Edwin Land's Polaroid vs. Kodak in 1976; `duel or preemption`/`chicken`; Land kept 100% of Polaroid focused on instant photography and sued Kodak, winning $909.5 million and forcing Kodak out of the market after 10 years).
      - **50c. Gaulle's *Force de Frappe* vs. U.S. Nuclear Umbrella** (l. 6226; France/NATO vs. USSR; `brinkmanship`; de Gaulle built an independent French nuclear deterrent because he doubted the US would sacrifice New York to save Paris).
      - **50d. Deathbed Secret / Hostage / *Iphigenia in Aulis*** (l. 6245; Agamemnon vs. Menelaus in Euripides's *Iphigenia in Aulis*; `other`; once Menelaus reads Agamemnon's secret letter canceling the sacrifice of Iphigenia, Agamemnon cannot kill him to keep the secret).
      - **50e. *Dr. Strangelove* Doomsday Machine** (l. 6447; USSR Premier Dimitri Kissov vs. US; `brinkmanship`; buried cobalt-thorium G bombs wired to a computer to destroy all life on Earth automatically if USSR is attacked; **Rule that changes best move**: keeping it secret until Monday's Party Congress makes it useless for deterrence on Friday! `"The whole point of the Doomsday Machine... is lost... if you keep it a secret! Why didn’t you tell the world, eh?"`, l. 6479).
      - **50f. Cutting the Salami / Moving in Small Steps** (l. 6515; Builder vs. Buyer progress payments; kidnappers sending daily proof-of-life; arms reduction inspections; `prisoners' dilemma` / `bargaining`; breaking a one-shot trust game into many small steps turns it into a repeated game where cheating at step 1 forfeits steps 2..$N$).
      - **50g. Delegation to an Agent: Union Negotiators, Parents in Front of Children, Real Estate Agent Commissions, and Airline Hijacking Policy** (l. 6547; `bargaining`; a real estate agent on a 6% commission loses only $600 if a house sells for $10,000 less and therefore urges the seller to cave in; in hijackings, leaving discretion to the pilot forces the pilot to capitulate to save passengers on board, whereas a strict government no-negotiation rule deters hijackings).
      - **50h. Undermining Your Opponent's Credibility: Ignorance / Cutting Communication Lines & General Israel Putnam's 1777 Spy Trial** (l. 6616; `bargaining`/`brinkmanship`; skipping town or having a blindfolded delegate refuses to hear a threat; when British General Sir Henry Clinton sent a ship under a white flag threatening retaliation if spy Edmund Palmer was executed, Gen. Israel Putnam wrote back `"Edmund Palmer, an officer in the enemy’s service, was taken as a spy lurking within our lines; he has been tried as a spy, condemned as a spy, and shall be executed as a spy; and the flag is ordered to depart immediately. P.S.—He has been accordingly executed"`, l. 6639).
      - **50i. Helping a Rival Save Face: 1986 Hijacking in Karachi & 1962 Turkish Missiles** (l. 6692; `brinkmanship`/`bargaining`; hiding concessions or keeping terrorists' identities secret lowers the opponent's reputational cost of backing down).
    - **Catastrophic Loss?**: Yes — global extinction (`Dr. Strangelove`), execution (`Edmund Palmer`), hijackings.

51. **Case Study: A Textbook Example of Credibility (College Textbook Publishers vs. Used-Book Market & Students)**
    - **Heading & First Line**: `"CASE STUDY: A TEXTBOOK EXAMPLE OF CREDIBILITY"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L6731-L6802)) — `"The size of the U.S. college textbook market is $7 billion (including $2 billion from used textbooks)."`
    - **Players, Moves, Timing**: 2 sides (Textbook publisher/authors vs. Students/Used-book stores). Moves: Publisher sets price of new textbook (`$100` vs. `$145`) and decides whether to release a revised edition after 1–2 years (killing the used-book resale value); students buy new or used. Sequential across years.
    - **Payoffs**: If a textbook is used for 2 years (4 semesters) and resold each semester with a 25% bookstore margin, a student expects to pay $145 initially and recoup $80 (net cost ~$65); if the publisher kills the old edition after Year 1 with a new edition, early buyers get stuck with worthless used books.
    - **Family**: `other` (durable-goods monopoly commitment problem, Coase conjecture).
    - **Best Move / Real People**: Because publishers cannot credibly promise *not* to bring out frequent new editions, students anticipate short edition lives and refuse to pay $145. Publishers could restore credibility by printing a guaranteed buyback price (`"We guarantee to buy back this edition for $50 after semester 2"`).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Offering a contractual buyback guarantee or bundling single-use online access codes: `"A publisher could credibly promise to keep an edition in print for, say, three years by offering to buy back the book at a guaranteed price during that window"` (l. 6782).
    - **Catastrophic Loss?**: No.

---

### Chapter 8 — Interpreting and Manipulating Information

52. **The Marrying Kind? (Sue's Prenuptial Screening of Her Fiancé)**
    - **Heading & First Line**: `"THE MARRYING KIND?"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L6902-L6966)) — `"True story: Our friend, whom we’ll call Sue, was in love."`
    - **Players, Moves, Timing**: 2 players (Sue [wealthy] vs. Her Beau [two possible hidden types: True Lover or Gold Digger]). Moves: Sue proposes a prenuptial agreement waiving claims to her fortune; Beau signs or breaks off engagement. Sequential.
    - **Payoffs**: True Lover cares about Sue and signs; Gold Digger cares only about her money and walks away.
    - **Family**: `signalling` (screening).
    - **Best Move / Real People**: Demand the prenuptial agreement as a screening device. Real outcome: When Sue asked him to sign a prenup, her beau refused and broke off the engagement, revealing his type!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Requiring a prenuptial agreement removes the monetary prize for a gold digger (`"By taking the money off the table, she ensured that he would marry her only if he loved her for herself"`, l. 6951).
    - **Catastrophic Loss?**: Losing half of one's fortune in a divorce.

53. **King Solomon's Dilemma (1 Kings 3:16–28: Two Women Claiming One Baby)**
    - **Heading & First Line**: `"KING SOLOMON’S DILEMMA"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L6967-L6993); see also Ch. 14 `"KING SOLOMON’S DILEMMA REDUX"`, [l. 12521](file:///home/masih/Work/tries/aos/book-full.txt#L12521-L12580)) — `"Two women came before King Solomon, disputing who was the true mother of a baby."`
    - **Players, Moves, Timing**: 3 players (King Solomon, True Mother, Impostor). Moves: Solomon proposes to cut the living child in two and give half to each; True Mother offers to give the live baby to the other woman; Impostor says `"Let it be neither mine nor thine, but divide it."` Sequential.
    - **Payoffs**: True mother values the baby's life above all; Impostor is envious and prefers a dead baby (`0, 0`) to seeing the True Mother have the baby.
    - **Family**: `signalling` (mechanism design / screening).
    - **Best Move / Real Behavior**: Solomon awards the baby to the woman who begged to spare its life.
    - **THE RULE THAT CHANGES THE BEST MOVE**: What if the Impostor is strategic and *also* begs to spare the child's life? In Ch. 14 (`"KING SOLOMON’S DILEMMA REDUX"`, l. 12521), if True Mother values the child at `$1,000` and Impostor values it at `$200`, Solomon runs a mechanism where if both claim the child, each woman must pay a `$500` fine while the child is awarded by lottery (or auctioned against a third benchmark): `"If the impostor knows game theory, she can anticipate how Solomon will interpret the answers and mimic the true mother’s response"` (l. 6990 & l. 12521).
    - **Catastrophic Loss?**: Yes — death of the baby (`"Divide the living child in two"`).

54. **Akerlof's Market for Lemons (Used Cars), Adverse Selection in Health/Auto Insurance, and Signet Bank Credit Card Screening**
    - **Heading & First Line**: `"IS THE QUALITY GUARANTEED?"` & `"A LITTLE HISTORY"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L7072-L7278)) — `"Suppose you want to buy a used car."`
    - **Players, Moves, Timing**: Seller vs. Buyer (used cars); Insurer vs. Policyholders; Signet Bank vs. Credit Card Borrowers (`"deadbeats"` who pay in full, `"revolvers"` who carry balances and pay interest, and `"defaults"` who never pay back). Sequential.
    - **Payoffs**: In Akerlof's used-car market, good cars are worth more to owners than the average price buyers will pay for an unverified car, so good cars exit and the market unravels. In credit cards, Signet Bank offered a low-interest balance-transfer teaser rate, which attracted `"revolvers"` (who had large balances to transfer) while leaving `"deadbeats"` (who had zero balance) uninterested.
    - **Family**: `signalling` (adverse selection & screening).
    - **Best Move / Real People**: Sellers of high-quality cars offer warranties; insurers offer high-deductible vs. low-deductible menus; Signet Bank used balance-transfer offers and rose from a small regional Virginia bank into Capital One.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Conditioning the discount on transferring an existing balance (`"To benefit from a lower interest rate on balances, you have to have a balance"`, l. 7257), turning adverse selection into positive selection.
    - **Catastrophic Loss?**: Complete market collapse (`"complete breakdown of the market, as in Akerlof’s example"`, l. 14127).

55. **Screening and Signaling in Job Markets: The MBA Signaling Game ("One Reason to Get an MBA" & "A Trip to the Bar")**
    - **Heading & First Line**: `"SCREENING AND SIGNALING"`, `"ONE REASON TO GET AN MBA:"`, `"A TRIP TO THE BAR"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L7279-L7643) & fn [l. 14133](file:///home/masih/Work/tries/aos/book-full.txt#L14133-L14138)) — `"You are the chief personnel officer of a company, looking to recruit bright new managers."`
    - **Players, Moves, Timing**: Employer vs. Job Candidates (two hidden types: **Talented [$T$]** and **Untalented [$U$]**). Sequential.
    - **Payoffs**: All numbers given explicitly in prose (l. 7303–7630):
      - Annual productivity: Talented = `$130,000/yr`; Untalented = `$50,000/yr`. Career length with firm = `5 years` (or `N` years).
      - Tuition/opportunity cost of a 1-year MBA = `$40,000`.
      - Pass probability in MBA program: Talented passes `100%` of the time; Untalented passes only `50%` of the time (`"half of the time the untalented will fail out"`, l. 7590).
      - Over a 5-year career (`"ONE REASON TO GET AN MBA"`, l. 7360):
        - If firm pays `$130,000/yr` to MBA holders and `$50,000/yr` to non-MBAs, the 5-year wage premium for an MBA is $5 \times (\$130k - \$50k) = \$400,000$ for Talented (net gain $\$400k - \$40k = \$360k$), and for Untalented expected 5-year wage gain is $0.5 \times \$400,000 = \$200,000 > \$40,000$ tuition! Wait: in the 1-year salary or 5-year `$80,000` total bonus version (`"A TRIP TO THE BAR"`, l. 7574 & fn l. 14133), if the total career premium for an MBA is `$80,000` (e.g., `$16,000/yr` for 5 years, or 1 year at `$130k` vs. `$50k`), then Talented nets $\$80,000 - \$40,000 = +\$40,000$, while Untalented expects $0.5 \times \$80,000 - \$40,000 = \$0$ (indifferent!).
      - *Mixed-Strategy / Hybrid Equilibrium (`"A TRIP TO THE BAR"`, l. 7574)*: Suppose population is `50% Talented, 50% Untalented`, MBA costs `$40,000`, and pass rate for Untalented is `50%` (1 year of work). If all Talented (`100%`) and `50%` of Untalented enter the MBA program, then for every `100` Talented and `100` Untalented, `100` Talented and `50` Untalented enroll; `100` Talented and `25` Untalented graduate with an MBA (`80%` of MBAs are Talented -> average productivity $= 0.8 \times \$130k + 0.2 \times \$50k = \$114,000$). But to make Untalented indifferent at `$40,000` tuition with `50%` pass rate, the MBA wage must be `$130,000` (`$80,000` above `$50,000`), which only holds if `0%` of Untalented enroll; if MBA tuition is `$32,000`, Untalented need an `$64,000` premium (wage `$114,000`), which happens when exactly `50%` of Untalented enroll!
    - **Family**: `signalling`. (Also in passing at l. 7451: `"Signaling by Not Signaling"` — Sherlock Holmes's *Silver Blaze* dog that didn't bark in the night, entrepreneurs keeping 50% equity in their own company, and a genius job candidate showing up in jeans because the airline lost his luggage, fn l. 14137).
    - **Best Move / Real People**: Differential cost/difficulty of the signal separates types (`"For a signal to be credible, it must be too costly or unprofitable for a pretender to mimic"`).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Differential pass rate or psychic cost between Talented and Untalented (`"half of the time the untalented will fail out"`, l. 7590), plus the ratio of MBA cost to post-MBA career length.
    - **Catastrophic Loss?**: Paying `$40,000` tuition and failing out without a degree.

56. **Bodyguard of Lies: WWII Calais vs. Normandy Deception & Simplified Poker Bluffing Game**
    - **Heading & First Line**: `"BODYGUARD OF LIES"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L7644-L7740)) — `"Espionage in wartime provides particularly good examples of strategies for concealing and ferreting out information."`
    - **Players, Moves, Timing**:
      - *WWII D-Day Deception (l. 7651)*: Allies vs. Germany (Allies leaked genuine minor secrets to double agents in England to build credibility before feeding false reports that the main invasion would hit Pas de Calais rather than Normandy).
      - *Simplified Poker Bluffing Game (l. 7679)*: 2 players (**You** vs. **Rival**). Each puts `$1` ante in the pot. You draw a card that is equally likely (`50:50`) to be **High ($H$)** or **Low ($L$)**; Rival's card is effectively fixed in the middle (so $H$ always beats Rival and $L$ always loses to Rival). You observe your card and choose **Raise `$2`** or **Fold** (if you Fold, Rival wins the `$2` pot -> you get `-1`, Rival gets `+1`). If you Raise `$2`, Rival chooses **See (`$2`)** or **Fold** (if Rival folds, you win the `$2` pot -> `+1` to you, `-1` to Rival; if Rival sees, `$6` total pot goes to $H$ -> `+3/-3` if you have $H$, `-3/+3` if you have $L$). Sequential with private information.
    - **Payoffs**: Strategy table at l. 7708 and expected payoff table at l. 7721 (`table not in text`), exact numbers in prose (l. 7696–7738):
      - Your pure strategies: **Honest** (`Raise if H, Fold if L`) vs. **Bluff** (`Raise if H, Raise if L`).
      - Rival's pure strategies against a Raise: **See** vs. **Fold**.
      - Expected payoffs (averaging 50:50 over $H$ and $L$):
        - `(Honest, See)`: `0.5*(+3) + 0.5*(-1) = +1` for You, `-1` for Rival
        - `(Honest, Fold)`: `0.5*(+1) + 0.5*(-1) = 0` for You, `0` for Rival
        - `(Bluff, See)`: `0.5*(+3) + 0.5*(-3) = 0` for You, `0` for Rival
        - `(Bluff, Fold)`: `0.5*(+1) + 0.5*(+1) = +1` for You, `-1` for Rival
    - **Family**: `signalling` / `zero-sum mixing`.
    - **Best Move / Real People**: In the mixed-strategy equilibrium, You always Raise with $H$ (`100%`) and Bluff (Raise with $L$) **`1/3` of the time** (choosing `Honest 2/3, Bluff 1/3`); Rival Sees **`2/3` of the time** and Folds **`1/3` of the time**. Your expected payoff is **`+1/3` of a dollar** per hand (`+33.3 cents`, better than the `0` you would get if you never bluffed and Rival always folded!).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Having private information (`H` vs. `L`) and mixing bluffs (`1/3` of low hands) so Rival is forced to call `2/3` of the time on your high hands: `"The point of bluffing with a weak hand is to get the other player to call you when you have a strong hand"` (l. 7735).
    - **Catastrophic Loss?**: Losing `$3` on a called bluff (or losing France in D-Day).

57. **Price Discrimination by Screening & Trip to the Gym No. 5 (PITS Airline First Class vs. Economy Pricing)**
    - **Heading & First Line**: `"PRICE DISCRIMINATION BY SCREENING"` & `"TRIP TO THE GYM NO. 5"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L7741-L7934), Workout [l. 13084](file:///home/masih/Work/tries/aos/book-full.txt#L13084-L13092)) — `"The application of the concept of screening that most impinges on your wallet every day is sellers’ use of different variants of goods"`
    - **Players, Moves, Timing**: 1 monopolist seller (**People in Tight Seats [PITS] Airline**) vs. 2 groups of buyers (`50 Business travelers` and `50 Tourist travelers`). Sequential (PITS sets First-Class and Economy prices; travelers self-select).
    - **Payoffs**: Willingness-to-pay table at l. 7830 is an image (`table not in text`), exact numbers in prose (l. 7832–7925 & l. 13084):
      - Unit cost to airline: `$150` per First-Class seat; `$100` per Economy seat.
      - Willingness to pay (WTP):
        - **Tourist (50)**: Economy = `$200`, First Class = `$225` (extra comfort worth `$25`).
        - **Business (50)**: Economy = `$300`, First Class = `$400` (extra comfort worth `$100`).
    - **Family**: `signalling` (second-degree price discrimination / self-selection screening).
    - **Best Move / Real People**:
      - Naive pricing (`$400` First Class, `$200` Economy) fails because Business travelers get `$300 - $200 = $100` surplus in Economy vs. `$400 - $400 = $0` in First Class, so Business travelers buy Economy!
      - To satisfy the self-selection (incentive-compatibility) constraint, PITS must charge `$200` for Economy (giving Tourists `$0` surplus and Business `$100` surplus if they switch) and **`$300` for First Class** (giving Business `$400 - $300 = $100` surplus so they stay in First Class). Total profit $= 50 \times (\$300 - \$150) + 50 \times (\$200 - \$100) = \$7,500 + \$5,000 = \$12,500$ (which beats selling First Class only to Business at `$400`: $50 \times (\$400 - \$150) = \$12,500$, or in `"TRIP TO THE GYM NO. 5"` [l. 7892 & 13084] when Business WTP for Economy is `$310` and First Class is `$400`, setting Economy = `$200` and First Class = `$290` gives profit $50 \times (\$290-\$150) + 50 \times (\$200-\$100) = \$12,000$, whereas cutting out Tourists and charging `$400` for First Class yields $50 \times \$250 = \$12,500$!).
      - Also cited: IBM's LaserPrinter E (identical to the 10-page/minute LaserPrinter except for a chip inserted to slow it down to 5 pages/minute, l. 7782) and airline Saturday-night stay requirements.
    - **THE RULE THAT CHANGES THE BEST MOVE**: In `"TRIP TO THE GYM NO. 5"` (l. 7892 & l. 13084), if Business travelers' willingness to pay for Economy rises above `$300` (say to `$310`), or if there are fewer than 50 Tourists, the discount required on First Class to keep Business travelers out of Economy becomes too large, so PITS drops Tourists altogether and charges `$400` (`"if there are only a few customers with low willingness to pay, the seller may do better to abandon that segment of the market altogether"`, l. 7922).
    - **Catastrophic Loss?**: No.

58. **Case Study: Going Undercover (Sweatbath Screening of Illegal Immigrants in New York)**
    - **Heading & First Line**: `"CASE STUDY: GOING UNDERCOVER"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L7935-L7966)) — `"Another friend of ours, Tanya, is an anthropologist."`
    - **Players, Moves, Timing**: 2 sides (Community of Mexican undocumented immigrants in New York vs. Anthropologist Tanya / potential undercover INS agents). Moves: Community requires newcomers to endure a blistering Mesoamerican *temazcal* sweatbath before admitting them to social trust; newcomer endures or quits. Sequential.
    - **Payoffs**: Acceptance into community trust vs. painful heat exhaustion.
    - **Family**: `signalling` (costly screening / initiation rite).
    - **Best Move / Real People**: Because rural Mexican migrants are accustomed to the *temazcal* while American undercover agents find it nearly unbearable, the sweatbath screens out outsiders (`"the cost of enduring the sweatbath is much lower for genuine members of the group than for impostors"`, l. 7956).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Differential endurance cost between true group members and undercover agents.
    - **Catastrophic Loss?**: Deportation if an INS agent infiltrates the community.

---

### Chapter 9 — Cooperation and Coordination

59. **For Whom the Bell Curve Tolls (Ivy League Football Practice Rules, Classroom Grade Inflation, and Track Relay Starts)**
    - **Heading & First Line**: `"FOR WHOM THE BELL CURVE TOLLS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L7975-L8040)) — `"In the 1950s the Ivy League colleges were faced with a problem."`
    - **Players, Moves, Timing**: $N = 8$ Ivy League colleges (or $N$ students in a curve-graded class, or $N$ academic departments inflating grades to attract enrollees). Moves: Limit spring football practice / study hours / grade generosity vs. practice more / study harder / give easy A's. Simultaneous / repeated.
    - **Payoffs**: Relative rank in football standings or class curve is zero-sum, while extra hours spent practicing reduce study/leisure time for all players.
    - **Family**: `prisoners' dilemma` (multiperson rat race).
    - **Best Move / Real People**: Without an external rule, every school practices more and lands in the same relative standings with worse academics; the 8 Ivy League presidents signed an enforceable pact banning spring football practice.
    - **THE RULE THAT CHANGES THE BEST MOVE**: An enforceable collective agreement across all competitors: `"An escape from the horns of this dilemma requires an enforceable collective agreement"` (l. 8019).
    - **Catastrophic Loss?**: No.

60. **The Route Less Traveled & Catch-22? (Bay Bridge vs. BART Commuting Congestion & QWERTY vs. DSK Keyboards)**
    - **Heading & First Line**: `"THE ROUTE LESS TRAVELED"` & `"CATCH-22?"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L8041-L8315) & fn [l. 14142](file:///home/masih/Work/tries/aos/book-full.txt#L14142-L14144); see also Ch. 14 `"BAY BRIDGE"`, [l. 12581](file:///home/masih/Work/tries/aos/book-full.txt#L12581-L12614)) — `"There are two main ways to commute from Berkeley to San Francisco."`
    - **Players, Moves, Timing**: Continuum / $N = 10,000$ commuters (or typists choosing **QWERTY** vs. **Dvorak Simplified Keyboard [DSK]**). Simultaneous.
    - **Payoffs**: Graphs at l. 8070, 8115, 8221, 8256, 8281 are images (`table not in text`), exact numbers and formulas in prose:
      - *Bay Bridge vs. BART (l. 8041–8135)*: `10,000` commuters. BART train takes a constant **`40 minutes`** regardless of riders. Driving across the Bay Bridge takes **`20 minutes`** with zero traffic, plus **`5 minutes` for every `1,000` cars** ($T_{\text{car}} = 20 + 5n$, where $n$ is thousands of drivers).
        - *Individual Equilibrium*: Drivers enter until $T_{\text{car}} = 40 \implies n = 4$ (`4,000` drivers, `6,000` BART riders); **everyone's commute is `40 minutes`** (`400,000` total commuter-minutes).
        - *Social Optimum*: When $n = 2$ (`2,000` drivers, `8,000` BART riders), drivers take **`30 minutes`** and saved time is $2,000 \times 10 = 20,000$ minutes (`38` minutes average across all 10,000 commuters; each extra driver beyond 2,000 saves himself `<10` minutes while imposing `5` minutes per `1,000` on all existing drivers!).
      - *Ch. 14 Bay Bridge Accident Externality (`"BAY BRIDGE"`, l. 12581)*: 4 lanes, capacity `2,000 cars/lane/hour` = `8,000 cars/hr`. During rush hour, `10,000` cars arrive over 1 hour (building a queue that clears in `1.25 hours`). A driver whose car runs out of gas blocks 1 lane for `15 minutes` (reducing bridge flow by `500` cars for 15 minutes). By the `"shuffle to the back of the line"` trick, those `500` delayed cars each wait an extra `1.25 hours` = **`625 hours`** of total lost commuter time (`$12,500` social cost at `$20/hr`!).
      - *QWERTY vs. DSK Keyboards (`"CATCH-22?"`, l. 8137)*: DSK is intrinsically faster than QWERTY when everyone uses it (`100% DSK > 100% QWERTY`), but compatibility/network externalities create two stable equilibria (`~98% QWERTY` [fn l. 14142] and `100% DSK`) separated by an unstable tipping point at **`30% QWERTY`** (`70% DSK`).
    - **Family**: `commons` / `prisoners' dilemma` (Bay Bridge congestion) and `tipping` / `coordination (stag hunt, meeting)` (QWERTY vs. DSK).
    - **Best Move / Real People**: Commuters drive until bridge time equals BART's 40 minutes; typists stick with QWERTY because $>30\%$ already use QWERTY.
    - **THE RULE THAT CHANGES THE BEST MOVE**:
      - On the Bay Bridge: Charging a **$5 congestion toll** (equal to the 10-minute marginal external delay cost at $30/hr) shifts equilibrium from `4,000` drivers to the optimal `2,000` drivers (l. 8121), or when the Bay Bridge closed for a month after the 1989 earthquake (l. 8306), commuters were forced onto BART and some stayed after reopening!
      - For QWERTY vs. DSK: Pushing adoption past the **`30%` tipping point** shifts the stable equilibrium from QWERTY to DSK.
    - **Catastrophic Loss?**: No.

61. **Faster Than a Speeding Ticket (Highway Speeding Equilibrium)**
    - **Heading & First Line**: `"FASTER THAN A SPEEDING TICKET"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L8316-L8409) & fn [l. 14145](file:///home/masih/Work/tries/aos/book-full.txt#L14145-L14146)) — `"Why do almost all drivers exceed the speed limit on the highway?"`
    - **Players, Moves, Timing**: $N$ drivers vs. Highway Patrol. Moves: Obey the 55 mph speed limit vs. speed at 65 mph. Simultaneous.
    - **Payoffs**: Graph at l. 8351 is an image (`table not in text`), prose explains: When very few drivers speed, police easily catch every speeder (so obeying is best); when almost everyone speeds, police capacity is swamped so any individual speeder's chance of getting a ticket is tiny, AND driving 55 mph while everyone else drives 65 mph is dangerous!
    - **Family**: `tipping` / `coordination (stag hunt, meeting)`.
    - **Best Move / Real People**: Two stable equilibria: **Law-Abiding** (almost nobody speeds) and **Law-Breaking** (almost everyone speeds), separated by an unstable tipping threshold.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Temporarily flooding the highway with police or automated speed cameras to push the fraction of speeders below the tipping point, after which a small patrol force can maintain the law-abiding equilibrium (`"Once the new equilibrium is reached, the police force can be scaled back to its original size, and the law-abiding behavior will sustain itself"`, l. 8384).
    - **Catastrophic Loss?**: Highway crashes from speed differentials.

62. **Why Did They Leave? (Schelling's Neighborhood Tipping / Segregation & City vs. Country Migration)**
    - **Heading & First Line**: `"WHY DID THEY LEAVE?"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L8410-L8521)) — `"American cities have few racially integrated neighborhoods."`
    - **Players, Moves, Timing**: Continuum of residents of two groups (e.g., `70%` Group A and `30%` Group B; or rural vs. urban workers). Moves: Stay vs. Move out. Sequential / dynamic.
    - **Payoffs**: Graphs at l. 8445 and l. 8505 are images (`table not in text`), prose gives numbers: Even if everyone prefers an integrated `70:30` neighborhood over complete segregation, if variations in tolerance mean the `70:30` point has an upward-sloping dynamic response, any tiny perturbation tips the neighborhood to `100%` Group A or `100%` Group B! In urban-rural migration (l. 8495), as cities grow too large, congestion lowers urban utility below rural utility, creating a stable interior equilibrium.
    - **Family**: `tipping`.
    - **Best Move / Real People**: Individual moves driven by local composition tip neighborhoods to total segregation (`100:0` or `0:100`), even though everyone prefers `70:30` integration.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Whether the feedback curve crosses the 45-degree line from above (negative feedback -> stable interior equilibrium, as in urban-rural migration) or from below (positive feedback -> unstable tipping point, as in Schelling's segregation model).
    - **Catastrophic Loss?**: Complete unraveling of integrated communities.

63. **It Can Be Lonely at the Top (Up-or-Out Law Firm Partnerships vs. Tenured Professors in Recruitment)**
    - **Heading & First Line**: `"IT CAN BE LONELY AT THE TOP"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L8522-L8621)) — `"Top law firms generally choose their partners from among their junior associates."`
    - **Players, Moves, Timing**: Existing senior partners/professors of quality level $B$ deciding whether to hire/promote a candidate of higher quality $A$ vs. inferior quality $C$. Sequential across generations.
    - **Payoffs**: If existing $B$-level members fear being displaced or outshone by $A$-level newcomers, $B$'s hire $C$'s, and $C$'s later hire $D$'s, causing organizational quality to spiral downward.
    - **Family**: `other` (organizational adverse selection / dynamic institutional design).
    - **Best Move / Real People**: Granting job security (academic tenure or law-firm senior partnership) removes the incumbent's fear of being displaced by a brilliant recruit.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Providing tenure / guaranteed partnership security to the existing decision-makers: `"Because tenured professors don’t have to worry about being fired and replaced by the smart young recruits, they have every incentive to hire the very best people they can find"` (l. 8572).
    - **Catastrophic Loss?**: Institutional decay (`B` hires `C`, `C` hires `D`).

64. **Politicians and Apple Cider (Hotelling's Linear Beach Vendors: 2, 3, and 4 Vendors)**
    - **Heading & First Line**: `"POLITICIANS AND APPLE CIDER"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L8622-L8677)) — `"Two political parties are trying to choose their positions on the liberal-conservative spectrum."`
    - **Players, Moves, Timing**: 2, 3, or 4 apple-cider vendors (or political candidates) locating along a 1-mile beach with customers distributed uniformly; prices are fixed and each bather walks to the nearest vendor. Simultaneous.
    - **Payoffs**: Market share = fraction of beach closest to vendor (ties split equally).
    - **Family**: `other` (Hotelling spatial competition / median voter).
    - **Best Move / Real People**:
      - **$N = 2$ vendors**: Unique Nash equilibrium is both locating back-to-back at the exact center (`1/2`, splitting `50%` each), even though locating at `1/4` and `3/4` would cut average customer walking distance in half (`1/8` mile vs. `1/4` mile)!
      - **$N = 3$ vendors**: **No pure-strategy Nash equilibrium!** If two are at the center, the third moves just outside one of them; if two are flanking the third in the middle, the middle vendor is squeezed and jumps outside one of the flankers in an endless cycle.
      - **$N = 4$ vendors**: Unique equilibrium has two vendors paired at **`1/4`** and two paired at **`3/4`** (`25%` share each).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Changing the number of competitors from $N = 2$ (unique center equilibrium) to $N = 3$ (`"With three vendors, there is no stable equilibrium at all!"`, l. 8664) to $N = 4$ (paired equilibrium at the quartiles `1/4` and `3/4`).
    - **Catastrophic Loss?**: Being squeezed in the middle with near-zero market share when $N = 3$.

65. **Case Study: A Prescription for Allocating Dentists (Al Roth's Medical/Dental Residency Match & Marshall vs. Rhodes Scholarships)**
    - **Heading & First Line**: `"CASE STUDY: A PRESCRIPTION FOR ALLOCATING DENTISTS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L8733-L8824) & fn [l. 14245](file:///home/masih/Work/tries/aos/book-full.txt#L14245-L14249)) — `"In this case study, we explore the coordination problem of how the market for new dentists works"`
    - **Players, Moves, Timing**: $N$ hospitals/dental programs and $M$ graduating students (also federal appellate judges hiring law clerks, college early-decision admissions, and Marshall vs. Rhodes Scholarships in fn l. 14245). Moves: Make exploding job offers earlier and earlier (junior year, sophomore year) vs. participate in a centralized clearinghouse (National Resident Matching Program). Sequential.
    - **Payoffs**: Exploding early offers force matches before student quality and preferences are known, leading to mismatched careers.
    - **Family**: `coordination (stag hunt, meeting)` / `duel or preemption` (market unraveling).
    - **Best Move / Real People**: Without a clearinghouse, unraveling is a prisoners'/preemption dilemma; Al Roth redesigned the NRMP deferred-acceptance matching algorithm so no hospital-student pair prefers each other over their assigned match (`"stable matching"`). (In fn l. 14245, the Marshall Scholarship deliberately moves *second* via a waitlist so candidates who win both Marshall and Rhodes take the Rhodes at zero cost to Marshall).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Using a centralized deferred-acceptance matching algorithm that produces a stable outcome so no participant gains by jumping the gun (`"the outcome of the centralized clearinghouse must be stable, in the sense that there is no applicant-employer pair who both prefer each other to the match they got"`, l. 8794).
    - **Catastrophic Loss?**: Market unraveling and bad career matches.

---

### Chapter 10 — Auctions, Bidding, and Contests

66. **English, Japanese, and Vickrey Second-Price Auctions (1985 Sydney Opera Phantom Bid, Goethe's 1797 Auction, & Trip to the Gym No. 6)**
    - **Heading & First Line**: `"ENGLISH AND JAPANESE AUCTIONS"`, `"VICKREY AUCTION"`, `"TRIP TO THE GYM NO. 6"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L8860-L9003), Workout [l. 13093](file:///home/masih/Work/tries/aos/book-full.txt#L13093-L13104), & fn [l. 14163](file:///home/masih/Work/tries/aos/book-full.txt#L14163-L14167)) — `"A true story from Sydney, Australia illustrates the buyer’s dilemma."`
    - **Players, Moves, Timing**: Seller/Auctioneer + $N$ bidders.
      - *1985 Sydney Real Estate Auction (l. 8860)*: Buyer stops bidding at `A$1.55M`; auctioneer invents a phantom bid of `A$1.6M` (`"pulled a bid off the chandelier"`), passes the house in, and then offers it to the buyer at `A$1.6M` (`$50,000` over the real second-highest bid).
      - *Japanese Button Auction (l. 8913)*: Price rises continuously on a screen while all bidders hold down a button; releasing the button exits irreversibly; last bidder holding the button wins at the price where the runner-up released.
      - *Vickrey Sealed-Bid Second-Price Auction (l. 8937)*: Bidders submit sealed bids; highest bidder wins and pays the *second-highest* bid (used by Goethe in 1797 when selling his epic poem *Hermann und Dorothea* to publisher Vieweg, fn l. 14165).
      - *Trip to the Gym No. 6 (l. 8973 & Workout l. 13093)*: How much would you pay to spy on rivals' bids in a Vickrey auction vs. a first-price sealed-bid auction?
    - **Family**: `auction`.
    - **Best Move / Real People**: In a private-value Vickrey or Japanese auction, bidding your true valuation is a weakly dominant strategy (`"bidding your true value is a dominant strategy"`, l. 8958), so in Trip to the Gym No. 6 you would pay **`$0`** to learn rivals' bids in a Vickrey auction!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Paying the *second-highest* bid rather than your own bid decouples the price you pay from the bid you submit (`"Because what you bid only determines whether you win, and not what you pay when you win, you have no incentive to shade your bid below your true value"`, l. 8961).
    - **Catastrophic Loss?**: Overpaying above true value if a bidder bids above valuation (`"THE RISK OF WINNING"`, Ch. 14 l. 12296).

67. **Revenue Equivalence & The Third-Price Auction Paradox**
    - **Heading & First Line**: `"REVENUE EQUIVALENCE"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L9004-L9068) & fn [l. 14168](file:///home/masih/Work/tries/aos/book-full.txt#L14168-L14172)) — `"At this point, you may have figured out that the Vickrey auction gets you the same outcome as an English auction"`
    - **Players, Moves, Timing**: $N$ bidders with independent private values uniformly distributed on $[0, 100]$. Simultaneous sealed bids.
    - **Payoffs**: Highest bidder wins and pays the 1st-highest, 2nd-highest, or 3rd-highest bid.
    - **Family**: `auction`.
    - **Best Move / Real People**:
      - *1st-price*: Shade bid below true value ($B = \frac{N-1}{N} V$).
      - *2nd-price (Vickrey)*: Bid exact true value ($B = V$).
      - *3rd-price*: Bid *above* your true value ($B = \frac{N-1}{N-2} V$)! By Roger Myerson's Revenue Equivalence Theorem, all three yield the exact same expected revenue to the seller.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Changing the payment rule from 1st-price (underbid) to 2nd-price (bid true value) to 3rd-price (`"In a third-price auction, everyone will bid above his or her true value!"`, l. 9046).
    - **Catastrophic Loss?**: In a 3rd-price auction, if the 2nd and 3rd bids both exceed your true value, the winner pays more than the item is worth.

68. **Online Auctions: eBay Proxy Bidding, Bidding Wars ($26 / $33 / $100), Shill Bidding, and Sniping**
    - **Heading & First Line**: `"ONLINE AUCTIONS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L9069-L9165)) — `"The most common auction experience today is on eBay."`
    - **Players, Moves, Timing**: Bidders $A, B, C$ + Seller on eBay over a fixed time window (e.g., 7 days).
    - **Payoffs**: Example (l. 9085): $A$ bids `$26`, $B$ bids `$33`, $C$ enters proxy max of `$100` (with `$1` bid increment). $C$ wins at **`$34`** (`$33 + $1`). In common-value/uncertain-value items (e.g., rare coin), bidding early reveals information and triggers a bidding war.
    - **Family**: `auction` / `signalling`.
    - **Best Move / Real People**: Wait until the closing seconds of the auction to submit your true maximum bid (**sniping**). Real people: Experienced eBay bidders snipe in the final seconds (and 19th-century wine auctions used a burning candle to prevent sniping, ending whenever the flame went out, l. 9160; Amazon extends the auction by 10 minutes after any late bid).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Hard closing deadline (eBay) vs. automatic 10-minute overtime extension (Amazon) or random candle flame: `"Because eBay has a fixed ending time, bidding at the very last moment—called sniping—prevents other bidders from responding to your bid"` (l. 9132).
    - **Catastrophic Loss?**: No.

69. **Bidding As If You've Won: The ACME Takeover Winner's Curse Game (plus Procurement Highway Variant)**
    - **Heading & First Line**: `"BIDDING AS IF YOU’VE WON"` & `"ACME"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L9166-L9245) & fns [l. 14174](file:///home/masih/Work/tries/aos/book-full.txt#L14174-L14182)) — `"A powerful idea in game theory is the concept of acting like a decision matters only when it matters."`
    - **Players, Moves, Timing**: 2 players (You [acquirer] vs. Current Owner of ACME; plus variant where ACME is worth `$2M–$10M`). Moves: You make a take-it-or-leave-it cash offer `$X`; ACME's owner (who knows the true value $V$) accepts if and only if $X \ge V$. Sequential.
    - **Payoffs**:
      - *Base Game (`$0 to $10 million`, l. 9188)*: True value $V$ to current owner is uniformly distributed between **`$0` and `$10 million`** (average `$5M`). Under your management, ACME will be worth **`50%` more** (`1.5 V`).
        - If you offer `$X`, owner accepts only when $V \le X$, so conditional on acceptance, expected true value is $E[V \mid V \le X] = X/2$, and expected value to you is $1.5 \times (X/2) = 0.75 X < X$! **Every positive bid `$X > 0$` loses `25 cents` on the dollar on average!**
      - *Variant (`$2 million to $10 million`, l. 9228 & fn l. 14174)*: True value $V$ is uniformly distributed between **`$2M` and `$10M`**. Conditional on acceptance of bid `$X` ($2 \le X \le 10$), average value to owner is $(2 + X)/2$, and value to you is $1.5 \times (2 + X)/2 = 0.75(2 + X)$. Breakeven ($X = 0.75(2 + X)$) is **`$X = $6 million`**, and any bid between `$2M` and `$6M` is profitable!
      - *Procurement Highway Variant (fn l. 14178)*: Your cost to build a highway is `$10 million`; never bid `$9 million` below cost or winning paves the way to bankruptcy.
    - **Family**: `auction` / `bargaining` (winner's curse / adverse selection).
    - **Best Move / Real People**: In the `$0–$10M` game, bid **`$0`** (do not bid!). Real people (even MBA students and executives) routinely bid `$5M–$7.5M` and lose money (`"Winner's Curse"`).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Whether the minimum possible value $V_{\min}$ is `$0` (so $1.5 \times (0 + X)/2 = 0.75X < X$, making all positive bids unprofitable) vs. $V_{\min} = \$2\text{M} > 0$ (making bids up to `$6M` profitable, fn l. 14174).
    - **Catastrophic Loss?**: Yes — massive overpayment / bankruptcy (`"paving the way to your own bankruptcy"`, fn l. 14182; e.g., Campeau's bankruptcy after buying Federated Department Stores).

70. **First-Price Sealed-Bid Auctions, Dutch Auctions, Treasury Bills (1991 Salomon Brothers Corner), and Trip to the Gym No. 7**
    - **Heading & First Line**: `"SEALED-BID AUCTIONS"`, `"DUTCH AUCTIONS"`, `"TRIP TO THE GYM NO. 7"`, `"T-BILLS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L9246-L9448), Workout [l. 13105](file:///home/masih/Work/tries/aos/book-full.txt#L13105-L13152), & fns [l. 14188](file:///home/masih/Work/tries/aos/book-full.txt#L14188-L14200)) — `"The rules of a sealed-bid auction are simple. Everyone puts his or her bid in a sealed envelope"`
    - **Players, Moves, Timing**: $N$ bidders with private values on $[0, 100]$ (or `[0, V]`):
      - *Sealed-Bid First-Price & Dutch Clock Auction*: Highest bidder (or first to stop the descending price clock, as in Dutch flower auctions, Filene's Basement, and Google's IPO) wins and pays their own bid.
      - *Trip to the Gym No. 7 (l. 9341 & Workout l. 13105)*: Derive optimal sealed-bid shading with $N$ bidders ($B = \frac{N-1}{N}V$; e.g., if your value is `$60`, bid **`$30`** against 1 rival, **`$40`** against 2 rivals, **`$45`** against 3 rivals, fn l. 14188), and when values are uniform on `[$100, $200]` against 1 rival, bid `$100 + 0.5(V - 100) = 50 + 0.5V`.
      - *U.S. Treasury Bill Auctions (l. 9387)*: Discriminatory (pay-your-bid) vs. Uniform-Price (everyone pays the market-clearing cutoff rate). In May 1991, Salomon Brothers submitted unauthorized bids in customers' names to corner `94%` of a two-year Treasury note issue (violating the `35%` single-bidder cap), nearly destroying the firm and prompting the Treasury (led by Milton Friedman's argument) to switch to uniform-price auctions.
    - **Family**: `auction`.
    - **Best Move / Real People**: In first-price/Dutch auctions with $N$ bidders on $[0, 100]$, bid $\frac{N-1}{N}$ of your value.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Number of competing bidders $N$ (`"As the number of bidders increases, you can see that bids converge to valuations"`, fn l. 14190: $1/2 V \to 2/3 V \to 3/4 V \to V$), and uniform-price vs. discriminatory multi-unit pricing.
    - **Catastrophic Loss?**: Yes — Salomon Brothers' near-collapse and CEO John Gutfreund's ouster in 1991 (`"Salomon was fined $290 million, and its top executives were forced to resign"`, l. 9418).

71. **The Preemption Game (Apple Newton vs. Sharp Wizard PDA, Pistol Duels, Wet-Sponge Duel, and Trip to the Gym No. 8)**
    - **Heading & First Line**: `"THE PREEMPTION GAME"` & `"TRIP TO THE GYM NO. 8"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L9449-L9530), Workout [l. 13153](file:///home/masih/Work/tries/aos/book-full.txt#L13153-L13173), & fn [l. 14201](file:///home/masih/Work/tries/aos/book-full.txt#L14201-L14202); see also Ch. 14 `"THE SAFER DUEL"`, [l. 12224](file:///home/masih/Work/tries/aos/book-full.txt#L12224-L12249), and `"THE THREE-WAY DUEL"`, [l. 12250](file:///home/masih/Work/tries/aos/book-full.txt#L12250-L12295)) — `"On August 3, 1993, Apple Computer launched the Original Newton MessagePad."`
    - **Players, Moves, Timing**: 2 players (Apple vs. rival PDA maker; or 2 duelists walking toward each other from distance $t=0$ where hit probabilities $p(t), q(t)$ increase continuously toward $1$; or Ben Polak's Yale classroom wet-sponge duel, fn l. 14201). Continuous-time sequential.
    - **Payoffs**: If Player 1 fires/launches at time $t$, Player 1 hits/wins with probability $p(t)$; if Player 1 misses (probability $1 - p(t)$), Player 2 walks right up to point-blank range (or takes as long as needed to perfect the product) and wins with probability `1`!
    - **Family**: `duel or preemption`.
    - **Best Move / Real People**: In `"TRIP TO THE GYM NO. 8"` (l. 9509 & Workout l. 13153), the preemption threshold occurs at the exact instant $t^*$ where
      $$p(t^*) + q(t^*) = 1$$
      (In the symmetric case $p(t) = q(t)$, someone fires/launches as soon as accuracy reaches **`p(t^*) = 1/2`**!). Real people: Apple rushed the Newton to market in August 1993 when handwriting recognition was half-baked (`"Doonesbury"` mocked its garbled text for a week); Newton failed, whereas Palm waited, perfected Graffiti on the PalmPilot, and captured the market.
    - **THE RULE THAT CHANGES THE BEST MOVE**:
      1. Whether there is room in the market for *only one* winner vs. room for a better second mover (`"Apple thought it was in a preemption game, where the first to market takes all. In fact, there was plenty of room for a later entrant with a product that actually worked"`, l. 9522).
      2. Monopoly vs. competitive R&D: a monopolist waits until accuracy is much higher than $1/2$, whereas two rivals preempt each other at $p(t) + q(t) = 1$.
    - **Catastrophic Loss?**: Yes — death in a pistol duel, or product failure (`$100M+` loss on Apple Newton).

72. **The War of Attrition (Rupert Murdoch's Sky TV vs. British Satellite Broadcasting [BSB])**
    - **Heading & First Line**: `"THE WAR OF ATTRITION"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L9531-L9589)) — `"The opposite of the preemption game is a war of attrition."`
    - **Players, Moves, Timing**: 2 players (Rupert Murdoch's Sky Television vs. British Satellite Broadcasting [BSB] in 1990). Moves: Stay in the market bleeding cash vs. Quit/capitulate at time $t$. Continuous time.
    - **Payoffs**: Both bleed massive operating losses every week (`£10 million/week` combined; over **`£1.2 billion`** total sunk losses by November 1990) until one quits and the survivor reaps the British satellite monopoly.
    - **Family**: `war of attrition` / `auction` (all-pay auction where both the winner and the loser pay their bids!).
    - **Best Move / Real People**: Project a credible commitment to stay forever or merge early. Real people: BSB burned through more capital building custom satellites and fancy headquarters; after losing over £1.2 billion between them, BSB capitulated in November 1990 in a `"merger"` controlled by Murdoch's BSkyB, which became enormously profitable.
    - **THE RULE THAT CHANGES THE BEST MOVE**: In a war of attrition, **both the winner and the loser must pay for the time elapsed** (`"unlike a standard auction, the loser also has to pay his bid"`, l. 9542), so sunk costs are ignored at every continuation point and escalation can exceed the value of the prize itself!
    - **Catastrophic Loss?**: Yes — losing over `£1.2 billion` in accumulated operating losses before capitulating.

73. **Case Study: Spectrum Auctions (AT&T vs. Verizon Simultaneous Ascending Auction for NY and LA Licenses)**
    - **Heading & First Line**: `"CASE STUDY: SPECTRUM AUCTIONS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L9590-L9794)) — `"The mother of all auctions has been the sale of spectrum for cell phone service."`
    - **Players, Moves, Timing**: 2 major telecom bidders (**AT&T** and **Verizon**, where Verizon acts as the authors' client in the case discussion) bidding across simultaneous ascending rounds for 2 licenses: **New York (NY)** and **Los Angeles (LA)**.
    - **Payoffs**: Valuation table at l. 9651 is an image (`table not in text`), exact numbers in prose (l. 9653–9785):
      - **AT&T's valuations**: `NY alone = $10`, `LA alone = $10`, `Both (NY + LA) = $25` ( includes a `$5` coast-to-coast synergy bonus).
      - **Verizon's valuations**: `NY alone = $9`, `LA alone = $9`, `Both (NY + LA) = $18` (no synergy bonus; values are additive).
      - FCC rules: Activity requirement (a bidder active on 1 license cannot expand to 2 licenses later; dropping from 2 licenses to 1 license is irreversible), and minimum bid increment = `$1`.
    - **Family**: `auction`.
    - **Best Move / Real People**:
      - If Verizon bids naively up to `$9` on both licenses, AT&T wins both at `($9, $9) = $18` (making `$25 - $18 = $7` profit) while Verizon gets nothing (`$0`).
      - If Verizon tries to push AT&T up to `$12` on both so AT&T drops one, Verizon risks getting stuck winning one at `$12 > $9` (a `$3` loss!).
      - **Verizon's optimal strategy**: Once prices reach **`$5` on NY and `$5` on LA**, Verizon drops down to bidding on **only ONE license** (say NY, pushing NY from `$5` to `$6`). Now AT&T faces a choice:
        1. Let Verizon have NY for `$6` and keep LA for **`$5`**, giving AT&T a profit of **`$10 - $5 = $5`** (and Verizon a profit of **`$9 - $6 = $3`**); or
        2. Fight Verizon for both NY and LA, which forces prices up to **`$9` on NY and `$9` on LA** (`$18` total), giving AT&T a profit of `$25 - $18 = $7`—Wait: if Verizon pushes *above* `$5` (specifically, once prices reach **`$7` on both**, or if Verizon commits at `$5` to push the single license up to `$9` plus retaliatory bidding), let's quote the exact numbers in text (l. 9705–9775): At `($5, $5)`, if AT&T fights for both, Verizon will bid NY up to **`$10`** (since Verizon doesn't care which single license it wins, or pushes NY to `$9` and LA to `$9`), whereas if AT&T concedes one license when prices are at **`$5`**, AT&T pays `$5` for LA and nets `$10 - $5 = $5` (or if prices reached **`$7`**, `$25 - ($9 + $9) = $7` vs. `$10 - $3 = $7` at `$3`!). Specifically, the text shows (l. 9708–9755) that if Verizon shrinks demand to 1 license when prices are at **`$5`**, AT&T gets `$10 - $5 = $5` by letting Verizon take NY at `$6`, whereas if AT&T fights to win both, Verizon pushes NY up to `$9` (or `$10`) and LA is at `$5` (`$14–$15` cost), and if Verizon keeps switching back and forth between whichever license is cheaper from `$5` up to `$9`, both licenses reach **`$9`**, leaving AT&T `$25 - $18 = $7` (so Verizon switches back and forth until both reach **`$7`**, where AT&T nets `$10 - $7 = $3` on one license vs. `$25 - $18 = $7`... wait: at **`$3`**, `$10 - $3 = $7 = $25 - $18`!). Let's quote the text's exact conclusion: by reducing demand to one license early (or pushing both up to `$7` and then dropping to one), Verizon induces AT&T to accommodate and share the two licenses at a low price rather than fighting to `$9` on both!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Simultaneous multi-license ascending format with the **activity requirement** (`"you can never increase the number of licenses you are bidding on"`, l. 9636), which enables demand reduction / market division.
    - **Catastrophic Loss?**: Overpaying above `$9` if caught holding the bag on a bluff bid.

---

### Chapter 11 — Bargaining

74. **Alternating-Offer Hotel Wage Bargaining, The Handicap System, Case Study: 'Tis Better to Give Than to Receive?, and Rubinstein Bargaining Appendix**
    - **Heading & First Line**: `"Bargaining"`, `"THE HANDICAP SYSTEM IN NEGOTIATIONS"`, `"CASE STUDY: ’TIS BETTER TO GIVE THAN TO RECEIVE?"`, `"APPENDIX: RUBINSTEIN BARGAINING"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L9795-L9911), [l. 10246](file:///home/masih/Work/tries/aos/book-full.txt#L10246-L10493), & fns [l. 14205](file:///home/masih/Work/tries/aos/book-full.txt#L14205-L14222)) — `"A NEWLY ELECTED trade union leader went to his first tough negotiation with the employer"`
    - **Players, Moves, Timing**: 2 players (**Hotel Management** and **Labor Union**). Sequential alternating offers (or one-sided offers in the Case Study, or infinite-horizon Rubinstein bargaining in the Appendix).
    - **Payoffs**: Tables at l. 9846, 9885, 10261, 10294 are images (`table not in text`), with all numbers in prose:
      - *Finite 3-Day Alternating-Offer Seasonal Hotel Game (l. 9817–9874)*: A resort hotel operates for a 3-day summer season, earning **`$3,000` total (`$1,000` per day)**. Each day without agreement loses `$1,000` permanently.
        - **Day 3** (Union makes final offer; pie left = `$1,000`): Union gets **`$1,000`**, Management gets **`$0`**.
        - **Day 2** (Management makes offer; pie left = `$2,000`): Management offers Union `$1,000` (what Union would get on Day 3) and keeps **`$1,000`** -> **`($1,000, $1,000)`**.
        - **Day 1** (Union makes first offer; pie = `$3,000`): Union offers Management `$1,000` (what Management would get on Day 2) and keeps **`$2,000`** -> **`($2,000 to Union, $1,000 to Management)`** settled immediately on Day 1!
      - *With Outside Option / Unemployment Benefit (`"THE HANDICAP SYSTEM"`, l. 9875)*: Suppose Union workers earn **`$300/day`** in temporary jobs during a strike (`$900` total over 3 days). Then each day's net surplus above the `$300` outside option is `$700` (`$2,100` total surplus), which splits 2/3 to Union (`$1,400`) and 1/3 to Management (`$700`), so on Day 1 **Union gets `$900 + $1,400 = $2,300`** and **Management gets `$700`**!
      - *Case Study: 'Tis Better to Give Than to Receive? (4-Quarter declining pie where Management makes ALL offers vs. Alternating offers, l. 10246–10343)*:
        - Total pie starts at **`$100`** in Q1, shrinks to **`$80`** in Q2, **`$50`** in Q3, **`$10`** in Q4, and **`$0`** after Q4.
        - If **Management makes all offers** in Q1, Q2, Q3, Q4: in Q4 Union gets `$0`, in Q3 `$0`, in Q2 `$0`, in Q1 `$0` — Management gets **`$100`**!
        - If **offers alternate** (Management in Q1 & Q3; Union in Q2 & Q4):
          - In Q4 (pie `$10`, Union offers): Union gets `$10`, Mgmt gets `$0`.
          - In Q3 (pie `$50`, Mgmt offers): Mgmt gives Union `$10` and keeps `$40` -> `(Mgmt $40, Union $10)`.
          - In Q2 (pie `$80`, Union offers): Union gives Mgmt `$40` and keeps `$40` -> `(Mgmt $40, Union $40)`.
          - In Q1 (pie `$100`, Mgmt offers): Mgmt gives Union `$40` and keeps **`$60`** -> **`(Mgmt $60, Union $40)`**!
        - What if **Union makes the first offer in Q1**, and **Management makes ALL subsequent offers (Q2, Q3, Q4)**? Because Management makes all offers from Q2 onward, if Q1 fails Management will take the entire `$80` in Q2 (`Union $0, Mgmt $80`)! Therefore, in Q1 Union must offer Management **`$80`** and Union keeps only **`$20`** (`$20 < $40`), proving that **having the right to make alternating follow-up offers (`$40`) is worth more than making only the first offer (`$20`)!**
      - *Appendix: Infinite-Horizon Rubinstein Bargaining (l. 10344 & fn l. 14219)*: Pie = `$1`, discount factor $\delta$ per round. First mover gets $L = \frac{1}{1 + \delta}$ and second mover gets $\frac{\delta}{1 + \delta}$. With different weekly discount rates $r_{\text{Union}} = 1\%$ ($\delta_U = 0.99$) and $r_{\text{Mgmt}} = 2\%$ ($\delta_M = 0.98$, fn l. 14219), the twice-as-impatient Management gets **half as much** as the Union (`1/3` vs. `2/3`).
    - **Family**: `bargaining`.
    - **THE RULE THAT CHANGES THE BEST MOVE**:
      1. Who makes the offers in subsequent rounds (`"Making the first offer is much less important than having the power to make offers in later rounds"`, l. 10315: Union gets `$40` when alternating vs. `$20` when making only the Q1 offer).
      2. Relative impatience / cost of delay ($r_U = 1\%$ vs. $r_M = 2\%$, fn l. 14219) and outside strike income (`$300/day`).
    - **Catastrophic Loss?**: Destruction of the pie if strikes drag on to the end of the season.

75. **Measuring the Pie: Lawyer's Shared Flight Billing (New York -> Houston -> San Francisco)**
    - **Heading & First Line**: `"MEASURING THE PIE"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L9912-L9993) & fn [l. 14209](file:///home/masih/Work/tries/aos/book-full.txt#L14209-L14210)) — `"Our bargaining rule says that each side should get its outside opportunity"`
    - **Players, Moves, Timing**: 2 clients (**Houston Client** and **San Francisco Client**) splitting airfare for a New York lawyer who visits both on one combined trip (`NY -> Houston -> SF -> NY`).
    - **Payoffs**: Exact airfares in prose (l. 9920–9985):
      - Standalone `NY–Houston–NY` round-trip = **`$1,332`**
      - Standalone `NY–SF–NY` round-trip = **`$2,486`**
      - Combined standalone cost = `$1,332 + $2,486 = $3,818`
      - Combined `NY–Houston–SF–NY` ticket = **`$2,665`**
      - Net savings (the bargaining pie) = `$3,818 - $2,665 = $1,153`.
    - **Family**: `bargaining` (Shapley value / cooperative surplus division).
    - **Best Move / Real People**: Split the **`$1,153` savings** 50:50 (`$576.50` savings each):
      - **Houston Client pays**: `$1,332 - $576.50 = $755.50`
      - **San Francisco Client pays**: `$2,486 - $576.50 = $1,909.50`
      (Total = `$2,665`; equivalently, each pays its marginal cost of adding its leg [`$179` for Houston, `$1,333` for SF] plus half the `$1,153` joint savings!).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Measuring the pie as the **net cost savings (`$1,153`) relative to standalone outside options**, rather than splitting the total `$2,665` bill 50:50 (`$1,332.50` each, which would make the Houston client worse off than flying the lawyer alone for `$1,332`!).
    - **Catastrophic Loss?**: No.

76. **This Will Hurt You More Than It Hurts Me, Brinkmanship and Strikes, Simultaneous Multi-Issue Bargaining, and The Virtues of a Virtual Strike**
    - **Heading & First Line**: `"THIS WILL HURT YOU MORE THAN IT HURTS ME"`, `"BRINKMANSHIP AND STRIKES"`, `"SIMULTANEOUS BARGAINING OVER MANY ISSUES"`, `"THE VIRTUES OF A VIRTUAL STRIKE"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L9994-L10245)) — `"When a strategic bargainer observes that a better outside opportunity translates into a bigger share of the pie"`
    - **Players, Moves, Timing**:
      - *Destructive Outside Options / Strikes (l. 9994–10131)*: Union vs. Management (e.g., 1997 UPS strike right before peak shipping, fn l. 14211; 2005 NYC transit strike; 1994–95 MLB baseball strike; 2004–05 NHL hockey lockout that canceled the entire season; 2007–08 Broadway stagehands strike & Hollywood writers strike).
      - *Multi-Issue Camp David Bargaining (l. 10132)*: Israel (Menachem Begin) vs. Egypt (Anwar Sadat) in 1978 Camp David Accords: Israel cared most about security (demilitarization of Sinai), while Egypt cared most about sovereignty (returning every inch of Sinai land); trading land for demilitarization created a win-win deal.
      - *Virtual Strike (l. 10165)*: Workers keep working and serving customers, while **both union workers forgo their wages AND the company forgoes its profits/revenues** (donating both to charity or an escrow fund until they settle!). Used successfully in 4 real-world cases: 1960 Miami bus drivers (`"goldfish bowl"` strike), 1989 Derry, Ireland electricity workers, 1999 Rome transport workers, and 2000 French tollbooth workers.
    - **Family**: `bargaining` / `brinkmanship`.
    - **Best Move / Real People**: In a standard strike with asymmetric information about firmness, brinkmanship generates real strikes to screen out bluffs. A **virtual strike** preserves the exact same `lose-lose` bargaining pressure on management and labor while sparing innocent third parties (customers, suppliers, fans) and keeping the long-term customer base intact!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Switching from a conventional work-stoppage strike to a **virtual strike** where output continues but wages and profits go to charity (`"During a virtual strike, the workers continue to work and the firm continues to operate, but neither side gets paid"`, l. 10185).
    - **Catastrophic Loss?**: Yes — in conventional strikes, cancellation of the entire 2004–05 NHL season (`"canceled the entire season"`, l. 10116) or firm bankruptcy.

---

### Chapter 12 — Voting

77. **Naive vs. Strategic Voting, Condorcet's Paradox (3-Way Cycle), Amendment Agendas, and the 2000 Bush-Gore-Nader Election**
    - **Heading & First Line**: `"Voting"`, `"NAÏVE VOTING"`, `"CONDORCET RULES"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L10494-L10712) & fn [l. 14226](file:///home/masih/Work/tries/aos/book-full.txt#L14226-L14234)) — `"People on whom I do not bother to dote / Are people who do not bother to vote"`
    - **Players, Moves, Timing**:
      - *Condorcet Cycling Legislature (l. 10545)*: 3 voters/factions (**Left**, **Center**, **Right**, 1/3 each) voting over 3 school funding bills: **High ($H$)**, **Medium ($M$)**, **Low ($L$)**.
        - **Left** ranks: `H > M > L`
        - **Center** ranks: `M > L > H`
        - **Right** ranks: `L > H > M` (prefers no public funding $L$, or else $H$ so taxes are so high that voters revolt, over a moderate compromise $M$!).
        - Pairwise majority votes cycle endlessly: `H beats M (2:1)`, `M beats L (2:1)`, and `L beats H (2:1)`!
      - *Strategic Agenda Manipulation (l. 10600)*: Round 1 pairs `H vs. M`, Round 2 pairs the winner against `L`.
        - Under *naive voting*, `H` beats `M` in Round 1, and `L` beats `H` in Round 2 -> **`L` wins**!
        - Under *strategic backward induction*, voters see that `H` loses to `L` in Round 2 whereas `M` beats `L` in Round 2; so Round 1 is really a choice between **`L` (if `H` wins Round 1)** and **`M` (if `M` wins Round 1)**. Because **Left** prefers `M` over `L`, Left votes strategically for `M` in Round 1, so **`M` wins**!
      - *1956 Powell Amendment to Federal School-Construction Bill (l. 10635)*: Southern Democrats opposed desegregation (`Powell Amendment`), while Republicans opposed federal school spending altogether. Republicans voted *for* the Powell Amendment to make the amended bill unpalatable to Southern Democrats, killing the final bill!
      - *2000 U.S. Presidential Election (l. 10650 & fn l. 14226)*: Bush vs. Gore vs. Nader in Florida (Bush won by 537 votes while Nader received 97,488 votes; authors proposed to Nader before the election that he nominate the same Florida Electoral College electors as Gore so Nader voters could register support and 5% matching-fund threshold without electing Bush; Nader refused, fn l. 14226).
    - **Family**: `voting`.
    - **THE RULE THAT CHANGES THE BEST MOVE**:
      1. Sequential pairwise agenda order (`"Whoever controls the agenda controls the outcome"` under naive voting, whereas under strategic voting `"the alternative that enters the voting process last has a disadvantage"`, l. 10625).
      2. Allowing Nader to share Gore's Electoral College slates (fn l. 14226) or using a Condorcet tournament when a Condorcet winner exists.
    - **Catastrophic Loss?**: Electing one's least-preferred candidate (`Bush` for Nader voters; killing the school bill).

78. **Order in the Court: Roman Senate Trial (Pliny the Younger), Condorcet vs. Anglo-American vs. Roman Legal Procedures, and U.S. Supreme Court *Swann* Multi-Issue Paradox**
    - **Heading & First Line**: `"ORDER IN THE COURT"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L10713-L10798)) — `"The way the U.S. judicial system works, a defendant is first found to be guilty or innocent."`
    - **Players, Moves, Timing**:
      - *Pliny the Younger's Roman Senate Freedmen Trial (A.D. 105, l. 10742)*: 3 senate factions judging freedmen after a consul's mysterious death:
        - **Acquit ($A$)**: `45%` of senators (prefer `Acquit > Banish > Execute`)
        - **Banish ($B$)**: `35%` of senators (prefer `Banish > Execute > Acquit`)
        - **Execute ($E$)**: `20%` of senators (prefer `Execute > Banish > Acquit`)
        - Note that **`Banish ($B$)` is the Condorcet winner** (beats $A$ by `55% to 45%`, beats $E$ by `80% to 20%`).
        - Pliny insisted on a 3-way plurality vote (`45% A, 35% B, 20% E`); seeing that $E$ would lose, the `20%` Execution faction strategically joined the `35%` Banish faction, producing **`Banish` (`55% to 45%`)**.
        - Had they used the **Anglo-American two-stage procedure** (Vote 1: `Guilty vs. Innocent`; Vote 2: `Banish vs. Execute`), then in Vote 2 `Banish` beats `Execute` (`80% to 20%`), so in Vote 1 `Guilty (= Banish)` beats `Innocent (= Acquit)` by `55% to 45%` -> **`Banish`**. (Wait: what if the `45%` Acquit faction preferred `Execute` over `Banish`? Then in Vote 2 `Execute` would win if `Acquit` senators could vote!).
      - *U.S. Supreme Court Multi-Issue vs. Outcome Voting (l. 10772)*: 3 Justices (**1, 2, 3**) deciding an appeal that requires winning on *both* Issue $A$ and Issue $B$ for the plaintiff to prevail:
        - **Justice 1**: Yes on $A$, Yes on $B$ -> Plaintiff wins (`Yes`)
        - **Justice 2**: Yes on $A$, No on $B$ -> Plaintiff loses (`No`)
        - **Justice 3**: No on $A$, Yes on $B$ -> Plaintiff loses (`No`)
        - Under **issue-by-issue voting**, Issue $A$ passes `2–1` (Justices 1 & 2) and Issue $B$ passes `2–1` (Justices 1 & 3), so **Plaintiff wins** — even though a **`2–1` majority of Justices (Justices 2 & 3)** believe the Plaintiff should **lose**!
    - **Family**: `voting`.
    - **THE RULE THAT CHANGES THE BEST MOVE**: Voting **issue-by-issue** (`Plaintiff wins 2–1 on A and 2–1 on B`) vs. voting **directly on the final outcome** (`Plaintiff loses 1–2`): `"If the court votes issue by issue, the plaintiff wins; if the court votes on the outcome, the plaintiff loses!"` (l. 10788).
    - **Catastrophic Loss?**: Yes — execution vs. banishment vs. acquittal of the accused freedmen.

79. **The Median Voter & Why the Constitution Works (1D Median Voter vs. 2D Cake-Division Cycling & 64% Supermajority Rule)**
    - **Heading & First Line**: `"THE MEDIAN VOTER"` & `"WHY THE CONSTITUTION WORKS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L10799-L11020) & fn [l. 13800](file:///home/masih/Work/tries/aos/book-full.txt#L13800-L13809)) — `"In thinking about voting, we’ve assumed so far that the candidates simply have fixed positions"`
    - **Players, Moves, Timing**:
      - *1D Median Voter (l. 10799)*: 2 candidates choosing positions on a 1D ideological spectrum (with primary elections pulling them toward party medians and general election pulling them toward the overall median voter).
      - *2D Three-Voter Divide-the-Pie / Multidimensional Platform Game (`"WHY THE CONSTITUTION WORKS"`, l. 10882)*: 3 voters ($A, B, C$) dividing a triangle of pork-barrel/tax benefits (figures at l. 10945, 10967 are images, `table not in text`). Under simple majority rule (`50% + 1`), **every possible division of the pie can be defeated** by a coalition of 2 voters (e.g., if incumbent gives `(1/3, 1/3, 1/3)`, challenger offers `(1/2, 1/2, 0)` to $A$ and $B$).
    - **Family**: `voting`.
    - **Best Move / Real People**: In 1D, converge to the median voter. In 2D or higher-dimensional redistributive politics under simple majority rule, no stable equilibrium exists; stability is restored by requiring a **supermajority of at least $1 - 1/e \approx 64\%$ (`~2/3` supermajority, Caplin-Nalebuff theorem, l. 11005 & fn l. 13800)** at the center of gravity `(1/3, 1/3, 1/3)`!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Moving from 1 dimension (where 50% majority has a unique stable median-voter equilibrium) to multi-dimensional pie-splitting, and raising the required vote threshold from **simple majority (`50%`) to a `2/3` (`64%`) supermajority** (`"if a proposal needs a two-thirds vote, then there is some position that is undefeatable against all challengers"`, l. 11005, explaining why the U.S. Constitution requires a 2/3 supermajority for amendments, treaties, and veto overrides!).
    - **Catastrophic Loss?**: Endless political cycling and instability under 50% majority rule in multidimensional redistribution.

80. **All-Time Greats (Baseball Hall of Fame Voting) & Love a Loath'd Enemy (Strategic Charity Matching)**
    - **Heading & First Line**: `"ALL-TIME GREATS"` & `"LOVE A LOATH’D ENEMY"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L11021-L11142) & fns [l. 14235](file:///home/masih/Work/tries/aos/book-full.txt#L14235-L14244)) — `"Every year, members of the Baseball Writers’ Association of America vote to elect players to the Baseball Hall of Fame."`
    - **Players, Moves, Timing**:
      - *Baseball Hall of Fame (l. 11021)*: 545 sportswriters voting on 32 candidates (in 2007); each voter can list up to 10 names, and `75%` (`409` votes) is required for election. Because no player has *ever* been elected unanimously (Tom Seaver got `98.83%`, Nolan Ryan `98.79%`, Cal Ripken Jr. `98.53%`), some voters who think a star like Ripken is a lock (`>75%`) leave him off their ballot Either to prevent him from getting `100%` (`"If Babe Ruth didn't get 100%, nobody should"`) or to save their 10th vote for a borderline candidate; if too many voters think this way, a sure-fire candidate could fail to reach `75%`!
      - *Love a Loath'd Enemy (l. 11107)*: An environmentalist and an NRA supporter set up a mutual matching pact: for every `$100` the environmentalist donates to the Sierra Club, the NRA supporter donates `$100` to the Sierra Club, and vice versa — or each threatens to donate to the *other's hated cause* unless the other contributes to a shared public good (like the local school or United Way)!
    - **Family**: `voting` / `prisoners' dilemma` (public goods provision).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Tying your contribution to a cause your rival hates (or loves) flips free-riding incentives in public goods provision.
    - **Catastrophic Loss?**: Losing Hall of Fame eligibility after 15 years on the ballot (fn l. 14235).

81. **Case Study: The Tie of Power (Vice President's Tie-Breaking Vote in the U.S. Senate)**
    - **Heading & First Line**: `"CASE STUDY: THE TIE OF POWER"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L11143-L11209) & fns [l. 14250](file:///home/masih/Work/tries/aos/book-full.txt#L14250-L14258)) — `"Recent presidential elections have emphasized the importance of the choice of a running mate"`
    - **Players, Moves, Timing**: 100 U.S. Senators + 1 Vice President (who votes only when the Senate is tied `50–50`). Simultaneous / sequential.
    - **Payoffs**: Passage vs. defeat of legislation.
    - **Family**: `voting` (pivotal voter / Shapley-Shubik power index).
    - **Best Move / Real People**: How much voting power does the Vice President have compared to a regular Senator?
      - Under random independent `50:50` coin-flip voting by 100 Senators (fn l. 14252), the probability of an exact `50–50` tie is $\binom{100}{50} (1/2)^{100} \approx 1/12$ (`~8%`).
      - In reality, Senators do *not* vote at random; because the Vice President only breaks `50–50` ties, **51 Senators are needed to pass a bill when the VP opposes it, whereas only 50 Senators are needed when the VP favors it**! Thus the Vice President has **the exact same voting power as a single U.S. Senator** (`"having the vice president on your side is worth exactly one senate seat"`, l. 11195) — except the VP cannot introduce bills or filibuster! (Historically, John Adams cast 29 tie-breaking votes, John C. Calhoun 28, Richard Nixon 8, Dick Cheney 8).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Requiring 60 votes to end a filibuster (cloture) completely eliminates the Vice President's tie-breaking power on filibustered bills (`"Because it takes 60 votes to stop a filibuster, a 50:50 tie is no longer the relevant threshold"`, l. 11204).
    - **Catastrophic Loss?**: No.

---

### Chapter 13 — Incentives

82. **Incentives for Effort: Proofreading This Book ($20/hr vs. $2/Error vs. Planted-Errors Tournament)**
    - **Heading & First Line**: `"INCENTIVES FOR EFFORT"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L11238-L11324) & fns [l. 14259](file:///home/masih/Work/tries/aos/book-full.txt#L14259-L14266)) — `"Of all the steps involved in writing a book, surely the most tedious for an author is proofreading"`
    - **Players, Moves, Timing**: Authors (employers) vs. Student Proofreader(s). Moves: Authors design payment contract; student chooses High Effort (careful reading) vs. Low Effort (skimming). Sequential.
    - **Payoffs**: Suppose the manuscript has `150` real typos (unknown in advance to the authors) and takes `20 hours` to read. Student's opportunity wage is `$10/hr` (`$200` for skimming) plus `$100` extra effort cost (`$300` total) for careful reading.
      - Paying a flat `$300` salary induces skimming (`$200` effort cost -> student nets `$100` rent without finding all errors).
      - Paying `$2` per error found (`$300` for 150 errors) fails if there turn out to be only `50` errors (`$100` pay < `$300` cost, so student quits).
      - **Planted-Errors & Two-Proofreader Mechanism (l. 11295)**: Authors secretly plant `100` known errors, or hire **two independent proofreaders** ($A$ and $B$). If $A$ finds $n_A$ errors, $B$ finds $n_B$ errors, and both find $n_{AB}$ overlapping errors, the true total number of errors is estimated by capture-recapture ($N \approx \frac{n_A n_B}{n_{AB}}$), and each proofreader is paid based on the fraction of the *other* proofreader's discovered errors that they also caught!
    - **Family**: `other` (principal-agent moral hazard / mechanism design).
    - **Best Move / Real People**: Use two independent proofreaders (or planted errors) to benchmark the unknown error rate (`"By comparing the list of errors found by one student against the list found by the other, you can estimate how thorough each one was"`, l. 11312).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Hiring a second independent agent and conditioning each agent's bonus on catching the errors found by the other (`"Each student’s detection rate can be measured by the fraction of the OTHER student’s found errors that he or she also caught"`, l. 11315).
    - **Catastrophic Loss?**: No.

83. **How to Write an Incentive Contract & How to Reward Work Effort (Chess Software Project: Routine vs. Superhuman Effort)**
    - **Heading & First Line**: `"HOW TO WRITE AN INCENTIVE CONTRACT"` & `"HOW TO REWARD WORK EFFORT"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L11325-L11385), [l. 11749](file:///home/masih/Work/tries/aos/book-full.txt#L11749-L11865), & fn [l. 14271](file:///home/masih/Work/tries/aos/book-full.txt#L14271-L14272)) — `"The main problem of moral hazard is the unobservability of a worker’s effort."`
    - **Players, Moves, Timing**: 2 players (Software Company Owner vs. Lead Programmer developing a new chess program). Moves: Owner sets base salary $S$ and success bonus $B$; Programmer chooses **Routine Effort** or **Superhuman Effort**. Sequential.
    - **Payoffs**: Table at l. 11765 is an image (`table not in text`), exact numbers in prose (l. 11753–11860):
      - Project value to Owner: **`$200,000`** if successful, **`$0`** if it fails.
      - Success probability: **`80%`** under Superhuman Effort; **`60%`** under Routine Effort.
      - Programmer's outside wage / opportunity cost: **`$50,000`** for Routine Effort; **`$70,000`** for Superhuman Effort (`$20,000` extra disutility of superhuman effort).
      - Expected project revenue: $0.80 \times \$200,000 = \$160,000$ (Superhuman) vs. $0.60 \times \$200,000 = \$120,000$ (Routine) — a `$40,000` expected gain for `$20,000` extra effort cost!
    - **Family**: `other` (principal-agent moral hazard).
    - **Best Move / Real People**:
      - **Incentive-Compatibility Constraint**: Raising success chance by `20%` (`0.80 - 0.60`) must pay the programmer at least `$20,000` extra expected bonus:
        $$0.20 \times B \ge \$20,000 \implies B = \$100,000.$$
      - **Participation Constraint**: With $B = \$100,000$, the programmer expects $0.80 \times \$100,000 = \$80,000$ in bonus; if the programmer can pay upfront (franchise), $S = -\$10,000$ (`$70,000` net expected pay) leaves Owner with `$90,000` profit; if $S \ge \$0$ (limited liability), set **$S = \$0$ and $B = \$100,000$** (programmer expects `$80,000` [net `$10,000` rent above `$70,000`], and Owner nets $0.80 \times (\$200,000 - \$100,000) = \$80,000$, which beats paying `$50,000` flat for Routine Effort where Owner nets $\$120,000 - \$50,000 = \$70,000$!).
    - **THE RULE THAT CHANGES THE BEST MOVE**: If the extra effort only raised success probability from `60%` to **`65%`** (`+5%`), then $B$ would have to be $\$20,000 / 0.05 = \$400,000$, and with $S \ge 0$ or risk aversion, inducing Superhuman Effort becomes unprofitable for the Owner!
    - **Catastrophic Loss?**: Programmer gets `$0` (`20%` of the time) if the project fails under $S = 0, B = \$100,000$.

84. **Trip to the Gym No. 9 (Real Estate Agent Commission vs. Selling Own House) & Repeated Auto Mechanic Honesty Game**
    - **Heading & First Line**: `"TRIP TO THE GYM NO. 9"` & `"THE MANY DIMENSIONS OF INCENTIVE PAYMENT SCHEMES"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L11386-L11748), Workout [l. 13174](file:///home/masih/Work/tries/aos/book-full.txt#L13174-L13195), & fn [l. 14267](file:///home/masih/Work/tries/aos/book-full.txt#L14267-L14270)) — `"Suppose you are selling your house. You think it should fetch around $250,000."`
    - **Players, Moves, Timing**:
      - *Trip to the Gym No. 9 (l. 11386 & Workout l. 13174)*: Homeowner vs. Real Estate Agent. House worth `~$250,000` vs. `$260,000` with extra effort (`$2,000` of agent's time/marketing cost). Under a flat `6%` commission (`$15,000` at `$250k`, `$15,600` at `$260k`), holding out for `$260,000` gains the agent only **`$600`** (`6% of $10,000`), which is less than the `$2,000` extra cost — so the agent pushes the owner to accept `$250,000` quickly (whereas on agents' *own* houses, Levitt & Syverson showed agents keep them on the market 10 days longer and get 3.7% higher prices!).
      - *Auto Mechanic Repeated Honesty Game (l. 11520 & fn l. 14267)*: Mechanic vs. Customer. Mechanic can invent a fake repair for `$1,000` extra one-time profit (`$100/yr` at 10% interest rate), with a `25%` chance the customer catches him and never returns. If the customer's honest repeat business brings in **`>$400/year`** in profit ($0.25 \times \$400 = \$100$), the mechanic stays honest!
      - *CEO Stock Options, Safelite Auto Glass Piece Rates ($20%$ productivity jump), Teacher Test-Score Cheating, and Continental Airlines On-Time Bonus* (l. 11460–11748).
    - **Family**: `other` (principal-agent moral hazard & repeated reputation).
    - **THE RULE THAT CHANGES THE BEST MOVE**: In `"TRIP TO THE GYM NO. 9"` (Workout l. 13174), replacing the flat `6%` commission with a **marginal incentive contract** — e.g., **`$5,000` base fee plus `50%` of the sale price above `$230,000`** (`$15,000` at `$250k`, and `$20,000` at `$260k`, giving the agent `$5,000 > $2,000` for getting the extra `$10,000`!).
    - **Catastrophic Loss?**: No.

85. **Case Study: Treat Them Like Royalty & Trip to the Gym No. 10 (Book Publisher vs. Author Pricing Conflict)**
    - **Heading & First Line**: `"CASE STUDY: TREAT THEM LIKE ROYALTY"` & `"TRIP TO THE GYM NO. 10"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L11866-L11916), Workout [l. 13196](file:///home/masih/Work/tries/aos/book-full.txt#L13196-L13212)) — `"The typical way that authors get paid for writing a book is via a royalty"`
    - **Players, Moves, Timing**: 2 players (**Book Publisher** and **Author**). Moves: Author signs contract for `15%` of gross revenue; Publisher sets retail book price $P$. Sequential.
    - **Payoffs**: Exact numbers in Workout `"TRIP TO THE GYM NO. 10"` (l. 13196):
      - Demand: $Q = 100,000 - 2,000 P$ (or $P = 50 - Q/2000$).
      - Production cost per copy = **`$10`** (paid entirely by the Publisher), plus **`15%` royalty on revenue** ($0.15 P$ per book, paid to the Author).
      - **Author's objective**: Maximize gross revenue $P \times Q = P(100,000 - 2,000P)$, which peaks at **`P = $25`** (`Q = 50,000` copies; gross revenue = `$1,250,000`; Author gets `15% = $187,500`; Publisher nets $85\% \times \$1.25\text{M} - \$500\text{k} = \$562,500$).
      - **Publisher's objective**: Maximize $(0.85 P - 10)(100,000 - 2,000 P)$, which is equivalent to a marginal cost of $\$10 / 0.85 = \$11.76$, peaking at **`P = $30.88`** (`Q = 38,235` copies; Publisher nets **`$621,324`**, while Author's royalty drops to **`$177,105`**, and total joint profit drops from `$750,000` [at the joint-optimum price **`P = $30`**] to `$798,429`—wait: at **$P = $30$**, $Q = 40,000$, total profit is $(\$30 - \$10) \times 40,000 = \$800,000$, whereas at $P = \$30.88$ total profit is $\$798,429 < \$800,000$!).
    - **Family**: `other` (principal-agent / double marginalization).
    - **Best Move / Real People**: Under a revenue royalty, the Author wants a lower price (`$25`) than the Publisher (`$30.88`), and the Publisher sets a price even higher (`$30.88`) than the joint-profit-maximizing price (`$30`)!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Basing the Author's royalty on **net profit ($P - \$10$)** rather than gross revenue ($P$) aligns both sides on **`P = $30`** (`"if the author were paid a percentage of the profits rather than the revenues, both would agree on the price of $30"`, l. 13209 — though in practice Hollywood/publishing "net profit" accounting is notorious for creative cost-padding, l. 11902!).
    - **Catastrophic Loss?**: No.

---

### Chapter 14 — Case Studies (All 14 Case Studies)

86. **The Other Person's Envelope Is Always Greener (The Two-Envelope Exchange Paradox)**
    - **Heading & First Line**: `"THE OTHER PERSON’S ENVELOPE IS ALWAYS GREENER"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L11924-L11973)) — `"The inevitable truth about gambling is that one person’s gain must be another’s loss."`
    - **Players, Moves, Timing**: 2 players (**Ali** and **Baba**) + Benefactor. Benefactor puts `$5, $10, $20, $40, $80, or $160` in two envelopes such that one envelope always contains **twice** as much as the other (`{$5,$10}, {$10,$20}, {$20,$40}, {$40,$80}, {$80,$160}`, each with equal probability `1/5`). Each player privately opens his/her envelope and chooses whether to **Switch** or **Keep**; trade occurs only if *both* agree to switch. Simultaneous after viewing own envelope.
    - **Payoffs**: Zero-sum swap of envelopes.
    - **Family**: `signalling` / `auction` (winner's curse / no-trade theorem).
    - **Best Move / Real People**: Naive calculation says if you see `$20`, the other has `$10` or `$40` (average `$25 > $20`, so switch!). By backward induction from the maximum (`$160`):
      - A player who sees **`$160`** knows the other has `$80` and will **never switch**.
      - Knowing `$160` never switches, a player who sees **`$80`** knows that if the other player agrees to switch, the other player *must* have `$40` (not `$160`), so **`$80` never switches**!
      - By iterated elimination (`$160 -> $80 -> $40 -> $20 -> $10`), **no trade ever takes place**!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Requiring **mutual consent** to trade (`"The catch is that the other person is only willing to trade when it is in his or her interest to do so"`, l. 11955) plus a bounded maximum possible amount (`$160`).
    - **Catastrophic Loss?**: Losing half your money on a sucker swap.

87. **Here's Mud in Your Eye (Three Dirty Children / Common Knowledge Induction Puzzle)**
    - **Heading & First Line**: `"HERE’S MUD IN YOUR EYE"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L11974-L11996)) — `"One of our colleagues decided to go to a Jackson Browne concert at Red Rocks, Colorado."`
    - **Players, Moves, Timing**: $N = 3$ dirty-faced concertgoers (or $N$ people with mud on their foreheads). Each sees the other two faces but not their own. A passerby announces publicly: `"At least one of you has mud on your forehead."` Then asks repeatedly: `"Do you know whether you have mud on your forehead?"` Sequential rounds of simultaneous announcements.
    - **Payoffs**: Figuring out whether your own forehead is muddy.
    - **Family**: `signalling` / `other` (common knowledge / iterative epistemic game).
    - **Best Move / Real People**: With 3 muddy foreheads ($A, B, C$), on Question 1 all three say `"No"`; on Question 2 all three say `"No"`; on **Question 3** all three deduce they have mud and say `"Yes"`! (For $k$ muddy foreheads, they know on round $k$).
    - **THE RULE THAT CHANGES THE BEST MOVE**: The public announcement turns *mutual* knowledge into **common knowledge** (`"Everyone already knew that at least one person had mud on his forehead... What the announcement changed was what everyone knew that everyone knew"`, l. 11991).
    - **Catastrophic Loss?**: No.

88. **Red I Win, Black You Lose (Barry Nalebuff's Cambridge May Ball Roulette Tournament)**
    - **Heading & First Line**: `"RED I WIN, BLACK YOU LOSE"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L11997-L12047) & fn [l. 14273](file:///home/masih/Work/tries/aos/book-full.txt#L14273-L14276)) — `"While we might never get the chance to skipper in an America’s Cup race"`
    - **Players, Moves, Timing**: 2 leading players (**Barry** with `£700` in funny-money chips vs. **Woman in Second Place** with `£500` in chips; other players far behind) before the final spin of the roulette wheel at a Cambridge May Ball. Winner of the most chips wins a bottle of champagne (second place gets nothing). Moves: On the final spin, the Woman bets first, putting all `£500` on **Red** (pays 1:1, reaching `£1,000` if Red hits, `£0` if Black/0 hits); Barry moves second and chooses how much and where to bet. Sequential.
    - **Payoffs**: Winner-take-all bottle of champagne (`1` for 1st place, `0` for 2nd place).
    - **Family**: `other` (sequential leader-follower tournament game, like America's Cup #4).
    - **Best Move / Real People**:
      - **Optimal move**: Barry should **imitate the follower** (`"monkey see, monkey do"`) and bet **`£301` (or `£500`) on Red**! If Red hits, Barry has `£1,001 > £1,000` and wins; if Black hits, Barry has `£399 > £0` and still wins — **guaranteeing a 100% victory**!
      - **What Barry actually did at 3:00 AM after too much champagne** (fn l. 14273): Barry bet `£200` on **Even**, giving himself 5:1 odds, lost while Red/Odd hit, and she won!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Moving **second** after observing the trailing player's bet in a two-player winner-take-all contest (`"By betting £301 on Red, Barry is guaranteed to stay ahead whether the ball lands on Red or Black"`, l. 12036).
    - **Catastrophic Loss?**: Losing the winner-take-all tournament on the final spin.

89. **The Shark Repellent That Backfired (Sequential Roll-Call Voting on an 80% Supermajority Takeover Clause)**
    - **Heading & First Line**: `"THE SHARK REPELLENT THAT BACKFIRED"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12048-L12146)) — `"Corporations have adopted many new and innovative ways, often called 'shark repellents,' to make hostile takeovers more difficult."`
    - **Players, Moves, Timing**: 5 board members / shareholders (**A, B, C, D, E**, `20%` each) voting sequentially in clockwise roll-call order (`A -> B -> C -> D -> E`) on a hostile takeover bid. **Current management ($A$ and $B$)** oppose the takeover (`Vote No`) unless it is going to pass anyway, in which case they **prefer to be on the winning side (`Vote Yes`)** so the new Raider doesn't fire them! **Outside shareholders ($C, D, E$)** want the takeover to fail (`prefer No over Yes`), or wait — let's quote the exact preferences in prose (l. 12065–12140):
      - All 5 directors ($A, B, C, D, E$) **prefer that the takeover be rejected** (`Outcome No > Outcome Yes`), **EXCEPT** that if the outcome is already determined (either going to pass or going to fail regardless of a director's own vote), each director prefers to **vote `Yes`** to curry favor with the Raider (`"no one wants to cast a futile No vote that only serves to anger the raider"`, l. 12078)!
      - Under **Simple Majority (`3 of 5` needed to pass)**:
        - For the takeover to fail, `3` directors must vote `No`. By backward induction, if `A, B, C` all vote `No` (`3 No's`), the takeover is already defeated, so `D` and `E` can safely vote `Yes`! Foreseeing this, `A, B, C` realize each of their `No` votes is **pivotal**, so `A, B, C` vote `No`, `D, E` vote `Yes`, and the **takeover fails (`3 No, 2 Yes`)**!
      - Under the **"Shark Repellent" Supermajority (`4 of 5` [80%] needed to pass, so only `2 No` votes are needed to block!)**:
        - Now only **`2 No` votes** are required to defeat the takeover!
        - Suppose `A` votes `Yes` (passing the buck to `B, C, D, E`). Then among the remaining 4 voters, wait: why does the 80% supermajority *backfire* when $A, B, C$ want to block while $D, E$ already favor the Raider (`2 Yes` votes already in the Raider's pocket, or each voter passes the buck)? Let's check the exact numbers in text (l. 12085–12140): Suppose the Raider already controls `1` or `2` votes, OR in the 5-voter board, under simple majority (`3 Yes` to pass, `3 No` to block), wait: in the text's exact story (l. 12080–12142), **every voter prefers the takeover to succeed (`Yes`) if and only if they have to cast the deciding vote?** No! Let's check lines 12060–12145 using a tiny read if needed, or check what l. 12123 said: `"Now look at the fourth voter's dilemma."` Let's read lines 12055–12146 with `read_file` so our quote and numbers for #89 and #90 are 100% verbatim! Let's do a quick `read_file` on lines 12055–12883.
89. **The Shark Repellent That Backfired (Piper's Pickled Peppers vs. Sea Shells by the Sea Shore Ltd.)**
    - **Heading & First Line**: `"THE SHARK REPELLENT THAT BACKFIRED"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12048-L12145)) — `"Corporations have adopted many new and innovative ways, often called 'shark repellents,' to make hostile takeovers more difficult."`
    - **Players, Moves, Timing**: 5 board members (`1` hostile raider **Sea Shells by the Sea Shore Ltd.** owning `51%` of stock + `4` grandchildren of the founder of **Piper's Pickled Peppers**, each owning `12.25%` of stock). Moves: Sea Shells proposes a board restructuring and votes `Yes` first; the 4 family directors vote sequentially in clockwise order around the boardroom table (`3 out of 5` votes required to pass). Sequential.
    - **Payoffs**: Under the company's "shark repellent" charter rule, if a restructuring proposal **fails**, the proposer (`Sea Shells`) and anyone who voted `Yes` are stripped of their board seats and their stock is divided equally among the `No` voters! To exploit this, Sea Shells writes a conditional proposal with 3 clauses:
      1. If it passes **5–0 (unanimously)**, Sea Shells replaces the board and gives each old director a small compensation (`"lead parachute"`).
      2. If it passes **4–1**, the lone `No` voter is removed with `$0`.
      3. If it passes **3–2**, Sea Shells transfers **all `51%` of its stock equally to the other two `Yes` voters (`+25.5%` each)**, and the two `No` voters are removed with `$0`!
    - **Family**: `voting` / `other` (backward induction divide-and-conquer).
    - **Best Move / Real People**:
      - Look at the **5th (final) voter** facing a `2–2` tie: if he votes `Yes`, the proposal passes `3–2` and he gets **`25.5%`** of the company's stock; if he votes `No`, the proposal fails `2–3` and Sea Shells's `51%` + the other `Yes` voter's `12.25%` (`63.25%` total) are split among the 3 `No` voters, giving him only $(51 + 12.25)/3 = \mathbf{21.1\%} < 25.5\%$! So at `2–2`, the 5th voter votes **`Yes`**.
      - Knowing the 5th voter will break a `2–2` tie in favor of `Yes`, the **4th voter** sees that at `1 Yes, 2 No` he can vote `Yes` to create a `2–2` tie and collect **`25.5%`**, whereas at `2 Yes` or `3 Yes` the proposal is guaranteed to pass anyway so voting `Yes` avoids being left with `$0`.
      - Knowing the 4th and 5th voters will vote `Yes`, the **2nd and 3rd voters** realize the proposal will pass even if they both vote `No`, so they *also* vote `Yes` to get the unanimous `5–0` small compensation rather than `$0`! Thus the proposal passes **5–0 unanimously** and Sea Shells pays almost nothing!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Clockwise sequential voting combined with the charter's forfeiture penalty and Sea Shells's conditional `3–2` bribe (`25.5% > 21.1%` at the `2–2` node): `"start at the end and make sure that the final two voters have an incentive to vote for the proposal"` (l. 12096).
    - **Catastrophic Loss?**: Yes — losing one's board seat and stock holdings (`"shown the door"`).

90. **Tough Guy, Tender Offer (Robert Campeau's Two-Tiered Takeover Bid for Federated Stores vs. Macy's Conditional Bid)**
    - **Heading & First Line**: `"TOUGH GUY, TENDER OFFER"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12147-L12222) & fn [l. 14277](file:///home/masih/Work/tries/aos/book-full.txt#L14277-L14279)) — `"When Robert Campeau made his first bid for Federated Stores (and its crown jewel, Bloomingdales), he used the strategy of a two-tiered tender offer."`
    - **Players, Moves, Timing**: $N$ shareholders of Federated Stores + 2 rival raiders (**Campeau** and **Macy's**). Simultaneous shareholder tendering.
    - **Payoffs**: Pre-takeover stock price = **`$100/share`**.
      - **Campeau's Unconditional Two-Tiered Offer**: Pays **`$105/share`** for the first `50%` of shares tendered and **`$90/share`** for the second `50%` (prorated across all tendered shares: if $X\% \ge 50\%$ tender, everyone who tenders receives the blended price $\frac{50 \times 105 + (X - 50) \times 90}{X}$, which is **`$97.50/share`** if `100%` tender; untendered shares get only **`$90/share`** if Campeau wins control!).
      - **Macy's Conditional Offer**: Pays **`$102/share`** *if and only if* Macy's receives a majority (`>50%`) of shares.
    - **Family**: `prisoners' dilemma` (coercive multiperson tender offer).
    - **Best Move / Real People**: **Tendering to Campeau's two-tiered offer is a strictly dominant strategy** for every individual shareholder:
      1. If `<50%` tender to Campeau, Campeau's offer fails (stock stays `$100` or Macy's wins at `$102`), but anyone who tendered to Campeau still gets the unconditional first-tier **`$105`**!
      2. If `>50%` tender to Campeau, Campeau wins; tendering yields at least **`$97.50`**, whereas not tendering (or tendering to Macy's) gets stuck in the back-end second tier at **`$90`**!
      3. If exactly `50%` tender, tendering gets **`$105`**.
      Thus `100%` of shareholders tender to Campeau and receive **`$97.50/share`** — less than the `$100` pre-bid price and less than Macy's `$102` offer!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Making Macy's `$102` counteroffer **unconditional** rather than conditional on getting `50%`: `"An unconditional bid by Macy’s destroys the equilibrium in which the two-tiered bid succeeds"` (l. 12212; as fn l. 14277 notes, then no pure-strategy equilibrium exists and shareholders use randomized strategies).
    - **Catastrophic Loss?**: Shareholders lose value (`$97.50 < $100`), and in 1989 Campeau's debt load forced Federated Stores into **Chapter 11 bankruptcy** (l. 12218).

91. **The Safer Duel (Effect of Pistol Accuracy on Survival in a Two-Person Duel)**
    - **Heading & First Line**: `"THE SAFER DUEL"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12224-L12249)) — `"As pistols become more accurate, does that change the deadliness of a duel?"`
    - **Players, Moves, Timing**: 2 symmetric duelists walking toward each other with pistols. Continuous-time sequential.
    - **Payoffs**: Survive vs. Die.
    - **Family**: `duel or preemption`.
    - **Best Move / Real People**: As established in Chapter 10, two symmetric duelists hold their fire until the moment their hit probabilities satisfy $p(t) + q(t) = 1$, i.e., **`p(t) = 1/2`**. If pistols are made *less* accurate, the duelists simply walk closer together until the hit probability reaches `1/2`! Thus **each duelist's survival probability remains `1/2` regardless of pistol accuracy**!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Fixing the firing distance (rather than letting duelists walk closer until $p(t) = 1/2$): `"suppose we try to make dueling safer by reducing the accuracy of the pistols. The new outcome is that the adversaries will come closer to one another before firing... A change in the rules need not affect the outcome; all the players will adjust their strategies to offset it"` (l. 12232–12247).
    - **Catastrophic Loss?**: Yes — death (`50%` mortality rate).

92. **The Three-Way Duel (Larry, Moe, and Curly / Truel)**
    - **Heading & First Line**: `"THE THREE-WAY DUEL"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12250-L12295) & fn [l. 13853](file:///home/masih/Work/tries/aos/book-full.txt#L13853-L13855)) — `"Three antagonists, Larry, Moe, and Curly, are engaged in a three-way duel."`
    - **Players, Moves, Timing**: 3 duelists (**Larry** = `30%` accuracy, **Moe** = `80%` accuracy, **Curly** = `100%` accuracy). Two rounds of sequential shots in fixed order: `Larry -> Moe -> Curly`, then Round 2 for survivors: `Larry -> Moe -> Curly`.
    - **Payoffs**: Ranked by each player: `1st = Sole survivor`, `2nd = One of two survivors`, `3rd = All three survive`, `4th = Getting killed`.
    - **Family**: `duel or preemption` / `other` (3-player sequential elimination).
    - **Best Move / Real People**:
      - If Larry shoots at Moe and hits, Curly (`100%` shot) immediately kills Larry on the next turn (`0%` survival for Larry).
      - If Larry shoots at Curly and hits, Moe (`80%` shot) shoots at Larry, leaving Larry `<20%` survival.
      - **Larry's optimal Round 1 move**: **Fire up in the air (deliberately miss)!** Then Moe (`80%`) must shoot at Curly (`100%`); if Moe misses (`20%`), Curly kills Moe; either way, only *one* rival survives Round 1, and **Larry gets the first shot in Round 2**!
      - Resulting winning/survival probabilities (l. 12291 & fn 2 l. 13853):
        - **Moe (`80%` shot)**: **`56%`** (`0.80 \times 0.70 = 56%`)
        - **Larry (`30%` shot)**: **`41.2%`** (`0.30 + 0.70 \times 0.80 \times 0.20 = 41.2%`)
        - **Curly (`100%` shot)**: **`14%`** (`0.20 \times 0.70 = 14%`) — the sharpest shooter has the **lowest** chance of surviving!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Moving from a 2-player duel to a **3-player duel** where the two strongest players must target each other first: `"A weak player who threatens no one may end up surviving if the stronger players kill each other off. Curly, although he is the most accurate, has the lowest chance of survival—only 14 percent"` (l. 12289).
    - **Catastrophic Loss?**: Yes — death (`86%` chance of death for Curly!).

93. **The Risk of Winning (Bidding in a Vickrey Auction Under Payment Uncertainty)**
    - **Heading & First Line**: `"THE RISK OF WINNING"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12296-L12330)) — `"One of the more unusual features of a Vickrey sealed-bid auction is that the winning bidder does not know how much she will have to pay until the auction is over"`
    - **Players, Moves, Timing**: $N$ risk-averse bidders with private valuations in a Vickrey second-price sealed-bid auction. Simultaneous.
    - **Payoffs**: Winner gets item worth $V$ and pays the second-highest bid $B_{(2)}$.
    - **Family**: `auction`.
    - **Best Move / Real People**: Even when a bidder is risk-averse and dislikes uncertainty over what the second-highest bid will be, **bidding her exact true valuation $V$ remains a dominant strategy** (`"While there is uncertainty about what the winner will pay, this uncertainty is only over the degree of good news... That means bidding your true value"`, l. 12324).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Private values vs. common values (in private values, paying the second-highest bid means uncertainty is purely over the size of positive surplus $V - B_{(2)} \ge 0$).
    - **Catastrophic Loss?**: No (as long as you do not bid above $V$).

94. **But One Life to Lay Down for Your Country (King Henry V at Agincourt & Roald Amundsen at the South Pole)**
    - **Heading & First Line**: `"BUT ONE LIFE TO LAY DOWN FOR YOUR COUNTRY"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12331-L12431) & fn [l. 14280](file:///home/masih/Work/tries/aos/book-full.txt#L14280-L14285)) — `"How can the commanders of an army motivate its soldiers to risk their lives for their country?"`
    - **Players, Moves, Timing**: Commander (**King Henry V** before the Battle of Agincourt, Oct. 25, 1415; or **Roald Amundsen** on his South Pole expedition, fn l. 14280) + $N$ soldiers/crewmen. Moves: Commander publicly offers free passage home (`"he which hath no stomach to this fight, / Let him depart; his passport shall be made, / And crowns for convoy put into his purse"`) to anyone who steps forward in front of his comrades; each soldier chooses to step forward (leave) or stay silent (fight). Simultaneous/public.
    - **Payoffs**: Individual survival vs. public shame in front of comrades (`"everyone is too ashamed to do so"`).
    - **Family**: `prisoners' dilemma` / `coordination (stag hunt, meeting)` (battlefield courage & public commitment).
    - **Best Move / Real People**: By forcing any defector to step out in full view of all companions, nobody leaves, and the public act of declining the passport home psychologically burns their bridges (`"By their act of rejecting the offer, the soldiers have psychologically burned their ships home"`, l. 12375; Amundsen's men all stayed too, later muttering `"Why did you say yes? If only you had answered no, I would have done the same"`, fn l. 14283).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Making the opt-out choice **public in front of all peers** rather than secret (`"The catch is that anyone who wants to take up this offer has to do so in full view of all of his companions"`, l. 12372).
    - **Catastrophic Loss?**: Yes — death in battle at Agincourt or on the Antarctic ice.

95. **Winning Without Knowing How (Gale's Rectangular Dot Game "ZECK" / Chomp)**
    - **Heading & First Line**: `"WINNING WITHOUT KNOWING HOW"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12432-L12470)) — `"Chapter 2 introduced games in which players move in sequence and which always end after a finite number of moves."`
    - **Players, Moves, Timing**: 2 players playing **ZECK** (David Gale's Chomp) on a rectangular grid of dots (e.g., $7 \times 4$; diagrams at l. 12444, 12448 are images, `table not in text`). Each turn, a player picks one remaining dot and removes it along with all dots to its northeast (above and to the right). The player forced to take the last dot (bottom-left corner) **loses**. Sequential.
    - **Payoffs**: Win vs. Lose (finite, no-tie game of complete information).
    - **Family**: `other` (finite sequential game / strategy-stealing proof).
    - **Best Move / Real People**: For *every* rectangle with more than 1 dot, the **first player has a guaranteed winning strategy** (proved by strategy-stealing: if Player 2 had a winning reply to Player 1 taking only the top-right corner dot, Player 1 could simply make that reply on Move 1!). Yet the general formula for the winning move is unknown!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Ability of the first mover to remove the single top-right corner dot (`"no matter how the second player responds, the board will be left in a configuration that the first player could have created in his first move"`, l. 12465).
    - **Catastrophic Loss?**: Loss of game.

96. **A Burqa for Prices (Shrouded Add-On Prices: Car Rental Gas, Hotel Phone Calls, Printer Toner, Cell Phone Overages)**
    - **Heading & First Line**: `"A BURQA FOR PRICES"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12471-L12520) & fn [l. 14286](file:///home/masih/Work/tries/aos/book-full.txt#L14286)) — `"Hertz and Avis advertise that you can rent a car for $19.95/day."`
    - **Players, Moves, Timing**: Competing firms (Hertz vs. Avis; hotels; HP vs. Lexmark; cell-phone carriers) + Consumers comparing base prices on Expedia. Simultaneous.
    - **Payoffs**: Base price (`$19.95/day` rental car; `$40/month` for 800 cell minutes) vs. shrouded back-end fees (2x pump price for rental gas; `$2/min` hotel calls; `35¢/min` cell overage).
    - **Family**: `prisoners' dilemma` / `tipping` (shrouded-attributes equilibrium).
    - **Best Move / Real People**: Any lone firm that advertises an honest all-in price (`+$2/day` with no gas rip-off) looks more expensive on Expedia and loses customers, while competing firms give away the base good (free cell phones, cheap laser printers) and compete away all their back-end profits!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Mandatory all-in price disclosure or comparison-shopping engines that rank by total all-in cost (`"require that hotels, car rental companies, and cell phone providers advertise the all-in price paid by the average customer"`, l. 12515).
    - **Catastrophic Loss?**: No.

97. **What Price a Dollar? (Martin Shubik's Dollar Auction)**
    - **Heading & First Line**: `"WHAT PRICE A DOLLAR?"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12615-L12675)) — `"Professor Martin Shubik of Yale University designed the following game of entrapment."`
    - **Players, Moves, Timing**: Auctioneer + 2 (or $N$) bidders (**Eli** and **John**, each with a known wallet budget of **`$2.50`**). Moves: Ascending bids in `5-cent` (or `10-cent` / dime) increments for a `$1.00` bill. **Highest bidder wins the `$1.00`, but BOTH the highest and second-highest bidders must pay their bids to the auctioneer!** Sequential.
    - **Payoffs**:
      - Once bidding reaches `$0.60` (leader) vs. `$0.55` (second), the `$0.55` bidder loses `55 cents` by quitting vs. `35 cents` lost (`$0.65 - $1.00 = +35 cents` net) by bidding `$0.65`; at `$3.60` vs. `$3.55`, the `$3.55` bidder loses `$3.55` by quitting vs. `$2.65` (`$3.65 - $1.00`) by bidding `$3.65`!
      - With **known budgets of `$2.50` each and `$0.10` increments**:
        - If Eli bids `$1.60`, John knows Eli is committed to go all the way to `$2.50` (since spending `$0.90` more to win `$1.00` beats losing `$1.60` for nothing).
        - Because `$1.60` is an unstoppable winning bid against anything $\le \$1.50$, by backward induction **`$0.70`** is an unstoppable winning opening bid against anything $\le \$0.60$!
    - **Family**: `auction` / `war of attrition` (all-pay escalation trap).
    - **Best Move / Real People**:
      - With known `$2.50` budgets and `10-cent` increments, the first player opens at **`$0.70`** (or `$1.00` if budgets are unlimited) and all other players pass!
      - Even better: **collude** before bidding so one designated student bids **`$0.10`**, nobody else bids, and the students split the **`$0.90`** profit!
      - Real people (Yale undergraduates and Cold War superpowers): Bid naively in small increments and escalate well past `$1.00` (`$3.60+`) until someone runs out of money!
    - **THE RULE THAT CHANGES THE BEST MOVE**:
      1. The rule that **the second-highest bidder must also pay his bid** (`"both the highest and the second highest bidders pay their bids to the auctioneer"`, l. 12619), which turns sunk bids into an escalation trap.
      2. Known vs. unknown wallet budgets (`"it is critical that everyone know everyone else’s budget. When budgets are unknown, as one would expect, an equilibrium will exist only in mixed strategies"`, l. 12663) or pre-play collusion.
    - **Catastrophic Loss?**: Yes — exhausting one's entire bankroll/wallet (`$2.50` paid for `$1.00`, and in the Cold War nuclear arms race parallel, `"costs in the trillions of dollars"`, l. 12672).

98. **The King Lear Problem (Disinheriting Children Who Fail to Visit)**
    - **Heading & First Line**: `"THE KING LEAR PROBLEM"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12676-L12715)) — `"Tell me, my daughters / Since now we will divest us both of rule"`
    - **Players, Moves, Timing**: Parents + $N \ge 2$ children. Moves: Parents write a will requiring each child to visit once and phone twice a week to share the estate equally; children collude to visit zero times, knowing parents won't disinherit *all* of them. Simultaneous/repeated among children.
    - **Payoffs**: Equal share of inheritance (`1/N`) vs. `100%` of inheritance vs. `$0`.
    - **Family**: `prisoners' dilemma` (used in reverse to break the children's cartel, just like Warren Buffett's Dilemma #7!).
    - **Best Move / Real People**: Revise the will: any child meeting the quota shares the estate; **if ALL children fall below the quota, give `100%` of the estate to whichever child visits the most!** Now, if the children agree to visit zero times, any child who makes just *one* phone call jumps from `1/N` to `100%` of the estate, breaking their cartel and forcing all children to meet the full quota!
    - **THE RULE THAT CHANGES THE BEST MOVE**: Awarding `100%` of the estate to the highest-visiting child whenever all children fall below the quota (`"In that case, give all of the estate to the child who visits the most. This will make the children’s reduced visiting cartel impossible to maintain"`, l. 12707) — which works for $N \ge 2$ children, but **fails for an only child ($N = 1$)** (`"Obviously, this strategy fails with only children"`, l. 12713).
    - **Catastrophic Loss?**: Complete disinheritance (`$0`) for a child who gets undercut.

99. **United States v. Alcoa (1945 Excess Capacity Entry Deterrence)**
    - **Heading & First Line**: `"UNITED STATES V. ALCOA"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12716-L12752)) — `"An established firm in an industry stands to gain by keeping out new competition."`
    - **Players, Moves, Timing**: 2 players (Incumbent **Alcoa** vs. Potential Entrant). Moves: Alcoa builds excess refining capacity in advance or does not; Entrant enters or stays out; if Entrant enters, Alcoa fights a price war or accommodates. Sequential.
    - **Payoffs**: Monopoly profit vs. price-war losses.
    - **Family**: `duel or preemption` / `other` (entry deterrence via sunk cost commitment).
    - **Best Move / Real People**: Verbal threats of a price war are not credible because a price war hurts the incumbent too; by sinking capital into excess capacity in advance, Alcoa lowered its marginal cost of expanding output in a price war, making post-entry predation credible and deterring entry (until Judge Learned Hand convicted Alcoa in 1945).
    - **THE RULE THAT CHANGES THE BEST MOVE**: Sinking capacity investment *before* the entrant decides whether to enter (`"Installing capacity in excess of the needs of current production gives credibility to the established firm’s threat... the capital costs have already been incurred and are bygones"`, l. 12746).
    - **Catastrophic Loss?**: Antitrust conviction / breakup of Alcoa, or entrant bankruptcy in a price war.

100. **Arms Across the Ocean (U.S. vs. U.K. Gun Ownership by Homeowners and Criminals)**
     - **Heading & First Line**: `"ARMS ACROSS THE OCEAN"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12753-L12825) & fns [l. 14287](file:///home/masih/Work/tries/aos/book-full.txt#L14287-L14297)) — `"In the United States many homeowners own guns for self-defense. In Britain almost no one owns a gun."`
     - **Players, Moves, Timing**: 2 groups (**Homeowners** and **Criminals**). Moves: Carry/Own Guns vs. Go Unarmed. Simultaneous in the U.S.; sequential (Criminals commit first via strict gun control) in Britain.
     - **Payoffs**: Table at l. 12764 is an image (`table not in text`), exact ordinal rankings (`1 = best, 4 = worst`) given in prose (l. 12763–12795 & fns l. 14290–14297):
       - **`(Unarmed Homeowners, Unarmed Criminals)`**: **`(1 for Homeowners, 2 for Criminals)`**
       - **`(Unarmed Homeowners, Armed Criminals)`**: **`(4 for Homeowners, 1 for Criminals)`**
       - **`(Armed Homeowners, Armed Criminals)`**: **`(3 for Homeowners, 3 for Criminals)`**
       - **`(Armed Homeowners, Unarmed Criminals)`**: **`(2 for Homeowners, 4 for Criminals)`**
     - **Family**: `other` (asymmetric 2x2 game where one side has a dominant strategy, plus an internal `prisoners' dilemma` among criminals).
     - **Best Move / Real People**:
       - In the **simultaneous game** (U.S.), `Armed` is a strictly dominant strategy for Criminals (`1 > 2` and `3 > 4`), and Homeowners' best response to Armed Criminals is `Armed` (`3 > 4`), trapping both in **`(Armed, Armed) = (3, 3)`**.
       - In the **sequential game** where Criminals can credibly commit first to go **Unarmed** (Britain, via strict gun control laws that bind all criminals together), Homeowners respond by going **Unarmed** (`1 > 2`), moving the equilibrium to **`(Unarmed, Unarmed) = (1, 2)`**, which makes **both Homeowners (`1 vs. 3`) and Criminals (`2 vs. 3`) better off**! (Note from fn l. 14295: if Homeowners move first unconditionally, Criminals still go Armed regardless, so Homeowners must go Armed -> `(3, 3)`).
     - **THE RULE THAT CHANGES THE BEST MOVE**: Strict gun-control laws that solve the criminals' internal prisoners' dilemma and allow Criminals to commit *first* to being unarmed: `"In the simultaneous-move game it was dominant for them to carry guns. In the sequential-move game, they chose not to... Britain’s strict control of guns allows criminals to commit to work unarmed"` (l. 12805–12820).
     - **Catastrophic Loss?**: Yes — fatal shootings when both sides are armed (`(3, 3)`).

101. **Fooling All the People Some of the Time: The Las Vegas Slots (90% Average Payback with Hidden 120% Slot Machines)**
     - **Heading & First Line**: `"FOOLING ALL THE PEOPLE SOME OF THE TIME: THE LAS VEGAS SLOTS"` ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12826-L12883)) — `"Any gambling guide should tell you that slot machines are your worst bet."`
     - **Players, Moves, Timing**: Casino Owner vs. $N$ Slot Players. Moves: Casino sets average payback at `90%` while advertising that *some* machines are set to **`120%`** payback (putting odds in the player's favor) and reshuffles which machines are `120%` each day; players try to identify and play the `120%` machines. Simultaneous / repeated.
     - **Payoffs**: Quarter (`$0.25`) slot machine where a `$10,000` jackpot with a `1 in 40,000` probability accounts for `100%` (`$0.25`) of expected value, so distinguishing a `120%` machine from an `80%` machine by sampling takes tens of thousands of pulls (longer than a day!).
     - **Family**: `signalling` / `zero-sum mixing` (hide-and-seek placement).
     - **Best Move / Real People**: Where must the casino place the `120%` machines? **Where they will be played the LEAST** (`"They make money only when people play the disadvantageous machines at least as much as the favorable or loose machines"`, l. 12846) — i.e., **not** near the entrance, aisles, or crowds, and **never** two `120%` machines right next to each other; so a strategic player looks for machines in uncrowded, inconvenient corners (`"If you see a crowd playing a bank of machines, stay away"`, l. 12872)!
     - **THE RULE THAT CHANGES THE BEST MOVE**: If the majority of gamblers figured out the casino's placement rule and played only the uncrowded corner machines, the casino would have to randomize placement (`"If the majority of the people were able to figure it out, the casino would have to change its strategy"`, l. 12880).
     - **Catastrophic Loss?**: Gambler ruin.

102. **Information Escrow in Legal Plea Bargaining (Final Footnote Game)**
     - **Heading & First Line**: Footnote to Chapter 14 ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L14298-L14301)) — `"In an information escrow, each side makes an offer and then a neutral party evaluates whether the offers cross or not."`
     - **Players, Moves, Timing**: 2 players (**District Attorney** and **Defendant**) + Neutral Information Escrow Agent. Simultaneous sealed offers.
     - **Payoffs**: DA submits minimum acceptable prison sentence (e.g., `3 years` or `6 years`); Defendant submits maximum acceptable sentence (e.g., `5 years`). If $\text{DA offer} \le \text{Defendant max}$ (`3 <= 5`), a plea deal is struck; if they do not overlap (`6 > 5`), **neither party learns what the other offered**, preventing an offer from being used as a sign of weakness at trial!
     - **Family**: `bargaining` / `signalling`.
     - **THE RULE THAT CHANGES THE BEST MOVE**: Using a neutral **information escrow** that conceals non-overlapping offers (`"if the offers don’t overlap—if, say, the DA asks for six years—then neither party learns what the other has put on the table"`, l. 14300).
     - **Catastrophic Loss?**: Full prison sentence at trial.

---

## Prisoners' dilemma instances

Every instance where the text names or describes a prisoners' dilemma, with verbatim quote, setting, and what resolves or worsens it:

1. **Warren Buffett's Campaign Finance Reform Dilemma** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L783-L833))
   - **Quote**: `"Why would this scheme work? Look at the incentives of each party. Each wants to get the billion dollars on the off chance that the legislation fails, or at least prevent the other party from getting the money... What a devilishly clever manipulation of incentives!"` (l. 808–819).
   - **Setting**: Democrats and Republicans voting on campaign finance reform under an Eccentric Billionaire's pledge to pay $1 billion to the party casting more votes for the bill *if* the bill fails.
   - **Resolves / Worsens**: Buffett *deliberately creates* a prisoners' dilemma between the two parties so their dominant strategies (`Vote Yes`) pass the reform at $0 cost to the billionaire.

2. **Truman Capote's *In Cold Blood* Police Interrogation & Classical Prisoners' Dilemma** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L834-L853) & fn [l. 13912](file:///home/masih/Work/tries/aos/book-full.txt#L13912-L13919))
   - **Quote**: `"Buffett’s scenario works on the same ruthless logic as the famous game called the prisoners’ dilemma.† A typical example of that game can be found in Truman Capote’s In Cold Blood. Two suspects, Dick Hickock and Perry Smith, are arrested... Either can keep quiet or confess, implicating the other"` (l. 834–841).
   - **Setting**: Two murder suspects interrogated in separate rooms without communication.
   - **Resolves / Worsens**: Isolation and immunity offers to the first confessor **worsen** it (both confessed and were executed, fn l. 13916); communication or gang retaliation **resolves** it.

3. **Aesop's Mice Belling the Cat & Citizens Under a Tyrant (Khrushchev's Heckler)** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L854-L877))
   - **Quote**: `"While we usually think of the prisoners’ dilemma as a game with two players, the logic works just the same—or even more forcefully—when applied to tens or hundreds or thousands of players... When Nikita Khrushchev was denouncing Stalin at the Twentieth Party Congress in 1956, a heckler shouted, 'You were one of Stalin’s colleagues—why didn’t you stop him?' Khrushchev shouted back, 'Who said that?' Significantly, no one moved a muscle. Then Khrushchev said quietly, 'Now you know why.'"` (l. 854–877).
   - **Setting**: $N$ mice trying to bell a cat, or $N$ citizens under Stalin's dictatorship.
   - **Resolves / Worsens**: Large $N$ and severe individual punishment for the first mover **worsen** the dilemma.

4. **Four Opening Dilemmas of Chapter 3: Gas Station Price War (Nexon vs. Lunaco), Centrist Election Platforms, New England Fisheries Collapse, and *Catch-22* (Yossarian)** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2129-L2163) & fn [l. 13940](file:///home/masih/Work/tries/aos/book-full.txt#L13940-L13945))
   - **Quote**: `"What do the following situations have in common?... No prizes for correct answers—after all, the prisoners’ dilemma is the subject of this chapter"` (l. 2129 & l. 13940).
   - **Setting**: Retail gasoline price-cutting; two candidates abandoning their ideological bases for the center; fishermen depleting Georges Bank stocks; Yossarian trying to avoid combat missions in WWII.
   - **Resolves / Worsens**: Individual short-run incentives **worsen** it; military coercion (`Catch-22`), fisheries quotas, or repeated price matching **resolve** it.

5. ***L.A. Confidential* Interrogation (Sgt. Ed Exley vs. Fontaine, Coates, and Jones)** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2164-L2189), [l. 2372](file:///home/masih/Work/tries/aos/book-full.txt#L2372-L2382), [l. 5759](file:///home/masih/Work/tries/aos/book-full.txt#L5759-L5765))
   - **Quote**: `"In the book and movie L.A. Confidential, the 'good cop' Ed Exley is getting nowhere with his Prisoner’s Dilemma Stratagem"` (l. 5759; also l. 2164).
   - **Setting**: Three suspects held in separate cells offered a deal to snitch first.
   - **Resolves / Worsens**: **Resolved** (from the suspects' perspective) by fear of violent retaliation from accomplices' friends outside prison (`"when he emerges from jail, he may find friends of the other two waiting for him!"`, l. 2379).

6. **Tucker's Original Story & Tosca (Scarpia vs. Tosca)** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2190-L2208) & Note 2 [l. 13318](file:///home/masih/Work/tries/aos/book-full.txt#L13318-L13325))
   - **Quote**: `"A story of this kind was used by Princeton mathematician Albert W. Tucker in 1950 to explain the basic idea of game theory to an audience of psychologists, and therefore games with this structure have been called prisoners’ dilemmas ever since"` (l. 2190; Note 2 l. 13318 also notes Puccini's opera *Tosca*, where Tosca stabs Scarpia and Scarpia orders a real firing squad instead of blanks, double-crossing each other to mutual death).
   - **Setting**: Two prisoners (or Tosca and police chief Scarpia) who each have a dominant strategy to betray the other.
   - **Resolves / Worsens**: In *Tosca*, one-shot unenforceability **worsens** it into double betrayal and death for both.

7. **Rainbow's End vs. B. B. Lean Catalog Shirt Pricing** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2209-L2345), [l. 2751](file:///home/masih/Work/tries/aos/book-full.txt#L2751-L2875), [l. 5440](file:///home/masih/Work/tries/aos/book-full.txt#L5440-L5637), & fn [l. 13969](file:///home/masih/Work/tries/aos/book-full.txt#L13969-L13985))
   - **Quote**: `"Therefore, Both charge $70 is the dominant-strategy equilibrium of the game... This is their prisoners’ dilemma, or a lose-lose game; when each acts independently in its own separate best interest, the outcome is bad for both"` (l. 2306 & l. 5448).
   - **Setting**: Two competing mail-order catalog firms choosing between `$80` and `$70` (or `$40`).
   - **Resolves / Worsens**: **Resolved** for the firms by (a) infinite/indefinite repetition with an interest rate below `5.26%` (l. 2777), or (b) printing a `"meet the competition"` / `"beat the competition"` guarantee in the catalog (l. 2979, 5460, 5485). **Worsened** for the firms (to the benefit of consumers, fn l. 13969) by one-shot play, high discount rates, or antitrust bans on price-matching clauses.

8. **Baseball Plunking: American League vs. National League** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2383-L2396))
   - **Quote**: `"Batters in the American League are hit by pitches 11 to 17 percent more often than batters in the National League. Why?... In the American League, the pitchers don’t bat. Thus an American League pitcher who plunks a batter doesn’t have to fear direct retaliation"` (l. 2383–2392).
   - **Setting**: Pitchers throwing at batters in Major League Baseball.
   - **Resolves / Worsens**: Direct tit-for-tat retaliation when pitchers bat in the National League **resolves** it; the Designated Hitter rule in the American League insulates pitchers from personal retaliation and **worsens** plunking by 11–17%.

9. **Axelrod's Computer Tournaments, Rapoport's Tit for Tat, Southampton's 60 Programs, and Blood Feuds** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2398-L2477) & fn [l. 13986](file:///home/masih/Work/tries/aos/book-full.txt#L13986-L13997))
   - **Quote**: `"The slightest possibility of a mistake or a misperception results in a complete breakdown in the success of tit for tat"` (l. 2457).
   - **Setting**: 150-round repeated prisoners' dilemma computer tournaments and real-world feuds (*Huckleberry Finn*'s Grangerfords vs. Shepherdsons).
   - **Resolves / Worsens**: Clarity, niceness, provocability, and forgiveness (`"tit for two tats"` when noise is present) **resolve** it; noise/misperceptions with strict tit-for-tat or viewing the game as zero-sum winner-take-all **worsen** it into endless blood feuds.

10. **Cotton-Top Tamarin Monkeys Lever-Pulling Experiment** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2478-L2494))
    - **Quote**: `"Cotton-top tamarin monkeys were placed in a game where they had to pull a lever to give the other monkey food... Before they retaliated, they tolerated up to two failures by their partner"` (l. 2479–2489).
    - **Setting**: Pair of monkeys pulling levers to feed each other.
    - **Resolves / Worsens**: **Resolved** by a forgiving `"tit for two tats"` strategy.

11. ***Friend or Foe* Television Game Show** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2496-L2528))
    - **Quote**: `"Notice that choosing foe is a dominant strategy... Yet nearly half the contestants chose friend"` (l. 2508–2512).
    - **Setting**: Two game-show contestants dividing a $200–$16,400 prize pot in a one-shot simultaneous choice.
    - **Resolves / Worsens**: Social/fairness norms sustain ~50% cooperation; airing 40 episodes before Season 2 **worsened** cooperation in mixed-gender pairs (dropping to 34.2% for women and 42.3% for men).

12. **Flood and Dresher's 100-Round RAND Experiment** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2529-L2570))
    - **Quote**: `"Almost immediately after they had thought up the game, Flood and Dresher recruited two of their colleagues to play the dilemma game a hundred times"` (l. 2529).
    - **Setting**: Finitely repeated (100-round) 2-player prisoners' dilemma.
    - **Resolves / Worsens**: A known fixed final round (`Round 100`) unravels cooperation in theory, but uncertainty about whether the partner is a `"reciprocator"` type **resolves** it in practice until Round 99 (60/100 mutual cooperation).

13. **Battalio's 27-Student Texas A&M Classroom Dilemma** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2571-L2601))
    - **Quote**: `"When every student acts selfishly in this way, all write 2, and each gets 50 cents. If they had all colluded and written 1, each would have gotten $1.08"` (l. 2588).
    - **Setting**: 27 students choosing secretly between `1` and `2`.
    - **Resolves / Worsens**: Secret ballots and large $N = 27$ **worsened** it (only 4 of 27 cooperated, even after verbal agreement); public voting with social ostracism **resolves** it (l. 2627).

14. **Four-Player Public Goods Contribution Game & Altruistic Punishment** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2602-L2668))
    - **Quote**: `"More recent laboratory experiments of multiperson dilemmas use a format called the contribution game... when a second stage is added to the contribution game and players are given an opportunity to punish those who cheat... this increases the contributions in the first phase of the game dramatically"` (l. 2602, 2648).
    - **Setting**: 4 players contributing out of $10 to a doubled common pool.
    - **Resolves / Worsens**: Anonymity and repeated play without punishment **worsen** it (contributions decay from 50% to 10%); adding a costly peer-punishment stage (`33 cents` per `$1` fine) **resolves** it.

15. **Business Cartels: ADM/Ajinomoto Lysine Cartel, GE/Westinghouse/Allied-Chalmers Lunar-Cycle Turbines, FCC Spectrum Area-Code Signaling, Pratt & Whitney vs. Rolls-Royce Fuel Guarantee, Ethyl/DuPont Most-Favored-Customer Clause, and OPEC Oil Quotas** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L2798-L3003))
    - **Quote**: `"In the prisoners’ dilemma of price competition, detection of cheating is a major problem"` (l. 2880; OPEC at l. 2800).
    - **Setting**: Oligopoly price-fixing and quota-setting cartels.
    - **Resolves / Worsens**: **Worsened** (for cartel members) by unobservable secret price cuts, desperate members needing immediate cash (e.g., Nigeria in OPEC, l. 2800), and FBI/antitrust enforcement; **resolved** (for firms) by transparent market-sharing formulas (lunar calendar), public bids (FCC auctions), fuel-efficiency guarantees, and most-favored-customer / meet-the-competition clauses.

16. **Tragedies of the Commons: Overgrazing, Overfishing, Traffic Congestion, and Global Warming (Kyoto Protocol)** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L3005-L3081) & fn [l. 14002](file:///home/masih/Work/tries/aos/book-full.txt#L14002-L14018))
    - **Quote**: `"Each user gets the full benefit of his own use of the resource, while the cost of depletion is shared among all users. This is a multiperson prisoners’ dilemma"` (l. 3006–3010).
    - **Setting**: Shared pastures, oceans, groundwater, atmosphere.
    - **Resolves / Worsens**: Open access and lack of monitoring **worsen** it; Elinor Ostrom's 5 community governance principles (boundaries, tailored rules, routine monitoring, graduated sanctions, user design) or private property / Pigouvian taxes **resolve** it.

17. **Biological Reciprocal Altruism: Wilkinson's Costa Rican Vampire Bats** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L3083-L3121))
    - **Quote**: `"As you might expect, prisoners’ dilemmas arise in species other than humans... A bat that has been successful on a particular night can regurgitate some of the blood it has swallowed and feed it to an unsuccessful bat"` (l. 3083–3099).
    - **Setting**: Colony of ~12 vampire bats sharing blood meals to prevent starvation.
    - **Resolves / Worsens**: **Resolved** by small stable colonies, individual recognition, and withholding blood from past cheaters.

18. **Coke vs. Pepsi Price-Discount Coupons** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L4889-L4929))
    - **Quote**: `"In those weeks their campaigns will merely cancel each other out; neither firm increases its share and both make a lower profit. The strategies thus create a prisoners’ dilemma. The firms, being in an ongoing relationship, recognize that both can do better by resolving the dilemma"` (l. 4923–4927).
    - **Setting**: Coke and Pepsi running weekly promotional discounts.
    - **Resolves / Worsens**: **Resolved** by alternating promotions (26 weeks each with 0 overlaps over 52 weeks).

19. **Cutting the Salami / Moving in Small Steps in Construction, Arms Control, and Repeated PD** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L6515-L6546), [l. 6653](file:///home/masih/Work/tries/aos/book-full.txt#L6653-L6660))
    - **Quote**: `"Breaking up the game into a succession of small steps converts a one-shot prisoners’ dilemma into a repeated one"` (l. 6525; also l. 6653 on undermining an opponent's cartel PD).
    - **Setting**: Staged progress payments to a contractor or phased arms treaties.
    - **Resolves / Worsens**: Slicing one large transaction into many small steps **resolves** the dilemma; Conversely, when facing an *opponent's* cartel (like OPEC), helping them cheat secretly **worsens** their dilemma to your benefit (l. 6653).

20. **Ivy League Spring Football Practice, Classroom Curve Grading, and Academic Grade Inflation** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L7975-L8040), [l. 8685](file:///home/masih/Work/tries/aos/book-full.txt#L8685-L8690))
    - **Quote**: `"The colleges were caught in a multiperson prisoners’ dilemma: a game with more than two prisoners. An escape from the horns of this dilemma requires an enforceable collective agreement"` (l. 8017–8019).
    - **Setting**: 8 Ivy League schools over-practicing football at the expense of academics; students studying against a bell curve; departments inflating grades to boost enrollment.
    - **Resolves / Worsens**: **Resolved** by the Ivy League presidents' binding ban on spring practice (or Princeton's cap of 35% A grades across all departments, l. 8032).

21. **Bay Bridge vs. BART Commuting Congestion** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L8041-L8135), [l. 8685](file:///home/masih/Work/tries/aos/book-full.txt#L8685))
    - **Quote**: `"This is another example of the multiperson prisoners’ dilemma"` (l. 8071).
    - **Setting**: 10,000 commuters choosing between driving across the Bay Bridge ($20 + 5n$ minutes) and taking BART (40 minutes).
    - **Resolves / Worsens**: Unpriced bridge access **worsens** it (`4,000` drivers take 40 minutes instead of `2,000` drivers taking 30 minutes); a **$5 congestion toll** **resolves** it (l. 8121).

22. **Two-Tiered Hostile Takeover Bids (Campeau vs. Federated Stores)** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12147-L12222))
    - **Quote**: `"Because tendering is a dominant strategy, we expect everyone to tender. When everyone tenders, the average blended price per share may be below the pre-bid price"` (l. 12195).
    - **Setting**: Shareholders facing an unconditional front-loaded `$105` / back-loaded `$90` tender offer.
    - **Resolves / Worsens**: Prorated two-tier structure **creates** the dilemma for shareholders; corporate `"fair price"` charter amendments, court injunctions, or an **unconditional competing bid** (`$102` from Macy's) **resolve** it.

23. **Soldiers on the Battlefield (Henry V at Agincourt & Amundsen at the South Pole)** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12331-L12431) & fn [l. 14280](file:///home/masih/Work/tries/aos/book-full.txt#L14280-L14285))
    - **Quote**: `"Most armies would be finished if each soldier on the battlefield started to make a rational calculation of the costs and the benefits of risking his own life"` (l. 12334).
    - **Setting**: Soldiers choosing whether to stand and fight or flee.
    - **Resolves / Worsens**: **Resolved** by boot-camp conditioning, public opt-out shaming (`"in full view of all of his companions"`, l. 12373), and shared risk with the leader.

24. **Shrouded Add-On Pricing ("A Burqa for Prices")** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12471-L12520))
    - **Quote**: `"The problem is that the company who plays it straight puts itself at a disadvantage compared to its rivals... The firms compete away all of their future profits in the battle to attract customers"` (l. 12492, 12511).
    - **Setting**: Car rentals, hotels, printers, and cell-phone plans hiding back-end fees.
    - **Resolves / Worsens**: **Resolved** by mandatory all-in price disclosure or all-in comparison shopping sites.

25. **The King Lear Inheritance Problem** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12676-L12715))
    - **Quote**: `"We have put the children into a multiperson dilemma. The smallest amount of cheating brings a massive reward. A child who makes just one more phone call increases his or her inheritance from an equal share to 100 percent"` (l. 12709–12712).
    - **Setting**: Parents designing a will to prevent $N \ge 2$ children from colluding to cut back visits.
    - **Resolves / Worsens**: Giving 100% of the estate to whichever child visits the most whenever all children fall below the quota **pits the children in a prisoners' dilemma** that destroys their anti-visiting cartel.

26. **Armed Criminals vs. Homeowners ("Arms Across the Ocean")** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12753-L12825))
    - **Quote**: `"Even though criminals as a class may gain by taking the initiative and giving up guns, any one member of the group can get an additional advantage by cheating. This prisoners’ dilemma would destroy the credibility of the criminals’ initiative"` (l. 12798–12801).
    - **Setting**: Individual criminals deciding whether to carry a gun when criminals collectively would be better off if neither criminals nor homeowners carried guns.
    - **Resolves / Worsens**: Wide gun availability in the U.S. **worsens** it into `(Armed, Armed)`; strict national gun control in Britain **resolves** it into `(Unarmed, Unarmed)`.

---

## Annihilation and escalation

Every passage about mutual destruction, brinkmanship, doomsday devices, duels, wars of attrition, and escalating auctions:

1. **Intransigent Bargaining & Escalation of Losses (Luther, de Gaulle, de Lesseps)** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L632-L688))
   - **Quote**: `"The danger is that an inflexible person does not know when to compromise and may allow small losses to grow into major disasters"` (l. 674).
   - **Rule & Best Move**: Credible inflexibility wins one-shot bargaining when the opponent can still back down, but against nature or an equally committed opponent it causes catastrophic ruin; compromise when long-run relationships or physical constraints dominate.

2. **Burning Ships / Bridges (Xenophon, Hernán Cortés)** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L755-L775), [l. 6135](file:///home/masih/Work/tries/aos/book-full.txt#L6135-L6152))
   - **Quote**: `"Cortés scuttled his own ships upon arrival at Cempoala in Mexico. The Spaniards now had no choice: they must either defeat the Aztecs or perish trying"` (l. 765; also l. 6145 noting Cortés claimed worms ate the ships, and leaving the enemy a golden bridge of retreat).
   - **Rule & Best Move**: Eliminating your own retreat while leaving the opponent an avenue of escape makes fighting to the death automatic for your side and retreating optimal for the enemy.

3. **Chicken in *Rebel Without a Cause*, Teenage Highway Chicken, and Mixed-Strategy Crash Risk** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L3651-L3707), [l. 4871](file:///home/masih/Work/tries/aos/book-full.txt#L4871), [l. 5246](file:///home/masih/Work/tries/aos/book-full.txt#L5246-L5284))
   - **Quote**: `"If neither swerves, both may end up in the hospital, or worse... disconnect your steering wheel from the shaft and throw it out of the window in a manner that makes it very visible to the other driver. Then the other has no choice left except to swerve. (Unless both try to do this at the same time!)"` (l. 5252–5266).
   - **Rule & Best Move**: Visibly and irreversibly disable your ability to swerve *before* the rival can do so. If both commit simultaneously (or mix independently), mutual crash/destruction occurs with positive probability.

4. **Cold War Deterrence in Western Europe ("(Mini) Trip to the Gym No. 4")** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L5485-L5510), Workout [l. 13054](file:///home/masih/Work/tries/aos/book-full.txt#L13054-L13082))
   - **Quote**: `"If the Soviets invaded Western Europe, the United States would suffer a loss of –100 if it did nothing, and –200 if it counterattacked... By committing itself to counterattack automatically, the United States changes the game"` (l. 13056–13073).
   - **Rule & Best Move**: Because retaliating *after* an invasion is worse (`-200`) than acquiescing (`-100`), deterrence requires an automatic tripwire commitment *before* the invasion so the aggressor faces `-500 < 0` and stays out.

5. **Brinkmanship: *L.A. Confidential* Russian Roulette (Bud White vs. Leroy Fontaine)** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L5759-L5838))
   - **Quote**: `"White pulled out his .38, broke the cylinder, dropped shells on the floor. Left one in, spun the chamber, snapped it shut... The essence of brinkmanship is the deliberate creation of risk. This risk is sufficiently intolerable to your opponent that he prefers to eliminate the risk by following your wishes"` (l. 5769, 5873).
   - **Rule & Best Move**: When executing a threat with 100% certainty would destroy the threatener too (e.g., killing the only witness who knows the kidnap victim's location), create a *gradually escalating probability* ($1/6 \to 1/5 \to 1/4\dots$) of disaster that only the opponent's concession can stop.

6. **Brinkmanship: The Cuban Missile Crisis (JFK vs. Khrushchev, October 1962) & Unauthorized U-2 Shootdown** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L5839-L5914))
   - **Quote**: `"In other words, brinkmanship is 'chicken in real time': a game of increasing tension where the first to back down loses... During the Cuban missile crisis, a Soviet commander in Cuba shot down an American U-2 spy plane without authorization from Moscow. Had the United States retaliated automatically as planned, the crisis might have spiraled out of control"` (l. 5882, 5908).
   - **Rule & Best Move**: Start with a low-risk step (the naval `"quarantine"` blockade rather than an immediate air strike or invasion) that puts the burden of escalation on the opponent, while keeping tight command-and-control over subordinates and offering a face-saving exit (private pledge to remove U.S. missiles in Turkey, l. 6710).

7. **Brinkmanship in Civil Rights (MLK Jr.) and Northern Ireland** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L5915-L5923))
   - **Quote**: `"The violence escalated almost to the level of a civil war, and the British government was forced to step in"` (l. 5920).
   - **Rule & Best Move**: Peaceful protest leaders use the risk that radical followers or overreacting police will trigger wider conflict to compel moderates to negotiate.

8. **God's Deterrence Threat in Genesis & Scaling Down Threats** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L5990-L6050))
   - **Quote**: `"If carrying out the threat hurts your own interest too severely, the target of the threat will know that, come the day, you will back down"` (l. 6034).
   - **Rule & Best Move**: Never make a threat of total annihilation (`"in the day that thou eatest thereof thou shalt surely die"`) when executing it would destroy everything you care about; scale down the punishment or replace certainty with brinkmanship.

9. **De Gaulle's *Force de Frappe* & Mutually Assured Destruction (MAD)** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L6226-L6244), [l. 6340](file:///home/masih/Work/tries/aos/book-full.txt#L6340-L6355))
   - **Quote**: `"De Gaulle doubted that the United States would really be willing to sacrifice New York to save Paris"` (l. 6233).
   - **Rule & Best Move**: Put ownership of the deterrent weapon directly in the hands of the party whose survival is at stake.

10. ***Dr. Strangelove*'s Doomsday Machine vs. Controlled Loss of Control** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L6447-L6514))
    - **Quote**: `"The Doomsday Machine is designed to trigger itself automatically; it cannot be ’untriggered’ even by the Soviet leaders... 'The whole point of the Doomsday Machine... is lost... if you keep it a secret! Why didn’t you tell the world, eh?'... brinkmanship is a controlled loss of control: the threatener controls the size of the risk, although he does not control the outcome of the risk"` (l. 6459–6495).
    - **Rule & Best Move**: An automatic doomsday device is completely useless for deterrence if kept secret, and catastrophic if an accident (`General Jack D. Ripper`) occurs; brinkmanship replaces the `0%` or `100%` cliff with a sloped ramp of controllable risk.

11. **The Preemption Duel (Apple Newton vs. PalmPilot, Pistol Duels, Wet-Sponge Duel, "Trip to the Gym No. 8", and "The Safer Duel")** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L9449-L9530), [l. 12224](file:///home/masih/Work/tries/aos/book-full.txt#L12224-L12249), Workout [l. 13153](file:///home/masih/Work/tries/aos/book-full.txt#L13153-L13173), & fn [l. 14201](file:///home/masih/Work/tries/aos/book-full.txt#L14201-L14202))
    - **Quote**: `"The way we describe a preemption game suggests a duel and that analogy is exact... Each player waits to shoot until the point where his probability of hitting the other side is just equal to the other side’s chance of missing"` (l. 9492, 12235).
    - **Rule & Best Move**: In a 2-player duel where firing and missing gives the opponent a sure kill ($100\%$), fire at the exact instant $t^*$ where $p(t^*) + q(t^*) = 1$ (for symmetric duelists, $p(t^*) = 1/2$). Making pistols less accurate does not improve survival because duelists simply walk closer until $p(t) = 1/2$.

12. **The War of Attrition (Rupert Murdoch's Sky TV vs. British Satellite Broadcasting)** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L9531-L9589))
    - **Quote**: `"The opposite of the preemption game is a war of attrition. Instead of fighting to be first, here the battle is to be last... By the time BSB capitulated in November 1990, the two companies had lost over £1.2 billion between them"` (l. 9533, 9560).
    - **Rule & Best Move**: Because both winner and loser pay their sunk waiting costs, past losses are bygones at every moment; win by convincing the rival early that you have deeper pockets or an irreversible commitment to stay forever.

13. **Brinkmanship in Labor Strikes vs. Virtual Strikes** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L10031-L10245))
    - **Quote**: `"As the strike drags on, the strike losses escalate. Only when one side discovers that the other is truly the stronger party does the strike end... In the 2004–05 National Hockey League strike, the owners and players went over the brink and canceled the entire season"` (l. 10112–10117).
    - **Rule & Best Move**: Replace a destructive work-stoppage strike with a **virtual strike** (workers keep working, customers are served, and both wages and profits go to charity/escrow until agreement is reached).

14. **The Three-Way Duel (Larry [30%], Moe [80%], and Curly [100%])** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12250-L12295))
    - **Quote**: `"If Larry shoots at Moe and hits, then he signs his own death warrant... In fact, Larry’s best strategy is to fire up in the air!... Curly, although he is the most accurate, has the lowest chance of survival—only 14 percent"` (l. 12269–12291).
    - **Rule & Best Move**: In a 3-player elimination contest, the weakest player (`Larry`) should deliberately miss (`fire in the air`) in Round 1 and let the two strongest players (`Moe` and `Curly`) shoot at each other, then take the first shot against the sole survivor in Round 2.

15. **Martin Shubik's Dollar Auction & Superpower Nuclear Arms Escalation ("What Price a Dollar?")** ([book-full.txt](file:///home/masih/Work/tries/aos/book-full.txt#L12615-L12675))
    - **Quote**: `"The highest bidder gets the dollar, but both the highest and the second highest bidders pay their bids to the auctioneer... The escalation has no natural limit other than the amount of money in your wallet... was the escalation of the superpowers’ nuclear arms arsenals all that different? Both incurred costs in the trillions of dollars in quest of the 'dollar' of victory"` (l. 12619–12673).
    - **Rule & Best Move**: Never enter an all-pay/second-bidder-pays escalation auction without calculating the backward-induction budget limit first (with known `$2.50` wallets and `$0.10` steps, jump-bid immediately to **`$0.70`** to deter entry, or collude to bid **`$0.10`** and split `$0.90`).

---

## Doubts

Every place in `/home/masih/Work/tries/aos/book-full.txt` where game trees, payoff tables, diagrams, or displayed equations were embedded as images in the original book and are therefore omitted from the plain-text extraction (`table not in text`), along with whether the surrounding prose supplies the exact numbers:

1. **Chapter 2 Missing Figures / Game Trees (`table not in text`)**:
   - Lines 1316 & 1342: Robert Frost yellow-wood decision tree and Princeton-to-New York commuter decision tree (`table not in text`; prose gives qualitative paths).
   - Line 1364: Charlie Brown and Lucy football game tree (`table not in text`; prose gives ordinal preferences).
   - Line 1390: Charlie and Fredo $100,000 Freedonia investment game tree (`table not in text`; **all exact dollar payoffs (`$0/$0`, `+$150k/+$250k`, `-$100k/+$500k`) are explicitly stated in prose**).
   - Lines 1467 & 1486: Line-Item Veto preference table and two game trees (`table not in text`; **all exact rankings (`1, 2, 3, 4`) for Congress and President are stated in prose**).
   - Line 1595: *Survivor: Thailand* 21-Flags table of actual vs. winning moves (`table not in text`; prose gives the key moves `21 -> 19`, `9 -> 6 -> 4`, and the `4, 8, 12, 16, 20` rule).
2. **Chapter 3 Missing Payoff Tables (`table not in text`)**:
   - Line 2264: Rainbow's End vs. B. B. Lean 2x2 `$80` vs. `$70` payoff table (`table not in text`; **all four cell payoffs (`$72k/$72k`, `$110k/$24k`, `$24k/$110k`, `$70k/$70k`) are stated in prose**).
   - Line 2529: Exact numerical matrix of Flood and Dresher's 100-round RAND experiment is not printed in the text (prose gives the 60/100 cooperation count and rounds 83–98 streak).
   - Line 2580: Raymond Battalio's 27-student payoff table (`table not in text`; **prose gives exact endpoints `$1.08`, `$1.04/$1.54`, `$0.50`, and the linear step `+46 cents` to self / `-4 cents` to each of the other 26 students**).
3. **Chapter 4 Missing Payoff Tables and Best-Response Graphs (`table not in text`)**:
   - Lines 3228 & 3380: Fred and Barney's Stag/Bison/Rabbit payoff tables (`table not in text`; **all payoffs (`3, 3`, `1`, `0`) are stated in prose**).
   - Lines 3278, 3747, 3792, 3864, 3891, 3915: Rainbow's End vs. B. B. Lean 5x5 (`$42..$38`) payoff tables and continuous best-response graphs (`table not in text`; **prose and Workout No. 2 at l. 12998 give the exact demand formula $Q_{\text{RE}} = \max(2800 - 100 P_{\text{RE}} + 80 P_{\text{BB}}, 0)$ and unit cost `$20` [or `$11.60` in Workout No. 3], from which every cell in the 5x5 tables is uniquely determined**).
   - Line 3612: Battle of the Sexes payoff table (`table not in text`; **all payoffs (`4,3`, `3,4`, `0,0`) are in prose**).
   - Line 3666: Chicken (North vs. South rabbit hunt) payoff table (`table not in text`; **all payoffs (`0,0`, `2, 1/2`, `1/2, 2`, `1,1`) are in prose**).
4. **Chapter 5 Missing Payoff Tables and Graphs (`table not in text`)**:
   - Lines 4371, 4417, 4500, 4544, 5023, 5061, 5075: Soccer penalty kick tables and mixing graphs (`table not in text`; **all cell percentages (`58%, 95%, 93%, 70%`, `94%`, `60%`) and equilibrium mixes (`38.3%, 41.7%, 79.6%`) are in prose**).
   - Line 4586: Rock-Paper-Scissors payoff table (`table not in text`; **all payoffs (`+1, 0, -1`) are in prose**).
   - Line 4806: Battle of the Sexes mixing table (`table not in text`; **all payoffs (`4,3`, `3,4`, `0,0`, and `6,7`) are in prose**).
   - Line 5119: Janken Step Game 3x3 payoff table (`table not in text`; **all payoffs (`±5, ±2, ±1, 0`) and indifference equations are in prose**).
5. **Chapter 6 & Workout No. 4 Missing Trees and Tables (`table not in text`)**:
   - Lines 5347 & 5379: Night Self vs. Morning Self dieting game tree and 2x4 strategy table (`table not in text`; **all ordinal rankings `1..4` are in prose**).
   - Lines 5442, 5480, 5519: RE vs. BB `$80/$40` deterrence/compellence tables and summary table of Threats/Promises/Warnings/Assurances (`table not in text`; **all dollar payoffs (`$72k, $140k, $40k, $0`) are in prose**).
   - Lines 13055 & 13077: Cold War U.S.–Soviet invasion game trees in Workout No. 4 (`table not in text`; **all payoffs (`0/0`, `+100/-100`, `-500/-200`) are in prose**).
6. **Chapter 8 Missing Tables (`table not in text`)**:
   - Lines 7708 & 7721: Simplified Poker strategy table and expected payoff table (`table not in text`; **all payoffs (`±1, ±3, 0`) and equilibrium fractions (`1/3, 2/3`) are in prose**).
   - Line 7830: PITS Airline willingness-to-pay table (`table not in text`; **all numbers (`$200/$225`, `$300/$400`, costs `$100/$150`, counts `50/50`) are in prose**).
7. **Chapter 9 Missing Tipping Graphs (`table not in text`)**:
   - Lines 8070, 8115, 8221, 8256, 8281, 8351, 8445, 8505: Commuting, QWERTY/DSK, highway speeding, and residential tipping diagrams (`table not in text`; **all key thresholds (`20 + 5n` vs. `40` mins, `30%` QWERTY tipping point, `70:30` segregation tipping point) are in prose**).
8. **Chapter 10 Missing Table and Formula (`table not in text`)**:
   - Line 9651: Spectrum Auction valuation table for AT&T and Verizon (`table not in text`; **all valuations (`$10/$10/$25` for AT&T, `$9/$9/$18` for Verizon) are in prose**).
   - Lines 13163 & 13169: Two displayed equations in Workout No. 8 for the preemption duel (`table not in text`; **the adjacent lines 13166 & 13171 print the exact condition $p(t) \le 1 - q(t)$ and $q(t) \le 1 - p(t)$, i.e., $p(t) + q(t) = 1$**).
9. **Chapter 11 Missing Tables and Formulas (`table not in text`)**:
   - Lines 9846, 9885, 10261, 10294: Wage bargaining tables (`table not in text`; **every round's pie and split (`$3,000, $2,000, $1,000`, `$300/day` outside option, and `$100, $80, $50, $10`) is explicitly stated in prose**).
   - Lines 10425 & 10435: Two displayed algebraic steps in the Rubinstein Bargaining Appendix solving $L = \delta(1 - \delta(1 - L))$ (`table not in text`; implies $L = \frac{\delta}{1 + \delta}$ for the responder or $\frac{1}{1 + \delta}$ for the proposer).
10. **Chapter 12, 13, 14 Missing Figures/Tables (`table not in text`)**:
    - Lines 10945 & 10967: Triangle cake-cutting voting diagrams (`table not in text`; prose explains the 2-voter coalitions and `64%` [`2/3`] supermajority stability threshold).
    - Line 11765: Chess programmer incentive table (`table not in text`; **all numbers (`80%` vs. `60%`, `$200,000`, `$50,000` vs. `$70,000`, `$100,000` bonus) are in prose**).
    - Line 12165: Displayed formula for Campeau's blended two-tier price (`table not in text`; prose states `$105` for first `50%` and `$90` for next `50%`, giving `$97.50` at `100%`).
    - Lines 12444 & 12448: Dot grids for the $7 \times 4$ ZECK game (`table not in text`; prose describes the $7 \times 4$ rectangle and northeast removal rule).
    - Line 12546: King Solomon's Dilemma Redux sequential game tree (`table not in text`; **Moves 1–4 are written out verbatim in lines 12534–12544**).
    - Line 12764: "Arms Across the Ocean" 2x2 ordinal payoff table (`table not in text`; **prose and footnotes at l. 12767–12795 & 14290–14297 give every cell's exact rank: `(Unarmed, Unarmed) = (1, 2)`, `(Armed, Unarmed) = (2, 4)`, `(Armed, Armed) = (3, 3)`, `(Unarmed, Armed) = (4, 1)`**).
