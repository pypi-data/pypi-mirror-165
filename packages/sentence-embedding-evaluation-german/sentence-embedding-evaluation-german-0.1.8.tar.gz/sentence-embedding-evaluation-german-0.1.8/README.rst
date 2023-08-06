|PyPI version| |PyPi downloads| |Total alerts| |Language grade: Python|

sentence-embedding-evaluation-german
====================================

Sentence embedding evaluation for German.

This library is inspired by
`SentEval <https://github.com/facebookresearch/SentEval>`__ but focuses
on German language downstream tasks.

Downstream tasks
----------------

The available downstream tasks are listed in the table below. If you
that think that a dataset is missing and should be added, please `open
an
issue <https://github.com/ulf1/sentence-embedding-evaluation-german/issues/new>`__.

+--------+--------+--------+--------+--------+--------+--------+--------+
| task   | type   | text   | lang   | #train | #test  | target | info   |
|        |        | type   |        |        |        |        |        |
+========+========+========+========+========+========+========+========+
| TOXIC  | 👿     | fa     | de-DE  | 3244   | 944    | binary | Ge     |
|        | toxic  | cebook |        |        |        | {0,1}  | rmEval |
|        | co     | co     |        |        |        |        | 2021,  |
|        | mments | mments |        |        |        |        | co     |
|        |        |        |        |        |        |        | mments |
|        |        |        |        |        |        |        | s      |
|        |        |        |        |        |        |        | ubtask |
|        |        |        |        |        |        |        | 1,     |
|        |        |        |        |        |        |        | `📁    |
|        |        |        |        |        |        |        |  <htt  |
|        |        |        |        |        |        |        | ps://g |
|        |        |        |        |        |        |        | ithub. |
|        |        |        |        |        |        |        | com/ge |
|        |        |        |        |        |        |        | rmeval |
|        |        |        |        |        |        |        | 2021to |
|        |        |        |        |        |        |        | xic/Sh |
|        |        |        |        |        |        |        | aredTa |
|        |        |        |        |        |        |        | sk>`__ |
|        |        |        |        |        |        |        | `📖    |
|        |        |        |        |        |        |        |  <http |
|        |        |        |        |        |        |        | s://ac |
|        |        |        |        |        |        |        | lantho |
|        |        |        |        |        |        |        | logy.o |
|        |        |        |        |        |        |        | rg/202 |
|        |        |        |        |        |        |        | 1.germ |
|        |        |        |        |        |        |        | eval-1 |
|        |        |        |        |        |        |        | .1>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| ENGAGE | 🤗     | fa     | de-DE  | 3244   | 944    | binary | Ge     |
|        | en     | cebook |        |        |        | {0,1}  | rmEval |
|        | gaging | co     |        |        |        |        | 2021,  |
|        | co     | mments |        |        |        |        | co     |
|        | mments |        |        |        |        |        | mments |
|        |        |        |        |        |        |        | s      |
|        |        |        |        |        |        |        | ubtask |
|        |        |        |        |        |        |        | 2,     |
|        |        |        |        |        |        |        | `📁    |
|        |        |        |        |        |        |        |  <htt  |
|        |        |        |        |        |        |        | ps://g |
|        |        |        |        |        |        |        | ithub. |
|        |        |        |        |        |        |        | com/ge |
|        |        |        |        |        |        |        | rmeval |
|        |        |        |        |        |        |        | 2021to |
|        |        |        |        |        |        |        | xic/Sh |
|        |        |        |        |        |        |        | aredTa |
|        |        |        |        |        |        |        | sk>`__ |
|        |        |        |        |        |        |        | `📖    |
|        |        |        |        |        |        |        |  <http |
|        |        |        |        |        |        |        | s://ac |
|        |        |        |        |        |        |        | lantho |
|        |        |        |        |        |        |        | logy.o |
|        |        |        |        |        |        |        | rg/202 |
|        |        |        |        |        |        |        | 1.germ |
|        |        |        |        |        |        |        | eval-1 |
|        |        |        |        |        |        |        | .1>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| FCLAIM | ☝️     | fa     | de-DE  | 3244   | 944    | binary | Ge     |
|        | f      | cebook |        |        |        | {0,1}  | rmEval |
|        | act-cl | co     |        |        |        |        | 2021,  |
|        | aiming | mments |        |        |        |        | co     |
|        | co     |        |        |        |        |        | mments |
|        | mments |        |        |        |        |        | s      |
|        |        |        |        |        |        |        | ubtask |
|        |        |        |        |        |        |        | 3,     |
|        |        |        |        |        |        |        | `📁    |
|        |        |        |        |        |        |        |  <htt  |
|        |        |        |        |        |        |        | ps://g |
|        |        |        |        |        |        |        | ithub. |
|        |        |        |        |        |        |        | com/ge |
|        |        |        |        |        |        |        | rmeval |
|        |        |        |        |        |        |        | 2021to |
|        |        |        |        |        |        |        | xic/Sh |
|        |        |        |        |        |        |        | aredTa |
|        |        |        |        |        |        |        | sk>`__ |
|        |        |        |        |        |        |        | `📖    |
|        |        |        |        |        |        |        |  <http |
|        |        |        |        |        |        |        | s://ac |
|        |        |        |        |        |        |        | lantho |
|        |        |        |        |        |        |        | logy.o |
|        |        |        |        |        |        |        | rg/202 |
|        |        |        |        |        |        |        | 1.germ |
|        |        |        |        |        |        |        | eval-1 |
|        |        |        |        |        |        |        | .1>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| VMWE   | ☁️     | new    | de-DE  | 6652   | 1447   | binary | Ge     |
|        | verbal | spaper |        |        |        | (f     | rmEval |
|        | idioms |        |        |        |        | igurat | 2021,  |
|        |        |        |        |        |        | ively, | verbal |
|        |        |        |        |        |        | lite   | i      |
|        |        |        |        |        |        | rally) | dioms, |
|        |        |        |        |        |        |        | `📁    |
|        |        |        |        |        |        |        | <https |
|        |        |        |        |        |        |        | ://git |
|        |        |        |        |        |        |        | hub.co |
|        |        |        |        |        |        |        | m/rafe |
|        |        |        |        |        |        |        | hr/vid |
|        |        |        |        |        |        |        | -disam |
|        |        |        |        |        |        |        | biguat |
|        |        |        |        |        |        |        | ion-sh |
|        |        |        |        |        |        |        | aredta |
|        |        |        |        |        |        |        | sk>`__ |
|        |        |        |        |        |        |        | `      |
|        |        |        |        |        |        |        | 📖 <ht |
|        |        |        |        |        |        |        | tps:// |
|        |        |        |        |        |        |        | aclant |
|        |        |        |        |        |        |        | hology |
|        |        |        |        |        |        |        | .org/2 |
|        |        |        |        |        |        |        | 020.fi |
|        |        |        |        |        |        |        | glang- |
|        |        |        |        |        |        |        | 1.29.p |
|        |        |        |        |        |        |        | df>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| OL19-A | 👿     | tweets | de-DE  | 3980   | 3031   | binary | Ge     |
|        | off    |        |        |        |        | {0,1}  | rmEval |
|        | ensive |        |        |        |        |        | 2018,  |
|        | la     |        |        |        |        |        | `      |
|        | nguage |        |        |        |        |        | 📁 <ht |
|        |        |        |        |        |        |        | tps:// |
|        |        |        |        |        |        |        | projec |
|        |        |        |        |        |        |        | ts.fza |
|        |        |        |        |        |        |        | i.h-da |
|        |        |        |        |        |        |        | .de/ig |
|        |        |        |        |        |        |        | gsa/da |
|        |        |        |        |        |        |        | ta-201 |
|        |        |        |        |        |        |        | 9/>`__ |
|        |        |        |        |        |        |        | `📖    |
|        |        |        |        |        |        |        | <https |
|        |        |        |        |        |        |        | ://cor |
|        |        |        |        |        |        |        | pora.l |
|        |        |        |        |        |        |        | inguis |
|        |        |        |        |        |        |        | tik.un |
|        |        |        |        |        |        |        | i-erla |
|        |        |        |        |        |        |        | ngen.d |
|        |        |        |        |        |        |        | e/data |
|        |        |        |        |        |        |        | /konve |
|        |        |        |        |        |        |        | ns/pro |
|        |        |        |        |        |        |        | ceedin |
|        |        |        |        |        |        |        | gs/pap |
|        |        |        |        |        |        |        | ers/ge |
|        |        |        |        |        |        |        | rmeval |
|        |        |        |        |        |        |        | /GermE |
|        |        |        |        |        |        |        | valSha |
|        |        |        |        |        |        |        | redTas |
|        |        |        |        |        |        |        | k2019I |
|        |        |        |        |        |        |        | ggsa.p |
|        |        |        |        |        |        |        | df>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| OL19-B | 👿     | tweets | de-DE  | 3980   | 3031   | 4      | Ge     |
|        | off    |        |        |        |        | catg.  | rmEval |
|        | ensive |        |        |        |        | (prof  | 2018,  |
|        | lan    |        |        |        |        | anity, | `      |
|        | guage, |        |        |        |        | i      | 📁 <ht |
|        | fine-g |        |        |        |        | nsult, | tps:// |
|        | rained |        |        |        |        | abuse, | projec |
|        |        |        |        |        |        | oth.)  | ts.fza |
|        |        |        |        |        |        |        | i.h-da |
|        |        |        |        |        |        |        | .de/ig |
|        |        |        |        |        |        |        | gsa/da |
|        |        |        |        |        |        |        | ta-201 |
|        |        |        |        |        |        |        | 9/>`__ |
|        |        |        |        |        |        |        | `📖    |
|        |        |        |        |        |        |        | <https |
|        |        |        |        |        |        |        | ://cor |
|        |        |        |        |        |        |        | pora.l |
|        |        |        |        |        |        |        | inguis |
|        |        |        |        |        |        |        | tik.un |
|        |        |        |        |        |        |        | i-erla |
|        |        |        |        |        |        |        | ngen.d |
|        |        |        |        |        |        |        | e/data |
|        |        |        |        |        |        |        | /konve |
|        |        |        |        |        |        |        | ns/pro |
|        |        |        |        |        |        |        | ceedin |
|        |        |        |        |        |        |        | gs/pap |
|        |        |        |        |        |        |        | ers/ge |
|        |        |        |        |        |        |        | rmeval |
|        |        |        |        |        |        |        | /GermE |
|        |        |        |        |        |        |        | valSha |
|        |        |        |        |        |        |        | redTas |
|        |        |        |        |        |        |        | k2019I |
|        |        |        |        |        |        |        | ggsa.p |
|        |        |        |        |        |        |        | df>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| OL19-C | 👿     | tweets | de-DE  | 1921   | 930    | binary | Ge     |
|        | ex     |        |        |        |        | (exp   | rmEval |
|        | plicit |        |        |        |        | licit, | 2018,  |
|        | vs. im |        |        |        |        | imp    | `      |
|        | plicit |        |        |        |        | licit) | 📁 <ht |
|        | o      |        |        |        |        |        | tps:// |
|        | ffense |        |        |        |        |        | projec |
|        |        |        |        |        |        |        | ts.fza |
|        |        |        |        |        |        |        | i.h-da |
|        |        |        |        |        |        |        | .de/ig |
|        |        |        |        |        |        |        | gsa/da |
|        |        |        |        |        |        |        | ta-201 |
|        |        |        |        |        |        |        | 9/>`__ |
|        |        |        |        |        |        |        | `📖    |
|        |        |        |        |        |        |        | <https |
|        |        |        |        |        |        |        | ://cor |
|        |        |        |        |        |        |        | pora.l |
|        |        |        |        |        |        |        | inguis |
|        |        |        |        |        |        |        | tik.un |
|        |        |        |        |        |        |        | i-erla |
|        |        |        |        |        |        |        | ngen.d |
|        |        |        |        |        |        |        | e/data |
|        |        |        |        |        |        |        | /konve |
|        |        |        |        |        |        |        | ns/pro |
|        |        |        |        |        |        |        | ceedin |
|        |        |        |        |        |        |        | gs/pap |
|        |        |        |        |        |        |        | ers/ge |
|        |        |        |        |        |        |        | rmeval |
|        |        |        |        |        |        |        | /GermE |
|        |        |        |        |        |        |        | valSha |
|        |        |        |        |        |        |        | redTas |
|        |        |        |        |        |        |        | k2019I |
|        |        |        |        |        |        |        | ggsa.p |
|        |        |        |        |        |        |        | df>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| OL18-A | 👿     | tweets | de-DE  | 5009   | 3398   | binary | Ge     |
|        | off    |        |        |        |        | {0,1}  | rmEval |
|        | ensive |        |        |        |        |        | 2018,  |
|        | la     |        |        |        |        |        | `📁 <h |
|        | nguage |        |        |        |        |        | ttps:/ |
|        |        |        |        |        |        |        | /githu |
|        |        |        |        |        |        |        | b.com/ |
|        |        |        |        |        |        |        | uds-ls |
|        |        |        |        |        |        |        | v/Germ |
|        |        |        |        |        |        |        | Eval-2 |
|        |        |        |        |        |        |        | 018-Da |
|        |        |        |        |        |        |        | ta>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| OL18-B | 👿     | tweets | de-DE  | 5009   | 3398   | 4      | Ge     |
|        | off    |        |        |        |        | catg.  | rmEval |
|        | ensive |        |        |        |        | (prof  | 2018,  |
|        | lan    |        |        |        |        | anity, | `📁 <h |
|        | guage, |        |        |        |        | i      | ttps:/ |
|        | fine-g |        |        |        |        | nsult, | /githu |
|        | rained |        |        |        |        | abuse, | b.com/ |
|        |        |        |        |        |        | oth.)  | uds-ls |
|        |        |        |        |        |        |        | v/Germ |
|        |        |        |        |        |        |        | Eval-2 |
|        |        |        |        |        |        |        | 018-Da |
|        |        |        |        |        |        |        | ta>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| ABSD-1 | 🤷     | ‘De    | de-DE  | 19432  | 2555   | binary | Ge     |
|        | rel    | utsche |        |        |        |        | rmEval |
|        | evance | Bahn’  |        |        |        |        | 2017,  |
|        | cl     | cu     |        |        |        |        | `      |
|        | assifi | stomer |        |        |        |        | 📁 <ht |
|        | cation | fe     |        |        |        |        | tps:// |
|        |        | edback |        |        |        |        | sites. |
|        |        |        |        |        |        |        | google |
|        |        |        |        |        |        |        | .com/v |
|        |        |        |        |        |        |        | iew/ge |
|        |        |        |        |        |        |        | rmeval |
|        |        |        |        |        |        |        | 2017-a |
|        |        |        |        |        |        |        | bsa/da |
|        |        |        |        |        |        |        | ta>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| ABSD-2 | 😃😐😡 | ‘De    | de-DE  | 19432  | 2555   | 3      | Ge     |
|        | sen    | utsche |        |        |        | catg.  | rmEval |
|        | timent | Bahn’  |        |        |        | (pos., | 2017,  |
|        | an     | cu     |        |        |        | neg.,  | `      |
|        | alysis | stomer |        |        |        | ne     | 📁 <ht |
|        |        | fe     |        |        |        | utral) | tps:// |
|        |        | edback |        |        |        |        | sites. |
|        |        |        |        |        |        |        | google |
|        |        |        |        |        |        |        | .com/v |
|        |        |        |        |        |        |        | iew/ge |
|        |        |        |        |        |        |        | rmeval |
|        |        |        |        |        |        |        | 2017-a |
|        |        |        |        |        |        |        | bsa/da |
|        |        |        |        |        |        |        | ta>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| ABSD-3 | 🛤️     | ‘De    | de-DE  | 19432  | 2555   | 20     | Ge     |
|        | aspect | utsche |        |        |        | catg.  | rmEval |
|        | cate   | Bahn’  |        |        |        |        | 2017,  |
|        | gories | cu     |        |        |        |        | `      |
|        |        | stomer |        |        |        |        | 📁 <ht |
|        |        | fe     |        |        |        |        | tps:// |
|        |        | edback |        |        |        |        | sites. |
|        |        |        |        |        |        |        | google |
|        |        |        |        |        |        |        | .com/v |
|        |        |        |        |        |        |        | iew/ge |
|        |        |        |        |        |        |        | rmeval |
|        |        |        |        |        |        |        | 2017-a |
|        |        |        |        |        |        |        | bsa/da |
|        |        |        |        |        |        |        | ta>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| MIO-S  | 😃😐😡 | ‘Der   | de-AT  | 1799   | 1800   | 3      | One    |
|        | sen    | Sta    |        |        |        | catg.  | M      |
|        | timent | ndard’ |        |        |        |        | illion |
|        | an     | new    |        |        |        |        | Posts  |
|        | alysis | spaper |        |        |        |        | C      |
|        |        | a      |        |        |        |        | orpus, |
|        |        | rticle |        |        |        |        | `📁 <h |
|        |        | web    |        |        |        |        | ttps:/ |
|        |        | co     |        |        |        |        | /githu |
|        |        | mments |        |        |        |        | b.com/ |
|        |        |        |        |        |        |        | OFAI/m |
|        |        |        |        |        |        |        | illion |
|        |        |        |        |        |        |        | -post- |
|        |        |        |        |        |        |        | corpus |
|        |        |        |        |        |        |        | /relea |
|        |        |        |        |        |        |        | ses/ta |
|        |        |        |        |        |        |        | g/v1.0 |
|        |        |        |        |        |        |        | .0>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| MIO-O  | 🤷     | ‘Der   | de-AT  | 1799   | 1800   | binary | One    |
|        | off    | Sta    |        |        |        |        | M      |
|        | -topic | ndard’ |        |        |        |        | illion |
|        | co     | new    |        |        |        |        | Posts  |
|        | mments | spaper |        |        |        |        | C      |
|        |        | a      |        |        |        |        | orpus, |
|        |        | rticle |        |        |        |        | `📁 <h |
|        |        | web    |        |        |        |        | ttps:/ |
|        |        | co     |        |        |        |        | /githu |
|        |        | mments |        |        |        |        | b.com/ |
|        |        |        |        |        |        |        | OFAI/m |
|        |        |        |        |        |        |        | illion |
|        |        |        |        |        |        |        | -post- |
|        |        |        |        |        |        |        | corpus |
|        |        |        |        |        |        |        | /relea |
|        |        |        |        |        |        |        | ses/ta |
|        |        |        |        |        |        |        | g/v1.0 |
|        |        |        |        |        |        |        | .0>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| MIO-I  | 👿     | ‘Der   | de-AT  | 1799   | 1800   | binary | One    |
|        | i      | Sta    |        |        |        |        | M      |
|        | nappro | ndard’ |        |        |        |        | illion |
|        | priate | new    |        |        |        |        | Posts  |
|        | co     | spaper |        |        |        |        | C      |
|        | mments | a      |        |        |        |        | orpus, |
|        |        | rticle |        |        |        |        | `📁 <h |
|        |        | web    |        |        |        |        | ttps:/ |
|        |        | co     |        |        |        |        | /githu |
|        |        | mments |        |        |        |        | b.com/ |
|        |        |        |        |        |        |        | OFAI/m |
|        |        |        |        |        |        |        | illion |
|        |        |        |        |        |        |        | -post- |
|        |        |        |        |        |        |        | corpus |
|        |        |        |        |        |        |        | /relea |
|        |        |        |        |        |        |        | ses/ta |
|        |        |        |        |        |        |        | g/v1.0 |
|        |        |        |        |        |        |        | .0>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| MIO-D  | 👿     | ‘Der   | de-AT  | 1799   | 1800   | binary | One    |
|        | di     | Sta    |        |        |        |        | M      |
|        | scrimi | ndard’ |        |        |        |        | illion |
|        | nating | new    |        |        |        |        | Posts  |
|        | co     | spaper |        |        |        |        | C      |
|        | mments | a      |        |        |        |        | orpus, |
|        |        | rticle |        |        |        |        | `📁 <h |
|        |        | web    |        |        |        |        | ttps:/ |
|        |        | co     |        |        |        |        | /githu |
|        |        | mments |        |        |        |        | b.com/ |
|        |        |        |        |        |        |        | OFAI/m |
|        |        |        |        |        |        |        | illion |
|        |        |        |        |        |        |        | -post- |
|        |        |        |        |        |        |        | corpus |
|        |        |        |        |        |        |        | /relea |
|        |        |        |        |        |        |        | ses/ta |
|        |        |        |        |        |        |        | g/v1.0 |
|        |        |        |        |        |        |        | .0>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| MIO-F  | 💡     | ‘Der   | de-AT  | 3019   | 3019   | binary | One    |
|        | fe     | Sta    |        |        |        |        | M      |
|        | edback | ndard’ |        |        |        |        | illion |
|        | co     | new    |        |        |        |        | Posts  |
|        | mments | spaper |        |        |        |        | C      |
|        |        | a      |        |        |        |        | orpus, |
|        |        | rticle |        |        |        |        | `📁 <h |
|        |        | web    |        |        |        |        | ttps:/ |
|        |        | co     |        |        |        |        | /githu |
|        |        | mments |        |        |        |        | b.com/ |
|        |        |        |        |        |        |        | OFAI/m |
|        |        |        |        |        |        |        | illion |
|        |        |        |        |        |        |        | -post- |
|        |        |        |        |        |        |        | corpus |
|        |        |        |        |        |        |        | /relea |
|        |        |        |        |        |        |        | ses/ta |
|        |        |        |        |        |        |        | g/v1.0 |
|        |        |        |        |        |        |        | .0>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| MIO-P  | ✉️     | ‘Der   | de-AT  | 4668   | 4668   | binary | One    |
|        | pe     | Sta    |        |        |        |        | M      |
|        | rsonal | ndard’ |        |        |        |        | illion |
|        | story  | new    |        |        |        |        | Posts  |
|        | co     | spaper |        |        |        |        | C      |
|        | mments | a      |        |        |        |        | orpus, |
|        |        | rticle |        |        |        |        | `📁 <h |
|        |        | web    |        |        |        |        | ttps:/ |
|        |        | co     |        |        |        |        | /githu |
|        |        | mments |        |        |        |        | b.com/ |
|        |        |        |        |        |        |        | OFAI/m |
|        |        |        |        |        |        |        | illion |
|        |        |        |        |        |        |        | -post- |
|        |        |        |        |        |        |        | corpus |
|        |        |        |        |        |        |        | /relea |
|        |        |        |        |        |        |        | ses/ta |
|        |        |        |        |        |        |        | g/v1.0 |
|        |        |        |        |        |        |        | .0>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| MIO-A  | ✴️     | ‘Der   | de-AT  | 1799   | 1800   | binary | One    |
|        | a      | Sta    |        |        |        |        | M      |
|        | rgumen | ndard’ |        |        |        |        | illion |
|        | tative | new    |        |        |        |        | Posts  |
|        | co     | spaper |        |        |        |        | C      |
|        | mments | a      |        |        |        |        | orpus, |
|        |        | rticle |        |        |        |        | `📁 <h |
|        |        | web    |        |        |        |        | ttps:/ |
|        |        | co     |        |        |        |        | /githu |
|        |        | mments |        |        |        |        | b.com/ |
|        |        |        |        |        |        |        | OFAI/m |
|        |        |        |        |        |        |        | illion |
|        |        |        |        |        |        |        | -post- |
|        |        |        |        |        |        |        | corpus |
|        |        |        |        |        |        |        | /relea |
|        |        |        |        |        |        |        | ses/ta |
|        |        |        |        |        |        |        | g/v1.0 |
|        |        |        |        |        |        |        | .0>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| SBCH-S | 😃😐😡 | ‘chat  | gsw    | 394    | 394    | 3      | SB-CH  |
|        | sen    | mania’ |        |        |        | catg.  | C      |
|        | timent | app    |        |        |        |        | orpus, |
|        | an     | com    |        |        |        |        | `📁 <  |
|        | alysis | ments, |        |        |        |        | https: |
|        |        | only   |        |        |        |        | //gith |
|        |        | co     |        |        |        |        | ub.com |
|        |        | mments |        |        |        |        | /spinn |
|        |        | la     |        |        |        |        | ingbyt |
|        |        | belled |        |        |        |        | es/SB- |
|        |        | as     |        |        |        |        | CH>`__ |
|        |        | Swiss  |        |        |        |        |        |
|        |        | German |        |        |        |        |        |
|        |        | are    |        |        |        |        |        |
|        |        | in     |        |        |        |        |        |
|        |        | cluded |        |        |        |        |        |
+--------+--------+--------+--------+--------+--------+--------+--------+
| SBCH-L | ⛰️     | ‘chat  | gsw    | 748    | 748    | binary | SB-CH  |
|        | d      | mania’ |        |        |        |        | C      |
|        | ialect | app    |        |        |        |        | orpus, |
|        | cl     | co     |        |        |        |        | `📁 <  |
|        | assifi | mments |        |        |        |        | https: |
|        | cation |        |        |        |        |        | //gith |
|        |        |        |        |        |        |        | ub.com |
|        |        |        |        |        |        |        | /spinn |
|        |        |        |        |        |        |        | ingbyt |
|        |        |        |        |        |        |        | es/SB- |
|        |        |        |        |        |        |        | CH>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| ARCHI  | ⛰️     | Audio  | gsw    | 18809  | 4743   | 4      | Arc    |
|        | d      | tr     |        |        |        | catg.  | hiMob, |
|        | ialect | anscri |        |        |        |        | `📁    |
|        | cl     | ptions |        |        |        |        |  <htt  |
|        | assifi | of     |        |        |        |        | ps://w |
|        | cation | inte   |        |        |        |        | ww.spu |
|        |        | rviews |        |        |        |        | r.uzh. |
|        |        | in     |        |        |        |        | ch/en/ |
|        |        | four   |        |        |        |        | depart |
|        |        | d      |        |        |        |        | ments/ |
|        |        | ialect |        |        |        |        | resear |
|        |        | r      |        |        |        |        | ch/tex |
|        |        | egions |        |        |        |        | tgroup |
|        |        | of     |        |        |        |        | /Archi |
|        |        | Switz  |        |        |        |        | Mob.ht |
|        |        | erland |        |        |        |        | ml>`__ |
|        |        |        |        |        |        |        | `📖 <h |
|        |        |        |        |        |        |        | ttps:/ |
|        |        |        |        |        |        |        | /aclan |
|        |        |        |        |        |        |        | tholog |
|        |        |        |        |        |        |        | y.org/ |
|        |        |        |        |        |        |        | L16-16 |
|        |        |        |        |        |        |        | 41>`__ |
+--------+--------+--------+--------+--------+--------+--------+--------+
| LSDC   | 🌊     | s      | nds    | 74140  | 8602   | 14     | Lower  |
|        | d      | everal |        |        |        | catg.  | Saxon  |
|        | ialect | genres |        |        |        |        | D      |
|        | cl     | (e.g.  |        |        |        |        | ialect |
|        | assifi | formal |        |        |        |        | Cla    |
|        | cation | texts, |        |        |        |        | ssific |
|        |        | fairy  |        |        |        |        | ation, |
|        |        | tales, |        |        |        |        | `📁    |
|        |        | n      |        |        |        |        |  <http |
|        |        | ovels, |        |        |        |        | s://gi |
|        |        | p      |        |        |        |        | thub.c |
|        |        | oetry, |        |        |        |        | om/Hel |
|        |        | t      |        |        |        |        | sinki- |
|        |        | heatre |        |        |        |        | NLP/LS |
|        |        | plays) |        |        |        |        | DC>`__ |
|        |        | from   |        |        |        |        | `📖    |
|        |        | the    |        |        |        |        | <https |
|        |        | 19th   |        |        |        |        | ://www |
|        |        | to     |        |        |        |        | .aclwe |
|        |        | 21st   |        |        |        |        | b.org/ |
|        |        | cent   |        |        |        |        | anthol |
|        |        | uries. |        |        |        |        | ogy/20 |
|        |        | Ext    |        |        |        |        | 20.var |
|        |        | incted |        |        |        |        | dial-1 |
|        |        | Lower  |        |        |        |        | .3>`__ |
|        |        | P      |        |        |        |        |        |
|        |        | russia |        |        |        |        |        |
|        |        | exc    |        |        |        |        |        |
|        |        | luded. |        |        |        |        |        |
|        |        | Gr     |        |        |        |        |        |
|        |        | onings |        |        |        |        |        |
|        |        | ex     |        |        |        |        |        |
|        |        | cluded |        |        |        |        |        |
|        |        | due to |        |        |        |        |        |
|        |        | lack   |        |        |        |        |        |
|        |        | of     |        |        |        |        |        |
|        |        | test   |        |        |        |        |        |
|        |        | exa    |        |        |        |        |        |
|        |        | mples. |        |        |        |        |        |
+--------+--------+--------+--------+--------+--------+--------+--------+

Download datasets
-----------------

.. code:: sh

   bash download-datasets.sh

Usage example
-------------

Import the required Python packages.

.. code:: py

   from typing import List
   import sentence_embedding_evaluation_german as seeg
   import torch

Step (1) Load your pretrained model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the following example, we generate a random embedding matrix for
demonstration purposes.

.. code:: py

   # (1) Instantiate an embedding model
   emb_dim = 512
   vocab_sz = 128
   emb = torch.randn((vocab_sz, emb_dim), requires_grad=False)
   emb = torch.nn.Embedding.from_pretrained(emb)
   assert emb.weight.requires_grad == False

Step (2) Specify your ``preprocessor`` function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need to specify your own preprocessing routine. The ``preprocessor``
function must convert a list of strings ``batch`` (``List[str]``) into a
list of feature vectors, or resp. a list of sentence embeddings
(``List[List[float]]``). In the following example, we generate some sort
of token IDs, retrieve the vectors from our random matrix, and average
these to feature vectors for demonstration purposes.

.. code:: py

   # (2) Specify the preprocessing
   def preprocesser(batch: List[str], params: dict=None) -> List[List[float]]:
       """ Specify your embedding or pretrained encoder here
       Paramters:
       ----------
       batch : List[str]
           A list of sentence as string
       params : dict
           The params dictionary
       Returns:
       --------
       List[List[float]]
           A list of embedding vectors
       """
       features = []
       for sent in batch:
           try:
               ids = torch.tensor([ord(c) % 128 for c in sent])
           except:
               print(sent)
           h = emb(ids)
           features.append(h.mean(axis=0))
       features = torch.stack(features, dim=0)
       return features

Step (3) Training settings
~~~~~~~~~~~~~~~~~~~~~~~~~~

We suggest to train a final layer with bias term (``'bias':True``), on a
loss function weighted by the class frequency (``'balanced':True``), a
batch size of 128, an over 500 epochs without early stopping.

.. code:: py

   # (3) Training settings
   params = {
       'datafolder': './datasets',
       'bias': True,
       'balanced': True,
       'batch_size': 128, 
       'num_epochs': 500,
       # 'early_stopping': True,
       # 'split_ratio': 0.2,  # if early_stopping=True
       # 'patience': 5,  # if early_stopping=True
   }

Step (4) Downstream tasks
~~~~~~~~~~~~~~~~~~~~~~~~~

We suggest to run the following downstream tasks. ``FCLAIM`` flags
comments that requires manual fact-checking because these contain
reasoning, arguments or claims that might be false. ``VMWE``
differentiates texts with figurative or literal multi-word expressions.
``OL19-C`` distincts between explicit and implicit offensive language.
``ABSD-2`` is a sentiment analysis dataset with customer reviews. These
four dataset so far can be assumed to be Standard German from Germany
(de-DE). ``MIO-P`` flags Austrian German (de-AT) comments if these
contain personal stories. ``ARCHI`` is a Swiss (gsw), and ``LSDC`` a
Lower German (nds) dialect identification task.

.. code:: py

   # (4) Specify downstream tasks
   downstream_tasks = ['FCLAIM', 'VMWE', 'OL19-C', 'ABSD-2', 'MIO-P', 'ARCHI', 'LSDC']

Step (5) Run the experiments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, start the evaluation. The suggested downstream tasks (step 4)
with 500 epochs (step 3) might requires 10-40 minutes but it’s highly
dependent on your computing resources. So grab a ☕ or 🍵.

.. code:: py

   # (5) Run experiments
   results = seeg.evaluate(downstream_tasks, preprocesser, **params)

Demo notebooks
--------------

Start Jupyter

.. code:: sh

   source .venv/bin/activate
   jupyter lab

Open an demo notebook

-  `Generic demo <demo/Jupyter%20Demo.ipynb>`__
-  `deepset example <demo/deepset%20example.ipynb>`__
-  `fasttext example <demo/fastText%20example.ipynb>`__
-  `SBert example <demo/SBert%20example.ipynb>`__

Appendix
--------

Installation & Downloads
~~~~~~~~~~~~~~~~~~~~~~~~

The ``sentence-embedding-evaluation-german`` `git
repo <http://github.com/ulf1/sentence-embedding-evaluation-german>`__ is
available as `PyPi
package <https://pypi.org/project/sentence-embedding-evaluation-german>`__

.. code:: sh

   pip install sentence-embedding-evaluation-german
   pip install git+ssh://git@github.com/ulf1/sentence-embedding-evaluation-german.git

You need to download the datasets as well. If you run the following
code, the datasets should be in a folder ``./datasets``.

.. code:: sh

   wget -q "https://raw.githubusercontent.com/ulf1/sentence-embedding-evaluation-german/main/download-datasets.sh" -O download-datasets.sh 
   bash download-datasets.sh

Development work for this package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install a virtual environment

.. code:: sh

   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt --no-cache-dir
   pip install -r requirements-dev.txt --no-cache-dir
   pip install -r requirements-demo.txt --no-cache-dir

(If your git repo is stored in a folder with whitespaces, then don’t use
the subfolder ``.venv``. Use an absolute path without whitespaces.)

Python commands

-  Jupyter for the examples: ``jupyter lab``
-  Check syntax:
   ``flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')``

Publish package

.. code:: sh

   pandoc README.md --from markdown --to rst -s -o README.rst
   python setup.py sdist 
   twine upload -r pypi dist/*

Clean up

.. code:: sh

   find . -type f -name "*.pyc" | xargs rm
   find . -type d -name "__pycache__" | xargs rm -r
   rm -r .pytest_cache
   rm -r .venv

New Dataset recommendation
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to recommend another or a new dataset, please `open an
issue <https://github.com/ulf1/sentence-embedding-evaluation-german/issues/new>`__.

Troubleshooting
~~~~~~~~~~~~~~~

If you have troubles to get this package running, please `open an
issue <https://github.com/ulf1/sentence-embedding-evaluation-german/issues/new>`__
for support.

Contributing
~~~~~~~~~~~~

Please contribute using `Github
Flow <https://guides.github.com/introduction/flow/>`__. Create a branch,
add commits, and `open a pull
request <https://github.com/ulf1/sentence-embedding-evaluation-german/compare/>`__.

Citation
~~~~~~~~

If you want to use this package in a research paper, please `open an
issue <https://github.com/ulf1/sentence-embedding-evaluation-german/issues/new>`__
because we have not yet decided how to make this package citable. You
should at least mention the PyPi version in your paper to ensure
reproducibility.

You certainly need to cite the actual evaluation datasets in your paper.
Please check the hyperlinks in the info column of the `table
above <#downstream-tasks>`__.

.. |PyPI version| image:: https://badge.fury.io/py/sentence-embedding-evaluation-german.svg
   :target: https://badge.fury.io/py/sentence-embedding-evaluation-german
.. |PyPi downloads| image:: https://img.shields.io/pypi/dm/sentence-embedding-evaluation-german
   :target: https://img.shields.io/pypi/dm/sentence-embedding-evaluation-german
.. |Total alerts| image:: https://img.shields.io/lgtm/alerts/g/ulf1/sentence-embedding-evaluation-german.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/sentence-embedding-evaluation-german/alerts/
.. |Language grade: Python| image:: https://img.shields.io/lgtm/grade/python/g/ulf1/sentence-embedding-evaluation-german.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/sentence-embedding-evaluation-german/context:python
