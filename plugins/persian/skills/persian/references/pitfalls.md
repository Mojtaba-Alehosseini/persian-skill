# pitfalls.md — Persian translation rules

> What machine-Persian gets wrong, and the idiomatic fix. ✗ = avoid, ✓ = use.
> P-numbers are **stable IDs** referenced elsewhere in the skill — never renumber or reuse them.
> 56 rules total; IDs run P1–P58 because **P27 and P30 were retired** (the gaps are intentional, not missing content).
>
> **Two parts:** the rule catalog (P1–P58) below, then **§ Worked exemplars** — aligned EN↔FA
> sentences cross-linked to the P-rules — at the very end.

## P1 · English it-clefts → plain Persian sentence
English "it was X that Y" / "it's X my fingers are curled around" must NOT be calqued
with «این … است که …». Persian prefers a plain S-O-V clause.
- EN: *it's Rahim Khan's pinky my fingers are curled around*
- ✗ این انگشتِ کوچکِ رحیم‌خان است که انگشتانم دورش حلقه شده
- ✓ دستم انگشتِ کوچکِ رحیم‌خان را گرفته بود

## P2 · Drop redundant / implied words
Persian routinely omits what English states explicitly when context carries it.
- EN: *my parents' wedding night* → ✓ عروسیِ پدر و مادرم  (the «شب / night» is usually dropped)
- Claude tends to translate every word ("شبِ عروسی") — often over-literal.

## P3 · Prefer a predicate verb over a bare adjective string
- EN: *looking tired and grim*
- ✗ خسته و عبوس
- ✓ خسته و گرفته به نظر می‌رسید

## P4 · Collocation-aware word choice
- business partner → ✓ شریکِ تجاری   (not شریکِ کاری)
- grim (this context) → ✓ گرفته   (not عبوس)

## P5 · Re-segment sentences to Persian rhythm
Don't preserve English dashes / clause order.  folded "I'm in his arms" into
the previous clause («در بغل بابا») and broke the pinky image into its own short
sentence. Persian narration favors shorter, re-segmented clauses over one long English period.

## P6 · Verb-final information order (don't mimic English fronting)
English "Upstairs was my bedroom…" fronts the location. Persian puts the subject first
and the locative + copula LAST.
- ✗ طبقهٔ بالا اتاقِ خوابِ من … قرار داشت
- ✓ اتاقِ خواب من … در طبقهٔ بالا بود

## P7 · Established Persian term over calque
- "the smoking room" → ✓ اتاقِ دخانیات   (not اتاقِ سیگار)
- "business" (as a topic of conversation) → ✓ کسب‌وکار   (not تجارت)

## P8 · Casual dialogue → idiomatic colloquial Persian (register)
Flat, literal dialogue is the #1 tell of machine Persian. Match the speaker's tone.
- EN: "Go on, now," he'd say.
- ✗ «برو دیگر، حالا»
- ✓ «بزن بچاک. فوراً.»

## P9 · Restructure "ask if I could X" → «اجازه خواستن که …»
- EN: Sometimes I asked Baba if I could sit with them
- ✗ گاهی از بابا می‌پرسیدم می‌توانم پیششان بنشینم یا نه
- ✓ گاهی از بابا می‌خواستم اجازه بدهد من هم بروم پیششان

## P10 · Reflexive «خود» for "their/his own" where it reads cleaner
- their pipes / their favorite topics → ✓ پیپ‌های خود / موضوعِ دلخواهِ خود  (often better than ‌پیپ‌هایشان)

---

## P11 · "had just X when Y" (past-perfect + when) → simultaneity frame, often nominalized
English's "X had just happened when Y" should not be calqued as «تازه X بود که Y». Persian
prefers a simultaneity frame, often nominalizing X ("the sound of the beep").
- EN: The microwave had just beeped when the lights went out
- ✗ مایکروفر تازه بوق زده بود که چراغ‌ها خاموش شد
- ✓ همزمان با صدای بوقِ مایکروفر، برق رفت

## P12 · Natural collocations for everyday events
- "the lights went out" → ✓ برق رفت   (not چراغ‌ها خاموش شد)
- "the music disappeared/stopped" → ✓ موسیقی قطع شد   (not موسیقی ناپدید شد)

## P13 · Stock exclamations & suggestion frames — use the Persian idiom, don't calque
- "Perfect timing" → ✓ چه به‌موقع!   (not «زمان‌بندی عالی»)
- "How about [doing X]?" (a suggestion) → ✓ موافقی…؟ / چطوره…؟   (not «نظرت چیست که…»)
- "tell each other" → ✓ به هم بگوییم   (not «به یکدیگر/به دیگری بگوییم»)

## P14 · Collapse English relative clauses into Persian nominalization
English "...at a hall where a group of poets were giving a recital" → Persian compresses the
"where ... were ...ing" clause into a noun phrase («هنگام شعرخوانیِ …»).
- ✗ …در تالاری که گروهی از شاعران بنگالی در حال شعرخوانی بودند
- ✓ …در سالن کنفرانسی هنگام شعرخوانیِ تعدادی از شاعران بنگالی

## P15 · English -ing participles → Persian coordinate finite verbs
"ran the water, **soaking** the knife" / "…to the coffeepot, **pouring** out…". Don't calque with «در حالِ …».
- ✗ آب را باز کرد، در حالی که چاقو را خیس می‌کرد
- ✓ شیر را باز کرد و چاقو را در آب گذاشت

## P16 · Drop light head-nouns; name the character in close POV
- "a **trick** he'd learned" → ✓ این را … یاد گرفته بود   (drop «ترفند»)
- when English "his/her" clearly points to a named character, Persian may make it explicit with the **name** for clarity — «اسمِ شوکمار» over bare «اسمش». (NB: شوکمار = the name *Shukumar*, شُبا = *Shoba* — names, not pronouns.)

## P17 · Domain/culinary vocabulary — use the real Persian term
- "ribbons of fat" (from lamb) → ✓ باریکه‌ی دنبه   (NOT «روبان‌های چربی»)
- "rubbed/sliced a lemon" → ✓ لیمو را قاچ کرد و مالید

## P18 · Render by sense when the literal is flat (use sparingly)
- "But it wasn't a consolation." → ✓ اما این فکرها دیگر فایده‌ای نداشت   (functional, not literal «تسلی»)
- Caveat: a translator's interpretive liberty — prefer fidelity unless the literal reads dead.

## P19 · Localize units & measurements
- "three feet" of snow → ✓ یک متر   (convert imperial → metric for Persian readers)

## P20 · Flatten varied English dialogue tags
- suggested / conceded / announced / recalled → usually ✓ گفت   (specify the manner only when it matters)

## P21 · Spoken-register immediate intention: «… رفتم»
- "I'm going to shower" (leaving right now) → ✓ من رفتم دوش بگیرم   (past form carries immediate intention)
- also: compress redundant dialogue tails ("…before the lights go", "I'll be down")

## P22 · "treat X (inanimate) as if" → recast to manner; don't calque
- ✗ با خانه طوری رفتار می‌کرد که انگار هتل است
- ✓ رفتارش در خانه طوری بود که انگار در هتل زندگی می‌کند

## P23 · Cultural localization — domesticate, but with care
- place names: "Haymarket" → «بازار» (+ footnote); produce: artichokes → «کنگر», plums → «آلوچه»
- ⚠ don't lose needed specificity (yams → «سیب‌زمینی» loses it) — footnote or keep the term when it matters

## P24 · The gold is NOT infallible — verify named entities, geography & numbers vs. source
A QA meta-rule for the skill: even master translations slip. Always re-check proper nouns,
places, and numbers against the English — never inherit the gold's errors.
- observed: "the Charles" (a river) → «خیابان چارلز» (a street); "missing teeth" → «دندان… درنیامده»

## P25 · Add affective particles where Persian colors emotion
- "It must have been so hot" (the baby) → ✓ فکر می‌کنم طفلکی … داشت می‌سوخت   (add «طفلکی/بیچاره»; epistemic "must have" → «فکر می‌کنم/حتماً»)

## P26 · English indirect speech → Persian direct quotation
- "She thanked him." → ✓ گفت: «متشکرم!»

## P28 · Colloquial speech markers (casual dialogue register)
- «یارو» = "the guy"; intensifier «حسابی» ("knew it well" → «حسابی بلد بود»)
- frame «از آن …هایی که» = "one of those … who"; casual loanwords ok in speech («کپی کردن»)

## P29 · High/emotional register: dignified and clear, not ornate
- keep «که» relative clauses when they flow (don't mechanically nominalize); front the cause «به خاطر…»
- prefer «گریه کردند» over the bookish «گریستند»

## P31 · English zeugma → split into parallel concrete Persian phrases
"bearing confections in his pocket and hopes … of his family" — one English verb can't carry a
concrete + an abstract object in Persian. Split and give each a home.
- ✓ «در جیبش شکلات و شیرینی داشت و در قلبش آرزوی شنیدن خبری از خانواده‌اش»

## P32 · English agentless passive → Persian impersonal ACTIVE (3rd-plural) ⭐
Persian strongly prefers active. Render "X was done" with an unspecified «…ـند», not «… شد».
- "Teachers were dragged… and shot" → ✓ «معلم‌ها را … کشاندند و … کشتند»  (NOT «کشته شدند»)
- one of the most frequent machine-Persian tells — check every passive.

## P33 · Explicitate unfamiliar foreign concepts (institutions, education, objects)
Spell out foreign concepts for the Persian reader instead of transliterating.
- "comic books" → «کتاب‌های (طنز) مصور» (not «کمیک‌بوک»)
- "graduate dormitory" → «خوابگاه دانشجویان فوق‌لیسانس و دکترا»
- often pairs with recasting: "didn't own a stove" → «شرایط پختن غذا فراهم نبود»

## P34 · Dialogue: front the action-beat + attribution before the quote
English: "…," he said, brushing salt from his beard. → Persian often leads with it.
- ✓ «پدرم همان‌طور که … پاک می‌کرد، گفت: «…»»

## P35 · «چرا» affirms a NEGATIVE question ⭐
"Isn't X…?" answered in the affirmative → «چرا» (not «بله»).
- "Isn't 1947 the independence date?" → «مگر … نیست؟» → ✓ «چرا، هست.»
- a uniquely Persian Q&A move the model routinely gets wrong.

## P36 · Merge English "but X. Therefore Y." into one causal Persian clause
- "…Bengali, but he is a Muslim. Therefore he lives in East Pakistan" → ✓ «یک بنگالی است؛ ولی چون مسلمان است، در شرق پاکستان زندگی می‌کند»
- related: name symbols/gestures — "drawing an X" → «ضرب‌در کشید» (the × sign)

---

## P37 · Anchor a floating English possessive idiom to a concrete noun
- "ten dollars **to my name**" → «حسابی بانکی معادل ده دلار» (not «ده دلار پول»)

## P38 · Re-architect long periodic sentences around their endpoint
- front the goal «برای رسیدن به انگلیس…»; background secondary clauses with «در حالی که…»

## P39 · Add an implied motion/gathering verb to make a tableau physical
- "ate on a table" → «دورِ میز حلقه می‌زدیم و با دست می‌خوردیم»

## P40 · "establish ourselves / make it" → ambition idiom «به جایی رسیدن»  (not «خود را تثبیت کردن»)

## P41 · Unpack phrasal verbs into physical components
- "moved out" → «اثاثش را جمع می‌کرد و می‌رفت»

## P42 · Life-events: "my turn came" → «نوبت به من رسید»; age via «…سالگی»

## P43 · "I was honored / it was an honor" (stative) → objective property of the thing
- → «کار… اعتبارآفرین بود»

## P44 · "on a budget" → a behavior clause «حواسم بود چقدر خرج می‌کنم»

## P45 · Unpack cultural metonyms to their referent
- "an English cup of tea" (= gentility) → «آداب و رسومِ انگلیسی»

## P46 · Replace a bare colon/juxtaposition with an explicit causal link
- "a holiday: men had landed on the moon" → «به افتخارِ…»

## P47 · Inanimate "contain/have" + list → split by real relation, animate verbs
- a wall cross gets its own sentence «… نصب شده بود»

## P48 · Reported notice → verbatim signboard text (quoted)
- "a sign said cooking was forbidden" → «تابلوی «آشپزی اکیداً ممنوع!»»

## P49 · Sensory adjective → impact verb
- "horns, shrill and prolonged" → «بوقِ ممتد… گوشِ آدم را می‌خراشید»

## P50 · Abstract subject → concrete sense-data
- "sirens heralded endless emergencies" → «صدای آژیر و نورِ چراغ‌گردان… تمامی نداشت»

## P51 · Keep rhetorical anaphora when it IS the point; localize each tail
- "no…no…no…" → «نه…و نه…» with each idiom localized

## P52 · "X was new to me" → «X برایم تازگی داشت»

## P53 · Weld "her voice was [manner]" into the speech-verb; use the Persian phone idiom
- "Who is speaking?" → «بله، شما؟»; "voice bold/clamorous" → «با صدای خشک جیغ کشید»

## P54 · Assign politeness/T-V (تو vs شما) by the social dynamic, not the phrase's dictionary register
- brusque landlady → clipped «بله؟» + «تو»

## P55 · Manner adverb on a dialogue tag → reason-phrase adjunct
- "adding tentatively" → «محضِ احتیاط اضافه کردم» (not «با تردید»)

---

## P56 · Reported gossip stays present-perfect «…شده است» (live-news feel), not past «بود»
- "her husband had fallen in love" → «عاشق زن دیگری شده است»

## P57 · English concessive "Not that I X" → plain Persian negative
- → «من سرزنشش نمی‌کنم» (not «نه اینکه سرزنشش کنم»)

## P58 · Address term / endearment fronts service-talk
In Persian service/dialogue, the endearment leads and the offer follows — don't bury «عزیزم/جانم» mid-sentence.
- "What can I get you, honey?" → ✓ «عزیزم، چی برات بیارم؟»   (formal: «عزیزم، چه میل دارید؟»)
- ✗ «چه چیزی می‌توانم برایتان بیاورم، عزیزم؟»  (calques English word order, flat register)

---

# Worked exemplars (aligned EN↔FA)

> Full worked examples of idiomatic EN→FA. Use alongside the rules above; P-numbers point to the rule.

**1.**
EN: There was a picture of my parents' wedding night, Baba dashing in his black suit and my mother a smiling young princess in white.
FA: عکسی از عروسیِ پدر و مادرم هم بود. بابا با کت و شلوار مشکی، و مادرم شاهزاده‌خانمِ جوان، لبخند بر لبی، با لباسی سفید.
note: "wedding night" → «عروسی»; "dashing" dropped; "smiling … in white" → «لبخند بر لبی، با لباسی سفید».

**2.**
EN: Here was Baba and his best friend and business partner, Rahim Khan, standing outside our house, neither one smiling—I am a baby in that photograph and Baba is holding me, looking tired and grim.
FA: در یکی از عکس‌ها بابا در کنار بهترین دوست و شریکِ تجاری‌اش، رحیم خان، جلو خانه ایستاده بودند و هیچ‌کدام لبخند نمی‌زدند؛ من توی عکس بچه بودم و در بغل بابا، بابا خسته و گرفته به نظر می‌رسید.
note: "business partner" → «شریکِ تجاری»; "grim" → «گرفته»; clause boundaries re-segmented (P5).

**3.**
EN: I'm in his arms, but it's Rahim Khan's pinky my fingers are curled around.
FA: … دستم انگشتِ کوچکِ رحیم خان را گرفته بود.
note: it-cleft flattened to plain S-O-V (P1); "pinky" → «انگشتِ کوچک».

**4.**
EN: Upstairs was my bedroom, Baba's room, and his study, also known as "the smoking room," which perpetually smelled of tobacco and cinnamon.
FA: اتاقِ خوابِ من و بابا و اتاقِ کارش که به آن «اتاقِ دخانیات» هم می‌گفتند و مدام بوی تنباکو و دارچین می‌داد، در طبقه‌ی بالا بود.
note: location + copula moved to the end (P6); "smoking room" → «دخانیات» (P7); "perpetually" → «مدام».

**5.**
EN: They stuffed their pipes—except Baba always called it "fattening the pipe"—and discussed their favorite three topics: politics, business, soccer.
FA: پیپ‌های خود را پر می‌کردند ـ بابا به این می‌گفت «هموار کردنِ پیپ» ـ و از سه موضوعِ دلخواهِ خود، سیاست، کسب‌وکار و فوتبال حرف می‌زدند.
note: reflexive «خود» for "their" (P10); "business" → «کسب‌وکار» (P7).

**6.**
EN: "Go on, now," he'd say. "This is grown-ups' time. Why don't you go read one of those books of yours?"
FA: … می‌گفت: «بزن بِچاک. فوراً. حالا وقتِ بزرگ‌ترهاست. چرا نمی‌روی یکی از کتاب‌هایت را بخوانی؟»
note: casual register — "Go on, now" → «بزن بِچاک. فوراً.» (P8).

**7.**
EN: The microwave had just beeped when the lights went out, and the music disappeared.
FA: همزمان با صدای بوقِ مایکروفر، برق هم رفت و موسیقی قطع شد.
note: "had just X when Y" → simultaneity frame (P11); "the lights went out" → «برق رفت» (P12).

**8.**
EN: "Perfect timing," Shoba said.
FA: شُبا گفت: «چه به‌موقع!»
note: stock exclamation, not a calque (P13).

**9.**
EN: "How about telling each other something we've never told before."
FA: «موافقی هر کدام یک چیزی بگوییم که تا حالا به هم نگفته‌ایم؟»
note: suggestion frame "how about…?" → «موافقی…؟» (P13).

**10.**
EN: He thought back to their first meeting, four years earlier at a lecture hall in Cambridge, where a group of Bengali poets were giving a recital.
FA: به اولین برخوردشان فکر کرد؛ چهار سال پیش در سالن کنفرانسی در کمبریج هنگامِ شعرخوانیِ تعدادی از شاعران بنگالی.
note: relative clause "where … were giving a recital" compressed to a noun phrase (P14).
