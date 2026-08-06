# Kessoku Website — Media Integration Contract

## Runtime behavior

The website resolves campaign media through `kessoku_site/media.py`.

Existing page code continues to request deterministic procedural posters. The media bridge hashes those poster bytes and substitutes approved campaign artwork when the matching repository file exists. When no approved image exists, the procedural poster remains visible, so missing media cannot break a deployment.

## Approved first-pass filenames

Place these files directly in `assets/media/`:

- `super-soldiers-city-of-zombies.webp`
- `heist-city-hero.webp`
- `heist-city-vigilante.webp`

The first two are currently connected to existing poster slots. The vigilante frame is registered for the alignment-specific presentation pass.

## Supported storage forms

The loader checks, in this order:

1. A normal binary WebP file, such as `heist-city-hero.webp`.
2. One Base64 text file, such as `heist-city-hero.webp.b64`.
3. Ordered Base64 parts, such as:
   - `heist-city-hero.webp.b64.part01`
   - `heist-city-hero.webp.b64.part02`
   - `heist-city-hero.webp.b64.part03`

Normal binary WebP files are the production format. Base64 forms exist only as a connector-safe fallback and should not be preferred when Git or the GitHub web interface can upload binary files normally.

## Export policy

- Format: WebP
- Color space: sRGB
- Recommended working crop: 16:9 or the slot-specific ratio in `assets/media/manifest.json`
- Recommended minimum hero width: 1920 pixels
- Quality: approximately 82–88
- Maximum target size: 1.5 MB per image
- No embedded text, logos, watermarks, HUD elements, or fake interface panels
- Preserve the outer 10 percent as a safe area for responsive cropping

## Replacement workflow

1. Generate or capture the image using `docs/IMAGE_ASSET_PROMPTS.md`.
2. Review composition, project consistency, anatomy, vehicle geometry, and unwanted text.
3. Export to the exact manifest filename.
4. Add it to `assets/media/`.
5. Refresh the Streamlit preview.
6. Verify desktop, tablet, and phone crops.
7. Remove a Base64 fallback for the same filename after the real WebP is committed.

## Failure behavior

A missing, malformed, or incomplete media payload is ignored. The original procedural artwork remains visible. This ensures that a media mistake does not prevent the site from starting.
