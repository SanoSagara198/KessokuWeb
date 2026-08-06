# Kessoku Website — Production Image Shot List

## Purpose

This document converts the website media manifest into a practical generation sequence. Each frame has one page responsibility, one composition rule, and one continuity anchor. The goal is not to accumulate attractive images; it is to build a coherent visual campaign that makes Kessoku, Super Soldiers, and Heist City immediately recognizable.

The detailed prompt language remains in `docs/IMAGE_ASSET_PROMPTS.md`. This shot list defines priority, placement, review criteria, and derivative crops.

## Current approved first-pass frames

The current media pass established three usable directions:

1. **Super Soldiers — City of Zombies**
   - Role: PvE operation dossier.
   - Strength: readable squad-versus-horde pressure and strong blue-grey atmosphere.
   - Continuity value: use its armor construction, cyan equipment lighting, weapons, smoke density, and ruined-city material language for all later Super Soldiers frames.

2. **Heist City — Pursuit hero**
   - Role: primary Heist City hero and pursuit identity.
   - Strength: immediately readable top-down grid, police convergence, wet asphalt, amber city light, and disciplined red/blue response lighting.
   - Continuity value: use its vehicle proportions, road geometry, city density, rain treatment, and police-light intensity for all later Heist City pursuit frames.

3. **Heist City — Vigilante**
   - Role: Vigilante alignment dossier.
   - Strength: clear lone-observer fantasy, city scale, moral distance, and cinematic negative space.
   - Continuity value: use its skyline, rooftop materials, wardrobe silhouette, and restrained night palette for later intelligence and investigation scenes.

## Priority A — campaign-defining images

These images should be generated next because they establish the recurring visual grammar for the entire website.

### A1. Super Soldiers primary hero

- **Filename:** `super-soldiers-hero.webp`
- **Placement:** Super Soldiers page hero.
- **Aspect:** 21:9.
- **Composition:** five-person squad on the center-right; left third remains dark and calm for the title.
- **Required story:** distinct tactical roles, coordinated advance, readable modular arena.
- **Continuity anchor:** City of Zombies armor and cyan-light language.
- **Reject when:** the squad looks like generic space marines, silhouettes merge, weapons dominate faces, or the left side becomes visually busy.

### A2. Super Soldiers 5v5 operation

- **Filename:** `super-soldiers-arena-operation.webp`
- **Placement:** 5v5 Arena operation dossier.
- **Aspect:** 16:9.
- **Composition:** foreground team occupies lower-right and center; objective and opposition remain readable; upper-left stays clear for the operation label.
- **Required story:** cover, angle control, flanking, support, and positional decision-making.
- **Continuity anchor:** approved Super Soldiers primary hero.
- **Reject when:** the image becomes a chaotic firefight, teams are visually indistinguishable, or the arena lacks tactical lanes.

### A3. Kessoku dual-world portfolio hero

- **Filename:** `kessoku-home-dual-world-hero.webp`
- **Placement:** homepage hero or closing manifesto.
- **Aspect:** 21:9.
- **Composition:** Super Soldiers world on the left, Heist City world on the right, one coherent horizon and lighting transition rather than a hard collage seam.
- **Required story:** two very different player fantasies connected by one production standard.
- **Continuity anchors:** approved Super Soldiers hero and Heist City pursuit hero.
- **Reject when:** it resembles a split-screen poster, contains a central logo, invents interface panels, or lacks usable typography space.

### A4. Heist City criminal alignment

- **Filename:** `heist-city-criminal.webp`
- **Placement:** Criminal alignment dossier.
- **Aspect:** 16:9.
- **Composition:** small crew and original getaway vehicle preparing in an alley that opens onto active traffic.
- **Required story:** planning, ambition, evidence risk, crew roles, and escape preparation.
- **Continuity anchor:** Heist City pursuit hero.
- **Reject when:** it imitates recognizable heist-film masks, becomes a static character lineup, or removes the living city from the background.

### A5. Heist City police alignment

- **Filename:** `heist-city-police.webp`
- **Placement:** Police alignment dossier.
- **Aspect:** 16:9.
- **Composition:** one interceptor, one partial roadblock, one officer managing civilians, target visible farther down the route.
- **Required story:** prediction, independent unit roles, proportional response, and containment.
- **Continuity anchor:** Heist City pursuit hero.
- **Reject when:** every police car follows in one line, the scene appears militarized, or real-world police branding appears.

### A6. Kessoku studio manifesto

- **Filename:** `kessoku-studio-manifesto.webp`
- **Placement:** Studio page closing visual.
- **Aspect:** 16:9.
- **Composition:** one central coherent world-state structure distributing into several bounded worlds; large clean region for manifesto copy.
- **Required story:** shared rules, bounded autonomous servers, one trustworthy simulation contract.
- **Continuity anchors:** cyan and amber campaign colors.
- **Reject when:** it resembles a server rack, cloud-computing stock image, dashboard, literal code screen, or generic AI artwork.

## Priority B — editorial gallery

These frames create page rhythm and provide material for devlogs, social cards, and future press pages.

### B1. Super Soldiers role silhouettes

A horizontal squad lineup staged inside the arena, with each role readable from posture and equipment rather than labels. Use this for a role/class section once the production roster is fixed.

### B2. Super Soldiers rescue moment

A close tactical frame showing one soldier stabilizing a teammate while two others hold different angles. This communicates teamwork more effectively than another firing pose.

### B3. Heist City civilian consequence

A street-level frame after a pursuit has passed: damaged street furniture, rerouted traffic, pedestrians reacting, police securing the intersection, and no giant explosion. This visualizes a city that remembers disruption.

### B4. Heist City evidence and investigation

A restrained interior or alley scene where evidence connects a vehicle, location, and suspect. Avoid floating holograms; use physical objects, surveillance photographs, maps, and environmental clues.

### B5. Heist City traffic ecosystem

High-oblique daylight or dusk shot showing traffic lanes, pedestrians, signals, service vehicles, police patrols, and varied city blocks operating without an active chase. This proves the city is more than pursuit scenery.

### B6. Kessoku bounded-world triptych

Three related frames showing one server-authoritative contract expressed as combat, traffic, and world presentation. This may use a triptych layout on the website, but each generated source must remain an independent single image.

## Priority C — responsive derivatives

Do not ask the image generator to crop the same composition mechanically. Generate or art-direct derivatives that preserve the intended subject hierarchy.

### Desktop hero

- 21:9 or 2.33:1.
- Important subjects remain between 28 and 82 percent of image width.
- Typography-safe region is deliberately composed, not blurred afterward.

### Standard editorial frame

- 16:9.
- Main subject remains inside the central 76 percent.
- Safe for two-column and full-width presentation.

### Mobile portrait

- 9:16.
- One dominant subject and one supporting environmental read.
- Do not stack a desktop group vertically through generative distortion.
- Produce dedicated portrait frames for:
  - Super Soldiers squad leader
  - City of Zombies defender
  - Heist City pursuit vehicle
  - Vigilante rooftop observer

### Social/Open Graph frame

- 1.91:1, recommended 1200×630.
- No text in the image; title and description remain HTML metadata.
- Strong central read at small preview size.
- Generate `kessoku-open-graph.webp` only after both primary game heroes are approved.

## Shared generation suffix

Append this direction to every production prompt:

> Original premium Roblox game-world key art with readable stylized proportions and physically coherent materials. Single cinematic frame. No words, typography, logos, watermarks, HUD, interface panels, split screens, collages, recognizable franchise characters, licensed vehicle designs, or real-world police branding. Preserve the requested negative-space region and keep critical subjects inside the central safe area.

## Review checklist

Before an image enters `assets/media/`:

1. The player fantasy is understandable in three seconds.
2. The frame belongs unmistakably to the correct game.
3. Characters, armor, vehicles, and environments match the approved anchor.
4. There is no accidental text, logo, watermark, or interface.
5. Hands, weapons, wheels, roads, and architectural lines are structurally coherent.
6. The requested typography-safe region is genuinely usable.
7. The image survives a phone-width crop.
8. WebP export remains within the media budget.
9. The filename exactly matches `assets/media/manifest.json`.
10. The website still renders its procedural fallback when the file is removed.

## Recommended next generation order

1. Super Soldiers primary hero.
2. Super Soldiers 5v5 operation.
3. Heist City criminal alignment.
4. Heist City police alignment.
5. Kessoku dual-world portfolio hero.
6. Kessoku studio manifesto.
7. Editorial gallery and mobile derivatives.
