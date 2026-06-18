# Research Summary: Why Automated Checks and Human Review Work Best Together

*This is an original summary written for portfolio purposes, synthesizing general, widely-known concepts in quality assurance rather than quoting or paraphrasing any single source.*

## Overview

There's a common assumption that automation and human review are competing approaches to quality assurance — that the goal is to automate as much as possible and only fall back on a person when the automation can't handle something. In practice, the more useful framing is that automated checks and human judgment are good at catching different *kinds* of problems, and a review process that relies on only one of them will have a predictable blind spot.

## What Automation Is Good At

Automated checks excel at anything that can be defined as a clear rule applied consistently across a large volume of data: Is this field blank? Does this date match an expected pattern? Does this value fall within an expected numeric range? Does this ID appear more than once? These checks don't get tired, don't skip rows, and run the same way on the 10,000th record as on the first. This makes automation the right tool for catching the bulk of mechanical, rule-based errors quickly.

## What Automation Struggles With

Automated checks are only as good as the rules they're built on, and many real-world data problems don't reduce to a clean rule. Whether two records with the same name represent the same person, whether an unusually high price is a typo or a genuine premium product, whether a missing value means "zero" or "not yet known" — these require context an automated script doesn't have access to. A rule built to catch one of these cases can also produce false positives, flagging legitimate records as problems simply because they happen to share a surface-level pattern with a real error.

## What Human Review Adds

A human reviewer brings exactly the contextual judgment that rule-based systems lack: recognizing that a flagged "duplicate" is actually two different customers who happen to share a name, or noticing that an entire batch of "formatting errors" actually originated from one specific data source that needs to be fixed at the root rather than corrected row-by-row. Human review is slower and doesn't scale to every row in a large dataset, which is exactly why it's most valuable when targeted at the cases automation flagged as uncertain, rather than spent re-checking everything the automated pass already handled confidently.

## The Practical Implication

The strongest review processes use automation to do a fast first pass across the entire dataset, surfacing a smaller set of flagged or low-confidence cases, and then apply human attention specifically to that smaller set. This division of labor — broad coverage from automation, contextual judgment from people — tends to catch more real problems with less total effort than either approach used alone.
