from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
import streamlit as st


class VehicleSpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    category: Literal["LAW ENFORCEMENT & SWAT", "EMERGENCY & EMS", "HAULING & UTILITY", "SUPER & HYPERCARS", "OFF-ROAD & 4X4"]
    role: str
    seats: int
    speed_tier: str
    durability: str
    mass_class: str
    features: tuple[str, ...]
    description: str


HEIST_VEHICLES: tuple[VehicleSpec, ...] = (
    # LAW ENFORCEMENT & SWAT
    VehicleSpec(
        name="Undercover Chicago Police Cruiser",
        category="LAW ENFORCEMENT & SWAT",
        role="High-Speed Pursuit Interceptor",
        seats=5,
        speed_tier="Tier 1 (High Pursuit)",
        durability="Reinforced Chasis",
        mass_class="Medium (20.9 studs)",
        features=("Concealed Lightbar", "High-Output Siren", "Pit-Maneuver Bumper", "Radio Grid"),
        description="The primary rapid-response unit of NewCity Police Department. High top speed and agile handling allow aggressive pursuit through crowded urban grids.",
    ),
    VehicleSpec(
        name="[UV] Lenco Bearcat",
        category="LAW ENFORCEMENT & SWAT",
        role="Tactical Armored SWAT Transport",
        seats=8,
        speed_tier="Tier 3 (Heavy Assault)",
        durability="Ballistic Armor Plating",
        mass_class="Heavy (24.6 studs)",
        features=("Bulletproof Glass", "8 Tactical Operative Seats", "Ramming Prow", "Gunner Hatch"),
        description="Heavy counter-terror tactical transport. Designed to breach fortified bank heists, absorb heavy automatic fire, and transport a full tactical squad into hot zones.",
    ),
    VehicleSpec(
        name="Ford 4x4 Interceptor",
        category="LAW ENFORCEMENT & SWAT",
        role="Sheriff & Perimeter Patrol",
        seats=5,
        speed_tier="Tier 2 (All-Terrain Pursuit)",
        durability="High-Clearance Armor",
        mass_class="Medium-Heavy (28.0 studs)",
        features=("Dual Spotlights", "Roof Lightbar", "All-Terrain Suspension", "Siren Cluster"),
        description="Rugged patrol cruiser built for peripheral highway intercepts and off-road canal pursuit around NewCity district boundaries.",
    ),

    # EMERGENCY & EMS
    VehicleSpec(
        name="AMR Emergency Ambulance",
        category="EMERGENCY & EMS",
        role="Paramedic Triage & Mobile Medical Unit",
        seats=6,
        speed_tier="Tier 2 (Emergency Response)",
        durability="Medium Transport",
        mass_class="Medium (19.6 studs)",
        features=("21 Emergency Surface Lights", "Stretcher Compartment", "Dual High-Lo Sirens", "Trauma Gear"),
        description="Essential city emergency infrastructure. Fast acceleration and high road presence clear traffic swiftly to rescue wounded operatives or escaped crews.",
    ),
    VehicleSpec(
        name="SSFD4 Heavy Fire Engine",
        category="EMERGENCY & EMS",
        role="Disaster Containment & Structural Breach",
        seats=4,
        speed_tier="Tier 4 (Super Heavy)",
        durability="Extreme Thermal / Kinetic Armor",
        mass_class="Colossal (39.7 studs)",
        features=("68 Scripts / Multi-Light Rig", "Hydraulic Water Cannon", "Extrication Gear", "Massive Momentum"),
        description="Massive structural response engine. Its immense forward mass pulverizes roadside obstacles and civilian vehicles during high-stakes pursuit blockades.",
    ),

    # HAULING & UTILITY
    VehicleSpec(
        name="Oshkosh JLTV",
        category="HAULING & UTILITY",
        role="Heavy Tactical Combat Utility",
        seats=5,
        speed_tier="Tier 3 (Armored Utility)",
        durability="Military Ballistic Armor",
        mass_class="Ultra Heavy (678 parts)",
        features=("635 Detailed Meshes", "Independent Suspension", "Reinforced Underbody", "Payload Bay"),
        description="Military-grade tactical utility platform. Extreme durability protects against explosive mines and heavy weapons fire during gold convoy transfers.",
    ),
    VehicleSpec(
        name="Mitsubishi Canter Tow Truck",
        category="HAULING & UTILITY",
        role="Vehicle Recovery & Road Obstruction",
        seats=3,
        speed_tier="Tier 3 (Utility Hauler)",
        durability="Heavy Industrial Frame",
        mass_class="Heavy (33.6 studs)",
        features=("Hydraulic Flatbed", "Winch Cable Rig", "Dual Passenger Seats", "Heavy Tow Bumper"),
        description="Specialized industrial utility truck. Enables syndicate crews to tow and impound rival getaway vehicles or clear barricaded escape intersections.",
    ),
    VehicleSpec(
        name="1996 Dodge Ram 1500",
        category="HAULING & UTILITY",
        role="Street Syndicate Pickup",
        seats=3,
        speed_tier="Tier 2 (Workhorse)",
        durability="Sturdy Steel Body",
        mass_class="Medium (21.0 studs)",
        features=("Open Cargo Bed", "High Torque V8", "13 Point Lights", "Off-Road Tires"),
        description="Everyday syndicate workhorse. Used for quick contraband transport, getaway crew staging, and drive-by perimeter suppression.",
    ),
    VehicleSpec(
        name="Ford E-Series Cargo Van",
        category="HAULING & UTILITY",
        role="Covert Logistics & Bank Heist Escape",
        seats=4,
        speed_tier="Tier 2 (Covert Transport)",
        durability="Reinforced Commercial Shell",
        mass_class="Medium-Large (24.8 studs)",
        features=("Enclosed Vault Cargo", "Sliding Side Doors", "Tinted Windows", "Radio Scrambler"),
        description="The quintessential bank heist getaway van. Discrete civilian exterior masks high-capacity interior vaults designed to transport multi-million dollar scores.",
    ),

    # SUPER & HYPERCARS
    VehicleSpec(
        name="Bugatti La Voiture Noire",
        category="SUPER & HYPERCARS",
        role="Apex Syndicate Hypercar",
        seats=2,
        speed_tier="Tier 1+ (Maximum Velocity)",
        durability="Lightweight Carbon Fiber",
        mass_class="Aerodynamic (20.7 studs)",
        features=("Quad-Turbocharged Engine", "Active Aero Wing", "Carbon Monocoque", "Zero-to-Sixty Blast"),
        description="The ultimate symbol of underworld wealth and speed. Outruns any standard police cruiser on straight highways, forcing law enforcement to deploy spike strips.",
    ),
    VehicleSpec(
        name="Pagani Zonda HP Barchetta",
        category="SUPER & HYPERCARS",
        role="High-Acuity Exotic Getaway",
        seats=2,
        speed_tier="Tier 1+ (Extreme Acceleration)",
        durability="Carbon-Titanium Weave",
        mass_class="Lightweight (19.8 studs)",
        features=("Naturally Aspirated V12", "Open-Top Cockpit", "High-Downforce Aero", "Exquisite Handling"),
        description="Rare Italian hypercar delivering surgical cornering precision through tight NewCity alleyways and harbor docks.",
    ),
    VehicleSpec(
        name="Ferrari FXX K (fxxk5)",
        category="SUPER & HYPERCARS",
        role="Track-Tuned Pursuit Missile",
        seats=2,
        speed_tier="Tier 1+ (Apex Track)",
        durability="Track Spec Composite",
        mass_class="Ultra Low Profile (4.6 studs high)",
        features=("Hybrid KERS Boost", "99 Custom Scripts", "Extreme Downforce Wings", "Slick Tires"),
        description="Uncompromising track missile. Features extreme lateral grip that makes corner escapes effortless, leaving pursuing patrol cars spinning out.",
    ),
    VehicleSpec(
        name="Chevrolet Corvette C5",
        category="SUPER & HYPERCARS",
        role="Street Muscle Getaway",
        seats=2,
        speed_tier="Tier 1 (High Power Muscle)",
        durability="Fiberglass Body",
        mass_class="Low Stance (22.2 studs)",
        features=("American V8 Roar", "Rear Wheel Drift Tuning", "Pop-up Headlights", "High Top Speed"),
        description="American muscle icon. High straight-line torque and controllable drift angles make it an accessible favorite for seasoned syndicate getaway drivers.",
    ),

    # OFF-ROAD & 4X4
    VehicleSpec(
        name="2018 Jeep Gladiator",
        category="OFF-ROAD & 4X4",
        role="All-Terrain Flank & Pursuit",
        seats=4,
        speed_tier="Tier 2 (Off-Road Cruiser)",
        durability="High-Clearance Off-Road",
        mass_class="Medium (24.3 studs)",
        features=("Open Bed Utility", "High-Travel Shocks", "12 Surface Lights", "Water Fording"),
        description="Dual-purpose utility pickup built to escape across riverbeds, construction yards, and unpaved mountain roads where police sedans bottom out.",
    ),
    VehicleSpec(
        name="Jeep Rubicon 2019",
        category="OFF-ROAD & 4X4",
        role="Off-Road Rock Crawler",
        seats=4,
        speed_tier="Tier 2 (Trail Master)",
        durability="Tubular Steel Frame",
        mass_class="Medium (22.0 studs)",
        features=("Locking Differentials", "Heavy Winch", "Knobby Mud Tires", "Roll Cage"),
        description="Unstoppable off-road specialist capable of traversing extreme terrain and breaking through environmental shortcuts.",
    ),
)


def render_heist_vehicle_showroom(accent: str) -> None:
    """Render the Heist City Vehicle Fleet Showroom."""
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,118,77,0.3);border-radius:12px;padding:20px;margin-bottom:20px;">
            <div style="font-size:20px;font-weight:900;color:#FF764D;letter-spacing:0.02em;">NEWCITY VEHICLE FLEET & PURSUIT CATALOG</div>
            <div style="font-size:13px;color:#AEB4BC;margin-top:4px;">
                Verified inventory of 35 production models cataloged in Studio across Law Enforcement, Armored SWAT, 
                Heavy Logistics, and Apex Hypercars.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    categories = ["ALL (15 Showcased)"] + sorted(list({v.category for v in HEIST_VEHICLES}))
    selected_cat = st.segmented_control("Fleet Division", categories, default=categories[0], width="stretch") or categories[0]

    filtered = HEIST_VEHICLES if "ALL" in selected_cat else [v for v in HEIST_VEHICLES if v.category == selected_cat]

    v_cols = st.columns(3, gap="medium")
    for i, car in enumerate(filtered):
        is_swat = "SWAT" in car.category or "LAW" in car.category
        is_hyper = "SUPER" in car.category
        card_border = "#FF764D" if is_swat else ("#76F3FF" if is_hyper else "rgba(255,255,255,0.15)")

        with v_cols[i % 3]:
            st.markdown(
                f"""
                <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-top:3px solid {card_border};border-radius:10px;padding:16px;margin-bottom:16px;min-height:270px;">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <span style="font-size:16px;font-weight:800;color:#F4F2EB;">{car.name}</span>
                    </div>
                    <div style="font-size:11px;font-weight:700;color:{card_border};margin-top:2px;">{car.category} &bull; {car.role}</div>
                    <div style="margin-top:10px;display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:12px;">
                        <div><strong style="color:#AEB4BC;">Capacity:</strong> <span style="color:#F4F2EB;">{car.seats} Seats</span></div>
                        <div><strong style="color:#AEB4BC;">Velocity:</strong> <span style="color:#F4F2EB;">{car.speed_tier}</span></div>
                        <div><strong style="color:#AEB4BC;">Armor:</strong> <span style="color:#F4F2EB;">{car.durability}</span></div>
                        <div><strong style="color:#AEB4BC;">Mass:</strong> <span style="color:#F4F2EB;">{car.mass_class}</span></div>
                    </div>
                    <div style="font-size:12px;color:#AEB4BC;line-height:1.5;margin-top:10px;">{car.description}</div>
                    <div style="margin-top:12px;display:flex;gap:4px;flex-wrap:wrap;">
                        {"".join(f'<span style="background:rgba(255,255,255,0.04);color:#D9DCE1;font-size:10px;padding:2px 6px;border-radius:4px;border:1px solid rgba(255,255,255,0.08);">{f}</span>' for f in car.features)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
