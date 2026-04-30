---
type: dashboard_embed_note
dashboard: ZippyLogitech_Corridor_Delay_Analytics
status: draft
created_at: 2026-04-30
---
# Obsidian Embed: Tableau Corridor Delay Dashboard

## Purpose

Use this note to embed the Tableau corridor delay dashboard inside the Zippy operating vault after publishing it to Tableau Server or Tableau Online.

## Embed Placeholder

Replace `YOUR_TABLEAU_URL` with the published workbook view URL.

```html
<iframe
  src="YOUR_TABLEAU_URL?:showVizHome=no&:embed=true"
  width="100%"
  height="900"
  frameborder="0">
</iframe>
```

## Suggested Placement

Add this link to `soul.md` or the control tower dashboard index:

```md
[[Obsidian Embed - Tableau Corridor Delay Dashboard]]
```

## Operating Rule

This dashboard is useful only if it drives action. Review it daily for:

- critical lanes below reliability threshold
- worsening P90 delay
- high terminal dwell
- poor carrier performance
- triangle routes with high handoff wait
- lanes where ASCT is saving meaningful time or cost
