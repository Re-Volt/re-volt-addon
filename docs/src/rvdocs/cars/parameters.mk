---
title: Car Parameters
---

:insert toc

## Syntax

|| Comments ||

    Lines can be commented out with a semicolon: `;`.
    Example:

        ; This line will be completely ignored
        Weight 0.002   ; This comment is used to describe something

### Number Lists 

Wheel, axle, spring and pin indices can be defined using number lists.
Those lists support dashes to express number ranges and numbers separated by commas.
For example:

    WHEEL 0-3 {
    ...
    }

This would apply the keys and values encased by the brackets to wheels 0 to 3.

    WHEEL 0, 1 {
    ...
    }

This would apply to wheels 0 and 1.