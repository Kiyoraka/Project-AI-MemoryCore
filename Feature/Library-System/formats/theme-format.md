# 🎨 Theme Entry Format
*Template for visual style entries*

## Required Fields
- Theme name and description
- Color palette with hex codes
- Tailwind classes
- Component styles
- Projects using this

## Template

```markdown
# [Theme Name]
*[Style description - e.g., "Emerald green with glassmorphism effects"]*

## Color Palette

| Role | Color Name | Hex | Tailwind Class |
|------|------------|-----|----------------|
| Primary | | | |
| Secondary | | | |
| Accent | | | |
| Background | | | |
| Surface | | | |
| Text Primary | | | |
| Text Secondary | | | |
| Success | | | |
| Error | | | |
| Warning | | | |

## Tailwind Config

```javascript
// tailwind.config.js colors extension
colors: {
  // Custom color definitions
}
```

## Component Styles

### Buttons
```html
<!-- Primary Button -->
<button class="...">

<!-- Secondary Button -->
<button class="...">

<!-- Outline Button -->
<button class="...">
```

### Cards
```html
<!-- Standard Card -->
<div class="...">

<!-- Glassmorphism Card (if applicable) -->
<div class="...">
```

### Navigation
```html
<!-- Top Navigation -->
<nav class="...">

<!-- Sidebar -->
<aside class="...">
```

### Forms
```html
<!-- Input Field -->
<input class="...">

<!-- Select -->
<select class="...">
```

## Special Effects

### Glassmorphism (if applicable)
```css
/* Glass effect settings */
backdrop-filter: blur(Xpx);
background: rgba(255, 255, 255, 0.X);
```

### Gradients
```css
/* Gradient definitions */
```

### Shadows
```css
/* Shadow styles */
```

## Typography
- **Font Family**: [Font name]
- **Headings**: [Weight, sizes]
- **Body**: [Weight, size]
- **Small**: [Weight, size]

## Dark Mode (if applicable)
- Supported: Yes/No
- Implementation notes

## Projects Using This
- [Project 1]
- [Project 2]

---
*Documented: [Date]*
```

## Example Entry Names
- `green-glassmorphism` - Emerald with glass effects
- `coffee-warm-earth` - Brown/cream coffee theme
- `purple-glassmorphism` - Purple with glass effects
- `ocean-blue-clean` - Blue professional clean
- `dark-modern-minimal` - Dark mode minimal

---
*Format v1.0 - January 3, 2026*
