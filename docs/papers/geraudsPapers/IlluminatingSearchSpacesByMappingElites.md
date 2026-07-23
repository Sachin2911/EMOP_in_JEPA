# IlluminatingSearchSpacesByMappingElites



---

## Page 1

Illuminating search spaces by mapping elites
Jean-BaptisteMouret1 andJeffClune2
1Universite´ PierreetMarieCurie-Paris6,CNRSUMR7222,France
2UniversityofWyoming,USA
Preprint–April21,2015
Nearly all science and engineering fields use search al-
gorithms, which automatically explore a search space to
findhigh-performingsolutions:chemistssearchthroughthe
spaceofmoleculestodiscovernewdrugs;engineerssearch
for stronger, cheaper, safer designs, scientists search for
models that best explain data, etc. The goal of search al-
gorithmshastraditionallybeentoreturnthesinglehighest-
performing solution in a search space. Here we describe a
new, fundamentally different type of algorithm that is more
useful because it provides a holistic view of how high-
performing solutions are distributed throughout a search Fig.1. TheMAP-Elitesalgorithmsearchesinahigh-dimensionalspace
space. Itcreatesamapofhigh-performingsolutionsateach tofindthehighest-performingsolutionateachpointinalow-dimensional
point in a space defined by dimensions of variation that featurespace,wheretheusergetstochoosedimensionsofvariationofin-
terestthatdefinethelowdimensionalspace.Wecallthistypeofalgorithm
a user gets to choose. This Multi-dimensional Archive of
an“illuminationalgorithm”,becauseitilluminatesthefitnesspotentialof
Phenotypic Elites (MAP-Elites) algorithm illuminates search
eachareaofthefeaturespace,includingtradeoffsbetweenperformance
spaces, allowing researchers to understand how interest- andthefeaturesofinterest.Forexample,MAP-Elitescouldsearchinthe
ing attributes of solutions combine to affect performance, spaceofallpossiblerobotdesigns(averyhighdimensionalspace)tofind
either positively or, equally of interest, negatively. For ex- thefastestrobot(aperformancecriterion)foreachcombinationofheight
andweight.
ample, a drug company may wish to understand how per-
formance changes as the size of molecules and their cost-
to-produce vary. MAP-Elites produces a large diversity of
byhumanengineers3: theyhavedesignedantennasthatNASA
high-performing, yet qualitatively different solutions, which
flewtospace4,foundpatentableelectroniccircuitdesigns3,auto-
can be more helpful than a single, high-performing solu-
matedscientificdiscovery5,andcreatedartificialintelligencefor
tion. Interestingly,becauseMAP-Elitesexploresmoreofthe
robots6–15. Becauseoftheirwidespreaduse,improvingsearchal-
search space, it also tends to find a better overall solution
gorithmsprovidessubstantialbenefitsforsociety.
thanstate-of-the-artsearchalgorithms. Wedemonstratethe
benefitsofthisnewalgorithminthreedifferentproblemdo- Mostsearchalgorithmsfocusonfindingoneorasmallsetof
mains ranging from producing modular neural networks to high-qualitysolutionsinasearchspace. Whatconstituteshigh-
designing simulated and real soft robots. Because MAP- qualityisdeterminedbytheuser,whospecifiesoneorafewob-
Elites (1) illuminates the relationship between performance jectives that the solution should score high on. For example, a
and dimensions of interest in solutions, (2) returns a set usermaywantsolutionsthatarehigh-performingandlow-cost,
of high-performing, yet diverse solutions, and (3) improves whereeachofthosedesiderataisquantifiablymeasuredeitherby
the state-of-the-art for finding a single, best solution, it will anequationorsimulator. Traditionalsearchalgorithmsinclude
catalyze advances throughout all science and engineering hillclimbing,simulatedannealing,evolutionaryalgorithms,gra-
fields. dientascent/descent,Bayesianoptimization,andmulti-objective
optimizationalgorithms1,2.Thelatterreturnasetofsolutionsthat
representthebesttradeoffsbetweenobjectives16.
Author’sNote:Thispaperisapreliminarydraftofapaperthatintro-
A subset of optimization problems are challenging because
ducestheMAP-Elitesalgorithmandexploresitscapabilities.Normally
theyrequiresearchingforoptimainafunctionorsystemthatis
wewouldnotpostsuchanearlydraftwithonlypreliminaryexperimen-
eithernon-differentiableorcannotbeexpressedmathematically,
taldata,butmanypeopleinthecommunityhaveheardofMAP-Elites,
typically because a physical system or a complex simulation is
areusingitintheirownpapers,andhaveaskedusforapaperthatde-
required. Suchproblemsrequire“blackbox”optimizationalgo-
scribesitsothattheycanciteit,tohelpthemimplementMAP-Elites,
rithms, which search for high-performing solutions armed only
andthatdescribestheexperimentswehavealreadyconductedwithit.
withtheabilitytodeterminetheperformanceofasolution, but
Wethuswanttoshareboththedetailsofthisalgorithmandwhatwe
without access to the evaluation function that determines that
havelearnedaboutitfromourpreliminaryexperiments. Alloftheex-
performance. On such problems, one cannot use optimization
perimentsinthispaperwillberedonebeforethefinalversionofthepaper
methods that require calculating the gradient of the function,
ispublished,andthedataarethussubjecttochange.
suchasgradientascent/descent.
Anotoriouschallengeinblackboxoptimizationisthepresence
1 Background and Motivation
oflocaloptima(alsocalledlocalminima)1,2.Aproblemwithmost
searchalgorithmsofthisclassisthattheytrytofollowapaththat
willleadtothebestglobalsolutionbyrelyingontheheuristicthat
Every field of science and engineering makes use of search al- randomchangestogoodsolutionsleadtobettersolutions. This
gorithms,alsoknownasoptimizationalgorithms,whichseekto approachdoesnotworkforhighlydeceptiveproblems,however,
automatically find a high-quality solution or set of high-quality becauseinsuchproblemsonehastocrosslow-performingvalleys
solutions amongst a large space of possible solutions1,2. Such tofindtheglobaloptima,orevenjusttofindbetteroptima2.
algorithms often find solutions that outperform those designed Becauseevolutionaryalgorithmsareoneofthemostsuccess-
MouretandClune arXiv | 1
5102
rpA
02
]IA.sc[
1v90940.4051:viXra


---

## Page 2

ful families of black-box search algorithms2,3, and because the will decrease exponentially when the number of dimensions of
workwebuildoncomesfromthatcommunity,hereweadoptthe thesearchspaceincreases).
language and metaphors of evolutionary computation. In that Herewepresentanewalgorithmthat,givenN dimensionsof
parlance,asolutionisanorganismorphenotypeorindividual,the variationofinterestchosenbytheuser,searchesforthehighest-
organism is described by a genome or genotype, and the actions performingsolutionateachpointinthespacedefinedbythose
performedbythatorganismaretheorganism’sbehavior.Theper- dimensions(Fig. 1). Thesedimensions arediscretized, withthe
formanceorqualityofasolutioniscalleditsfitness,andtheequa- granularityafunctionofavailablecomputationalresources.Note
tion, simulation, etc. thatreturnsthatfitnessvalueisthefitness thatthesearchspacecanbehigh-dimensional,orevenofinfinite
function. The way of stochastically producing new solutions is dimensions,butthefeaturespaceislow-dimensionalbydesign.
to take an existing solution and mutate its genome, meaning to We call this algorithm the multi-dimensional archive of pheno-
change the genome in some random way, and or to produce a typicelites,orMAP-Elites. Itwasusedandbrieflydescribedin6,
newsolutiondescriptorbysamplingportionsoftwoparentde- butthispaperisthefirsttodescribeandexploreitspropertiesin
scriptors,aprocesscalledcrossover. Solutionsthatproducenew detail.
offspringorganismsarethosethatareselected,andsuchselection ThebenefitsofMAP-Elitesincludethefollowing:
istypicallybiasedtowardssolutionswithhigherfitness2.
• Allowinguserstocreatediversityinthedimensionsofvari-
To encourage a broad exploration of the search space,
ationtheychoose.
many modern evolutionary algorithms encourage diversity
through a variety of different techniques, including increas-
• Illuminatingthefitnesspotentialoftheentirefeaturespace,
ing mutation rates when the rate of performance improve-
not just the high-performing areas, revealing relationships
mentstagnates1,2,17–19,explicitlyselectingforgeneticdiversity2,20
betweendimensionsofinterestandperformance.
or behavioral diversity21–25, or changing the structure of the
population26. Such diversity-promoting techniques often im- • Improved optimization performance; the algorithm often
prove the quality of the solutions produced and the number of findsabettersolutionthanthecurrentstate-of-the-artsearch
different types of solutions explored, but search algorithms still algorithms in complex search spaces because it explores
tendtoconvergetooneorafewgoodsolutionsearlyandcease moreofthefeaturespace,whichhelpsitavoidlocaloptima
tomakefurtherprogress2,21,25.
andthusfinddifferent,andoftenbetter,fitnesspeaks.
An alternate idea proposed in recent years is to abandon the
goal of improving performance altogether, and instead select • The search for a solution in any single cell is aided by the
only for diversity in the feature space (also called the behavior simultaneoussearchforsolutionsinothercells. Thisparal-
space): This algorithm, called Novelty Search, can perform bet- lel search is beneficial because (1) it may be more likely to
ter than performance-driven search on deceptive problems21–24. generate a solution for one cell by mutating a solution to
The user defines how to measure the distance between behav- a more distant cell, a phenomenon called “goal switching”
iors,andthenNoveltySearchseekstoproduceasmanydifferent in a new paper that uses MAP-Elites37, or (2) if it is more
behaviors as possible according to this distance metric. The al- likely to produce a solution to a cell by crossing over two
gorithm stops when an individual in the population solves the solutions from other cells. If either reason is true, MAP-
objective(i.e. theirperformanceishighenough). BecauseNov- Elites should outperform a separate search conducted for
eltySearchdoesnotworkwellwithverylargefeature/behavioral eachcell. Thereisevidencethatsupportsthisclaimbelow,
spaces27,28,therehavebeenmanyproposalsforcombiningselec- andthisspecificexperimentwasconductedinNguyenetal.
tion for novelty and performance28–31. The main focus of these 201537, which found that MAP-Elites does produce higher-
hybridalgorithmsremainsfindingthesinglebestindividualthat performing solutions in each cell than separately searching
solvesatask,orasetofindividualsthatrepresentthebestpossi- forahigh-performingsolutionineachofthosecells.
bletradeoffbetweencompetingobjectives.
• Returning a large set of diverse, high-performing individ-
In the last few years, a few algorithms have been designed
uals embedded in a map that describes where they are lo-
whosegoalisnottoreturnoneindividualthatperformswellon
catedinthefeaturespace,whichcanbeusedtocreatenew
oneobjective,butarepertoireofindividualsthateachperforms
wellonadifferent, relatedobjective14,22,32. Alongwithresearch typesofalgorithmsorimprovetheperformanceofexisting
algorithms6.
into behavioral diversity and Novelty Search, such repertoire-
gatheringalgorithmsinspirethealgorithmwepresentinthispa-
per. 2 Optimization vs. Illumination Algorithms
Whiletheexplorationofsearchspacesisatthecenterofmany
discussionsinoptimization,werarelyseethesesearchspacesbe- Optimizationalgorithmstrytofindthehighest-performingsolu-
causetheyareoftentoohigh-dimensionaltobevisualized.While tioninasearchspace. Sometimestheyaredesignedtoreturna
thecomputerscienceliteratureoffersplentyofoptionsfordimen- set of high-performing solutions, where members in the set are
sionality reduction and visualization of high-dimensional data also good on other objectives, and where the set represents the
33–36,suchalgorithmsare“passive”inthattheytakeafixeddata solution on the Pareto front of tradeoffs between performance
set and search for the best low-dimensional visualization of it. andqualitywithrespecttothoseotherobjectives. Optimization
Theydonottackletheissueofgeneratingthisdataset. Inother algorithms are not traditionally designed to report the highest-
words, they do not explore a high-dimensional space in such a performingsolutionpossibleinanareaofthefeaturespacethat
wayastorevealinterestingpropertiesaboutittoauserviaalow- cannotproduceeitherthehighest-performingsolutionoverall,or
dimensionalvisualization. Suchexplorationalgorithmsarenec- asolutionontheParetofront.
essarywhentheentiresearchspaceistoolargetobesimplyvisu- Adifferentkindofalgorithm, whichwecallilluminationalgo-
alizedbyadimensionalityreductionalgorithm,butinsteadmust rithms, are designed to return the highest-performing solution
beactivelyexploredtolearninterestingfactsaboutit. Forexam- at each point in the feature space. They thus illuminate the fit-
ple,toidentifyalltheperformancepeaksinalargesearchspace, ness potential of each region of the feature space. In biological
wemustactivelysearchforthem.Itisnotenoughtosamplemil- terms,theyilluminatethephenotype-fitnessmap38. Anyillumi-
lionsofsolutionsandplotthem,forthesamereasonasrandom nationalgorithmcanalsobeusedasanoptimizationalgorithm,
sampling is often not a good optimization algorithm: finding a makingilluminationalgorithmsasupersetofoptimizationalgo-
fitness peak by chance is very unlikely for large search spaces rithms. MAP-Elites is an illumination algorithm. It is inspired
(inmostcases,theprobabilityoffindingthebestpossiblefitness bytwopreviousilluminationalgorithms,NoveltySearch+Local
MouretandClune arXiv | 2


---

## Page 3

procedureMAP-ELITESALGORITHM(SIMPLE,DEFAULTVERSION)
(P ←∅,X ←∅) (cid:46)Createanempty,N-dimensionalmapofelites:{solutionsX andtheirperformancesP}
foriter=1→Ido (cid:46)RepeatforIiterations.
ifiter<Gthen (cid:46)InitializebygeneratingGrandomsolutions
x(cid:48) ←random solution()
else (cid:46)Allsubsequentsolutionsaregeneratedfromelitesinthemap
x←random selection(X) (cid:46)RandomlyselectanelitexfromthemapX
x(cid:48) ←random variation(x) (cid:46)Createx(cid:48),arandomlymodifiedcopyofx(viamutationand/orcrossover)
b(cid:48) ←feature descriptor(x(cid:48)) (cid:46)Simulatethecandidatesolutionx(cid:48)andrecorditsfeaturedescriptorb(cid:48)
p(cid:48) ←performance(x(cid:48)) (cid:46)Recordtheperformancep(cid:48)ofx(cid:48)
ifP(b(cid:48))=∅orP(b(cid:48))<p(cid:48)then (cid:46)Iftheappropriatecellisemptyoritsoccupants’sperformanceis≤p(cid:48),then
P(b(cid:48))←p(cid:48) (cid:46)storetheperformanceofx(cid:48)inthemapofelitesaccordingtoitsfeaturedescriptorb(cid:48)
X(b(cid:48))←x(cid:48) (cid:46)storethesolutionx(cid:48)inthemapofelitesaccordingtoitsfeaturedescriptorb(cid:48)
returnfeature-performancemap(PandX)
Fig.2.Apseudocodedescriptionofthesimple,defaultversionofMAP-Elites.
Competition (NS+LC)22 and the Multi-Objective Landscape Ex- measuring the behavior of the phenotype while it performs, ei-
plorationalgorithm(MOLE)32.Allthreearedescribedbelow. therinsimulationorreality.
Note that there may be many levels of indirection between x
andb x.Withdirectencoding,eachelementinthegenomespecifies
3 Details of the MAP-Elites algorithm anindependentcomponentofthephenotype2,7,39. Inthatcase,it
is straightforward to map genotypes into phenotypes, and then
MAP-Elitesisquitesimple,bothconceptuallyandtoimplement. measureperformanceandfeatures(evaluatingthephenotypein
PseudocodeofthealgorithmisinFig.2. First, auserchoosesa asimulatorortherealworldifnecessary).Anextralevelofindi-
performancemeasuref(x)thatevaluatesasolutionx.Forexam- rectioncanoccurwithindirectencoding,alsoknownasgenerative
ple, if searching for robot morphologies, the performance mea- or developmental encoding, in which information in the genome
surecouldbehowfasttherobotis. Second,theuserchoosesN canbereusedtoaffectmanypartsofthephenotype(alsocalled
dimensions of variation of interest that define a feature space of pleiotropy);suchencodingshavebeenshowntoimproveregular-
interesttotheuser.Forrobotmorphologies,onedimensionofin- ity,performance,andevolvability2,7,8,11–13,39–42. Inotherwords,a
terestcouldbehowtalltherobotis,anothercouldbeitsweight,a complexprocesscanexistthatmapsgenomex →tophenotype
thirdcouldbeitsenergyconsumptionpermetermoved,etc. An p
x
→tofeaturesb xandperformancefx.
alternateexamplecouldbesearchingforchessprograms,where MAP-ElitesstartsbyrandomlygeneratingGgenomesandde-
theperformancemeasureisthewinpercentage,andthedimen- terminingtheperformanceandfeaturesofeach. Inarandomor-
sionsofvariationcouldbetheaggressivenessofplay,thespeed der,thosegenomesareplacedintothecellstowhichtheybelong
withwhichmovesareselected,etc. Afurtherexampleisevolv- inthefeaturespace(ifmultiplegenomesmaptothesamecell,the
ing drug molecules, where performance could be a drug’s effi- highest-performingonepercellisretained). Atthatpointtheal-
cacyanddimensionsofvariationcouldbethesizeofmolecules, gorithmisinitialized,andthefollowingstepsarerepeateduntil
thecosttoproducethem,theirperishability,etc. a termination criterion is reached. (1) A cell in the map is ran-
Eachdimensionofvariationisdiscretizedbasedonuserprefer- domlychosenandthegenomeinthatcellproducesanoffspring
enceoravailablecomputationalresources.Thisgranularitycould viamutationand/orcrossover.(2)Thefeaturesandperformance
bemanuallyspecifiedorautomaticallytunedtotheavailablere- of that offspring are determined, and the offspring is placed in
sources,includingstartingwithacoarsediscretizationandthen thecellifthecellisemptyoriftheoffspringishigher-performing
increasingthegranularityastimeandcomputationallow. thanthecurrentoccupantofthecell,inwhichcasethatoccupant
Givenaparticulardiscretization,MAP-Eliteswillsearchforthe isdiscarded.
highest performing solution for each cell in the N-dimensional Theterminationcriterioncanbemanythings, suchasifaset
featurespace.Forexample,MAP-Eliteswillsearchforthefastest amount of time expires, a fixed amount of computational re-
robotthatistall,heavy,andefficient;thefastestrobotthatistall, sources are consumed, or some property of the archive is pro-
heavy,andinefficient,thefastestrobotthatistall,light,andeffi- duced. Examplesofthelattercouldincludeacertainpercentage
cient,etc. ofthemapcellsbeingfilled,averagefitnessinthemapreaching
Thesearchisconductedinthesearchspace,whichisthespace aspecificlevel,ornsolutionstoaproblembeingdiscovered.
ofallpossiblevaluesofx,wherexisadescriptionofacandidate Onecanconsiderthearchive,whichisthesetofdescriptorsin
solution. In our example, the search space contains all possible allthecells,asthetraditionalpopulationinanevolutionaryalgo-
descriptionsofrobotmorphologies(notethatwemustsearchin rithm. ThedifferenceisthatinMAP-Eliteseachmemberofthe
thespaceofdescriptionsofrobotmorphologies;itisnotpossible population is by definition diverse, at least according to the di-
tosearchdirectlyinthespaceofrobotmorphologiesordirectly mensionsofthefeaturespace.
inthefeaturespace).Wecallthexdescriptoragenomeorgenotype The above description, for which pseudocode is provided in
andtherobotmorphologythephenotype,orp x. Wehavealready Fig. 2, is the default way to implement MAP-Elites. To encour-
mentioned that a function f(x), called a fitness function, returns age a more uniform exploration of the space at a coarse resolu-
theperformanceofeachx. Afeature(a.k.a. behavior)function tion,andthenamorefine-grainedsearchafterwards,wecreated
b(x)mustalsoexistorbedefinedthat,foreachx,determinesx’s a hierarchical version that starts with larger cells in the feature
valueineachoftheN featuredimensions. Inotherwords,b(x) spacethatarethensubdividedintosmallercellsduringsearchaf-
returnsb x,whichisanN-dimensionalvectordescribingx’sfea- terpredeterminednumbersofevaluationshavebeenperformed
tures. In our example, the first dimension of b x is the robot’s (Methods). Wefurtherparallelizedthisalgorithmtorunonclus-
height,theseconddimensionisitsweight,andthethirdisitsen- tersofnetworkedcomputers,byfarmingoutbatchesofevalua-
ergy consumption per meter moved, etc. Some elements of the tionstoslavenodes,insteadofperformingeachevaluationseri-
feature vector may be directly measured in the phenotype (e.g. ally(Methods). Section8containsideasforadditional,alternate
height, weight), but others (e.g. energy consumption) require possiblevariantsofMAP-Elites.
MouretandClune arXiv | 3


---

## Page 4

TherearetwothingstonoteaboutMAP-Elites: calculations are O(nlog(n))43 each generation. MAP-Elites
onlyneedstolookupthecurrentoccupantofthecell,which
• Itisnotguaranteedthatallcellsinthefeaturespacewillbe
isO(1).
filled, fortworeasons. (1)Theremaybenogenomexthat
mapstoaparticularcellinthefeaturespace. Forexample, • Novelty Search contains both a current population and an
itmaybeimpossibletohavearobotofacertainheightand archive of previous solutions that serves as a memory of
weightduetophysicallaws. (2)Thesearchalgorithmmay whichpointsinthefeaturespacehavebeenvisited. Main-
fail to produce a genome that maps to a cell in the feature tainingbothapopulationandanarchiverequiresmanyad-
space,evenifsuchagenomeexists. ditionalparametersthathavetobechosencarefullyorper-
formancecanbedetrimentallyaffected29.
• Therearemanygenotypesthatcanbemappedtothesame
cellinthefeaturespace,perhapsaninfinitenumber. Forex- • GiventhatNoveltySearchrewardsindividualsthataredis-
ample,therearemanyrobotblueprintsthatproducearobot
tantfromeachotherinthefeaturespace,havingonlyapop-
withthesameheight,weight,andenergyconsumption. For
ulation would lead to “cycling”, a phenomenon where the
that reason, and because it is not known a priori which
populationmovesfromoneareaofthefeaturespacetoanew
genomeswillmaptowhichcells,itisnotpossibletosearch
areaandbackagain,withoutanymemoryofwhereithasal-
directlyinthefeaturespace. Recallthatthereis, evenwith
readyexplored. ThearchiveinNS+LClimits, butdoesnot
direct encodings, and especially with indirect encodings, a
eliminate,thisphenomenon.MAP-Elitesdoesawaywiththe
complexmappingfromgenomextothefeaturevectorb x.If
archivevs.populationdistinctionbyhavingonlyanarchive.
itispossibleinagivenproblemtodirectlytakestepsinthe
Itthusavoidscyclingandisalwayssimultaneouslyfocused
feature space, then MAP-Elites is unnecessary because one
onexpandingintonewniches(untiltherearenoneleft)and
couldsimplyperformexhaustivesearchinthefeaturespace.
improvingtheperformanceofexistingniches.
OnecanthinkofMAP-Elitesasawayoftryingtoperform
Itisthusquiteeasytointuitwhattheselectionpressurefor
suchanexhaustivesearchinthefeaturespace,butwiththe
MAP-Elitesisovertime. Incontrast,theselectionpressures
additionalchallengeoftryingtofindthehighest-performing
forNoveltySearcharemoredynamicandthushardertoun-
solutionforeachcellinthatfeaturespace.
derstand,evenforNoveltySearchvariantsthathaveonlyan
archiveandnopopulation29. Forexample,itishardtopre-
4 Differences between MAP-Elites and previous,
dicthowmuchsearchwillbefocusedineachareaofthefea-
related algorithms turespace,becausearelativelysparseareaduringoneeraof
thesearchcanbecomerelativelycrowdedlateron,andvice
In 2011, Lehman and Stanley22 note that combining a selective versa.
pressureforfeaturediversitywithoneperformanceobjectivethat
ThedynamicsofNS+LCareevenmoredynamic, complex,
allofthedifferenttypesofphenotypescompeteonisakintohav-
andunpredictable. Onethingtokeepinmindisthat,while
ing butterflies and bacteria compete with bears and badgers on
theperformanceofsolutionsinNS+LCisonlyjudgedver-
one performance criterion (e.g. speed). Doing so is unhelpful
sus neighbors, these relative performance scores are then
forproducingthefastestofeachtypeofcreature, giventhedif-
competed globally within the (relative) performance objec-
ferentspeedscalesthesecreaturesexhibit. Instead,Lehmanand
tive.Overall,therefore,NS+LCbiasessearchtowardsunder-
Stanley propose encouraging diversity in the feature space, but
explored areas of the feature space (taking into account
havingeachorganismcompeteonperformanceonlywithother
the archive and the population), areas of the search space
organismsthatarenearitinthefeaturespace,analgorithmthey
withthehighestrelativeperformance,andtradeoffsbetween
callNoveltySearch+LocalCompetition(NS+LC)22. NS+LCaccom-
these two objectives. An organism in an area that is bet-
plishesthesegoalsviaamulti-objectivealgorithmwithtwoob-
ter than its neighbors, but where this gap is not as large
jectives:(1)maximizinganorganism’sperformancerelativetoits
as elsewhere, will not be explored as often unless or until
closest15neighbors(i.e.localcompetition,butnotethattheserel-
that larger performance gap elsewhere is reduced. The fo-
ativescoresarethenenteredintoaglobalcompetition,theimpli-
cus of the (relative) performance objective is thus complex
cationsofwhicharediscussedbelow),and(2)maximizinganov-
andever-changing. Thediversityobjectiveisalsocomplex
elty objective, which rewards organisms the further they are in
and dynamic, because NS+LC does not only store one so-
featurespacefromtheir15closestneighbors. Whereasnormally
lution per cell. Many solutions can pile up in one area of
evolutionary algorithms do not produce much diversity within
thespace,creatingapressuretoexploreunder-exploredar-
onerun,butinsteadhavetoperformmultiple,independentruns
easuntilthoseareasaremoreexploredrelativetotheinitial
toshowcasediversity8,NS+LCproducesasubstantialamountof
area,creatingapressuretoreturntotheinitialarea,andso
differenttypesofhighperformingcreatureswithinoneevolving
on.
population22.
NS+LC inspired us to create two algorithms that also seek to For both objectives, thus, it is hard to intuit both the dy-
find the highest performing solution at each point in a feature namicsthemselvesandwhateffectsthesedynamicshaveon
space. ThefirstwastheMulti-ObjectiveLandscapeExploration search. MAP-Elites, incontrast, producesoffspringbyuni-
(MOLE)algorithm32andthesecondisMAP-Elites,thealgorithm formlysamplingfromtheexistingarchive,suchthattheonly
presented in this paper. MOLE has two objectives: the first is thingthatchangesovertimeisthenumberofcellsthatare
performance,andthesecondforeachorganismtobeasfarfrom filledandtheirperformance. MAP-Elitesthusembodiesthe
otherorganismsaspossible,wheredistanceismeasuredinafea- mainprincipleofilluminationalgorithms,whichistosearch
turespacethatauserspecifies. forthehighest-performingsolutionateachpointofthefea-
BothNS+LCandMOLEhavesimilargoalstoMAP-Elites:they turespace,inamoresimple,intuitive,andpredictableway.
searchforthehighest-performingsolutionateachpointinafea-
• In the default version of MAP-Elites, organisms only com-
turespace. However,botharemorecomplicatedand,aswillbe
petewiththeorganism(thecurrentoccupant)intheircell,so
shown in the results section, do not perform as well as MAP-
therangeoffeaturestheycompetewithisfixed. InNovelty
Elitesempirically.
Search and NS+LC, organisms compete with their nearest
SpecificdifferencesbetweenMAP-ElitesandNS+LCinclude:
neighborsinthefeaturespace.Especiallyatthebeginningof
• NoveltySearchneedstocomputethefeaturedistancetoev- therunbeforethearchivefillsup,thatmightmeanthator-
ery other organism each generation; such nearest neighbor ganismsarecompetingwithothersthathaveverydifferent
MouretandClune arXiv | 4


---

## Page 5

features,whichiscontrarytothespiritoflocalcompetition • Precision (opt-in reliability): For each run, if (and only if)
inthefeaturespace. aruncreatesasolutioninacell,theaverageacrossallsuch
cellsofthehighestperformingsolutionproducedforthatcell
SpecificdifferencesbetweenMAP-ElitesandMOLEinclude: divided by the highest performing solution any algorithm
found for that cell. Section 9.4.2 provides the formal equa-
• MOLEfeaturesoneglobalperformancecompetition(viathe
tion.
performance objective). Thus, a few high-performing indi-
viduals will dominate this objective, making it hard to rec- Thismetricmeasuresadifferentnotionofreliability,which
ognize and keep a slightly better performing solution in a isthetrustwecanhavethat,ifanalgorithmreturnsasolu-
low-ormedium-performingregionofthespace.MAP-Elites tioninacell,thatsolutionwillbehigh-performingrelativeto
isbetteratrecognizingandkeepinganyimprovementtofit- whatispossibleforthatcell. Toanthropomorphize, theal-
ness in any region of the space, no matter how the perfor- gorithm gets to opt-in which cells it wishes to fill and thus
manceofthatcellcomparestoothercells. Asanexampleof be measured on. The ideal illumination algorithm would
whenMOLEmightfailtorewardanimportantinnovation, haveaperfectscoreof1forthiscriterion. Optimizational-
imagine a new solution in a medium-performing, densely gorithmsshouldfarebetteronthiscriterionthanglobalreli-
packed region of the space, that is higher-performing than ability,becausetheywilltendtoexploreonlyafewareasof
anything previously found in that cell. This new solution, the feature space, but should produce high-performing so-
which represents the best performance yet found in that lutionsinmanycellsinthoseareas. Note, however, thatif
cell, would not be selected for because it is neither high- anoptimizationalgorithmstartsinalow-performingregion
performing versus other organisms in the population, nor ofthefeaturespaceandmovestoaneighboringregion,itis
would it be kept because it is diverse. Thus, the organism expected that its relative performance in the cells it started
doesnotperformwellineitheroftheMOLEobjectives,yet inwillstaylow,asoptimizationalgorithmsarenotaskedto
it is precisely what we truly want: the highest performing improve performance in those cells. Thus, even ideal opti-
individualfoundsofarinthatareaofthefeaturespace. mization algorithms are not expected to perform perfectly
onthiscriteriononaverage, althoughtheymaydosoonce
• LikeNoveltySearch,thediversityobjectiveinMOLEhasun- inawhile.
stabletemporaldynamics.Thepopulationmayrushtoarel-
ativelyunexploredarea,fillitup,thenrushofftoanewrel- • Coverage: Measureshowmanycellsofthefeaturespacea
ativelyunexploredarea, andthenrushbacktotheoriginal runofanalgorithmisabletofillofthetotalnumberthatare
area.Itdoesnotevenlysearchforimprovementstoallareas possibletofill.Themathematicaldetailsarespecifiedinsec-
ofthemapsimultaneously. tion9.4.3.Thismeasuredoesnotincludetheperformanceof
thesolutionsinthefilledcells. Theidealilluminationalgo-
rithm would score perfectly on this metric. The ideal opti-
5 Criteria for Measuring the Algorithms
mization algorithm is not expected to perform well on this
criterion.
Therearemanydifferentwaystoquantifythequalityofillumi-
nationalgorithmsandoptimizationalgorithms.Inthispaper,we
evaluatealgorithmsonthefollowingquantifiablemeasures: 6 Experiments and Results
• Global Performance: For each run, the single highest- We evaluated MAP-Elites in three different search spaces: neu-
performing solution found by that algorithm anywhere in ralnetworks,simulatedsoftrobotmorphologies,andareal,soft
thesearchspacedividedbythehighestperformancepossi- robotic arm. The neural network search space is interesting be-
ble in that domain. If it is not known what the maximum cause evaluations are fast, allowing us to draw high-resolution
theoretical performance is, as is the case for all of our do- feature-space maps for a high-dimensional search space. The
mains,itcanbeestimatedbydividingbythehighestperfor- experiments with both simulated and real soft robot are inter-
mancefoundbyanyalgorithminanyrun. Thismeasureis esting because soft robots are important, new design spaces
thetraditional,mostcommonwaytoevaluateoptimization wheretraditionaldesignandcontrolmethodsdonotworkwell,
algorithms. Onecanalsomeasurewhetheranyillumination if at all. Thus, we need advanced search algorithms to find
algorithmalsoperformswellonthismeasurement.Boththe high-performing designs. The first two search spaces (neu-
ideal optimization algorithm and the ideal illumination al- ral networks and simulated soft robots) are extremely high-
gorithmareexpectedtoperformperfectlyonthismeasure. dimensional, demonstrating the ability of MAP-Elites to cre-
atelow-dimensionalfeaturemapsfromhigh-dimensionalsearch
• Globalreliability: Foreachrun,theaverageacrossallcells spaces. The third, involving the soft robot arm, involves eval-
of the highest-performing solution the algorithm found for uations that are performed directly on a real robot because the
each cell (0 if it did not produce a solution in that cell) di- softpropertiesoftherobotaretoocomplextosimulate. Thisdo-
videdbythebestknownperformanceforthatcellasfound maindemonstratesthatMAP-Elitesisalsoeffectiveeveninalow-
byanyrunofanyalgorithm.Cellsforwhichnosolutionwas dimensional,challenging,real-worldproblem.
found by any run of any algorithm are not included in the
calculation (to avoid dividing by zero, and because it may
6.1 Searchspace1: neuralnetworks
notbepossibletofillsuchcellsandalgorithmsthusshould
notbepenalizedfornotdoingso).Section9.4.1providesthe
ThisproblemdomainisidenticaltoonefromCluneetal. 201332,
formalequation.
which itself is based on the domain from Kashtan and Alon
This measure assesses how reliable an algorithm is at find- 200544.Thefollowingexplanationofthedomainisadaptedfrom
ingthehighest-performingsolutionforeachcellinthemap. Cluneetal.201332.
It is the most important measure we want an illumination The problem involves a neural network that receives stimuli
algorithmtoperformwellon,andtheidealilluminational- fromaneight-pixelretina.Patternsshownontheretina’sleftand
gorithm would perform perfectly on it. There is no reason righthalvesmayeachcontainanobject(i.e.apatternofinterest).
toexpectpureoptimizationalgorithms, evenidealones, to Networks have to answer whether an object is present on both
performwellonthiscriterion. theleftandrightsidesoftheretina32,44. Eachnetworkiteratively
MouretandClune arXiv | 5


---

## Page 6

seesallpossible256inputpatternsandanswerstrue(≥0)orfalse earlydraftofthepaperwedonotyethavedatatosharebecause
(<0).Itsperformanceisthepercentageofcorrectanswers. theMOLErunsinthatpaperwereatalowerresolution;wewill
Because it has been shown that minimizing connection costs addafaircomparisonofMOLEtoMAP-Elitesinafuturedraftof
promotes the evolution of modularity32, it is interesting to vi- thispaper.WecanreportthattheMOLEfiguresfromCluneetal.
sualize the relationship between network connection costs and 2013requiredmergingdatafrommany(specifically,30)different
modularity.Todoso,wecancreatea2Dfeaturespacewherethe runs of MOLE, meaning that across many MOLE runs we took
firstfeaturedimension(xaxis)isconnectioncost(thesumofthe thehighest-performingnetworkfoundineachcell. Thevariance
squared length of the connections in a network32), and the sec- intheseMOLErunswashigh,suchthatmanyoftherunsdidnot
ond feature dimension is network modularity (computed using findhigh-performingnetworksinlargeregionsofthespace;we
anefficientapproximationofNewman’smodularityscore45).The thuswereonlyabletogetagoodpictureofthefitnesspotentialof
resolutionofthemapis512×512;themapisfilledbythehierar- eachregionbytakingdatafrommanydifferentruns. Thathigh
chicalversionofMAP-Eliteswith10,000evaluations(Methods). variancemeansthatanyindividualMOLErundidnotproduce
Forthisdomain, wecompareMAP-Elitestothreeotheralgo- areliable,consistent,truepictureofthefitnesspotentialofeach
rithms: (1)atraditional,single-objectiveevolutionaryalgorithm region of the space; such a picture only came into view with a
withselectionforperformanceonly,whichthusdoesnotexplic- tremendousamountofcomputationspentonmanyMOLEruns.
itlyseekdiversityineitherfeaturedimension,(2)noveltysearch Incontrast,eachindividualMAP-Elitesrunproducesaconsistent
with local competition (NS+LC) 22, which is described above, picture that looks similar to the result of merging many MOLE
where novelty is measured in the same 2D feature space, and runs. There is still variance between MAP-Elites runs, but it is
(3)torandomsampling. Forthesethreecontrolexperiments,we much smaller, meaning that each run of the algorithm is more
recordallthecandidatesolutionsevaluatedbythealgorithmand reliable.
then keep the best one found per cell in the feature space (i.e. We next investigated the assumption that elites are found by
theeliteperformerforeachcell),andreportandplotthesedata. mutating genomes nearby in the feature space, and found that
Each treatment is allocated the same number of fitness evalua- thisassumptionislargelytrue(Fig. 4,Left). Mostorganismsde-
tions(Methods).Foreachtreatment,20independentrunsareper- scend from nearby organisms, whether close neighbors, nearby
formed,meaning20independentreplicatesthateachstartwitha neighbors, ormoredistantneighborswithinthesameregionof
differentrandomnumberseedandthushavedifferentstochastic the space. None of the organisms we randomly sampled were
events. producedbyaparentmorethanhalfwayacrossthefeaturemap.
The results reveal that MAP-Elites scores significantly higher That said, many high-performing elites do descend, not from
(p<1×10−7)thanthethreecontrolalgorithmsonallfourcriteria immediate neighbors, but from a high-performing neighbor a
describedinsection5:globalperformance,globalreliability,pre- mediumdistanceaway. Thatfactshowsthatpurelylocalsearch,
cision,andcoverage(Fig. 3,Top). Qualitatively,thedifferencein whichlikelyconcentratesononeareaofthefeaturespace, may
MAP-Elitesvs. thecontrolsisapparentintypical,examplemaps not be the best way to discover high-performing solutions, and
producedbyeachtreatment(Fig.3,Bottom).Overall,MAP-Elites suggeststhatonereasonMAP-Elitesisabletofindsomanyhigh-
finds solutions that are more diverse and high-performing than performing solutions is because collecting a large reservoir of
traditional optimization algorithms (here called the “traditional diverse, high-performing solutions makes it more likely to find
EA”), novelty search with local competition, and random sam- new,different,high-performingsolutions.
pling. Lookingatthedirectparentsofelitessuggeststhatarelatively
Itissurprisingthat,evenwhenlookingonlyatthebestperfor- local,butoverlapping,searchistakingplaceineachregionofthe
manceoverall(globalperformance),MAP-Elitesoutperformsthe map. However, looking at the entire lineage of four randomly
traditionalEA,whichfocusesexplicitlyonfindingthesinglebest- chosenelitesrevealsthatlineagesfrequentlytraverselongpaths
performingindividualinthesearchspace. Thatislikelybecause throughmanydifferentregionsofthemap(Fig. 4,right). These
theretinaproblemisdeceptive32andthistraditionalevolutionary lineagesfurtherunderscorethebenefitofsimultaneouslysearch-
algorithmhasnopressurefordiversity,whichisknowntohelp ingforhigh-performingorganismsateachpointinthemap: do-
withdeception2. ingsomayprovidesteppingstonestohigh-performingsolutions
While MAP-Elites significantly outperforms all controls on in a region that may not have been discovered had search been
bothreliabilityandprecision(opt-inreliability),thegapismuch tryingtoincreaseperformancebysearchingonlyinthatregion.
narrowerforprecision,asistobeexpected.Intermsofcoverage, Thisresultwasreplicatedinarecentstudyinadifferentdomain
random sampling was the second best of the algorithms in our thatinvestigatedthisissuewithMAP-Elitesinmoredepth37.
study. MAP-Elites likely outperforms it in this regard because
mutations to members of a diverse population are more likely
6.2 Simulatedsoft,locomotingrobotmorphologies
to fill new cells versus randomly generating genomes. That is
especiallytrueifcellsaremorelikelytobefilledbymutatinga Softrobotsaremadeofsoft,deformablematerials;theyopenup
nearbycellthanbyrandomlysamplingfromthespaceofallpos- newdesignspaces,allowingthecreationofrobotsthatcanper-
siblegenotypes. Imagine,forexample,thatmostrandomlysam- formtasksthattraditionalrobotscannot46–49. Forexample,they
pledgenotypesareinthecenterofamap. Inthatcase,itwould canadapttheirshapetotheirenvironment,whichisusefulinre-
beunlikelytoproduceanorganisminacornerbyrandomsam- strictedspaceslikepipelines,caves,andbloodarteries. Theyare
pling. In contrast, MAP-Elites could slowly accumulate organ- also safer to have around humans50. However, they are harder
ismsincellscloserandclosertothecorner,makingitmorelikely todesignbecausetheircomponentshavemanymorenon-linear
toeventuallyfillthatcorner. Randomsamplinglikelyproduces degreesoffreedom48,51.
morecoveragethanthetraditionalEAbecausethelattertendsto It has previously been shown that an evolutionary algorithm
allocate new individuals as offspring of the highest-performing withamodern,generativeencoding(explainedbelow)canpro-
organismsfoundsofar,focusingsearchnarrowlyattheexpense duce a diversity of soft robots morphologies that move in dif-
ofexploringthefeaturespace. Itisnotclearwhyrandomsam- ferentways8. However,thediversityofmorphologiesshownin
plingproducedmorecoveragethanNS+LC,althoughthisresult that paper and its accompanying video (https://youtu.be/
needstobetestedacrossawiderrangeofparametersbeforeits z9ptOeByLA4)camefromdifferentrunsofevolution.Withineach
robustnessisknown. run, most of the morphologies were similar. As is typical with
WecanalsoreportanecdotallythatMAP-Elitesperformsmuch evolutionaryalgorithms,ineachrunthesearchfoundalocalop-
betterinthisdomainthantheMOLEalgorithm,whichwaspre- timumandbecamestuckonit,spendingmostofthetimeexplor-
viouslyappliedtothissamedomainandfeaturespace32.Forthis ingthesimilardesignsonthatpeak.
MouretandClune arXiv | 6


---

## Page 7

Global performance Reliability Precision Coverage
1.05
1.0 1.0 1.0
1.00
0.8 0.8 0.8
0.95
0.6 0.6 0.6
0.90
0.4 0.4 0.4
0.85
0.80 0.2 0.2 0.2
0.75 0.0 0.0 0.0
Tr a diti o n n a R l E a A n N d S o + m L S C a m pli n M g A P- Elit e s Tr a diti o n n a R l E a A n N d S o + m L S C a m pli n M g A P- Elit e s Tr a diti o n n a R l E a A n N d S o + m L S C a m pli n M g A P- Elit e s Tr a diti o n n a R l E a A n N d S o + m L S C a m pli n M g A P- Elit e s
5.0 0.950 5.0 0.92 5.0 0.84
0.925 0.90 0.83
4.0 0.900 4.0 0.88 4.0 0.82
3.0 0.875 3.0 0.86 3.0 0.81
0.80
0.850 0.84
2.0 0.825 2.0 0.82 2.0 0.79
0.78
0.80
1.0 0.800 1.0 1.0 0.77
0.78
0.775 0.76
0.76
0.0 1.0 2.0 3.0 4.0 5.0 0.750 0.0 1.0 2.0 3.0 4.0 5.0 0.0 1.0 2.0 3.0 4.0 5.0 0.75
(b) TraditionalEA (c) NoveltySearch+LocalCompetition (d) RandomSampling
1.000
5.0
0.975
0.950
4.0
0.925
3.0 0.900
0.875
2.0 0.850
0.825
1.0 0.800
0.775
0.0 1.0 2.0 3.0 4.0 5.0 0.750
(e) MAP-Elites
Fig.3. MAP-Elitesproducessignificantlyhigher-performingandmorediversesolutionsthancontrolalgorithms. Top: MAP-Elitessignificantlyout-
performs controls on global performance (finding the single highest-performing solution), reliability (average performance across all fillable cells),
precision (average performance only of cells filled by the algorithm), and coverage (the number of cells filled). All of the metrics are normalized.
Section5explainsthesemetricsinmoredetail. Intheboxplotforeachmetric,theblacklineshowsthemedian. Bottom: Examplemapsproduced
byasinglerun(thefirstone)ofeachtreatment. AsdescribedinCluneetal. 201332,thex-axisisconnectioncost,they-axisismodularity,andheat
mapcolorsindicatenormalizedperformance.ThesemapsshowthatMAP-Elitesilluminatesmoreofthefeaturespace,revealingthefitnesspotential
ofeacharea.
The morphologies evolved in Cheney et al.8 also rarely in- werealsointerestedinmorphologiesofdifferentsizes,whichcan
cludedoneofthefourmaterialsavailable,astiff(darkblue)ma- alsobeaddedasadifferentdimensionofvariationtobeexplored
terial analogous to bone. The authors (one of which is the last byMAP-Elites.
authoronthispaper)triedmanydifferentparametersandenvi- HerewetestwhetherMAP-Elitescanaddresstheissuesraised
ronmentalchallengestoencouragetheoptimizationalgorithmto inthetwopreviousparagraphs. Specifically,wetest(1)whether
usemoreofthismaterial,butitrarelydid. Onecould,ofcourse, MAP-Elitescanproducealargediversityofmorphologieswithin
explicitlyincludeaterminthefitnessfunctiontorewardthein- one run and (2) whether it can produce high-performing mor-
clusionofthismaterial,butthatmaycauseevolutiontooverin- phologies for a range of levels of bone use and body size, and
vestinit,anditishardtoknowaheadoftimehowmuchmaterial combinationsthereof.
to encourage the inclusion of to produce interesting, functional WeadoptthesamedomainasCheneyetal. 20138byevolving
designs. Theidealwouldbetoseethehighest-performingcrea- multi-material,softrobotsintheVoxcadsimulator52. Robotsare
tureateachlevelofboneuse,andthuslearnhowtheuseofbone specifiedinaspaceof10×10×10voxels,whereeachvoxelisei-
affectsbothfitnessandmorphologydesign. Thatisexactlywhat theremptyorfilledwithoneoffourkindsofmaterial:bone(dark
MAP-Elites is designed for. The authors of Cheney et al. 2013 blue, stiff), soft support tissue (light blue, deformable), muscles
MouretandClune arXiv | 7


---

## Page 8

Fig.4. Mostelitesarefoundbymutatingaparentgenomethatwasnearbyinthefeaturespace,buttheentirelineagesofexampleelitesreveals
search paths that traverse large distances through the feature space. The data in these plots are from the neural network domain. As in Fig. 3
andFig.3ofCluneetal.32,thex-axisisconnectioncostandthey-axisismodularity. Left: Forarandomsubsetofelitesfromtheneuralnetwork
domain,wedrawanarrowpointingatthatelitethatstartsinthelocationoftheparentthatproducedthatelite.Iftherewerenocorrelationbetweenthe
locationofaneliteanditsparent,therewouldbefarmorelongarrows.Mostelitesareproducedfromparentswithinarangeofdistancesinanearby
region(approximately0.2orless). Thecolorofthebeginningofeacharrowdenotestheperformanceoftheparent,andthecolortowardthetipof
thearrowdenotestheperformanceoftheelite. Notethatmanyhigh-performingelitesdescendfromotherhigh-performingelites,butoftennotfrom
directneighboringcells. Thesedatasuggestthatcollectinghigh-performingelitesinmanydifferentlocationshelpsdiscoverhigh-performingelitesin
newlocations,whichislikelywhyMAP-Elitesisabletofindsomanydifferent,high-performingsolutions. Right: Examplelineagestracingallofthe
descendantsoffourrandomlyselectedfinalelites.Foreachofthefourelites,adashedlineofadifferentcolor(green,orange,blue,orpurple)startsat
itsrandomlygenerated,generation0ancestor(redcircle),whichinterestinglyisthesameforallfourelites.Notethatthecolorsandpathsareharderto
differentiatewhenthedifferentlineagesoverlap.Eachdashedlinepassesthroughthelocationinthefeaturespaceofeachancestoralongthelineage
ofthateliteandterminatesatthatelite’slocationinthefeaturespace. Thecolorofarrowsalongeachlineagedenotetheperformanceoftheparent
thatwaslocatedatthetailendofthearrowandproducedtheoffspringatarrowhead. Themainconclusionisthatthesteppingstonesthatleadtoa
high-performingeliteataparticularlocationinthefeaturespacearedistributedthroughoutthefeaturespace,suggestingthatMAP-Elites’strategyof
simultaneouslyrewardinghigh-performingorganismsateachpointinthespacemayhelpdiscoverhigh-performingsolutionsinverydifferentregions.
thatcontractandexpandinphase(green,cyclicalvolumetricac- implementedintheSferesv2 60 evolutionaryplatform,whichhas
tuationof20%),andmusclesthatcontractandexpandinopposite somedeparturesfromtheoriginalNEATalgorithm. Specifically,
phase(red,counter-cyclicalvolumetricactuationof20%). ourdirectencodingdoesnotincludecrossoverorgeneticdiver-
The material of each voxel is encoded with a compositional sityviaspeciation. SeeMouretandDoncieux201225 foramore
pattern-producingnetwork(CPPN)53,anencodingbasedonde- detaileddescriptionoftheSferesversionofNEAT.
velopmental biology that causes robot phenotypes to be more Performanceforthesesoftrobotsisdefinedasthedistancecov-
regular and high-performing7,8,11,12,53–57. CPPNs are similar to eredin10simulatedseconds. Thefirst(x-axis)dimensionofthe
neuralnetworks,butwithevolvableactivationfunctions(inthis feature space is the percentage of voxels that are the stiff bone
paper, thefunctionscanbesine, sigmoid, Gaussian, andlinear) (darkblue)material. Thesecondfeature-spacedimensionisthe
thatallowthenetworktocreategeometricpatternsinthepheno- percentageofvoxelsfilled.Theresolutionofthemapis128×128.
typestheyencode. Becausetheseactivationfunctionsareregu- Welaunched10runsforeachtreatment,butsomehadnotcom-
larmathematicalfunctions,thephenotypesproducedbyCPPNs pletedintimetobeincludedinthisdraftofthepaper. Wethus
tend to be regular (e.g. a Gaussian function can create symme- includedataonlyfromrunsthatfinishedinourplotsandstatisti-
tryandasinefunctioncancreaterepetition).CPPNnetworksare calanalyses(7fortheEAtreatment,5fortheEA+Diversitytreat-
genomesthatareruniterativelyforeachvoxelintheworkspace ment,and8fortheMAP-Elitestreatment). Inlaterdraftsofthis
todeterminewhetherthatvoxelisemptyorfulland,iffull,which paperwewillreportonacompletesetoffinishedexperiments,
typeofmaterialispresent. Specifically,foreachvoxel,theCarte- whichwillalsohavealargerandconsistentnumberofrunsper
sian(x,y,andz)coordinatesofthevoxelanditsdistancefromthe treatment.
center(d)areprovidedasinputstotheCPPN,andoneCPPNout- OurtwocontrolalgorithmsareimplementedinNSGA-IIand
putspecifieswhetheravoxelisempty. Ifthevoxelisnotempty, havebeenusedinpreviousstudies25,57:(1)asingle-objectiveevo-
themaximumvalueofanadditionalfouroutputs(oneperma- lutionaryalgorithmoptimizingperformanceonly,whichwerefer
terial type) determines the type of material for that voxel. This to as the “traditional EA” or just “EA” for short, and (2) a two-
method of separating the presence of a phenotypic component objectiveevolutionaryalgorithmthatoptimizesperformanceand
anditsparametersintoseparateCPPNoutputshasbeenshown diversity, which we call EA+D. Diversity is measured for each
to improve performance58,59. If there are multiple disconnected individual as the average distance in the feature space to every
voxel patches, only the most central patch is considered as the other individual. Both control treatments performed the same
robot morphology. A lengthier explanation of CPPNs and how numberofevaluationsasMAP-Elites.
they specify the voxels of the soft robots in this domain can be Inthisdomain,MAP-Elitesdoesafarbetterjobthanthecon-
found in Cheney et al. 20138, from which some text in this de- trols of revealing the fitness potential of each area of the fea-
scriptionofmethodswasderived. turespace, whichisthegoalofilluminationalgorithms(Fig.5).
While the soft robot morphologies are indirectly encoded by It has significantly higher reliability and coverage (p < 0.002),
CPPNs,theCPPNnetworksthemselvesaredirectlyencodedand andexamplemapshighlightthetremendousdifferenceinterms
evolvedaccordingtotheprinciplesoftheNEATalgorithm20,asis ofexploringthefeaturespacebetweentheMAP-Elitesillumina-
customaryforCPPNs7,8,11,12,53–56. Here,theNEATprinciplesare tionalgorithmandthetwocontroloptimizationalgorithms,even
MouretandClune arXiv | 8


---

## Page 9

thoughonehasadiversitypressure. gorithmstolearnofthishigh-performingregionofthespace,but
Intermsofglobalperformance,whileMAP-Eliteshasahigher withMAP-Elitesitjumpsoutvisuallyineachmap. Evenwithin
medianvalue,thereisnosignificantdifferencebetweenitandthe this island, we can still see smooth gradients in the desired di-
othertreatments(p>0.05).Ifonecaredonlyaboutfindingasin- mensionsofvariation,startingwithsheetsmadeentirelyofmus-
gle, high-performingsolution, thentherewouldthusbenosta- cleandtransitioningtosheetsmademostlyofbone. Spacecon-
tisticaldifferencebetweenMAP-Elitesandthetwooptimization straintspreventshowingallofthefinalelites,butweconsistently
algorithmcontrols.However,ifonewantedavarietyofdifferent, observedthatonecanstartinnearlyanylocationofthemapand
high-performingsolutions,MAP-Elitesproducesfarmore. smoothlyvarythedesignsfoundthereinanydirection.Asecond
MAP-Elitesissignificantlyworseatprecisionthanthetwocon- examplemapisprovided(Fig.6,Bottom)toshowthatthesefind-
trolalgorithms(p < 0.01). Thisresultislikelyexplainedbythe ingsarenotlimitedtoonerunofMAP-Elites,butareconsistently
factthatthecontrolalgorithmsallocatealloftheirevaluationsto found in each map: while the actual design themes are differ-
very few cells, and thus find good solutions for those cells. In entfrommaptomap,thefactthatMAP-Elitesprovidessmooth
contrast, MAP-Elites has to distribute its evaluations across or- changesinthesethemesaccordingtothedesireddimensionsof
ders of magnitude more cells, making it hard to always find a variationsisconsistent.
high-performing solution in each cell. Note that MAP-Elites is
usuallycompetingagainstitselfinthisregard:becausethereisso 6.3 Realsoftrobotarm
little exploration by the control algorithms, they rarely produce
thehighest-performingsolutionacrossallrunsofalltreatments Whiletheprevioussectionfeaturedsimulatedsoftrobots,inthis
foraparticularcell.ThoseinsteadtendtocomefromMAP-Elites. sectionwetestwhetherMAP-Elitescanhelpfindcontrollersfor
Thus,mostlowprecisionscoresforMAP-Elitescomewhenone areal,physical,softrobotarm. Thephysicsofthisarmarequite
runofMAP-Elitesdoesnotfindashigh-performingasolutionin complicatedanddifficulttosimulate,makingitnecessarytoper-
acellasanotherrunofMAP-Elites. Wehypothesizethatifeach form all evaluations on the real robot. That limits the number
runofMAP-Elitesweregivenmoreevaluations(i.e. runlonger), of evaluations that can be performed, requiring a small feature
itwouldcatchupto,ifnotsurpass,thecontrolsinprecision.That space. ThisdomainthusdemonstratesthatMAP-Elitesiseffec-
isabeneficial, andrare, propertyforanevolutionaryalgorithm tive even on a challenging, real-world problem with expensive
tohave: thatitcanbenefitfromadditionalcomputationbecause evaluationsandasmallfeaturespace.
itdoesnotgetstuckonlocaloptimaandceasetoinnovate. We built a soft robotic arm (Fig. 7) by connecting 3 actuated
Thereisvarianceinthemapsproducedbyindependentruns joints (dynamixel AX-18 servos) with highly compliant tubes
ofMAP-Elites. Thatreflectsthefactthatitisastochasticsearch (made of flexible, washing machine drain pipes). An external
algorithm with historical contingency. The perfect illumination cameratrackedaredpointattheendofthearm. Asolutionis
algorithmwouldalwaysfindthehighest-performingsolutionat a set of 3 numbers specifying the angle of each of the 3 joints.
eachpointinthemap, andthushavenobetween-runvariance. Specifically, each servo can move between -150 and +150 steps
However,whiletherearedifferencesbetweenthemapsofdiffer- (out of the possible range for AX-18s of -512 and + 512 steps,
entruns,theylargelyrevealthesameoverallpattern(Figs.5and whichcoversall360degreesofrotation). Whenthearmisfully
6). extendedandhorizontal,thefirstservofromthebaseisatposi-
Bylookingatpicturesandvideosoftheelitesinthefinalmap tion150,andtheothertwoareatposition0.
ofindividualruns,weobservedthatMAP-Elitesdoesindeedpro- The feature space is one-dimensional: the x-value of the red
ducesmoothchangesacrossthechosendimensionsofvariation circleattheendofthearm(inthecoordinatesoftheimagefrom
(Fig. 6). Consider the column of examples from the right side theperspectiveofthecamera). Itisdiscretizedinto64cells. The
ofFig.6,Top,wherethepercentofvoxelsfilledisroughly75%. performancefunctionistomaximizethey-valueoftheendofthe
Startingatthebottom, witharound10%bone, thereisadesign arm.Theexperimentsthusattempttodiscovertheboundariesof
witharedmusclehindleg,greenmusclefrontleg,andnobone theworkspaceoftherobot,whichishardtocomputeanalytically
inthebackconnectingtheselegs(insteadthereislightbluesoft withaflexiblerobot.
tissue).Sweepingupinthatcolumn,thepercentageofboneisin- WeevaluatedMAP-Elitesandtwocontrols: randomsampling
creased,predominantlyinthebackconnectingthelegs,andthe andatraditionalgridsearchalgorithm. Intherandomsampling
softtissueandamountofmuscleineachlegisreducedtogradu- control, each solution is determined by randomly choosing an
allyincreasetheamountofdarkbluebone.Thesesamecreatures angle for each joint in the allowable range. The grid search al-
visualizedfromtheside(rightmostcolumnofimagesinFig. 6, gorithmspecifies, foreachjoint, eightpointsevenlydistributed
Top)showsthatthebasicbipedlocomotionpatternispreserved withintherangeofallowableanglesforthatjoint,andthentests
despitethesechanges,goingfrom(inthebottom)afast,flexible all combinations of the possible values for each joint. We repli-
biped that resembles a rabbit, to a slow biped creature that re- catedeachexperiment10times,exceptforgridsearch,whichis
semblesaturtlewithamassive,heavyshell. MAP-Elitesisthus adeterministicalgorithmandthusneedonlyberunonce. Each
achievingitsgoalofprovidingtherequestedvariationandpro- MAP-Elitesandrandomsamplingexperimentwereallocated640
ducingahigh-performingsolutionofeachtype. Truetothemo- evaluations;thegridsearchrequired729evaluations(9×9×9).
tivationofilluminationalgorithms22,32,findingthefastest,heavy Theresultsshowthatallthreetreatmentsfindapproximately
shelledturtledoesnotprecludefindingthefastestrabbit: inthis thecorrectboundaryforhighvaluesofx(∼600to∼800).Ourob-
case,theybothcanwintherace. servationsoftherobotrevealedwhythisisarelativelyeasytask:
Fromthesemaps,onecanalsolearnaboutthefitnesspotential thesepointscanbereachedbysettingtheanglesofthefirstand
ofdifferentregionsofthefeaturespace. Forexample,theprevi- secondjoints(countingfromthebase)toputthethirdjointonthe
ousexampleshowedthat,holdingthepercentageofvoxelsfilled ground,andonlychangingtheangleofthisthirdjoint. Because
at75%,themoreboneinacreature,thesloweritis.Thefullmap oftheflexibilityofthelinks,manydifferentcombinationsofan-
revealsthatisgenerallytrueforalmostallbodysizes. Themaps glesforthefirstandsecondjointresultinhavingthewristonthe
alsorevealaninteresting,anomalous,long,skinnyislandofhigh table.
performanceinthecolumnwherethepercentageofvoxelsfilled Intermediate values of x (approximately 400-600) represent
isroughly7%. Itturnsoutthatcolumncontainsavarietyofdif- harderproblems,becauseinthisrangetherearefewerjointangle
ferent solutions that are all one voxel wide. Some quirk of the values that combine to reach near the maximum height. MAP-
simulatorallowstheseverticalsheetorganismstoperformbetter Elitesoutperformsbothgridsearchandrandomsamplinginthis
thancreaturesthataremorethanonevoxelwide. Itmighttake region.Evenwhentheyareattheirbest,MAP-Elitestendstoout-
hundredsorthousandsofrunswithtraditionaloptimizational- performthesealgorithms. Foreachcontrolalgorithm, thereare
MouretandClune arXiv | 9


---

## Page 10

Global performance Reliability Precision Coverage
0.075
1.0 1.0 1.0
0.070
0.8 0.8 0.8
0.065
0.6 0.6 0.6
0.060
0.4 0.4 0.4
0.055
0.050 0.2 0.2 0.2
0.045 0.0 0.0 0.0
E A E A + D
M A
P- Elit e s E A E A + D
M A
P- Elit e s E A E A + D
M A
P- Elit e s E A E A + D
M A
P- Elit e s
0.064 0.064 0.064
1.2 1.2 1.2
0.056 0.056 0.056
1.0 0.048 1.0 0.048 1.0 0.048
0.8 0.040 0.8 0.040 0.8 0.040
0.6 0.032 0.6 0.032 0.6 0.032
0.024 0.024 0.024
0.4 0.4 0.4
0.016 0.016 0.016
0.2 0.2 0.2
0.008 0.008 0.008
0.0 0.2 0.4 0.6 0.8 1.0 1.2 0.000 0.0 0.2 0.4 0.6 0.8 1.0 1.2 0.000 0.0 0.2 0.4 0.6 0.8 1.0 1.2 0.000
0.064 0.064 0.064
1.2 1.2 1.2
0.056 0.056 0.056
1.0 0.048 1.0 0.048 1.0 0.048
0.8 0.040 0.8 0.040 0.8 0.040
0.6 0.032 0.6 0.032 0.6 0.032
0.024 0.024 0.024
0.4 0.4 0.4
0.016 0.016 0.016
0.2 0.2 0.2
0.008 0.008 0.008
0.0 0.2 0.4 0.6 0.8 1.0 1.2 0.000 0.0 0.2 0.4 0.6 0.8 1.0 1.2 0.000 0.0 0.2 0.4 0.6 0.8 1.0 1.2 0.000
(a)EA (b)EA+D (c)MAP-Elites
Fig.5.MAP-Elitesdoesmuchbetterthanatraditionalevolutionaryalgorithm(EA)andanEAwithdiversity(EA+D)atfindinghigh-performingsolutions
throughoutafeaturespace. Dataarefromthesimulated,softrobotmorphologiesproblemdomain. Top: MAP-Elitessignificantlyoutperformsthe
controlsinglobalreliabilityandcoverage(top, p < 0.002). Bottom: Qualitatively, examplemapsproducedbytwoindependentrunsdemonstrate
MAP-Elites’abilitytobothfillcells(coverage)andrevealthefitnesspotentialofdifferentareasofthefeaturespace.Notethedifferenceinfeature-space
explorationbetweentheMAP-Elitesilluminationalgorithmandtheoptimizationalgorithms.
valuesinthisregionweretheirperformanceisespeciallypoor. 7 Discussion and Conclusion
Thispaperintroducestheterm“illuminationalgorithms”forthe
Lower values of x represent even harder challenges. Grid classofalgorithmsthattrytofindthehighest-performingsolu-
search found only a few points below 500, and thus provides a tion at each point in a user-defined feature space. It also intro-
less-informative(lower-resolution)picturethanMAP-Elitesdoes. ducesanewilluminationalgorithmcalledMAP-Elites,whichis
Tohavegoodcoverageofthislow-x-valueregion(200-500), we simplertoimplementandunderstandthanpreviousillumination
would need to significantly increase the resolution (discretiza- algorithms, namely Novelty Search + Local Competition22 and
tion) of grid search, which would require exponentially more MOLE32. Finally,thepaperpresentspreliminaryevidenceshow-
evaluations. Therarityofhigh-performingsolutionsinthispart ing that MAP-Elites tends to perform significantly better than
of the feature space results in even lower performance for ran- control algorithms, either illumination algorithms or optimiza-
dom sampling. MAP-Elites, in contrast, provides many high- tionalgorithms,onthreedifferentproblemdomains. Becauseof
performing solutions for all values of x. These data are still thepreliminarynatureoftheexperimentaldata,wedonotwish
toopreliminarytoprovidereliablestatisticalresults,butweplot forreadersatthispointtoconcludeanythingforcertainyetabout
themtoshowwhatweknowtodateaboutMAP-Elitesandthe MAP-Elites’ empirical performance, but in many cases the data
controlsinthisproblemdomain. suggest that MAP-Elites is a promising new illumination algo-
MouretandClune arXiv | 10


---

## Page 11

rithmthatoutperformspreviousones. biasing towards cells who have empty adjacent cells, cells
Perhapsthebestwaytounderstandthebenefitsofillumination nearlow-performingareas,cellsnearhigh-performingareas,
algorithmsversusoptimizationalgorithmsistoviewthefeature etc.Inpreliminaryexperiments,suchbiasesdidnotperform
maps from the simulated soft robot domain (Fig. 5). Optimiza- betterthanthedefaultMAP-Elites.
tionalgorithmsmayreturnahighperformingsolution,butthey
• Including crossover. Crossover may be especially effective
donotteachusabouthowkeyfeaturesofasearchspacerelate
when restricted to occurring between organisms nearby in
to performance. MAP-Elites and other illumination algorithms,
thefeaturespace. Doingsoallowsdifferentcompetingcon-
in contrast, map the entire feature space to inform users about
ventionsinthepopulation(e.g.tall,skinnyorganismsbeing
whatispossibleandthevarioustradeoffsbetweenfeaturesand
crossedoveronlywithothertall,skinnyorganisms,andthe
performance. Such phenotype-fitness maps, as they are known
in biology38, are interesting in their own right, and can also be same for short, fat organisms). One could make crossover
only occur within a certain radius of an individual or as
puttopracticaluse.Forexample,arecentpapershowedthatthe
a probabilistic function of the distance between organisms
mapcanprovidearepertoireofdifferent,high-performingsolu-
(leadingtooverlappingcrossoverzones),oronlywithincer-
tionthatcaninitiatesearchfornewbehaviorsincaseanoriginal
tainregions(moreakintoanislandmodel). Notethateven
behavior no longer works (e.g. if a robot becomes damaged or
findsitselfinanewenvironment)6. withgeographicallyrestrictedcrossover,offspringcouldstill
endupindifferentareasofthefeaturespacethantheirpar-
MAP-Elitesisalsoapowerfuloptimizationalgorithm,putting
ents(eitherduetotheeffectsofmutationorcrossover).
asideitsadditionalbenefitsregardingilluminatingfeatureland-
scapes. It significantly outperformed or matched control algo-
rithms according to the narrow question of which algorithm 9 Methods
foundthesingle,highest-performingsolutionineachrun.Asdis-
cussedabove,thatcouldbebecausesimultaneouslysearchingfor 9.1 Statistics
amultitudeofdifferent,relatedsteppingstonesmaybeamuch
Thestatisticaltestforallpvaluesisatwo-tailedMann-Whitney
better way to reach any individual stepping stone than directly
searchingonlyforasolutiontothatsteppingstone37. Utest.
For a similar reason, illumination algorithms like MAP-Elites
mayhelpevolutionaryalgorithmsmoveclosertotheopen-ended 9.2 Hierarchical,ParallelizedMAP-Elites
evolution seen in the natural world, which produced a tremen-
Tofirstencourageacourse-grainedsearch,andthenallowforin-
dous diversity of organisms (within one run). In nature, there
creased granularity, we created a hierarchical version of MAP-
are a multitude of different niches, and a species being good in
Elites. Itstartswithlargercellsandthensubdividesthosecells
onenichedoesnotprecludeadifferentspeciesfrombeinggood
over time. In this hierarchical version of MAP-Elites, the sizes
in another: i.e., that bears are stronger does not crowd out the
ability for butterflies to flourish in their own way22. By simul- of cells shrink during search, and thus the range of differences
infeaturesthatanorganismcompeteswithchanges,althoughit
taneouslyrewardingamultitudeofdifferenttypesofcreatures,
isboundedtowithinacell: competitionisthusstillrestrictedto
MAP-Elitescapturessomeofthatdiversity-creatingforceofna-
solutionswithsimilarfeatures.
ture. OnedrawbacktoMAP-Elites, however, isthatitdoesnot
TomakeMAP-Elitesrunfasteronasupercomputercontaining
allow the addition of new types of cells over time that did not
manynetworkedcomputers, wecreatedabatched, parallelized
existinthe originalfeaturespace. Itthus, by definition, cannot
versionofhierarchicalMAP-Elites. Itfarmsoutbatchesofeval-
exhibit open-ended evolution. Nature, in contrast, creates new
uationstoslavenodesandreceivesperformancescoresandbe-
niches while filling others (e.g. beavers create new types of en-
havioraldescriptorsbackfromthesenodes. Theseoptimizations
vironmentsthatotherspeciescanspecializeon). Futureworkis
shouldnothaveanyqualitativeeffectontheoverallperformance
requiredtoexplorehowtocreateilluminationalgorithmsthatdo
ofthealgorithm. Alloftheexperimentsinthispaperwerecon-
notjustrevealthefitnesspotentialofapredefinedfeaturespace,
ductedwiththishierarchical,paralleledversionofMAP-Elites.
butthatreportthehighest-performingsolutionsateachpointin
aneverexpandingfeaturespacethatisintelligentlyenlargedover
time. 9.3 Experimentalparameters
Inconclusion,illuminationalgorithms,whichfindthehighest-
Retinaexperiments. 20replicatesforeachtreatment.
performingsolutionateachpointinauser-definedfeaturespace,
TheMAP-Elitesparametersareasfollows:
are valuable new tools to help us learn about complex search
spaces.Theyilluminatethefitnesspotentialofdifferentcombina- • startingsizeofthemap:16×16
tionsoffeaturesofinterest,andtheycanalsoserveaspowerful
• finalsizeofthemap:512×512
optimization algorithms. MAP-Elites represents a simple, intu-
itive,new,promisingilluminationalgorithmthatcanservethese • batchsize:2,000
goals. Italsocapturessomeofthediversitygeneratingpowerof
naturebecauseitsimultaneouslyrewardsthehighest-performing • numberofiterations:10,000
solutionsinamultitudeofdifferentniches.
• initialbatch:20,000
8 Alternate variants of MAP-Elites • resolutionchangeprogram(4changes):
– iteration0:64×64
ThefollowingarealternatewaystoimplementMAP-Elites. Fu-
– iteration1250:128×128
tureresearchisnecessarytoseewhether,andonwhichtypesof
problems,anyofthesevariantsisconsistentlybetterthanthesim- – iteration2500:256×256
ple,defaultversionofMAP-Elitesusedinthispaper. – iteration5000:512×512
Possiblevariantsofthisalgorithminclude:
• feature1:connectioncost(see32)
• Storing more than one genome per feature cell to promote
diversity • feature2:networkmodularity(see32)
• Biasingthechoiceofwhichcellsproduceoffspring,suchas • performance:percentanswerscorrectonretinaproblem32
MouretandClune arXiv | 11


---

## Page 12

Soft robots experiments. The MAP-Elites parameters are as WethendefinetheglobalreliabilityG(m)ofamapmasfollows:
follows:
1 (cid:88) m(x,y)
• feature1:percentageofbones G(m)= n(M) M(x,y)
x,y
• feature2:percentageofvoxelsfilled
where x,y ∈ {[x min ,··· ,x max ;y min ,··· ,y max ]}, and n(M) is
• performance:covereddistance thenumberofnon-zeroentriesinM (i.e. thenumberofunique
cellsthatwerefilledbyanyrunfromanytreatment).
• startingresolution:64×64
• finalresolution:128×128 9.4.2 Precision(opt-inreliability)
• batchsize:1024 Sameasglobalreliability,butforeachrun,thenormalizedperfor-
manceisaveragedonlyforthecellsthatwerefilledbythatalgo-
• initialbatch:4096 rithminthatrun.Thismeasureaddressesthefollowingquestion:
whenacellisfilled,howhigh-performingisthesolutionrelative
• iterations:1400
towhatispossibleforthatcell?
Mathematically, the opt-in reliability, or precision, P(m) of a
Soft physical arm. 10replicatesforeachtreatmentexceptfor mapmis:
thegridsearch,whichisdeterministicandthusrequiresonlyone 1 (cid:88) m(x,y)
P(m)=
run. n(m) M(x,y)
x,y
Forthegridsearch:
• totalnumberofevaluations:512 for x,y ∈ {[x min ,··· ,x max ;y min ,··· ,y max ]|filledm (x,y)=1},
wherefilledm (x,y)isabinarymatrixthathasa1inan(x,y)cell
• discretizationoftheparameters:8steps ifthealgorithmproducedasolutioninthatcelland0otherwise,
andwheren(M)isthenumberofnon-zeroentriesinM (i.e. the
Fortherandomsampling: numberofuniquecellsthatwerefilledbyanyrunfromanytreat-
ment).
• totalnumberofevaluations:420
• wereportthebestsolutionfoundineachofthe64cellsused 9.4.3 Coverage
byMAP-Elites
For a map m produced by one run of one algorithm, we count
ForMAP-Elites:
thenumberofnon-empty(i.e.filled)cellsinthatmapanddivide
• totalnumberofevaluations:420 bythetotalnumberofcellsthattheoreticallycouldbefilledgiven
thedomain(i.e.forwhichagenomeexistsinthesearchspacethat
• feature1:xcoordinate mapstothatfeature-spacecell). Unfortunately,wedonotknow
thistotalnumberofcellsthattheoreticallycouldbefilledforthe
• fitness:maximizeheight(ycoordinate)
experimentaldomainsinthispaper.Weapproximatethisnumber
bycountingthenumberofuniquecellsthathavebeenfilledby
• startingresolution:64
anyrunfromanytreatment. Usingthenotationoftheprevious
• finalresolution:64 twosections,thisnumberisn(F M ),whereF M =filledM.
• batchsize:10
10 References
• initialbatch:120
• iterations:30
1. S.J.Russell,P.Norvig,J.FCanny,J.M.Malik,andD.D.Edwards.
Artificialintelligence:amodernapproach,volume74.Prenticehall
9.4 Quantifiablemeasurementsofalgorithmquality EnglewoodCliffs,1995.
2. D. Floreano and C. Mattiussi. Bio-inspired artificial intelligence:
The notation in this section assumes a two-dimensional feature theories,methods,andtechnologies. TheMITPress,2008.
map(xandy),butcanbegeneralizedtoanynumberofdimen- 3. J.R.Koza,MartinAKeane,MatthewJStreeter,WilliamMydlowec,
sions. Jessen Yu, and Guido Lanza. Genetic programming IV: Routine
human-competitivemachineintelligence. Kluwer,2003.
4. G.S. Hornby, J.D. Lohn, and D.S. Linden. Computer-automated
9.4.1 Globalreliability evolutionofanx-bandantennafornasa’sspacetechnology5mis-
sion. EvolutionaryComputation,19(1):1–23,2011.
Measureshowclosethehighestperformingsolutionfoundbythe 5. M. Schmidt and H. Lipson. Distilling free-form natural laws from
algorithmforeachcellinthemapistothehighestpossibleper- experimentaldata. science,324(5923):81–85,2009.
formanceforthatcell,averagedoverallcellsinthemap.Because 6. A.Cully,J.Clune,D.Tarapore,andJ-B.Mouret. Robotsthatcan
adaptlikenaturalanimals. arXiv,1407.3501,2015.
wedonotknowthehighestperformancepossibleforeachcell,
7. J. Clune, K.O. Stanley, R.T. Pennock, and C. Ofria. On the per-
weapproximateitbysettingitequaltothehighestperformance formanceofindirectencodingacrossthecontinuumofregularity.
foundforthatcellbyanyrunofanyalgorithm. Cellsthathave IEEE Transactions on Evolutionary Computation, 15(4):346–367,
neverbeenfilledbyanyalgorithmareignored.Ifanalgorithmin 2011.
8. N. Cheney, R. MacCurdy, J. Clune, and H. Lipson. Unshackling
arundoesnotproduceasolutioninacell, theperformancefor
evolution:Evolvingsoftrobotswithmultiplematerialsandapower-
thatalgorithmforthatcellissetto0becausethealgorithmfound
fulgenerativeencoding. InProceedingsoftheGeneticandEvolu-
zeropercentofthatcell’spotential. tionaryComputationConference,pages167–174,2013.
WefirstdefineM x,yasthebestsolutionfoundacrossallrunsof 9. G.S. Hornby, S. Takamura, T. Yamamoto, and M. Fujita. Au-
alltreatmentsatcoordinatesx,y. IfM=m 1 ,··· ,m k isavector tonomous evolution of dynamic gaits with two quadruped robots.
IEEETransactionsonRobotics,21(3):402–410,2005.
containingthefinalmapfromeveryrunofeverytreatment,then
10. S Doncieux, N Bredeche, J Mouret, and A Eiben. Evolutionary
robotics: What, why, andwhereto. Name: FrontiersinRobotics
M = max m (x,y)
x,y i andAI,2(4),2015.
i∈[1,···,k]
MouretandClune arXiv | 12


---

## Page 13

11. J.Yosinski,J.Clune,D.Hidalgo,S.Nguyen,J.C.Zagal,andH.Lip- learning. InProceedingsoftheGeneticandEvolutionaryCompu-
son. Evolving robot gaits in hardware: the hyperneat generative tationConference,2015.
encodingvs.parameteroptimization. InProceedingsoftheEuro- 38. James J Bull, Richard H Heineman, and Claus O Wilke. The
peanConferenceonArtificialLife,pages890–897,2011. phenotype-fitnessmapinexperimentalevolutionofphages. PLoS
12. S. Lee, J. Yosinski, K. Glette, H. Lipson, and J. Clune. Evolving One,6(11):e27796,2011.
gaits for physical robots with the hyperneat generative encoding: 39. K.O.StanleyandR.Miikkulainen.Ataxonomyforartificialembryo-
thebenefitsofsimulation. InApplicationsofEvolutionaryComput- geny. ArtificialLife,9(2):93–130,2003.
ing.Springer,2013. 40. G.S.Hornby,H.Lipson,andJ.B.Pollack. Generativerepresenta-
13. J.Clune,B.E.Beckmann,C.Ofria,andR.T.Pennock.Evolvingco- tionsfortheautomateddesignofmodularphysicalrobots. IEEE
ordinatedquadrupedgaitswiththeHyperNEATgenerativeencod- TransactionsonRoboticsandAutomation,19(4):703–719,2003.
ing.InProceedingsoftheIEEECongressonEvolutionaryCompu- 41. G.S.HornbyandJ.B.Pollack.Creatinghigh-levelcomponentswith
tation,pages2764–2771,2009. agenerativerepresentationforbody-brainevolution. ArtificialLife,
14. AntoineCullyandJ-BMouret. Evolvingabehavioralrepertoirefor 8(3):223–246,2002.
awalkingrobot. Evolutionarycomputation,2015. 42. G.S.Hornby. Functionalscalabilitythroughgenerativerepresenta-
15. H.LipsonandJ.B.Pollack. Automaticdesignandmanufactureof tions:theevolutionoftabledesigns. EnvironmentandPlanningB,
roboticlifeforms. Nature,406(6799):974–978,2000. 31(4):569–588,2004.
16. K.Deb. Multi-objectiveoptimizationusingevolutionaryalgorithms, 43. Jerome H Friedman, Jon Louis Bentley, and Raphael Ari Finkel.
volume16. Wiley,2001. Analgorithmforfindingbestmatchesinlogarithmicexpectedtime.
17. J. Clune, S. Goings, B. Punch, and E. Goodman. Investigations ACM Transactions on Mathematical Software (TOMS), 3(3):209–
in meta-gas: panaceas or pipe dreams? In Proceedings of the 226,1977.
Genetic and Evolutionary Computation Conference Workshops, 44. N.KashtanandU.Alon. Spontaneousevolutionofmodularityand
pages235–241.ACM,2005. networkmotifs.ProceedingsoftheNationalAcademyofSciences,
18. A´goston E Eiben, Robert Hinterding, and Zbigniew Michalewicz. 102(39):13773,2005.
Parametercontrolinevolutionaryalgorithms.EvolutionaryCompu- 45. E.A.LeichtandM.E.J.Newman.Communitystructureindirected
tation,IEEETransactionson,3(2):124–141,1999. networks. Physicalreviewletters,pages118703–118707,2008.
19. J. Clune, D. Misevic, C. Ofria, R.E. Lenski, S.F. Elena, and 46. Deepak Trivedi, Christopher D Rahn, William M Kier, and Ian D
R. Sanjua´n. Natural selectionfails to optimize mutation rates for Walker. Softrobotics: Biologicalinspiration, stateoftheart, and
long-termadaptationonruggedfitnesslandscapes.PLoSCompu- futureresearch. AppliedBionicsandBiomechanics,5(3):99–117,
tationalBiology,4(9):e1000187,2008. 2008.
20. K.O. Stanley and R. Miikkulainen. Evolving neural networks 47. FilipIlievski,AaronD.Mazzeo,RobertF.Shepherd,XinChen,and
through augmenting topologies. Evolutionary Computation, George M. Whitesides. Soft robotics for chemists. Angewandte
10(2):99–127,2002. Chemie,123(8):1930–1935,2011.
21. J. Lehman and K.O. Stanley. Abandoning objectives: Evolution 48. HodLipson. Challengesandopportunitiesfordesign,simulation,
through the search for novelty alone. Evolutionary Computation, andfabricationofsoftrobots. SoftRobotics,1(1):21–27,2014.
19(2):189–223,2011. 49. Cecilia Laschi, Matteo Cianchetti, Barbara Mazzolai, Laura
22. J.LehmanandK.O.Stanley. Evolvingadiversityofvirtualcrea- Margheri, MaurizioFollador, andPaoloDario. Softrobotarmin-
turesthroughnoveltysearchandlocalcompetition.InProceedings spiredbytheoctopus.AdvancedRobotics,26(7):709–727,2012.
ofthe13thannualconferenceonGeneticandevolutionarycompu- 50. A. Bicchi and G. Tonietti. Fast and ”soft-arm” tactics [robot arm
tation,pages211–218.ACM,2011. design]. RoboticsAutomationMagazine,IEEE,11(2):22–33,June
23. J.LehmanandK.O.Stanley. Noveltysearchandtheproblemwith 2004.
objectives.InGeneticProgrammingTheoryandPracticeIX,pages 51. J.HillerandH.Lipson. Automaticdesignandmanufactureofsoft
37–56.Springer,2011. robots. Robotics,IEEETransactionson,28(2):457–466,2012.
24. J.LehmanandK.O.Stanley. Exploitingopen-endednesstosolve 52. JonathanHillerandHodLipson. Dynamicsimulationofsoftmulti-
problemsthroughthesearchfornovelty.InProceedingsofArtificial material3d-printedobjects. SoftRobotics,1(1):88–101,2014.
LifeXI,volume11,pages329–336,2008. 53. K.O.Stanley. Compositionalpatternproducingnetworks: Anovel
25. J.-B.MouretandS.Doncieux. Encouragingbehavioraldiversityin abstractionofdevelopment. GeneticProgrammingandEvolvable
evolutionaryrobotics: anempiricalstudy. EvolutionaryComputa- Machines,8(2):131–162,2007.
tion,1(20),2012. 54. K.O.Stanley,D.B.D’Ambrosio,andJ.Gauci. Ahypercube-based
26. DarrellWhitley,SorayaRana,andRobertBHeckendorn. Theis- encoding for evolving large-scale neural networks. Artificial life,
landmodelgeneticalgorithm:Onseparability,populationsizeand 15(2):185–212,2009.
convergence. JournalofComputingandInformationTechnology, 55. J.GauciandK.O.Stanley. Autonomousevolutionoftopographic
7:33–48,1999. regularities in artificial neural networks. Neural Computation,
27. Joel Lehman and Kenneth O Stanley. Revising the evolutionary 22(7):1860–1898,2010.
computationabstraction: minimalcriterianoveltysearch. InPro- 56. Nicholas Cheney, Jeff Clune, and Hod Lipson. Evolved electro-
ceedingsofthe12thannualconferenceonGeneticandevolution- physiologicalsoftrobots.InALIFE14:TheFourteenthConference
arycomputation,pages103–110.ACM,2010. on the Synthesis and Simulation of Living Systems, volume 14,
28. G. Cuccu and F. Gomez. When novelty is not enough. In Ap- pages222–229,2014.
plicationsofEvolutionaryComputation,pages234–243.Springer, 57. D.TaraporeandJ.-B.Mouret. Evolvabilitysignaturesofgenerative
2011. encodings: beyondstandardperformancebenchmarks. Informa-
29. Gomes J., Mariano P., and A. L. Christensen. Devising effective tionSciences,pagetoappear,2015.
novelty search algorithms: a comprehensive empirical study. In 58. PhillipVerbancsicsandKennethOStanley. Constrainingconnec-
ProceedingsoftheGeneticandEvolutionaryComputationConfer- tivitytoencouragemodularityinhyperneat. InProceedingsofthe
ence,2015. 13thannualconferenceonGeneticandevolutionarycomputation,
30. Jean-BaptisteMouret. Novelty-basedmultiobjectivization. InNew pages1483–1490.ACM,2011.
horizonsinevolutionaryrobotics,pages139–154.Springer,2011. 59. J.Huizinga,J-B.Mouret,andJ.Clune. Evolvingneuralnetworks
31. Benjamin Inden, Yaochu Jin, Robert Haschke, Helge Ritter, and thatarebothmodularandregular: Hyperneatplustheconnection
BernhardSendhoff.Anexaminationofdifferentfitnessandnovelty cost technique. In Proceedings of the Genetic and Evolutionary
basedselectionmethodsfortheevolutionofneuralnetworks. Soft ComputationConference,pages697–704,2014.
Computing,17(5):753–767,2013. 60. Jean-Baptiste Mouret and Ste´phane Doncieux. Sferesv2:
32. J.Clune,J-B.Mouret,andH.Lipson. Theevolutionaryoriginsof Evolvin’inthemulti-coreworld. InIEEECongressonEvolutionary
modularity. ProceedingsoftheRoyalSocietyB,280(20122863), Computation,2010.
2013.
33. JoshuaBTenenbaum,VinDeSilva,andJohnCLangford.Aglobal
geometricframeworkfornonlineardimensionalityreduction. Sci- 11 Acknowledgements
ence,290(5500):2319–2323,2000.
34. S.Haykin. NeuralNetworks:AComprehensiveFoundation. Pren- ThankstoRobyVelez,AnhNguyen,andJoostHuizingaforhelp-
ticeHall,2ndedition,1998.
fuldiscussionsandcommentsonthemanuscript.
35. TeuvoKohonen. Self-organizingmaps,volume30. SpringerSci-
ence&BusinessMedia,2001.
36. David F Andrews. Plots of high-dimensional data. Biometrics,
pages125–136,1972.
37. A. Nguyen, J. Yosinski, and J. Clune. Innovation engines: Au-
tomated creativity and improved stochastic optimization via deep
MouretandClune arXiv | 13


---

## Page 14

enob
%
% voxels filled
ssentfi
used in arXiv
triped triped triped
Same orgs,
bipeds
from the side
two-arm
jumper biped biped biped
crawler
enob
%
% voxels filled
ssentfi
used in arXiv
3-legged triped
(muscle legs) 3-legged triped
(muscle legs)
Fig. 6. Example maps annotated with example organisms from different areas of the feature space. Within a map, MAP-Elites smoothly adapts
a design theme along the desired dimensions of variation. Between maps, one can see that there is some variation between maps, both in the
performancediscoveredatspecificpoints,andinthetypesofsolutionsdiscovered.Thatsaid,ingeneraleachmapgenerallypaintsthesameoverall
pictureoftheperformancecapabilitiesofeachregionofthefeaturespace.Notethedifferentscaleofthebottomcolormap.Additionalexamplemaps
areshowninFig.5.Becausevideosdoabetterjobofrevealingthesimilarityanddifferencesintheseorganisms,bothintheirbodyandtheirbehavior,
afuturedraftofthepaperwillincludeavideooftheseindividuals.
MouretandClune arXiv | 14


---

## Page 15

Global performance Reliability Precision Coverage
800
1.0 1.0 1.0
780
760 0.8 0.8 0.8
740
720 0.6 0.6 0.6
700
0.4 0.4 0.4
680
660
0.2 0.2 0.2
640
620 0.0 0.0 0.0
Gri d
R a
s
n
e
d
a
o
r c m h s a m pli n g M A P- Elit e s Gri d
R a
s
n
e
d
a
o
r c m h s a m pli n g M A P- Elit e s Gri d
R a
s
n
e
d
a
o
r c m h s a m pli n g M A P- Elit e s Gri d
R a
s
n
e
d
a
o
r c m h s a m pli n g M A P- Elit e s
Fig.7. Onareal,softrobot,MAP-Elitesconsistentlyfindshigh-performingsolutions(higheryvalues)acrossthefeaturespace(differentxvalues)
thancontrols.
MouretandClune arXiv | 15