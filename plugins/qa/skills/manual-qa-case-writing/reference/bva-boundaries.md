# BVA Boundaries per Input Type

## Contents
- Text inputs
- Numeric inputs
- Date inputs
- List / pagination
- File upload
- How to use

## How to use

For every input in the feature, emit boundary cases mechanically. No judgment — if the form has a text field, emit the empty case. If it has numeric, emit the zero case. Don't skip.

Each boundary becomes its own 6-field TC block in qa.md.

## Text inputs
Emit cases for:
- Empty string `""`
- Whitespace only `"   "`
- Single character `"a"`
- Maximum length minus 1
- Maximum length
- Maximum length plus 1
- Emoji `"😀👨‍👩‍👧"`
- RTL text (Arabic/Hebrew sample)
- Script payload (`<script>alert(1)</script>`, `'; DROP TABLE users; --`)

## Numeric inputs
Emit cases for:
- Zero `0`
- Negative `-1`
- Maximum int (`2^31 - 1` if 32-bit)
- Decimal `1.5`
- Locale separators (`1,000` vs `1.000` depending on locale)

## Date inputs
Emit cases for:
- Today (time of execution matters)
- Past date (1 year ago)
- Future date (1 year ahead)
- DST boundary (a date spanning daylight saving transition in user's locale)
- User TZ different from server TZ
- Feb 29 (leap year handling)

## List / pagination
If the feature has lists:
- 0 items (empty state)
- 1 item
- `page-size - 1`
- Exactly `page-size`
- `page-size + 1` (first pagination)
- `1000+` items (stress)

## File upload
If the feature accepts files:
- 0 bytes (empty file)
- Maximum allowed size
- Maximum + 1 (rejection)
- Wrong MIME type
- Corrupted file (valid extension, invalid content)
