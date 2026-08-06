from __future__ import annotations

from .models import (
    Alignment,
    DetailBlock,
    DevelopmentUpdate,
    Game,
    Metric,
    Mode,
    Skill,
    SkillCategory,
    StoryBeat,
)


SUPER_SOLDIERS = Game(
    slug="super-soldiers",
    title="SUPER SOLDIERS",
    category="TACTICAL ACTION / PVP + PVE",
    tagline="Every second is a tactical decision.",
    pitch=(
        "A mobile-first Roblox combat game where players and bots fight through one "
        "server-owned simulation. Enter a focused 5v5 arena or hold the line in City of Zombies."
    ),
    long_description=(
        "Super Soldiers is built around compressed tactical consequence. The player must read space, "
        "commit to movement, preserve ammunition, understand cooldown windows, and coordinate with a "
        "team under time pressure. Competitive arena and cooperative survival are not separate technical "
        "products: they are two operational expressions of the same combat model, so every improvement "
        "to hit validation, movement authority, bot reasoning, readability, or mobile control strengthens both."
    ),
    accent="#76F3FF",
    accent_rgb=(118, 243, 255),
    status="AUTHORITY BETA",
    features=(
        ("One combat truth", "Damage, ammunition, reloads, cooldowns, skills, status, score and match state resolve through one server-owned simulation."),
        ("Readable pressure", "Strong silhouettes, bounded effects and deliberate feedback let players understand danger before spectacle overwhelms the fight."),
        ("Shared rules", "Players and bots enter the same damage, movement, targeting and scoring contracts instead of using incompatible shortcuts."),
        ("Two operations", "Competitive 5v5 and cooperative survival change the objective pressure without fragmenting the combat foundation."),
        ("Mobile-first control", "A fixed tactical camera, direct input vocabulary and constrained visual noise preserve precision on touch devices."),
        ("Deterministic pacing", "Match phases, respawns, overtime and PvE escalation run on bounded simulation rails rather than frame-rate-dependent authority."),
    ),
)

HEIST_CITY = Game(
    slug="heist-city",
    title="HEIST CITY",
    category="SYSTEMIC OPEN WORLD / CRIME + LAW",
    tagline="Every street takes a side.",
    pitch=(
        "A top-down city where traffic, police, criminals and vigilantes occupy the same world. "
        "Drive, chase, hack, investigate and decide what power means when the city pushes back."
    ),
    long_description=(
        "Heist City treats the city as a participant rather than scenery. Traffic density, police response, "
        "civilian behavior, wanted pressure, mission opportunities, evidence, vehicle condition and route choice "
        "all belong to one shared world. The flat rectangular street grid makes pursuit tactics legible: police can "
        "predict, intercept and contain; criminals can create misdirection and exploit mobility; vigilantes can act on "
        "information neither side fully controls. The goal is a systemic crime-and-law sandbox where actions create "
        "understandable consequences instead of isolated scripted reactions."
    ),
    accent="#FFB84D",
    accent_rgb=(255, 184, 77),
    status="CITY SYSTEMS ALPHA",
    features=(
        ("A city with memory", "Wanted pressure, traffic, witnesses, evidence and mission state react to the same server-authored history."),
        ("Systemic pursuit", "Police predict routes, cut across the grid, ram, contain and coordinate instead of following a single breadcrumb trail."),
        ("Physical traffic", "Server-owned vehicle proxies create shared occupancy and collision truth while clients render scalable visual models."),
        ("Three alignments", "Crime, law and vigilantism expose different information, incentives and consequences inside one simulation."),
        ("Progression with utility", "Hacking, combat, driving and intelligence skills change available decisions rather than merely increasing numbers."),
        ("A bounded city", "Autonomous servers simulate a measured population and clear area of responsibility instead of depending on global coordination."),
    ),
)


SUPER_MODES = (
    Mode(
        key="arena",
        title="5V5 ARENA",
        strapline="Ten combatants. One authoritative match.",
        player_fantasy=(
            "Enter a compact tactical arena where every movement exposes intent. Win by creating better angles, "
            "protecting team momentum and converting short windows of advantage before the opposing squad resets."
        ),
        description=(
            "The arena mode is designed for repeatable four-minute matches with clear phases, immediate team identity "
            "and decisive overtime. Bots fill empty positions and can assume abandoned roles, but they remain subject to "
            "the same combat and movement rules as human players. The result should feel fast without becoming arbitrary: "
            "players understand why a push succeeded, why a duel was lost and which decision can improve next round."
        ),
        objective=(
            "Control space, preserve combat resources and build a score advantage before the core timer expires. "
            "When regulation ends without resolution, overtime compresses the decision window and forces commitment."
        ),
        facts=("10 combatants", "4-minute core match", "6-second respawn", "Bot takeover on leave"),
        metrics=(
            Metric(label="Tempo", value=92),
            Metric(label="Teamplay", value=88),
            Metric(label="Precision", value=84),
            Metric(label="Pressure", value=79),
            Metric(label="Exploration", value=35),
        ),
        loop=(
            StoryBeat(code="01 / DEPLOY", title="Read the opening", description="Identify the first safe lane, the enemy formation and the most valuable early position before both teams fully commit."),
            StoryBeat(code="02 / CONTEST", title="Create local advantage", description="Use focus fire, timing and movement discipline to turn a balanced encounter into a temporary numerical or positional edge."),
            StoryBeat(code="03 / CONVERT", title="Spend momentum", description="Advance only as far as the team can support, convert eliminations into score, and deny the opponent a clean reset."),
            StoryBeat(code="04 / RESET", title="Rebuild the formation", description="Recover ammunition, cooldowns and spacing before the next contact instead of carrying a broken formation into another fight."),
            StoryBeat(code="05 / DECIDE", title="Commit under pressure", description="Use the final regulation or overtime window to make a coordinated decision rather than five disconnected individual plays."),
        ),
        systems=(
            DetailBlock(
                title="Server-sampled combat intent",
                summary="The client communicates intent; it does not report authoritative hits or outcomes.",
                description=(
                    "Combat input is sampled through server-authored actions and resolved inside the fixed simulation. "
                    "This keeps damage, ammunition, cooldowns and status transitions coherent across players, bots and latency conditions."
                ),
                bullets=("No client-authored hit truth", "One validation path for players and bots", "Fixed-step cooldown and reload timing", "Bounded replication of presentation state"),
            ),
            DetailBlock(
                title="Readable tactical camera",
                summary="The camera reveals the decision space without becoming another source of mechanical noise.",
                description=(
                    "The isometric/orbital presentation prioritizes nearby threats, team spacing and movement intention. "
                    "The camera avoids unnecessary vertical pitch and preserves a stable frame of reference on mobile."
                ),
                bullets=("Stable orientation", "Clear edge pressure", "Mobile-safe framing", "Reduced shake and occlusion"),
            ),
            DetailBlock(
                title="Authoritative match lifecycle",
                summary="Every phase has an explicit owner, transition and recovery path.",
                description=(
                    "Loading, countdown, regulation, overtime, finished state, respawn and bot substitution are supervised "
                    "as one match transaction. No client can advance the match or manufacture score state."
                ),
                bullets=("Explicit state machine", "Server-owned timer", "Deterministic overtime", "Bot fill and takeover"),
            ),
        ),
    ),
    Mode(
        key="zombies",
        title="CITY OF ZOMBIES",
        strapline="Hold the city. Adapt to the horde.",
        player_fantasy=(
            "Survive as a squad inside a collapsing city operation. Read the next threat, rescue a failing position, "
            "manage ammunition and decide when a defensive line is no longer worth holding."
        ),
        description=(
            "City of Zombies turns the same combat foundation into a cooperative pressure engine. Threat density rises, "
            "safe areas become temporary, and the squad must balance elimination speed against rescue timing and resource loss. "
            "The mode is not about infinite enemies alone; it is about the tactical consequences of being surrounded, separated or exhausted."
        ),
        objective=(
            "Maintain squad viability through escalating encounters, complete operational objectives and preserve enough "
            "combat capacity to survive the next pressure spike rather than merely the current wave."
        ),
        facts=("Cooperative survival", "Escalating waves", "Shared score pressure", "Adaptive bot support"),
        metrics=(
            Metric(label="Tempo", value=76),
            Metric(label="Teamplay", value=94),
            Metric(label="Precision", value=69),
            Metric(label="Pressure", value=96),
            Metric(label="Exploration", value=63),
        ),
        loop=(
            StoryBeat(code="01 / SECURE", title="Establish a temporary line", description="Clear immediate threats, identify escape directions and create enough space for the squad to make deliberate decisions."),
            StoryBeat(code="02 / SCAVENGE", title="Recover capability", description="Acquire ammunition, health and positional knowledge without dispersing beyond the squad's ability to support itself."),
            StoryBeat(code="03 / ESCALATE", title="Absorb the pressure spike", description="Respond to denser or more dangerous enemy composition by changing formation, target priority and movement tempo."),
            StoryBeat(code="04 / RESCUE", title="Protect the run", description="Decide whether to recover a downed ally, contain the threat first or abandon an unsalvageable location before the entire squad collapses."),
            StoryBeat(code="05 / RELOCATE", title="Leave before the city closes", description="Recognize when a position has consumed too many resources and move while a viable route still exists."),
        ),
        systems=(
            DetailBlock(
                title="Shared enemy authority",
                summary="PvE enemies use the same authoritative damage and movement contracts as competitive bots.",
                description=(
                    "Enemy pressure is generated through bounded server-owned work. Target selection, navigation intent, damage, "
                    "status and score remain visible and consistent to the entire squad."
                ),
                bullets=("Bounded spawn budgets", "Shared damage contracts", "Server-owned targeting", "Consistent crowd state"),
            ),
            DetailBlock(
                title="Escalation instead of noise",
                summary="Difficulty grows through tactical composition and pressure timing, not only raw enemy count.",
                description=(
                    "The mode can combine movement denial, rescue pressure, durable enemies and route collapse to create distinct "
                    "encounters while keeping the simulation measurable."
                ),
                bullets=("Composition-driven waves", "Threat-role diversity", "Explicit pressure phases", "Performance-aware density"),
            ),
            DetailBlock(
                title="Run continuity",
                summary="Every encounter changes the resources and options available in the next one.",
                description=(
                    "A successful fight can still be strategically expensive. Health, ammunition, positioning and squad cohesion "
                    "carry forward so the team must judge the cost of every hold and rescue."
                ),
                bullets=("Persistent resource pressure", "Meaningful rescue decisions", "Adaptive support bots", "Shared run score"),
            ),
        ),
    ),
)


ALIGNMENTS = (
    Alignment(
        key="criminal",
        title="CRIMINAL",
        code="UNDERWORLD / 01",
        fantasy="Build a crew that turns mobility, information and nerve into control of the city's illicit economy.",
        description=(
            "The criminal path begins with small jobs and limited leverage. As influence grows, the player must coordinate vehicles, "
            "safe routes, crew roles and timing while the police learn the organization’s habits. Success increases opportunity, but it "
            "also creates a more coherent adversary response: surveillance, targeted containment and pressure on predictable assets."
        ),
        objective="Convert risk into influence without allowing the city to close around the organization.",
        progression=(
            "Progression moves from opportunistic street work to organized operations. The player earns access to more ambitious jobs, "
            "specialized crew capability and stronger logistical options, but becomes easier to identify if the same methods are repeated."
        ),
        methods=("Route manipulation", "Crew coordination", "Vehicle theft and recovery", "Hacking and surveillance disruption", "Misdirection and false trails"),
        consequences=("Escalating wanted pressure", "Evidence accumulation", "Asset exposure", "More coordinated police doctrine", "Rival opportunity and betrayal"),
        accent="#FF764D",
        metrics=(
            Metric(label="Risk", value=94), Metric(label="Control", value=58),
            Metric(label="Mobility", value=88), Metric(label="Intel", value=64),
            Metric(label="Force", value=82),
        ),
        loop=(
            StoryBeat(code="01 / FIND", title="Identify an opportunity", description="Read the city for vulnerable routes, valuable targets and moments when law enforcement capacity is committed elsewhere."),
            StoryBeat(code="02 / PREPARE", title="Shape the operation", description="Choose vehicles, crew functions, escape options and digital interference before the first irreversible action."),
            StoryBeat(code="03 / EXECUTE", title="Create speed and confusion", description="Complete the objective while minimizing unnecessary evidence and preserving at least one viable exit strategy."),
            StoryBeat(code="04 / ESCAPE", title="Break prediction", description="Change route, vehicle or behavior before police convert partial information into containment."),
            StoryBeat(code="05 / CONSOLIDATE", title="Turn profit into influence", description="Invest rewards into capability while managing the exposure created by a growing organization."),
        ),
        systems=(
            DetailBlock(title="Heat and evidence", summary="Visible danger and durable investigative pressure are related but distinct.", description="Immediate wanted pressure governs pursuit intensity. Evidence persists beyond the chase and can make later operations easier to anticipate.", bullets=("Short-term heat", "Long-term evidence", "Witness and camera sources", "Methods become recognizable")),
            DetailBlock(title="Crew as capability", summary="A crew expands what can be attempted, but also increases coordination cost.", description="Drivers, combat specialists, hackers and scouts create new operation shapes. Poor sequencing or unclear roles can make a larger crew less effective than a disciplined small team.", bullets=("Role specialization", "Shared operation state", "Failure propagation", "Recovery and substitution")),
        ),
    ),
    Alignment(
        key="police",
        title="POLICE",
        code="DISPATCH / 02",
        fantasy="Turn incomplete information into coordinated containment while keeping the city moving around the incident.",
        description=(
            "Police gameplay is not a faster version of ordinary traffic AI. Officers must interpret dispatch information, infer likely routes, "
            "choose proportional tactics and coordinate units with different positions. Pursuit can involve ramming and roadblocks, but the best "
            "outcome is a controlled arrest produced by prediction rather than indefinite tail-following."
        ),
        objective="Turn information and positioning into a controlled arrest rather than a chaotic chase.",
        progression=(
            "Progression expands situational awareness and command authority. The player moves from responding to local incidents toward coordinating "
            "multi-unit pursuit, evidence-led investigation and area containment without treating every event as maximum-force combat."
        ),
        methods=("Dispatch interpretation", "Route prediction", "Rolling roadblocks", "Pursuit intervention", "Evidence and witness analysis"),
        consequences=("Civilian risk", "Loss of containment", "Escalation accountability", "Resource displacement", "Public trust and operational legitimacy"),
        accent="#66A8FF",
        metrics=(
            Metric(label="Risk", value=69), Metric(label="Control", value=94),
            Metric(label="Mobility", value=81), Metric(label="Intel", value=90),
            Metric(label="Force", value=76),
        ),
        loop=(
            StoryBeat(code="01 / RECEIVE", title="Interpret the dispatch", description="Separate confirmed facts from uncertainty and understand which nearby units can influence the incident quickly."),
            StoryBeat(code="02 / PREDICT", title="Read the grid", description="Use road geometry, target behavior and traffic conditions to identify likely escape corridors and interception points."),
            StoryBeat(code="03 / POSITION", title="Create containment", description="Assign units to pressure, intercept and block instead of stacking every vehicle behind the suspect."),
            StoryBeat(code="04 / INTERVENE", title="End the movement", description="Choose a proportionate tactic—boxing, roadblock, controlled ram or direct confrontation—when the geometry supports it."),
            StoryBeat(code="05 / RESOLVE", title="Secure the outcome", description="Transition from pursuit to arrest, scene control and evidence preservation without losing world-state continuity."),
        ),
        systems=(
            DetailBlock(title="Predictive pursuit", summary="Police units reason about destination and interception, not only target position.", description="The rectangular city grid allows units to calculate viable cuts, opposing approaches and containment arcs with bounded search costs.", bullets=("Route hypothesis", "Independent unit objectives", "Interception timing", "Fallback pursuit rail")),
            DetailBlock(title="Proportional doctrine", summary="Tactics should reflect threat, evidence and environment.", description="Minor traffic violations should not immediately produce maximum-force response. Violence, organized activity and repeated escape behavior justify stronger containment and specialized units.", bullets=("Threat classification", "Escalation thresholds", "Civilian-risk awareness", "Tactical role assignment")),
        ),
    ),
    Alignment(
        key="vigilante",
        title="VIGILANTE",
        code="UNSANCTIONED / 03",
        fantasy="Operate between law and crime using information, timing and selective intervention rather than institutional power.",
        description=(
            "The vigilante path is defined by asymmetry. The player can investigate criminal activity, expose corruption, interfere with police or criminals, "
            "and redirect events without controlling either institution. Because the role lacks formal protection, success depends on remaining difficult to classify "
            "and on understanding consequences before acting."
        ),
        objective="Use asymmetric knowledge to disrupt both sides without becoming predictable or captured by either.",
        progression=(
            "Progression expands investigative reach, covert access and the ability to manipulate information. Greater capability also creates a clearer signature, "
            "forcing the player to vary methods and decide which interventions justify exposure."
        ),
        methods=("Surveillance and pattern analysis", "Selective hacking", "Anonymous intervention", "Evidence release", "Temporary alliances"),
        consequences=("Loss of anonymity", "Hostility from both factions", "Collateral disruption", "Moral compromise", "Information becoming weaponized"),
        accent="#9DE4B2",
        metrics=(
            Metric(label="Risk", value=86), Metric(label="Control", value=67),
            Metric(label="Mobility", value=91), Metric(label="Intel", value=96),
            Metric(label="Force", value=62),
        ),
        loop=(
            StoryBeat(code="01 / OBSERVE", title="Find the hidden pattern", description="Collect enough context to distinguish a meaningful system from ordinary city noise."),
            StoryBeat(code="02 / VERIFY", title="Test the theory", description="Use surveillance, contact networks or controlled interference to determine whether the suspected relationship is real."),
            StoryBeat(code="03 / CHOOSE", title="Define the intervention", description="Decide who should be protected, exposed, delayed or disrupted and accept that no intervention is neutral."),
            StoryBeat(code="04 / ACT", title="Change the event", description="Use timing and asymmetric access to produce an outcome neither formal faction expected."),
            StoryBeat(code="05 / DISAPPEAR", title="Protect future agency", description="Remove traces, vary methods and preserve enough uncertainty to operate again."),
        ),
        systems=(
            DetailBlock(title="Information asymmetry", summary="The vigilante wins by knowing more at the right moment, not by outgunning every faction.", description="Investigation connects incidents, routes, organizations and evidence so the player can identify leverage invisible to a direct pursuit or heist loop.", bullets=("Pattern recognition", "Cross-faction evidence", "Covert observation", "Selective disclosure")),
            DetailBlock(title="Reputation without a badge", summary="Actions create interpretations among groups that do not fully understand the player.", description="Criminals, police and civilians can react differently to the same intervention. Remaining useful without becoming owned by a faction is a central tension.", bullets=("Multiple reputation lenses", "Uncertain identity", "Conditional cooperation", "Escalating counter-intelligence")),
        ),
    ),
)


SKILL_CATEGORIES = (
    SkillCategory(
        key="hacking",
        title="HACKING",
        summary="Manipulate city infrastructure, surveillance and transactional systems to create time, money or uncertainty.",
        accent="#76F3FF",
        skills=(
            Skill(name="Plate Spoof", tier=1, description="Temporarily reduce the reliability of automated vehicle identification after a clean vehicle change."),
            Skill(name="Signal Priority", tier=1, description="Request a short traffic-light advantage on a selected route without freezing the whole intersection network."),
            Skill(name="ATM Lift", tier=2, description="Extract additional value from compromised terminals while increasing evidence and cooldown pressure."),
            Skill(name="Camera Loop", tier=2, description="Repeat a short surveillance window to obscure one movement corridor for a limited duration."),
            Skill(name="Grid Override", tier=3, description="Coordinate several nearby infrastructure effects as one bounded operation instead of independent hacks."),
            Skill(name="Dispatch Noise", tier=3, description="Inject a plausible competing signal that delays confident police classification without deleting real world state."),
        ),
    ),
    SkillCategory(
        key="combat",
        title="COMBAT",
        summary="Improve control, recovery and decision quality in violent encounters rather than turning the player into a damage sponge.",
        accent="#FF764D",
        skills=(
            Skill(name="Controlled Burst", tier=1, description="Improve weapon stability when firing in disciplined intervals instead of sustained panic fire."),
            Skill(name="Weapon Retention", tier=1, description="Reduce disruption when moving, taking light impact or recovering from close contact."),
            Skill(name="Armor Discipline", tier=2, description="Gain more value from protection by managing exposure and recovery windows correctly."),
            Skill(name="Breach Momentum", tier=2, description="Carry a short initiative advantage through a successful close-range entry or takedown."),
            Skill(name="Quick Recovery", tier=3, description="Return to deliberate control faster after a severe hit without bypassing authoritative status rules."),
            Skill(name="Last Position", tier=3, description="Gain a limited tactical option while critically pressured, designed to create escape or team rescue rather than invulnerability."),
        ),
    ),
    SkillCategory(
        key="driving",
        title="DRIVING",
        summary="Expand control over acceleration, weight transfer, impact and route commitment across ordinary traffic and pursuit conditions.",
        accent="#FFB84D",
        skills=(
            Skill(name="Launch Control", tier=1, description="Convert traction into a cleaner start without granting impossible acceleration."),
            Skill(name="Brake Turn", tier=1, description="Preserve more steering authority during controlled deceleration into sharp city corners."),
            Skill(name="Impact Control", tier=2, description="Reduce loss of control from glancing collisions when the vehicle meets valid stability conditions."),
            Skill(name="Pursuit Read", tier=2, description="Surface clearer information about likely interception pressure and dangerous route commitment."),
            Skill(name="Vehicle Recovery", tier=3, description="Recover from spins or curb impacts more effectively while preserving physical consequence."),
            Skill(name="Escape Line", tier=3, description="Identify a temporary high-value route through traffic based on current world state rather than a scripted shortcut."),
        ),
    ),
    SkillCategory(
        key="intelligence",
        title="INTELLIGENCE",
        summary="Turn observation into prediction by connecting people, places, vehicles, incidents and evidence.",
        accent="#9DE4B2",
        skills=(
            Skill(name="Street Memory", tier=1, description="Retain clearer knowledge of recently observed vehicles, routes and recurring activity."),
            Skill(name="Threat Read", tier=1, description="Recognize stronger indicators of immediate danger before an encounter becomes fully committed."),
            Skill(name="Evidence Sense", tier=2, description="Identify which traces are likely to matter to police, criminals or future investigations."),
            Skill(name="Network Map", tier=2, description="Connect repeated contacts and locations into a visible relationship model."),
            Skill(name="False Trail", tier=3, description="Create a believable alternate interpretation by combining several consistent signals rather than erasing evidence."),
            Skill(name="Mastermind", tier=3, description="Preview the likely second-order consequences of a complex operation before confirming the plan."),
        ),
    ),
)


STUDIO_PRINCIPLES = (
    ("SERVER OWNS TRUTH", "Clients render state and send intent. Damage, vehicles, score, sessions and world consequences remain authoritative."),
    ("SYSTEMS SHARE RULES", "Players, bots, traffic and world actors use the same simulation contracts instead of parallel convenience implementations."),
    ("WORK STAYS BOUNDED", "Every server has measurable populations, budgets and responsibilities that remain autonomous under concurrency."),
    ("CLARITY BEATS NOISE", "Presentation exists to reveal danger, opportunity and consequence rather than hide weak decisions behind spectacle."),
    ("FAILURE MUST RECOVER", "Lifecycle ownership, supervision and truthful retry are part of the architecture rather than emergency patches."),
    ("SCALE IS MULTIPLICATION", "Growth comes from many stable autonomous servers, not one unbounded process pretending to serve everyone."),
)


DEVELOPMENT_UPDATES = (
    DevelopmentUpdate(state="ACTIVE", project="SUPER SOLDIERS", title="Authority beta", description="Move combat, bots, match lifecycle and input onto fixed server-owned simulation rails."),
    DevelopmentUpdate(state="ACTIVE", project="HEIST CITY", title="Physical traffic", description="Create shared physical vehicle truth while preserving scalable client rendering and pooling."),
    DevelopmentUpdate(state="NEXT", project="HEIST CITY", title="Pursuit intelligence", description="Expand predictive interception, containment roles, reckless tactics and recovery behavior on the city grid."),
    DevelopmentUpdate(state="PLANNED", project="KESSOKU", title="Public media pass", description="Replace procedural art direction with approved screenshots, logos, key art and short gameplay loops."),
)
