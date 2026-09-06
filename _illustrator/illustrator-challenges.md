# Illustrator scripting: what we tried and why we stopped

September 2026. An attempt to make space plans faster to iterate on by driving
Illustrator's variables from a script. **The conclusion was that scripted
variable management is not stable enough to rely on**, and the work was
reverted. The CSV + VariableImporter method in the
[playbook](https://playbook.makerfaireorlando.com/space-planning/printed-space-plans)
remains the way we do this.

This is a record so nobody spends the same day twice.

## What we were trying to fix

1. **The Variable Importer is slow.** `VariableImporter.jsx` parses the CSV in
   ExtendScript and builds the XML Illustrator actually wants. On Spirit — 432
   spaces, so 432 variables — that parsing is where the time goes.
2. **Round-trip latency.** Every placement tweak meant a full
   `update_exhibits.py` run before it showed up on the plan.

## What we built

- `_python/make_variable_library.py` — generated Illustrator variable library
  XML directly from the space-plan CSVs, in milliseconds, so Illustrator only
  had to do one native `importVariables()` call.
- `_illustrator/load_variables.jsx` — a dialog to load a data file, bind
  variables, show a blank data set, and clear all variables.

Both are gone. The findings below are the part worth keeping.

## What actually worked

**Generating the variable library XML in Python is sound and fast.** Output was
verified byte-for-byte against the source CSVs — 2,808 cells across three
buildings, including ampersands and apostrophes — and Illustrator imported it
via the native **Variables panel > Load Variable Library** noticeably faster
than VariableImporter did.

That part was never the problem.

## What broke

### Binding is the hard part, and it's slow

Importing a variable library **creates variables but binds nothing**. An unbound
variable appears in the Variables panel and in every data set, but switching
data sets changes nothing on the page — a silent, very confusing failure.

Binding by script (`textFrame.contentVariable = variable`, matching
`pageItem.name`) worked but was slow enough to be unusable, and had to be
redone from scratch after any clear.

### Clearing variables does not blank the plan

Removing a variable removes the *binding*, not the text. The exhibit names stay
exactly where they were, on a document that now needs every object re-bound.
Clearing 434 variables took **62 seconds** and achieved nothing visible.

### Reading `Variable.pageItems` crashes Illustrator

Walking that property across a few hundred variables to report which ones were
bound crashed Illustrator outright, on script load. There is no safe way to ask
"is this bound?" at this scale.

### Progress feedback is barely possible

Illustrator will not display a modeless `Window("palette")` from a script
launched via **File > Scripts** — it simply never appears. The workable pattern
is a *modal* dialog running the work from its own `onShow` handler, which then
forbids `alert()`/`confirm()` inside the work. Several attempts to get a
progress bar to show during a long operation did not produce a reliable result.

### Text still overflows the cells

Even with the data loaded correctly, long maker names wrap past the bottom of
the space box. The 20-character truncation in the label is not enough on its
own; the cells need real overflow handling. This is unsolved regardless of how
the data gets in.

## Findings worth keeping

Genuinely useful things learned, independent of the approach:

| Finding | Detail |
|---|---|
| Native import exists | **Variables panel > Load Variable Library** reads CSV *or* XML. `VariableImporter.jsx` is from 2015 and predates it. |
| XML beats CSV for import | XML preserves line breaks (`&#13;`) and real data set names. Native CSV import can't name data sets from a column. |
| The XML schema | SVG wrapper with the `ns_*` entity DOCTYPE; `<variable trait="textcontent" category="&ns_flows;">` per space; one `<p>` per cell with `&#13;` between lines; `<v:sampleDataSet dataSetName="...">` per view. |
| Binding is by object *name* | Not contents. VariableImporter's "Bind By Name" matches `pageItem.name` in the Layers panel, `TextFrame`s only. |
| `variables.removeAll()` throws | PARM error — the collection is read-only. `dataSets.removeAll()` **does** work. |
| **Binding cost scales with data set count** | Binding an object makes Illustrator reconcile that variable across *every* data set. Fewer data sets = faster everything. |

That last row is why the exporter now emits **two** data sets instead of five.

## A real bug this turned up

The shared-space path in `update_exhibits.py` wrote `spList[2]` and `spList[3]`
on a list holding only two elements. **Any two exhibits assigned the same space
number crashed the entire script.** Git history confirms the `> > ` marker never
once appeared in an exported CSV. That fix was kept.

## If someone picks this up again

Don't start with the import — that part works. Start with **binding**, because
everything failed downstream of it:

- Can the templates be bound *once*, by hand or by script, and saved so the
  binding survives? Bindings do live with the objects and survive re-imports.
  If binding is genuinely one-time per template, most of this becomes viable.
- Are the template's cell text objects actually *named* for their space codes
  in the Layers panel? If not, nothing binds and that is the first job.
- Solve cell overflow before anything else — it's the visible quality problem.

Until then: CSV, VariableImporter, and the manual steps in the playbook.
