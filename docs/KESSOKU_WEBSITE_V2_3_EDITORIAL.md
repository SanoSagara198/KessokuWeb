# Kessoku Website V2.3 — Editorial Presentation Pass

## Objective

V2.3 improves perceived production quality without changing the content model, interaction contracts, or public claims. The site should read like a premium game-studio portfolio rather than a continuous technical dashboard.

## Implemented presentation changes

### Global reading progress

A two-pixel progress line uses CSS scroll-linked animation only when the browser explicitly supports `animation-timeline`. Unsupported browsers omit the effect. Reduced-motion users do not receive the animation.

### Studio marquee

A restrained line beneath the primary identity surface repeats the four portfolio themes:

- Super Soldiers / tactical pressure
- Heist City / urban consequence
- Server authority / shared truth
- Kessoku / Argentina

The marquee is decorative, hidden from accessibility navigation, disabled under reduced motion, and removed on small screens.

### Hero metadata rails

Every principal route now follows the cinematic hero with four factual metadata cells. These cells establish format, player feeling, platform or world model, and current public development state.

The metadata is structural and does not introduce fabricated player counts, dates, performance claims, or commercial metrics.

### Project signatures

Homepage project cards now receive three supporting statements:

1. Player role
2. Repeated gameplay rhythm
3. System promise

This makes the cards useful even before final media is available and prevents the portfolio from relying solely on atmospheric copy.

### Expanded footer

The former single-line footer has been replaced by a studio closing statement with:

- Kessoku identity
- concise studio positioning
- active-world summary
- truthful public status
- canonical-link warning
- studio location and portfolio principle

No unofficial social or contact destinations were added.

## Responsive behavior

### Desktop

- Four-column hero metadata rail
- Three-column project signatures
- Three-column footer
- Animated studio marquee

### Tablet and phone

- Two-column hero metadata rail
- Single-column project signatures
- Single-column footer
- Marquee removed to preserve viewport space
- Existing campaign focal-position rules remain authoritative

## Accessibility

- Decorative marquee uses `aria-hidden`.
- Progress and marquee animation are disabled under `prefers-reduced-motion`.
- Content does not depend on animation.
- Metadata remains visible text rather than chart-only information.
- Existing keyboard focus rules remain unchanged.

## Performance

The V2.3 layer adds only CSS and small HTML fragments. It introduces no new Python dependency, remote request, JavaScript bundle, analytics library, or external font.

## Repository validation

`scripts/validate_site.py` performs a dependency-free repository audit:

- parses every Python file with `ast`
- rejects deprecated `use_container_width` source calls
- rejects the removed navigation dependency in `requirements.txt`
- validates media-manifest IDs, filenames, and WebP extensions
- validates committed binary or Base64 media payloads
- enforces the 1.5 MB media budget
- verifies required V2.3 files

The script is committed but has not been executed against a local checkout in this connector-only environment. Community Cloud preview remains the authoritative runtime validation.

## Preview checklist

Review the preview branch at desktop, tablet, and phone widths.

### Global

- Top identity bar and primary navigation do not overlap.
- Marquee does not create horizontal page overflow.
- Scroll progress remains two pixels high and does not cover controls.
- Unsupported browsers do not display a broken progress effect.
- Reduced-motion mode removes moving presentation elements.

### Heroes

- Metadata text remains factual and readable.
- Four cells collapse to two columns on phone widths.
- Campaign art remains legible behind hero copy.
- Procedural fallback heroes preserve the same layout.

### Homepage projects

- Project signatures remain visually connected to the correct project card.
- CTA buttons remain clearly separated from metadata.
- Cards remain balanced when only one project has approved media.

### Footer

- Three columns collapse cleanly.
- No unofficial link appears.
- Long status text does not overflow.

## Evidence boundary

The implementation head reviewed before the final documentation and README wording commits was `c7bda19045855209e966ccb744a32a467fd61f0c`.

Confirmed through repository inspection:

- no `use_container_width` source matches
- the removed navigation package is absent from `requirements.txt`
- V2.3 stylesheet is imported by the shared component layer
- README is updated to V2.3 with the validation command
- media slots remain fallback-safe

Not yet confirmed through a browser render:

- final sticky stacking across all viewport sizes
- scroll-linked animation behavior in Streamlit Community Cloud browsers
- campaign-media focal crops after binary upload
- complete interactive route smoke test

## Definition of done

V2.3 is complete when:

- all four routes render without exceptions
- navigation remains stable on refresh
- editorial additions do not change application state
- campaign media and procedural fallbacks produce equivalent layout dimensions
- no deprecated Streamlit width arguments are emitted
- no stale dependency claim remains in public documentation
- mobile and reduced-motion presentation have been visually reviewed
