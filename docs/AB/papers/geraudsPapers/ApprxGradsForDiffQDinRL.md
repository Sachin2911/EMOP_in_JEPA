# ApprxGradsForDiffQDinRL



---

## Page 1

Approximating Gradients for Differentiable Quality Diversity in
Reinforcement Learning
BryonTjanaka MatthewC.Fontaine
UniversityofSouthernCalifornia UniversityofSouthernCalifornia
LosAngeles,California,USA LosAngeles,California,USA
tjanaka@usc.edu mfontain@usc.edu
JulianTogelius StefanosNikolaidis
NewYorkUniversity UniversityofSouthernCalifornia
Brooklyn,NewYork,USA LosAngeles,California,USA
julian@togelius.com nikolaid@usc.edu
ABSTRACT
Considertheproblemoftrainingrobustlycapableagents.Oneap-
proachistogenerateadiversecollectionofagentpolices.Training
canthenbeviewedasaqualitydiversity(QD)optimizationprob- Sample coefficients Branch solutions
lem,wherewesearchforacollectionofperformantpoliciesthat
arediversewithrespecttoquantifiedbehavior.Recentworkshows
thatdifferentiablequalitydiversity(DQD)algorithmsgreatlyaccel-
erateQDoptimizationwhenexactgradientsareavailable.However, ES TD3 Train TD3 critic from
agentpoliciestypicallyassumethattheenvironmentisnotdiffer- Approximate experience Evaluate policies
entiable.ToapplyDQDalgorithmstotrainingagentpolicies,we in environment
mustapproximategradientsforperformanceandbehavior.Wepro-
posetwovariantsofthecurrentstate-of-the-artDQDalgorithm
thatcomputegradientsviaapproximationmethodscommonin
reinforcementlearning(RL).Weevaluateourapproachonfoursim-
Update Insert solutions into
ulatedlocomotiontasks.Onevariantachievesresultscomparable and MAP-Elites Archive
tothecurrentstate-of-the-artincombiningQDandRL,whilethe
otherperformscomparablyintwolocomotiontasks.Theseresults Figure1:WedeveloptwoRLvariantsoftheCMA-MEGAal-
provideinsightintothelimitationsofcurrentDQDalgorithmsin gorithm.SimilartoCMA-MEGA,thevariantssamplegradi-
domainswheregradientsmustbeapproximated.Sourcecodeis entcoefficients𝒄andbrancharoundasolutionpoint𝝓∗.We
availableathttps://github.com/icaros-usc/dqd-rl evaluateeachbranchedsolution𝝓𝑖 ′aspartofapolicy𝜋
𝝓𝑖 ′
and
CCSCONCEPTS
insert 𝝓𝑖 ′ into the archive. We then update 𝝓∗ and N(𝝁,𝚺)
to maximize archive improvement. Our RL variants differ
•Computingmethodologies→Reinforcementlearning;Evo- fromCMA-MEGAbyapproximatinggradientswithESand
lutionaryrobotics. TD3,sinceexactgradientsareunavailableinRLsettings.
KEYWORDS
1 INTRODUCTION
qualitydiversity,reinforcementlearning,neuroevolution
Wefocusontheproblemofextendingdifferentiablequalitydiver-
ACMReferenceFormat: sity(DQD)toreinforcementlearning(RL)domains.Wepropose
BryonTjanaka,MatthewC.Fontaine,JulianTogelius,andStefanosNiko- toapproximategradientsfortheobjectiveandmeasurefunctions,
laidis.2022.ApproximatingGradientsforDifferentiableQualityDiversity resultingintwovariantsoftheDQDalgorithmCMA-MEGA[19].
inReinforcementLearning.InGeneticandEvolutionaryComputationCon- Considerahalf-cheetahagent(Fig.2)trainedforlocomotion,
ference(GECCO’22),July9–13,2022,Boston,MA,USA.ACM,NewYork,NY, wheretheagentmustcontinuewalkingforwardevenwhenone
USA,20pages.https://doi.org/10.1145/3512290.3528705 footisdamaged.IfweframethischallengeasanRLproblem,two
approachestodesignarobustlycapableagentwouldbeto(1)de-
signarewardfunctionand(2)applydomainrandomization[47,58].
However,priorwork[8,29]suggeststhatdesigningsuchareward
functionisdifficult,whiledomainrandomizationmayrequireman-
This work is licensed under a Creative Commons Attribution International 4.0 License. uallyselectinghundredsofenvironmentparameters[44,47].
GECCO ’22, July 9–13, 2022, Boston, MA, USA Asanalternativeapproach,considerthatwehaveintuitionon
© 2022 Copyright held by the owner/author(s).
whatbehaviorswouldbeusefulforadaptingtodamage.Forin-
ACM ISBN 978-1-4503-9237-2/22/07.
https://doi.org/10.1145/3512290.3528705 stance,wecanmeasurehowofteneachfootisusedduringtraining,
1102


---

## Page 2

GECCO’22,July9–13,2022,Boston,MA,USA BryonTjanaka,MatthewC.Fontaine,JulianTogelius,andStefanosNikolaidis
andwecanpre-trainacollectionofpoliciesthatarediverseinhow
theagentusesitsfeet.Whenoneoftheagent’sfeetisdamaged
duringdeployment,theagentcanadapttothedamagebyselecting
apolicythatdidnotmovethedamagedfootduringtraining[9,13].
Pre-trainingsuchacollectionofpoliciesmaybeviewedasa Front: 5.8% Back: 96.8%
qualitydiversity(QD)optimizationproblem[9,13,40,49].Formally,
QD assumes an objective function 𝑓 and one or more measure
functions𝒎.ThegoalofQDistofindsolutionssatisfyingalloutput
combinationsof𝒎,i.e.movingdifferentcombinationsoffeet,while
maximizingeachsolution’s𝑓,i.e.walkingforwardquickly.Most Front: 83.9% Back: 11.1%
QDalgorithmstreat𝑓 and𝒎asblackboxes,butrecentwork[19]
proposesdifferentiablequalitydiversity(DQD),whichassumes𝑓 Figure2:Ahalf-cheetahagentexecutingtwowalkingpoli-
and𝒎aredifferentiablefunctionswithexactgradientinformation. cies.Inthetoprow,theagentwalksonitsbackfootwhile
QDalgorithmshavebeenappliedtoproceduralcontentgeneration tappingthegroundwithitsfrontfoot.Inthebottomrow,the
[25],robotics[13,40],aerodynamicshapedesign[22],andscenario agentwalksonitsfrontfootwhilejerkingitsbackfoot.Val-
generationinhuman-robotinteraction[17,18]. uesbeloweachrowshowthepercentageoftimeeachfoot
TherecentlyproposedDQDalgorithmCMA-MEGA[19]outper- contactstheground(eachfootismeasuredindividually,so
formsQDalgorithmsbyordersofmagnitudewhenexactgradients valuesdo notsumto100%). Withthese policies,theagent
areavailable,suchaswhensearchingthelatentspaceofagenera- couldcontinuewalkingevenifonefootisdamaged.
tivemodel.However,RLproblemslikethehalf-cheetahlackthese
gradientsbecausetheenvironmentistypicallynon-differentiable,
thuslimitingtheapplicabilityofDQD.Toaddressthislimitation,we measures2𝑚 𝑖(𝝓) ∈R(for𝑖 ∈1..𝑘)or,asajointmeasure,𝒎(𝝓) ∈
drawinspirationfromhowevolutionstrategies(ES)[1,39,51,60] R𝑘.Thesemeasuresforma𝑘-dimensionalmeasurespaceX.For
anddeepRLactor-criticmethods[21,38,53,54]optimizeareward every 𝒙 ∈ X, the QD objective is to find solution 𝝓 such that
objectivebyapproximatinggradientsforgradientdescent.Ourkey 𝒎(𝝓)=𝒙and𝑓(𝝓)ismaximized.SinceXiscontinuous,itwould
requireinfinitememorytosolvetheQDproblem,soalgorithmsin
insightistoapproximateobjectiveandmeasuregradientsforDQD
algorithmsbyadaptingESandactor-criticmethods.
theMAP-Elitesfamily[13,40]discretizeXbyformingatesselation
Ourworkmakesthreecontributions.(1)Weformalizetheprob- Yconsistingof𝑀cells.Thus,werelaxtheQDproblemtooneof
lemofqualitydiversityforreinforcementlearning(QD-RL)and searchingforanarchiveAconsistingof𝑀elites𝝓𝑖 ,oneforeach
reduceittoaninstanceofDQD.(2)WedeveloptwoQD-RLvari- cellinY.Then,theQDobjectiveistomaximizetheperformance
antsoftheDQDalgorithmCMA-MEGA,whereeachalgorithm 𝑓(𝝓𝑖)ofallelites:
approximatesobjectiveandmeasuregradientswithadifferentcom-
𝑀
binationofESandactor-criticmethods.(3)Webenchmarkour (cid:213)
max 𝑓(𝝓𝑖) (1)
variantsonfourPyBulletlocomotiontasksfromQDGym[15,42]. 𝝓1..𝑀 𝑖=1
Onevariantperformscomparably(intermsofQDscore;Sec.5.1.3)
tothestate-of-the-artPGA-MAP-Elites[43]intwotasks.Theother 2.1.1 DifferentiableQualityDiversity(DQD). InDQD,weassume
variantachievescomparableQDscorewithPGA-MAP-Elitesinall 𝑓 and 𝒎 are first-order differentiable. We denote the objective
tasks1butislessefficientthanPGA-MAP-Elitesintwotasks. gradientas∇𝑓(𝝓),orabbreviatedas∇𝑓,andthemeasuregradients
Theseresultscontrastwithpriorwork[19]whereCMA-MEGA
as∇𝒎(𝝓)or∇𝒎.
vastlyoutperformsaDQDalgorithminspiredbyPGA-MAP-Elites
2.2 QualityDiversityforReinforcement
onbenchmarkfunctionswheregradientinformationisavailable.
Learning(QD-RL)
Overall,weshedlightonthelimitationsofCMA-MEGAinQD
domains where the main challenge comes from optimizing the WedefineQD-RLasaninstanceoftheQDprobleminwhicheach
objectiveratherthanfromexploringmeasurespace.Atthesame solution𝝓parameterizesanRLpolicy𝜋
𝝓
.Then,theobjective𝑓(𝝓)
time,sincewedecouplegradientestimatesfromQDoptimization, is the expected discounted return of𝜋 𝝓 , and the measures 𝒎(𝝓)
ourworkopensapathforfutureresearchthatwouldbenefitfrom arefunctionsof𝜋 .Formally,drawingontheMarkovDecision
𝝓
independentimprovementstoeitherDQDorRL. Process(MDP)formulation[55],werepresentQD-RLasatuple
(S,U,𝑝,𝑟,𝛾,𝒎).Ondiscretetimesteps𝑡 inanepisodeofinterac-
2 PROBLEMSTATEMENT tion,anagentobservesstate𝑠 ∈Sandtakesaction𝑎∈Uaccord-
2.1 QualityDiversity(QD) ingtoapolicy𝜋 𝝓 (𝑎|𝑠).Theagentthenreceivesscalarreward𝑟(𝑠,𝑎)
andobservesnextstate𝑠′ ∈ S accordingto𝑠′ ∼ 𝑝(·|𝑠,𝑎).Each
WeadoptthedefinitionofQDfrompriorwork[19].Forasolution
vector𝝓 ∈ R𝑛,QDconsidersanobjectivefunction 𝑓(𝝓) and𝑘 e n p u i m so b d e e r t o h f u t s im ha e s st a ep tr s a i j n ec t t h o e ry e 𝜉 pi = so { d 𝑠 e 0 , , a 𝑎 n 0 d ,𝑠 t 1 h ,𝑎 e 1 p , r . o ., b 𝑠 𝑇 ab } i , l w ity he th re a 𝑇 tp i o s l t i h cy e
1WenotethattheperformanceoftheCMA-MEGAisworsethanPGA-MAP-Elites
𝜋
𝝓
takestrajectory𝜉is𝑝
𝝓
(𝜉)=𝑝(𝑠0)(cid:206)𝑇
𝑡=
−
0
1𝜋
𝝓
(𝑎 𝑡|𝑠 𝑡)𝑝(𝑠 𝑡+1|𝑠
𝑡
,𝑎 𝑡).
intwoofthetasks,albeitwithinvariance.Weconsideritlikelythatadditionalruns
wouldresultinPGA-MAP-Elitesperformingsignificantlybetterinthesetasks.We 2Priorworkreferstomeasurefunctionoutputsas“behaviorcharacteristics,”“behavior
leavefurtherevaluationforfuturework. descriptors,”or“featuredescriptors.”
1103


---

## Page 3

ApproximatingGradientsforDifferentiableQualityDiversityinReinforcementLearning GECCO’22,July9–13,2022,Boston,MA,USA
Now,wedefinetheexpecteddiscountedreturnofpolicy𝜋
𝝓
as intotargetnetworks𝜋
𝝓′
,𝑄
𝜽1 ′
,𝑄
𝜽2 ′
viaanexponentiallyweighted
movingaveragewithupdaterate𝜏.
(cid:34) 𝑇 (cid:35)
𝑓(𝝓)=E 𝜉∼𝑝 𝝓 (cid:213) 𝛾𝑡𝑟(𝑠 𝑡 ,𝑎 𝑡) (2) 3.2 QualityDiversityAlgorithms
𝑡=0
wherethediscountfactor𝛾 ∈ (0,1)tradesoffbetweenshort-and 3.2.1 MAP-ElitesextensionsforQD-RL. OneofthesimplestQD
long-termrewards.Finally,wequantifythebehaviorofpolicy𝜋 algorithmsisMAP-Elites[13,40].MAP-Elitescreatesanarchive
𝝓
viaa𝑘-dimensionalmeasurefunction𝒎(𝝓). AbytesselatingthemeasurespaceXintoagridofevenly-sized
cells.Then,itdraws𝜆initialsolutionsfromamultivariateGaussian
2 p . r 2 o .1 blem Q . D S - i R nc L e a t s h a e n ex in a s c t t a g n r c a e d o ie f n D ts Q ∇ D. 𝑓 W an e d r ∇ ed 𝒎 uc u e s Q ua D ll - y R d L o to no a t D ex Q i D st N MA (𝝓 P 0 - , E 𝜎 li 𝑰 t ) es ce c n om te p re u d te a s t 𝑓 so (𝝓 m ) e a 𝝓 n 0 d . 𝒎 Ne ( x 𝝓 t ) ,f a o n r d e i a n c s h er s t a s m 𝝓 p i l n e t d o s A olu .I t n io s n u 𝝓 b- ,
inQD-RL,wemustinsteadapproximatethem.
sequentiterations,MAP-Elitesrandomlyselects𝜆solutionsfrom
3 BACKGROUND
AandaddsGaussiannoise,i.e.solution𝝓becomes𝝓+N(0,𝜎𝑰).
Solutionsareplacedintocellsbasedontheirmeasures;ifasolution
3.1 Single-ObjectiveReinforcementLearning hashigher𝑓 thanthesolutioncurrentlyinthecell,itreplacesthat
Wereviewalgorithmswhichtrainapolicytomaximizeasingleob- solution.OnceinsertedintoA,solutionsareknownaselites.
jective,i.e.𝑓(𝝓)inEq.2,withthegoalofapplyingthesealgorithms’ Duetothehighdimensionalityofneuralnetworkparameters,
gradientapproximationstoDQDinSec.4. directpolicyoptimizationwithMAP-Eliteshasnotproveneffective
inQD-RL[9],althoughindirectencodingshavebeenshownto
3.1.1 Evolutionstrategies(ES). ES[4]isaclassofevolutionary scaletolargepolicynetworks[23,50].Fordirectsearch,several
algorithmswhichoptimizestheobjectivebysamplingapopulation extensionsmergeMAP-Eliteswithactor-criticmethodsandES.For
ofsolutionsandmovingthepopulationtowardsareasofhigher instance,PolicyGradientAssistedMAP-Elites(PGA-MAP-Elites)
performance.NaturalEvolutionStrategies(NES)[60,61]isatypeof [43]combinesMAP-EliteswithTD3.Eachiteration,PGA-MAP-
ESwhichupdatesthesamplingdistributionofsolutionsbytaking Elites evaluates 𝜆 solutions for insertion into the archive. 𝜆 of
2
steps on distribution parameters in the direction of the natural thesearecreatedbyselectingrandomsolutionsfromthearchive
gradient[2].Forexample,withaGaussiansamplingdistribution, andtakinggradientascentstepswithaTD3critic.Theother 𝜆
eachiterationofanNESwouldcomputenaturalgradientstoupdate 2
solutions are created with a directional variation operator [59]
themean𝝁andcovariance𝚺.
whichselectstwosolutions𝝓1 and𝝓2 fromthearchiveandcreates
WeconsideranNES-inspiredalgorithm[51]whichhasdemon-
anewoneaccordingto𝝓′=𝝓1+𝜎1N(0,𝑰)+𝜎2(𝝓2−𝝓1)N(0,1).
stratedsuccessinRLdomains.Thisalgorithm,whichwereferto
Finally,PGA-MAP-Elitesmaintainsa“greedyactor”whichprovides
asOpenAI-ES,samples𝜆 solutionsfromanisotropicGaussian
𝑒𝑠 actionswhentrainingthecritics(identicallytotheactorinTD3).
butonlycomputesagradientstepforthemean𝝓.Eachsolution
Everyiteration,PGA-MAP-Elitesinsertsthisgreedyactorintothe
sampledbyOpenAI-ESisrepresentedas𝝓+𝜎𝝐𝑖 ,where𝜎 isthe
archive.PGA-MAP-Elitesachievesstate-of-the-artperformanceon
fixedstandarddeviationoftheGaussianand𝝐𝑖 ∼ N(0,𝑰).Once locomotiontasksintheQDGymbenchmark[42].
thesesolutionsareevaluated,OpenAI-ESestimatesthegradientas
AnotherMAP-ElitesextensionisME-ES[9],whichcombines
1 (cid:213)
𝜆𝑒𝑠 MAP-EliteswithanOpenAI-ESoptimizer.Inthe“explore-exploit”
∇𝑓(𝝓)≈ 𝑓(𝝓+𝜎𝝐𝑖)𝝐𝑖 (3) variant, ME-ES alternates between two phases. In the “exploit”
𝜆 𝜎
𝑒𝑠 𝑖=1 phase,ME-ESrestartsOpenAI-ESatamean𝝓andoptimizesthe
OpenAI-ESthenpassesthisestimatetoanAdamoptimizer[32] objectivefor𝑘iterations,insertingthecurrent𝝓intothearchive
whichoutputsagradientascentstepfor𝝓.Tomaketheestimate ineachiteration.Inthe“explore”phase,ME-ESrepeatsthispro-
moreaccurate,OpenAI-ESfurtherincludestechniquessuchasmir- cess,butOpenAI-ESinsteadoptimizesfornovelty,wherenovelty
rorsamplingandranknormalization[5,26,60]. isthedistanceinmeasurespacefromanewsolutiontopreviously
encounteredsolutions.ME-ESalsohasan“exploit”variantandan
3.1.2 Actor-criticmethods. WhileEStreatstheobjectiveasablack “explore”variant,whicheachexecuteonlyonetypeofphase.
box,actor-criticmethodsleveragetheMDPstructureoftheobjec-
OurworkisrelatedtoME-ESinthatwealsoadaptOpenAI-ES,
tive,i.e.thefactthat𝑓(𝝓)isasumofMarkovianvalues.Weare
butinsteadofalternatingbetweenfollowinganoveltygradientand
mostinterestedinTwinDelayedDeepDeterministicpolicygradient
objectivegradient,wecomputeallobjectiveandmeasuregradients
(TD3)[21],anoff-policyactor-criticmethod.TD3maintains(1)an
andallowaCMA-ES[28]instancetodecidewhichgradientstofol-
actorconsistingofthepolicy𝜋 and(2)acriticconsistingofstate-
𝝓 lowbysamplinggradientcoefficientsfromamultivariateGaussian
actionvaluefunctions𝑄 (𝑠,𝑎)and𝑄 (𝑠,𝑎)whichdifferonlyin
𝜽1 𝜽2 updatedovertime(Sec.3.2.2).WeincludeMAP-Elites,PGA-MAP-
randominitialization.Throughinteractionsintheenvironment,the
Elites,andME-ESasbaselinesinourexperiments.RefertoFig.3
actorgeneratesexperiencewhichisstoredinareplaybufferB.This
foradiagramwhichcomparesthesealgorithmstoourapproach.
experienceissampledtotrain𝑄 and𝑄 .Simultaneously,the
𝜽1 𝜽2
actorimprovesbymaximizing𝑄 viagradientascent(𝑄 isonly 3.2.2 CovarianceMatrixAdaptationMAP-ElitesviaaGradientAr-
𝜽1 𝜽2
usedduringcritictraining).Specifically,foranobjective𝑓′which borescence(CMA-MEGA). WedirectlyextendCMA-MEGA[19]to
isbasedonthecriticandapproximates𝑓,TD3estimatesagradient address QD-RL. CMA-MEGA is a DQD algorithm based on the
∇𝑓′(𝝓) andpassesittoanAdamoptimizer.Notably,TD3never QDalgorithmCMA-ME[20].TheintuitionbehindCMA-MEGA
updatesnetworkweightsdirectly,insteadaccumulatingweights isthatifweknewwhichdirectionthecurrentsolutionpoint𝝓∗
1104


---

## Page 4

GECCO’22,July9–13,2022,Boston,MA,USA BryonTjanaka,MatthewC.Fontaine,JulianTogelius,andStefanosNikolaidis
shouldmoveinobjective-measurespace,thenwecouldcalculate
How are solutions generated?
thatchangeinsearchspaceviaalinearcombinationofobjective
andmeasuregradients.FromCMA-ME,weknowagooddirection Mutate solutions that are Maintain an evolution strategy
currently in the archive. separate from the archive.
isonethatresultsinthelargestarchiveimprovement.
Eachiteration,CMA-MEGAfirstcalculatesobjectiveandmea- How are archive solutions How are gradients combined when
modified? generating new solutions?
suregradientsforasolutionpoint𝝓∗.Next,itgenerates𝜆newsolu-
tionsbysamplinggradientcoefficients𝒄 ∼N(𝝁,𝚺)andcomputing Genetic algorithm Take multiple Maintain gradient Take an objective
operator small gradient coefficients with gradient or novelty
𝝓′←𝝓∗+𝑐0∇𝑓(𝝓∗)+(cid:205)𝑘
𝑗=1
𝑐 𝑗∇𝑚 𝑗(𝝓∗).CMA-MEGAinsertsthese a
w
sc
i
e
th
n t
T
s
D
te
3
p
.
s a
i
C
n
M
sta
A
n
-
c
E
e
S gra
O
di
p
e
e
n
n
t
A
st
I
e
-
p
E S
w
.
ith
solutionsintothearchiveandcomputestheirimprovement,Δ.Δ
isdefinedas𝑓(𝝓′)if𝝓′populatesanewcell,and𝑓(𝝓′)−𝑓(𝝓′) MAP-Elites PGA-MAP-Elites How are gradients ME-ES
E approximated?
if𝝓′improvesanexistingcell(replacesaprevioussolution𝝓′).
E
AfterCMA-MEGAinsertsthesolutions,itranksthembyΔ.Ifa Approximate Approximate Approximate
objective gradient measure gradients objective gradient
solutionpopulatesanewcell,itsΔalwaysrankshigherthanthat with OpenAI-ES. with OpenAI-ES. with TD3.
ofasolutionwhichonlyimprovesanexistingcell.CMA-MEGA
thenmovesthesolutionpoint𝝓∗towardsthelargestarchiveim- CMA-MEGA (ES) CMA-MEGA (TD3, ES)
provement,butalsoadaptsthedistributionN(𝝁,𝚺)towardsbetter
gradientcoefficientsbythesameranking.Byleveraginggradient Figure 3: Diagram of MAP-Elites extensions for QD-RL,
information,CMA-MEGAsolvesQDbenchmarkswithordersof showing how our CMA-MEGA variants differ from other
magnitudefewersolutionevaluationsthanpreviousQDalgorithms. QD-RLalgorithms.
3.2.3 BeyondMAP-Elites. SeveralQD-RLalgorithmshavebeen
developed outside the MAP-Elites family. NS-ES [11] builds on methodsassumethattrajectorydiversity,ratherthantargetingspe-
Novelty Search (NS) [35, 36], a family of QD algorithms which cificbehavioraldiversity,isenoughtodriveexplorationtodiscover
addsolutionstoanunstructuredarchiveonlyiftheyarefaraway asingleoptimalpolicy.
fromexistingarchivesolutionsinmeasurespace.UsingOpenAI-
ES,NS-ESconcurrentlyoptimizesseveralagentsfornovelty.Its 4 APPROXIMATINGGRADIENTSFORDQD
variantsNSR-ESandNSRA-ESoptimizeforalinearcombinationof
SinceDQDalgorithmsrequireexactobjectiveandmeasuregradi-
noveltyandobjective.Meanwhile,theQD-RLalgorithm[7](distinct
ents,wecannotdirectlyapplyCMA-MEGAtoQD-RL.Toaddress
fromtheQD-RLproblemwedefine)maintainsanarchivewithall
thislimitation,wereplaceexactgradientswithgradientapproxi-
pastsolutionsandoptimizes agentsalongaParetofront ofthe
mations(Sec.4.1)anddeveloptwoCMA-MEGAvariants(Sec.4.2).
objectiveandnovelty.Finally,DiversityviaDeterminants(DvD)
[46]leveragesakernelmethodtomaintaindiversityinapopulation 4.1 ApproximatingObjectiveandMeasure
ofsolutions.AsNS-ES,QD-RL,andDvDdonotoutputaMAP-
Gradients
Elitesgridarchive,weleavetheirinvestigationforfuturework.
WeadaptgradientapproximationsfromESandactor-criticmethods.
3.3 DiversityinReinforcementLearning SincetheobjectivehasanMDPstructure,weestimateobjective
gradients∇𝑓 withESandactor-criticmethods.Sincethemeasures
HerewedistinguishQD-RLfrompriorworkwhichalsoapplies
areblackboxes,weestimatemeasuregradients∇𝒎withES.
diversitytoRL.Oneareaofworkisinlatent-andgoal-conditioned
policies.Forlatent-conditionedpolicy𝜋 𝝓 (𝑎|𝑠,𝑧)[16,33,37]orgoal- 4.1.1 ApproximatingobjectivegradientswithESandactor-critic
conditionedpolicy𝜋 𝝓 (𝑎|𝑠,𝑔)[3,52],varyingthelatentvariable𝑧 methods. Weestimateobjectivegradientswithtwomethods.First,
orgoal𝑔resultsindifferentbehaviors,e.g.differentwalkinggaits wetreattheobjectiveasablackboxandestimateitsgradientwith
orwalkingtoadifferentlocation.WhileQD-RLalsoseeksarange ablackboxmethod,namelytheOpenAI-ESgradientestimatein
ofbehaviors,themeasures𝒎(𝝓) arecomputedafter evaluating Eq.3.SinceOpenAI-ESperformswellinRLdomains[34,45,51],
𝝓,ratherthanbeforetheevaluation.Ingeneral,QD-RLfocuseson webelievethisestimateissuitableforapproximatinggradientsfor
findingavarietyofpoliciesforasingletask,ratherthanattempting CMA-MEGAinQD-RLsettings.Importantly,thisestimaterequires
tosolveavarietyoftaskswithasingleconditionedpolicy. environmentinteractionbyevaluating𝜆 solutions.
𝑒𝑠
Anotherareaofworkcombinesevolutionaryandactor-critic Sincetheobjectivehasawell-definedstructure,i.e.itisasum
algorithms to solve single-objective hard-exploration problems ofrewardsfromanMDP(Eq.2),wealsoestimateitsgradientwith
[10,30,31,48,56].Inthesemethods,anevolutionaryalgorithmsuch anactor-criticmethod,TD3.TD3iswell-suitedforthispurpose
ascross-entropymethod[14]facilitatesexplorationbygenerating becauseitefficientlyestimatesobjectivegradientsforthemultiple
adiversepopulationofpolicies,whileanactor-criticalgorithm policiesthatCMA-MEGAandotherQD-RLalgorithmsgenerate.
suchasTD3trainshigh-performingpolicieswiththispopulation’s Inparticular,oncethecriticistrained,TD3canprovideagradient
environmentexperience.QD-RLdiffersfromthesemethodsinthat estimateforanypolicywithoutadditionalenvironmentinteraction.
itviewsdiversityasacomponentoftheoutput,whilethesemeth- Amongactor-criticmethods,weselectTD3sinceitachieveshigh
odsviewdiversityasameansforenvironmentexploration.Hence, performancewhileoptimizingprimarilyfortheRLobjective.Prior
QD-RLmeasurespolicybehaviorviaameasurefunctionandcol- work[21]showsthatTD3outperformson-policyactor-criticmeth-
lectsdiversepoliciesinanarchive.Incontrast,theseRLexploration ods[53,54].Whiletheoff-policySoftActor-Critic[27]algorithm
1105


---

## Page 5

ApproximatingGradientsforDifferentiableQualityDiversityinReinforcementLearning GECCO’22,July9–13,2022,Boston,MA,USA
canoutperformTD3,itoptimizesamaximum-entropyobjective Algorithm 1: CMA-MEGA (ES) and CMA-MEGA (TD3,
designedtoencourageexploration.Inourwork,weexploreby ES). Highlighted portions are only executed in CMA-
findingpolicieswithdifferentmeasures.Thus,weleaveforfuture MEGA(TD3,ES).AdaptedfromCMA-MEGA[19].Referto
worktheproblemofintegratingQD-RLwiththeactiondiversity AppendixAforfunctionswhosenamesareinSmall_Caps.
encouragedbyentropymaximization.
1 CMA-MEGAvariants(𝑒𝑣𝑎𝑙𝑢𝑎𝑡𝑒,𝝓0,𝑁,𝜆,𝜎 𝑔 ,𝜂,𝜆 𝑒𝑠 ,𝜎 𝑒):
4.1.2 ApproximatingmeasuregradientswithES. Sincemeasuresdo
Input:Function𝑒𝑣𝑎𝑙𝑢𝑎𝑡𝑒whichexecutesapolicy𝝓and
nothavespecialpropertiessuchasanMDPstructure(Sec.2.2),we
outputsobjective𝑓(𝝓)andmeasures𝒎(𝝓),
onlyestimatetheirgradientwithblackboxmethods.Thus,similar
initialsolution𝝓0 ,desirediterations𝑁,batch
size𝜆,initialCMA-ESstepsize𝜎 ,learningrate
totheobjective,weapproximateeachmeasure’sgradient∇𝑚
𝑖
with 𝑔
𝜂,ESbatchsize𝜆 ,ESstandarddeviation𝜎
theOpenAI-ESgradientestimate,replacing𝑓 with𝑚 inEq.3. 𝑒𝑠 𝑒
𝑖
Result:Generates𝑁𝜆solutions,storingelitesinan
SincetheOpenAI-ESgradientestimaterequiresadditionalenvi-
ronmentinteraction,allofourCMA-MEGAvariantsrequireenvi-
archiveA
ronmentinteractiontoestimategradients.However,theenviron- 2 𝜆′←𝜆−1 −1
mentinteractionrequiredtoestimatemeasuregradientsremains 3 InitializeemptyarchiveA,solutionpoint𝝓∗←𝝓0
constantevenasthenumberofmeasuresincreases,sincewecan 4 InitializeCMA-ESwithpopulation𝜆′,resultingin
reusethesame𝜆 𝑒𝑠 solutionstoestimateeach∇𝑚 𝑖 . 𝝁 =0,𝚺=𝜎 𝑔𝑰,andinternalCMA-ESparameters𝒑
tot
In
he
p
o
ro
b
b
je
le
c
m
tiv
s
e
w
,
h
it
e
m
re
a
t
y
he
be
m
f
e
e
a
a
s
s
u
ib
re
le
sh
to
av
e
e
st
a
im
nM
ate
D
e
P
a
s
c
t
h
ru
∇
ct
𝑚
ur
𝑖
e
w
s
i
i
t
m
h
il
i
a
ts
r 5
6 f
B
o
,
r
𝑄
𝑖
𝜽
𝑡𝑒
1 ,
𝑟
𝑄
←
𝜽2 ,
1
𝜋
.
𝝓
.𝑁
𝑞 ,
d
𝑄
o
𝜽1 ′ ,𝑄 𝜽2 ′ ,𝜋 𝝓𝑞 ′ ←Initialize_TD3()
ownTD3instance.Intheenvironmentsinourwork(Sec.5.1),each
7
𝑓(𝝓∗),𝒎(𝝓∗)←𝑒𝑣𝑎𝑙𝑢𝑎𝑡𝑒(𝝓∗)
measure isnon-Markovian sinceitcalculates theproportion of
8
Update_Archive(A,𝝓∗,𝑓(𝝓∗),𝒎(𝝓∗))
timeawalkingagent’sfootspendsontheground.Thiscalculation
dependsontheentireagenttrajectoryratherthanononestate. 9 ∇𝑓(𝝓∗),∇𝒎(𝝓∗)←ES_Gradients(𝝓∗,𝜆 𝑒𝑠 ,𝜎 𝑒 )
10 ∇𝑓(𝝓∗)←TD3_Gradient(𝝓∗,𝑄 𝜽1 ,B)
4.2 CMA-MEGAVariants 11 Normalize∇𝑓(𝝓∗)and∇𝒎(𝝓∗)tobeunitvectors
OurchoiceofgradientapproximationsleadstotwoCMA-MEGA 12 for𝑖 ←1..𝜆′do
variants.CMA-MEGA(ES)approximatesobjectiveandmeasure 13 𝒄𝑖 ∼N(𝝁,𝚺)
gradientswithOpenAI-ES,whileCMA-MEGA(TD3,ES)approx- 14 ∇𝑖 ←𝑐 𝑖,0∇𝑓(𝝓∗)+(cid:205)𝑘 𝑗=1 𝑐 𝑖,𝑗∇𝑚 𝑗(𝝓∗)
imatestheobjectivegradientwithTD3andmeasuregradientswith 15 𝝓𝑖 ′←𝝓∗+∇𝑖
OpenAI-ES.Fig.1showsanoverviewofbothalgorithms,andAlgo- 16 𝑓(𝝓𝑖 ′),𝒎′(𝝓𝑖 ′)←𝑒𝑣𝑎𝑙𝑢𝑎𝑡𝑒(𝝓𝑖 ′)
rithm1showstheirpseudocode.AsCMA-MEGA(TD3,ES)builds 17 Δ 𝑖 ←Update_Archive(A,𝝓𝑖 ′,𝑓(𝝓𝑖 ′),𝒎(𝝓𝑖 ′))
onCMA-MEGA(ES),wepresentonlyCMA-MEGA(TD3,ES)and 18 end
highlightlinesthatCMA-MEGA(TD3,ES)additionallyexecutes. 19 Rank𝒄𝑖 ,∇𝑖 byΔ 𝑖
IdenticallytoCMA-MEGA,thetwovariantsmaintainthreepri-
20 AdaptCMA-ESparameters𝝁,𝚺,𝒑basedon
marycomponents:asolutionpoint𝝓∗,amultivariateGaussian
rankingsof𝒄𝑖
d
E
i
l
s
it
t
e
ri
s
b
a
u
r
t
c
io
h
n
iv
N
eA
(𝝁
f
,
o
𝚺
r
)
s
f
t
o
o
r
ri
s
n
a
g
m
s
p
o
l
l
i
u
n
t
g
io
g
n
r
s
a
.
d
W
ien
e
t
in
co
it
e
ia
ffi
li
c
z
i
e
en
th
ts
e
,
a
a
r
n
c
d
hi
a
v
M
ea
A
n
P
d
-
21 𝝓∗←𝝓∗+𝜂(cid:205) 𝑖 𝜆 =1 𝑤 𝑖∇rank[i]// 𝑤 𝑖 is part of 𝒑
solutionpointonline3,andweinitializethecoefficientdistribution 22 ifthereisnochangeinAthen
aspartofaCMA-ESinstanceonline4.3 23 RestartCMA-ESwith𝝁 =0,𝚺=𝜎 𝑔𝑰
Inthemainloop(line6),wefollowtheworkflowshowninFig. 24
Set𝝓∗toarandomlyselectedelitefromA
1.First,afterevaluating𝝓∗andinsertingitintothearchive(line 25 end
7-8),weapproximateitsgradientswitheitherESorTD3(line9-10). 26 𝑓(𝝓𝑞),𝒎(𝝓𝑞)←𝑒𝑣𝑎𝑙𝑢𝑎𝑡𝑒(𝝓𝑞)
Thisgradientapproximationformsthekeydifferencebetweenour 27 Update_Archive(A,𝝓𝑞 ,𝑓(𝝓𝑞),𝒎(𝝓𝑞))
variantsandtheoriginalCMA-MEGAalgorithm[19]. 28 Addexperiencefromallcallsto𝑒𝑣𝑎𝑙𝑢𝑎𝑡𝑒intoB
( f l r i o n
N
m e
e
1 t
x
3 h
t
-
,
e 1
w
5 c ) o
e
. e W
b
ffi
r
e
a
c
n
t ie h
c
n e
h
n t
f
d
r
e
o
i v s
m
a tr lu i
𝝓
b a u
∗
te t
t
i
o
o ea n
c
c
r
a h
e
n
a
𝝓 d
t
𝑖
e
′ c a
s
o n
o
m d
lu
p i
t
n u
io
s t e i
n
n r
s
t g
𝝓
i p t
𝑖 ′
e i
b
n r
y
t t u o
s
r t
a
b h
m
a e t
p
i a o
l
r
i
n c
n
h s
g
i ∇ v
𝒄
e
𝑖
𝑖 3
2
0
9
end
Train_TD3(𝑄 𝜽1 ,𝑄 𝜽2 ,𝜋 𝝓𝑞 ,𝑄 𝜽1 ′ ,𝑄 𝜽2 ′ ,𝜋 𝝓𝑞 ′ ,B)
(line16-17).
Finally,weupdatethesolutionpointandthecoefficientdistribu-
tion’sCMA-ESinstancebyforminganimprovementrankingbased OurCMA-MEGAvariantshavetwoadditionalcomponents.First,
ontheimprovementΔ 𝑖 (Sec.3.2.2;line19-21).Importantly,sincewe wecheckifnosolutionswereinsertedintothearchiveattheend
rankbasedonimprovement,thisupdateenablestheCMA-MEGA of the iteration, which would indicate that we should reset the
variantstomaximizetheQDobjective(Eq.1)[19]. coefficientdistributionandthesolutionpoint(line22-24).Second,
inthecaseofCMA-MEGA(TD3,ES),wemanageaTD3instance
3WesettheCMA-ESbatchsize𝜆′slightlylowerthanthetotalbatchsize𝜆(line2). similartohowPGA-MAP-Elitesdoes(Sec.3.2.1).ThisTD3instance
WhileCMA-MEGA(ES)andCMA-MEGA(TD3,ES)bothevaluate𝜆solutionseach consistsofareplaybufferB,criticnetworks𝑄 and𝑄 ,agreedy
iteration,oneevaluationisreservedfor𝝓∗(line7).InCMA-MEGA(TD3,ES),one 𝜽1 𝜽2
moreevaluationisreservedforthegreedyactor(line26). actor𝜋 𝝓𝑞 ,andtargetnetworks𝑄 𝜽1 ′ ,𝑄 𝜽2 ′ ,𝜋 𝝓𝑞 ′ (allinitializedonline
1106


---

## Page 6

GECCO’22,July9–13,2022,Boston,MA,USA BryonTjanaka,MatthewC.Fontaine,JulianTogelius,andStefanosNikolaidis
5).Attheendofeachiteration,weusethegreedyactortotrainthe QDAnt QDHalf-Cheetah QDHopper QDWalker
critics,andwealsoinsertitintothearchive(line26-29).
5 EXPERIMENTS
WecompareourtwoproposedCMA-MEGAvariants(CMA-MEGA
(ES),CMA-MEGA(TD3,ES))withthreebaselines(PGA-MAP-Elites, Figure4:QDGymlocomotionenvironments[42].
ME-ES,MAP-Elites)infourlocomotiontasks.WeimplementMAP-
ElitesasdescribedinSec.3.2.1,andweselecttheexplore-exploit
variantforME-ESsinceithasperformedatleastaswellasboth
archivehasanobjectivevalueofatleast0.Thus,weuseQDscore
theexplorevariantandtheexploitvariantinseveraldomains[9].
defined as (cid:205)
𝑖
𝑀 =11𝝓𝑖exists(𝑓(𝝓𝑖) −minobjective). We also define
5.1 EvaluationDomains
amaximumobjectiveequivalenttoeachenvironment’s“reward
threshold”inPyBulletGym.Thisthresholdistheobjectivevalueat
5.1.1 QDGym. Weevaluateouralgorithmsinfourlocomotion whichanagentisconsideredtohavesuccessfullylearnedtowalk.
environmentsfromQDGym[42],alibrarybuiltonPyBulletGym WereporttwometricsinadditiontoQDscore.Archivecoverage,
[12,15]andOpenAIGym[6].AppendixClistsallenvironment the proportion of cells for which the algorithm found an elite,
details.Ineachenvironment,theQDalgorithmoutputsanarchive gaugeshowwelltheQDalgorithmexploresmeasurespace,and
ofwalkingpoliciesforasimulatedagent.Theagentisprimarily bestperformance,thehighestobjectiveofanyeliteinthearchive,
rewardedforitsforwardspeed.Therearealsorewardshaping[41] gaugeshowwelltheQDalgorithmexploitstheobjective.
signals,suchasapunishmentforapplyinghigherjointtorques,
intendedtoguidepolicyoptimization.Themeasurescomputethe 5.2 ExperimentalDesign
proportionoftime(numberoftimestepsdividedbytotaltimesteps
Wefollowabetween-groupsdesign,wherethetwoindependent
inanepisode)thateachoftheagent’sfeetcontactstheground.
variablesareenvironment(QDAnt,QDHalf-Cheetah,QDHopper,
QDGymischallengingbecausetheobjectiveineachenviron-
QDWalker)andalgorithm(CMA-MEGA(ES),CMA-MEGA(TD3,
mentdoesnot“align”withthemeasures,inthatfindingpolicies
ES),PGA-MAP-Elites,ME-ES,MAP-Elites).Thedependentvariable
withdifferentmeasures(i.e.exploringthearchive)doesnotneces-
istheQDscore.Ineachenvironment,weruneachalgorithmfor5
sarilyleadtooptimizationoftheobjective.Whileitmaybetrivial
trialswithdifferentrandomseedsandtestthreehypotheses:
tofillthearchivewithlow-performingpolicieswhichstandinplace
H1:CMA-MEGA(ES)willoutperformallbaselines(PGA-MAP-
andliftthefeetupanddowntoachievedifferentmeasures,the
Elites,ME-ES,MAP-Elites).
agents’complexity(highdegreesoffreedom)makesitdifficultto
H2:CMA-MEGA(TD3,ES)willoutperformallbaselines.
learnahigh-performingpolicyforeachvalueofthemeasures.
H3:CMA-MEGA(TD3,ES)willoutperformCMA-MEGA(ES).
5.1.2 Hyperparameters. Eachagent’spolicyisaneuralnetwork H1andH2arebasedonpriorwork[19]whichshowedthatin
whichtakesinstatesandoutputsactions.Therearetwohidden QDbenchmarkdomains,CMA-MEGAoutperformsalgorithmsthat
layersof128nodes,andthehiddenandoutputlayershavetanh donotleveragebothobjectiveandmeasuregradients.H3isbased
activation.WeinitializeweightswithXavierinitialization[24]. onresults[45]whichsuggestthatactor-criticmethodsoutperform
Forthearchive,wetesselateeachenvironment’smeasurespace ESinPyBulletGym.Thus,weexpecttheTD3objectivegradientto
intoagridofevenly-sizedcells(seeTable6forgriddimensions). bemoreaccuratethantheESobjectivegradient,leadingtomore
Eachmeasureisboundtotherange[0,1],theminandmaxpro- efficienttraversalofobjective-measurespaceandhigherQDscore.
portionoftimethatonefootcancontacttheground.
Eachalgorithmevaluates1millionsolutionsintheenvironment. 5.3 Implementation
Duetocomputationallimits,weevaluateeachsolutiononceinstead
WeimplementallQDalgorithmswiththepyribslibrary[57]except
ofaveragingmultipleepisodes,soeachalgorithmruns1million
forME-ES,whichweadaptfromtheauthors’implementation.We
episodestotal.RefertoAppendixBforfurtherhyperparameters.
runeachexperimentwith100CPUsonahigh-performancecluster.
WeallocateoneNVIDIATeslaP100GPUtoalgorithmsthattrain
5.1.3 Metrics. OurprimarymetricisQDscore[49],whichprovides
TD3(CMA-MEGA(TD3,ES)andPGA-MAP-Elites).Dependingon
aholisticviewofalgorithmperformance.QDscoreisthesumofthe
objectivevaluesofallelitesinthearchive,i.e.(cid:205) 𝑖 𝑀 =11𝝓𝑖exists 𝑓(𝝓𝑖), t r h ef e er al t g o o T ri a t b h l m e1 a 2 n , d A e p n p v e i n ro di n x m E en fo t r ,e m a e c a h n e r x u p n e t r i i m m e e s n . t W la e st h s a 4 v - e 2 r 0 e h le o a u se rs d ;
where𝑀isthenumberofarchivecells.Wenotethatthecontribu-
oursourcecodeathttps://github.com/icaros-usc/dqd-rl
tionofacelltotheQDscoreis0ifthecellisunoccupied.Weset
theobjective𝑓 tobetheexpectedundiscountedreturn,i.e.weset
6 RESULTS
𝛾 =1inEq.2.
Sinceobjectivesmaybenegative,analgorithm’sQDscoremay Weran5trialsofeachalgorithmineachenvironment.Ineach
be penalized when adding a new solution. To prevent this, we trial,weallocated1millionevaluationsandrecordedtheQDscore,
define a minimum objective in each environment by taking the archive coverage, and best performance. Fig. 5 plots these met-
lowestobjectivevaluethatwasinsertedintothearchiveinany rics,andAppendixElistsfinalvaluesofallmetrics.AppendixG
experimentinthatenvironment.Wesubtractthisminimumfrom showsexampleheatmapsandhistogramsofeacharchive,andthe
everysolution,suchthateverysolutionthatwasinsertedintoan supplementalmaterialcontainsvideosofgeneratedagents.
1107


---

## Page 7

ApproximatingGradientsforDifferentiableQualityDiversityinReinforcementLearning GECCO’22,July9–13,2022,Boston,MA,USA
1.5
1.0
0.5
0.0
erocS
DQ
1e6 QD Ant 1e6 QD Half-Cheetah 1e6 QD Hopper 1e6 QD Walker
2.0 1.5
4
1.5 1.0
2 1.0
0.5 0.5
0 0.0 0.0
1.00
0.75
0.50
0.25
0.00
egarevoC
evihcrA
1.00 1.00 1.00
0.75 0.75 0.75
0.50 0.50 0.50
0.25 0.25 0.25
0.00 0.00 0.00
3000
2000
1000
0.00 0.25 0.50 0.75 1.00
Evaluations 1e6
ecnamrofreP
tseB
CMA-MEGA (ES) PGA-MAP-Elites MAP-Elites
CMA-MEGA (TD3, ES) ME-ES
3000 3000
2000
2000
2000
1000
0 1000 1000
−1000
0 0
0.00 0.25 0.50 0.75 1.00 0.00 0.25 0.50 0.75 1.00 0.00 0.25 0.50 0.75 1.00
Evaluations 1e6 Evaluations 1e6 Evaluations 1e6
Figure5:PlotsofQDscore,archivecoverage,andbestperformanceforthe5algorithmsinourexperimentsinall4environ-
mentsfromQDGym.Thex-axisinallplotsisthenumberofsolutionsevaluated.Solidlinesshowthemeanover5trials,and
shadedregionsshowthestandarderrorofthemean.
6.1 Analysis ME-ESinallenvironments.CMA-MEGA(TD3,ES)achievessignif-
Totestourhypotheses,weconductedatwo-wayANOVAwhich icantlyhigherQDscorethanMAP-ElitesinQDHalf-Cheetahand
examinedtheeffectofalgorithmandenvironmentontheQDscore. Walker,withnosignificantdifferenceinQDAntandQDHopper.
WenotethattheANOVArequiresQDscorestohavethesamescale, H3:CMA-MEGA(TD3,ES)achievessignificantlyhigherQD
buteachenvironment’sQDscorehasadifferentscalebydefault. scorethanCMA-MEGA(ES)inQDHopperandQDWalker,but
Thus,forthisanalysis,wenormalizedQDscoresbydividingby thereisnosignificantdifferenceinQDAntandQDHalf-Cheetah.
eachenvironment’smaximumQDscore,definedasgridcells*(max
6.2 Discussion
objective-minobjective)(seeAppendixCforthesequantities).
Wefoundastatisticallysignificantinteractionbetweenalgo- WediscusshowtheCMA-MEGAvariantsdifferfromthebaselines
rithmandenvironmentonQDscore,𝐹(12,80)=16.82,𝑝 <0.001. (Sec.6.2.1-6.2.4)andhowtheydifferfromeachother(Sec.6.2.5).
Simplemaineffectsanalysisindicatedthatthealgorithmhada
significanteffectonQDscoreineachenvironment,soweranpair- 6.2.1 PGA-MAP-Elitesandobjective-measurespaceexploration. Of
theCMA-MEGAvariants,CMA-MEGA(TD3,ES)performedthe
wisecomparisons(two-sidedt-tests)withBonferronicorrections
closesttoPGA-MAP-Elites,withnosignificantQDscoredifference
(AppendixF).Ourresultsareasfollows:
inanyenvironment.Thisresultdiffersfrompriorwork[19]inQD
H1:ThereisnosignificantdifferenceinQDscorebetweenCMA-
benchmarkdomains,whereCMA-MEGAoutperformedOG-MAP-
MEGA(ES)andPGA-MAP-ElitesinQDAntandQDHalf-Cheetah,
Elites,abaselineDQDalgorithminspiredbyPGA-MAP-Elites.
butinQDHopperandQDWalker,CMA-MEGA(ES)attainssignif-
Weattributethisdifferencetothedifficultyofexploringobjective-
icantlylowerQDscorethanPGA-MAP-Elites.CMA-MEGA(ES)
measurespaceinthebenchmarkdomains.Forexample,thelinear
achievessignificantlyhigherQDscorethanME-ESinallenviron-
projectionbenchmarkdomainisdesignedtobe“distorted”[20].
mentsexceptQDHopper,wherethereisnosignificantdifference.
Valuesinthecenterofitsmeasurespaceareeasytoobtainwithran-
ThereisnosignificantdifferencebetweenCMA-MEGA(ES)and
domsampling,whilevaluesattheedgesareunlikelytobesampled.
MAP-ElitesinalldomainsexceptQDHopper,whereCMA-MEGA
Hence,highQDscorearisesfromexploringmeasurespaceand
(ES)attainssignificantlylowerQDscore.
fillingthearchive.SinceCMA-MEGAadaptsitssamplingdistribu-
H2: In all environments, there is no significant difference in
tion,itisabletoperformthisexploration,whileOG-MAP-Elites
QDscorebetweenCMA-MEGA(TD3,ES)andPGA-MAP-Elites.
remains“stuck”inthecenterofthemeasurespace.
CMA-MEGA(TD3,ES)achievessignificantlyhigherQDscorethan
Incontrast,asdiscussedinSec.5.1.1,itisrelativelyeasytofill
thearchiveinQDGym.Weseethisempirically:inallenvironments,
1108


---

## Page 8

GECCO’22,July9–13,2022,Boston,MA,USA BryonTjanaka,MatthewC.Fontaine,JulianTogelius,andStefanosNikolaidis
allalgorithmsachievenearly100%archivecoverage,usuallywithin 6.2.5 CMA-MEGAvariantsandgradientestimates. InQDHopper
the first 250k evaluations (Fig. 5). Hence, the best QD score is andQDWalker,CMA-MEGA(TD3,ES)hadsignificantlyhigher
achievedbyincreasingtheobjectivevalueofsolutionsafterfilling QDscorethanCMA-MEGA(ES).Onepotentialexplanationisthat
thearchive.PGA-MAP-Elitesachievesthisbyoptimizinghalfof PyBulletGym(andhenceQDGym)augmentsrewardswithreward
itsgeneratedsolutionswithrespecttoitsTD3critic.Thegenetic shapingsignalsintendedtopromoteoptimalsolutionsfordeepRL
operatorlikelyfurtherenhancestheefficacyofthisoptimization, algorithms.Inpriorwork[45],thesesignalsledPPO[54]totrain
bytakingpreviously-optimizedsolutionsandcombiningthemto successful walking agents, while they led OpenAI-ES into local
obtainhigh-performingsolutionsinotherpartsofthearchive. optima.Forinstance,OpenAI-EStrainedagentswhichstoodstill
Ontheotherhand,theCMA-MEGAvariantsplacelessemphasis soastomaximizeonlytherewardsignalforstayingupright.
onmaximizingtheperformanceofeachsolution,comparedtoPGA- Duetothesesignals,TD3’sobjectivegradientseemsmoreuseful
MAP-Elites:ineachtrial,PGA-MAP-Elitestakes5millionobjective thanthatofOpenAI-ESinQDHopperandQDWalker.Infact,the
gradientstepswithrespecttoitsTD3critic,whiletheCMA-MEGA algorithmswhichperformedbestinQDHopperandQDWalker
variantsonlycompute5kobjectivegradients,becausetheydedicate wereonesthatcalculatedobjectivegradientswithTD3,i.e.PGA-
alargepartoftheevaluationtoestimatingthemeasuregradients. MAP-ElitesandCMA-MEGA(TD3,ES).
ThisdifferencesuggestsapossibleextensiontoCMA-MEGA(TD3, Priorwork[45]foundthatrewardscouldbetailoredforES,such
ES)inwhichsolutionsareoptimizedwithrespecttotheTD3critic thatOpenAI-ESoutperformedPPO.Extensionsofourworkcould
beforebeingevaluatedintheenvironment. investigate whether there is a similar effect for QD algorithms,
wheretailoringtherewardleadsCMA-MEGA(ES)tooutperform
6.2.2 PGA-MAP-Elitesandoptimizationefficiency. Whiletherewas PGA-MAP-ElitesandCMA-MEGA(TD3,ES).
no significant difference in the final QD scores of CMA-MEGA
(TD3,ES)andPGA-MAP-Elites,CMA-MEGA(TD3,ES)wasless
efficientthanPGA-MAP-Elitesinsomeenvironments.Forinstance, 7 CONCLUSION
inQDHopper,PGA-MAP-Elitesreached1.5MQDscoreafter100k
ToextendDQDtoRLsettings,weadaptedgradientapproximations
evaluations,butCMA-MEGA(TD3,ES)required400kevaluations.
fromactor-criticmethodsandES.Byintegratingtheseapproxima-
We can quantify optimization efficiency with QD score AUC, tionswithCMA-MEGA,weproposedtwonovelvariantsthatwe
theareaunderthecurve(AUC)oftheQDscoreplot.ForaQD
evaluatedonfourlocomotiontasksfromQDGym.CMA-MEGA
algorithmwhichexecutes𝑁 iterationsandevaluates𝜆solutions
(TD3,ES)performedcomparablytothestate-of-the-artPGA-MAP-
periteration,wedefineQDscoreAUCasaRiemannsum:
Elitesinalltasksbutwaslessefficientintwoofthetasks.CMA-
𝑁
(cid:213) MEGA(ES)performedcomparablyintwotasks.
QDscoreAUC= (𝜆∗QDscoreatiteration𝑖) (4)
Ourresultscontrastpriorwork[19]whereCMA-MEGAout-
𝑖=1
performedabaselinealgorithminspiredbyPGA-MAP-Elitesin
AftercomputingQDscoreAUC,weranstatisticalanalysissimilar QDbenchmarkdomains.Thedifferenceseemstobethatdifficulty
toSec.6.1andfoundCMA-MEGA(TD3,ES)hadsignificantlylower inthebenchmarksarisesfromahard-to-exploremeasurespace,
QDscoreAUCthanPGA-MAP-ElitesinQDAntandQDHopper. whereasdifficultyinQDGymarisesfromanobjectivewhichre-
TherewasnosignificantdifferenceinQDHalf-CheetahandQD quiresrigorousoptimization.Assuch,futureworkcouldformalize
Walker.Assuch,whileCMA-MEGA(TD3,ES)obtainedcomparable thenotionsof“explorationdifficulty”ofameasurespaceand“op-
finalQDscorestoPGA-MAP-Elitesinalltasks,itwaslessefficient timizationdifficulty”ofanobjectiveandevaluatealgorithmsin
atachievingthosescoresinQDAntandQDHopper. benchmarksthatcoveraspectrumofthesemetrics.
ForpractitionerslookingtoapplyDQDinRLsettings,werecom-
6.2.3 ME-ES and archive insertions. With one exception (CMA-
mendestimatingobjectivegradientswithanoff-policyactor-critic
MEGA(ES)inQDHopper),bothCMA-MEGAvariantsachieved
methodsuchasTD3insteadofwithanES.Duetothedifficulty
significantlyhigherQDscorethanME-ESinallenvironments.We
ofmoderncontrolbenchmarks,itisimportanttoefficientlyopti-
attributethisresulttothenumberofsolutionseachalgorithmin-
mizetheobjective—TD3benefitsoverESsinceitcancomputethe
sertsintothearchive.Eachiteration,ME-ESevaluates200solutions
objectivegradientwithoutfurtherenvironmentinteraction.Fur-
(AppendixB)butonlyinsertsoneintothearchive,foratotalof5000
thermore,rewardsignalsinthesebenchmarksaredesignedfordeep
solutionsinsertedduringeachrun.Giventhateacharchivehasat
RLmethods,makingTD3gradientsmoreusefulthanESgradients.
least1000cells,ME-EShas,onaverage,5opportunitiestoinsert
ByreducingQD-RLtoDQD,wehavedecoupledQD-RLinto
asolutionthatimproveseachcell.Incontrast,theCMA-MEGA
DQDoptimizationandRLgradientapproximations.Inthefuture,
variantshave100timesmoreinsertions.ThoughtheCMA-MEGA
weenvisionalgorithmswhichbenefitfromadvancesineithermore
variantsevaluate200solutionsperiteration,theyinsert100ofthese
efficientDQDormoreaccurateRLgradientapproximations.
intothearchive.Thistotalsto500kinsertionsperrun,allowingthe
CMA-MEGAvariantstograduallyimprovearchivecells.
ACKNOWLEDGMENTS
6.2.4 MAP-Elitesandrobustness. Inmostcases,bothCMA-MEGA
variantshadsignificantlyhigherQDscorethanMAP-Elitesorno Theauthorsthanktheanonymousreviewers,Ya-ChuanHsu,Her-
significantdifference,butinQDHopper,MAP-Elitesachievedsig- ambNemlekar,andGautamSalhotrafortheirinvaluablefeedback.
nificantlyhigherQDscorethanCMA-MEGA(ES).However,we ThisworkwaspartiallysupportedbytheNSFNRI(#1053128)and
foundthatMAP-Elitessolutionswerelessrobust(seeAppendixD). NSFGRFP(#DGE-1842487).
1109


---

## Page 9

ApproximatingGradientsforDifferentiableQualityDiversityinReinforcementLearning GECCO’22,July9–13,2022,Boston,MA,USA
REFERENCES
[20] MatthewC.Fontaine,JulianTogelius,StefanosNikolaidis,andAmyK.Hoover.
[1] YouheiAkimoto,YuichiNagata,IsaoOno,andShigenobuKobayashi.2010.Bidi- 2020. CovarianceMatrixAdaptationfortheRapidIlluminationofBehavior
rectionalRelationbetweenCMAEvolutionStrategiesandNaturalEvolution Space.InProceedingsofthe2020GeneticandEvolutionaryComputationConference
Strategies.InParallelProblemSolvingfromNature,PPSNXI,RobertSchaefer, (Cancún,Mexico)(GECCO’20).AssociationforComputingMachinery,NewYork,
CarlosCotta,JoannaKołodziej,andGünterRudolph(Eds.).SpringerBerlinHei- NY,USA,94–102. https://doi.org/10.1145/3377930.3390232
delberg,Berlin,Heidelberg,154–163. [21] ScottFujimoto,HerkevanHoof,andDavidMeger.2018. AddressingFunc-
[2] Shun-ichi Amari. 1998. Natural Gradient Works Efficiently in tionApproximationErrorinActor-CriticMethods.InProceedingsofthe35th
Learning. Neural Computation 10, 2 (02 1998), 251–276. https: InternationalConferenceonMachineLearning(ProceedingsofMachineLearning
//doi.org/10.1162/089976698300017746arXiv:https://direct.mit.edu/neco/article- Research,Vol.80),JenniferDyandAndreasKrause(Eds.).PMLR,1587–1596.
pdf/10/2/251/813415/089976698300017746.pdf http://proceedings.mlr.press/v80/fujimoto18a.html
[3] MarcinAndrychowicz,FilipWolski,AlexRay,JonasSchneider,RachelFong, [22] AdamGaier,AlexanderAsteroth,andJean-BaptisteMouret.2018.Data-efficient
Peter Welinder, Bob McGrew, Josh Tobin, OpenAI Pieter Abbeel, and Wo- designexplorationthroughsurrogate-assistedillumination.Evolutionarycompu-
jciech Zaremba. 2017. Hindsight Experience Replay. In Advances in Neu- tation26,3(2018),381–410.
ral Information Processing Systems, I. Guyon, U. V. Luxburg, S. Bengio, [23] AdamGaier,AlexanderAsteroth,andJean-BaptisteMouret.2020.Discovering
H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett (Eds.), Vol. 30. RepresentationsforBlack-BoxOptimization.InProceedingsofthe2020Geneticand
Curran Associates, Inc. https://proceedings.neurips.cc/paper/2017/file/ EvolutionaryComputationConference(Cancún,Mexico)(GECCO’20).Association
453fadbd8a1a3af50a9df4df899537b5-Paper.pdf forComputingMachinery,NewYork,NY,USA,103–111. https://doi.org/10.
[4] Hans-GeorgBeyerandHans-PaulSchwefel.2002. Evolutionstrategies–A 1145/3377930.3390221
comprehensiveintroduction.NaturalComputing1,1(01Mar2002),3–52. https: [24] XavierGlorotandYoshuaBengio.2010.Understandingthedifficultyoftraining
//doi.org/10.1023/A:1015059928466 deepfeedforwardneuralnetworks.InProceedingsoftheThirteenthInternational
[5] DimoBrockhoff,AnneAuger,NikolausHansen,DirkV.Arnold,andTimHohm. ConferenceonArtificialIntelligenceandStatistics(ProceedingsofMachineLearning
2010.MirroredSamplingandSequentialSelectionforEvolutionStrategies.In Research,Vol.9),YeeWhyeTehandMikeTitterington(Eds.).PMLR,ChiaLaguna
ParallelProblemSolvingfromNature,PPSNXI,RobertSchaefer,CarlosCotta, Resort,Sardinia,Italy,249–256. https://proceedings.mlr.press/v9/glorot10a.html
JoannaKołodziej,andGünterRudolph(Eds.).SpringerBerlinHeidelberg,Berlin, [25] DanieleGravina,AhmedKhalifa,AntoniosLiapis,JulianTogelius,andGeorgiosN
Heidelberg,11–21. Yannakakis.2019.Proceduralcontentgenerationthroughqualitydiversity.In
[6] GregBrockman,VickiCheung,LudwigPettersson,JonasSchneider,JohnSchul- 2019IEEEConferenceonGames(CoG).IEEE,1–8.
man,JieTang,andWojciechZaremba.2016.OpenAIGym.CoRRabs/1606.01540 [26] DavidHa.2017. AVisualGuidetoEvolutionStrategies. blog.otoro.net(2017).
(2016).arXiv:1606.01540 http://arxiv.org/abs/1606.01540 https://blog.otoro.net/2017/10/29/visual-evolution-strategies/
[7] GeoffreyCideron,ThomasPierrot,NicolasPerrin,KarimBeguir,andOlivier [27] TuomasHaarnoja,AurickZhou,PieterAbbeel,andSergeyLevine.2018. Soft
Sigaud.2020.QD-RL:EfficientMixingofQualityandDiversityinReinforcement Actor-Critic:Off-PolicyMaximumEntropyDeepReinforcementLearningwitha
Learning.CoRRabs/2006.08505(2020).arXiv:2006.08505 https://arxiv.org/abs/ StochasticActor.InProceedingsofthe35thInternationalConferenceonMachine
2006.08505 Learning(ProceedingsofMachineLearningResearch,Vol.80),JenniferDyand
[8] JackClarkandDarioAmodei.2016. FaultyRewardFunctionsintheWild. AndreasKrause(Eds.).PMLR,1861–1870. https://proceedings.mlr.press/v80/
https://openai.com/blog/faulty-reward-functions/. haarnoja18b.html
[9] CédricColas,VashishtMadhavan,JoostHuizinga,andJeffClune.2020.Scaling [28] NikolausHansen.2016. TheCMAEvolutionStrategy:ATutorial. CoRR
MAP-ElitestoDeepNeuroevolution.InProceedingsofthe2020GeneticandEvo- abs/1604.00772(2016).arXiv:1604.00772 http://arxiv.org/abs/1604.00772
lutionaryComputationConference(Cancún,Mexico)(GECCO’20).Association [29] AlexIrpan.2018.DeepReinforcementLearningDoesn’tWorkYet.https://www.
forComputingMachinery,NewYork,NY,USA,67–75. https://doi.org/10.1145/ alexirpan.com/2018/02/14/rl-hard.html.
3377930.3390217 [30] ShauhardaKhadka,SomdebMajumdar,TarekNassar,ZachDwiel,EvrenTumer,
[10] CédricColas,OlivierSigaud,andPierre-YvesOudeyer.2018.GEP-PG:Decoupling SantiagoMiret,YinyinLiu,andKaganTumer.2019. CollaborativeEvolution-
ExplorationandExploitationinDeepReinforcementLearningAlgorithms.In aryReinforcementLearning.InProceedingsofthe36thInternationalConference
Proceedingsofthe35thInternationalConferenceonMachineLearning(Proceedings
onMachineLearning(ProceedingsofMachineLearningResearch,Vol.97),Ka-
ofMachineLearningResearch,Vol.80),JenniferDyandAndreasKrause(Eds.). malikaChaudhuriandRuslanSalakhutdinov(Eds.).PMLR,3341–3350. https:
PMLR,1039–1048. https://proceedings.mlr.press/v80/colas18a.html //proceedings.mlr.press/v97/khadka19a.html
[11] EdoardoConti,VashishtMadhavan,FelipePetroskiSuch,JoelLehman,Kenneth [31] ShauhardaKhadkaandKaganTumer.2018.Evolution-GuidedPolicyGradientin
Stanley,andJeffClune.2018.ImprovingExplorationinEvolutionStrategiesfor ReinforcementLearning.InAdvancesinNeuralInformationProcessingSystems,
DeepReinforcementLearningviaaPopulationofNovelty-SeekingAgents.In S.Bengio,H.Wallach,H.Larochelle,K.Grauman,N.Cesa-Bianchi,andR.Garnett
AdvancesinNeuralInformationProcessingSystems31,S.Bengio,H.Wallach, (Eds.),Vol.31.CurranAssociates,Inc. https://proceedings.neurips.cc/paper/
H.Larochelle,K.Grauman,N.Cesa-Bianchi,andR.Garnett(Eds.).Curran 2018/file/85fc37b18c57097425b52fc7afbb6969-Paper.pdf
Associates, Inc., 5027–5038. http://papers.nips.cc/paper/7750-improving- [32] DiederikP.KingmaandJimmyBa.2015.Adam:AMethodforStochasticOpti-
exploration-in-evolution-strategies-for-deep-reinforcement-learning-via-a- mization.In3rdInternationalConferenceonLearningRepresentations,ICLR2015,
population-of-novelty-seeking-agents.pdf SanDiego,CA,USA,May7-9,2015,ConferenceTrackProceedings,YoshuaBengio
[12] ErwinCoumansandYunfeiBai.2016–2020.PyBullet,aPythonmoduleforphysics andYannLeCun(Eds.). http://arxiv.org/abs/1412.6980
simulationforgames,roboticsandmachinelearning.http://pybullet.org. [33] SaurabhKumar,AviralKumar,SergeyLevine,andChelseaFinn.2020. One
[13] AntoineCully,JeffClune,DaneshTarapore,andJean-BaptisteMouret.2015. SolutionisNotAllYouNeed:Few-ShotExtrapolationviaStructuredMaxEntRL.
Robotsthatcanadaptlikeanimals. Nature521(052015),503–507. https: AdvancesinNeuralInformationProcessingSystems33(2020).
//doi.org/10.1038/nature14422 [34] JoelLehman,JayChen,JeffClune,andKennethO.Stanley.2018. ESisMore
[14] Pieter-TjerkdeBoer,DirkP.Kroese,ShieMannor,andReuvenY.Rubinstein. thanJustaTraditionalFinite-DifferenceApproximator.InProceedingsofthe
2005.ATutorialontheCross-EntropyMethod.AnnalsofOperationsResearch GeneticandEvolutionaryComputationConference(Kyoto,Japan)(GECCO’18).
134,1(01Feb2005),19–67. https://doi.org/10.1007/s10479-005-5724-z AssociationforComputingMachinery,NewYork,NY,USA,450–457. https:
[15] BenjaminEllenberger.2018–2019. PyBulletGymperium. https://github.com/ //doi.org/10.1145/3205455.3205474
benelot/pybullet-gym. [35] Joel Lehman and Kenneth O. Stanley. 2011. Abandoning Objec-
[16] BenjaminEysenbach,AbhishekGupta,JulianIbarz,andSergeyLevine.2019. tives: Evolution Through the Search for Novelty Alone. Evolu-
DiversityisAllYouNeed:LearningSkillswithoutaRewardFunction.InInterna- tionary Computation 19, 2 (06 2011), 189–223. https://doi.org/
tionalConferenceonLearningRepresentations. https://openreview.net/forum?id= 10.1162/EVCO_a_00025 arXiv:https://direct.mit.edu/evco/article-
SJx63jRqFm pdf/19/2/189/1494066/evco_a_00025.pdf
[17] MatthewFontaineandStefanosNikolaidis.2021.AQualityDiversityApproach [36] JoelLehmanandKennethO.Stanley.2011. EvolvingaDiversityofVirtual
toAutomaticallyGeneratingHuman-RobotInteractionScenariosinSharedAu- CreaturesthroughNoveltySearchandLocalCompetition.InProceedingsof
tonomy.Robotics:ScienceandSystems(2021). the13thAnnualConferenceonGeneticandEvolutionaryComputation(Dublin,
[18] MatthewC.Fontaine,Ya-ChuanHsu,YulunZhang,BryonTjanaka,andSte- Ireland)(GECCO’11).AssociationforComputingMachinery,NewYork,NY,
fanosNikolaidis.2021. OntheImportanceofEnvironmentsinHuman-Robot USA,211–218. https://doi.org/10.1145/2001576.2001606
Coordination.Robotics:ScienceandSystems(2021). [37] Yunzhu Li, Jiaming Song, and Stefano Ermon. 2017. InfoGAIL: Inter-
[19] MatthewC.FontaineandStefanosNikolaidis.2021. DifferentiableQuality pretable Imitation Learning from Visual Demonstrations. In Advances in
Diversity.AdvancesinNeuralInformationProcessingSystems34(2021). https: Neural Information Processing Systems, I. Guyon, U. V. Luxburg, S. Ben-
//proceedings.neurips.cc/paper/2021/file/532923f11ac97d3e7cb0130315b067dc- gio,H.Wallach,R.Fergus,S.Vishwanathan,andR.Garnett(Eds.),Vol.30.
Paper.pdf Curran Associates, Inc. https://proceedings.neurips.cc/paper/2017/file/
2cd4e8a2ce081c3d7c32c3cde4312ef7-Paper.pdf
1110


---

## Page 10

GECCO’22,July9–13,2022,Boston,MA,USA BryonTjanaka,MatthewC.Fontaine,JulianTogelius,andStefanosNikolaidis
[38] TimothyP.Lillicrap,JonathanJ.Hunt,AlexanderPritzel,NicolasHeess,Tom [58] JoshTobin,RachelFong,AlexRay,JonasSchneider,WojciechZaremba,andPieter
Erez,YuvalTassa,DavidSilver,andDaanWierstra.2016.Continuouscontrol Abbeel.2017. Domainrandomizationfortransferringdeepneuralnetworks
withdeepreinforcementlearning.In4thInternationalConferenceonLearning fromsimulationtotherealworld.In2017IEEE/RSJInternationalConferenceon
Representations,ICLR2016,SanJuan,PuertoRico,May2-4,2016,ConferenceTrack IntelligentRobotsandSystems(IROS).23–30. https://doi.org/10.1109/IROS.2017.
Proceedings,YoshuaBengioandYannLeCun(Eds.). http://arxiv.org/abs/1509. 8202133
02971 [59] VassilisVassiliadesandJean-BaptisteMouret.2018.DiscoveringtheEliteHy-
[39] HoriaMania,AureliaGuy,andBenjaminRecht.2018.SimpleRandomSearchof pervolumebyLeveragingInterspeciesCorrelation.InProceedingsoftheGe-
StaticLinearPoliciesisCompetitiveforReinforcementLearning.InProceedingsof neticandEvolutionaryComputationConference(Kyoto,Japan)(GECCO’18).
the32ndInternationalConferenceonNeuralInformationProcessingSystems(Mon- AssociationforComputingMachinery,NewYork,NY,USA,149–156. https:
tréal,Canada)(NIPS’18).CurranAssociatesInc.,RedHook,NY,USA,1805–1814. //doi.org/10.1145/3205455.3205602
[40] Jean-BaptisteMouretandJeffClune.2015.Illuminatingsearchspacesbymapping [60] DaanWierstra,TomSchaul,TobiasGlasmachers,YiSun,JanPeters,andJürgen
elites.CoRRabs/1504.04909(2015).arXiv:1504.04909 http://arxiv.org/abs/1504. Schmidhuber.2014.NaturalEvolutionStrategies.JournalofMachineLearning
04909 Research15,27(2014),949–980. http://jmlr.org/papers/v15/wierstra14a.html
[41] AndrewY.Ng,DaishiHarada,andStuartJ.Russell.1999. PolicyInvariance [61] DaanWierstra,TomSchaul,JanPeters,andJuergenSchmidhuber.2008.Natural
UnderRewardTransformations:TheoryandApplicationtoRewardShaping.In EvolutionStrategies.In2008IEEECongressonEvolutionaryComputation(IEEE
ProceedingsoftheSixteenthInternationalConferenceonMachineLearning(ICML WorldCongressonComputationalIntelligence).3381–3387. https://doi.org/10.
’99).MorganKaufmannPublishersInc.,SanFrancisco,CA,USA,278–287. 1109/CEC.2008.4631255
[42] OlleNilsson.2021.QDgym.https://github.com/ollenilsson19/QDgym.
[43] OlleNilssonandAntoineCully.2021. PolicyGradientAssistedMAP-Elites.
InProceedingsoftheGeneticandEvolutionaryComputationConference(Lille,
France)(GECCO’21).AssociationforComputingMachinery,NewYork,NY,USA,
866–875. https://doi.org/10.1145/3449639.3459304
[44] OpenAI,IlgeAkkaya,MarcinAndrychowicz,MaciekChociej,MateuszLitwin,
BobMcGrew,ArthurPetron,AlexPaino,MatthiasPlappert,GlennPowell,
RaphaelRibas,JonasSchneider,NikolasTezak,JerryTworek,PeterWelinder,
LilianWeng,QimingYuan,WojciechZaremba,andLeiZhang.2019. Solving
Rubik’sCubewithaRobotHand.arXivpreprint(2019).
[45] PaoloPagliuca,NicolaMilano,andStefanoNolfi.2020. EfficacyofModern
Neuro-EvolutionaryStrategiesforContinuousControlOptimization.Frontiers
inRoboticsandAI7(2020),98. https://doi.org/10.3389/frobt.2020.00098
[46] JackParker-Holder,AldoPacchiano,KrzysztofMChoromanski,andStephenJ
Roberts.2020. EffectiveDiversityinPopulationBasedReinforcementLearn-
ing. In Advances in Neural Information Processing Systems, H. Larochelle,
M.Ranzato,R.Hadsell,M.F.Balcan,andH.Lin(Eds.),Vol.33.CurranAs-
sociates,Inc.,18050–18062. https://proceedings.neurips.cc/paper/2020/file/
d1dc3a8270a6f9394f88847d7f0050cf-Paper.pdf
[47] XueBinPeng,MarcinAndrychowicz,WojciechZaremba,andPieterAbbeel.
2018.Sim-to-RealTransferofRoboticControlwithDynamicsRandomization.In
2018IEEEInternationalConferenceonRoboticsandAutomation(ICRA).3803–3810.
https://doi.org/10.1109/ICRA.2018.8460528
[48] PourchotandSigaud.2019.CEM-RL:Combiningevolutionaryandgradient-based
methodsforpolicysearch.InInternationalConferenceonLearningRepresentations.
https://openreview.net/forum?id=BkeU5j0ctQ
[49] JustinK.Pugh,LisaB.Soros,andKennethO.Stanley.2016.QualityDiversity:
ANewFrontierforEvolutionaryComputation. FrontiersinRoboticsandAI3
(2016),40. https://doi.org/10.3389/frobt.2016.00040
[50] NemanjaRakicevic,AntoineCully,andPetarKormushev.2021.PolicyManifold
Search:ExploringtheManifoldHypothesisforDiversity-BasedNeuroevolution.
InProceedingsoftheGeneticandEvolutionaryComputationConference(Lille,
France)(GECCO’21).AssociationforComputingMachinery,NewYork,NY,USA,
901–909. https://doi.org/10.1145/3449639.3459320
[51] TimSalimans,JonathanHo,XiChen,SzymonSidor,andIlyaSutskever.2017.
Evolution Strategies as a Scalable Alternative to Reinforcement Learning.
arXiv:1703.03864[stat.ML]
[52] TomSchaul,DanielHorgan,KarolGregor,andDavidSilver.2015.UniversalValue
FunctionApproximators.InProceedingsofthe32ndInternationalConferenceon
MachineLearning(ProceedingsofMachineLearningResearch,Vol.37),Francis
BachandDavidBlei(Eds.).PMLR,Lille,France,1312–1320. https://proceedings.
mlr.press/v37/schaul15.html
[53] JohnSchulman,SergeyLevine,PieterAbbeel,MichaelJordan,andPhilippMoritz.
2015. TrustRegionPolicyOptimization.InProceedingsofthe32ndInterna-
tionalConferenceonMachineLearning(ProceedingsofMachineLearningResearch,
Vol.37),FrancisBachandDavidBlei(Eds.).PMLR,Lille,France,1889–1897.
https://proceedings.mlr.press/v37/schulman15.html
[54] JohnSchulman,FilipWolski,PrafullaDhariwal,AlecRadford,andOlegKlimov.
2017. ProximalPolicyOptimizationAlgorithms. CoRRabs/1707.06347(2017).
arXiv:1707.06347 http://arxiv.org/abs/1707.06347
[55] RichardS.SuttonandAndrewG.Barto.2018.ReinforcementLearning:AnIntro-
duction(seconded.).TheMITPress. http://incompleteideas.net/book/the-book-
2nd.html
[56] YunhaoTang.2021. GuidingEvolutionaryStrategieswithOff-PolicyActor-
Critic.InProceedingsofthe20thInternationalConferenceonAutonomousAgents
andMultiAgentSystems(VirtualEvent,UnitedKingdom)(AAMAS’21).Interna-
tionalFoundationforAutonomousAgentsandMultiagentSystems,Richland,
SC,1317–1325.
[57] BryonTjanaka,MatthewC.Fontaine,YulunZhang,SamSommerer,Nathan
Dennler,andStefanosNikolaidis.2021.pyribs:Abare-bonesPythonlibraryfor
qualitydiversityoptimization.https://github.com/icaros-usc/pyribs.
1111