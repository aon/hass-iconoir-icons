# Iconoir Icons for Home Assistant

Use the [Iconoir](https://iconoir.com) icon set in Home Assistant with the
`iconoir:` prefix — e.g. `icon: iconoir:sofa`. Iconoir's thinner 1.5px stroke
reads lighter than the default Material Design or Lucide icons.

Home Assistant's icon API only accepts a **single filled path** per icon, while
Iconoir ships stroke-based SVGs. This integration bundles a curated set of
Iconoir icons pre-converted to single filled paths (via real polygon offset, so
closed shapes stay as thin outlines rather than solid blobs).

> This is a **curated** pack — it ships only the icons in [`ICONS`](custom_components/iconoir_icons/data/main.js),
> not all ~1,500 Iconoir glyphs. Open an issue/PR to add more.

## Installation (HACS)

1. HACS → three-dot menu → **Custom repositories**.
2. Add `https://github.com/aon/hass-iconoir-icons`, category **Integration**.
3. Search for **Iconoir Icons** in HACS and **Download** it.
4. **Restart** Home Assistant.
5. Go to **Settings → Devices & Services → Add Integration → Iconoir Icons**.
6. **Hard-refresh** the frontend (clear the service worker / cache) so
   `window.customIcons.iconoir` registers.

## Usage

```yaml
type: button
icon: iconoir:sofa
```

Verify a name is available from the browser console:

```js
await window.customIcons.iconoir.getIcon("sofa"); // { path: "...", viewBox: "0 0 24 24" }
```

## Stroke width

Because Home Assistant renders each icon as a **filled** path, the stroke
weight is baked into the geometry — it can't be changed with CSS. Instead the
pack bundles the icons pre-generated at several widths, and you pick one:

**Settings → Devices & Services → Iconoir Icons → Configure → Stroke width.**

| Width | Feel |
| ----- | ---- |
| `1.0 px` | thin / delicate |
| `1.25 px` | light |
| `1.5 px` | default (Iconoir's native weight) |
| `1.75 px` | bold |
| `2.0 px` | heavy |

After changing it, **reload the browser** — the new width applies to fresh
frontend loads. (Internally the integration serves `main.js?w=<width>`; the
changed URL also busts the cache.)

## Included icons

`bed` `chromecast` `cloud` `cloud-sunny` `compact-disc` `cutlery` `desk` `droplet` `fog`
`half-moon` `heavy-rain` `home-simple` `lamp` `light-bulb` `log-out` `movie`
`rain` `smartphone-device` `snow` `sofa` `sun-light` `switch-off`
`temperature-high` `thunderstorm` `tv` `video-projector` `warning-triangle`
`washing-machine` `wind`

## Credits

- Icons: [Iconoir](https://iconoir.com) (MIT).
- Integration pattern inspired by
  [hass-lucide-icons](https://github.com/karlis-vagalis/hass-lucide-icons).

## License

MIT — see [LICENSE](LICENSE).
