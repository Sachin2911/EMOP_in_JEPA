# ROSARL



---

## Page 1

ReinforcementLearningConference(August2024)
ROSARL: Reward-Only Safe Reinforcement Learning
GeraudNangueTasse1,TamlinLove1,2,MarkNemecek3,StevenJames1&BenjaminRosman1
1SchoolofComputerScienceandAppliedMathematics,UniversityoftheWitwatersrand
2InstitutdeRobòticaiInformáticaIndustrial,UniversidadPolitécnicadeCataluna
3DepartmentofComputerScience,DukeUniversity
tlove@iri.upc.edu,mark.nemecek@duke.edu
{geraud.nanguetasse1,steven.james,benjamin.rosman1}@wits.ac.za
Abstract
Animportantprobleminreinforcementlearningisdesigningagentsthatlearntosolvetasks
safelyinanenvironment.Acommonsolutionistodefineeitherapenaltyinthereward
functionoracosttobeminimisedwhenreachingunsafestates.However,designingreward
or cost functions is non-trivial and can increase with the complexity of the problem. To
addressthis,weinvestigatetheconceptofaMinmaxpenalty,thesmallestpenaltyforunsafe
statesthatleadstosafeoptimalpolicies,regardlessoftaskrewards.Wederiveanupperand
lowerboundonthispenaltybyconsideringbothenvironmentdiameterandcontrollability.
Additionally,weproposeasimplealgorithmforagentstoestimatethispenaltywhilelearning
taskpolicies.Ourexperimentsdemonstratetheeffectivenessofthisapproachinenabling
agentstolearnsafepoliciesinhigh-dimensionalcontinuouscontrolenvironments.
1 Introduction
Reinforcementlearning(RL)hasrecentlyachievedsuccessacrossavarietyofdomains,suchasvideogames
(Shaoetal.,2019),robotics(Kalashnikovetal.,2018;Kahnetal.,2018)andautonomousdriving(Kiran
etal.,2021).However,ifwehopetodeployRLintherealworld,agentsmustbecapableofcompletingtasks
whileavoidingunsafeorcostlybehaviour.Forexample,anavigatingrobotmustavoidcollidingwithobjects
andactorsaroundit,whilesimultaneouslylearningtosolvetherequiredtask.Figure1showsanexample.
Many approaches in RL deal with this problem by allocating arbitrary penalties to unsafe states when
hand-craftingtherewardfunction.However,theproblemofspecifyingarewardfunctionfordesirable,safe
behaviourisnotoriouslydifficult(Amodeietal.,2016).Importantly,penaltiesthataretoosmallmayresult
inunsafebehaviour,whilepenaltiesthataretoolargemayresultinincreasedlearningtimes. Furthermore,
TRPO TRPO Lagrangian CPO TRPO Minmax (Ours)
Figure1:Exampletrajectoriesofpriorwork—TRPO(Schulmanetal.,2015)(left-most),TRPO-Lagrangian
(Rayetal.,2019)(middle-left),CPO(Achiametal.,2017)(middle-right)—comparedtoours(right-most)in
theSafetyGymdomain(Rayetal.,2019).Foreach,apointmassagentlearnstoreachagoallocation(green
cylinder)whileavoidingunsaferegions(bluecircles).Thecyanblockisarandomlyplacedmovableobstacle.
Ourapproachlearnssaferpoliciesthanthebaselines,andworksbysimplychangingtherewardsreceivedfor
enteringunsaferegionstoalearnedpenalty(keepingtherewardsreceivedforallothertransitionsunchanged).
1


---

## Page 2

ReinforcementLearningConference(August2024)
theserewardsmustbespecifiedbyanexpertforeachnewtaskanagentfaces.Ifouraimistodesigntruly
autonomous,generalagents,itisthensimplyimpracticaltorequirethatahumandesignerspecifypenaltiesto
guaranteeoptimalbutsafebehavioursforeverytask.
Whensafetyisanexplicitgoal,acommonapproachistoconstrainpolicylearningaccordingtosomethreshold
on cumulative cost (Schulman et al., 2015; Ray et al., 2019; Achiam et al., 2017). While effective, these
approachesrequirethedesignofacostfunctionwhosespecificationcanbeaschallengingasdesigninga
rewardfunction.Additionally,thesemethodsmaystillresultinunacceptablyfrequentconstraintviolationsin
practice,duetothelargecostthresholdtypicallyused.SeeAppendixCforfurtherdiscussionofrelatedworks.
Ratherthanattemptingtobothmaximisearewardfunctionandminimiseacostfunction,whichrequires
specifyingbothrewardsandcostsandanewlearningobjective,weshouldsimplyaimtohaveabetterreward
function—sincewethendonothavetospecifyyetanotherscalarsignalnorchangethelearningobjective.This
approachisconsistentwiththerewardhypothesis(Sutton&Barto,2018)whichstates:“Allofwhatwemean
bygoalsandpurposescanbewellthoughtofasmaximisationoftheexpectedvalueofthecumulativesum
ofareceivedscalarsignal(reward).”Therefore,thequestionweexamineinthisworkishowtodetermine
theMinmaxpenalty—thesmallestpenaltyassignedtounsafestatessuchthattheprobabilityofreachingsafe
goalsismaximisedbyanoptimalpolicy.Ratherthanrequiringanexpert’sinput,weshowthatthispenaltycan
beboundedbytakingintoaccountthediameterandcontrollabilityofanenvironment,andapracticalestimate
ofitcanbelearnedbyanagentusingitscurrentvalueestimates.Wemakethefollowingmaincontributions:
(i) BoundingtheMinmaxpenalty(Section3.3):Weobtaintheanalyticalformofanupperandlower
boundontheMinmaxpenaltyandprovethatusingtheupperboundresultsinlearnedbehaviours
thatminimisetheprobabilityofvisitingunsafestates(Theorem2);Wealsoshowthatthesebounds
canbeaccuratelyestimatedusingpolicyevaluation(Sutton&Barto,2018)(Theorem1).
(ii) Learning safe policies (Section 4): We show that accurately estimating the Minmax penalty or
boundsisNP-hard(Theorem3).Hence,weproposeasimplemodel-freealgorithmforlearninga
practicalestimateoftheMinmaxpenaltywhilelearningthetaskpolicy.Sincetheapproachonly
modifiestherewardsforunsafetransitionswiththeestimatedpenalty(keepingtherewardsforother
transitionsunchanged),itcanbeintegratedintoanyRLpipelinethatlearnsvaluefunctions.
(iii) Experiments (Section 5): Finally, we investigate the behaviour of agents that only rely on their
learnedMinmaxpenaltytosolvetaskssafely.Ourresultsdemonstratethatthesereward-onlyagents
arecapableoflearningtosolvetaskswhileavoidingunsafestates.Additionally,whilepriormethods
oftenviolatesafetyconstraints,weobservethatreward-onlyagentsconsistentlylearnsaferpolicies.
2 Background
WeconsiderthetypicalRLsettingwherethetaskfacedbyanagentismodelledbyaMarkovDecisionProcess
(MDP).AnMDPisdefinedasatuple⟨S,A,P,R⟩,whereS isafinitesetofstates,Aisafinitesetofactions,
P :S×A×S →[01]isthetransitionprobabilityfunction,andR:S×A×S →[R R ]isthereward
MIN MAX
function. Our focus is on undiscounted MDPs that model stochastic shortest path problems (Bertsekas &
Tsitsiklis,1991)inwhichanagentmustreachsomegoalsinthenon-emptysetofabsorbingstatesG ⊂Swhile
avoidingunsafeabsorbingstatesG! ⊂G.Thesetofnon-absorbingstatesS\Garereferredtoasinternalstates.
Wewillalsorefertothetuple⟨S,A,P⟩astheenvironment,andtheMDP⟨S,A,P,R⟩asatasktobesolved.
Apolicyπ :S →Aisamappingfromstatestoactions.ThevaluefunctionVπ(s)=E[ P∞ R(s ,a ,s )]
t=0 t t t+1
associatedwithapolicyspecifiestheexpectedreturnunderthatpolicystartingfromstates.Thegoalofan
agentistolearnanoptimalpolicyπ∗ thatmaximisesthevaluefunctionVπ∗(s) = V∗(s) = max Vπ(s)
π
foralls ∈ S.Sincetasksareundiscounted,π∗ isguaranteedtoexistbyassumingthatthevaluefunction
ofimproperpoliciesisunboundedfrombelow—whereproperpoliciesarethosethatareguaranteedtoreach
anabsorbingstate(VanNiekerketal.,2019).Sincetherealwaysexistsadeterministicπ∗(Sutton&Barto,
1998),andπ∗isproper,wewillfocusourattentiononthesetofalldeterministicproperpoliciesΠ.
2


---

## Page 3

ReinforcementLearningConference(August2024)
3 AvoidingUnsafeAbsorbingStates
Givenanenvironment,weaimtoboundthesmallestpenalty(hencethelargestreward)touseasfeedbackfor
unsafetransitionstoguaranteesafeoptimalpolicies.Weformallydefineasafepolicyasaproperpolicythat
minimisestheprobabilityofreachinganyunsafeterminalstates:
Definition1 Consideranenvironment⟨S,A,P⟩.Wheres isthefinalstateofatrajectoryandG! ⊂G isthe
T
non-emptysetofunsafeabsorbingstates,letPπ(s ∈G!)betheprobabilityofreachingG!fromsundera
s T
properpolicyπ ∈Π.sThenπiscalledsafeif π ∈argminPπ′(s ∈G!) foralls∈S.
s T
π′∈Π
Remark1 Since proper policies reach G, Definition 1 equivalently says that safe policies are those that
maximisetheprobabilityofreachingsafegoalstatesG\G!.Sinceoptimalpoliciesarealsoproper,thismeans
that safe optimal policies also maximise the probability of reaching G \G!. For example, looping forever
inanon-absorbingregionofthestatespaceisneitherproper,norsafe,noroptimal.
We now define the Minmax penalty R as the largest reward for unsafe transitions that lead to safe
Minmax
optimalpolicies:
Definition2 Consider an environment ⟨S,A,P⟩ where task rewards R(s,a,s′) are bounded by
[R R ] for all s′ ̸∈ G!. Let π∗ be an optimal policy for one such task ⟨S,A,P,R⟩. We define the
MIN MAX
MinmaxpenaltyofthisenvironmentasthescalarR ∈Rthatsatisfiesthefollowing:
Minmax
(i) IfR(s,a,s′)<R foralls′ ∈G!,thenπ∗issafeforallR;
Minmax
(ii) IfR(s,a,s′)>R forsomes′ ∈G!reachablefromS\G,thenthereexistsanRs.t.π∗isunsafe.
Minmax
3.1 AMotivatingExample:TheChain-WalkEnvironment
Toillustratethedifficultyindesigningrewardfunctionsforsafebehaviour,considerthesimplechain-walk
environmentinFigure2a.Itconsistsoffourstatess , s ,s , s whereG ={s , s }andG! ={s }.The
0 1 2 3 1 3 1
agenthastwoactionsa ,a ,theinitialstateiss ,andthediagramdenotesthetransitionprobabilities.Task
1 2 0
rewardsforsafetransitionsareboundedby[R R ]=[−10].Theabsorbingtransitionshaveareward
MIN MAX
of0whileallothertransitionshavearewardofR =−1,andtheagentmustreachthegoalstate s ,but
step 3
nottheunsafestate s .Hence,thequestionhereiswhatpenaltytogivefortransitionsfroms into s such
1 0 1
thattheoptimalpoliciesaresafe.Figures2b-2dexemplifyhowtoolargepenaltiesresultinlongerconvergence
times,whiletoosmallonesresultinunsafepolicies,demonstratingtheneedtofindtheMinmaxpenalty.
a1/a2 s3
w.p.
a
(
1
1
/a
−
2
p2)
s2
w
a
.
1
p
/
.
a
p
2
2
a1w.p.(1−p1) w.p a . 2 p1
a1
w.p.p1
a1/a2 s1 a2 s0
w.p.(1−p1) p1=p2 [01]
(a)Chain-walk
]001
[
ytlaneP
1.0
0.8
0.6
0.4
0.2
0.0 Rstep [ 10]
(b) Failure rates with
R =−1
step
]001
[
ytlaneP
1.0
0.8
0.6
0.4
0.2
0.0 Rstep [ 10]
(c)Failurerateswith
p =p =0.4
1 2
]001
[
ytlaneP
140
120 100
80
60
40
(d) Total timesteps
withp =p =0.4
1 2
Figure2:Theeffectofdifferentpenaltiesforunsafetransitions(s to s )onoptimalpoliciesinthechain-walk
0 1
environment.(a)Thetransitionprobabilitiesofthechain-walkenvironment(wherep ,p ∈[01]);(b)The
1 2
failurerateforeachpenaltyin[−100]andeachtransitionprobabilities(p =p ∈[01]),withataskreward
1 2
ofR =−1;(c)Thefailurerateforeachpenaltyin[−100]andeachtaskrewardin[−10],withtransition
step
probabilitiesgivenbyp =p =0.4;(d)Thetotaltimestepsneededtolearnoptimalpoliciestoconvergence
1 2
(usingvalueiteration(Sutton&Barto,1998))foreachpenaltyin[−100]andeachtaskrewardin[−10],with
transitionprobabilitiesgivenbyp =p =0.4.Theblackdashedlinesin(b)and(c)showtheMinmaxpenalty.
1 2
3


---

## Page 4

ReinforcementLearningConference(August2024)
Sincethetransitionsperactionarestochastic,controlledbyp ,p ∈[01],and s isfurtherfromthestartstate
1 2 3
s than s ,theagentmaynotalwaysbeabletoavoid s .Infact,forp =p =0and−1penaltyfortransi-
0 1 1 1 2
tionsinto s ,theoptimalpolicyistoalwayspicka whichalwaysreaches s .Forasufficientlyhighpenalty
1 2 1
forreaching s (anypenaltyhigherthan−2),theoptimalpolicyistoalwayspickactiona ,whichalways
1 1
reaches s .However,forp =p =0.4(Figure2c),ahigherpenaltyisrequiredfora tostayoptimal.Tocap-
3 1 2 1
turethisrelationshipbetweenthestochasticityofanenvironmentandtherequiredpenaltytoobtainsafepolicies,
weintroduceanotionofcontrollability,whichmeasurestheabilityofanagenttoreachsafegoals.Additionally,
observethatasp increases,theprobabilitythattheagentcantransitionfroms to s decreases—thereby
2 2 3
increasingthenumberoftimestepsspenttoreachthegoal.Therefore,thepenaltyfor s mustalsoconsider
1
theenvironment’sdiametertoensureanoptimalpolicywillnotsimplyreach s toavoidself-transitionsins .
1 2
3.2 OntheDiameterandControllabilityofEnvironments
Clearly,thesizeofthepenaltythatneedstobegivenforunsafestatesdependsonthesizeoftheenvironment.
Wedefinethissizeasthediameteroftheenvironment,whichisthehighestexpectedtimestepstoreachan
absorbingstatefromaninternalstatewhenfollowingaproperpolicy:
Definition3 DefinethediameterofanenvironmentasD := max maxE[T(s ∈G|π)],whereT(s ∈
T T
s∈S\G π∈Π
G|π)isthetimestepstakentoreachG fromswhenfollowingaproperpolicyπ.
Giventhediameterofanenvironment,apossiblenaturalchoicefortherewardforunsafestatesistogive
a penalty that is as large as receiving the smallest task reward for the longest path to safe goal states:
R¯ :=R D′, where D′ is the diameter for safe policies D′ := max maxE(cid:2) T(s ∈G\G!|π) (cid:3) .
MAX MIN T
s∈S\G π∈Π
However,whileR¯ aimstomakereachingunsafestatesworsethanreachingsafegoals,itdoesnotconsider
MAX
thecontrollabilityofanenvironment,northepossibilitythatanunsafepolicyreceivesR everywhereinits
MAX
trajectory.Wecanformallydefinethecontrollabilityofanenvironmentasfollows:
Definition4 DefinethedegreeofcontrollabilityasC := min min Pπ(s ̸∈G!).
s T
s∈S\G π∈Π
Ps π(sT̸∈G!)̸=0
C measuresthedegreeofcontrollabilityoftheenvironmentbysimplytakingthesmallestnon-zeroprobability
ofreachingsafegoalstatesbyfollowingaproperpolicy.Forexample,ifthedynamicsaredeterministic,then
anydeterministicpolicyπwilleitherreachasafegoalornot.Thatis,Pπ(s ̸∈G!)willeitherbe0or1.Since
s T
werequirePπ(s ̸∈G!)̸=0,itmustbethatC =1.Consider,forexample,thechain-walkenvironmentwith
s T
differentchoicesforp.Sinceactionsins donotaffectthetransitionprobability,thereareonly2relevant
2
d P e
s
π t
1
e 2( rm s
T
in ̸∈ ist G ic !) po = lic p i
1
e 1 s ( π p 1
2
( = s) 1 = ).H a 1 er a e n , d C π = 2 (s 1 ) w = he a n 2 . p
1
Th = is p g
2
iv = es 0 P b s π e 1 1 c ( a s u T se ̸∈ th G e ! t ) as = ki ( s 1 d − ete p r 1 m )1 in ( i p s 2 tic = an 1 d ) a s n
3
d
isreachable.C thentendsto0.5asp andp getscloserto0.5,makingtheenvironmentuniformlyrandom.
1 2
Finally,theenvironmentisnotcontrollablewhenp=1since s isunreachablefroms .
3 2
Remark2 WecanthinkofC =0asthelimitofC whensafegoalsareunreachable.
Giventhediameterandcontrollabilityofanenvironment,wecannowdefineachoicefortheMinmaxpenalty
thattakesintoaccountbothD,C,andR :R¯ :=(R −R )D.Thischoiceofpenaltysaysthat
MAX MIN MIN MAX C
sincestochasticshortestpathtasksrequireanagenttolearntoachievedesiredterminalstates,iftheagent
enters an unsafe terminal state, it should receive the largest penalty possible by a proper policy. We now
investigatetheeffectofthesepenaltiesonthefailurerateofoptimalpolicies.
3.3 OntheFailureRateofOptimalPolicies
Webeginbyproposingasimplemodel-basedalgorithmforestimatingthediameterandcontrollability,from
whichthepenaltiesarethenobtained.Wedescribethemethodhereandpresentthepseudo-codeinAlgorithm
4


---

## Page 5

ReinforcementLearningConference(August2024)
p1=p2 [01]
]001
[
ytlaneP
1.0
0.8
0.6
0.4
RMinmax 0.2 RMIN
RMAX
0.0 p1=0,p2 [01]
(a)R =−1
step
]001
[
ytlaneP
1.0
0.8
0.6
0.4
RMinmax 0.2 RMIN
RMAX
0.0 p2=0,p1 [01]
(b)R =−1
step
]001
[
ytlaneP
1.0
0.8
0.6
0.4
RMinmax 0.2 RMIN
RMAX
0.0 Rstep [ 10]
(c)R =−1
step
]001
[
ytlaneP
1.0
0.8
0.6
0.4
RMinmax 0.2 RMIN
RMAX
0.0 Rstep [ 10]
(d)p =p =0.4
1 2
]001
[
ytlaneP
1.0
0.8
0.6
0.4
RMinmax 0.2 RMIN
RMAX
0.0 Rstep [ 10]
(e)p =0,p =0.4
1 2
]001
[
ytlaneP
1.0
0.8
0.6
0.4
RMinmax 0.2 RMIN
RMAX
0.0
(f)p =0.4,p =0
1 2
Figure3:Failureratesofoptimalpoliciesinthechain-walkenvironment.Weshowtheeffectofstochasticity
(p andp )andtaskrewards(R )onthebounds(R¯ andR¯ )oftheMinmaxpenalty(R ).The
1 2 step MIN MAX Minmax
controllabilityanddiameterfortheboundsareestimatedusingAlgorithm1.
1inAppendixB.Here,thediameterisestimatedasfollows:(i)Foreachdeterministicpolicyπ,estimateits
expectedtimestepsT(s ∈G)(orT(s ∈G\G!)forD′)byusingpolicyevaluation(Sutton&Barto,2018)
T T
withrewardsof1atallinternalstates;(ii)Then,calculateD usingtheequationinDefinition3.Similarly,
thecontrollabilityisestimatedbyestimatingthereachprobabilityPπ(s ̸∈G!)ofeachdeterministicpolicy
s T
πusingrewardsof1fortransitionsintosafegoalstatesandzerorewardsotherwise.Thisapproachconverges
viatheconvergenceofpolicyevaluation(Theorem1).
Theorem1(Estimation) Algorithm1convergestoDandC foranygivencontrollableenvironment.
Figure 3 shows the result of applying this algorithm in the chain-walk MDP. Here, R is compared
Minmax
toaccountingforD only(R¯ )andaccountingforbothC andD (R¯ ).Interestingly,wecanobserve
MAX MIN
R¯ ≤ R and R¯ ≥ R consistently, highlighting how considering the diameter only is
MIN Minmax MAX Minmax
insufficienttoguaranteesafeoptimalpolicies.ItalsoindicatesthatthesepenaltiesmayboundR in
Minmax
general.WeshowinTheorem2thatthisisindeedthecase.
Theorem2(SafetyBounds) Consider a controllable environment where task rewards are bounded by
[R R ] foralls′ ̸∈G!.ThenR¯ ≤R ≤R¯ .
MIN MAX MIN Minmax MAX
Theorem 2 says that for any MDP whose rewards for unsafe transitions are bounded above by R¯ , the
MIN
optimal policy both minimises the probability of reaching unsafe states and maximises the probability of
reachingsafegoalstates.Hence,anypenaltyR¯ −ϵ,whereϵ>0canbearbitrarilysmall,willguarantee
MIN
safe optimal policies. Similarly, the theorem shows that any reward higher than R¯ may have optimal
MAX
policiesthatdonotminimisetheprobabilityofreachingunsafestates.ThesecanbeobservedinFigure3.
ThefiguredemonstrateswhyconsideringboththediameterandcontrollabilityofanMDPisnecessaryto
guaranteesafepolicies,becausethediameteralonedoesnotalwaysminimisethefailurerate.
4 PracticalAlgorithmforLearningSafePolicies
WhiletheMinmaxpenaltyofanMDPcanbeaccuratelyestimatedusingpolicyevaluation(Algorithm1),
itrequiresknowledgeoftheenvironmentdynamics(oranestimateofit).Thesearedifficultquantitiesto
estimatefromanagent’sexperience,whichisfurthercomplicatedbytheneedtoalsolearnthetrueoptimal
policyfortheestimatedMinmaxpenalty.Hence,obtaininganaccurateestimateoftheMinmaxpenaltyis
impracticalinmodel-freeandfunctionapproximationsettingswherethestateandactionspacesarelarge.
Infact,itisNP-hardsinceitdependsonthediameter,whichrequiressolvingalongest-pathproblem.
Theorem3(Complexity) EstimatingtheMinmaxpenaltyR accuratelyisNP-hard.
Minmax
Given the above challenges, we require a practical method for learning the Minmax penalty. Ideally, this
methodshouldrequirenoknowledgeoftheenvironmentdynamicsandshouldeasilyintegratewithexistingRL
approaches.Toachievethis,wefirstnotethat(R −R )D =(DR −DR )1 =(V −V )1,
MIN MAX C MIN MAX C MIN MAX C
whereV andV arethevaluefunctionbounds.Hence,apracticalestimateoftheMinmaxpenaltycanbe
MIN MAX
efficientlylearnedbyestimatingthevaluegapV −V usingobservationsoftherewardandtheagent’s
MIN MAX
5


---

## Page 6

ReinforcementLearningConference(August2024)
estimateofthevaluefunction.Wedescribethemethodhereandpresentthepseudo-codeinAlgorithm2in
AppendixB.ThisalgorithmrequiresinitialestimatesofR andR ,whichinthisworkareinitialisedto0.
MIN MAX
Theagentreceivesarewardr aftereachenvironmentinteractionandupdatesitsestimateoftherewardbounds
t
R ← min(R ,r )andR ← max(R ,r ),thevalueboundsV ← min(V ,R ,V(s ))
MIN MIN t MAX MAX t MIN MIN MIN t
andV ←max(V ,R ,V(s )),andtheMinmaxpenaltyR¯ ←V −V ,whereV(s )isthe
MAX MAX MAX t MIN MIN MAX t
learnedvaluefunctionattimestept.SincethecontrollabilityCisalsoexpensivetoestimate,itisnotexplicitly
consideredinthisestimateofR¯ .Instead,giventhatthemainpurposeofC istomakeR¯ morenegative
MIN MIN
themorestochastictheenvironmentis,wenoticethatthisisalreadyachievedinpracticebytherewardand
valueestimates.SinceR isestimatedusingR ←min(R ,r ),theneverytimetheagententersan
MIN MIN MIN t
unsafestate,wehavethat:r ←R¯ ,R ←R¯ ,andthenR¯ ←R¯ −V .Thismeansthatwhen
t MIN MIN MIN MIN MIN MAX
theestimatedV isgreaterthanzero,thepenaltyestimateR¯ becomemorenegativeeverytimetheagent
MAX MIN
entersanunsafestate.Finally,wheneveranagentencountersanunsafestate,therewardr isreplacedby
t
R¯ todisincentiviseunsafebehaviour.SinceV isestimatedusingV ←max(V ,R ,V(s )),
MIN MAX MAX MAX MAX t
itleadstoanoptimisticestimationofR¯ .Hence,weobservenoneedtoaddanϵ>0toR¯ .
MIN MIN
5 Experiments
WhilethetheoreticalMinmaxpenaltyisguaranteedtoleadtooptimalsafepolicies,itisunclearwhetherthis
alsoholdsforthepracticalestimateproposedinSection4.Hence,thissectionaimstoinvestigatethreemain
naturalquestionsregardingtheproposedpracticalalgorithm(seeAppendixDforadditionalexperiments):
How does Algorithm 2 (i) behave when the theoretical assumptions are satisfied? (ii) behave when the
theoreticalassumptionsarenotsatisfied?(iii)comparetopriorapproachestowardsSafeRL?Foreachresult,
wereportthemean(solidline)andonestandarddeviationaroundit(shadedregion).
5.1 HowdoesAlgorithm2behavewhenthetheoreticalassumptionsaresatisfied?
Domain(LAVAGRIDWORLD) Thisisasimplegridworldenvironmentwith11positions(|S|=11)and4
cardinalactions(|A|=4).TheagentheremustreachagoallocationGwhileavoidingalavalocationL(hence
G ={L,G}andG! ={L}).Awallisalsopresentintheenvironmentand,whilenotunsafe,mustbenavigated
around.Theenvironmenthasaslipprobability(sp),sothatwithprobabilitysptheagent’sactionisoverridden
witharandomaction.TheagentreceivesR =+1rewardforreachingthegoal,aswellasR =−0.1
MAX step
rewardateachtimesteptoincentivisetakingtheshortestpathtothegoal.Totestourapproach,wemodify
Q-learning(Watkins,1989)withϵ-greedyexplorationsuchthattheagentupdatesitsestimateoftheMinmax
penalty as learning progresses and uses it as the reward whenever the lava state is reached, following the
procedureoutlinedinSection4.Theaction-valuefunctionisinitialisedto0forallstatesandactions,ϵ=0.1
andthelearningrateα=0.1.Theexperimentsarerunover10,000episodesandaveragedover70runs.
SetupandResults WeexaminetheperformanceofourmodifiedQ-learningapproachacrossthreevalues
oftheslipprobabilityoftheLAVAGRIDWORLD.Aslipprobabilityof0representsafullydeterministicenvi-
ronment,whileaslipprobabilityof0.5representsamorestochasticenvironment.ResultsareplottedinFigure
4.Inthecaseofthefullydeterministicenvironment,theMinmaxpenaltyboundobtainedviaAlgorithm1is
R¯ =−9.9,sinceC =1andD =9.However,theagentisabletolearnarelativelysmallerpenalty(−1.1in
MIN
Figure4b)toconsistentlyminimisefailurerateandmaximisereturns(Figures4cand4d).Theresultingoptimal
policythenchoosestheshorterpaththatpassesnearthelavalocation(sp=0inFigure4a).Asthestochasticity
oftheenvironmentincreases,alargerpenaltyislearnedtoincentiviselonger,saferpolicies.Giventhestarting
positionoftheagentnexttothelava,thefailurerateinevitablyincreaseswithincreasedstochasticity.Theresult-
ingoptimalpolicythenchoosesthelongerpaththatpassestotheleftofthecentrewall(sp=0.25andsp=0.5
inFigure4a).Wecan,therefore,concludethatwhilethereisagapbetweenthetrueMinmaxpenaltyandtheone
learnedviaAlgorithm2,thisalgorithmcanstilllearnoptimalsafepolicieswhenthetheoreticalsettingholds.
5.2 HowdoesAlgorithm2behavewhenthetheoreticalassumptionsarenotsatisfied?
Domain(SafetyGym PILLAR) ThisisacustomSafetyGymenvironment(Rayetal.,2019),inwhich
thesimplepointrobotmustnavigatetoagoallocation  aroundalargepillar  (henceG = {  ,  }and
6


---

## Page 7

ReinforcementLearningConference(August2024)
5.0=ps 52.0=ps 0=ps 1.25 1.50 1.75 2.00
2.25 2.50 2.75 0.0 0.2 0.4 0.6 0.8 1.0
episode 1e5
(a)Trajectories
seitlanep 0.3 s s p p = = 0 0.25 0.2 sp=0.5
0.1 0.0 0.0 0.2 0.4 0.6 0.8 1.0
episode 1e5
(b)Learnedpenalty
seruliaf sp=0 0.75 s s p p = = 0 0 . . 2 5 5 0.50 0.25 0.00 0.25
0.50 0.75 1.000.0 0.2 0.4 0.6 0.8 1.0
episode 1e5
(c)Failurerate
snruter
sp=0 sp=0.25 sp=0.5
(d)Averagereturns
Figure4:EffectofincreaseintheslipprobabilityoftheLAVAGRIDWORLDonthelearnedMinmaxpenalty
andcorrespondingfailurerateandreturns.Theblackcirclein(a)representstheagent.
G! ={  }).JustasinRayetal.(2019),theagentusespseudo-lidartoobservethedistancetoobjectsaround
it(|S| = R60),andtheactionspaceiscontinuousovertwoactuatorscontrollingthedirectionandforward
velocity(|A|=R2).Thegoal,pillar,andagentlocationsremainunchangedforallepisodes.Thediscount
factorisγ =0.99,andtheagentisrewardedforreachingthegoal(witharewardof1)aswellasformoving
towardsit(thedefaultdensedistance-basedreward).Eachepisodeterminatesoncetheagentreachesthegoal
orcollideswiththepillar(witharewardof−1).Otherwise,episodesterminateafter1000timesteps.This
domaindoesnotsatisfytheshortestpathsettingweassumesince:itisdiscounted,optimalpoliciesarenot
guaranteedtoreachG andpoliciesthatdonotreachG arenotguaranteedtohavevaluefunctionsthatare
unboundedfrombelow(duetothedenserewards).Totestourapproachinthissetting,wemodifyTRPO
(Schulmanetal.,2015)(denotedTRPO-Minmax)tousetheestimateoftheMinmaxpenaltyasdescribed
inAlgorithm2.Theexperimentsarerunover10millionstepsandaveragedover10runs.
SetupandResults WeexaminetheperformanceofTRPO-MinmaxforfivelevelsofnoiseinthePILLAR
environment,similarlytotheexperimentsinSection5.1.Here,thevalueofthenoisedenotesthenumber
bywhicharandomactionvectorisscaledbeforevectoradditionwiththeagent’saction.Resultsareplottedin
Figure5.WeobservesimilarresultstoSection5.1,wheretheagentusesitslearnedMinmaxpenalty(Figure
5b)tosuccessfullylearnsafepolicies(Figure5c)whilesolvingthetask(Figure5d),usingsaferpathsformore
noisydynamics(Figure5a).Interestingly,italsocorrectlyprioritiseslowfailurerateswhenthedynamics
aretoonoisytosafelyreachthegoal(noise≥5).Wecan,therefore,concludethatAlgorithm2canlearnsafe
policiesevenindiscountedhigh-dimensionalcontinuous-controldomainsrequiringfunctionapproximation.
noise = 0.0 noise = 2.5 noise = 5.0 noise = 7.5 noise = 10.0
0
noise=5 100
200
300
noise=0 400
500 noise=2.5 2 4 6 8
TotalEnvInteracts 1e6
(a)Trajectories
ytlanePegarevA
0.8
0.6
0.4
0.2
0.0 2 4 6 8
TotalEnvInteracts 1e6
(b)Learnedpenalty
tsoCpEegarevA
4
3
2
1
0
1
2 2 4 6 8
TotalEnvInteracts 1e6
(c)Failurerate
teRpEegarevA
(d)Averagereturns
Figure5:PerformanceofTRPO-MinmaxinthePILLARenvironmentwithvaryingnoiselevels.
5.3 HowdoesAlgorithm2comparetopriorapproachestowardsSafeRL?
Baselines AsabaselinerepresentativeoftypicalRLapproaches,weuseTrustRegionPolicyOptimisation
(TRPO)(Schulmanetal.,2015).Torepresentconstraint-basedapproaches,wecompareagainstConstrained
PolicyOptimisation(CPO)(Achiametal.,2017),TRPOwithLagrangianconstraints(TRPO-Lagrangian)(Ray
etal.,2019),andSautéRLwithTRPO(Sauté-TRPO)(Sootlaetal.,2022).AllbaselinesexceptSauté-TRPO
use the implementations provided by Ray et al. (2019), and form a set of widely used baselines in safety
domains(Zhangetal.,2020;Sootlaetal.,2022;Yangetal.,2023).Sauté-TRPOusestheimplementation
provided by Sootla et al. (2022). As in Ray et al. (2019), all approaches use feed-forward MLPs, value
7


---

## Page 8

ReinforcementLearningConference(August2024)
networksofsize(256,256),andtanhactivationfunctions.Thecostthresholdfortheconstrainedalgorithms
issetto0,thebestwefound.Theexperimentsarerunover10millionepisodesandaveragedover10runs.
SetupandResults WecomparetheperformanceofTRPO-Minmaxtothatofthebaselinesfordifferentlevels
ofnoiseinthePILLARdomain.Figure6showstheresults.Weobservethatinthedeterministiccasenoise=0,
allthealgorithmsachievesimilarperformance(exceptSauté-TRPO),successfullymaximisingreturns(Figure
6dtop)whileminimisingthefailurerates(Figure6ctop).However,inthestochasticcasenoise=2.5,wecan
observethatallthebaselinesexceptSauté-TRPOachievesignificantlyhighreturns(Figure6dbottom)atthe
expenseofarapidlyincreasingcumulativecost(Figure6bbottom).Theseresultsarealsoconsistentwiththe
benchmarksofRayetal.(2019)wherethecumulativecostofTRPOisgreaterthanthatofTRPO-Lagrangian,
whichisgreaterthanthatofCPO.Interestingly,Sauté-TRPOistheworst-performingofallthebaselines.It
successfullymaximisesreturnswhileminimisingcostonlyforthedeterministicenvironment(noise=0),but
completelyfailsforthestochasticone(noise=2.5).Finally,byexaminingtheepisodelength(Figure6a)and
failurerates(Figure6c)forallthebaselinesinthestochasticcase,wecanconcludethattheyhavealllearned
riskypoliciesthatmaximiserewardsovershorttrajectoriesthatarehighlylikelytoresultincollisions.Wealso
provideadditionalresultsintheappendixfornoise≥5(Figures9-11)tofurtherdemonstratethispoint.In
contrast,theresultsobtainedshowthatTRPO-Minmaxsuccessfullymaximisesreturnswhileminimisingcost
forbothdeterministicandstochasticenvironments.Inaddition,whenthenoiselevelistoohighnoise≥5,
TRPO-Minmaxconsistentlyprioritisesmaintaininglowfailureratesovermaximisingreturns.
TRPO TRPO Lagrangian CPO SauteTRPO TRPO Minmax (Ours)
1000
800
600
400
200
0
2 4 6 8
TotalEnvInteracts 1e6
neLpE
1100
1000
900
800 700
600
500
400
300
2 4 6 8
TotalEnvInteracts 1e6
neLpE
7000
6000 5000
4000
3000
2000
1000
0
2 4 6 8
TotalEnvInteracts 1e6
(a)Episodelength
tsoCevitalumuC
12000
10000
8000 6000
4000
2000
0
2 4 6 8
TotalEnvInteracts 1e6
tsoCevitalumuC
1.0
0.8
0.6
0.4
0.2
0.0
0.2
2 4 6 8
TotalEnvInteracts 1e6
(b)Cumulativecost
tsoCpEegarevA
0.8
0.6
0.4
0.2
0.0
2 4 6 8
TotalEnvInteracts 1e6
tsoCpEegarevA
4
3 2
1
0 1
2
3
4
2 4 6 8
TotalEnvInteracts 1e6
(c)Failurerate
teRpEegarevA
3
2
1
0
1
2
2 4 6 8
TotalEnvInteracts 1e6
teRpEegarevA
(d)Averagereturns
Figure6:ComparisonwithbaselinesinthePILLARenvironment.(top)noise=0,(bottom)noise=2.5.
6 DiscussionandFutureWork
ThispaperinvestigatesanewapproachtowardssafeRLbyaskingthequestion:Isascalarrewardenoughto
solvetaskssafely?Toanswerthisquestion,weboundtheMinmaxpenalty,whichtakesintoaccountthediame-
terandcontrollabilityofanenvironmentinordertominimisetheprobabilityofencounteringunsafestates.We
provethatthepenaltydoesindeedminimisethisprobability,andpresentamethodthatusesanagent’svalue
estimatestolearnanestimateofthepenalty.Ourresultsintabularandhigh-dimensionalcontinuoussettings
havedemonstratedthat,byencodingthesafebehaviourdirectlyintherewardfunctionviatheMinmaxpenalty,
agentsareabletosolvetaskswhileprioritisingsafety,learningsaferpoliciesthanpopularconstraint-basedap-
proaches.Finally,whileweshowthatscalarrewardsareindeedenoughforsafeRL,thecurrentanalysisisonly
applicabletounsafeterminalstates—whichonlycoverstasksthatcanbenaturallyrepresentedbystochastic-
shortestpathMDPs.GiventhatotherpopularRLsettingslikediscountedMDPscanbeconvertedtostochastic
shortestpathMDPs(Bertsekas,1987;Sutton&Barto,1998),apromisingfuturedirectioncouldbetofindthe
dualofourresultsforothertheoreticallyequivalentsettings.Inconclusion,weseethisreward-onlyapproachas
apromisingdirectiontowardstrulyautonomousagentscapableofindependentlylearningtosolvetaskssafely.
8


---

## Page 9

ReinforcementLearningConference(August2024)
References
JoshuaAchiam,DavidHeld,AvivTamar,andPieterAbbeel. Constrainedpolicyoptimization. InInternational
ConferenceonMachineLearning,pp.22–31.PMLR,2017.
MohammedAlshiekh,RoderickBloem,RüdigerEhlers,BettinaKönighofer,ScottNiekum,andUfukTopcu.
Safereinforcementlearningviashielding. InProceedingsoftheAAAIConferenceonArtificialIntelligence,
volume32,2018.
EitanAltman. ConstrainedMarkovdecisionprocesses:stochasticmodeling. Routledge,1999.
Dario Amodei, Chris Olah, Jacob Steinhardt, Paul Christiano, John Schulman, and Dan Mané. Concrete
problemsinAIsafety. arXivpreprintarXiv:1606.06565,2016.
DimitriPBertsekas. DynamicProgramming:Determinist.andStochast.Models. Prentice-Hall,1987.
DimitriPBertsekasandJohnNTsitsiklis. Ananalysisofstochasticshortestpathproblems. Mathematicsof
OperationsResearch,16(3):580–595,1991.
YinlamChow,OfirNachum,EdgarDuenez-Guzman,andMohammadGhavamzadeh. ALyapunov-based
approachtosafereinforcementlearning. AdvancesinNeuralInformationProcessingSystems,31,2018.
GalDalal,KrishnamurthyDvijotham,MatejVecerik,ToddHester,CosminPaduraru,andYuvalTassa. Safe
explorationincontinuousactionspaces. arXivpreprintarXiv:1801.08757,2018.
RatiDevidze,GoranRadanovic,ParameswaranKamalaruban,andAdishSingla. Explicablerewarddesign
forreinforcementlearningagents. AdvancesinNeuralInformationProcessingSystems,34:20118–20131,
2021.
Aria HasanzadeZonuzy, Archana Bura, Dileep Kalathil, and Srinivas Shakkottai. Learning with safety
constraints:SamplecomplexityofreinforcementlearningforconstrainedMDPs. InProceedingsofthe
AAAIConferenceonArtificialIntelligence,volume35,pp.7667–7674,2021.
GregoryKahn,AdamVillaflor,BosenDing,PieterAbbeel,andSergeyLevine. Self-superviseddeeprein-
forcementlearningwithgeneralizedcomputationgraphsforrobotnavigation. In2018IEEEInternational
ConferenceonRoboticsandAutomation(ICRA),pp.5129–5136.IEEE,2018.
DmitryKalashnikov,AlexIrpan,PeterPastor,JulianIbarz,AlexanderHerzog,EricJang,DeirdreQuillen,
EthanHolly,MrinalKalakrishnan,VincentVanhoucke,etal. Scalabledeepreinforcementlearningfor
vision-basedroboticmanipulation. InConferenceonRobotLearning,pp.651–673.PMLR,2018.
BRaviKiran,IbrahimSobh,VictorTalpaert,PatrickMannion,AhmadAAlSallab,SenthilYogamani,and
Patrick Pérez. Deep reinforcement learning for autonomous driving: A survey. IEEE Transactions on
IntelligentTransportationSystems,2021.
Zachary C Lipton, Kamyar Azizzadenesheli, Abhishek Kumar, Lihong Li, Jianfeng Gao, and Li Deng.
Combatingreinforcementlearning’sSisypheancursewithintrinsicfear. arXivpreprintarXiv:1611.01211,
2016.
AndrewYNg,DaishiHarada,andStuartRussell. Policyinvarianceunderrewardtransformations:Theoryand
applicationtorewardshaping. InInternationalConferenceonMachineLearning,volume99,pp.278–287,
1999.
Alex Ray, Joshua Achiam, and Dario Amodei. Benchmarking Safe Exploration in Deep Reinforcement
Learning. 2019.
John Schulman, Sergey Levine, Pieter Abbeel, Michael Jordan, and Philipp Moritz. Trust region policy
optimization. InInternationalConferenceonMachineLearning,pp.1889–1897.PMLR,2015.
KunShao,ZhentaoTang,YuanhengZhu,NannanLi,andDongbinZhao. Asurveyofdeepreinforcement
learninginvideogames. arXivpreprintarXiv:1912.10944,2019.
9


---

## Page 10

ReinforcementLearningConference(August2024)
SatinderSingh,RichardLLewis,andAndrewGBarto. Wheredorewardscomefrom? InProceedingsofthe
AnnualConferenceoftheCognitiveScienceSociety,pp.2601–2606.CognitiveScienceSociety,2009.
Aivar Sootla, Alexander I Cowen-Rivers, Taher Jafferjee, Ziyan Wang, David H Mguni, Jun Wang, and
Haitham Ammar. Sauté RL: Almost surely safe reinforcement learning using state augmentation. In
InternationalConferenceonMachineLearning,pp.20423–20443.PMLR,2022.
Adam Stooke, Joshua Achiam, and Pieter Abbeel. Responsive safety in reinforcement learning by PID
Lagrangianmethods. InInternationalConferenceonMachineLearning,pp.9133–9143.PMLR,2020.
RichardSuttonandAndrewBarto. Introductiontoreinforcementlearning,volume135. MITpressCambridge,
1998.
RichardSuttonandAndrewBarto. Reinforcementlearning:Anintroduction. MITpress,2018.
GuyTennenholtz,NadavMerlis,LiorShani,ShieMannor,UriShalit,GalChechik,AssafHallak,andGal
Dalal. Reinforcementlearningwithaterminator. AdvancesinNeuralInformationProcessingSystems,35:
35696–35709,2022.
BenjaminVanNiekerk,StevenJames,AdamEarle,andBenjaminRosman. Composingvaluefunctionsin
reinforcementlearning. InInternationalConferenceonMachineLearning,pp.6401–6409.PMLR,2019.
NolanCWagener,ByronBoots,andChing-AnCheng. Safereinforcementlearningusingadvantage-based
intervention. InInternationalConferenceonMachineLearning,pp.10630–10640.PMLR,2021.
C.Watkins. Learningfromdelayedrewards. PhDthesis,King’sCollege,Cambridge,1989.
Tsung-YenYang,JustinianRosca,KarthikNarasimhan,andPeterJRamadge. Projection-basedconstrained
policyoptimization. arXivpreprintarXiv:2010.03152,2020.
YujieYang,YuxuanJiang,YichenLiu,JianyuChen,andShengboEbenLi. Model-freesafereinforcement
learningthroughneuralbarriercertificate. IEEERoboticsandAutomationLetters,8(3):1295–1302,2023.
YimingZhang,QuanVuong,andKeithRoss. Firstorderconstrainedoptimizationinpolicyspace. Advances
inNeuralInformationProcessingSystems,33:15338–15349,2020.
10


---

## Page 11

ReinforcementLearningConference(August2024)
A ProofsofTheoreticalResults
Theorem1(Estimation) Algorithm1convergestoDandC foranygivencontrollableenvironment.
Proof Thisfollowsfromtheconvergenceguaranteeofpolicyevaluation(Sutton&Barto,1998).
Theorem2(SafetyBounds) Consider a controllable environment where task rewards are bounded by
[R R ] foralls′ ̸∈G!.ThenR¯ ≤R ≤R¯ .
MIN MAX MIN Minmax MAX
Proof Letπ∗beanoptimalpolicyforanarbitrarytask⟨S,A,P,R⟩intheenvironment.Giventhedefinition
oftheMinmaxpenalty(Definition2),weneedtoshowthefollowing:
(i) IfR(s,a,s′)<R¯ foralls′ ∈G!,thenπ∗issafeforallR;and
MIN
(ii) IfR(s,a,s′)>R¯ forsomes′ ∈G!reachablefromS\G,thenthereexistsanRs.t.π∗isunsafe.
MAX
(i)Sinceπ∗isoptimal,itisalsoproperandhencemustreachG.
Assumeπ∗isunsafe.Thenthereexistsanotherproperpolicyπthatissafe,suchthat
Pπ(s ∈G!)<Pπ∗ (s ∈G!) forsomes∈S.
s T s T
Then,
Vπ∗ (s)≥Vπ(s)
" ∞ # " ∞ #
=⇒Eπ∗ X R(s ,a ,s ) ≥Eπ X R(s ,a ,s )
s t t t+1 s t t t+1
t=0 t=0
=⇒Eπ∗(cid:2) GT−1+R(s ,a ,s ) (cid:3) ≥Eπ(cid:2) GT−1+R(s ,a ,s ) (cid:3) ,
s T T T+1 s T T T+1
T−1
X
whereGT−1 = R(s ,a ,s )andT isarandomvariabledenotingwhens ∈G.
t t t+1 T+1
t=0
=⇒Eπ∗(cid:2) GT−1(cid:3) + (cid:16) Pπ∗ (s ̸∈G!)R(s ,a ,s )+Pπ∗ (s ∈G!)R¯ (s ,a ,s ) (cid:17)
s s T T T T+1 s T unsafe T T T+1
≥Eπ(cid:2) GT−1(cid:3) + (cid:0) Pπ(s ̸∈G!)R(s ,a ,s )+Pπ(s ∈G!)R¯ (s ,a ,s ) (cid:1) ,
s s T T T T+1 s T unsafe T T T+1
whereR¯ denotestherewardsfortransitionsintoG!anda =π∗(s ).
unsafe T T
=⇒Eπ∗(cid:2) GT−1(cid:3) + (cid:16) Pπ∗ (s ̸∈G!)R(s ,a ,s )+R¯ (s ,a ,s ) (cid:17)
s s T T T T+1 unsafe T T T+1
≥Eπ(cid:2) GT−1(cid:3) + (cid:0) Pπ(s ̸∈G!)R(s ,a ,s )+Pπ(s ∈G!)R¯ (s ,a ,s ) (cid:1) ,
s s T T T T+1 s T unsafe T T T+1
=⇒Eπ∗(cid:2) GT−1(cid:3) + (cid:0) 1−Pπ(s ∈G!) (cid:1) R¯ (s ,a ,s )
s s T unsafe T T T+1
≥Eπ(cid:2) GT−1(cid:3) + (cid:16) Pπ(s ̸∈G!)−Pπ∗ (s ̸∈G!) (cid:17) R(s ,a ,s )
s s T s T T T T+1
=⇒Eπ∗(cid:2) GT−1(cid:3) + (cid:0) 1−Pπ(s ∈G!) (cid:1) R¯
s s T MIN
>Eπ(cid:2) GT−1(cid:3) + (cid:16) Pπ(s ̸∈G!)−Pπ∗ (s ̸∈G!) (cid:17) R(s ,a ,s ),
s s T s T T T T+1
sinceR¯ (s ,a ,s )<R¯ .
unsafe T T T+1 MIN
=⇒Eπ∗(cid:2) GT−1(cid:3) + (cid:0) 1−Pπ(s ∈G!) (cid:1) (R −R ) D
s s T MIN MAX C
>Eπ(cid:2) GT−1(cid:3) + (cid:16) Pπ(s ̸∈G!)−Pπ∗ (s ̸∈G!) (cid:17) R(s ,a ,s )
s s T s T T T T+1
=⇒Eπ∗(cid:2) GT−1(cid:3)
+(R −R )D
s MIN MAX
>Eπ(cid:2) GT−1(cid:3) + (cid:16) Pπ(s ̸∈G!)−Pπ∗ (s ̸∈G!) (cid:17) R(s ,a ,s ), usingdefinitionofC.
s s T s T T T T+1
11


---

## Page 12

ReinforcementLearningConference(August2024)
=⇒Eπ∗(cid:2) GT−1(cid:3)
−R D
s MAX
>Eπ(cid:2) GT−1(cid:3) + (cid:16) Pπ(s ̸∈G!)−Pπ∗ (s ̸∈G!) (cid:17) R(s ,a ,s )−R D
s s T s T T T T+1 MIN
=⇒Eπ∗(cid:2) GT−1(cid:3)
−R D >0,
s MAX
sinceEπ(cid:2) GT−1(cid:3) + (cid:16) Pπ(s ̸∈G!)−Pπ∗ (s ̸∈G!) (cid:17) R(s ,a ,s )≥R D
s s T s T T T T+1 MIN
=⇒Eπ∗(cid:2) GT−1(cid:3)
>R D.
s MAX
But this is a contradiction since the expected return of following an optimal policy up to a terminal state
without the reward for entering the terminal state must be less than receiving R for every step of the
MAX
longestpossibletrajectorytoG.Hencewemusthaveπ∗ ∈argminPπ(s ∈G!).
s T
π
(ii)Assumeπ∗issafe.Then,Pπ∗(s ̸∈G!)≥Pπ′(s ̸∈G!)foralls∈S,π′ ∈Π.
s T s T
Letπbethepolicythatmaximisestheprobabilityofreachings′ ∈G!fromsomestates∈G.Then,similarly
to(i),wehave
Vπ∗ (s)≥Vπ(s)
=⇒Eπ∗(cid:2) GT−1(cid:3) + (cid:16) Pπ∗ (s ∈G!)−Pπ(s ∈G!) (cid:17) R¯ (s ,a ,s )
s s T s T unsafe T T T+1
≥Eπ(cid:2) GT−1(cid:3) + (cid:16) Pπ(s ̸∈G!)−Pπ∗ (s ̸∈G!) (cid:17) R(s ,a ,s )
s s T s T T T T+1
=⇒Eπ(cid:2) GT−1(cid:3) + (cid:16) Pπ(s ∈G!)−Pπ∗ (s ∈G!) (cid:17) R¯ (s ,a ,s )
s s T s T unsafe T T T+1
≤Eπ∗(cid:2) GT−1(cid:3) + (cid:16) Pπ∗ (s ̸∈G!)−Pπ(s ̸∈G!) (cid:17) R(s ,a ,s )
s s T s T T T T+1
=⇒Eπ(cid:2) GT−1(cid:3) + (cid:16) Pπ(s ∈G!)−Pπ∗ (s ∈G!) (cid:17) R¯
s s T s T MAX
<Eπ∗(cid:2) GT−1(cid:3) + (cid:16) Pπ∗ (s ̸∈G!)−Pπ(s ̸∈G!) (cid:17) R(s ,a ,s ), sinceR¯ >R¯ .
s s T s T T T T+1 unsafe MAX
=⇒Eπ(cid:2) GT−1(cid:3) + (cid:16) Pπ(s ∈G!)−Pπ∗ (s ∈G!) (cid:17) R D′
s s T s T MIN
<Eπ∗(cid:2) GT−1(cid:3) + (cid:16) Pπ∗ (s ̸∈G!)−Pπ(s ̸∈G!) (cid:17) R(s ,a ,s ), bydefinitionofR¯ .
s s T s T T T T+1 MAX
=⇒Eπ(cid:2) GT−1(cid:3) +R D′
s MIN
<Eπ∗(cid:2) GT−1(cid:3) + (cid:16) Pπ∗ (s ̸∈G!)−Pπ(s ̸∈G!) (cid:17) R(s ,a ,s )
s s T s T T T T+1
=⇒Eπ(cid:2) GT−1(cid:3) +R D′ <0
s MIN
ButthisisacontradictionwhenRissuchthattheagentreceivesarewardofR ≥|R |D′atleastonce
MAX MIN
initstrajectorywhenfollowingπandzeroeverywhereelse.
Theorem3(Complexity) EstimatingtheMinmaxpenaltyR accuratelyisNP-hard.
Minmax
Proof ThisfollowsfromtheNP-hardnessoflongest-pathproblems.SincetheMinmaxpenaltyisboundedby
R¯ andR¯ ,botharedefinedbythediameter,whichisinturndefinedastheexpectedtotaltimestepsof
MIN MAX
thelongestpath.
12


---

## Page 13

ReinforcementLearningConference(August2024)
B Algorithms
Algorithm1:EstimatingtheDiameterandControllability
Input :⟨S,A,P⟩,R (s′):=1(s′ ̸∈G),R (s,a,s′):=1(s̸∈G ands′ ∈G\G!)
D C
Initialise:DiameterD =0,ControllabilityC =1,ValuefunctionsVπ(s)=0,Vπ(s)=0,Error∆=1
D C
forπ ∈Πdo forπ ∈Πdo
/*PolicyevaluationforD*/ /*PolicyevaluationforC*/
while∆>0do while∆>0do
∆←0 ∆←0
fors∈S do fors∈S do
v′← P P(s′|s,π(s))(R D (s′)+V D π(s′)) v′← P P(s′|s,π(s))(R C (s,π(s),s′)+V C π(s′))
s′ s′
V ∆ D π = (s m )← ax{ v ∆ ′ ,|V D π(s)−v′|} ∆ V C π = (s m )← ax{ v ∆ ′ ,|V C π(s)−v′|}
endfor endfor
endwhile endwhile
fors∈S do fors∈S do
D =max{D,V D π(s)} C =min{C,V C π(s)}ifV C π(s)̸=0elseC
endfor endfor
endfor endfor
Algorithm2:RLwhilelearningMinmaxpenalty
Input :RLalgorithmA,maxtimestepsT
Initialise: R =0,R =0,V =R ,V =R ,πandV asperA
MIN MAX MIN MIN MAX MAX
fortinTdo
observeastates ,takeanactiona usingπasperA,andobserves ,r
t t t+1 t
R ,R ←min(R ,r ),max(R ,r )
MIN MAX MIN t MAX t
V ,V ←min(V ,R ,V(s )),max(V ,R ,V(s ))
MIN MAX MIN MIN t MAX MAX t
R¯ ←V −V
MIN MIN MAX
r ←R¯ if s ∈G! else r
t MIN t+1 t
updateπandV with(s ,a ,s ,r )asperA
t t t+1 t
endfor
13


---

## Page 14

ReinforcementLearningConference(August2024)
C RelatedWork
Rewardshaping:TheproblemofdesigningrewardfunctionstoproducedesiredpoliciesinRLsettingsiswell-
studied(Singhetal.,2009).Particularfocushasbeenplacedonthepracticeofrewardshaping,inwhichan
initialrewardfunctionprovidedbyanMDPisaugmentedinordertoimprovetherateatwhichanagentlearns
thesameoptimalpolicy(Ngetal.,1999;Devidzeetal.,2021).Whilesacrificingsomeoptimality,otherap-
proacheslikeLiptonetal.(2016)proposeshapingrewardsusinganideaofintrinsicfear.Here,theagenttrainsa
supervisedfearmodelrepresentingtheprobabilityofreachingunsafestatesinafixedhorizon,scalessaidprob-
abilitiesbyafearfactor,andthensubtractsthescaledprobabilitiesfromQ-learningtargets.Theseapproaches
differfromoursinthattheyseektofindrewardfunctionsthatimproveconvergencewhilepreservingtheopti-
malityfromaninitialrewardfunction.Incontrast,weseektodeterminetheoptimalrewardsforterminalstates
inordertominimiseundesirablebehavioursirrespectiveoftheoriginalrewardfunctionandoptimalpolicy.
ConstrainedRL:DisincentivisingorpreventingundesirablebehavioursiscoretothefieldofsafeRL.A
popularapproachistodefineconstraintsonthebehaviourofanagent,taskingtheagentwithlimitingthe
accumulationofcostsassociatedwithviolatingsafetyconstraintswhilesimultaneouslymaximisingreward
(Altman, 1999; Achiam et al., 2017; Chow et al., 2018; Ray et al., 2019; HasanzadeZonuzy et al., 2021).
Widelyusedexamplesoftheseapproachesincludeconstrainedpolicyoptimisation(CPO)(Achiametal.,
2017),whichaugmentsTRPO(Schulmanetal.,2015)withconstraintstosatisfyaconstrainedMDP,and
TRPO-Lagrangian(Rayetal.,2019),whichcombinesLagrangianmethodswithTRPO.Anotherexampleis
SautéRL(Sootlaetal.,2022),whichincorporatesthecostfunctionintotherewardsandaugmentsthestatewith
theremaining"costbudget"spentbyviolatingsafetyconstraints.Otherconstraint-basedapproachesinclude
Projection-basedCPO(Yangetal.,2020),whichprojectsaTRPOpolicyontoaspacedefinedbyconstraints,
andPIDLagrangianmethods(Stookeetal.,2020),whichaugmentLagrangianmethodswithPIDcontrol.
Shielding:Anotherimportantlineofworkinvolvesrelyingoninterventionsfromamodel(Dalaletal.,2018;
Wageneretal.,2021)orhuman(Tennenholtzetal.,2022)topreventunsafeactionsfrombeingconsideredbythe
agent(shieldingtheagent)orpreventtheenvironmentfromexecutingthoseunsafeactionsbycorrectingthem
(shieldingtheenvironment).Otherapproachesherealsolookatusingtemporallogicstodefineorenforcesafety
constraintsontheactionsconsideredorselectedbytheagent(Alshiekhetal.,2018).Theseapproachesfitseam-
lesslyintoourproposedreward-onlyframeworksincetheyareprimarilyaboutmodificationsonthetransition
dynamicsandnottherewardfunction—forexample,unsafeactionsherecansimplyleadtounsafegoalstates.
14


---

## Page 15

ReinforcementLearningConference(August2024)
D AdditionalExperimentsandFigures
TRPO TRPO Lagrangian CPO SauteTRPO TRPO Minmax (Ours)
7000
6000 5000
4000
3000
2000
1000
0
2 4 6 8
TotalEnvInteracts 1e6
tsoCevitalumuC
1000
800
600
400
200
0
2 4 6 8
TotalEnvInteracts 1e6
(a)Cumulativecost
neLpE
1.0
0.8
0.6
0.4
0.2
0.0
0.2
2 4 6 8
TotalEnvInteracts 1e6
(b)Episodelength
tsoCpEegarevA
4
3 2
1
0 1
2
3
4
2 4 6 8
TotalEnvInteracts 1e6
(c)Failurerate
teRpEegarevA
(d)Averagereturns
Figure7:PerformancecomparisonwithbaselinesinthePILLARenvironmentwithnoise=0.
12000
10000
8000 6000
4000
2000
0
2 4 6 8
TotalEnvInteracts 1e6
tsoCevitalumuC
1100
1000
900
800 700
600
500
400
300
2 4 6 8
TotalEnvInteracts 1e6
(a)Cumulativecost
neLpE
0.8
0.6
0.4
0.2
0.0
2 4 6 8
TotalEnvInteracts 1e6
(b)Episodelength
tsoCpEegarevA
3
2
1
0
1
2
2 4 6 8
TotalEnvInteracts 1e6
(c)Failurerate
teRpEegarevA
(d)Averagereturns
Figure8:PerformancecomparisonwithbaselinesinthePILLARenvironmentwithnoise=2.5.
10000
8000
6000
4000 2000
0
2 4 6 8
TotalEnvInteracts 1e6
tsoCevitalumuC
1000
900
800
700 600
500
2 4 6 8
TotalEnvInteracts 1e6
(a)Cumulativecost
neLpE
0.7
0.6 0.5
0.4
0.3 0.2 0.1
0.0
2 4 6 8
TotalEnvInteracts 1e6
(b)Episodelength
tsoCpEegarevA
2.5
2.0
1.5
1.0
0.5 0.0 0.5
1.0
2 4 6 8
TotalEnvInteracts 1e6
(c)Failurerate
teRpEegarevA
(d)Averagereturns
Figure9:PerformancecomparisonwithbaselinesinthePILLARenvironmentwithnoise=5.
8000
7000
6000 5000
4000
3000
2000
1000
0
2 4 6 8
TotalEnvInteracts 1e6
tsoCevitalumuC
1000
900
800
700
600
2 4 6 8
TotalEnvInteracts 1e6
(a)Cumulativecost
neLpE
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0.0
2 4 6 8
TotalEnvInteracts 1e6
(b)Episodelength
tsoCpEegarevA
0.4
0.2
0.0
0.2
0.4
0.6
0.8
2 4 6 8
TotalEnvInteracts 1e6
(c)Failurerate
teRpEegarevA
(d)Averagereturns
Figure10:PerformancecomparisonwithbaselinesinthePILLARenvironmentwithnoise=7.5.
8000
6000
4000
2000
0
2 4 6 8
TotalEnvInteracts 1e6
tsoCevitalumuC
1000
900
800
700
600
500
2 4 6 8
TotalEnvInteracts 1e6
(a)Cumulativecost
neLpE
0.7
0.6 0.5
0.4
0.3
0.2
0.1
0.0
2 4 6 8
TotalEnvInteracts 1e6
(b)Episodelength
tsoCpEegarevA
0.75
0.50 0.25
0.00
0.25
0.50
0.75
2 4 6 8
TotalEnvInteracts 1e6
(c)Failurerate
teRpEegarevA
(d)Averagereturns
Figure11:PerformancecomparisonwithbaselinesinthePILLARenvironmentwithnoise=10.
15


---

## Page 16

ReinforcementLearningConference(August2024)
noise = 0.0 noise = 2.5 noise = 5.0 noise = 7.5 noise = 10.0
(a)TRPO.Failurespernoiselefttoright:0,0,1,1,1
3 3 3
(b)TRPO-Lagrangian.Failurespernoiselefttoright:0,1,1,1,1
3 3 3 3
(c)CPO.Failurespernoiselefttoright:0,0,1,1,1
3 3 3
(d)Sauté-RL.Failurespernoiselefttoright:0,1,1,1,1
3 3 3 3
(e)TRPO-Minmax.Failurespernoiselefttoright:0,0,0,1,0
3
Figure12:SampletrajectoriesofpolicieslearnedbyeachbaselineandourTRPO-Minmaxapproachinthe
SafetyGymPILLARenvironmentwithvaryingnoiselevels.Tosamplethetrajectoriesforeachnoiselevel,we
usethesamethreeenvironmentrandomseedsacrossallthealgorithms.
16


---

## Page 17

ReinforcementLearningConference(August2024)
(a)POINTGOAL1-HARD (b)POINTPUSH1-HARD
(c)POINTBUTTON1-HARD (d)CARBUTTON1-HARD
Figure13:AdditionalSafety-Gymdomains.(a)isamodifiedversionofthePOINTGOAL1taskfromOpenAI’s
SafetyGymenvironments(Rayetal.,2019),whichrepresentscomplex,high-dimensional,continuouscontrol
tasks. In all of the original domains, G = ∅ by default. We only modify POINTGOAL1 to make unsafe
transitionsterminalG =G! ={stateswithcost>0},leavingthesafegoalstatesnon-terminal(G\G! =∅).
Here,asimplerobotmustnavigatetoagoallocation  acrossa2Dplanewhileavoidingseveralhazards
(whereG =G! ={ }).Theagent’ssensors,actions,andrewardsareidenticaltothePILLARdomain.Unlike
thePILLARdomain,thegoal’slocationisrandomlyresetwhentheagentreachesit,butdoesnotterminatethe
episode.(b-d)aremodifiedsimilarlytothePOINTGOAL1-HARDenvironment.POINTPUSH1-HARDissimilar
toPOINTGOAL1-HARD,butwiththeadditionofapillarobstacle  andalargebox theagentmustpushto
thegoallocation  toreceivethegoalreward(whereG =G! ={ ,  }).Finally,POINTBUTTON1-HARD
andCARBUTTON1-HARDarealsosimilartoPOINTGOAL1-HARD,butwiththemorecomplexcarrobotfor
CARBUTTON1-HARDandtheadditionofthesetoboth:(i)Gremlins ,whicharedynamicobstaclesthat
movearoundtheenvironmentandmustbeavoided;and(ii)Buttons ,wheretheagentmustreachthegoal
buttonwithacylinder  toreceivethegoalreward(whereG =G! ={ , , }).
17


---

## Page 18

ReinforcementLearningConference(August2024)
TRPO TRPO Lagrangian CPO SauteTRPO TRPO Minmax (Ours)
1000
900
800
700
600 500
400
300
200
2 4 6 8
TotalEnvInteracts 1e6
neLpE
17500
15000
12500
10000
7500
5000
2500
0
2 4 6 8
TotalEnvInteracts 1e6
(a)Episodelength.
tsoCevitalumuC
1.0
0.8
0.6
0.4
0.2
0.0
2 4 6 8
TotalEnvInteracts 1e6
(b)Cumulativecost.
tsoCpEegarevA
(c)Failurerate (d)Averagereturns
Figure14:PerformanceinPOINTGOAL1-HARD(whereG =G! ={ }).Here,higherepisodelengthsare
better(inadditiontohigherreturns)sinceepisodesonlyterminatewhentheagentreachesahazardorafter
1000timesteps.SimilartoFigure6,allthebaselinesexceptSauté-RLachievesignificantlyhighreturnsat
theexpenseofarapidlyincreasingcumulativecost.Bycomparison,TRPO-Minmaxdramaticallyreduces
thefailureratewhilestillbeingabletosolvethetask,asobservedbyaveragereturnsachievedaswellasthe
trajectoriesobserved.However,returnsarelowersinceTRPO-Minmaxlearnssaferpathstothegoalsbutthe
denserewardfunctionincentivisesmovingtowardsthegoaldespitethelargenumberofhazardsin-between.
1000
900
800
700
600
2 4 6 8
TotalEnvInteracts 1e6
neLpE
6000
5000
4000
3000
2000
1000
0
2 4 6 8
TotalEnvInteracts 1e6
(a)Episodelength.
tsoCevitalumuC
0.7
0.6 0.5
0.4
0.3
0.2
0.1
0.0
2 4 6 8
TotalEnvInteracts 1e6
(b)Cumulativecost.
tsoCpEegarevA
4
2
0
2
4
6
2 4 6 8
TotalEnvInteracts 1e6
(c)Failurerate
teRpEegarevA
(d)Averagereturns
Figure15:PerformanceinPOINTPUSH1-HARD(whereG =G! ={ ,  }).Here,higherepisodelengthsare
better(inadditiontohigherreturns)sinceepisodesonlyterminatewhentheagentreachesahazardorafter
1000timesteps.SimilartoFigure6,thebaselinesachievesignificantlyhighreturnsattheexpenseofarapidly
increasingcumulativecostwhileTRPO-Minmaxconsistentlyprioritisesmaintaininglowfailurerates.
1000
800
600
400
200
2 4 6 8
TotalEnvInteracts 1e6
neLpE
50000
40000
30000
20000
10000
0
2 4 6 8
TotalEnvInteracts 1e6
(a)Episodelength.
tsoCevitalumuC
1.0
0.8
0.6
0.4
0.2
2 4 6 8
TotalEnvInteracts 1e6
(b)Cumulativecost.
tsoCpEegarevA
4
2
0
2
4
2 4 6 8
TotalEnvInteracts 1e6
(c)Failurerate
teRpEegarevA
(d)Averagereturns
Figure 16: Performance in POINTBUTTON1-HARD (where G = G! = { , , }). Here, higher episode
lengthsarebetter(inadditiontohigherreturns)sinceepisodesonlyterminatewhentheagentreachesahazard
orafter1000timesteps.SimilartoFigure6,thebaselinesachievesignificantlyhighreturnsattheexpenseofa
rapidlyincreasingcumulativecostwhileTRPO-Minmaxconsistentlyprioritisesmaintaininglowfailurerates.
1000
800
600
400
200
2 4 6 8
TotalEnvInteracts 1e6
neLpE
70000
60000 50000
40000
30000 20000
10000
0
2 4 6 8
TotalEnvInteracts 1e6
(a)Episodelength.
tsoCevitalumuC
1.0
0.8
0.6
0.4
0.2
0.0
2 4 6 8
TotalEnvInteracts 1e6
(b)Cumulativecost.
tsoCpEegarevA
2
1
0
1
2
3
2 4 6 8
TotalEnvInteracts 1e6
(c)Failurerate
teRpEegarevA
(d)Averagereturns
Figure17:PerformanceinCARBUTTON1-HARD(whereG =G! ={ , , }).Here,higherepisodelengths
arebetter(inadditiontohigherreturns)sinceepisodesonlyterminatewhentheagentreachesahazardorafter
1000timesteps.SimilartoFigure6,thebaselinesachievesignificantlyhighreturnsattheexpenseofarapidly
increasingcumulativecostwhileTRPO-Minmaxconsistentlyprioritisesmaintaininglowfailurerates.
18


---

## Page 19

ReinforcementLearningConference(August2024)
(a)TRPOsuccesses(top)andfailures(bottom)
(b)TRPO-Lagrangiansuccesses(top)andfailures(bottom)
(c)CPOsuccesses(top)andfailures(bottom)
(d)Sauté-RLsuccesses(top)andfailures(bottom)
(e)TRPO-Minmaxsuccesses(top)andfailures(bottom)
Figure18:SampletrajectoriesofpolicieslearnedbyeachbaselineandourMinmaxapproachintheSafety
GymPOINTGOAL1-HARDdomain,intheexperimentsofFigure14.Trajectoriesthathithazardsortakemore
than1000timestepstoreachthegoallocationareconsideredfailures.
19


---

## Page 20

ReinforcementLearningConference(August2024)
TRPO TRPO Lagrangian CPO SauteTRPO TRPO Minmax (Ours)
17500
15000
12500
10000
7500
5000
2500
0
2 4 6 8
TotalEnvInteracts 1e6
tsoCevitalumuC
1.0
0.8
0.6
0.4
0.2
0.0
2 4 6 8
TotalEnvInteracts 1e6
(a)Thecumulativecost.
tsoCpEegarevA
(b)Failurerate
1000
900
800
700
600
500
400
300
2 4 6 8
TotalEnvInteracts 1e6
neLpE
12.5
10.0
7.5
5.0
2.5
0.0
2.5
5.0
7.5
2 4 6 8
TotalEnvInteracts 1e6
(c)Averageepisodelength
teRpEegarevA
(d)Averagereturns
Figure19:ComparisonwithbaselinesinthePOINTGOAL1-HARDenvironment(whereG =G! ={ ,  }).
Here,higherepisodelengthsarebetter(inadditiontohigherreturns)sinceepisodesonlyterminatewhenthe
agentreachesahazardorafter1000timesteps.ThisexperimentissimilartoFigure14,butusesacostthreshold
of25forthebaselines(asinRayetal.(2019))tocheckitseffectontheperformanceofthebaselineswhen
episodesimmediatelyterminateatunsafestates.Wecanobservedrasticallyworsefailureratesandcumulative
costsforthebaselinescomparedtotheirperformanceinFigure14(wherethecostthresholdwas0).Similar
resultswereobtainedwhenusingacostthresholdof1.Theseshowhowsensitivesuchapproachesaretothe
costthreshold,whileareward-onlyapproachlikeTRPO-Minmaxdoesnotdependonsuchhyperparameters.
20


---

## Page 21

ReinforcementLearningConference(August2024)
(a)TRPOsuccesses(top)andfailures(bottom)
(b)TRPO-Lagrangiansuccesses(top)andfailures(bottom)
(c)CPOsuccesses(top)andfailures(bottom)
(d)Sauté-RLsuccesses(top)andfailures(bottom)
(e)TRPO-Minmaxsuccesses(top)andfailures(bottom)
Figure20:SampletrajectoriesofpolicieslearnedbyeachbaselineandourMinmaxapproachintheSafety
GymPOINTGOAL1-HARDdomain,intheexperimentsofFigure19.Trajectoriesthathithazardsortakemore
than1000timestepstoreachthegoallocationareconsideredfailures.
21


---

## Page 22

ReinforcementLearningConference(August2024)
TRPO TRPO Lagrangian CPO SauteTRPO TRPO Minmax (Ours)
600000
500000
400000
300000
200000
100000
0
2 4 6 8
TotalEnvInteracts 1e6
tsoCevitalumuC
120
100
80
60
40
20
0
2 4 6 8
TotalEnvInteracts 1e6
(a)Thecumulativecost.
tsoCpEegarevA
(b)Failurerate
1040
1020
1000
980
960
2 4 6 8
TotalEnvInteracts 1e6
neLpE
25
20
15
10
5
0
5
10
2 4 6 8
TotalEnvInteracts 1e6
(c)Averageepisodelength
teRpEegarevA
(d)Averagereturns
Figure21:ComparisonwithbaselinesintheoriginalSafetyGymPOINTGOAL1environment.Thisdomainis
thesameasPOINTGOAL1-HARD,exceptthatepisodesdonotterminatewhenahazardishit(henceevery
episodeonlyterminatesafter1000steps).Wesetthecostthresholdforthebaselinesto25asinRayetal.
(2019)ForTRPOMinmax,wereplacetherewardwiththeMinmaxpenaltyeverytimetheagentisinan
unsafestate(thatiseverytimethecostisgreaterthanzero),asinpreviousexperimentsandasperAlgorithm
2.WhileTRPOMinmaxstillbeatsthebaselinesinsafeexploration(a-b),itstrugglestomaximiserewards
whileavoidingunsafestates(d).
22


---

## Page 23

ReinforcementLearningConference(August2024)
(a)TRPOsuccesses(top)andfailures(bottom)
(b)TRPO-Lagrangiansuccesses(top)andfailures(bottom)
(c)CPOsuccesses(top)andfailures(bottom)
(d)Sauté-RLsuccesses(top)andfailures(bottom)
(e)TRPO-Minmaxsuccesses(top)andfailures(bottom)
Figure22:SampletrajectoriesofpolicieslearnedbyeachbaselineandourMinmaxapproachintheSafetyGym
POINTGOAL1-HARDdomain,intheexperimentsofFigure21.Trajectoriesthathithazards(thehitsarehigh-
lightedbytheredspheres)ortakemorethan1000timestepstoreachthegoallocationareconsideredfailures.
23