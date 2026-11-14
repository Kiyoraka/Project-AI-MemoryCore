---
name: time-adaptive-web-design
description: "Use when designing a website whose light, palette, and interface respond to time, weather, or place. Also use for ambient WebGL scenes, interactive environmental landing pages, or requests inspired by KrackedLab's digital ocean."
---

# Time-Adaptive Web Design

Design a place-responsive website with one environment shared by the scene and interface.

## Activation

When this skill activates, state the proposed setting and environmental inputs.
Then follow the protocol. Do not assume every project needs an ocean or WebGL.

## Context Guard

| Request | Action |
| --- | --- |
| Time-responsive website or ambient environment | Run the full protocol. |
| Environmental landing page without WebGL | Apply the design and fallback steps. |
| Image-only prompt or static illustration | Use the image workflow instead. |
| Request to copy KrackedLab assets or code | Stop and discuss licensing and attribution. |

## Protocol

### 1. Set the brief

- Record the place, audience, primary action, and desired mood.
- Record available inputs: local time, location, weather, or user-controlled time.
- Ask before assuming a location, weather source, brand identity, or paid service.
- Choose one visual subject that stays recognizable through every time state.

### 2. Design the environmental model

- Define dawn, day, golden hour, dusk, and night as connected states.
- Tie each state to light direction, sky, foreground, accent, and readable text color.
- Interpolate colors across state boundaries. Avoid abrupt palette changes.
- Use real solar position only when the location and date are known.
- Keep weather optional. A failed fetch must not erase the experience.
- Label simulated, cached, and live conditions accurately.

### 3. Compose one visual world

- Give the scene a stable horizon, depth cues, and a clear focal area.
- Reserve quiet space for type. Keep controls off the focal subject.
- Give foreground, midground, and distance distinct motion and contrast.
- Use restrained interaction: pointer response, touch ripple, or one contextual action.
- Avoid unrelated effects that compete with the main scene.

### 4. Make the interface belong to the scene

- Drive interface color and scene color from the same state model.
- Pair expressive display type with readable labels and values.
- Keep live status, current time, and controls legible across all states.
- Provide a time scrubber only when exploring time serves the brief.
- Give the scrubber keyboard control, labels, and current-value text.

### 5. Build fallbacks before polishing effects

- Provide a useful static scene when WebGL is unavailable.
- Honor reduced motion without removing the page's content.
- Check touch targets, focus visibility, contrast, and narrow screens.
- Cap rendering work on mobile and reduce detail when frames slow down.
- Keep audio off until the user starts it. Provide a mute control.

### 6. Present and check

- Deliver the setting, visual direction, state map, interaction map, and fallback plan.
- When implementing, test dawn, day, golden hour, dusk, and night.
- Test offline conditions, no WebGL, reduced motion, keyboard, touch, and mobile.
- State which inputs are live and which are simulated.

## Reference

[KrackedLab](https://github.com/strdst7/kdlabcreative-aimirah) demonstrates this design method.
Its ocean uses solar palettes, optional weather, an editorial interface, and time scrubbing.
Read its `site/beach/palette.js`, `site/beach/hud.js`, and `site/beach/main.js` for examples.

Use its design principles as reference. Do not copy code, shaders, images, or audio.
The reference project uses AGPL-3.0. Check its license before reusing any material.

## Level History

- **Lv.1** — Design a time-adaptive site with shared environment and interface state.
