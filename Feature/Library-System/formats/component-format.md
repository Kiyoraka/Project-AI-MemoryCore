# 🧩 Component Entry Format
*Template for reusable UI component entries*

## Required Fields
- Component name and description
- Props/inputs
- Structure (HTML/Vue)
- Styling
- Usage examples

## Template

```markdown
# [Component Name]
*[What this component does]*

## Use Case
- When to use this component
- Problem it solves
- User interaction it handles

## Props / Inputs

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| | | | | |

## Emits / Events

| Event | Payload | Description |
|-------|---------|-------------|
| | | |

## Structure

```vue
<template>
  <!-- Component structure -->
</template>

<script setup>
// Component logic
</script>
```

## Styling

```vue
<style scoped>
/* Component styles */
</style>
```

Or Tailwind classes:
```html
<!-- Key Tailwind patterns used -->
```

## Usage Example

```vue
<!-- How to use this component -->
<ComponentName
  :prop1="value"
  @event="handler"
/>
```

## Variations
- [Variation 1]: [Description]
- [Variation 2]: [Description]

## Accessibility
- Keyboard navigation
- Screen reader support
- ARIA attributes

## Projects Using This
- [Project 1]
- [Project 2]

---
*Documented: [Date]*
```

## Example Entry Names
- `data-table-filters` - Table with search, sort, filter
- `modal-form` - Modal with form validation
- `sidebar-collapsible` - Collapsible sidebar navigation
- `card-grid-responsive` - Responsive card grid layout
- `dropdown-searchable` - Searchable dropdown select

---
*Format v1.0 - January 3, 2026*
